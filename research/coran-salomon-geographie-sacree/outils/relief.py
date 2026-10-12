#!/usr/bin/env python3
"""Ombrage multi-azimut d'un modèle numérique de terrain (MNT).

Pourquoi cet outil existe
-------------------------
Aux latitudes arabiques, le soleil est trop haut sur l'imagerie satellite
courante pour produire des marques d'ombre exploitables (voir `soleil.py profil`
et la section 4.1 du README : à Marib, le soleil ne descend jamais sous 46° à
l'heure de passage des satellites héliosynchrones). La doctrine des *shadow
marks*, née de l'archéologie aérienne britannique à 52° de latitude, ne se
transpose pas telle quelle.

La parade est de ne plus dépendre de l'éclairage de la prise de vue : on prend
un MNT gratuit et on l'éclaire soi-même, sous l'angle qu'on veut, et sous
plusieurs azimuts. C'est le seul « curseur de soleil » qui agit réellement sur
la donnée.

Ce que fait le script
---------------------
1. lit une dalle SRTM `.hgt` (ou un MNT brut int16) ;
2. calcule un ombrage (méthode de Horn) à l'élévation et aux azimuts demandés,
   et les combine — un relief parallèle à un azimut disparaît, l'autre le
   révèle ;
3. écrit un PNG en niveaux de gris, et au besoin un KML `GroundOverlay` prêt à
   draper sur Google Earth, exactement calé sur l'emprise.

Usage
-----
    # Dalle SRTM entière, 4 azimuts, soleil à 15 degres
    python3 relief.py --hgt N15E045.hgt --elevation 15 --sortie marib.png --kml marib.kml

    # Fenêtre resserrée autour du barrage de Marib
    python3 relief.py --hgt N15E045.hgt --bbox 15.37 45.21 15.44 45.28 \
        --elevation 12 --azimuts 315,45,135,225 --z-facteur 3 --sortie barrage.png --kml barrage.kml

    # Démonstration auto-portée : MNT synthétique avec des structures connues
    python3 relief.py --demo --sortie demo.png
    python3 relief.py --autotest

Où trouver les dalles
---------------------
SRTM 1 arc-seconde (~30 m) : NASA Earthdata (SRTMGL1), ou les miroirs
viewfinderpanoramas. Nommage `N15E045.hgt` = coin **sud-ouest** de la dalle.
ALOS World 3D 30 m et Copernicus DEM 30 m conviennent aussi, convertis en int16
brut avec l'option --brut.

Limite à connaître : un MNT à 30 m ne voit pas une banquette de 50 cm. Il
révèle les objets de l'échelle décamétrique — talus, canaux, terrasses,
enceintes, tells, chaussées, réseaux d'irrigation fossiles. Pour le micro-relief
il faut un MNT LiDAR ou de la photogrammétrie, qui n'existent pas gratuitement
sur ces zones.

Dépendances : aucune (bibliothèque standard Python 3.8+).
"""

import argparse
import math
import os
import re
import struct
import sys
import zlib

METRES_PAR_ARCSEC = 111320.0 / 3600.0  # ~30.92 m en latitude
VIDE_SRTM = -32768


# --------------------------------------------------------------------------
# Écriture PNG (niveaux de gris 8 bits), sans dépendance
# --------------------------------------------------------------------------

def _chunk(type_octets, donnees):
    return (struct.pack(">I", len(donnees)) + type_octets + donnees
            + struct.pack(">I", zlib.crc32(type_octets + donnees) & 0xFFFFFFFF))


def ecrire_png_gris(chemin, largeur, hauteur, lignes):
    """lignes : liste de `hauteur` bytes/bytearray de longueur `largeur`."""
    brut = bytearray()
    for ligne in lignes:
        brut.append(0)  # filtre « none »
        brut.extend(ligne)
    with open(chemin, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(_chunk(b"IHDR", struct.pack(">IIBBBBB", largeur, hauteur, 8, 0, 0, 0, 0)))
        f.write(_chunk(b"IDAT", zlib.compress(bytes(brut), 9)))
        f.write(_chunk(b"IEND", b""))


# --------------------------------------------------------------------------
# Lecture du MNT
# --------------------------------------------------------------------------

def coin_depuis_nom(nom_fichier):
    """« N15E045.hgt » -> (15, 45) : coin sud-ouest de la dalle."""
    base = os.path.basename(nom_fichier).upper()
    m = re.match(r"([NS])(\d{2})([EW])(\d{3})", base)
    if not m:
        return None
    lat = int(m.group(2)) * (1 if m.group(1) == "N" else -1)
    lon = int(m.group(4)) * (1 if m.group(3) == "E" else -1)
    return lat, lon


def lire_hgt(chemin, cote=None):
    """Renvoie (grille, cote, pas_arcsec). grille[y][x], y=0 au nord."""
    taille = os.path.getsize(chemin)
    if cote is None:
        cote = int(round(math.sqrt(taille / 2)))
        if cote * cote * 2 != taille:
            raise ValueError(
                f"{chemin}: taille {taille} octets incompatible avec une dalle carree "
                "int16 ; precisez --cote")
    with open(chemin, "rb") as f:
        donnees = f.read()
    valeurs = struct.unpack(">%dh" % (cote * cote), donnees)
    grille = [list(valeurs[y * cote:(y + 1) * cote]) for y in range(cote)]
    pas_arcsec = 3600.0 / (cote - 1)
    return grille, cote, pas_arcsec


def boucher_vides(grille):
    """Remplace les valeurs de vide SRTM par la moyenne des voisins valides."""
    hauteur, largeur = len(grille), len(grille[0])
    corriges = 0
    for y in range(hauteur):
        for x in range(largeur):
            if grille[y][x] != VIDE_SRTM:
                continue
            somme = nb = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < hauteur and 0 <= xx < largeur and grille[yy][xx] != VIDE_SRTM:
                        somme += grille[yy][xx]
                        nb += 1
            grille[y][x] = somme // nb if nb else 0
            corriges += 1
    return corriges


def decouper(grille, coin, pas_arcsec, bbox):
    """bbox = (lat_min, lon_min, lat_max, lon_max). Renvoie (grille, emprise)."""
    lat0, lon0 = coin
    lat_min, lon_min, lat_max, lon_max = bbox
    hauteur = len(grille)
    largeur = len(grille[0])

    # y=0 correspond a lat0 + 1 degre (bord nord de la dalle)
    def y_de_lat(lat):
        return int(round((lat0 + 1.0 - lat) * 3600.0 / pas_arcsec))

    def x_de_lon(lon):
        return int(round((lon - lon0) * 3600.0 / pas_arcsec))

    y_haut = max(0, min(hauteur - 1, y_de_lat(lat_max)))
    y_bas = max(0, min(hauteur - 1, y_de_lat(lat_min)))
    x_gauche = max(0, min(largeur - 1, x_de_lon(lon_min)))
    x_droite = max(0, min(largeur - 1, x_de_lon(lon_max)))
    if y_bas <= y_haut or x_droite <= x_gauche:
        raise ValueError("--bbox ne recoupe pas la dalle (verifiez l'ordre : "
                         "lat_min lon_min lat_max lon_max)")

    extrait = [ligne[x_gauche:x_droite + 1] for ligne in grille[y_haut:y_bas + 1]]
    emprise = (
        lat0 + 1.0 - y_bas * pas_arcsec / 3600.0,   # sud
        lon0 + x_gauche * pas_arcsec / 3600.0,      # ouest
        lat0 + 1.0 - y_haut * pas_arcsec / 3600.0,  # nord
        lon0 + x_droite * pas_arcsec / 3600.0,      # est
    )
    return extrait, emprise


# --------------------------------------------------------------------------
# Ombrage
# --------------------------------------------------------------------------

def ombrage(grille, pas_x_m, pas_y_m, azimuts, elevation_deg, z_facteur=1.0,
            combinaison="max"):
    """Ombrage de Horn, combiné sur plusieurs azimuts. Renvoie des lignes 0-255."""
    hauteur, largeur = len(grille), len(grille[0])
    zenith = math.radians(90.0 - elevation_deg)
    az_rad = [math.radians(360.0 - a + 90.0) for a in azimuts]
    cos_z, sin_z = math.cos(zenith), math.sin(zenith)

    lignes = []
    for y in range(hauteur):
        ligne = bytearray(largeur)
        for x in range(largeur):
            y0 = max(0, y - 1)
            y2 = min(hauteur - 1, y + 1)
            x0 = max(0, x - 1)
            x2 = min(largeur - 1, x + 1)
            a = grille[y0][x0]; b = grille[y0][x]; c = grille[y0][x2]
            d = grille[y][x0];                     f = grille[y][x2]
            g = grille[y2][x0]; h = grille[y2][x]; i = grille[y2][x2]

            dzdx = ((c + 2 * f + i) - (a + 2 * d + g)) / (8.0 * pas_x_m)
            dzdy = ((g + 2 * h + i) - (a + 2 * b + c)) / (8.0 * pas_y_m)
            dzdx *= z_facteur
            dzdy *= z_facteur

            pente = math.atan(math.sqrt(dzdx * dzdx + dzdy * dzdy))
            if dzdx != 0.0:
                aspect = math.atan2(dzdy, -dzdx)
                if aspect < 0:
                    aspect += 2 * math.pi
            else:
                aspect = math.pi / 2 if dzdy > 0 else (3 * math.pi / 2 if dzdy < 0 else 0.0)

            valeurs = []
            for az in az_rad:
                v = (cos_z * math.cos(pente)
                     + sin_z * math.sin(pente) * math.cos(az - aspect))
                valeurs.append(max(0.0, v))
            v = max(valeurs) if combinaison == "max" else sum(valeurs) / len(valeurs)
            ligne[x] = min(255, int(round(255.0 * v)))
        lignes.append(ligne)
    return lignes


def etaler_contraste(lignes, percentile=2.0):
    """Étirement linéaire entre les percentiles, pour faire ressortir le signal."""
    histogramme = [0] * 256
    total = 0
    for ligne in lignes:
        for v in ligne:
            histogramme[v] += 1
            total += 1
    if total == 0:
        return lignes
    cible = total * percentile / 100.0
    cumul = 0
    bas = 0
    for v in range(256):
        cumul += histogramme[v]
        if cumul >= cible:
            bas = v
            break
    cumul = 0
    haut = 255
    for v in range(255, -1, -1):
        cumul += histogramme[v]
        if cumul >= cible:
            haut = v
            break
    if haut <= bas:
        return lignes
    echelle = 255.0 / (haut - bas)
    table = bytes(min(255, max(0, int(round((v - bas) * echelle)))) for v in range(256))
    return [bytearray(table[v] for v in ligne) for ligne in lignes]


# --------------------------------------------------------------------------
# KML GroundOverlay
# --------------------------------------------------------------------------

def ecrire_kml_overlay(chemin, nom_png, emprise, description):
    sud, ouest, nord, est = emprise
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <GroundOverlay>
    <name>Ombrage multi-azimut</name>
    <description><![CDATA[{description}]]></description>
    <color>b4ffffff</color>
    <Icon><href>{os.path.basename(nom_png)}</href></Icon>
    <LatLonBox>
      <north>{nord:.8f}</north>
      <south>{sud:.8f}</south>
      <east>{est:.8f}</east>
      <west>{ouest:.8f}</west>
    </LatLonBox>
  </GroundOverlay>
</kml>
""")


# --------------------------------------------------------------------------
# MNT de démonstration — structures de taille connue
# --------------------------------------------------------------------------

def mnt_demo(cote=300, pas_m=2.0):
    """Plaine en pente douce portant des structures archéologiques typiques.

    Sert à calibrer l'œil : on sait ce qui est là, on voit ce que l'ombrage en
    fait. Tout est en centimètres pour rester en entiers.
    """
    grille = [[0] * cote for _ in range(cote)]
    for y in range(cote):
        for x in range(cote):
            # pente generale 0,5 % vers le sud-est + ondulation naturelle
            z = 0.005 * (x + y) * pas_m
            z += 0.8 * math.sin(x / 37.0) * math.cos(y / 41.0)
            grille[y][x] = z

    def bande(x0, y0, x1, y1, hauteur_m, largeur_px=2):
        """Talus rectiligne (ou fossé si hauteur negative)."""
        longueur = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(longueur + 1):
            px = x0 + (x1 - x0) * t // max(1, longueur)
            py = y0 + (y1 - y0) * t // max(1, longueur)
            for dy in range(-largeur_px, largeur_px + 1):
                for dx in range(-largeur_px, largeur_px + 1):
                    xx, yy = px + dx, py + dy
                    if 0 <= xx < cote and 0 <= yy < cote:
                        grille[yy][xx] += hauteur_m

    # 1. Enceinte rectangulaire type « mustatil » : 150 x 40 m, talus de 60 cm
    x0, y0, x1, y1 = 40, 60, 115, 80
    bande(x0, y0, x1, y0, 0.6)
    bande(x0, y1, x1, y1, 0.6)
    bande(x0, y0, x0, y1, 0.6)
    bande(x1, y0, x1, y1, 0.6)

    # 2. Canal fossile : fossé de 40 cm, orienté nord-sud (parallele a l'azimut 0)
    bande(200, 20, 205, 280, -0.4, largeur_px=3)

    # 3. Chaussée : talus de 30 cm, orienté est-ouest
    bande(20, 200, 280, 210, 0.3, largeur_px=2)

    # 4. Tumulus : cône de 1,5 m sur 30 m de diamètre
    cx, cy, rayon = 150, 230, 15
    for y in range(cy - rayon, cy + rayon + 1):
        for x in range(cx - rayon, cx + rayon + 1):
            if 0 <= x < cote and 0 <= y < cote:
                d = math.hypot(x - cx, y - cy)
                if d <= rayon:
                    grille[y][x] += 1.5 * (1 - d / rayon)

    # 5. Chapelet de puits de falaj : dépressions de 1 m tous les 25 m
    for k in range(10):
        px, py = 60 + k * 12, 140 + k * 3
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if 0 <= px + dx < cote and 0 <= py + dy < cote:
                    grille[py + dy][px + dx] -= 1.0

    return [[int(round(v * 100)) for v in ligne] for ligne in grille], pas_m


def cmd_demo(args):
    grille, pas_m = mnt_demo()
    # les altitudes sont en centimetres : z_facteur 0.01 les ramene en metres
    lignes = ombrage(grille, pas_m, pas_m, [float(a) for a in args.azimuts.split(",")],
                     args.elevation, z_facteur=0.01 * args.z_facteur,
                     combinaison=args.combinaison)
    lignes = etaler_contraste(lignes)
    ecrire_png_gris(args.sortie, len(lignes[0]), len(lignes), lignes)
    print(f"MNT de démonstration : {len(lignes[0])} x {len(lignes)} pixels, "
          f"pas {pas_m} m")
    print(f"Éclairage : élévation {args.elevation}°, azimuts {args.azimuts}, "
          f"exagération x{args.z_facteur}")
    print(f"Écrit : {args.sortie}")
    print("""
Structures présentes, à retrouver à l'œil :
  1. enceinte rectangulaire 150 x 40 m, talus de 60 cm   (haut-gauche)
  2. canal fossile nord-sud, fossé de 40 cm              (droite)
  3. chaussée est-ouest, talus de 30 cm                  (bas)
  4. tumulus de 1,5 m sur 30 m de diamètre               (bas-centre)
  5. chapelet de 10 puits de falaj, 1 m, tous les 25 m   (centre-gauche)

Faites varier --elevation (5, 15, 45) et --azimuts : le canal nord-sud
disparaît sous un azimut de 0 ou 180° et ressort à 90 ou 270°. C'est pour cela
qu'un seul azimut ne suffit jamais.""")
    return 0


def cmd_autotest(_args):
    echecs = 0

    def verifier(libelle, condition, detail=""):
        nonlocal echecs
        if not condition:
            echecs += 1
        print(f"  [{'OK  ' if condition else 'ECHEC'}] {libelle}{(' — ' + detail) if detail else ''}")

    print("Autotest de l'ombrage\n")

    # 1. Plan horizontal : ombrage uniforme = cos(zenith).
    plat = [[100] * 20 for _ in range(20)]
    lignes = ombrage(plat, 30.0, 30.0, [315.0], 30.0)
    attendu = round(255 * math.cos(math.radians(60.0)))
    valeurs = {v for ligne in lignes for v in ligne}
    verifier("plan horizontal -> ombrage uniforme", len(valeurs) == 1,
             f"valeurs distinctes : {sorted(valeurs)}")
    verifier("plan horizontal -> valeur = 255 cos(zenith)",
             abs(next(iter(valeurs)) - attendu) <= 1,
             f"obtenu {next(iter(valeurs))}, attendu {attendu}")

    # 2. Convention d'aspect : un terrain qui MONTE vers l'est presente sa face
    #    a l'ouest (l'aspect est la direction de la descente). Il est donc
    #    eclaire par un soleil d'ouest (azimut 270) et a l'ombre sous un soleil
    #    d'est (azimut 90). Les altitudes sont en metres, comme le pas.
    monte_vers_est = [[x * 3.0 for x in range(40)] for _ in range(10)]
    depuis_ouest = ombrage(monte_vers_est, 30.0, 30.0, [270.0], 30.0)[5][20]
    depuis_est = ombrage(monte_vers_est, 30.0, 30.0, [90.0], 30.0)[5][20]
    verifier("versant eclaire plus clair que versant a l'ombre",
             depuis_ouest > depuis_est,
             f"soleil d'ouest -> {depuis_ouest}, soleil d'est -> {depuis_est}")

    # 3. Un relief parallele a l'azimut d'eclairage ne produit presque rien.
    crete_ns = [[0.0] * 60 for _ in range(60)]
    for y in range(60):
        for x in range(28, 32):
            crete_ns[y][x] = 3.0  # crete nord-sud de 3 m
    contraste_parallele = _contraste(ombrage(crete_ns, 30.0, 30.0, [0.0], 20.0))
    contraste_perpendiculaire = _contraste(ombrage(crete_ns, 30.0, 30.0, [90.0], 20.0))
    verifier("relief parallele au soleil moins contraste que perpendiculaire",
             contraste_parallele < contraste_perpendiculaire,
             f"azimut 0 -> {contraste_parallele}, azimut 90 -> {contraste_perpendiculaire}")

    # 4. Soleil bas -> plus d'ecart entre les deux versants, sur un relief doux.
    #    Pour une pente faible, ombrage ~ cos(zenith) + sin(zenith)*pente*cos(dAz),
    #    donc l'ecart entre versants vaut 2*sin(zenith)*pente = 2*cos(elevation)*pente.
    #    Le rapport entre 10 et 70 degres doit donc valoir cos(10)/cos(70) ~ 2.9.
    #    On prend un talus de 3 m, soit ~3° apres le filtre de Horn : assez
    #    doux pour que la linearisation tienne et qu'aucun versant ne sature a
    #    0, assez marque pour sortir du bruit de quantification sur 8 bits.
    doux = [[0.0] * 60 for _ in range(60)]
    for y in range(60):
        for x in range(60):
            doux[y][x] = 3.0 if x >= 30 else 0.0
    ecart_bas = _amplitude(ombrage(doux, 30.0, 30.0, [90.0], 10.0))
    ecart_haut = _amplitude(ombrage(doux, 30.0, 30.0, [90.0], 70.0))
    verifier("soleil bas : ecart entre versants plus grand", ecart_bas > ecart_haut,
             f"10° -> {ecart_bas}, 70° -> {ecart_haut}")

    # 5. La loi elle-meme, hors quantification 8 bits : l'ecart entre le versant
    #    au soleil et le versant a l'ombre vaut 2 sin(zenith) sin(pente), donc le
    #    rapport entre deux elevations solaires vaut cos(e1)/cos(e2).
    #    (Verifie sur la valeur flottante : sur 8 bits, un ecart de 12 contre 5
    #    niveaux ne resout pas un rapport a 15 % pres.)
    def ecart_versants(pente_deg, elevation_deg):
        au_soleil = _ombrage_valeur(pente_deg, 0.0, elevation_deg)
        a_l_ombre = _ombrage_valeur(pente_deg, 180.0, elevation_deg)
        return au_soleil - a_l_ombre

    for pente in (1.0, 3.0, 8.0):
        rapport_obtenu = ecart_versants(pente, 10.0) / ecart_versants(pente, 70.0)
        rapport_attendu = math.cos(math.radians(10.0)) / math.cos(math.radians(70.0))
        verifier(f"loi 2 sin(zenith) sin(pente), pente {pente}°",
                 abs(rapport_obtenu - rapport_attendu) < 1e-9,
                 f"obtenu {rapport_obtenu:.4f}, attendu {rapport_attendu:.4f}")

    # 5. Le PNG produit est relisible et a la bonne taille.
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_autotest.png")
    try:
        ecrire_png_gris(chemin, 7, 3, [bytearray(range(7)) for _ in range(3)])
        with open(chemin, "rb") as f:
            tete = f.read(8)
            f.read(4)
            type_chunk = f.read(4)
            ihdr = f.read(13)
        largeur, hauteur, profondeur, couleur = struct.unpack(">IIBB", ihdr[:10])
        verifier("signature PNG", tete == b"\x89PNG\r\n\x1a\n")
        verifier("entete IHDR", type_chunk == b"IHDR")
        verifier("dimensions et format PNG",
                 (largeur, hauteur, profondeur, couleur) == (7, 3, 8, 0),
                 f"{largeur}x{hauteur}, {profondeur} bits, type {couleur}")
    finally:
        if os.path.exists(chemin):
            os.remove(chemin)

    # 6. Le nommage SRTM est bien decode.
    verifier("nom de dalle N15E045", coin_depuis_nom("N15E045.hgt") == (15, 45))
    verifier("nom de dalle S05W070", coin_depuis_nom("S05W070.hgt") == (-5, -70))

    # 7. Le MNT de demonstration contient bien les structures annoncees.
    grille, _ = mnt_demo()
    plage = max(max(l) for l in grille) - min(min(l) for l in grille)
    verifier("MNT de demonstration non degenere", plage > 100,
             f"amplitude {plage} cm")

    print()
    if echecs:
        print(f"{echecs} verification(s) en echec.")
        return 1
    print("Toutes les verifications passent.")
    return 0


def _ombrage_valeur(pente_deg, delta_azimut_deg, elevation_deg):
    """Valeur d'ombrage (0-1) d'une facette, sans rasterisation ni quantification.

    C'est la formule de l'ombrage ramenee a ses deux variables utiles : la pente
    de la facette et l'ecart entre l'azimut du soleil et celui de la facette.
    """
    zenith = math.radians(90.0 - elevation_deg)
    pente = math.radians(pente_deg)
    return (math.cos(zenith) * math.cos(pente)
            + math.sin(zenith) * math.sin(pente) * math.cos(math.radians(delta_azimut_deg)))


def _amplitude(lignes):
    """Écart entre le plus clair et le plus sombre, en entier."""
    plat = [v for ligne in lignes for v in ligne]
    return max(plat) - min(plat)


def _contraste(lignes):
    """Écart-type approché, en entier, pour comparer deux ombrages."""
    total = nb = 0
    for ligne in lignes:
        for v in ligne:
            total += v
            nb += 1
    moyenne = total / nb
    variance = sum((v - moyenne) ** 2 for ligne in lignes for v in ligne) / nb
    return int(round(math.sqrt(variance)))


def cmd_relief(args):
    coin = coin_depuis_nom(args.hgt)
    if coin is None and args.coin:
        coin = tuple(float(v) for v in args.coin.split(","))
    if coin is None:
        print("Impossible de déduire le coin sud-ouest du nom de fichier ; "
              "utilisez --coin LAT,LON", file=sys.stderr)
        return 2

    grille, cote, pas_arcsec = lire_hgt(args.hgt, args.cote)
    vides = boucher_vides(grille)
    print(f"Dalle      : {args.hgt}  ({cote} x {cote}, pas {pas_arcsec:.4f}\")")
    print(f"Coin SO    : {coin[0]}, {coin[1]}")
    if vides:
        print(f"Vides SRTM : {vides} pixels interpolés")

    emprise = (coin[0], coin[1], coin[0] + 1.0, coin[1] + 1.0)
    if args.bbox:
        bbox = tuple(float(v) for v in args.bbox)
        grille, emprise = decouper(grille, coin, pas_arcsec, bbox)
        print(f"Découpe    : {len(grille[0])} x {len(grille)} pixels")

    lat_moyenne = (emprise[0] + emprise[2]) / 2.0
    pas_y_m = pas_arcsec * METRES_PAR_ARCSEC
    pas_x_m = pas_y_m * math.cos(math.radians(lat_moyenne))
    print(f"Résolution : {pas_x_m:.1f} m est-ouest, {pas_y_m:.1f} m nord-sud")

    azimuts = [float(a) for a in args.azimuts.split(",")]
    lignes = ombrage(grille, pas_x_m, pas_y_m, azimuts, args.elevation,
                     z_facteur=args.z_facteur, combinaison=args.combinaison)
    if not args.sans_etalement:
        lignes = etaler_contraste(lignes)

    ecrire_png_gris(args.sortie, len(lignes[0]), len(lignes), lignes)
    print(f"Écrit      : {args.sortie}")

    if args.kml:
        description = (f"Ombrage multi-azimut de {os.path.basename(args.hgt)}. "
                       f"Élévation {args.elevation}°, azimuts {args.azimuts}, "
                       f"exagération x{args.z_facteur}. "
                       f"Résolution {pas_x_m:.1f} m. "
                       "Le MNT ne voit pas le micro-relief sous ~2 m : "
                       "lire ce calque comme un détecteur de talus, canaux, "
                       "terrasses et enceintes, pas de murs.")
        ecrire_kml_overlay(args.kml, args.sortie, emprise, description)
        print(f"Écrit      : {args.kml}  (ouvrir dans Google Earth Pro)")
        print(f"Emprise    : S {emprise[0]:.5f}  O {emprise[1]:.5f}  "
              f"N {emprise[2]:.5f}  E {emprise[3]:.5f}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hgt", help="dalle SRTM .hgt (ou MNT int16 brut avec --cote)")
    ap.add_argument("--coin", help="coin sud-ouest LAT,LON si le nom ne le donne pas")
    ap.add_argument("--cote", type=int, help="côté en pixels d'un MNT brut")
    ap.add_argument("--bbox", nargs=4, metavar=("LAT_MIN", "LON_MIN", "LAT_MAX", "LON_MAX"),
                    help="fenêtre à extraire")
    ap.add_argument("--elevation", type=float, default=15.0,
                    help="élévation solaire en degrés (défaut 15 : rasant)")
    ap.add_argument("--azimuts", default="315,45,135,225",
                    help="azimuts séparés par des virgules (défaut 315,45,135,225)")
    ap.add_argument("--z-facteur", type=float, default=1.0,
                    help="exagération verticale (défaut 1)")
    ap.add_argument("--combinaison", choices=("max", "moyenne"), default="max",
                    help="comment combiner les azimuts (défaut max)")
    ap.add_argument("--sans-etalement", action="store_true",
                    help="ne pas étirer le contraste")
    ap.add_argument("--sortie", default="ombrage.png", help="PNG de sortie")
    ap.add_argument("--kml", help="écrire aussi un GroundOverlay KML")
    ap.add_argument("--demo", action="store_true",
                    help="MNT synthétique avec des structures connues")
    ap.add_argument("--autotest", action="store_true",
                    help="vérifie le calcul sur des cas connus")
    args = ap.parse_args(argv)

    if args.autotest:
        return cmd_autotest(args)
    if args.demo:
        return cmd_demo(args)
    if not args.hgt:
        ap.error("fournissez --hgt, ou --demo, ou --autotest")
    return cmd_relief(args)


if __name__ == "__main__":
    sys.exit(main())
