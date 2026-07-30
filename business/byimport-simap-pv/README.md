# ByImport — Système courtage marchés publics suisses (Photovoltaïque)

Kit opérationnel pour positionner **ByImport** comme fournisseur de modules
photovoltaïques sur les marchés publics suisses (simap.ch), via un **partenaire
installateur suisse porteur** (montage « Voie C »).

> ⚠️ **Statut du kit.** C'est un système *prêt à exécuter*, pas un marché en
> cours. Il ne contient **aucun appel d'offres réel** : les avis simap doivent
> être récupérés par toi (plateforme en JavaScript, non scrapable de façon
> fiable). Le cycle de démonstration (`04-cycle-demo-pv.md`) utilise un marché
> **illustratif explicitement étiqueté** — chiffres et adjudicateur fictifs.

---

## Le contexte ByImport (décisions actées)

| Paramètre | Décision |
|---|---|
| Famille produit prioritaire | **Panneaux solaires / PV** (les véhicules sont écartés au démarrage — voir pourquoi dans `01-veille-simap.md`) |
| Zone | Toute la Suisse |
| Statut ByImport | Société **étrangère**, import déjà actif avec fournisseurs |
| Montage suisse | **Voie C** — partenaire installateur suisse porte l'offre ; ByImport fournit les modules en amont (grossiste) |
| Blocage à lever | Pas encore de partenaire suisse → `02-recherche-partenaire.md` |
| TVA CH | À vérifier (assujettissement probable dès vente/import en CH) |

## Pourquoi ce modèle (résumé)

La plupart des marchés PV publics sont des **installations clé en main (travaux)**,
où la pose est la prestation caractéristique et ne peut pas être sous-traitée.
ByImport ne sera donc **pas le soumissionnaire** mais le **fournisseur de modules**
de l'installateur qui soumissionne. Avantage de ByImport = **coût module plus bas**.
C'est un modèle grossiste-revendeur propre, invisible pour l'adjudicateur, et qui
résout d'un coup le blocage « jeune société sans références » (c'est le partenaire
qui apporte aptitude et références).

## Les 4 agents

| Agent | Rôle | Livrable |
|---|---|---|
| 1 — Veilleur | Repérer et résumer les avis PV pertinents | Fiche marché structurée |
| 2 — Sourcing | Trouver les modules certifiés au meilleur coût rendu | Specs + coût rendu CHF/Wc |
| 3 — Marge | Modèle financier **à deux étages** (ByImport → installateur → État) | Marge brute CHF / % + verdict compétitivité |
| 4 — Bid Manager | Rédiger la proposition (côté fourniture modules) | Offre + annexe technique |

## Comment utiliser ce kit

1. **`01-veille-simap.md`** — crée ton compte simap, charge les alertes CPV, filtre par procédure/seuil.
2. **`02-recherche-partenaire.md`** — trouve ton installateur-porteur (méthode des avis d'adjudication + email type + clauses contrat).
3. **`03-modele-marge.md`** + **`modele_marge.py`** — chiffre instantanément ta compétitivité dès que tu as un coût rendu.
4. **`templates/`** — remplis la lettre d'offre + l'annexe technique.
5. **`04-cycle-demo-pv.md`** — exemple complet de bout en bout pour voir le rendu.

## Garde-fous (à ne jamais oublier)

- **Modules certifiés IEC 61215 / IEC 61730 + CE**, et inscrits sur les listes
  **Pronovo** (sinon l'installation ne donne pas droit aux subventions → l'installateur refuse).
- Ne vise pas le module le moins cher absolu : vise **qualité certifiée à bon prix**.
- Le partenaire porte SAV / garantie / pose vis-à-vis de l'État ; ByImport le couvre en amont (garantie produit fabricant).
- Voie C = **pont** : les références s'accumulent chez le partenaire. Objectif à terme : basculer en filiale suisse (Voie A) une fois la rentabilité prouvée.
