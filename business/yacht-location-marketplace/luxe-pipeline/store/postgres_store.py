#!/usr/bin/env python3
"""Optional Postgres store — upsert canonical listings + empty legs.

psycopg is imported lazily so the rest of the pipeline runs with zero external
dependencies. Install with: pip install -r requirements-optional.txt

Connection via DATABASE_URL (e.g. postgresql://user:pass@host:5432/db).
Apply db/schema.sql once before first use.
"""
from __future__ import annotations

import json
import os
from typing import Any


def _connect():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional path
        raise RuntimeError(
            "psycopg not installed. `pip install -r requirements-optional.txt`") from exc
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("Set DATABASE_URL to use the Postgres store")
    return psycopg.connect(dsn)


UPSERT_LISTING = """
INSERT INTO listing (id, asset_type, source_id, url, title, status,
                     location_base, region, country, currency,
                     price_week_low, price_week_high, price_per_hour,
                     capacity, year_built, specs, media, raw_hash, last_seen)
VALUES (%(id)s, %(asset_type)s, %(source_id)s, %(url)s, %(title)s, %(status)s,
        %(location_base)s, %(region)s, %(country)s, %(currency)s,
        %(price_week_low)s, %(price_week_high)s, %(price_per_hour)s,
        %(capacity)s, %(year_built)s, %(specs)s, %(media)s, %(raw_hash)s, now())
ON CONFLICT (id) DO UPDATE SET
    last_seen = now(), status = EXCLUDED.status, currency = EXCLUDED.currency,
    price_per_hour = EXCLUDED.price_per_hour, specs = EXCLUDED.specs,
    media = EXCLUDED.media, raw_hash = EXCLUDED.raw_hash;
"""

UPSERT_EMPTY_LEG = """
INSERT INTO empty_leg (id, listing_id, from_iata, to_iata, leg_date,
                       window_start, window_end, aircraft, pax, price, currency,
                       discount_pct_est, is_active)
VALUES (%(id)s, %(listing_id)s, %(from_iata)s, %(to_iata)s, %(leg_date)s,
        %(window_start)s, %(window_end)s, %(aircraft)s, %(pax)s, %(price)s,
        %(currency)s, %(discount_pct_est)s, true)
ON CONFLICT (id) DO UPDATE SET
    price = EXCLUDED.price, seen_at = now(), is_active = true;
"""


def _listing_row(item: dict[str, Any]) -> dict[str, Any]:
    loc = item.get("location") or {}
    jet = (item.get("pricing") or {}).get("jet") or {}
    yacht = (item.get("pricing") or {}).get("yacht") or {}
    return {
        "id": item["id"], "asset_type": item["asset_type"],
        "source_id": (item.get("source") or {}).get("site", "unknown"),
        "url": (item.get("source") or {}).get("url"), "title": item.get("title"),
        "status": item.get("status", "available"),
        "location_base": loc.get("base"), "region": loc.get("region"),
        "country": (loc.get("country") or "")[:2] or None,
        "currency": (item.get("pricing") or {}).get("currency"),
        "price_week_low": yacht.get("low_season_week"),
        "price_week_high": yacht.get("high_season_week"),
        "price_per_hour": (item.get("jet_specs") or {}).get("price_per_hour_est")
        or jet.get("price"),
        "capacity": (item.get("jet_specs") or {}).get("pax")
        or (item.get("yacht_specs") or {}).get("guests_cruising"),
        "year_built": (item.get("jet_specs") or {}).get("year")
        or (item.get("yacht_specs") or {}).get("year_built"),
        "specs": json.dumps(item.get("jet_specs") or item.get("yacht_specs") or {}),
        "media": json.dumps(item.get("media") or {}),
        "raw_hash": item.get("raw_hash"),
    }


def upsert(listings: list[dict[str, Any]]) -> int:
    """Upsert listings (+ empty legs) into Postgres. Returns row count."""
    conn = _connect()
    n = 0
    with conn, conn.cursor() as cur:
        for item in listings:
            cur.execute(
                "INSERT INTO source (id, asset_type, base_url, access_layer) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
                ((item.get("source") or {}).get("site", "unknown"),
                 item["asset_type"], (item.get("source") or {}).get("url") or "",
                 (item.get("source") or {}).get("access_layer", "api")))
            cur.execute(UPSERT_LISTING, _listing_row(item))
            el = item.get("empty_leg")
            if el and el.get("is_empty_leg"):
                cur.execute(UPSERT_EMPTY_LEG, {
                    "id": item["id"], "listing_id": item["id"],
                    "from_iata": (el.get("from") or {}).get("iata"),
                    "to_iata": (el.get("to") or {}).get("iata"),
                    "leg_date": el.get("date"),
                    "window_start": el.get("window_start"),
                    "window_end": el.get("window_end"),
                    "aircraft": (item.get("jet_specs") or {}).get("aircraft_model"),
                    "pax": el.get("seats"), "price": el.get("price"),
                    "currency": el.get("currency"),
                    "discount_pct_est": el.get("discount_pct_est"),
                })
            n += 1
    conn.close()
    return n
