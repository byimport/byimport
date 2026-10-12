#!/usr/bin/env python3
"""Géométrie solaire : trouver les fenêtres à soleil bas pour la prospection.

Pourquoi cet outil existe
-------------------------
Les marques d'ombre (micro-reliefs enterrés révélés par une ombre rasante) ne se
lisent que sur une image **acquise** à faible élévation solaire. Le curseur
d'ensoleillement de Google Earth n'y change rien : il éclaire le modèle de
terrain, pas l'image satellite. Il faut donc parcourir l'imagerie historique et
ne retenir que les dates où le soleil était bas.

Cet outil calcule élévation et azimut du soleil pour un lieu et une date, et
liste les fenêtres utiles sur une période. Il remplace une dépendance à un
service en ligne (SunCalc) par un calcul local reproductible.

Algorithme : NOAA Solar Calculator (précision ~0,1° sur la période 1900-2100),
suffisant pour choisir une image ; ce n'est pas de l'astrométrie de précision.

Usage
-----
    # Position du soleil à un instant précis (UTC)
    python3 soleil.py position --lat 15.4042 --lon 45.3557 --date 2026-01-15 --heure 07:00

    # Meilleures fenêtres d'ombre sur une année, pour un site du KML
    python3 soleil.py fenetres --site "Temple d'Awwam" --kml ../coordonnees.kml --annee 2026

    # Idem par coordonnées, en ne gardant que le soleil sous 25 degres
    python3 soleil.py fenetres --lat 18.255 --lon 53.6489 --annee 2026 --elevation-max 25

    # Profil mensuel : elevation du soleil a l'heure de passage typique (10h30 locale)
    python3 soleil.py profil --lat 26.7917 --lon 37.9528 --annee 2026

Dépendances : aucune (bibliothèque standard Python 3.8+).
"""

import argparse
import datetime as dt
import math
import sys
import xml.etree.ElementTree as ET

KML_NS = "{http://www.opengis.net/kml/2.2}"

# Heure locale de passage des satellites optiques héliosynchrones les plus
# utilisés en prospection (Sentinel-2 ~10h30, Landsat ~10h00-10h15, la plupart
# des images très haute résolution entre 10h et 11h30 solaires).
HEURE_PASSAGE_TYPIQUE = 10.5


# --------------------------------------------------------------------------
# Position solaire — NOAA Solar Calculator
# --------------------------------------------------------------------------

def _jour_julien(moment_utc):
    """Jour julien (avec fraction) pour un datetime UTC."""
    annee, mois = moment_utc.year, moment_utc.month
    jour = moment_utc.day
    if mois <= 2:
        annee -= 1
        mois += 12
    a = annee // 100
    b = 2 - a + a // 4
    jj = (math.floor(365.25 * (annee + 4716))
          + math.floor(30.6001 * (mois + 1))
          + jour + b - 1524.5)
    fraction = (moment_utc.hour + moment_utc.minute / 60
                + moment_utc.second / 3600) / 24
    return jj + fraction


def position_solaire(latitude, longitude, moment_utc):
    """Renvoie (elevation_deg, azimut_deg, declinaison_deg) pour un instant UTC.

    L'élévation est corrigée de la réfraction atmosphérique. L'azimut est compté
    depuis le nord, dans le sens des aiguilles d'une montre.
    """
    jj = _jour_julien(moment_utc)
    jc = (jj - 2451545.0) / 36525.0

    # Longitude et anomalie moyennes du Soleil
    long_moy = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360.0
    anom_moy = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    excentricite = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)

    anom_rad = math.radians(anom_moy)
    equation_centre = (math.sin(anom_rad) * (1.914602 - jc * (0.004817 + 0.000014 * jc))
                       + math.sin(2 * anom_rad) * (0.019993 - 0.000101 * jc)
                       + math.sin(3 * anom_rad) * 0.000289)

    long_vraie = long_moy + equation_centre
    long_apparente = (long_vraie - 0.00569
                      - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * jc)))

    obliquite_moy = 23.0 + (26.0 + (21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813))) / 60.0) / 60.0
    obliquite = obliquite_moy + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * jc))

    declinaison = math.degrees(math.asin(
        math.sin(math.radians(obliquite)) * math.sin(math.radians(long_apparente))))

    # Équation du temps (minutes)
    vary = math.tan(math.radians(obliquite / 2.0)) ** 2
    l0_rad = math.radians(long_moy)
    equation_temps = 4.0 * math.degrees(
        vary * math.sin(2 * l0_rad)
        - 2 * excentricite * math.sin(anom_rad)
        + 4 * excentricite * vary * math.sin(anom_rad) * math.cos(2 * l0_rad)
        - 0.5 * vary * vary * math.sin(4 * l0_rad)
        - 1.25 * excentricite * excentricite * math.sin(2 * anom_rad))

    minutes_utc = moment_utc.hour * 60 + moment_utc.minute + moment_utc.second / 60.0
    temps_solaire_vrai = (minutes_utc + equation_temps + 4.0 * longitude) % 1440.0
    angle_horaire = temps_solaire_vrai / 4.0 - 180.0
    if angle_horaire < -180.0:
        angle_horaire += 360.0

    lat_rad = math.radians(latitude)
    decl_rad = math.radians(declinaison)
    ha_rad = math.radians(angle_horaire)

    cos_zenith = (math.sin(lat_rad) * math.sin(decl_rad)
                  + math.cos(lat_rad) * math.cos(decl_rad) * math.cos(ha_rad))
    cos_zenith = max(-1.0, min(1.0, cos_zenith))
    zenith = math.degrees(math.acos(cos_zenith))
    elevation_brute = 90.0 - zenith

    # Réfraction atmosphérique (approximation NOAA)
    if elevation_brute > 85.0:
        refraction = 0.0
    elif elevation_brute > 5.0:
        te = math.tan(math.radians(elevation_brute))
        refraction = (58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5) / 3600.0
    elif elevation_brute > -0.575:
        refraction = (1735.0 + elevation_brute * (-518.2 + elevation_brute * (
            103.4 + elevation_brute * (-12.79 + elevation_brute * 0.711)))) / 3600.0
    else:
        refraction = (-20.772 / math.tan(math.radians(elevation_brute))) / 3600.0

    elevation = elevation_brute + refraction

    # Azimut depuis le nord, sens horaire
    if abs(math.cos(math.radians(zenith))) < 1e-9 or abs(math.cos(lat_rad)) < 1e-9:
        azimut = 180.0 if latitude > 0 else 0.0
    else:
        arg = ((math.sin(lat_rad) * math.cos(math.radians(zenith)) - math.sin(decl_rad))
               / (math.cos(lat_rad) * math.sin(math.radians(zenith))))
        arg = max(-1.0, min(1.0, arg))
        if angle_horaire > 0:
            azimut = (math.degrees(math.acos(arg)) + 180.0) % 360.0
        else:
            azimut = (540.0 - math.degrees(math.acos(arg))) % 360.0

    return elevation, azimut, declinaison


def longueur_ombre(hauteur_m, elevation_deg):
    """Longueur de l'ombre portée par un relief de `hauteur_m` mètres.

    C'est le chiffre qui décide si une structure enfouie est détectable : une
    banquette de 40 cm projette 2,3 m d'ombre à 10 degres de soleil (lisible a
    50 cm/pixel) et seulement 23 cm a 60 degres (invisible).
    """
    if elevation_deg <= 0.5:
        return float("inf")
    return hauteur_m / math.tan(math.radians(elevation_deg))


# --------------------------------------------------------------------------
# Lecture du KML pour retrouver un site par son nom
# --------------------------------------------------------------------------

def sites_du_kml(chemin):
    arbre = ET.parse(chemin)
    resultats = []
    for pm in arbre.getroot().iter(KML_NS + "Placemark"):
        nom_node = pm.find(KML_NS + "name")
        coords = pm.find(f"{KML_NS}Point/{KML_NS}coordinates")
        if nom_node is None or coords is None or not (coords.text or "").strip():
            continue
        morceaux = coords.text.strip().split(",")
        resultats.append(((nom_node.text or "").strip(), float(morceaux[1]), float(morceaux[0])))
    return resultats


def resoudre_site(args):
    """Renvoie (nom, lat, lon) depuis --lat/--lon ou --site + --kml."""
    if args.lat is not None and args.lon is not None:
        return ("%.4f, %.4f" % (args.lat, args.lon), args.lat, args.lon)
    if args.site:
        if not args.kml:
            print("--site exige --kml", file=sys.stderr)
            sys.exit(2)
        candidats = [s for s in sites_du_kml(args.kml)
                     if args.site.lower() in s[0].lower()]
        if not candidats:
            print(f"Aucun site du KML ne correspond a « {args.site} »", file=sys.stderr)
            sys.exit(1)
        if len(candidats) > 1:
            print("Plusieurs sites correspondent — précisez :", file=sys.stderr)
            for nom, _, _ in candidats:
                print(f"  - {nom}", file=sys.stderr)
            sys.exit(1)
        return candidats[0]
    print("Fournissez --lat et --lon, ou --site avec --kml", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Sous-commandes
# --------------------------------------------------------------------------

def cmd_position(args):
    nom, lat, lon = resoudre_site(args)
    date = dt.date.fromisoformat(args.date)
    heure, minute = (int(x) for x in args.heure.split(":"))
    moment = dt.datetime(date.year, date.month, date.day, heure, minute,
                         tzinfo=dt.timezone.utc)
    elevation, azimut, declinaison = position_solaire(lat, lon, moment)
    print(f"Site        : {nom}  ({lat:.5f}, {lon:.5f})")
    print(f"Instant     : {moment.isoformat()}")
    print(f"Élévation   : {elevation:7.2f}°")
    print(f"Azimut      : {azimut:7.2f}°  (depuis le nord, sens horaire)")
    print(f"Déclinaison : {declinaison:7.2f}°")
    if elevation <= 0:
        print("\nLe soleil est sous l'horizon : aucune imagerie optique.")
        return 0
    print("\nOmbre portée par un micro-relief :")
    for hauteur in (0.2, 0.5, 1.0, 2.0):
        print(f"  {hauteur:>4.1f} m de relief  ->  {longueur_ombre(hauteur, elevation):6.2f} m d'ombre")
    verdict = ("EXCELLENT pour les marques d'ombre" if elevation < 20
               else "BON" if elevation < 30
               else "MÉDIOCRE — ombres trop courtes" if elevation < 45
               else "INUTILISABLE pour les marques d'ombre")
    print(f"\nVerdict : {verdict}")
    return 0


def cmd_fenetres(args):
    nom, lat, lon = resoudre_site(args)
    print(f"Site           : {nom}  ({lat:.5f}, {lon:.5f})")
    print(f"Année          : {args.annee}")
    print(f"Seuil retenu   : élévation <= {args.elevation_max}° à l'heure de passage satellite")
    print(f"Heure utilisée : {args.heure_passage:.2f} h solaire locale (passage héliosynchrone typique)")
    print()

    # Heure UTC correspondant à l'heure solaire locale demandée
    decalage_h = lon / 15.0
    heure_utc = args.heure_passage - decalage_h

    lignes = []
    debut = dt.date(args.annee, 1, 1)
    for n in range(366):
        jour = debut + dt.timedelta(days=n)
        if jour.year != args.annee:
            break
        h = int(heure_utc) % 24
        m = int(round((heure_utc - int(heure_utc)) * 60)) % 60
        decalage_jour = -1 if heure_utc < 0 else (1 if heure_utc >= 24 else 0)
        moment = dt.datetime(jour.year, jour.month, jour.day, h, m,
                             tzinfo=dt.timezone.utc) + dt.timedelta(days=decalage_jour)
        elevation, azimut, _ = position_solaire(lat, lon, moment)
        lignes.append((jour, elevation, azimut))

    retenues = [l for l in lignes if l[1] <= args.elevation_max and l[1] > 0]
    if not retenues:
        meilleure = min(lignes, key=lambda l: l[1] if l[1] > 0 else 999)
        print(f"Aucune date sous {args.elevation_max}° à cette heure.")
        print(f"Le minimum annuel est {meilleure[1]:.1f}° le {meilleure[0].isoformat()}.")
        print("Relevez --elevation-max, ou visez une image de début de matinée "
              "(--heure-passage 8.0) si le catalogue en contient.")
        return 0

    # Regrouper en plages continues
    plages = []
    debut_plage = retenues[0]
    precedent = retenues[0]
    for courant in retenues[1:]:
        if (courant[0] - precedent[0]).days > 1:
            plages.append((debut_plage, precedent))
            debut_plage = courant
        precedent = courant
    plages.append((debut_plage, precedent))

    print("Fenêtres favorables (chercher des images acquises dans ces plages) :")
    for a, b in plages:
        jours = (b[0] - a[0]).days + 1
        elev_min = min(l[1] for l in retenues if a[0] <= l[0] <= b[0])
        print(f"  {a[0].isoformat()} -> {b[0].isoformat()}  ({jours:>3} jours, "
              f"élévation min {elev_min:.1f}°)")

    pire = min(retenues, key=lambda l: l[1])
    print(f"\nMeilleur jour  : {pire[0].isoformat()} — élévation {pire[1]:.1f}°, "
          f"azimut {pire[2]:.1f}°")
    print(f"Ombre attendue : {longueur_ombre(0.5, pire[1]):.2f} m pour 50 cm de relief")
    print("\nL'azimut indique la direction vers le soleil : les ombres tombent à "
          "l'opposé. Une structure linéaire parallèle aux ombres ne produit "
          "presque rien — comparez deux saisons aux azimuts différents.")
    return 0


def cmd_profil(args):
    nom, lat, lon = resoudre_site(args)
    decalage_h = lon / 15.0
    heure_utc = args.heure_passage - decalage_h
    print(f"Site : {nom}  ({lat:.5f}, {lon:.5f})")
    print(f"Élévation solaire à {args.heure_passage:.1f} h solaire locale, "
          f"le 15 de chaque mois de {args.annee}\n")
    print("  Mois        Élévation   Azimut   Ombre pour 50 cm   Lisibilité")
    print("  " + "-" * 64)
    noms_mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                 "août", "septembre", "octobre", "novembre", "décembre"]
    for mois in range(1, 13):
        h = int(heure_utc) % 24
        m = int(round((heure_utc - int(heure_utc)) * 60)) % 60
        decalage_jour = -1 if heure_utc < 0 else (1 if heure_utc >= 24 else 0)
        moment = dt.datetime(args.annee, mois, 15, h, m,
                             tzinfo=dt.timezone.utc) + dt.timedelta(days=decalage_jour)
        elevation, azimut, _ = position_solaire(lat, lon, moment)
        ombre = longueur_ombre(0.5, elevation)
        note = ("++" if elevation < 20 else "+" if elevation < 30
                else "-" if elevation < 45 else "--")
        print(f"  {noms_mois[mois - 1]:<12}{elevation:7.1f}°{azimut:9.1f}°"
              f"{ombre:14.2f} m   {note}")
    print("\n  ++ excellent   + bon   - médiocre   -- inutilisable")
    return 0


def cmd_autotest(_args):
    """Vérifie le calcul sur des cas dont la réponse est connue d'avance."""
    echecs = 0

    def verifier(libelle, obtenu, attendu, tolerance):
        nonlocal echecs
        ok = abs(obtenu - attendu) <= tolerance
        if not ok:
            echecs += 1
        marque = "OK  " if ok else "ECHEC"
        print(f"  [{marque}] {libelle}: obtenu {obtenu:.3f}, attendu {attendu:.3f} "
              f"(+/- {tolerance})")

    print("Autotest de la position solaire\n")

    # 1. Déclinaison aux solstices et aux équinoxes.
    _, _, d = position_solaire(0, 0, dt.datetime(2026, 6, 21, 12, tzinfo=dt.timezone.utc))
    verifier("déclinaison au solstice de juin", d, 23.44, 0.1)
    _, _, d = position_solaire(0, 0, dt.datetime(2026, 12, 21, 12, tzinfo=dt.timezone.utc))
    verifier("déclinaison au solstice de décembre", d, -23.44, 0.1)
    _, _, d = position_solaire(0, 0, dt.datetime(2026, 3, 20, 12, tzinfo=dt.timezone.utc))
    verifier("déclinaison à l'équinoxe de mars", d, 0.0, 0.4)

    # 2. Le soleil passe au zénith sur le tropique du Cancer au solstice de juin.
    #    Midi solaire au méridien de Greenwich, corrigé de l'équation du temps.
    meilleure = max(
        (position_solaire(23.436, 0, dt.datetime(2026, 6, 21, 12, mn, tzinfo=dt.timezone.utc))[0]
         for mn in range(0, 60)),
        default=0)
    verifier("élévation max sur le tropique du Cancer (21 juin)", meilleure, 90.0, 0.2)

    # 3. L'élévation au midi solaire vaut 90 - |latitude - déclinaison|.
    for lat in (15.4, 26.8, 31.8, -20.0):
        elev_max = max(
            position_solaire(lat, 0, dt.datetime(2026, 9, 23, 11, mn, tzinfo=dt.timezone.utc))[0]
            for mn in range(0, 60))
        _, _, decl = position_solaire(lat, 0, dt.datetime(2026, 9, 23, 12, tzinfo=dt.timezone.utc))
        verifier(f"midi solaire a {lat}° de latitude", elev_max,
                 90.0 - abs(lat - decl), 0.3)

    # 4. Symétrie : à l'équinoxe, le soleil se lève plein est partout.
    #    On cherche l'instant où l'élévation traverse zéro et on lit l'azimut.
    for lat in (15.4, 31.8):
        azimut_lever = None
        for minutes in range(0, 1440):
            moment = dt.datetime(2026, 3, 20, tzinfo=dt.timezone.utc) + dt.timedelta(minutes=minutes)
            e, a, _ = position_solaire(lat, 0, moment)
            if e > 0:
                azimut_lever = a
                break
        verifier(f"azimut au lever a l'équinoxe, lat {lat}°", azimut_lever, 90.0, 1.5)

    # 5. Longueur d'ombre : tangente de 45° = 1.
    verifier("ombre d'un relief de 1 m a 45°", longueur_ombre(1.0, 45.0), 1.0, 1e-9)

    print()
    if echecs:
        print(f"{echecs} verification(s) en echec.")
        return 1
    print("Toutes les verifications passent.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = ap.add_subparsers(dest="commande", required=True)

    def ajouter_lieu(p):
        p.add_argument("--lat", type=float, help="latitude décimale")
        p.add_argument("--lon", type=float, help="longitude décimale")
        p.add_argument("--site", help="nom (partiel) d'un repère du KML")
        p.add_argument("--kml", help="fichier KML où chercher --site")

    p = sous.add_parser("position", help="position du soleil à un instant donné (UTC)")
    ajouter_lieu(p)
    p.add_argument("--date", required=True, help="AAAA-MM-JJ")
    p.add_argument("--heure", default="10:00", help="HH:MM en UTC (défaut 10:00)")
    p.set_defaults(fonction=cmd_position)

    p = sous.add_parser("fenetres", help="plages de l'année à soleil bas")
    ajouter_lieu(p)
    p.add_argument("--annee", type=int, default=2026)
    p.add_argument("--elevation-max", type=float, default=30.0,
                   help="seuil d'élévation en degrés (défaut 30)")
    p.add_argument("--heure-passage", type=float, default=HEURE_PASSAGE_TYPIQUE,
                   help="heure solaire locale du passage satellite (défaut 10.5)")
    p.set_defaults(fonction=cmd_fenetres)

    p = sous.add_parser("profil", help="élévation mois par mois")
    ajouter_lieu(p)
    p.add_argument("--annee", type=int, default=2026)
    p.add_argument("--heure-passage", type=float, default=HEURE_PASSAGE_TYPIQUE)
    p.set_defaults(fonction=cmd_profil)

    p = sous.add_parser("autotest", help="vérifie le calcul sur des cas connus")
    p.set_defaults(fonction=cmd_autotest)

    args = ap.parse_args(argv)
    return args.fonction(args)


if __name__ == "__main__":
    sys.exit(main())
