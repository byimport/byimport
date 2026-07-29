#!/usr/bin/env python3
"""Teste statistiquement les « alignements » entre sites d'un fichier KML.

Pourquoi cet outil existe
-------------------------
Dans n'importe quel semis de points assez dense, un grand nombre de triplets
apparaissent « alignés » à quelques kilomètres près, par pur effet
combinatoire : le nombre de triplets croît en n^3. Trouver trois sites alignés
sur Google Earth n'est donc pas une découverte tant qu'on n'a pas montré qu'il y
en a *plus que le hasard n'en produit*.

Ce script compte les triplets alignés dans les données réelles, puis rejoue le
même comptage sur des milliers de semis aléatoires de même effectif, tirés dans
la même enveloppe géographique (avec pondération en cos(latitude) pour tirer
uniformément par unité de surface). Il renvoie un p-value empirique.

Lecture : si p > 0,05, l'alignement observé est du bruit.

Limite du modèle nul — à connaître avant d'interpréter
------------------------------------------------------
Le semis aléatoire est tiré *uniformément* dans l'enveloppe des données. Si vos
points réels sont **regroupés en grappes** (plusieurs monuments d'un même site,
plusieurs temples d'une même oasis), le modèle nul ne reproduit pas ce
regroupement : il sous-estime le hasard et fabrique un p-value artificiellement
bas. Deux points voisins paraissent en effet « alignés » avec n'importe quel
troisième point lointain.

Parade : augmenter --separation-min-km jusqu'à ce que les triplets ne puissent
plus reposer sur une grappe locale (150 km est un bon point de départ à l'échelle
du Proche-Orient), et comparer les deux passes. Si le signal disparaît quand on
sépare les points, il n'y avait pas de signal.

Usage
-----
    python3 test_alignements.py ../coordonnees.kml
    python3 test_alignements.py ../coordonnees.kml --tolerance-km 5 --simulations 2000
    python3 test_alignements.py ../coordonnees.kml --dossier "B. Saba" --montrer 15

Dépendances : aucune (bibliothèque standard Python 3.8+).
"""

import argparse
import math
import random
import sys
import xml.etree.ElementTree as ET

R_TERRE_KM = 6371.0088
KML_NS = "{http://www.opengis.net/kml/2.2}"


# --------------------------------------------------------------------------
# Géométrie sphérique
# --------------------------------------------------------------------------

def _rad(deg):
    return math.radians(deg)


def distance_angulaire(a, b):
    """Distance angulaire (radians) entre deux points (lat, lon) en degrés."""
    lat1, lon1 = _rad(a[0]), _rad(a[1])
    lat2, lon2 = _rad(b[0]), _rad(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * math.asin(min(1.0, math.sqrt(h)))


def cap_initial(a, b):
    """Azimut initial (radians) du grand cercle a -> b."""
    lat1, lon1 = _rad(a[0]), _rad(a[1])
    lat2, lon2 = _rad(b[0]), _rad(b[1])
    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    return math.atan2(y, x)


def ecart_perpendiculaire_km(depart, arrivee, point):
    """Écart perpendiculaire (cross-track) de `point` au grand cercle depart->arrivee.

    Renvoie (ecart_km, position_le_long_km). La position le long de l'arc sert à
    vérifier que le point est bien *entre* les deux autres, et non au-delà.
    """
    d13 = distance_angulaire(depart, point)
    if d13 == 0.0:
        return 0.0, 0.0
    theta13 = cap_initial(depart, point)
    theta12 = cap_initial(depart, arrivee)
    dxt = math.asin(max(-1.0, min(1.0, math.sin(d13) * math.sin(theta13 - theta12))))
    cos_dxt = math.cos(dxt)
    if abs(cos_dxt) < 1e-12:
        dat = 0.0
    else:
        ratio = math.cos(d13) / cos_dxt
        dat = math.acos(max(-1.0, min(1.0, ratio)))
    return abs(dxt) * R_TERRE_KM, dat * R_TERRE_KM


# --------------------------------------------------------------------------
# Comptage des alignements
# --------------------------------------------------------------------------

def compter_alignements(points, tolerance_km, separation_min_km, collecter=False):
    """Compte les triplets alignés. Un triplet (A, B, C) compte si C est entre A
    et B, et si son écart perpendiculaire au grand cercle AB est <= tolerance_km.
    """
    n = len(points)
    total = 0
    details = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = points[i], points[j]
            longueur_km = distance_angulaire(a, b) * R_TERRE_KM
            if longueur_km < separation_min_km:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                c = points[k]
                if (distance_angulaire(a, c) * R_TERRE_KM < separation_min_km
                        or distance_angulaire(b, c) * R_TERRE_KM < separation_min_km):
                    continue
                ecart_km, le_long_km = ecart_perpendiculaire_km(a, b, c)
                if le_long_km <= 0 or le_long_km >= longueur_km:
                    continue  # C n'est pas entre A et B
                if ecart_km <= tolerance_km:
                    total += 1
                    if collecter:
                        details.append((ecart_km, i, j, k, longueur_km))
    return total, details


# --------------------------------------------------------------------------
# Lecture KML
# --------------------------------------------------------------------------

def lire_kml(chemin, filtre_dossier=None):
    """Renvoie [(nom, lat, lon), ...]. `filtre_dossier` filtre sur le nom du
    dossier KML parent (correspondance partielle, insensible à la casse).
    """
    arbre = ET.parse(chemin)
    racine = arbre.getroot()
    resultats = []

    def nom_de(element):
        noeud = element.find(KML_NS + "name")
        return (noeud.text or "").strip() if noeud is not None else ""

    def parcourir(element, dossier_courant):
        for enfant in element:
            if enfant.tag == KML_NS + "Folder":
                parcourir(enfant, nom_de(enfant) or dossier_courant)
            elif enfant.tag == KML_NS + "Document":
                parcourir(enfant, dossier_courant)
            elif enfant.tag == KML_NS + "Placemark":
                if filtre_dossier and filtre_dossier.lower() not in dossier_courant.lower():
                    continue
                coords = enfant.find(f"{KML_NS}Point/{KML_NS}coordinates")
                if coords is None or not (coords.text or "").strip():
                    continue
                morceaux = coords.text.strip().split(",")
                lon, lat = float(morceaux[0]), float(morceaux[1])
                resultats.append((nom_de(enfant) or "(sans nom)", lat, lon))

    parcourir(racine, "")
    return resultats


# --------------------------------------------------------------------------
# Simulation de Monte-Carlo
# --------------------------------------------------------------------------

def tirer_semis_aleatoire(n, bornes, rng):
    """Tire n points uniformément *par unité de surface* dans l'enveloppe."""
    lat_min, lat_max, lon_min, lon_max = bornes
    s_min = math.sin(_rad(lat_min))
    s_max = math.sin(_rad(lat_max))
    points = []
    for _ in range(n):
        lat = math.degrees(math.asin(rng.uniform(s_min, s_max)))
        lon = rng.uniform(lon_min, lon_max)
        points.append((lat, lon))
    return points


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kml", help="fichier KML à analyser")
    ap.add_argument("--tolerance-km", type=float, default=5.0,
                    help="écart perpendiculaire maximal pour dire « aligné » (défaut : 5)")
    ap.add_argument("--separation-min-km", type=float, default=25.0,
                    help="distance minimale entre deux sites d'un triplet, pour éviter de "
                         "compter des sites voisins d'un même complexe (défaut : 25)")
    ap.add_argument("--simulations", type=int, default=1000,
                    help="nombre de semis aléatoires (défaut : 1000)")
    ap.add_argument("--dossier", default=None,
                    help="ne garder que les points d'un dossier KML dont le nom contient ceci")
    ap.add_argument("--montrer", type=int, default=10,
                    help="nombre de meilleurs triplets à afficher (défaut : 10)")
    ap.add_argument("--graine", type=int, default=20260729,
                    help="graine aléatoire, pour un résultat reproductible")
    args = ap.parse_args(argv)

    sites = lire_kml(args.kml, args.dossier)
    if len(sites) < 3:
        print("Moins de 3 points retenus : rien à tester.", file=sys.stderr)
        return 1

    points = [(lat, lon) for _, lat, lon in sites]
    noms = [nom for nom, _, _ in sites]

    print(f"Fichier      : {args.kml}")
    if args.dossier:
        print(f"Filtre       : dossier contenant « {args.dossier} »")
    print(f"Sites retenus: {len(sites)}")
    print(f"Tolérance    : {args.tolerance_km} km d'écart perpendiculaire")
    print(f"Séparation   : au moins {args.separation_min_km} km entre sites d'un triplet")
    print()

    observes, details = compter_alignements(
        points, args.tolerance_km, args.separation_min_km, collecter=True)
    print(f"Triplets alignés observés : {observes}")

    if details and args.montrer > 0:
        details.sort(key=lambda t: t[0])
        print(f"\nLes {min(args.montrer, len(details))} plus serrés :")
        for ecart_km, i, j, k, longueur_km in details[:args.montrer]:
            print(f"  {ecart_km:7.2f} km d'écart | {noms[i]} -- {noms[j]} "
                  f"(arc {longueur_km:.0f} km), point intermédiaire : {noms[k]}")

    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    bornes = (min(lats), max(lats), min(lons), max(lons))
    print(f"\nEnveloppe des tirages : lat {bornes[0]:.3f}..{bornes[1]:.3f}, "
          f"lon {bornes[2]:.3f}..{bornes[3]:.3f}")

    rng = random.Random(args.graine)
    au_moins_autant = 0
    somme = 0
    for _ in range(args.simulations):
        semis = tirer_semis_aleatoire(len(points), bornes, rng)
        compte, _ = compter_alignements(semis, args.tolerance_km, args.separation_min_km)
        somme += compte
        if compte >= observes:
            au_moins_autant += 1

    moyenne_hasard = somme / args.simulations
    p = (au_moins_autant + 1) / (args.simulations + 1)  # estimateur conservateur

    print(f"Simulations           : {args.simulations}")
    print(f"Moyenne au hasard     : {moyenne_hasard:.1f} triplets")
    print(f"p-value empirique     : {p:.4f}")
    print()
    if p > 0.05:
        print("VERDICT : p > 0,05. Les alignements observés sont compatibles avec le hasard.")
        print("          Aucun dessin intentionnel n'est démontré par ces points.")
    else:
        print("VERDICT : p <= 0,05. Il y a plus d'alignements que le hasard n'en produit")
        print("          dans cette enveloppe. Attention : ce n'est PAS une preuve d'intention.")
        print("          Vérifiez d'abord les causes banales — sites échelonnés le long d'une")
        print("          même route caravanière, d'un même wadi, d'une même côte ou d'un même")
        print("          piémont — qui alignent les points sans aucune géométrie sacrée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
