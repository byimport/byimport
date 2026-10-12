# ALULA-01 / TAYMA-01 — mustatils, tombes à pendentif, enceintes

**C'est la zone à travailler en premier si vous voulez trouver quelque chose d'inédit.** Elle est la
seule du dossier où la prospection satellite a un taux de succès documenté et massif : plus d'un
millier de *mustatils* ont été repérés en Arabie du Nord-Ouest par lecture d'imagerie, puis
confirmés au sol et par survol (projets AAKSAU/AAKSA). La méthode y est prouvée, le terrain y est
loin d'être épuisé.

## Emprise

| | ALULA-01 | TAYMA-01 |
|---|---|---|
| Boîte | `26.55 37.80` → `26.90 38.10` | `27.52 38.40` → `27.75 38.70` |
| Dimensions | 29,8 × 38,7 km = **1 154 km²** | 29,6 × 25,4 km = **752 km²** |
| Grille | 80 tuiles de 4 km | 56 tuiles de 4 km |
| Charge | ~10,7 h | ~7,5 h |
| Dalles SRTM | `N26E037.hgt`, `N26E038.hgt` | `N27E038.hgt` |

```bash
cd outils
python3 prospection.py grille --bbox 26.55 37.80 26.90 38.10 \
    --tuile-km 4 --nom ALULA-01 --kml ../zones/alula-grille.kml --csv ../zones/alula-grille.csv
python3 prospection.py grille --bbox 27.52 38.40 27.75 38.70 \
    --tuile-km 4 --nom TAYMA-01 --kml ../zones/tayma-grille.kml --csv ../zones/tayma-grille.csv
```

Tuiles de 4 km et non 5 : les cibles sont petites et nombreuses, il faut descendre plus bas en
altitude d'œil, donc couvrir moins à la fois.

## Pourquoi ça marche ici alors que les ombres sont inutilisables

Le soleil descend à **35,9°** en décembre à al-ʿUlā : trop haut pour des marques d'ombre. Et
pourtant la méthode fonctionne — parce que **les cibles se détectent par leur géométrie en plan, pas
par leur relief**. Un mustatil est un rectangle de 20 à 600 m de long, délimité par deux murets
bas : ce qui le trahit, c'est la *forme*, un rectangle parfait au milieu d'une harra basaltique, pas
l'ombre de ses 50 cm de hauteur.

**C'est la distinction centrale de tout ce dossier :**

| Détection par | Dépend du soleil ? | Exemples |
|---|---|---|
| **Géométrie en plan** | non | mustatils, desert kites, enceintes, chapelets de puits, parcellaire |
| **Relief / ombre** | oui, et le soleil est trop haut ici | talus isolés, micro-reliefs sans forme reconnaissable |
| **Contraste de sol** | non | marques de sol, sabkhas, déflation |

Visez la première colonne, et les latitudes arabiques cessent d'être un handicap.

## Ce qu'on cherche

| Cible | Signature | Échelle | Où |
|---|---|---|---|
| **Mustatils** | rectangle très allongé, deux murets longs + plateforme à une extrémité | 20 – 600 m | plateaux de harra, bords de wadi |
| **Desert kites** | deux murs en entonnoir convergeant vers un enclos | 100 m – 3 km | pentes et couloirs de passage |
| **Tombes à pendentif** | cairn circulaire prolongé d'une « queue » de pierres | 10 – 100 m | lignes de crête, versants |
| **Champs de cairns** | semis de points clairs réguliers | 5 – 20 m l'unité | reliefs, interfluves |
| **Enceintes et « portes » (gates)** | rectangles de murets, souvent sur coulée basaltique | 50 – 500 m | harra |
| **Chapelets de puits (falaj)** | points alignés, espacement très régulier | 10 – 50 m d'intervalle | piémonts, vallées |

## Déjà répertorié — à exclure d'office

| Site | Coordonnées |
|---|---|
| Hégra / Madāʾin Ṣāliḥ | 26.79167, 37.95278 |
| Qaṣr al-Farīd | ≈26.800, 37.954 |
| Dadan (al-Khuraybah) | 26.62581, 37.92094 |
| Jabal Ikmah (approx. ±800 m) | ≈26.650, 37.890 |
| Taymāʾ | 27.62972, 38.54389 |

Toute la zone d'al-ʿUlā est en outre couverte par les campagnes RCU/AFALULA : **interrogez EAMENA et
l'Atlas du patrimoine saoudien avant de considérer un candidat comme inédit.** Le taux de doublon y
est élevé, et c'est une bonne nouvelle : cela veut dire que ce que vous voyez est réel.

## Imagerie

```
$ python3 soleil.py profil --lat 26.7917 --lon 37.9528 --annee 2026
  décembre    35.9°   155.7°    0.69 m   -
  janvier     36.4°   150.8°    0.68 m   -
  juin        69.2°    94.6°    0.19 m   --
```

1. **Google Earth à très haute résolution** — c'est l'outil principal ici, parce que la détection
   est géométrique. Balayez à ~1,5 km d'altitude d'œil.
2. **Imagerie d'hiver (novembre à février)** malgré tout : à 36° de soleil, les murets de 50 cm
   donnent un liseré d'ombre de 70 cm, assez pour souligner un contour déjà reconnu.
3. **Ombrage MNT** en appui, pour situer les cibles dans la topographie (crêtes pour les tombes à
   pendentif, plateaux pour les mustatils) :
   ```bash
   python3 relief.py --hgt N26E037.hgt --bbox 26.55 37.80 26.90 38.10 \
       --elevation 12 --sortie alula-relief.png --kml alula-relief.kml
   ```
4. **CORONA** pour les secteurs désormais urbanisés ou mis en culture autour d'al-ʿUlā.

## Faux positifs propres à cette zone

1. **Enclos à bétail modernes (*zarāʾib*)** — rectangles eux aussi, mais petits (10–40 m), proches
   d'une piste, souvent avec traces de troupeau rayonnantes et déjections visibles.
2. **Carrières et aires de stockage** — bords irréguliers, tas de déblais, accès carrossable.
3. **Aménagements touristiques récents** d'al-ʿUlā — très nombreux depuis 2019 : parkings, sentiers,
   plateformes. Vérifier systématiquement sur une image antérieure à 2018.
4. **Diaclases du basalte** — la harra se fracture en motifs polygonaux et linéaires réguliers que
   l'œil convertit volontiers en murs. Un mur a une épaisseur constante ; une diaclase non.
5. **Pare-feux et clôtures** — rectilignes sur des kilomètres.

## Critère d'arrêt

136 tuiles à `fait`. Comptez un rendement réaliste : sur ce type de terrain, les campagnes publiées
trouvent de l'ordre de quelques structures par centaine de km² en dehors des concentrations
connues. **Zéro trouvaille sur une tuile est un résultat**, à consigner comme tel.
