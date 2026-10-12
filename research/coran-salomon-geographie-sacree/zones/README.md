# Paquets de travail par zone

Le dossier principal donne la méthode. Ce répertoire la rend exécutable : cinq zones délimitées,
chacune avec son emprise, sa charge de travail chiffrée, ses cibles, ses faux positifs propres et
son critère d'arrêt.

## Choisir

| Zone | Surface | Tuiles | Charge | Chances de trouver | Risque de se perdre |
|---|---|---|---|---|---|
| [`al-ula-tayma.md`](al-ula-tayma.md) | 1 154 + 752 km² | 80 + 56 de 4 km | ~18 h | **Élevées** — c'est là que la prospection satellite a son meilleur taux de succès publié | Faible |
| [`marib.md`](marib.md) | 712 km² | 35 de 5 km | ~5 h | Moyennes — zone très étudiée, mais le réseau hydraulique fossile reste sous-cartographié | Faible |
| [`dhofar.md`](dhofar.md) | 1 841 km² | 80 de 5 km | ~11 h | Faibles en absolu, élevées en apprentissage — on y refait la découverte de 1990 avec les données d'aujourd'hui | **Élevé** : les lignes sismiques pétrolières y fabriquent des « voies antiques » à la pelle |
| [`jerusalem-bethleem.md`](jerusalem-bethleem.md) | 335 km² | 90 de 2 km | ~12 h | Nulles — tout est déjà cartographié | Nul — c'est un terrain d'entraînement, pas une chasse |

**Si vous débutez**, commencez par Jérusalem/Bethléem : vous y verrez des aqueducs antiques dont la
position est publiée, donc vous saurez si votre œil fonctionne. Puis passez à al-ʿUlā.

**Si vous voulez la meilleure chance de trouver quelque chose d'inédit**, allez directement à
al-ʿUlā/Taymāʾ.

## Utiliser

Chaque fiche donne la commande qui produit sa grille. Exemple, pour Marib :

```bash
cd outils
python3 prospection.py grille --bbox 15.30 45.15 15.50 45.45 \
    --tuile-km 5 --nom MARIB-01 \
    --kml ../zones/marib-grille.kml --csv ../zones/marib-grille.csv
```

La grille de Marib est déjà produite ici (`marib-grille.kml` et `marib-grille.csv`) comme exemple
de ce que vous obtenez : un calque de 35 tuiles numérotées à ouvrir dans Google Earth Pro, et un
tableau de suivi où chaque tuile passe de `a_faire` à `fait`.

Puis, pour chaque zone :

```bash
# Quand chercher : profil solaire mois par mois
python3 soleil.py profil --lat <lat> --lon <lon> --annee 2026

# Avec quoi voir le relief : ombrage multi-azimut d'une dalle SRTM
python3 relief.py --hgt N15E045.hgt --bbox <lat_min> <lon_min> <lat_max> <lon_max> \
    --elevation 12 --sortie zone.png --kml zone.kml

# Ce que vous trouvez est-il déjà connu ?
python3 prospection.py proximite --journal ../journal-de-prospection.csv --kml ../coordonnees.kml
```

## Règle commune à toutes les zones

Un candidat n'existe pas tant qu'il n'a pas : **deux sources d'imagerie indépendantes**, **une
explication alternative écrite** dans le journal, et **un contrôle de doublon** contre
`coordonnees.kml` puis contre EAMENA. Les trois, pas deux sur trois.

Et le rappel qui vaut partout : aucune fouille, aucune visite, et pas de publication des
coordonnées précises d'un site non répertorié — voir la section 5 du dossier principal.
