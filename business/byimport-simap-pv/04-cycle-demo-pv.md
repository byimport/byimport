# Cycle de démonstration — les 4 agents de bout en bout

> ⚠️ **MARCHÉ FICTIF — ILLUSTRATIF UNIQUEMENT.** Adjudicateur, références, dates,
> quantités et prix ci-dessous sont **inventés** pour montrer le rendu du
> système. Ne soumets jamais sur cette base. Remplace par un vrai avis simap.

Ce document montre exactement ce que tu obtiendras quand tu me fourniras un avis
réel (lien simap ou texte/PDF du cahier des charges).

---

## ÉTAPE 1 — Agent 1 : Fiche marché

| Champ | Valeur (fictive) |
|---|---|
| Adjudicateur | Commune de [Exemple-Ville], service des bâtiments |
| Réf. simap | XXXXXX (fictif) |
| Objet | Fourniture et pose d'une installation PV en toiture sur l'école primaire |
| Type de marché | Travaux (installation clé en main) |
| Puissance visée | ~200 kWc |
| Procédure | Sur invitation (estimée 300–500k travaux) |
| Critères d'attribution | Prix 40 % · Qualité technique 30 % · Délais 15 % · Références/SAV 15 % |
| Variantes | Autorisées |
| Délai de dépôt | [date fictive — ~6 semaines] |

**Lecture Agent 1 :** ✅ part module significative, ✅ variantes autorisées,
✅ prix pèse 40 %, ✅ délai compatible appro. → Marché retenu. ByImport intervient
comme **fournisseur de modules** de l'installateur-porteur.

## ÉTAPE 2 — Agent 2 : Sourcing module

| Spec | Proposition (fictive) |
|---|---|
| Module | Mono TOPCon 440 Wc, bifacial |
| Rendement | ~22,3 % |
| Certifications | IEC 61215, IEC 61730, CE, éligible Pronovo |
| Garantie | 15 ans produit / 87 % à 30 ans |
| Quantité | ~455 modules → 200 kWc |
| Coût rendu estimé | ~0,13 CHF/Wc (DDP, douane + TVA import récupérable) |
| Délai | ~5 semaines dès commande ferme |
| Fournisseurs | 2-3 sources (UE en priorité, Asie en second) — à verrouiller |

> Hypothèse de coût à remplacer par tes vrais devis fournisseurs + transitaire.

## ÉTAPE 3 — Agent 3 : Marge à deux étages

Calculé avec `modele_marge.py --puissance-wc 200000 --cout-rendu 0.13 --marge-pct 20 --prix-marche 0.25` :

```
Étage 1 — ByImport (fournisseur module)
  Coût rendu module         0.130 CHF/Wc   → CHF 26'000
  Prix vente → installateur 0.156 CHF/Wc   → CHF 31'200  (CA ByImport)
  >> Marge brute ByImport   CHF 5'200  (16.7 %)

Étage 2 — Compétitivité vs marché installateur
  Prix module marché CH     0.250 CHF/Wc   → CHF 50'000
  Économie offerte à l'installateur  CHF 18'800  (37.6 %)

  VERDICT : ✅ COMPÉTITIF
```

**Lecture :** sur ce marché fictif, ByImport encaisse **~5 200 CHF** de marge brute
sur le poste module tout en faisant **économiser ~18 800 CHF** à l'installateur vs
son sourcing habituel. Tout le monde y gagne, et l'installateur devient plus
agressif sur le prix global → meilleures chances d'adjudication.

> Sur des marchés plus gros ou répétés (contrats-cadres), l'effet volume rend la
> marge absolue bien plus intéressante.

## ÉTAPE 4 — Agent 4 : Proposition

Deux documents, à partir des modèles `templates/` :

1. **Offre de fourniture modules** (`offre-modules-byimport.md`) — ByImport → installateur :
   prix rendu, garanties, délais, économie chiffrée.
2. **Annexe technique** (`annexe-technique-modules.md`) — conformité IEC/CE/Pronovo +
   tableau de correspondance point par point au cahier des charges, à intégrer au
   dossier simap du porteur.

---

## Ce qu'il me faut pour rejouer ce cycle en RÉEL

- Un **avis simap PV réel** (lien, ou texte/PDF du cahier des charges), **et/ou**
- tes **vrais chiffres** : coût rendu module (CHF/Wc), prix marché installateur, marge cible.

Donne-moi l'un ou l'autre et je remplace chaque ligne fictive par du concret.
