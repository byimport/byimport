-- Canonical storage for luxury charter listings (yachts + jets).
-- Single source of truth for the DDL described in LUXE_MODULE_1_SCRAPING.md §1.5.
-- Postgres 14+. Requires the postgis extension only if you use the geo columns.

-- CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS source (
    id           TEXT PRIMARY KEY,            -- 'avinode', 'yachtcharterfleet'
    asset_type   TEXT NOT NULL CHECK (asset_type IN ('yacht', 'jet')),
    base_url     TEXT NOT NULL,
    access_layer TEXT NOT NULL,               -- api|affiliate|json-ld|css|fixture
    robots_ok    BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS listing (
    id              TEXT PRIMARY KEY,                          -- 'jet:avinode:leg-123'
    asset_type      TEXT NOT NULL CHECK (asset_type IN ('yacht', 'jet')),
    source_id       TEXT NOT NULL REFERENCES source(id),
    url             TEXT,
    title           TEXT,
    status          TEXT DEFAULT 'available',
    location_base   TEXT,
    region          TEXT,
    country         CHAR(2),
    -- geo          GEOGRAPHY(POINT, 4326),   -- enable with postgis
    currency        CHAR(3),
    price_week_low  NUMERIC,   -- yacht
    price_week_high NUMERIC,   -- yacht
    price_per_hour  NUMERIC,   -- jet
    capacity        INT,       -- guests (yacht) / pax (jet)
    year_built      INT,
    specs           JSONB NOT NULL DEFAULT '{}',
    media           JSONB NOT NULL DEFAULT '{}',
    raw_hash        TEXT,
    first_seen      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_listing_type_region ON listing (asset_type, region);
CREATE INDEX IF NOT EXISTS idx_listing_specs_gin   ON listing USING GIN (specs);

CREATE TABLE IF NOT EXISTS empty_leg (
    id               TEXT PRIMARY KEY,
    listing_id       TEXT REFERENCES listing(id),
    from_iata        CHAR(4),
    to_iata          CHAR(4),
    leg_date         DATE NOT NULL,
    window_start     TIMESTAMPTZ,
    window_end       TIMESTAMPTZ,
    aircraft         TEXT,
    pax              INT,
    price            NUMERIC,
    currency         CHAR(3),
    discount_pct_est INT,
    seen_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at       TIMESTAMPTZ,
    is_active        BOOLEAN NOT NULL DEFAULT true
);
CREATE INDEX IF NOT EXISTS idx_empty_leg_route_date
    ON empty_leg (from_iata, to_iata, leg_date) WHERE is_active;

CREATE TABLE IF NOT EXISTS price_history (
    listing_id      TEXT REFERENCES listing(id),
    captured_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    price_week_low  NUMERIC,
    price_week_high NUMERIC,
    price_per_hour  NUMERIC,
    PRIMARY KEY (listing_id, captured_at)
);
