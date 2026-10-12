#!/usr/bin/env python3
"""Outils de prospection : grille de balayage et contrôle de doublon.

Deux opérations reviennent à chaque campagne, et les deux se font mal à la main.

1. `grille` — découper une zone en tuiles numérotées, pour balayer
   systématiquement au lieu de butiner. Produit un KML à ouvrir dans Google
   Earth et un CSV de suivi (une ligne par tuile, à cocher). Le balayage
   discipliné bat l'intuition : sans grille, on repasse trois fois sur le même
   wadi photogénique et jamais sur le quart nord-est.

2. `proximite` — avant de crier à la découverte, mesurer la distance au site
   connu le plus proche. La majorité des « trouvailles » sont des sites déjà
   publiés, vus sous un autre angle.

Usage
-----
    # Grille de 5 km sur la zone de Marib
    python3 prospection.py grille --bbox 15.30 45.15 15.50 45.45 \\
        --tuile-km 5 --nom MARIB-01 --kml marib-grille.kml --csv marib-grille.csv

    # Ce candidat est-il deja connu ?
    python3 prospection.py proximite --lat 15.4042 --lon 45.3557 --kml ../coordonnees.kml

    # Verifier tout un journal de prospection d'un coup
    python3 prospection.py proximite --journal ../journal-de-prospection.csv --kml ../coordonnees.kml

    python3 prospection.py autotest

Dépendances : aucune (bibliothèque standard Python 3.8+).
"""

import argparse
import csv
import math
import os
import sys
import xml.etree.ElementTree as ET

R_TERRE_KM = 6371.0088
KML_NS = "{http://www.opengis.net/kml/2.2}"


def distance_km(a, b):
    """Distance orthodromique entre deux (lat, lon) en degrés."""
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * R_TERRE_KM * math.asin(min(1.0, math.sqrt(h)))


def sites_du_kml(chemin):
    arbre = ET.parse(chemin)
    sites = []
    for pm in arbre.getroot().iter(KML_NS + "Placemark"):
        nom = pm.find(KML_NS + "name")
        coords = pm.find(f"{KML_NS}Point/{KML_NS}coordinates")
        if nom is None or coords is None or not (coords.text or "").strip():
            continue
        morceaux = coords.text.strip().split(",")
        sites.append(((nom.text or "").strip(), float(morceaux[1]), float(morceaux[0])))
    return sites


# --------------------------------------------------------------------------
# Grille de balayage
# --------------------------------------------------------------------------

def construire_grille(bbox, tuile_km):
    """bbox = (lat_min, lon_min, lat_max, lon_max). Renvoie la liste des tuiles."""
    lat_min, lon_min, lat_max, lon_max = bbox
    if lat_max <= lat_min or lon_max <= lon_min:
        raise ValueError("bbox invalide : attendu lat_min lon_min lat_max lon_max")

    pas_lat = tuile_km / 110.574  # degrés de latitude par km
    tuiles = []
    ligne = 0
    lat = lat_min
    while lat < lat_max - 1e-12:
        lat_haut = min(lat + pas_lat, lat_max)
        lat_milieu = (lat + lat_haut) / 2.0
        # un degré de longitude se raccourcit avec la latitude
        km_par_degre_lon = 111.320 * math.cos(math.radians(lat_milieu))
        pas_lon = tuile_km / max(1e-9, km_par_degre_lon)
        colonne = 0
        lon = lon_min
        while lon < lon_max - 1e-12:
            lon_droite = min(lon + pas_lon, lon_max)
            tuiles.append({
                "ligne": ligne,
                "colonne": colonne,
                "sud": lat,
                "ouest": lon,
                "nord": lat_haut,
                "est": lon_droite,
                "lat_centre": (lat + lat_haut) / 2.0,
                "lon_centre": (lon + lon_droite) / 2.0,
            })
            lon = lon_droite
            colonne += 1
        lat = lat_haut
        ligne += 1
    return tuiles


def _etiquette(tuile, prefixe):
    # ligne 0 en bas : on numerote du sud vers le nord, lettre pour la colonne
    lettre = chr(ord("A") + tuile["colonne"]) if tuile["colonne"] < 26 else f"C{tuile['colonne']}"
    return f"{prefixe}-{lettre}{tuile['ligne'] + 1}"


def ecrire_kml_grille(chemin, tuiles, prefixe, description):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{prefixe} — grille de balayage</name>
    <description><![CDATA[{description}]]></description>
    <Style id="tuile">
      <LineStyle><color>ff00aaff</color><width>2</width></LineStyle>
      <PolyStyle><fill>0</fill></PolyStyle>
    </Style>
""")
        for tuile in tuiles:
            nom = _etiquette(tuile, prefixe)
            s, o, n, e = tuile["sud"], tuile["ouest"], tuile["nord"], tuile["est"]
            f.write(f"""    <Placemark>
      <name>{nom}</name>
      <styleUrl>#tuile</styleUrl>
      <description>Centre {tuile['lat_centre']:.5f}, {tuile['lon_centre']:.5f}</description>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>
        {o:.6f},{s:.6f},0 {e:.6f},{s:.6f},0 {e:.6f},{n:.6f},0 {o:.6f},{n:.6f},0 {o:.6f},{s:.6f},0
      </coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>
""")
        f.write("  </Document>\n</kml>\n")


def ecrire_csv_grille(chemin, tuiles, prefixe):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tuile", "lat_centre", "lon_centre", "sud", "ouest", "nord", "est",
                    "statut", "date_balayage", "source_image", "date_image",
                    "candidats_trouves", "notes"])
        for tuile in tuiles:
            w.writerow([_etiquette(tuile, prefixe),
                        f"{tuile['lat_centre']:.5f}", f"{tuile['lon_centre']:.5f}",
                        f"{tuile['sud']:.5f}", f"{tuile['ouest']:.5f}",
                        f"{tuile['nord']:.5f}", f"{tuile['est']:.5f}",
                        "a_faire", "", "", "", "0", ""])


def cmd_grille(args):
    bbox = tuple(float(v) for v in args.bbox)
    tuiles = construire_grille(bbox, args.tuile_km)
    lat_moy = (bbox[0] + bbox[2]) / 2.0
    hauteur_km = (bbox[2] - bbox[0]) * 110.574
    largeur_km = (bbox[3] - bbox[1]) * 111.320 * math.cos(math.radians(lat_moy))
    surface = hauteur_km * largeur_km

    print(f"Zone        : {args.nom}")
    print(f"Emprise     : {bbox[0]:.4f} {bbox[1]:.4f} -> {bbox[2]:.4f} {bbox[3]:.4f}")
    print(f"Dimensions  : {largeur_km:.1f} km est-ouest x {hauteur_km:.1f} km nord-sud "
          f"= {surface:.0f} km2")
    print(f"Tuiles      : {len(tuiles)} de {args.tuile_km} km de cote")
    minutes = len(tuiles) * args.minutes_par_tuile
    print(f"Charge      : ~{minutes:.0f} min a {args.minutes_par_tuile} min/tuile "
          f"= {minutes / 60.0:.1f} h de balayage")

    description = (f"Grille de balayage {args.nom}. {len(tuiles)} tuiles de "
                   f"{args.tuile_km} km. Balayer en bandes, avec 20 % de "
                   "recouvrement a l'oeil. Cocher chaque tuile dans le CSV.")
    if args.kml:
        ecrire_kml_grille(args.kml, tuiles, args.nom, description)
        print(f"Écrit       : {args.kml}")
    if args.csv:
        ecrire_csv_grille(args.csv, tuiles, args.nom)
        print(f"Écrit       : {args.csv}")
    if not args.kml and not args.csv:
        for tuile in tuiles:
            print(f"  {_etiquette(tuile, args.nom)}  "
                  f"{tuile['lat_centre']:.5f}, {tuile['lon_centre']:.5f}")
    return 0


# --------------------------------------------------------------------------
# Contrôle de doublon
# --------------------------------------------------------------------------

def plus_proches(sites, point, combien=3):
    classes = sorted(((distance_km((lat, lon), point), nom, lat, lon)
                      for nom, lat, lon in sites), key=lambda t: t[0])
    return classes[:combien]


def _verdict(distance, seuil):
    if distance <= seuil:
        return "DÉJÀ RÉPERTORIÉ — c'est très probablement le même site"
    if distance <= seuil * 10:
        return "PROCHE d'un site connu — vérifier que ce n'est pas une annexe du même ensemble"
    return "AUCUN site connu à proximité dans ce KML"


def cmd_proximite(args):
    sites = sites_du_kml(args.kml)
    print(f"Référentiel : {args.kml} ({len(sites)} sites)")
    print(f"Seuil       : {args.seuil_km} km\n")

    points = []
    if args.journal:
        with open(args.journal, encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                try:
                    points.append((ligne.get("id") or "(sans id)",
                                   float(ligne["latitude"]), float(ligne["longitude"])))
                except (KeyError, TypeError, ValueError):
                    continue
        if not points:
            print("Aucune ligne exploitable dans le journal "
                  "(colonnes attendues : id, latitude, longitude).", file=sys.stderr)
            return 1
    elif args.lat is not None and args.lon is not None:
        points.append(("candidat", args.lat, args.lon))
    else:
        print("Fournissez --lat et --lon, ou --journal", file=sys.stderr)
        return 2

    for identifiant, lat, lon in points:
        print(f"{identifiant}  ({lat:.5f}, {lon:.5f})")
        for distance, nom, _, _ in plus_proches(sites, (lat, lon)):
            print(f"    {distance:9.2f} km  {nom}")
        d0 = plus_proches(sites, (lat, lon), 1)[0][0]
        print(f"    -> {_verdict(d0, args.seuil_km)}\n")

    print("Rappel : ce KML ne contient que les sites de ce dossier. Un candidat "
          "« sans site connu à proximité » doit encore être confronté à EAMENA "
          "et aux gazetteers nationaux avant toute conclusion.")
    return 0


# --------------------------------------------------------------------------
# Autotest
# --------------------------------------------------------------------------

def cmd_autotest(_args):
    echecs = 0

    def verifier(libelle, condition, detail=""):
        nonlocal echecs
        if not condition:
            echecs += 1
        print(f"  [{'OK  ' if condition else 'ECHEC'}] {libelle}{(' — ' + detail) if detail else ''}")

    print("Autotest de la prospection\n")

    # 1. Distance : un degré de latitude vaut ~111,2 km, partout.
    d = distance_km((0.0, 0.0), (1.0, 0.0))
    verifier("1° de latitude = 111,2 km", abs(d - 111.19) < 0.2, f"{d:.2f} km")
    d = distance_km((60.0, 0.0), (61.0, 0.0))
    verifier("1° de latitude identique a 60° N", abs(d - 111.19) < 0.3, f"{d:.2f} km")

    # 2. Un degré de longitude se raccourcit en cos(latitude).
    equateur = distance_km((0.0, 0.0), (0.0, 1.0))
    soixante = distance_km((60.0, 0.0), (60.0, 1.0))
    verifier("1° de longitude a 60° N = moitie de celui a l'equateur",
             abs(soixante / equateur - 0.5) < 0.01,
             f"{soixante:.2f} / {equateur:.2f} = {soixante / equateur:.3f}")

    # 3. Grille : les tuiles couvrent l'emprise sans trou ni chevauchement.
    bbox = (15.30, 45.15, 15.50, 45.45)
    tuiles = construire_grille(bbox, 5.0)
    verifier("la grille n'est pas vide", len(tuiles) > 0, f"{len(tuiles)} tuiles")
    verifier("la grille part du coin sud-ouest",
             abs(tuiles[0]["sud"] - bbox[0]) < 1e-9 and abs(tuiles[0]["ouest"] - bbox[1]) < 1e-9)
    verifier("la grille s'arrete au coin nord-est",
             abs(tuiles[-1]["nord"] - bbox[2]) < 1e-9 and abs(tuiles[-1]["est"] - bbox[3]) < 1e-9)
    lignes = {}
    for t in tuiles:
        lignes.setdefault(t["ligne"], []).append(t)
    continu = True
    for _, groupe in lignes.items():
        groupe.sort(key=lambda t: t["colonne"])
        for precedent, suivant in zip(groupe, groupe[1:]):
            if abs(precedent["est"] - suivant["ouest"]) > 1e-9:
                continu = False
    verifier("tuiles jointives en longitude", continu)

    # 4. La taille réelle d'une tuile correspond à ce qui est demandé.
    t = tuiles[0]
    cote_ns = distance_km((t["sud"], t["lon_centre"]), (t["nord"], t["lon_centre"]))
    cote_eo = distance_km((t["lat_centre"], t["ouest"]), (t["lat_centre"], t["est"]))
    verifier("cote nord-sud = 5 km", abs(cote_ns - 5.0) < 0.1, f"{cote_ns:.2f} km")
    verifier("cote est-ouest = 5 km", abs(cote_eo - 5.0) < 0.1, f"{cote_eo:.2f} km")

    # 5. Étiquettes uniques.
    etiquettes = [_etiquette(t, "Z") for t in tuiles]
    verifier("etiquettes uniques", len(set(etiquettes)) == len(etiquettes),
             f"{len(etiquettes)} tuiles, {len(set(etiquettes))} etiquettes")

    # 6. Proximité : un site confronté à lui-même donne zéro.
    kml = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "coordonnees.kml")
    if os.path.exists(kml):
        sites = sites_du_kml(kml)
        verifier("le KML de reference se lit", len(sites) > 30, f"{len(sites)} sites")
        nom, lat, lon = sites[0]
        d0 = plus_proches(sites, (lat, lon), 1)[0][0]
        verifier("distance d'un site a lui-meme = 0", d0 < 1e-6, f"{d0:.9f} km ({nom})")
        # Un point au milieu de l'ocean Pacifique n'est proche de rien.
        d_loin = plus_proches(sites, (-30.0, -140.0), 1)[0][0]
        verifier("un point tres eloigne est signale comme tel", d_loin > 5000,
                 f"{d_loin:.0f} km")
    else:
        print("  [SAUTE] tests sur coordonnees.kml (fichier absent)")

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

    p = sous.add_parser("grille", help="découper une zone en tuiles de balayage")
    p.add_argument("--bbox", nargs=4, required=True,
                   metavar=("LAT_MIN", "LON_MIN", "LAT_MAX", "LON_MAX"))
    p.add_argument("--tuile-km", type=float, default=5.0)
    p.add_argument("--nom", default="ZONE")
    p.add_argument("--kml")
    p.add_argument("--csv")
    p.add_argument("--minutes-par-tuile", type=float, default=8.0,
                   help="pour estimer la charge de travail (défaut 8)")
    p.set_defaults(fonction=cmd_grille)

    p = sous.add_parser("proximite", help="distance au site connu le plus proche")
    p.add_argument("--kml", required=True)
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--journal", help="CSV avec colonnes id, latitude, longitude")
    p.add_argument("--seuil-km", type=float, default=0.5,
                   help="en deçà, on considère que c'est le même site (défaut 0,5)")
    p.set_defaults(fonction=cmd_proximite)

    p = sous.add_parser("autotest", help="vérifie les calculs sur des cas connus")
    p.set_defaults(fonction=cmd_autotest)

    args = ap.parse_args(argv)
    return args.fonction(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # sortie tronquee par un `| head` : ce n'est pas une erreur
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
