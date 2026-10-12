# MARIB-01 — réseaux d'irrigation fossiles de Sabaʾ

> **Yémen : conflit armé actif, mines et engins non explosés. Travail à distance exclusivement.**
> Marib a été une ligne de front. Rien dans cette fiche n'autorise ni ne prépare une visite.

## Emprise

| | |
|---|---|
| Boîte | `15.30 45.15` → `15.50 45.45` |
| Dimensions | 32,2 km est-ouest × 22,1 km nord-sud = **712 km²** |
| Grille | 35 tuiles de 5 km (`marib-grille.kml`, `marib-grille.csv`) |
| Charge | ~4,7 h de balayage à 8 min/tuile |
| Dalle SRTM | `N15E045.hgt` |

```bash
cd outils
python3 prospection.py grille --bbox 15.30 45.15 15.50 45.45 \
    --tuile-km 5 --nom MARIB-01 \
    --kml ../zones/marib-grille.kml --csv ../zones/marib-grille.csv
```

## Pourquoi cette zone

Le barrage de Marib n'était pas un réservoir : c'était un **déviateur**. Il relevait les crues du
wadi Dhana et les distribuait, par deux écluses, dans deux oasis irriguées de part et d'autre du
wadi. Cette agriculture a déposé pendant un millénaire des limons qui ont surélevé les champs de
plusieurs mètres — un relief artificiel, à l'échelle décamétrique, **exactement la taille que voit
un MNT à 30 m**.

C'est donc l'une des rares zones du dossier où l'outil gratuit est adapté à la cible. Le réseau
principal est publié (fouilles du DAI) ; ce qui reste à cartographier, ce sont les ramifications
distales, les prises d'eau secondaires et l'extension maximale des périmètres irrigués.

## Ce qu'on cherche

| Cible | Signature | Échelle |
|---|---|---|
| Canaux de distribution fossiles | linéaments rectilignes à très faible pente, souvent en éventail depuis les écluses | 100 m – 5 km |
| Champs surélevés par le limon | damier de micro-plateaux, bords nets, surface lisse | 50 – 500 m |
| Prises d'eau et répartiteurs | élargissements ponctuels au nœud de deux linéaments | 20 – 100 m |
| Tells et habitats | buttes régulières, sommet aplani, souvent au contact du périmètre irrigué | 50 – 300 m |
| Murs de contour et digues | lignes épaisses suivant une courbe de niveau | 200 m – 2 km |

## Déjà répertorié — à exclure d'office

| Site | Coordonnées |
|---|---|
| Temple d'Awwām (Maḥram Bilqīs) | 15.40420, 45.35570 |
| Temple de Barʾān | 15.40315, 45.34318 |
| Barrage moderne | 15.39639, 45.24361 |
| Écluses de l'ancien barrage (approx. ±400 m) | ≈15.401, 45.238 |
| Ancienne ville de Marib (tell) | 15.42250, 45.33250 |

```bash
python3 prospection.py proximite --journal ../journal-de-prospection.csv --kml ../coordonnees.kml
```

## Imagerie : ce qui marche ici, et ce qui ne marche pas

**Les marques d'ombre ne marchent pas.** À la latitude de Marib, le soleil n'est jamais sous
**46,2°** à l'heure de passage des satellites héliosynchrones (minimum annuel, décembre et
janvier). Un talus de 50 cm y projette 48 cm d'ombre : invisible.

```
$ python3 soleil.py profil --lat 15.4042 --lon 45.3557 --annee 2026
  janvier     46.2°   145.7°    0.48 m   --
  juin        67.4°    66.1°    0.21 m   --
  décembre    46.2°   151.4°    0.48 m   --
```

**Ce qui marche, par ordre d'efficacité :**

1. **Ombrage multi-azimut du MNT** — vous choisissez l'éclairage, donc vous obtenez le soleil bas
   que le ciel ne vous donnera jamais ici :
   ```bash
   python3 relief.py --hgt N15E045.hgt --bbox 15.30 45.15 15.50 45.45 \
       --elevation 10 --azimuts 0,45,90,135 --z-facteur 2 \
       --sortie marib-relief.png --kml marib-relief.kml
   ```
   Les canaux fossiles sont majoritairement est-ouest (ils descendent du wadi) : **l'azimut 0 ou
   180 les effacera**. C'est pour cela qu'on en met quatre.
2. **Marques de sol** sur Sentinel-2 — les limons irrigués ont une signature spectrale distincte
   des sables environnants. Elles sont indifférentes à la hauteur du soleil.
3. **CORONA (1960-72)** — antérieur à l'agriculture mécanisée et au barrage moderne : la meilleure
   image de l'état fossile du réseau.

## Faux positifs propres à cette zone

1. **Périmètres irrigués modernes** — pivots circulaires et parcellaire rectangulaire net, autour
   du barrage de 1986. Le réseau antique est en éventail, le moderne en damier.
2. **Terrassements militaires** — berms, tranchées, positions de tir, nombreux depuis 2015. Bords
   trop nets, pas de patine, absents des images CORONA et des images d'avant 2014.
3. **Lits de wadi tressés** — les chenaux naturels imitent des canaux. Un canal antique suit une
   pente douce et régulière et ignore parfois la topographie locale ; un chenal naturel suit
   toujours la ligne de plus grande pente.
4. **Routes et pistes récentes** — rectilignes sur des kilomètres, indifférentes au relief.

## Critère d'arrêt

La zone est traitée quand les 35 tuiles sont à `fait` dans le CSV, avec pour chacune au moins deux
sources d'imagerie datées, et que chaque candidat retenu porte une explication alternative écrite
et un contrôle de doublon. Pas « quand on a trouvé quelque chose ».
