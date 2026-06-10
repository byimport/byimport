#!/usr/bin/env python3
"""Reference: Stripe webhook — on paid booking, send the reservation to the owner.

⚠️ NOT LIVE. Requires STRIPE_WEBHOOK_SECRET and a real mail/notification channel.

Flow on `checkout.session.completed`:
  1. verify the Stripe signature (never trust an unverified webhook),
  2. read metadata (ref, date, pax, phone, owner_email, owner_payout, margin),
  3. notify the owner (email/SMS/WhatsApp) with the reservation,
  4. record the booking; the payout to the owner is already handled by the
     destination charge (owner gets total - fee, you keep the margin).
"""
from __future__ import annotations

import json
import os


def notify_owner(reservation: dict) -> None:
    """Send the reservation to the owner. Replace with real email/SMS/WhatsApp.

    Reference uses SMTP env vars; swap for SendGrid/Postmark/Twilio as needed.
    """
    to = reservation.get("owner_email")
    if not to:
        print("[webhook] no owner email on reservation; skipping notify")
        return
    subject = f"New booking — {reservation.get('ref')} on {reservation.get('date')}"
    body = (f"New paid booking:\n"
            f"  Route/asset : {reservation.get('ref')}\n"
            f"  Date        : {reservation.get('date')}\n"
            f"  Guests      : {reservation.get('pax')}\n"
            f"  Client phone: {reservation.get('phone')}\n"
            f"  Your payout : €{reservation.get('owner_payout_eur')}\n")
    host = os.environ.get("SMTP_HOST")
    if not host:
        print(f"[webhook] (DRY) would email {to}:\n{subject}\n{body}")
        return
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["From"] = os.environ.get("SMTP_FROM", "bookings@example.com")
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", 587))) as s:
        s.starttls()
        if os.environ.get("SMTP_USER"):
            s.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASS", ""))
        s.send_message(msg)


def handle_event(payload: bytes, sig_header: str) -> dict:
    """Verify + process a Stripe webhook. Returns the parsed reservation."""
    try:
        import stripe  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pip install stripe (reference dependency)") from exc

    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not secret:
        raise RuntimeError("STRIPE_WEBHOOK_SECRET not set")
    event = stripe.Webhook.construct_event(payload, sig_header, secret)

    if event["type"] == "checkout.session.completed":
        meta = event["data"]["object"].get("metadata", {})
        reservation = {
            "ref": meta.get("ref"), "date": meta.get("date"),
            "pax": meta.get("pax"), "phone": meta.get("phone"),
            "owner_email": meta.get("owner_email"),
            "owner_payout_eur": meta.get("owner_payout_eur"),
            "platform_margin_eur": meta.get("platform_margin_eur"),
        }
        notify_owner(reservation)
        # TODO: persist the booking (DB / Airtable / the postgres store)
        return reservation
    return {"ignored": event["type"]}


def handler(request):  # pragma: no cover - serverless adapter
    payload = request.get("rawBody", b"")
    sig = request.get("headers", {}).get("stripe-signature", "")
    result = handle_event(payload, sig)
    return {"statusCode": 200, "body": json.dumps({"ok": True, "result": result})}
