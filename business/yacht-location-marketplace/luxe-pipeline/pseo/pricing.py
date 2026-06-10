#!/usr/bin/env python3
"""Pricing model — margin split + per-person display.

Business rules (configurable via env, defaults from the brief):
- The CSV price is the PUBLIC price the client pays (margin already included).
- Platform margin = SITE_MARGIN_PCT of the public price (default 40%).
  → owner payout = public * (1 - margin) ; platform keeps public * margin.
- Headline display = public / SITE_GROUP_SIZE  ("from €X per person",
  default group size 10) — ALWAYS shown next to the real total + group size
  (French consumer law: a per-person price must not hide the total).
"""
from __future__ import annotations

import os


def _envf(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


MARGIN_PCT = max(0.0, min(0.9, _envf("SITE_MARGIN_PCT", 0.40)))
GROUP_SIZE = max(1, int(_envf("SITE_GROUP_SIZE", 10)))


def to_amount(value) -> float | None:
    """Parse a price cell ('9500', '9 500', '', None) -> float or None."""
    if value is None:
        return None
    s = str(value).replace(" ", "").replace(" ", "").replace(",", ".")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def per_person(total, group: int = GROUP_SIZE) -> int | None:
    amt = to_amount(total)
    if amt is None:
        return None
    return round(amt / max(1, group))


def owner_payout(total) -> float | None:
    amt = to_amount(total)
    return round(amt * (1 - MARGIN_PCT), 2) if amt is not None else None


def platform_margin(total) -> float | None:
    amt = to_amount(total)
    return round(amt * MARGIN_PCT, 2) if amt is not None else None
