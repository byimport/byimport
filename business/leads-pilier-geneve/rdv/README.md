# Dossier `rdv/` — RDV pris (registre + fiches clients)

Stockage des **rendez-vous qualifiés pris**, avec les informations clients importantes.
Alimenté par vous ou par l'**agent IA** au moment où un RDV est booké, puis transmis au
conseiller **SwissKap**.

## Contenu

| Fichier | Rôle |
|---|---|
| `registre-rdv.csv` | **Registre central** : une ligne par RDV pris. Format CSV → ouvrable dans Excel/Sheets, et automatisable (Make/n8n) pour pousser vers SwissKap ou le CRM. |
| `*.rdv` | **Une fiche par RDV** (ex. `2026-0042.rdv`), format `clé : valeur` simple à lire et à parser. Détail complet d'un dossier (cf. `../MODELE_FICHE_RDV.md`). |

## Champs importants (registre)

`ref, date_creation, nom, email, telephone, adresse, canton, travail,
preference_pilier, avoirs_estimes_chf, date_rdv, heure_rdv, format,
conseiller_swisskap, opt_in, statut`

- **email** — adresse email du client (contact principal).
- **preference_pilier** — `2e` / `3e` / `2e+3e` (ce qui intéresse le client).
- **travail** — employeur / profession (et statut : salarié, indépendant, frontalier…).
- **adresse** — adresse du client (canton renseigné à part pour le routage/fiscalité).
- **opt_in** — preuve de consentement (date + source) — **obligatoire** avant tout contact
  (cf. `../CONFORMITE_APPELS.md`).
- **statut** — `pris` / `confirmé` / `honoré` / `no-show` / `signé` / `annulé`.

## Règles

1. **Ne rien stocker sans opt-in valide** (la colonne `opt_in` doit être remplie).
2. Données sensibles (avoirs financiers) → ce dossier relève du **registre des traitements
   nLPD** ; accès restreint, durée de conservation définie (cf. `../CONFORMITE_APPELS.md`).
3. Ce sont des **données réelles de clients** : en production, ce dossier **ne doit pas** être
   poussé dans un dépôt public. Les fichiers ici présents sont des **exemples fictifs** servant
   de gabarit. Garder les vraies données dans le CRM / un stockage privé chiffré.
