# DHOFAR-01 — pistes caravanières autour de Shiṣr

Zone d'apprentissage avant tout : on y **refait la découverte de 1990-92 avec les données
d'aujourd'hui**. En 1990, l'équipe de Nicholas Clapp et Ranulph Fiennes, appuyée par Ron Blom
(JPL/NASA), a détecté sur Landsat, SPOT et le radar SIR-B des pistes caravanières effacées
convergeant vers un point du désert, puis a fouillé au sol et mis au jour le comptoir de Shiṣr.
Vous disposez gratuitement de bien mieux que ce qu'ils avaient.

Ce qu'il faut tenir en tête : **cette méthode a livré un vrai site 🟢, elle n'a pas livré Iram 🔴.**
L'équation Shiṣr = Ubar = Iram aux colonnes n'est pas admise par la recherche. Venez chercher des
pistes et des points d'eau, pas une cité mythique.

## Emprise

| | |
|---|---|
| Boîte | `18.10 53.45` → `18.45 53.90` |
| Dimensions | 47,6 km est-ouest × 38,7 km nord-sud = **1 841 km²** |
| Grille | 80 tuiles de 5 km |
| Charge | ~10,7 h de balayage |
| Dalles SRTM | `N18E053.hgt` |

```bash
cd outils
python3 prospection.py grille --bbox 18.10 53.45 18.45 53.90 \
    --tuile-km 5 --nom DHOFAR-01 --kml ../zones/dhofar-grille.kml --csv ../zones/dhofar-grille.csv
```

## Ce qu'on cherche

| Cible | Signature | Échelle |
|---|---|---|
| **Pistes caravanières fossiles** | faisceaux de linéaments parallèles, légèrement sinueux, convergeant vers un point d'eau | 1 – 50 km |
| **Effondrements karstiques** | dépressions circulaires, bords abrupts — ce sont les points d'eau, donc les aimants à sites | 20 – 200 m |
| **Cairns de jalonnement** | points clairs isolés sur les hauteurs, espacés régulièrement le long d'un itinéraire | 2 – 10 m |
| **Aires de campement** | concentrations de cercles de pierres, sol décapé | 20 – 100 m |
| **Contrastes de sabkha** | croûte saline moulant une structure enfouie | 10 – 500 m |

Le raisonnement qui a marché en 1990 et qui marche encore : **ne cherchez pas le site, cherchez ce
qui y mène.** Une piste est longue, donc visible sur une image basse résolution ; un site est petit.
Remontez les faisceaux jusqu'à leur convergence.

## Déjà répertorié — à exclure d'office

| Site | Coordonnées |
|---|---|
| Shiṣr (« Ubar ») | 18.25500, 53.64889 |

Hors boîte mais à connaître, sur la même route de l'encens : Sumhuram/Khor Rori (17.04170,
54.43560), Al-Balīd (17.00060, 54.14170), Wadi Dawkah (17.24670, 54.06110).

## Imagerie

```
$ python3 soleil.py profil --lat 18.2550 --lon 53.6489 --annee 2026
  décembre    43.5°   152.5°    0.53 m   -
  janvier     43.7°   147.1°    0.52 m   -
  juin        68.2°    72.7°    0.20 m   --
```

Encore une fois trop haut pour des marques d'ombre. Ici, l'ordre d'efficacité change :

1. **Landsat et Sentinel-2 en vue large, d'abord.** C'est contre-intuitif mais c'est la leçon de
   1990 : les pistes se voient **mieux** à basse résolution, parce que la haute résolution noie le
   faisceau dans le détail du sol. Commencez à 30 m de résolution, descendez ensuite.
2. **CORONA (1960-72)** — décisif ici : antérieur aux pistes 4×4, aux lignes sismiques et à
   l'exploration pétrolière qui ont depuis ravagé la lisibilité du désert.
3. **Ombrage MNT** pour les effondrements karstiques, qui sont de vrais objets topographiques :
   ```bash
   python3 relief.py --hgt N18E053.hgt --bbox 18.10 53.45 18.45 53.90 \
       --elevation 15 --azimuts 315,45,135,225 --sortie dhofar-relief.png --kml dhofar-relief.kml
   ```

## Faux positifs — la zone la plus piégeuse du dossier

1. **Lignes sismiques d'exploration pétrolière.** *La* cause de fausses découvertes dans le Rubʿ
   al-Khālī et ses marges. Grilles de lignes parfaitement droites, parfois sur des dizaines de
   kilomètres, se coupant à angle droit, d'espacement constant. Une piste caravanière ne fait jamais
   d'angle droit, ne garde jamais un espacement constant, et contourne les obstacles.
2. **Pistes 4×4 modernes** — multiples traces parallèles, mais sans patine, visibles seulement sur
   les images récentes et absentes de CORONA.
3. **Plateformes de forage et carrières** — rectangles décapés avec accès.
4. **Motifs dunaires** — les barkhanes et les cordons produisent des alignements réguliers à grande
   échelle, d'origine purement éolienne.
5. **Chenaux de wadi fossiles** — ramifiés en arbre, alors qu'un faisceau de pistes est en
   convergence, pas en arborescence.

**Test rapide** : si vos « voies » se coupent à 90° ou gardent un espacement constant sur plus de
2 km, ce sont des lignes sismiques. Vérifiez sur CORONA : si elles sont absentes avant 1972, c'est
réglé.

## Critère d'arrêt

80 tuiles à `fait`. Attendez-vous à ne rien trouver d'inédit : la zone a été ratissée par les
campagnes omanaises et le ministère du Patrimoine. L'objectif ici est de **savoir reconnaître une
piste fossile d'une ligne sismique**, compétence qui sert ensuite partout.
