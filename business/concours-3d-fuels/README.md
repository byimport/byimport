# SERDP/ESTCP — 3D Surface Fuels & Vegetation Modeling Prize Challenge

Dossier de travail pour une candidature au concours du DoD (prix : 40 000 / 25 000 / 20 100 $).
**Ce dossier vit sous `business/` et n'a aucun lien avec le plugin Toprank.**

## Échéances (fuseau EDT)

| Étape | Date | Statut |
|---|---|---|
| Inscription portail (formulaire monday.com) | ouvert | **À FAIRE — action du candidat** |
| Soumission Phase 1 (prototype) | **20 juillet 2026 23:59** | en construction |
| Sélection demi-finalistes | 28 juillet 2026 | — |
| Soumission finale | 12 août 2026 23:59 | — |
| Demo Day (en personne, Floride) | 19 août 2026 | déplacement requis |

## Thèse stratégique (pourquoi on peut être compétitif)

Le concours s'appelle « **Surface Fuels & understory** ». Or l'outil de référence fourni,
FastFuels, est **fort sur la canopée et faible sous 2 m** — exactement la zone que le jury
valorise (critère « pertinence : focus carburants de surface et sous-étage »). Notre angle :

> **Reconstruire les voxels de combustible sous 2 m à partir du lidar discret NEON, les valider
> contre les relevés terrain NEON, puis les fusionner avec la canopée FastFuels.**

C'est défendable scientifiquement, généralisable (NEON couvre plusieurs écosystèmes US → critère
« généralité »), et 100 % réalisable sur ordinateur (pas de collecte terrain propre → critère
« coût raisonnable / scalabilité »).

## Données (toutes publiques et gratuites)

- **FastFuels SDK** (`fastfuels-core`, `fastfuels-sdk`) — canopée 3D voxelisée. Imposé/encouragé par le concours.
- **NEON lidar discret** `DP1.30003.001` — nuage de points aérien, pour reconstruire le sous-étage.
- **NEON structure de végétation ligneuse** `DP1.10098.001` — vérité terrain (position, hauteur, espèce) pour la validation.
- **NEON herbacé/couverture** (relevés de placettes) — validation du combustible de surface fin.
- Sites NEON candidats multi-écosystèmes : SOAP (forêt Sierra), TALL (pin du sud), JORN (désert arbustif) → démontre la généralité.

## Livrables exigés (Phase 1)

1. Données 3D géoréférencées, voxels 1 m³, propriétés de combustible — zone ≥ 100 m × 100 m (viser 1 km²).
2. Code Python d'ingestion/visualisation.
3. Cartes et visualisations 3D.
4. **Documentation de validation** (méthode, incertitudes, comparaison terrain).
5. Polygone GeoJSON projeté de la zone.

## Plan de sprint 16 jours

- **J1–3** : environnement + acquisition données (FastFuels sur 1 site, lidar + terrain NEON du même site).
- **J4–8** : pipeline sous-étage (filtrage sol, voxelisation 1 m³, dérivation charge de combustible fine).
- **J9–11** : fusion canopée FastFuels + sous-étage ; export formats concours (netcdf/geotiff/geojson).
- **J12–14** : validation quantitative contre terrain NEON (métriques + figures), rédaction doc.
- **J15–16** : visualisations 3D, relecture grille de jugement, soumission.

## Structure du dossier

```
src/      pipeline Python (voir src/README)
data/     caches locaux (non versionnés — .gitignore)
docs/     documentation de validation et méthodologie (livrable jury)
outputs/  produits générés (voxels, cartes) — non versionnés
```

## Honnêteté sur les limites

- Je (l'assistant) construis le code, la méthode et la documentation. **L'inscription, la
  soumission et le Demo Day sont vos actions** — je ne peux pas m'inscrire ni voyager à votre place.
- L'exécution lourde (téléchargement lidar de plusieurs Go, voxelisation) doit tourner sur
  **votre machine ou une instance cloud** ; ce conteneur est éphémère et non dimensionné pour ça.
- L'issue la plus probable reste de ne pas gagner : on affronte des labos de télédétection. Le pari
  vaut l'effort surtout pour l'apprentissage et l'exposition DoD (OTA/CRADA), pas comme revenu attendu.
