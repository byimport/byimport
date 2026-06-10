#!/usr/bin/env python3
"""Reference: create a Stripe Checkout Session for a charter booking.

⚠️ NOT LIVE. This is reference code. Going live requires:
  - a real Stripe account + STRIPE_SECRET_KEY,
  - Stripe Connect (owners onboarded as connected accounts) for the payout,
  - a legal entity + KYC (you are handling third-party funds),
  - replacing the placeholder owner mapping (owners.json).

Marketplace split (destination charge): the client pays the full price by card;
Stripe routes the owner's share to their connected account and keeps your
platform margin as the application fee — so you "keep the margin" automatically
and never improperly hold the owner's money.

  application_fee_amount = platform margin  (SITE_MARGIN_PCT, default 40%)
  owner receives          = total - application_fee

Deploy as a serverless function (Vercel/Netlify) — do NOT ship secret keys to
the static site. Install: pip install stripe   (NOT part of the zero-dep core).
"""
from __future__ import annotations

import csv
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from pseo import pricing  # noqa: E402

DATA_DIR = os.path.join(_ROOT, "pseo", "data")


def _route_price_eur(ref: str) -> float | None:
    """Recompute the price server-side from the ref — never trust the client."""
    # ref is the route slug, e.g. "geneva-to-nice"
    with open(os.path.join(DATA_DIR, "routes.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            slug = f"{row['from_iata']}-{row['to_iata']}".lower()
            # match against the human slug used on the site is done by the caller;
            # here we expose both iata and a price lookup helper.
            if ref in (slug, row.get("keyword", "")):
                return pricing.to_amount(row.get("price_from_eur"))
    return None


def _load_owners() -> dict:
    """ref -> {email, stripe_account}. Copy owners.example.json -> owners.json."""
    path = os.path.join(os.path.dirname(__file__), "owners.json")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def create_session(ref: str, date: str, pax: int, phone: str,
                   price_eur: float | None = None) -> dict:
    """Build a Stripe Checkout Session (destination charge). Returns the session.

    In production this runs in a serverless function and returns {url} to redirect
    the client to Stripe's hosted payment page.
    """
    try:
        import stripe  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional path
        raise RuntimeError("pip install stripe (reference dependency)") from exc

    secret = os.environ.get("STRIPE_SECRET_KEY")
    if not secret:
        raise RuntimeError("STRIPE_SECRET_KEY not set — cannot create a real session")
    stripe.api_key = secret

    total = price_eur if price_eur is not None else _route_price_eur(ref)
    if total is None:
        raise ValueError(f"No price found for ref={ref!r}")

    amount_cents = int(round(total * 100))
    fee_cents = int(round((pricing.platform_margin(total) or 0) * 100))
    owners = _load_owners()
    owner = owners.get(ref, {})

    payment_intent_data = {}
    if owner.get("stripe_account"):
        # destination charge: owner gets total - application_fee, you keep the fee
        payment_intent_data = {
            "application_fee_amount": fee_cents,
            "transfer_data": {"destination": owner["stripe_account"]},
        }

    base = os.environ.get("SITE_BASE_URL", "https://example.com")
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "quantity": 1,
            "price_data": {
                "currency": "eur",
                "unit_amount": amount_cents,
                "product_data": {"name": f"Charter booking — {ref}"},
            },
        }],
        payment_intent_data=payment_intent_data or None,
        success_url=f"{base}/booking/confirmed?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base}/booking/cancelled",
        metadata={"ref": ref, "date": date, "pax": str(pax), "phone": phone,
                  "owner_email": owner.get("email", ""),
                  "owner_payout_eur": str(pricing.owner_payout(total)),
                  "platform_margin_eur": str(pricing.platform_margin(total))},
    )
    return session


# --- Vercel/Netlify-style entrypoint (pseudocode for the real deployment) -----
def handler(request):  # pragma: no cover - serverless adapter
    body = request.get("body") or {}
    session = create_session(
        ref=body.get("ref", ""), date=body.get("date", ""),
        pax=int(body.get("pax", 1)), phone=body.get("phone", ""))
    return {"statusCode": 303, "headers": {"Location": session["url"]}}
