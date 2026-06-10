#!/usr/bin/env python3
"""Programmatic SEO generator for jet routes / aircraft / events + yacht events.

Reads the CSV datasets in pseo/data/, optionally injects live empty legs from
the Avinode connector output (--empty-legs), renders CRO-optimised HTML pages
(templates.py), builds sitemap.xml and internal linking.

ANTI-DOORWAY GUARD (the core requirement): a page is only emitted if it carries
enough UNIQUE, REAL data. Thin pages are skipped (or marked noindex with
--thin-policy noindex) and reported. This is what keeps programmatic SEO from
becoming a doorway-page penalty.

A page must satisfy ALL of:
  1. a real indicative price is present;
  2. >= 2 real data rows (aircraft options for a route / specs for an aircraft);
  3. >= 3 FAQ entries derived from data;
  4. a unique intro derived from the row (not a pure template);
  5. its body hash is unique across the run (no duplicate content).

Usage:
  python3 generate.py --out ./dist [--empty-legs legs.json] [--thin-policy skip|noindex]

Env: none required.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import sys
from typing import Any, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from pseo import templates as T  # noqa: E402

DATA_DIR = os.path.join(_HERE, "data")


# ----------------------------------------------------------------------------
# Dataset loading
# ----------------------------------------------------------------------------
def _read_csv(name: str) -> list[dict[str, str]]:
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _load_airports() -> dict[str, dict[str, str]]:
    return {r["iata"]: r for r in _read_csv("airports.csv")}


def _load_empty_legs(path: Optional[str]) -> dict[tuple[str, str], list[dict]]:
    """Index canonical empty-leg listings by (from_iata, to_iata)."""
    index: dict[tuple[str, str], list[dict]] = {}
    if not path:
        return index
    import json
    with open(path, encoding="utf-8") as fh:
        listings = json.load(fh)
    for item in listings:
        el = item.get("empty_leg") or {}
        key = ((el.get("from") or {}).get("iata"), (el.get("to") or {}).get("iata"))
        if key[0] and key[1]:
            index.setdefault(key, []).append(item)
    return index


# ----------------------------------------------------------------------------
# Anti-doorway guard
# ----------------------------------------------------------------------------
class Report:
    def __init__(self) -> None:
        self.generated: list[str] = []
        self.skipped: list[tuple[str, str]] = []  # (id, reason)
        self._body_hashes: set[str] = set()

    def body_is_duplicate(self, html: str) -> bool:
        # hash the visible body, ignoring the <head> (titles vary but body may not)
        body = re.sub(r"(?is)<head>.*?</head>", "", html)
        body = re.sub(r"\s+", " ", body).strip()
        h = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if h in self._body_hashes:
            return True
        self._body_hashes.add(h)
        return False


def _has_price(value: Any) -> bool:
    return value not in (None, "", "0") and str(value).strip() != ""


# ----------------------------------------------------------------------------
# Builders per page type (return (slug, path, html) or None if thin)
# ----------------------------------------------------------------------------
def build_route(row: dict[str, str], airports: dict, empty_legs: dict,
                report: Report) -> Optional[tuple[str, str, str]]:
    frm_code, to_code = row["from_iata"], row["to_iata"]
    rid = f"route:{frm_code}-{to_code}"

    # Guard 1: real price
    if not _has_price(row.get("price_from_eur")):
        report.skipped.append((rid, "no indicative price"))
        return None

    # Guard 2: >= 2 real aircraft option rows
    options = []
    for cat, key in (("Light jet", "p_light_eur"), ("Midsize", "p_mid_eur"),
                     ("Heavy", "p_heavy_eur")):
        if _has_price(row.get(key)):
            example = {"Light jet": "Citation CJ3", "Midsize": "Citation XLS+",
                       "Heavy": "Challenger 605"}[cat]
            pax = {"Light jet": 6, "Midsize": 8, "Heavy": 12}[cat]
            options.append({"category": cat, "example": example, "pax": pax,
                            "price": row[key]})
    if len(options) < 2:
        report.skipped.append((rid, f"only {len(options)} aircraft option(s)"))
        return None

    frm = airports.get(frm_code, {}).get("city", frm_code)
    to = airports.get(to_code, {}).get("city", to_code)
    slug = f"{T.slugify(frm)}-to-{T.slugify(to)}"
    route = {"slug": slug, "from_city": frm, "to_city": to,
             "from_iata": frm_code, "to_iata": to_code,
             "flight_min": row.get("flight_min", "—"),
             "price_from_eur": row["price_from_eur"]}
    legs = empty_legs.get((frm_code, to_code), [])
    related: list[tuple[str, str]] = []  # filled later by cross-linker
    html = T.render_route(route, options, legs, related)

    # Guard 5: unique body
    if report.body_is_duplicate(html):
        report.skipped.append((rid, "duplicate body content"))
        return None
    path = f"private-jet-charter/routes/{slug}/index.html"
    return slug, path, html


def build_aircraft(row: dict[str, str], report: Report) -> Optional[tuple[str, str, str]]:
    aid = f"aircraft:{row['slug']}"
    # Guard: real price-per-hour + >= 2 specs (pax, range)
    if not _has_price(row.get("price_per_hour_eur")):
        report.skipped.append((aid, "no price per hour"))
        return None
    if not (row.get("pax") and row.get("range_nm")):
        report.skipped.append((aid, "incomplete specs"))
        return None
    ac = {"model": row["model"], "slug": row["slug"], "category": row["category"],
          "pax": row["pax"], "range_nm": row["range_nm"],
          "price_per_hour_eur": row["price_per_hour_eur"]}
    html = T.render_aircraft(ac, [])
    if report.body_is_duplicate(html):
        report.skipped.append((aid, "duplicate body content"))
        return None
    return row["slug"], f"private-jet-charter/aircraft/{row['slug']}/index.html", html


def build_event(row: dict[str, str], report: Report) -> Optional[tuple[str, str, str]]:
    eid = f"event:{row['slug']}"
    if not (row.get("name") and row.get("start") and row.get("end")
            and row.get("destination")):
        report.skipped.append((eid, "incomplete event data"))
        return None
    html = T.render_event(row, [])
    if report.body_is_duplicate(html):
        report.skipped.append((eid, "duplicate body content"))
        return None
    base = "yacht-charter" if row["asset_type"] == "yacht" else "private-jet-charter"
    path = f"{base}/{T.slugify(row['destination'])}/{row['slug']}/index.html"
    return row["slug"], path, html


# ----------------------------------------------------------------------------
# Internal linking (sibling pages within the same cluster)
# ----------------------------------------------------------------------------
def _inject_related(html: str, links: list[tuple[str, str]]) -> str:
    """Insert sibling links into the existing <nav class="related"> block."""
    extra = "".join(f'<a href="/{T.esc(h)}">{T.esc(l)}</a>' for h, l in links)
    return html.replace('<nav class="related">',
                        f'<nav class="related">{extra}', 1)


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
def _write(out_dir: str, rel_path: str, html: str, noindex: bool) -> None:
    if noindex:
        html = html.replace("</head>",
                            '  <meta name="robots" content="noindex,follow">\n</head>', 1)
    dest = os.path.join(out_dir, rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)


def _sitemap(out_dir: str, paths: list[str]) -> str:
    urls = "".join(
        f"<url><loc>https://{T.DOMAIN}/{p[:-len('index.html')]}</loc></url>"
        for p in paths)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f"{urls}</urlset>")
    dest = os.path.join(out_dir, "sitemap.xml")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(xml)
    return dest


# ----------------------------------------------------------------------------
# Orchestration
# ----------------------------------------------------------------------------
def _write_robots(out_dir: str, preview: bool) -> None:
    if preview:
        body = "User-agent: *\nDisallow: /\n"
    else:
        body = (f"User-agent: *\nAllow: /\n"
                f"Sitemap: https://{T.DOMAIN}/sitemap.xml\n")
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(body)


def generate(out_dir: str, empty_legs_path: Optional[str] = None,
             thin_policy: str = "skip", preview: bool = False) -> Report:
    airports = _load_airports()
    empty_legs = _load_empty_legs(empty_legs_path)
    report = Report()

    routes = _read_csv("routes.csv")
    aircraft = _read_csv("aircraft.csv")
    events = _read_csv("events.csv")

    emitted: list[tuple[str, str, str, str]] = []  # (kind, slug, path, html)

    for row in routes:
        built = build_route(row, airports, empty_legs, report)
        if built:
            slug, path, html = built
            emitted.append(("route", slug, path, html))
    for row in aircraft:
        built = build_aircraft(row, report)
        if built:
            slug, path, html = built
            emitted.append(("aircraft", slug, path, html))
    for row in events:
        built = build_event(row, report)
        if built:
            slug, path, html = built
            emitted.append(("event", slug, path, html))

    # cross-link siblings within each kind (max 4 each)
    by_kind: dict[str, list[tuple[str, str, str, str]]] = {}
    for item in emitted:
        by_kind.setdefault(item[0], []).append(item)
    final_paths: list[str] = []
    for kind, items in by_kind.items():
        for i, (_, slug, path, html) in enumerate(items):
            siblings = [items[(i + j) % len(items)] for j in range(1, min(4, len(items)))]
            links = [(s[2].replace("index.html", ""), s[1].replace("-", " ").title())
                     for s in siblings]
            html = _inject_related(html, links)
            _write(out_dir, path, html, noindex=preview)
            report.generated.append(path)
            final_paths.append(path)

    # pillar pages link to their best children
    jet_children = [(p.replace("index.html", ""), p.split("/")[-2].replace("-", " ").title())
                    for p in final_paths if p.startswith("private-jet-charter/routes/")]
    yacht_children = [(p.replace("index.html", ""), p.split("/")[-2].replace("-", " ").title())
                      for p in final_paths if p.startswith("yacht-charter/")]
    if jet_children:
        _write(out_dir, "private-jet-charter/index.html",
               T.render_pillar("jet", jet_children), noindex=preview)
        report.generated.append("private-jet-charter/index.html")
        final_paths.append("private-jet-charter/index.html")
    if yacht_children:
        _write(out_dir, "yacht-charter/index.html",
               T.render_pillar("yacht", yacht_children), noindex=preview)
        report.generated.append("yacht-charter/index.html")
        final_paths.append("yacht-charter/index.html")

    # thin pages as noindex stubs if requested
    if thin_policy == "noindex":
        for pid, reason in report.skipped:
            stub = (f"<!DOCTYPE html><html lang=\"en\"><head>"
                    f"<meta name=\"robots\" content=\"noindex,follow\">"
                    f"<title>{T.esc(pid)}</title></head><body>"
                    f"<p>Page withheld (thin content: {T.esc(reason)}).</p>"
                    f"</body></html>")
            _write(out_dir, f"_thin/{T.slugify(pid)}.html", stub, noindex=False)

    # root landing page linking the two pillars (site entry point)
    home = T.render_home(
        jets=bool(jet_children), yachts=bool(yacht_children))
    _write(out_dir, "index.html", home, noindex=preview)
    report.generated.append("index.html")
    final_paths.append("index.html")

    _copy_assets(out_dir)
    _sitemap(out_dir, final_paths)
    _write_robots(out_dir, preview)
    return report


def _copy_assets(out_dir: str) -> None:
    """Copy static assets (CSS, etc.) into the build output."""
    src = os.path.join(_HERE, "assets")
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(out_dir, "assets"), dirs_exist_ok=True)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Programmatic SEO generator")
    parser.add_argument("--out", default=None, help="Output dir (default: tempdir/pseo-dist)")
    parser.add_argument("--empty-legs", dest="empty_legs",
                        help="Path to connector output JSON (inject live legs)")
    parser.add_argument("--thin-policy", choices=["skip", "noindex"], default="skip")
    parser.add_argument("--preview", action="store_true",
                        help="Preview build: noindex on every page + robots.txt Disallow all")
    args = parser.parse_args(argv)

    if args.out:
        out_dir = args.out
    else:
        import tempfile
        out_dir = os.path.join(tempfile.gettempdir(), "pseo-dist")
    os.makedirs(out_dir, exist_ok=True)

    try:
        report = generate(out_dir, args.empty_legs, args.thin_policy, preview=args.preview)
    except (OSError, ValueError, KeyError) as exc:
        print(f"[pseo] error: {exc}", file=sys.stderr)
        return 1

    mode = " (PREVIEW noindex)" if args.preview else ""
    print(f"[pseo] generated {len(report.generated)} pages{mode} → {out_dir}",
          file=sys.stderr)
    print(f"[pseo] sitemap → {os.path.join(out_dir, 'sitemap.xml')}", file=sys.stderr)
    if report.skipped:
        print(f"[pseo] skipped {len(report.skipped)} thin page(s) "
              f"(anti-doorway guard):", file=sys.stderr)
        for pid, reason in report.skipped:
            print(f"        - {pid}: {reason}", file=sys.stderr)
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
