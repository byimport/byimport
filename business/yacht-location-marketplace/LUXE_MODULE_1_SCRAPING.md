# Module 1 — Architecture de scraping & mapping data (Yachts & Jets)

> ⚙️ **Implémentation runnable** : le connector Avinode (jets), le schéma JSON canonique, le DDL Postgres et le stockage sont codés et testés dans [`luxe-pipeline/`](./luxe-pipeline/) — exécutables en stdlib pure (mode `--fixture` sans credentials).

> **Règle d'ingénieur n°1 : ne scrape que ce que tu ne peux pas obtenir par API/feed.** Le scraping DOM est fragile (casse à chaque refonte), risqué (ToS, IP-ban, RGPD si données perso) et coûteux à maintenir. Hiérarchie de collecte ci-dessous, de la plus robuste à la plus fragile.

## 1.0 Hiérarchie des sources (du robuste au fragile)

| Niveau | Source | Yachts | Jets | Robustesse |
|---|---|---|---|---|
| **A. API / marketplace B2B** | Le canal des pros | **Avinode** (n/a yacht), **MYBA / Ankor Systems / CharterIndex** (data agents centraux) | **Avinode + SchedAero** (l'API de référence empty legs & dispo), **PrivateFly/ACS** partenaires | ⭐⭐⭐⭐⭐ |
| **B. Flux affiliés / partenaires** | Programmes d'apport | YachtCharterFleet & CharterWorld ont des accords B2B/affiliés | XO, VistaJet (programme partenaires) | ⭐⭐⭐⭐ |
| **C. Données structurées de page** | JSON-LD `schema.org`, `__NEXT_DATA__`, API XHR internes | Souvent présentes | Souvent présentes | ⭐⭐⭐ |
| **D. Scraping CSS/XPath** | Dernier recours | Tous | Tous | ⭐⭐ |

➡️ **Architecture cible** : un *connector* par source, chacun implémentant la même interface `fetch() -> List[RawListing]`, peu importe la couche (A/B/C/D). Le reste du pipeline (normalisation, dédup, stockage) est agnostique de la source.

## 1.1 Les sources prioritaires

### Yachts (charter)
| Site | Ce qu'on extrait | Meilleure couche d'accès |
|---|---|---|
| **YachtCharterFleet** | Prix/semaine (low/high season), longueur, cabines, guests, constructeur, année, refit, localisation/saison | C (JSON-LD `Product`/embedded JSON) → D |
| **CharterWorld** | Idem + tarifs APA, équipage, zones | C → D |
| **Fraser Yachts** | Fleet charter & sale, specs, prix sur demande | D (souvent SSR, peu de JSON-LD) |
| **Burgess** | Superyachts charter/sale, specs détaillées | D |
| **Camper & Nicholsons / BoatInternational** | Flotte + data marché | C → D |

### Jets (charter & empty legs)
| Site | Ce qu'on extrait | Meilleure couche d'accès |
|---|---|---|
| **Air Charter Service (ACS)** | Devis par route, types d'appareils, empty legs | B/C (XHR de devis) |
| **Paramount Business Jets** | Estimateur de prix par route, specs appareils | C (API d'estimation) |
| **XO** | Vols partagés, deals, empty legs, prix/siège | C (API mobile/web JSON) → B |
| **VistaJet** | Flotte, programme, pas de prix public (lead-based) | D (specs flotte only) |
| **Empty legs agrégés** (LunaJets, Mighty Jet, emptylegmarket, GlobeAir) | Route, date, appareil, prix discount | C (souvent un JSON XHR « /api/legs ») |

> 🎯 **Pro tip empty legs** : l'or des jets, ce sont les **empty legs** (vols de repositionnement à -50/-75 %). Ils sont **éphémères (24-72 h)** → ton scraper doit tourner en **quasi temps réel** (cron 15-30 min) et notifier, pas en batch quotidien.

## 1.2 Stratégie d'extraction — cibler le JSON, pas le CSS

**Ordre de tentative dans chaque connector :**

1. **JSON-LD** : `<script type="application/ld+json">` → souvent un objet `Product`, `Vehicle`, `Offer`, `Boat`. **Le plus stable** (ne bouge pas avec le redesign visuel).
2. **État applicatif embarqué** : `__NEXT_DATA__` (Next.js), `__NUXT__`, `window.__INITIAL_STATE__`, `__APOLLO_STATE__`. Contient souvent **toute la fiche** en JSON propre.
3. **API XHR interne** : ouvrir DevTools → onglet Network → filtrer `Fetch/XHR` → repérer l'endpoint qui renvoie la donnée (ex. `/api/v2/yachts/{id}`, `/charter/quote`). **Frappe l'API directement** (10× plus rapide et stable que le DOM).
4. **CSS/XPath** : seulement si 1-3 échouent.

### Patterns de sélecteurs (TEMPLATES à vérifier/adapter — les DOM changent)

> ⚠️ Ne copie pas ces sélecteurs en aveugle : ils illustrent la *méthode*. Vérifie chacun dans l'inspecteur avant prod. Préfère les attributs sémantiques (`itemprop`, `data-*`) aux classes utilitaires (`.css-1x2y3z`) qui changent à chaque build.

```python
# Champs canoniques → patterns de sélection (CSS d'abord, XPath en repli)
SELECTOR_HINTS = {
    # --- communs ---
    "title":      ['h1[itemprop="name"]', 'h1.listing-title', '//h1'],
    "price_raw":  ['[itemprop="price"]', '.price, .charter-price, .from-price',
                   '//*[contains(@class,"price")][1]'],
    "currency":   ['[itemprop="priceCurrency"]::attr(content)'],
    "location":   ['[itemprop="homeLocation"]', '.cruising-area, .base-location'],
    # --- yacht ---
    "length_m":   ['[data-spec="length"]', 'li:contains("Length") .value',
                   '//tr[th[contains(.,"Length")]]/td'],
    "guests":     ['[data-spec="guests"]', 'li:contains("Guests") .value'],
    "cabins":     ['[data-spec="cabins"]', 'li:contains("Cabins") .value'],
    "builder":    ['[data-spec="builder"]', 'li:contains("Builder") .value'],
    "year_built": ['[data-spec="year"]', 'li:contains("Year") .value'],
    "refit_year": ['li:contains("Refit") .value'],
    # --- jet ---
    "aircraft_model": ['[data-aircraft]', '.aircraft-type'],
    "pax":            ['[data-spec="pax"]', '.seats .value'],
    "route_from":     ['[data-from]', '.leg-origin'],
    "route_to":       ['[data-to]', '.leg-destination'],
    "empty_leg_date": ['[data-leg-date]', 'time[datetime]::attr(datetime)'],
    "price_per_hour": ['[data-hourly]', '.hourly-rate'],
}
```

## 1.3 Anti-bot — stratégie réaliste et graduée

> Ces sites de luxe sont protégés (Cloudflare, DataDome, PerimeterX/HUMAN, Akamai). **N'attaque pas frontalement.** Le coût/risque monte avec le niveau ; reste au plus bas qui marche.

| Niveau | Quand | Stack |
|---|---|---|
| **0. Politesse** | Toujours | `robots.txt` respecté, 1 req / 3-8 s jitterée, cache HTTP (ETag/Last-Modified), heures creuses, `Accept-Language` cohérent |
| **1. HTTP brut + UA rotation** | Sites légers (couches C avec API ouverte) | `httpx`/`requests` + pool d'User-Agents réalistes + headers complets cohérents (pas juste l'UA : `sec-ch-ua`, `Referer`, `Accept`) |
| **2. Proxies résidentiels rotatifs** | IP datacenter bloquées | **BrightData / Oxylabs / SOAX** résidentiels, rotation par session, géo-ciblage (IP du pays du site) |
| **3. Navigateur furtif** | JS lourd / fingerprint | **Playwright + playwright-stealth** (ou `patchright`), ou **camoufox** (Firefox anti-fingerprint), viewport/timezone/locale cohérents |
| **4. API de scraping managée** | Cloudflare/DataDome agressifs | **ScrapingBee / BrightData Web Unlocker / Zyte API** : ils gèrent JS-render + résolution challenge + proxies. Tu paies, mais tu externalises le combat anti-bot |

### Anti-fingerprint — ce qui te grille vraiment
- **Cohérence > furtivité.** Une IP résidentielle française + `Accept-Language: en-US` + timezone `America/New_York` = signal de bot évident. Aligne IP/locale/timezone/UA.
- **Rythme humain.** Pas de 50 req/s. Jitter, pauses, navigation plausible (page liste → fiche).
- **Réutilise les sessions/cookies** (passe le challenge une fois, garde le `cf_clearance`).
- **TLS/HTTP2 fingerprint** : `requests` a une signature JA3 de bot. Utilise `curl_cffi` (`impersonate="chrome124"`) pour matcher le fingerprint TLS d'un vrai Chrome — souvent ça suffit là où les proxies seuls échouent.

### ⚖️ Garde-fou légal (non négociable)
- **ToS** : la plupart de ces sites interdisent le scraping. Risque = blocage, courrier d'avocat, voire action. **Pour les sources critiques, sécurise un accord d'affiliation/data plutôt que de scraper en douce.**
- **Données personnelles** (noms de propriétaires, contacts équipage, brokers) → **RGPD**. Ne stocke pas de PII sans base légale. Pour ce module, **ne collecte QUE de la donnée produit/prix**, pas de personnes.
- **Pas de contournement de paywall/login.** Scraper derrière une authentification = aggravant. Reste sur le public.

## 1.4 Schéma JSON canonique (la « source de vérité » inter-sources)

```json
{
  "$schema": "https://schema.luxcharter.internal/listing.v1.json",
  "id": "yc:yachtcharterfleet:ad-12345",
  "asset_type": "yacht",
  "source": { "site": "yachtcharterfleet", "url": "https://...", "scraped_at": "2026-06-06T08:30:00Z", "access_layer": "json-ld" },
  "title": "M/Y Example 50m",
  "status": "available",
  "location": { "base": "Monaco", "region": "West Mediterranean", "country": "MC", "lat": 43.74, "lon": 7.42 },
  "pricing": {
    "currency": "EUR",
    "yacht": { "low_season_week": 280000, "high_season_week": 320000, "apa_pct": 30, "vat_note": "plus VAT" },
    "jet": null
  },
  "yacht_specs": {
    "length_m": 50.0, "beam_m": 9.2, "guests_cruising": 12, "guests_sleeping": 12,
    "cabins": 6, "crew": 11, "builder": "Benetti", "year_built": 2016, "refit_year": 2022,
    "type": "motor", "amenities": ["jacuzzi","stabilizers","wifi","tender","jetski"]
  },
  "jet_specs": null,
  "empty_leg": null,
  "media": { "hero": "https://...", "gallery": ["https://...","https://..."] },
  "raw_hash": "sha256:...",
  "first_seen": "2026-05-01T00:00:00Z",
  "last_seen": "2026-06-06T08:30:00Z"
}
```

Variante **jet / empty leg** (mêmes enveloppe + champs spécifiques) :

```json
{
  "id": "jet:lunajets:leg-98765",
  "asset_type": "jet",
  "empty_leg": {
    "is_empty_leg": true,
    "from": { "iata": "LBG", "city": "Paris", "country": "FR" },
    "to":   { "iata": "NCE", "city": "Nice", "country": "FR" },
    "date": "2026-06-12",
    "window_start": "2026-06-12T09:00:00Z",
    "window_end": "2026-06-12T18:00:00Z",
    "price": 8900, "currency": "EUR", "discount_pct_est": 65, "seats": 8
  },
  "jet_specs": { "aircraft_model": "Citation XLS+", "category": "midsize",
                 "pax": 8, "range_nm": 2100, "year": 2019, "price_per_hour_est": 4200 }
}
```

## 1.5 Stockage — PostgreSQL (recommandé) ou Airtable (MVP)

### PostgreSQL (DDL prod-ready)

```sql
-- Sources
CREATE TABLE source (
    id          TEXT PRIMARY KEY,            -- 'yachtcharterfleet'
    asset_type  TEXT NOT NULL CHECK (asset_type IN ('yacht','jet')),
    base_url    TEXT NOT NULL,
    access_layer TEXT NOT NULL,              -- api|affiliate|json-ld|css
    robots_ok   BOOLEAN NOT NULL DEFAULT true
);

-- Annonces (cœur, polymorphe + JSONB pour les specs variables)
CREATE TABLE listing (
    id           TEXT PRIMARY KEY,                       -- 'yc:site:adid'
    asset_type   TEXT NOT NULL CHECK (asset_type IN ('yacht','jet')),
    source_id    TEXT NOT NULL REFERENCES source(id),
    url          TEXT NOT NULL,
    title        TEXT,
    status       TEXT DEFAULT 'available',
    -- géo
    location_base   TEXT,
    region          TEXT,
    country         CHAR(2),
    geo             GEOGRAPHY(POINT, 4326),
    -- prix dénormalisés pour requêtes rapides
    currency        CHAR(3),
    price_week_low  NUMERIC,   -- yacht
    price_week_high NUMERIC,   -- yacht
    price_per_hour  NUMERIC,   -- jet
    -- specs typées communes + reste en JSONB
    capacity        INT,       -- guests (yacht) / pax (jet)
    year_built      INT,
    specs           JSONB NOT NULL DEFAULT '{}',
    media           JSONB NOT NULL DEFAULT '{}',
    raw_hash        TEXT,
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_listing_type_region ON listing(asset_type, region);
CREATE INDEX idx_listing_specs_gin   ON listing USING GIN (specs);
CREATE INDEX idx_listing_geo         ON listing USING GIST (geo);

-- Empty legs (haute volatilité, table dédiée)
CREATE TABLE empty_leg (
    id           TEXT PRIMARY KEY,
    listing_id   TEXT REFERENCES listing(id),
    from_iata    CHAR(4), to_iata CHAR(4),
    leg_date     DATE NOT NULL,
    window_start TIMESTAMPTZ, window_end TIMESTAMPTZ,
    aircraft     TEXT, pax INT,
    price        NUMERIC, currency CHAR(3), discount_pct_est INT,
    seen_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at   TIMESTAMPTZ,                 -- leg_date + buffer
    is_active    BOOLEAN NOT NULL DEFAULT true
);
CREATE INDEX idx_empty_leg_route_date ON empty_leg(from_iata, to_iata, leg_date) WHERE is_active;

-- Historique de prix (détecter baisses/hausses = signal de vente)
CREATE TABLE price_history (
    listing_id  TEXT REFERENCES listing(id),
    captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    price_week_low NUMERIC, price_week_high NUMERIC, price_per_hour NUMERIC,
    PRIMARY KEY (listing_id, captured_at)
);
```

> **Dédup & upsert** : clé `id` déterministe (`site:adid`) + `raw_hash` (sha256 du JSON normalisé). À chaque run : `INSERT ... ON CONFLICT (id) DO UPDATE SET last_seen=now(), ...` et n'écris dans `price_history` que si le hash de prix a changé.

### Airtable (MVP, < 50k lignes)
- Table **Listings** : `id` (clé primaire texte), `asset_type` (single select), `source` (link → Sources), `title`, `region`, `country`, `currency`, `price_week_low`, `price_week_high`, `price_per_hour`, `capacity`, `year_built`, `specs_json` (long text), `url`, `hero` (attachment/url), `first_seen`, `last_seen`.
- Table **EmptyLegs** : `route` (formula `from→to`), `from`, `to`, `leg_date`, `aircraft`, `price`, `discount_pct`, `is_active`, `expires_at`.
- Sync via API Airtable (`pyairtable`), upsert sur `id`. Bascule vers Postgres dès que tu dépasses ~quelques 10k lignes ou que tu veux du géo/temps réel.

## 1.6 Squelette de code (Playwright + curl_cffi + pydantic + extruct)

```python
# pip install curl_cffi playwright playwright-stealth extruct pydantic w3lib psycopg[binary]
from __future__ import annotations
import asyncio, hashlib, json, random
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from curl_cffi import requests as creq          # fingerprint TLS d'un vrai Chrome
import extruct                                    # extraction JSON-LD/microdata

UAS = [  # pool réaliste, à élargir
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]
PROXIES = ["http://user:pass@gate.residential-provider.com:7777"]  # rotatif résidentiel

class Listing(BaseModel):
    id: str
    asset_type: str
    source: dict
    title: Optional[str] = None
    location: dict = Field(default_factory=dict)
    pricing: dict = Field(default_factory=dict)
    yacht_specs: Optional[dict] = None
    jet_specs: Optional[dict] = None
    empty_leg: Optional[dict] = None
    media: dict = Field(default_factory=dict)
    raw_hash: Optional[str] = None

def _hash(d: dict) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

# --- Couche 1 : HTTP furtif (TLS impersonation) -------------------------------
def fetch_http(url: str) -> Optional[str]:
    try:
        r = creq.get(url, impersonate="chrome124",
                     headers={"User-Agent": random.choice(UAS),
                              "Accept-Language": "en-GB,en;q=0.9"},
                     proxies={"https": random.choice(PROXIES)}, timeout=30)
        return r.text if r.status_code == 200 else None
    except Exception:
        return None

# --- Couche 3 : navigateur furtif (fallback JS lourd) -------------------------
async def fetch_browser(url: str) -> Optional[str]:
    from playwright.async_api import async_playwright
    from playwright_stealth import stealth_async
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, proxy={"server": random.choice(PROXIES)})
        ctx = await browser.new_context(
            user_agent=random.choice(UAS), locale="en-GB",
            timezone_id="Europe/Monaco", viewport={"width":1440,"height":900})
        page = await ctx.new_page(); await stealth_async(page)
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(random.randint(1500, 4000))  # rythme humain
        html = await page.content(); await browser.close()
        return html

# --- Extraction : JSON-LD d'abord, CSS en repli ------------------------------
def extract_jsonld(html: str, url: str) -> list[dict]:
    data = extruct.extract(html, base_url=url, syntaxes=["json-ld"])
    return data.get("json-ld", [])

def parse_yacht(html: str, url: str, site: str, ad_id: str) -> Listing:
    blocks = extract_jsonld(html, url)
    product = next((b for b in blocks if b.get("@type") in ("Product","Boat","Vehicle")), {})
    offer = product.get("offers", {}) or {}
    payload = {
        "id": f"yc:{site}:{ad_id}", "asset_type": "yacht",
        "source": {"site": site, "url": url,
                   "scraped_at": datetime.now(timezone.utc).isoformat(),
                   "access_layer": "json-ld" if product else "css"},
        "title": product.get("name"),
        "pricing": {"currency": offer.get("priceCurrency"),
                    "yacht": {"high_season_week": offer.get("price")}},
        # ... compléter via SELECTOR_HINTS si product vide (parsel/lxml)
    }
    payload["raw_hash"] = _hash(payload)
    return Listing(**payload)

async def scrape(url, site, ad_id):
    html = fetch_http(url) or await fetch_browser(url)   # gradation 1 -> 3
    if not html: return None
    return parse_yacht(html, url, site, ad_id)
```

### Alternative Scrapy (pour le volume) — middleware rotation
```python
# settings.py
DOWNLOAD_DELAY = 4
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# rotation proxy/UA via scrapy-rotating-proxies + scrapy-fake-useragent
ROTATING_PROXY_LIST_PATH = "proxies.txt"
DOWNLOADER_MIDDLEWARES = {
  "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
  "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
  "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
}
# Pour Cloudflare/DataDome agressif : router ces domaines vers Zyte/ScrapingBee API
```

## 1.7 Orchestration & fraîcheur
- **Listings yacht/jet (stables)** : crawl **quotidien** (nuit, heures creuses).
- **Empty legs (volatils)** : crawl **toutes les 15-30 min**, push d'alerte (webhook/Slack/Telegram) sur nouvelle leg matchant une route surveillée.
- **Stack** : Airflow/Prefect (ou simple cron + queue) ; un DAG par source ; retry exponentiel ; circuit-breaker si taux de ban > seuil → bascule couche 4 (API managée) automatiquement.
- **Observabilité** : log taux de succès/ban par source, dérive du nombre de champs extraits (alerte si un site a changé son DOM → un connector retourne 0 specs).

## 1.8 Erreurs qui tuent ce module
1. **Scraper en couche D ce qui existe en couche A/B.** → Maintenance infinie. Cherche l'API/feed d'abord.
2. **Sélecteurs sur classes utilitaires** (`.css-1ab2`). → Cassent au prochain build. Cible JSON-LD / `data-*` / `itemprop`.
3. **Stocker de la PII produit-broker sans base légale RGPD.** → Risque juridique. Ce module = data produit only.
4. **Batch quotidien sur les empty legs.** → Tu rates 90 % des deals (durée de vie < 72 h).
5. **Attaque frontale anti-bot.** → IP grillée en 1h. Politesse + cohérence fingerprint d'abord, force brute jamais.
