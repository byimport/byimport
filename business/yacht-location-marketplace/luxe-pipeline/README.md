# luxe-pipeline — implémentation runnable (connector Avinode + générateur pSEO)

> Outillage **business standalone** (hors périmètre plugin Toprank). Met en code
> exécutable ce que `LUXE_MODULE_1_SCRAPING.md` (collecte/stockage) et
> `LUXE_MODULE_3_SEO.md` (pSEO) décrivent. **Python 3.11, stdlib pure, zéro
> `pip install`** pour le cœur. `psycopg`/`jsonschema` = extras optionnels.

## ⚠️ Honnêteté sur Avinode

L'API **Avinode / SchedAero** est *partner-gated* : l'auth exacte, les chemins
d'endpoint et la forme des réponses sont derrière une adhésion et **n'ont pas pu
être vérifiés ici**. `connectors/avinode.py` est écrit contre la **forme générale
documentée** (OAuth2 client-credentials + endpoint de recherche de trips/empty
legs renvoyant du JSON) et **doit être réconcilié avec la vraie doc une fois
crédencé**. Les chemins sont surchargeables par variables d'env.

→ Pour tourner **sans credentials**, utilise le **mode `--fixture`** : le
normaliseur est entièrement exercé, sans aucun appel réseau.

Garde-fous légaux (ToS, robots.txt, RGPD) : voir `../LUXE_MODULE_1_SCRAPING.md`
et `../LUXE_MODULE_2_LEADGEN.md`. Ce module ne collecte que de la **donnée
produit/prix**, pas de PII.

## Arborescence

```
luxe-pipeline/
  schema/listing.schema.json   contrat JSON canonique (source de vérité)
  db/schema.sql                DDL Postgres (source de vérité)
  common/                      _uid.py (écriture atomique), http.py (urllib + retry)
  connectors/                  base.py (ABC), avinode.py (client + normaliseur + CLI)
  store/                       json_store.py (défaut), postgres_store.py (optionnel)
  pseo/                        data/*.csv, templates.py, generate.py
  tests/                       fixtures + tests unittest hermétiques
  requirements-optional.txt    psycopg, jsonschema (extras)
```

## Mise en ligne

`build_site.sh` produit un site statique dans `dist/` (par défaut en **PREVIEW
`noindex`**). Config Vercel (`vercel.json`) et Netlify (`netlify.toml`) fournies.
Procédure complète, checklist preview→production et garde-fous : **`DEPLOIEMENT.md`**.

```bash
bash build_site.sh                       # PREVIEW noindex (défaut)
python3 -m http.server -d dist 8080      # prévisualiser localement
```

## Quickstart (hors-ligne, zéro install)

```bash
cd luxe-pipeline

# 1) Connector Avinode en mode fixture -> JSON canonique
python3 connectors/avinode.py \
  --fixture tests/fixtures/avinode_trip_search.json \
  --output /tmp/legs.json

# 2) Générer les pages pSEO + sitemap, en injectant les empty legs réelles
python3 pseo/generate.py --out ./dist --empty-legs /tmp/legs.json

# 3) Tests
python3 -m unittest discover -s tests -p 'test_*.py'
```

Sortie attendue de l'étape 2 : ~23 pages, un `sitemap.xml`, et un rapport stderr
listant les pages **skippées par le garde-fou anti-doorway** (route sans prix,
avion sans tarif horaire).

## Connector Avinode — usage

```bash
# Offline (recommandé pour dev/CI) :
python3 connectors/avinode.py --fixture tests/fixtures/avinode_trip_search.json --output legs.json

# Live (nécessite des credentials) :
export AVINODE_CLIENT_ID=...        # ou AVINODE_API_TOKEN=...
export AVINODE_CLIENT_SECRET=...
python3 connectors/avinode.py --from LBG --to NCE \
  --date-from 2026-06-10 --date-to 2026-06-20 --output legs.json
```

Variables d'env (mode live) : `AVINODE_API_BASE`, `AVINODE_TOKEN_URL`,
`AVINODE_SEARCH_PATH`, `AVINODE_CLIENT_ID`/`AVINODE_CLIENT_SECRET` ou
`AVINODE_API_TOKEN`. Sans creds ni `--fixture` → exit code 2 + message clair
(jamais de scraping silencieux ; le scraping reste documenté en MODULE_1).

Sortie : liste d'objets conformes à `schema/listing.schema.json`
(`asset_type:"jet"`, bloc `empty_leg`, `jet_specs`, `id = jet:avinode:<legId>`).

### Étendre à d'autres sources
Implémente `connectors/base.BaseConnector.fetch() -> list[dict]` (mêmes objets
canoniques). Un connector yachts (MYBA/Ankor) ou un fallback scraping se branche
sans toucher au stockage ni au pSEO.

## Stockage

- **Défaut** : `store/json_store.save(listings, path)` (écriture atomique 0600).
- **Postgres (optionnel)** : `pip install -r requirements-optional.txt`, applique
  `db/schema.sql`, configure `DATABASE_URL`, puis `store/postgres_store.upsert(listings)`
  (upsert idempotent `ON CONFLICT (id)`, + table `empty_leg`).

## Générateur pSEO — garde-fou anti-doorway

`pseo/generate.py` lit `pseo/data/*.csv` et n'émet une page **que si** elle porte
de la donnée réelle et unique (sinon **skip** + rapport, ou `--thin-policy
noindex` pour des stubs `noindex`). Une page doit satisfaire **toutes** ces
règles :

1. prix indicatif réel présent ;
2. ≥ 2 lignes de données réelles (options appareils d'une route / specs d'un avion) ;
3. ≥ 3 FAQ dérivées des données ;
4. intro unique dérivée de la ligne (pas de gabarit pur) ;
5. corps de page unique sur tout le run (pas de contenu dupliqué).

C'est ce qui distingue le pSEO légitime des *doorway pages* pénalisées par Google.

Génère : pages **pillar** (jets/yachts), **route**, **aircraft**, **event** ;
`sitemap.xml` ; maillage interne (pages sœurs + lien pilier) ; HTML on-page CRO
(prix above-the-fold, form 4 champs, WhatsApp/Call, empty legs live, sticky CTA)
+ JSON-LD `Service`/`Offer`/`FAQPage`/`BreadcrumbList`/`Event`.

Les datasets `pseo/data/*.csv` contiennent des valeurs **indicatives** à
remplacer par tes données réelles (idéalement alimentées par le connector et tes
tarifs négociés).

## Le pont Module 1 → Module 3
La sortie du connector (`--output legs.json`) se réinjecte dans le générateur
(`--empty-legs legs.json`) : les empty legs réelles apparaissent dans la page
route correspondante (`from_iata`/`to_iata`). Donnée fraîche → contenu unique →
SEO + conversion.
