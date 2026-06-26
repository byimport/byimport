# By Solar — Segmentation des contacts opt-in (via crm-query / crm-reports)

Objectif : produire une **audience consentante** pour une campagne email solaire, sans jamais supposer qu'un contact présent en CRM accepte d'être démarché.

## Pré-requis : un connecteur CRM connecté

Les skills `crm-query` / `crm-reports` lisent depuis le CRM connecté au host (HubSpot = surface de référence). Ils ne créent et ne modifient rien, et ils n'envoient aucun email.

## Étape 1 — Découvrir les propriétés (ne rien coder en dur)

Les noms de propriétés et les valeurs d'énumération sont **spécifiques au portail**. Avant de filtrer, faire découvrir par `crm-query` :

- la propriété de **consentement / abonnement marketing** (mots-clés : `opt_in`, `consent`, `subscription`, `marketing`, `email_status`) ;
- la propriété de **cycle de vie** et la valeur qui correspond à un prospect exploitable (`lifecyclestage`) ;
- la propriété **géographique** (région / canton / code postal) pertinente pour la zone d'intervention de By Solar ;
- toute propriété **maison/toiture** utile au ciblage solaire si elle existe (type de logement, propriétaire vs locataire, surface de toit) — sinon, ne pas l'inventer.

## Étape 2 — Construire le segment (consentement = filtre dur)

Demander à `crm-query` un groupe de filtres **ET** du type :

```
objet = contacts
ET  consentement = opt-in (valeur découverte à l'étape 1)
ET  HAS_PROPERTY(consentement)            ← exclut les consentements non renseignés
ET  lifecyclestage IN (<valeurs exploitables>)
ET  région IN (<zone d'intervention By Solar>)
[ET propriétaire = oui, si la propriété existe]
```

Règles non négociables :

- **Pas d'opt-in renseigné → hors segment.** « Présent en CRM » ≠ « accepte d'être contacté ».
- Le **compte** annoncé vient du `total` renvoyé, pas de la première page.
- `crm-query` doit **rappeler la définition exacte du filtre** et **combien de fiches ont été exclues** faute de consentement — ce nombre est un garde-fou, pas du bruit.

## Étape 3 — Dimensionner / profiler (crm-reports)

Pour décider de l'effort de campagne, demander à `crm-reports` des agrégats sur le **même périmètre consentant** :

- nombre de contacts opt-in **par région** (`GROUP BY` région) ;
- répartition **par cycle de vie** ;
- contacts opt-in **créés par mois** sur 6–12 mois (`DATE_TRUNC(createdate,'MONTH')`) pour voir la dynamique de collecte.

Rappel dialecte : pas de `HAVING` ni de `COUNT(DISTINCT)` ; le filtrage par seuil se fait côté client après le `GROUP BY` (voir `crm/reports/references/sql-syntax.md`).

## Étape 4 — Exporter la définition, pas un fichier sauvage de PII

- Persister la **définition du segment** (la spec de filtres) est utile pour la réutiliser : `{data_dir}/crm/segments/by-solar-optin.json`. Ne jamais committer ce fichier s'il vit sous un `.notfair/` projet.
- L'**export des contacts eux-mêmes** vers l'ESP se fait à l'étape suivante (`esp-handoff.md`) — idéalement par synchro CRM↔ESP native plutôt qu'un CSV qui traîne.

## Si le segment opt-in est vide ou minuscule

Ne pas « compenser » en élargissant à des contacts non consentants. À la place, générer des leads opt-in avec les skills déjà présents dans le plugin :

- landing page solaire + formulaire de **consentement explicite** (cases non pré-cochées) → `seo/content-writer`, `seo/seo-page` ;
- acquisition payante ciblée → `google-ads/*`, `meta-ads/*` ;
- visibilité locale → `seo/seo-analysis`, `seo/geo-optimizer`.

Les leads consentants ainsi collectés alimentent le CRM, puis ce pipeline.
