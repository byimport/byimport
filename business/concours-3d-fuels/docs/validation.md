# Méthodologie de validation (livrable jury — Phase 1)

Le concours exige que chaque soumission explique comment la précision est évaluée. La crédibilité
de la validation est un critère de jugement explicite. Voici le protocole que le pipeline met en œuvre.

## 1. Vérité terrain

Source : NEON **structure de végétation ligneuse** `DP1.10098.001` et relevés de couverture
herbacée, co-localisés avec les tuiles lidar `DP1.30003.001` du même site et de la même période.
Ces relevés donnent, par placette, la hauteur des individus, la couverture et la strate — donc une
référence indépendante pour le combustible de surface/sous-étage sous 2 m.

## 2. Métriques

- **Concordance de hauteur de strate** : distribution des hauteurs de retours voxelisés vs. hauteurs
  mesurées des individus < 2 m (test de Kolmogorov–Smirnov + biais médian).
- **Corrélation charge ↔ densité** : régression entre densité de retours par voxel (proxy) et
  charge/couverture terrain par placette → calibre le proxy en unités physiques, avec R² et RMSE.
- **Rétention spatiale** : validation croisée en laissant des placettes de côté (hold-out) pour
  mesurer la généralisation, pas seulement l'ajustement.

## 3. Généralité inter-écosystèmes

Rejouer le protocole sur ≥ 2 sites contrastés (ex. forêt de conifères SOAP, pin du sud TALL,
arbustaie désertique JORN) et rapporter les métriques par site. Le jury valorise une méthode qui
tient sur plusieurs écosystèmes, pas un sur-ajustement à un site.

## 4. Incertitudes déclarées

- Erreur de normalisation du sol (comparer approche moyenne-cellule vs. PDAL `filters.hag_nn`).
- Effet d'occlusion du lidar sous canopée dense (densité de retours au sol plus faible).
- Résolution/hétérogénéité sous 1 m non résolue par des voxels 1 m³ (limite déclarée honnêtement).

## 5. Reproductibilité

Toute la chaîne est scriptée (`src/`), les sources de données sont publiques et gratuites, les
paramètres (taille de voxel, plafond sous-étage, site) sont des arguments CLI. Un évaluateur peut
rejouer le pipeline de bout en bout — argument fort face à des soumissions non reproductibles.

> Statut : protocole défini. L'implémentation `src/validate.py` reste à écrire une fois les
> premières tuiles NEON téléchargées et voxelisées (sprint J12–14).
