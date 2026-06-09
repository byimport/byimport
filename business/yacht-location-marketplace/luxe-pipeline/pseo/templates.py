#!/usr/bin/env python3
"""HTML page builders (stdlib only) for programmatic SEO pages.

Renders the CRO-optimised on-page template from LUXE_MODULE_3_SEO.md §3.3:
price above the fold, 4-field quote form, WhatsApp/Call CTAs, live empty legs,
aircraft price table, FAQ, internal linking and JSON-LD (Service/Offer/
FAQPage/BreadcrumbList). No Jinja2 — plain functions + html.escape.
"""
from __future__ import annotations

import html
import json
import os
from typing import Any, Optional

from pseo import pricing


def _load_branding() -> dict:
    """Brand identity, overridable without touching code.

    Priority: env vars (SITE_BRAND/SITE_DOMAIN/SITE_PHONE/SITE_WHATSAPP) >
    branding.json at the luxe-pipeline root > placeholder defaults.
    Fill branding.json (copy branding.example.json) with your real values to
    move from PREVIEW placeholders to a production-ready site.
    """
    defaults = {"brand": "{{BRAND}}", "domain": "example.com",
                "phone": "+377 00 00 00 00", "whatsapp": "00000000000"}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg_path = os.path.join(root, "branding.json")
    if os.path.isfile(cfg_path):
        try:
            with open(cfg_path, encoding="utf-8") as fh:
                defaults.update({k: v for k, v in json.load(fh).items() if v})
        except (OSError, ValueError):
            pass
    return {
        "brand": os.environ.get("SITE_BRAND", defaults["brand"]),
        "domain": os.environ.get("SITE_DOMAIN", defaults["domain"]),
        "phone": os.environ.get("SITE_PHONE", defaults["phone"]),
        "whatsapp": os.environ.get("SITE_WHATSAPP", defaults["whatsapp"]),
    }


_BRANDING = _load_branding()
BRAND = _BRANDING["brand"]
DOMAIN = _BRANDING["domain"]
WA_NUMBER = _BRANDING["whatsapp"]
PHONE = _BRANDING["phone"]


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _jsonld(obj: dict) -> str:
    return (f'<script type="application/ld+json">'
            f'{json.dumps(obj, ensure_ascii=False)}</script>')


def _head(title: str, description: str, canonical: str, ld_blocks: list[dict]) -> str:
    blocks = "\n  ".join(_jsonld(b) for b in ld_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  {blocks}
</head>
<body>"""


def _trust_bar() -> str:
    return ('<nav class="trust-bar"><span>&#10003; Quote &lt; 2h</span>'
            '<span>&#10003; 24/7</span><span>&#10003; Certified operators</span>'
            '<span>&#10003; Full discretion</span></nav>')


def price_headline(total, unit: str = "total") -> str:
    """Per-person headline (÷ group size) shown WITH the real total + basis.

    Compliant display: the per-person figure attracts, the total and the
    'N guests' basis are always visible right next to it.
    """
    pp = pricing.per_person(total)
    amt = pricing.to_amount(total)
    if pp is None or amt is None:
        return '<p class="subhead">Price on request &middot; pay by card</p>'
    return (f'<p class="subhead">From <strong>&euro;{pp:,} / person</strong> '
            f'<span class="price-basis">({pricing.GROUP_SIZE} guests &middot; '
            f'&euro;{amt:,.0f} {esc(unit)} &middot; pay securely by card)</span></p>')


def _quote_form(route_tag: str) -> str:
    return f"""  <form class="quote" action="/api/create-checkout-session" method="post" data-ref="{esc(route_tag)}">
    <input type="hidden" name="ref" value="{esc(route_tag)}">
    <input type="date" name="date" required aria-label="Date">
    <input type="number" name="pax" min="1" max="40" placeholder="Guests" required>
    <input type="tel" name="phone" placeholder="Phone (instant callback)" required>
    <button type="submit" class="btn-book">Book &amp; pay by card &rarr;</button>
  </form>
  <p class="pay-note">Secure card payment &middot; instant booking sent to the owner &middot; full discretion</p>
  <div class="cta-instant">
    <a class="btn-wa" href="https://wa.me/{WA_NUMBER}">WhatsApp now</a>
    <a class="btn-call" href="tel:{esc(PHONE)}">Call {esc(PHONE)}</a>
  </div>"""


def _sticky_cta() -> str:
    return (f'<div class="sticky-cta"><a href="https://wa.me/{WA_NUMBER}">WhatsApp</a>'
            f'<a href="tel:{esc(PHONE)}">Call</a><a href="#top">Get price</a></div>')


def _related(links: list[tuple[str, str]]) -> str:
    items = "".join(f'<a href="{esc(href)}">{esc(label)}</a>' for href, label in links)
    return f'<nav class="related">{items}</nav>'


def _faq_section(faqs: list[tuple[str, str]]) -> str:
    rows = "".join(
        f"<details{' open' if i == 0 else ''}><summary>{esc(q)}</summary>"
        f"<p>{esc(a)}</p></details>" for i, (q, a) in enumerate(faqs))
    return f'<section class="faq"><h2>FAQ</h2>{rows}</section>'


def _faqpage_ld(faqs: list[tuple[str, str]]) -> dict:
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faqs]}


def _breadcrumb_ld(trail: list[tuple[str, str]]) -> dict:
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "item": f"https://{DOMAIN}{path}"}
                for i, (name, path) in enumerate(trail)]}


def _empty_legs_block(legs: list[dict]) -> str:
    if not legs:
        return ""
    rows = []
    for leg in legs:
        el = leg.get("empty_leg") or {}
        ac = (leg.get("jet_specs") or {}).get("aircraft_model") or "Jet"
        disc = el.get("discount_pct_est")
        price = el.get("price")
        rows.append(
            f"<li><b>{esc(el.get('date'))}</b> {esc(ac)} &middot; "
            f"{esc(el.get('seats'))} pax &middot; "
            f"<strong>&euro;{esc(int(price)) if price else '—'}</strong>"
            f"{f' (-{esc(disc)}%)' if disc else ''} "
            f'<a href="/book/{esc(leg.get("id"))}">Reserve</a></li>')
    return (f'<section class="empty-legs"><h2>Live empty legs</h2>'
            f'<ul>{"".join(rows)}</ul></section>')


# ----------------------------------------------------------------------------
# Route page (jet)
# ----------------------------------------------------------------------------
def render_route(route: dict, aircraft_rows: list[dict],
                 empty_legs: list[dict], related: list[tuple[str, str]]) -> str:
    frm, to = route["from_city"], route["to_city"]
    price_from = route["price_from_eur"]
    path = f"/private-jet-charter/routes/{route['slug']}/"
    canonical = f"https://{DOMAIN}{path}"
    title = f"Private Jet Charter {frm} to {to} — Price & Availability | {BRAND}"
    desc = (f"Charter a private jet from {frm} to {to}. Indicative price from "
            f"€{price_from}, {route['flight_min']} min flight. "
            f"Quote in under 2 hours, 24/7. Empty legs available.")

    faqs = [
        (f"How much is a private jet from {frm} to {to}?",
         f"From €{price_from} one way for the smallest suitable jet; the "
         f"final price depends on the aircraft category and the date."),
        (f"How long is the flight {frm} to {to} by private jet?",
         f"About {route['flight_min']} minutes."),
        (f"Can I book {frm} to {to} last minute or same day?",
         "Yes, subject to availability — call us for live options and empty legs."),
    ]
    service_ld = {"@context": "https://schema.org", "@type": "Service",
                  "serviceType": "Private jet charter", "areaServed": [frm, to],
                  "provider": {"@type": "Organization", "name": BRAND,
                               "url": f"https://{DOMAIN}"},
                  "offers": {"@type": "Offer", "priceCurrency": "EUR",
                             "price": str(price_from)}}
    breadcrumb = _breadcrumb_ld([("Private jet charter", "/private-jet-charter/"),
                                 ("Routes", "/private-jet-charter/routes/"),
                                 (f"{frm} to {to}", path)])

    rows = "".join(
        f"<tr><td>{esc(a['category'])}</td><td>{esc(a['example'])}</td>"
        f"<td>{esc(a['pax'])}</td><td>€{esc(a['price'])}</td></tr>"
        for a in aircraft_rows)
    table = (f'<section class="aircraft"><h2>Aircraft &amp; indicative prices — '
             f'{esc(frm)} to {esc(to)}</h2><table><thead><tr><th>Category</th>'
             f'<th>Example</th><th>Pax</th><th>From</th></tr></thead>'
             f'<tbody>{rows}</tbody></table></section>')

    parts = [
        _head(title, desc, canonical, [service_ld, _faqpage_ld(faqs), breadcrumb]),
        '<a id="top"></a>', '<header class="hero">', _trust_bar(),
        f"<h1>Private Jet Charter — {esc(frm)} &rarr; {esc(to)}</h1>",
        price_headline(price_from, unit=f"total · {esc(route['flight_min'])} min flight"),
        _quote_form(route["slug"]), "</header>",
        _empty_legs_block(empty_legs), table, _faq_section(faqs),
        _related(related + [("All private jet charters", "/private-jet-charter/")]),
        _sticky_cta(), "</body></html>",
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Aircraft page (jet)
# ----------------------------------------------------------------------------
def render_aircraft(ac: dict, related: list[tuple[str, str]]) -> str:
    path = f"/private-jet-charter/aircraft/{ac['slug']}/"
    canonical = f"https://{DOMAIN}{path}"
    title = f"{ac['model']} Charter — Price per Hour & Specs | {BRAND}"
    desc = (f"Charter a {ac['model']} ({ac['category']}). From "
            f"€{ac['price_per_hour_eur']}/hour, up to {ac['pax']} passengers, "
            f"{ac['range_nm']} nm range. Quote in under 2 hours.")
    faqs = [
        (f"How much does it cost to charter a {ac['model']}?",
         f"From €{ac['price_per_hour_eur']} per flight hour, plus taxes and fees."),
        (f"How many passengers fit in a {ac['model']}?",
         f"Up to {ac['pax']} passengers."),
        (f"What is the range of the {ac['model']}?",
         f"About {ac['range_nm']} nautical miles."),
    ]
    service_ld = {"@context": "https://schema.org", "@type": "Service",
                  "serviceType": f"{ac['model']} private jet charter",
                  "provider": {"@type": "Organization", "name": BRAND},
                  "offers": {"@type": "Offer", "priceCurrency": "EUR",
                             "price": str(ac["price_per_hour_eur"]),
                             "unitText": "HUR"}}
    breadcrumb = _breadcrumb_ld([("Private jet charter", "/private-jet-charter/"),
                                 ("Aircraft", "/private-jet-charter/aircraft/"),
                                 (ac["model"], path)])
    specs = (f'<section class="aircraft"><h2>{esc(ac["model"])} specifications</h2>'
             f"<table><tbody>"
             f"<tr><th>Category</th><td>{esc(ac['category'])}</td></tr>"
             f"<tr><th>Passengers</th><td>{esc(ac['pax'])}</td></tr>"
             f"<tr><th>Range</th><td>{esc(ac['range_nm'])} nm</td></tr>"
             f"<tr><th>From</th><td>€{esc(ac['price_per_hour_eur'])}/hour</td></tr>"
             f"</tbody></table></section>")
    parts = [
        _head(title, desc, canonical, [service_ld, _faqpage_ld(faqs), breadcrumb]),
        '<a id="top"></a>', '<header class="hero">', _trust_bar(),
        f"<h1>{esc(ac['model'])} Charter</h1>",
        (f'<p class="subhead">{esc(ac["category"])} &middot; up to '
         f"{esc(ac['pax'])} pax &middot; from <strong>€"
         f"{esc(ac['price_per_hour_eur'])}/hour</strong></p>"),
        _quote_form(f"aircraft-{ac['slug']}"), "</header>",
        specs, _faq_section(faqs),
        _related(related + [("All aircraft", "/private-jet-charter/aircraft/")]),
        _sticky_cta(), "</body></html>",
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Event page (yacht or jet)
# ----------------------------------------------------------------------------
def render_event(ev: dict, related: list[tuple[str, str]]) -> str:
    asset = ev["asset_type"]
    base = "/yacht-charter" if asset == "yacht" else "/private-jet-charter"
    verb = "Rent a superyacht" if asset == "yacht" else "Charter a private jet"
    path = f"{base}/{_slugify(ev['destination'])}/{ev['slug']}/"
    canonical = f"https://{DOMAIN}{path}"
    title = f"{ev['name']} — {verb} in {ev['destination']} | {BRAND}"
    desc = (f"{verb} for {ev['name']} ({ev['start']} to {ev['end']}) in "
            f"{ev['destination']}. Limited availability — secure yours early. "
            f"Response in under 2 hours, 24/7.")
    faqs = [
        (f"How do I charter for {ev['name']} in {ev['destination']}?",
         "Send your dates and party size; we confirm availability and a fixed "
         "quote, typically within 2 hours."),
        (f"When should I book for {ev['name']}?",
         f"As early as possible — availability for {ev['destination']} closes "
         f"fast around the event ({ev['start']}–{ev['end']})."),
        ("What is included?",
         "Vessel or aircraft, crew, and logistics; extras (catering, transfers) "
         "are quoted on request."),
    ]
    event_ld = {"@context": "https://schema.org", "@type": "Event",
                "name": ev["name"], "startDate": ev["start"], "endDate": ev["end"],
                "location": {"@type": "Place", "name": ev["destination"]}}
    breadcrumb = _breadcrumb_ld([(verb, base + "/"),
                                 (ev["destination"], f"{base}/{_slugify(ev['destination'])}/"),
                                 (ev["name"], path)])
    parts = [
        _head(title, desc, canonical, [event_ld, _faqpage_ld(faqs), breadcrumb]),
        '<a id="top"></a>', '<header class="hero">', _trust_bar(),
        f"<h1>{esc(verb)} — {esc(ev['name'])}</h1>",
        (f'<p class="subhead">{esc(ev["destination"])} &middot; '
         f"{esc(ev['start'])} to {esc(ev['end'])}</p>"),
        _quote_form(f"event-{ev['slug']}"), "</header>",
        _faq_section(faqs),
        _related(related + [("More charters", base + "/")]),
        _sticky_cta(), "</body></html>",
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Pillar pages
# ----------------------------------------------------------------------------
def render_pillar(asset_type: str, child_links: list[tuple[str, str]]) -> str:
    if asset_type == "jet":
        path, h1 = "/private-jet-charter/", "Private Jet Charter"
        intro = ("On-demand private jet charter across Europe and beyond. Fixed "
                 "quotes, certified operators, and live empty-leg deals.")
    else:
        path, h1 = "/yacht-charter/", "Luxury Yacht Charter"
        intro = ("Crewed superyacht and day charters in the Mediterranean's top "
                 "destinations, for the season's marquee events.")
    canonical = f"https://{DOMAIN}{path}"
    title = f"{h1} — Prices, Routes & Availability | {BRAND}"
    breadcrumb = _breadcrumb_ld([(h1, path)])
    links = "".join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in child_links)
    parts = [
        _head(title, intro, canonical, [breadcrumb]),
        '<a id="top"></a>', '<header class="hero">', _trust_bar(),
        f"<h1>{esc(h1)}</h1>", f'<p class="subhead">{esc(intro)}</p>',
        _quote_form(f"pillar-{asset_type}"), "</header>",
        f'<section class="cluster"><h2>Popular {esc(h1.lower())}</h2>'
        f"<ul>{links}</ul></section>", _sticky_cta(), "</body></html>",
    ]
    return "\n".join(parts)


def render_home(*, jets: bool, yachts: bool) -> str:
    """Site root landing page linking to the pillars."""
    canonical = f"https://{DOMAIN}/"
    title = f"Private Jet & Superyacht Charter | {BRAND}"
    intro = ("On-demand private jet and luxury yacht charter. Fixed quotes in "
             "under 2 hours, certified operators, full discretion, 24/7.")
    cards = []
    if jets:
        cards.append('<a class="card" href="/private-jet-charter/">'
                     "<h2>Private jet charter &rarr;</h2>"
                     "<p>Routes, aircraft, live empty legs.</p></a>")
    if yachts:
        cards.append('<a class="card" href="/yacht-charter/">'
                     "<h2>Superyacht charter &rarr;</h2>"
                     "<p>Mediterranean destinations &amp; events.</p></a>")
    breadcrumb = _breadcrumb_ld([(BRAND, "/")])
    parts = [
        _head(title, intro, canonical, [breadcrumb]),
        '<a id="top"></a>', '<header class="hero">', _trust_bar(),
        f"<h1>{esc(BRAND)} — Private Jet &amp; Superyacht Charter</h1>",
        f'<p class="subhead">{esc(intro)}</p>',
        _quote_form("home"), "</header>",
        f'<section class="cluster">{"".join(cards)}</section>',
        _sticky_cta(), "</body></html>",
    ]
    return "\n".join(parts)


def _slugify(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


# expose slugify for the generator
slugify = _slugify
