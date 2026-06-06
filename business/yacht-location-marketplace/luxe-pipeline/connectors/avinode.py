#!/usr/bin/env python3
"""Avinode (jets) connector — fetch empty legs / trips and normalise to schema v1.

Avinode + SchedAero is the B2B marketplace the private-jet industry actually
runs on. Using its API is more robust and ToS-clean than scraping broker
websites (see LUXE_MODULE_1_SCRAPING.md §1.0).

⚠️ HONESTY: the Avinode API is partner-gated. The exact auth flow, endpoint
paths and response shape are behind a membership and CANNOT be verified here.
This client is written against the documented general shape (OAuth2
client-credentials + a trip/empty-leg search endpoint returning JSON) and MUST
be reconciled with the real API docs once you have credentials. Override the
endpoint paths via env vars if they differ.

To run WITHOUT credentials (offline), use --fixture with a recorded-shape
response: the normaliser is fully exercised without any network call.

Usage:
  # offline, from a recorded response
  python3 avinode.py --fixture ../tests/fixtures/avinode_trip_search.json --output legs.json

  # live (needs creds in env or .env)
  python3 avinode.py --from LBG --to NCE --date-from 2026-06-10 --date-to 2026-06-20 --output legs.json

Env vars (live mode):
  AVINODE_API_BASE        (default https://services.avinode.com)
  AVINODE_TOKEN_URL       (default {API_BASE}/oauth2/token)
  AVINODE_SEARCH_PATH     (default /api/v1/trips/search)
  AVINODE_CLIENT_ID / AVINODE_CLIENT_SECRET   (OAuth2 client-credentials)
  AVINODE_API_TOKEN       (alternative: a ready bearer token, skips OAuth)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

# --- make sibling packages importable when run as a script -------------------
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.http import HttpError, request_json  # noqa: E402
from common._uid import portable_uid, secure_write_json  # noqa: E402
from connectors.base import BaseConnector, content_hash  # noqa: E402


# ----------------------------------------------------------------------------
# Config loading (.env walk-up, same spirit as the repo's SEO scripts)
# ----------------------------------------------------------------------------
def _load_env_files() -> None:
    here = os.path.abspath(os.path.dirname(__file__))
    for _ in range(6):
        for name in (".env.local", ".env"):
            path = os.path.join(here, name)
            if os.path.isfile(path):
                try:
                    with open(path, encoding="utf-8") as fh:
                        for line in fh:
                            line = line.strip()
                            if not line or line.startswith("#") or "=" not in line:
                                continue
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
                except Exception:
                    pass
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent


# ----------------------------------------------------------------------------
# Normalisation: raw Avinode leg -> canonical schema v1
# ----------------------------------------------------------------------------
def _num(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any) -> Optional[int]:
    n = _num(value)
    return int(n) if n is not None else None


def _airport(node: Any) -> dict[str, Any]:
    """Tolerant extraction of an airport node across plausible field names."""
    if not isinstance(node, dict):
        return {"iata": None, "city": None, "country": None}
    return {
        "iata": node.get("iata") or node.get("icao") or node.get("code"),
        "city": node.get("city") or node.get("name"),
        "country": node.get("country") or node.get("countryCode"),
    }


def normalize_leg(raw: dict[str, Any], *, site: str = "avinode",
                  access_layer: str = "api") -> dict[str, Any]:
    """Map one raw Avinode empty-leg/trip object to the canonical schema."""
    leg_id = (raw.get("id") or raw.get("legId") or raw.get("tripId")
              or raw.get("sellerLiftId") or "unknown")
    seg = raw.get("segment") or raw.get("leg") or raw
    dep = _airport(seg.get("departureAirport") or seg.get("from") or seg.get("origin"))
    arr = _airport(seg.get("arrivalAirport") or seg.get("to") or seg.get("destination"))

    aircraft = raw.get("aircraft") or raw.get("lift") or {}
    price_node = raw.get("price") or raw.get("sellerPrice") or {}
    price = _num(price_node.get("amount") if isinstance(price_node, dict) else price_node)
    currency = (price_node.get("currency") if isinstance(price_node, dict) else None) \
        or raw.get("currency")

    payload: dict[str, Any] = {
        "id": f"jet:{site}:{leg_id}",
        "asset_type": "jet",
        "source": {
            "site": site,
            "url": raw.get("url") or raw.get("permalink"),
            "scraped_at": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc).isoformat(),
            "access_layer": access_layer,
        },
        "title": (f"{aircraft.get('aircraftType') or aircraft.get('type') or 'Private jet'} "
                  f"{dep.get('iata') or '?'}→{arr.get('iata') or '?'}").strip(),
        "status": "available",
        "location": {
            "base": dep.get("city"),
            "region": None,
            "country": dep.get("country"),
            "lat": None,
            "lon": None,
        },
        "pricing": {"currency": currency, "yacht": None,
                    "jet": {"price": price, "per": "leg"}},
        "yacht_specs": None,
        "jet_specs": {
            "aircraft_model": aircraft.get("aircraftType") or aircraft.get("type")
            or aircraft.get("model"),
            "category": aircraft.get("category") or aircraft.get("categoryName"),
            "pax": _int(aircraft.get("maxPax") or aircraft.get("seats") or aircraft.get("pax")),
            "range_nm": _int(aircraft.get("rangeNm") or aircraft.get("range")),
            "year": _int(aircraft.get("yearOfManufacture") or aircraft.get("year")),
            "price_per_hour_est": _num(raw.get("pricePerHour")),
        },
        "empty_leg": {
            "is_empty_leg": bool(raw.get("isEmptyLeg", raw.get("emptyLeg", True))),
            "from": dep,
            "to": arr,
            "date": (seg.get("departureDate") or seg.get("date")
                     or (seg.get("departureDateTime") or "")[:10] or None),
            "window_start": seg.get("departureDateTime") or seg.get("windowStart"),
            "window_end": seg.get("arrivalDateTime") or seg.get("windowEnd"),
            "price": price,
            "currency": currency,
            "discount_pct_est": _int(raw.get("discountPct") or raw.get("discountPercentage")),
            "seats": _int(aircraft.get("maxPax") or aircraft.get("seats")),
        },
        "media": {"hero": (aircraft.get("imageUrl") or None), "gallery": []},
    }
    payload["raw_hash"] = content_hash(payload)
    return payload


def _extract_legs(api_response: Any) -> list[dict[str, Any]]:
    """Pull the list of leg objects from plausible response envelopes."""
    if isinstance(api_response, list):
        return api_response
    if isinstance(api_response, dict):
        for key in ("data", "results", "trips", "emptyLegs", "items", "legs"):
            val = api_response.get(key)
            if isinstance(val, list):
                return val
    return []


# ----------------------------------------------------------------------------
# Connector
# ----------------------------------------------------------------------------
class AvinodeConnector(BaseConnector):
    site = "avinode"
    asset_type = "jet"
    access_layer = "api"

    def __init__(self, *, from_iata: str, to_iata: str,
                 date_from: str, date_to: str) -> None:
        self.from_iata = from_iata
        self.to_iata = to_iata
        self.date_from = date_from
        self.date_to = date_to
        self.api_base = os.environ.get("AVINODE_API_BASE", "https://services.avinode.com")
        self.search_path = os.environ.get("AVINODE_SEARCH_PATH", "/api/v1/trips/search")
        self._token: Optional[str] = None

    # --- auth ---------------------------------------------------------------
    def _authenticate(self) -> str:
        if self._token:
            return self._token
        direct = os.environ.get("AVINODE_API_TOKEN")
        if direct:
            self._token = direct
            return direct
        cid = os.environ.get("AVINODE_CLIENT_ID")
        secret = os.environ.get("AVINODE_CLIENT_SECRET")
        if not (cid and secret):
            raise HttpError(
                "No Avinode credentials. Set AVINODE_API_TOKEN, or "
                "AVINODE_CLIENT_ID + AVINODE_CLIENT_SECRET, or use --fixture.")
        token_url = os.environ.get("AVINODE_TOKEN_URL", f"{self.api_base}/oauth2/token")
        resp = request_json(token_url, method="POST",
                            form={"grant_type": "client_credentials",
                                  "client_id": cid, "client_secret": secret})
        self._token = (resp or {}).get("access_token")
        if not self._token:
            raise HttpError("Avinode OAuth response had no access_token")
        return self._token

    # --- live fetch ---------------------------------------------------------
    def fetch(self) -> list[dict[str, Any]]:
        token = self._authenticate()
        url = f"{self.api_base}{self.search_path}"
        body = {
            "departureAirport": self.from_iata,
            "arrivalAirport": self.to_iata,
            "departureDateFrom": self.date_from,
            "departureDateTo": self.date_to,
            "emptyLegsOnly": True,
        }
        resp = request_json(url, method="POST",
                            headers={"Authorization": f"Bearer {token}"}, body=body)
        return [normalize_leg(r, site=self.site, access_layer="api")
                for r in _extract_legs(resp)]


def fetch_from_fixture(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        resp = json.load(fh)
    return [normalize_leg(r, site="avinode", access_layer="fixture")
            for r in _extract_legs(resp)]


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Avinode jets connector")
    parser.add_argument("--fixture", help="Path to a recorded API response (offline mode)")
    parser.add_argument("--from", dest="from_iata", help="Departure IATA/ICAO")
    parser.add_argument("--to", dest="to_iata", help="Arrival IATA/ICAO")
    parser.add_argument("--date-from", dest="date_from", help="YYYY-MM-DD")
    parser.add_argument("--date-to", dest="date_to", help="YYYY-MM-DD")
    parser.add_argument("--output", help="Output JSON file (default: secure tempfile)")
    args = parser.parse_args(argv)

    _load_env_files()

    try:
        if args.fixture:
            print(f"[avinode] offline mode: normalising fixture {args.fixture}",
                  file=sys.stderr)
            listings = fetch_from_fixture(args.fixture)
        else:
            missing = [n for n, v in (("--from", args.from_iata), ("--to", args.to_iata),
                                       ("--date-from", args.date_from),
                                       ("--date-to", args.date_to)) if not v]
            if missing:
                print(f"[avinode] missing args for live mode: {', '.join(missing)} "
                      f"(or use --fixture)", file=sys.stderr)
                return 2
            conn = AvinodeConnector(from_iata=args.from_iata, to_iata=args.to_iata,
                                    date_from=args.date_from, date_to=args.date_to)
            listings = conn.fetch()
    except HttpError as exc:
        print(f"[avinode] {exc}", file=sys.stderr)
        return 2 if "credentials" in str(exc).lower() else 1
    except (OSError, ValueError) as exc:
        print(f"[avinode] error: {exc}", file=sys.stderr)
        return 1

    import tempfile
    out_path = args.output or os.path.join(
        tempfile.gettempdir(), f"avinode_legs_{portable_uid()}.json")
    secure_write_json(out_path, listings)

    with_price = sum(1 for x in listings if (x.get("empty_leg") or {}).get("price"))
    print(f"[avinode] {len(listings)} legs normalised "
          f"({with_price} with price) → {out_path}", file=sys.stderr)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
