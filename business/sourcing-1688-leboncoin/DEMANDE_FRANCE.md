# Étape 1 — Détecter les produits réellement recherchés en France

L'erreur n°1 du sourcing 1688 est de partir du produit ("c'est pas cher, je vais le vendre")
au lieu de partir de la demande. Méthode : on ne source **que** ce que les Français cherchent
déjà activement, avec un prix de marché observable sur Leboncoin.

## 1. Sources de données de demande (gratuites)

### Google Trends (geo=FR)
- URL : `https://trends.google.fr/trends/explore?geo=FR`
- Usage : valider qu'un produit est en **tendance montante ou stable**, repérer la saisonnalité
  (ex. "borne arcade" pic à Noël, "brumisateur" pic juin-août, "chauffage d'appoint" pic octobre).
- Règle : éviter les pics éphémères (gadgets viraux TikTok déjà retombés). Chercher des courbes
  en plateau ou en croissance sur 12-24 mois.
- Scriptable : l'endpoint non officiel de Trends est instable ; pour de la veille fiable, exporter
  le CSV depuis l'interface ou utiliser la bibliothèque `pytrends` en acceptant des ruptures.

### Google Keyword Planner (gratuit avec un compte Google Ads)
- Donne le **volume de recherche mensuel en France** par mot-clé, ex. "fauteuil oeuf",
  "station énergie portable", "kit karaoké enfant".
- C'est la donnée à reporter dans la colonne `volume_recherche_mensuel` de
  `scripts/produits_candidats.csv`.
- Seuil indicatif : < 1 000 recherches/mois en France = niche trop étroite pour ce modèle,
  sauf panier moyen élevé (> 80 €).

### Signaux Leboncoin (lecture manuelle, 15 min/produit)
Sur la recherche Leboncoin du produit candidat, relever :
1. **Nombre d'annonces actives** → mesure la concurrence (colonne `concurrence` du CSV, 1 = quasi
   personne, 5 = saturé).
2. **Prix médian des annonces** → c'est le `prix_marche_lbc_eur` du CSV. Prendre la médiane des
   annonces *en bon état / neuf*, pas le prix le plus haut.
3. **Ancienneté des annonces** : si les annonces datent de plusieurs mois, ça ne se vend pas.
   Si elles tournent en quelques jours (vérifier en revisitant à J+7), la demande est réelle.
4. **Recherches sauvegardées / compteur de vues** quand visible.

### Signaux complémentaires
- **Amazon.fr meilleures ventes** par catégorie : un produit dans le top 100 d'une catégorie a une
  demande prouvée ; Leboncoin devient intéressant quand on peut se placer 20-30 % sous le prix
  Amazon tout en gardant sa marge x3 (fréquent : Amazon vend via revendeurs qui ont déjà 2 marges).
- **AliExpress "best-sellers" expédiés de France** : ce qui se vend en B2C à l'unité depuis la
  Chine se vend encore mieux en local avec remise en main propre.
- **Facebook Marketplace** : mêmes signaux que Leboncoin, deuxième source de validation.

## 2. Profil du produit gagnant 1688 → Leboncoin

| Critère | Cible | Pourquoi |
|---|---|---|
| Prix de vente Leboncoin | 30 – 150 € | En dessous, la marge absolue ne paie pas le temps ; au-dessus, l'acheteur Leboncoin devient méfiant envers un vendeur sans historique |
| Poids unitaire | < 2 kg (idéal < 1 kg) | Le fret Chine→France et la livraison FR sont les 2 postes qui tuent la marge |
| Volume colis | Non encombrant | Le maritime groupé n'est rentable qu'à partir de cartons complets |
| Casse / SAV | Faible (pas de verre, pas d'électronique fragile) | Un retour = marge de 2-3 ventes effacée |
| Conformité | Pas de CE complexe | Voir liste d'exclusion dans `CADRE_LEGAL.md` |
| Différenciation | Produit "introuvable en magasin" ou 2-3× moins cher qu'en GMS | C'est la raison d'achat sur Leboncoin |
| Récurrence | Achetable en lot de 20-100 sans risque | Le modèle est la rotation, pas le coup unique |

## 3. Catégories qui cochent les cases (point de départ, à valider au cas par cas)

- **Maison / rangement** : organiseurs, étagères modulables, cintres spéciaux, boîtes sous vide.
- **Sport / plein air** : sangles de musculation, accessoires fitness, matériel de camping léger,
  accessoires vélo (hors casques — norme EN 1078).
- **Accessoires auto/moto** : organiseurs de coffre, housses, supports téléphone, tapis.
- **Animaux** : fontaines à eau, jouets robustes, harnais, tapis de léchage.
- **Bricolage léger** : organiseurs de visserie, lampes d'atelier sur batterie standard,
  outils à main spécialisés.
- **Décoration / éclairage LED basse tension** (USB ou 12 V avec alimentation déjà certifiée).

### Catégories à ÉVITER (risque conformité ou plateforme)

- Jouets et puériculture (norme EN 71, responsabilité pénale).
- Cosmétiques, compléments alimentaires, contact alimentaire (règlement CE 1935/2004).
- Électrique 230 V (CE + LVD réels exigés ; les certificats fournis par 1688 sont souvent faux).
- Contrefaçons et "inspirations" de marques — saisie douane + poursuites. Si le produit 1688
  arbore un logo ou ressemble à un produit de marque, on passe.
- Couteaux, lasers, e-cigarettes : restrictions Leboncoin et/ou légales.

## 4. Routine de veille hebdomadaire (1 h/semaine)

1. 20 min — Google Trends FR : passer en revue 5-10 requêtes candidates, noter les variations.
2. 20 min — Leboncoin : re-vérifier les annonces témoins repérées à J-7 (vendues ? toujours là ?).
3. 10 min — Mettre à jour `scripts/produits_candidats.csv` (volumes, prix médians, concurrence).
4. 10 min — Lancer `python3 scripts/score_produits.py scripts/produits_candidats.csv` et regarder
   si le classement change. Les 2-3 produits de tête sont les candidats à échantillonner
   (voir `SOURCING_1688.md`).
