# By Solar — Contacter via HubSpot (uniquement les contacts opt-in)

> Hors périmètre plugin. Décrit comment **contacter** les leads dans HubSpot **sans** cold-emailing, et précise ce que l'automatisation peut / ne peut pas faire.

## Ce que le connecteur HubSpot (MCP) peut et ne peut pas faire

| Peut (via le MCP) | Ne peut PAS (via le MCP) |
|---|---|
| Lire / rechercher des contacts (`search_crm_objects`, `query_crm_data`) | **Envoyer un email marketing** |
| Découvrir le schéma, résoudre les owners | **Enrôler dans une séquence d'emails** |
| Créer / mettre à jour des fiches & associations (`manage_crm_objects`, avec confirmation) | Démarrer une campagne d'envoi |

**Conclusion : l'envoi ne se fait pas par l'automatisation.** Il se déclenche dans **HubSpot Marketing Email / Sequences (interface)**, par un humain, vers une liste **opt-in**. L'automatisation prépare tout *jusqu'à* l'envoi.

> Note : le seul outil d'envoi d'emails réellement exposé dans cet environnement est **Apollo** (séquences de prospection à froid, envoi irréversible). Il n'est **pas** utilisé ici : démarcher des particuliers solaires non consentants est interdit en France/UE. On ne l'emploie pas pour By Solar.

## Procédure conforme (de bout en bout)

1. **Segmenter les opt-in** (lecture seule) — via `crm-query`, sortir les contacts qui matchent la cible **et** dont la propriété de consentement marketing = vrai (voir `segmentation.md`). Exclure tout consentement non renseigné. Le compte vient du `total`.
2. **Matérialiser la liste dans HubSpot** — créer une **liste active** HubSpot fondée sur les mêmes critères (cycle de vie, région, `hs_marketable_status` / propriété de consentement). La liste se met à jour seule et respecte les désinscriptions. (Création/MAJ de fiches possible via `manage_crm_objects` avec confirmation ; la *liste* elle-même se construit côté interface HubSpot.)
3. **Choisir le bon canal selon la relation :**
   - **Lead opt-in marketing** (a demandé une simulation/devis) → **HubSpot Marketing Email** (one-to-many) avec les modèles de `email-templates.md`. Désinscription injectée automatiquement par HubSpot.
   - **Lead chaud individuel** (a pris RDV, échange en cours) → email 1:1 commercial, pas de blast.
   - **B2B pertinent** (copro, agriculteur, local pro) → séquence possible si message lié à la fonction + opt-out clair.
4. **Vérifier l'envoi technique** — domaine authentifié (SPF/DKIM/DMARC), `hs_marketable_status` = marketable sur les contacts visés (HubSpot facture et filtre là-dessus), pied de page légal complet.
5. **Lancer depuis l'interface HubSpot** — l'humain déclenche l'envoi marketing vers la liste opt-in. L'automatisation ne « pousse » pas l'envoi.
6. **Boucler dans le CRM** — taguer les répondants (lead chaud) pour le suivi commercial ; refléter les désinscriptions sur la propriété de consentement (écriture via `manage_crm_objects`, avec confirmation) pour que les futurs segments les excluent.

## Garde-fous (non négociables)
- **Aucun envoi à un contact non opt-in.** « Présent dans HubSpot » ≠ « marketable ».
- **Aucune séquence de prospection à froid** vers des particuliers.
- Désinscriptions traitées et respectées ; preuve de consentement conservée.
- L'automatisation s'arrête à la préparation : le **bouton d'envoi** reste une action humaine, vers une audience consentante.

## Si tu veux que je « contacte » maintenant
Ce que je peux faire tout de suite, proprement :
- construire le **segment opt-in** (`crm-query`) et te donner sa taille + sa définition ;
- rédiger l'email/la séquence (`email-templates.md`) prêt à coller dans HubSpot ;
- préparer les **mises à jour de fiches** (tags, scoring) via `manage_crm_objects`, **après ta confirmation**.

Ce que je ne ferai pas : déclencher un envoi de masse vers des prospects non consentants.
