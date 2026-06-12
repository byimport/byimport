# Étape 5 — Automatisation : ce qui est scriptable, ce qui ne l'est pas

## 1. La vérité d'abord : publication sur Leboncoin

| Voie | Statut | Verdict |
|---|---|---|
| Bot/script qui publie via le site (Selenium, etc.) | Interdit par les CGU, détection DataDome très agressive | **À exclure** — bannissement du compte (et du compte pro associé), annonces supprimées |
| API publique Leboncoin pour particuliers | N'existe pas | — |
| **Compte PRO + import de catalogue** | Officiel | **La seule voie d'automatisation réelle.** Leboncoin PRO permet l'import d'annonces via flux/fichier, en direct ou via des agrégateurs-partenaires agréés (les outils multi-diffusion du marché de l'occasion et de l'e-commerce s'interfacent avec Leboncoin) |
| Publication manuelle assistée (annonce pré-générée à coller) | Conforme | Le compromis de départ : 3-4 min par annonce au lieu de 20 |

**Décision pour ce projet :** démarrer en publication manuelle assistée (volume faible — quelques
annonces par semaine), basculer sur l'import catalogue PRO quand le stock dépasse ~15 références
actives. Le reste de la chaîne est automatisé dès le jour 1.

## 2. Le pipeline automatisé

```
[Veille demande]      [Scoring]         [Marge]          [Annonces]        [Suivi]
 CSV candidats   →  score_produits.py →  marge_calc.py →  modèles ci-     →  tableur ventes
 (mise à jour        (classement auto)    (GO/NO-GO        dessous           (rotation, repricing)
  hebdo manuelle                           chiffré)        (génération
  ou pytrends)                                             par IA)
```

### 2.1 Veille demande (semi-auto)
- Tenir `scripts/produits_candidats.csv` à jour (routine hebdo de `DEMANDE_FRANCE.md` §4).
- Optionnel : script `pytrends` en cron hebdomadaire pour alimenter la colonne tendance —
  accepter que l'endpoint non officiel casse de temps en temps.

### 2.2 Scoring (auto)
```bash
python3 scripts/score_produits.py scripts/produits_candidats.csv
```
Classe les candidats par score combinant demande, multiplicateur de marge (calculé via le même
moteur que `marge_calc.py`), marge absolue, concurrence et risque de conformité. Les produits
dont le multiplicateur est < 2,5 ou le risque conformité ≥ 4 sont marqués NO-GO quoi qu'il arrive.

### 2.3 Calcul de marge et pricing (auto)
```bash
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --multiplicateur-cible 3   # → prix plancher
```
Donne le verdict GO/NO-GO et le prix de vente plancher pour atteindre le multiplicateur cible.

### 2.4 Génération des annonces (auto, publication manuelle)
Générer le texte avec un agent IA (Claude) à partir de ce gabarit — une annonce Leboncoin qui
convertit est concrète, locale et sans superlatifs creux :

```
Titre (≤ 50 car.) : [Produit] [attribut clé] — NEUF
Prix : [prix plancher arrondi au palier psychologique : 29, 39, 49…]

Corps :
- 1re ligne = bénéfice concret ("Range 24 paires de chaussures sur 60 cm de largeur")
- 3-5 puces specs (dimensions, matière, poids, contenu du lot)
- État : neuf, jamais utilisé [+ "disponible en plusieurs exemplaires" si stock]
- Remise en main propre à [ville] ou envoi Mondial Relay 48 h
- Mentions pro obligatoires (compte PRO) : garantie légale 2 ans, rétractation 14 j sur envoi
Photos : 3 minimum — produit reçu RÉEL sous lumière naturelle, jamais les rendus 1688
  (différence visible = litiges "non conforme" en série)
```

Règles de pricing :
- Démarrer au prix médian du marché constaté, pas en dessous : sur Leboncoin, le moins cher
  attire les négociateurs durs, pas les acheteurs rapides.
- Marges de négociation : afficher plancher + 10-15 %, refuser sous le plancher (le script donne
  le plancher exact).

### 2.5 Suivi et repricing (semi-auto)
Un tableur (ou CSV + script) avec : référence, stock restant, date de mise en ligne, vues,
contacts, prix actuel. Règles simples :
- Annonce > 10 jours sans contact → vérifier photos/titre, puis -10 %.
- Stock écoulé à > 70 % en < 2 semaines → +10 % sur les unités restantes et déclencher le réassort.
- Rotation complète du lot > 8 semaines → solder et abandonner la référence (règle de
  `MARGES_ET_COUTS.md` §3).

## 3. Ce que l'on n'automatise volontairement PAS

- **La validation d'échantillon** : aucun script ne voit qu'un produit sent le plastique ou
  casse au déballage. C'est le contrôle qualité qui protège la note vendeur.
- **Les réponses acheteurs** : des réponses types (dispo, dimensions, remise en main propre,
  envoi) préparées dans un fichier suffisent ; l'envoi reste humain — le ton "vrai vendeur"
  est un avantage concurrentiel sur Leboncoin.
- **La déclaration douanière** : toujours relire la valeur déclarée par l'agent (cf.
  `CADRE_LEGAL.md` §3).

## 4. Trajectoire d'industrialisation

| Palier | Déclencheur | Évolution |
|---|---|---|
| 0 → 5 ventes/sem | Démarrage | Pipeline ci-dessus, publication manuelle assistée |
| 5 → 20 ventes/sem | Stock ≥ 15 références | Compte PRO + import catalogue / agrégateur partenaire ; étiquettes d'envoi en lot |
| > 20 ventes/sem | Plafond temps perso | Multi-canal (Leboncoin PRO + Vinted pro + marketplace), prépa/expédition externalisée (3PL), passage en société si CA s'approche des plafonds micro |
