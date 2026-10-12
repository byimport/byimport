# BETHLEEM-01 — terrain d'entraînement, hydraulique antique

**Vous ne trouverez rien d'inédit ici, et c'est exactement l'intérêt.** Tout est fouillé, publié,
cartographié. Vous pouvez donc vérifier si votre œil fonctionne : repérez une structure, puis
confrontez-la à la littérature. Si vous ne retrouvez pas des aqueducs dont la position est connue au
mètre près, vous n'êtes pas prêt à chercher des mustatils inconnus au Nefoud.

Faites cette zone **avant** al-ʿUlā. Deux heures ici économisent dix heures d'illusions ailleurs.

## Emprise

| | |
|---|---|
| Boîte | `31.64 35.08` → `31.80 35.28` |
| Dimensions | 18,9 km est-ouest × 17,7 km nord-sud = **335 km²** |
| Grille | 90 tuiles de 2 km |
| Charge | ~12 h (zone dense, tuiles petites) |
| Dalle SRTM | `N31E035.hgt` |

```bash
cd outils
python3 prospection.py grille --bbox 31.64 35.08 31.80 35.28 \
    --tuile-km 2 --nom BETHLEEM-01 \
    --kml ../zones/bethleem-grille.kml --csv ../zones/bethleem-grille.csv
```

Tuiles de 2 km : terrain urbanisé et très dense, il faut travailler bas.

## Ce qu'on cherche — et qu'on sait déjà trouver

| Cible | Signature | Vérifiable ? |
|---|---|---|
| **Aqueducs** (al-ʿArrūb, al-Biyār, Wādī al-Bayyār) | linéament à pente constante et très faible, suivant les courbes de niveau, traversant les vallées par des coudes | oui, tracés publiés |
| **Bassins de Salomon** | trois grands réservoirs rectangulaires en enfilade | oui, 31.68900, 35.16982 |
| **Terrasses agricoles anciennes** | gradins épousant le versant, murets de pierre sèche | oui |
| **Citernes et birkets** | dépressions rectangulaires maçonnées | oui |
| **Tours de vigne (*qusur*)** | petites constructions circulaires isolées dans les terrasses | oui |

L'aqueduc est l'objet-école parfait : **un canal antique a une pente constante de l'ordre de 0,1 à
0,3 %.** Il ne descend donc jamais tout droit dans la pente, il la contourne. C'est le critère qui
distingue, partout dans le monde, un canal d'un chenal naturel. Entraînez-vous à le voir ici, où la
réponse est connue.

## Déjà répertorié — à exclure d'office

| Site | Coordonnées |
|---|---|
| Bassins de Salomon (Birak Sulaymān) | 31.68900, 35.16982 |
| Dôme du Rocher (hors boîte, au nord) | 31.77802, 35.23543 |
| Mosquée al-Aqṣā | 31.77617, 35.23583 |
| Mur occidental | 31.77675, 35.23444 |
| Grotte de Sédécias | 31.78262, 35.23085 |

## Imagerie : la meilleure configuration solaire du dossier

```
$ python3 soleil.py profil --lat 31.6890 --lon 35.1698 --annee 2026
  décembre    31.4°   156.9°    0.82 m   -
  janvier     32.1°   152.4°    0.80 m   -
  juin        68.3°   107.0°    0.20 m   --
```

31,4° en décembre, c'est le minimum le plus bas des cinq zones — et à 8 h solaire locale en
novembre, on descend à **16,4°**, soit 1,69 m d'ombre pour 50 cm de relief :

```bash
python3 soleil.py fenetres --lat 31.6890 --lon 35.1698 --annee 2026 \
    --elevation-max 25 --heure-passage 8.0
```

C'est aussi la seule zone du dossier où les **marques de végétation** fonctionnent vraiment : climat
méditerranéen, couvert végétal saisonnier, donc stress hydrique différentiel au-dessus des
structures enterrées. Regardez les images de fin de saison sèche (août-septembre) sur Sentinel-2.

## Faux positifs propres à cette zone

1. **Infrastructures contemporaines** — la zone est densément bâtie et équipée : conduites, routes,
   murs de soutènement récents, barrière de séparation. Tout linéament droit y est moderne jusqu'à
   preuve du contraire.
2. **Terrasses modernes** — l'agriculture en terrasses est toujours pratiquée ; l'ancienneté ne se
   lit pas sur l'image.
3. **Carrières** anciennes et modernes, très nombreuses.
4. **Chemins creux** — ils imitent un canal, mais descendent la pente au lieu de la suivre.

## L'exercice, concrètement

1. Balayez sans documentation ouverte, et marquez tout linéament à pente faible et constante.
2. Mesurez la pente de chaque candidat avec l'outil chemin de Google Earth Pro (profil
   d'élévation) : gardez ceux entre 0,05 et 0,5 %.
3. **Seulement ensuite**, confrontez à la littérature sur les aqueducs de Jérusalem.
4. Comptez vos faux positifs et vos ratés. Ce chiffre est votre taux d'erreur personnel — c'est la
   donnée la plus utile que cette zone puisse vous donner, et vous l'emporterez partout ailleurs.

## Critère d'arrêt

Quand votre taux de faux positifs sur deux tuiles consécutives tombe sous 50 %. Pas avant.
