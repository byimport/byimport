# Sourcing 1688 → Revente Leboncoin (France) — Système semi-automatisé

Objectif : identifier des produits **réellement recherchés en France**, les acheter en gros sur
**1688.com** (prix usine Chine), les revendre sur **Leboncoin** avec une marge nette cible de
**x2,5 à x3 sur le coût de revient complet**, en automatisant tout ce qui peut l'être légalement.

## Avertissement honnête (à lire avant tout)

1. **La publication 100 % automatisée sur Leboncoin n'existe pas pour un particulier.**
   Les bots de publication violent les CGU et entraînent un bannissement du compte (détection
   DataDome). La seule voie légitime d'automatisation de la publication est un **compte
   Leboncoin PRO** avec import de catalogue via un flux / un partenaire agréé (voir
   `AUTOMATISATION.md`). Tout le reste du pipeline (détection de la demande, scoring, calcul de
   marge, génération des annonces, repricing, suivi) est automatisable — et c'est ce que fait ce
   dossier.
2. **Acheter pour revendre = activité commerciale.** Le faire sous un profil "particulier" sans
   statut est du travail dissimulé (risque fiscal + URSSAF + DGCCRF). Le statut
   micro-entrepreneur coûte ~30 min à créer et règle le problème. Voir `CADRE_LEGAL.md`.
3. **L'importateur, c'est vous.** En important depuis la Chine pour revendre, vous portez la
   responsabilité de la conformité produit (CE, sécurité, REACH). Certaines catégories sont à
   exclure d'office (jouets, puériculture, cosmétiques, électrique 230 V non certifié).

## Le système en 5 étapes

| Étape | Quoi | Automatisation | Doc |
|---|---|---|---|
| 1. Demande | Détecter ce que les Français cherchent (Google Trends, Keyword Planner, signaux Leboncoin) | Semi-auto (veille scriptable) | `DEMANDE_FRANCE.md` |
| 2. Scoring | Croiser demande × marge × poids × concurrence × risque conformité | **Auto** — `scripts/score_produits.py` | ce README + scripts |
| 3. Sourcing | Acheter sur 1688 via agent (CSSBuy, Superbuy…), échantillon puis lot | Manuel (et c'est voulu : contrôle qualité) | `SOURCING_1688.md` |
| 4. Marge | Coût de revient complet → prix de vente plancher | **Auto** — `scripts/marge_calc.py` | `MARGES_ET_COUTS.md` |
| 5. Vente | Annonces optimisées Leboncoin, repricing, réponses types | Génération auto des annonces, publication manuelle (ou flux PRO) | `AUTOMATISATION.md` |

## Démarrage rapide

```bash
# 1. Calculer la marge d'un produit candidat
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 49

# 2. Scorer une liste de produits candidats (CSV fourni en exemple)
python3 scripts/score_produits.py scripts/produits_candidats.csv
```

## Règle d'or économique

Un produit n'est candidat que si **prix de vente Leboncoin ≥ 3 × coût de revient rendu France**
(achat + agent + fret + douane + TVA + livraison France + provision invendus). En dessous de x2,5,
les retours, la casse et le temps passé mangent la marge. Le détail du calcul est dans
`MARGES_ET_COUTS.md` ; le script `marge_calc.py` applique exactement cette règle.

## Contenu du dossier

- `DEMANDE_FRANCE.md` — détecter les produits recherchés en France (méthode + sources de données)
- `RECHERCHE_PRIX_ALIBABA.md` — prix d'achat réels constatés sur Alibaba pour le shortlist (juin 2026)
- `SOURCING_1688.md` — acheter sur 1688 depuis la France (agents, MOQ, échantillons, pièges)
- `MARGES_ET_COUTS.md` — structure de coûts complète et seuils de rentabilité
- `CADRE_LEGAL.md` — statut, TVA, douane, conformité CE, règles Leboncoin
- `AUTOMATISATION.md` — pipeline d'automatisation : ce qui est scriptable, ce qui ne l'est pas
- `scripts/marge_calc.py` — calculateur de marge en ligne de commande (stdlib uniquement)
- `scripts/score_produits.py` — classement automatique d'une liste de produits candidats
- `scripts/produits_candidats.csv` — modèle de fichier d'entrée avec exemples chiffrés
