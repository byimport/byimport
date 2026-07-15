#!/usr/bin/env python3
"""Générateur de pages « location à la couchette » — un port d'Europe par page.

Entrées : data/ports_europe.json (49 ports) + une flotte (par défaut la fixture).
Sorties : dist/index.html (annuaire complet groupé par région), dist/port/<id>.html
(page port : localisation carte, bateaux basés là, tarifs entier + à la couchette),
dist/sitemap.xml.

Garde-fou anti-doorway (même règle que luxe-pipeline/pseo) : les ports SANS bateau
n'ont pas de page dédiée — ils figurent dans l'index en « ouverture prochaine »,
et sont listés sur stderr. Publier 40 pages vides tuerait le SEO du site.

Usage :
    python3 generate.py --out ./dist [--flotte data/flotte_fixture.json]
                        [--marge 0.25] [--uplift 1.30] [--base-url https://example.com]
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pricing import price_berths, price_extra  # noqa: E402

HERE = Path(__file__).resolve().parent

CSS = """
body{font-family:Georgia,serif;max-width:960px;margin:0 auto;padding:24px;color:#1a2332}
h1,h2{font-weight:600} a{color:#0b5394} table{border-collapse:collapse;width:100%;margin:16px 0}
th,td{border:1px solid #cbd5e1;padding:8px 10px;text-align:left;font-size:15px}
th{background:#eef2f7} .prix{font-weight:700;white-space:nowrap} .muted{color:#64748b;font-size:14px}
.badge{background:#eef2f7;border-radius:4px;padding:2px 8px;font-size:13px}
.galerie{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.galerie img{width:220px;height:150px;object-fit:cover;border-radius:6px}
.galerie .attente{width:220px;height:150px;border-radius:6px;display:flex;align-items:center;
justify-content:center;background:linear-gradient(160deg,#0b3954,#1d6fa5);color:#e8f1f8;
font-size:13px;text-align:center;padding:8px;box-sizing:border-box}
footer{margin-top:32px;border-top:1px solid #cbd5e1;padding-top:12px;color:#64748b;font-size:13px}
"""


def _page(title: str, body: str) -> str:
    return (
        "<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
        f"<body>{body}<footer>Tarifs indicatifs par jour, haute saison. "
        "Données de démonstration (flotte fixture) — remplacer par les bateaux sous mandat. "
        "Sortie confirmée à partir du seuil minimal de couchettes vendues ; skipper professionnel inclus."
        "</footer></body></html>"
    )


def _maps_link(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps?q={lat},{lon}"


def _boat_rows(boats: list[dict], marge: float, uplift: float) -> str:
    rows = []
    for b in sorted(boats, key=lambda x: x["tarif_net_jour_eur"]):
        p = price_berths(b["tarif_net_jour_eur"], b["couchettes"], marge=marge, uplift_couchette=uplift)
        rows.append(
            "<tr>"
            f"<td><strong>{html.escape(b['nom'])}</strong><br><span class='muted'>{html.escape(b['modele'])}</span></td>"
            f"<td>{html.escape(b['type'])}</td>"
            f"<td>{b['cabines']} cab. / {b['couchettes']} couch.</td>"
            f"<td class='prix'>{p.prix_couchette_eur} € <span class='muted'>/ couchette</span></td>"
            f"<td class='prix'>{p.prix_bateau_entier_eur} € <span class='muted'>/ bateau</span></td>"
            f"<td class='muted'>départ dès {p.couchettes_min_depart} couchettes · complet : "
            f"+{p.uplift_vs_bateau_entier:.0%} vs location entière</td>"
            "</tr>"
        )
    return (
        "<table><tr><th>Bateau</th><th>Type</th><th>Capacité</th>"
        "<th>Prix / couchette / jour</th><th>Bateau entier / jour</th><th>Conditions</th></tr>"
        + "".join(rows) + "</table>"
    )


def _galerie(boat: dict) -> str:
    """Galerie photo d'un bateau. Sans photos réelles : cadre « photos à venir »
    (jamais de photo d'un autre bateau — la fiche doit montrer LE bateau réservé)."""
    photos = boat.get("photos") or []
    if photos:
        imgs = "".join(
            f"<img src='{html.escape(p['src'])}' alt='{html.escape(p.get('alt', boat['nom']))}' loading='lazy'>"
            for p in photos
        )
    else:
        imgs = (
            f"<div class='attente'>📷 Photos de « {html.escape(boat['nom'])} » en cours de shooting "
            "— reportage réalisé à la signature du mandat</div>"
        )
    return f"<h3>{html.escape(boat['nom'])} — {html.escape(boat['modele'])}</h3><div class='galerie'>{imgs}</div>"


def _extras_table(extras: list[dict]) -> str:
    rows = "".join(
        "<tr>"
        f"<td><strong>{html.escape(e['nom'])}</strong><br><span class='muted'>{html.escape(e['description'])}</span></td>"
        f"<td class='prix'>{price_extra(e['prix_net_eur'], marge=e.get('marge', 0.5))} € "
        f"<span class='muted'>/ {html.escape(e['unite'])}</span></td>"
        "</tr>"
        for e in extras
    )
    return (
        "<h2>Composez votre journée — options à bord</h2>"
        "<p>Chef cuisinier, batelier supplémentaire, photographe… ajoutez-les à la réservation, "
        "à la couchette comme au bateau entier.</p>"
        f"<table><tr><th>Option</th><th>Prix</th></tr>{rows}</table>"
    )


def build(
    out: Path,
    ports: list[dict],
    boats: list[dict],
    marge: float,
    uplift: float,
    base_url: str,
    extras: list[dict] | None = None,
) -> dict:
    by_port: dict[str, list[dict]] = {}
    for b in boats:
        by_port.setdefault(b["port_id"], []).append(b)

    unknown = sorted(set(by_port) - {p["id"] for p in ports})
    if unknown:
        raise SystemExit(f"flotte incohérente : port_id inconnus {unknown}")

    (out / "port").mkdir(parents=True, exist_ok=True)
    generated, skipped = [], []

    for port in ports:
        port_boats = by_port.get(port["id"], [])
        if not port_boats:  # anti-doorway : pas de page sans offre réelle
            skipped.append(port["id"])
            continue
        body = (
            f"<p><a href='../index.html'>← Tous les ports</a></p>"
            f"<h1>Location à la couchette — {html.escape(port['nom'])}</h1>"
            f"<p><span class='badge'>{html.escape(port['pays'])}</span> "
            f"<span class='badge'>{html.escape(port['region'])}</span> "
            f"<span class='badge'>saison : {html.escape(port['saison'])}</span></p>"
            f"<p>📍 Bateaux amarrés à <strong>{html.escape(port['nom'])}</strong> — "
            f"<a href='{_maps_link(port['lat'], port['lon'])}' rel='nofollow'>voir sur la carte</a> "
            f"<span class='muted'>({port['lat']}, {port['lon']})</span></p>"
            "<p>Réservez <strong>une couchette</strong> (cabine partagée par groupe de 2) au lieu du bateau entier : "
            "embarquement à bord avec skipper, prix par personne, départ confirmé dès le seuil minimal atteint.</p>"
            + _boat_rows(port_boats, marge, uplift)
            + "".join(_galerie(b) for b in sorted(port_boats, key=lambda x: x["nom"]))
            + (_extras_table(extras) if extras else "")
        )
        (out / "port" / f"{port['id']}.html").write_text(
            _page(f"Location bateau à la couchette — {port['nom']}", body), encoding="utf-8"
        )
        generated.append(port["id"])

    # Index : TOUS les ports, groupés par région ; sans page = « ouverture prochaine »
    regions: dict[str, list[dict]] = {}
    for port in ports:
        regions.setdefault(port["region"], []).append(port)
    sections = []
    for region in sorted(regions):
        items = []
        for port in sorted(regions[region], key=lambda p: p["nom"]):
            n = len(by_port.get(port["id"], []))
            if n:
                items.append(
                    f"<li><a href='port/{port['id']}.html'>{html.escape(port['nom'])}</a> "
                    f"<span class='badge'>{n} bateau{'x' if n > 1 else ''}</span></li>"
                )
            else:
                items.append(
                    f"<li>{html.escape(port['nom'])} <span class='muted'>— ouverture prochaine</span></li>"
                )
        sections.append(f"<h2>{html.escape(region)}</h2><ul>{''.join(items)}</ul>")
    index_body = (
        "<h1>Location de bateaux à la couchette — ports d'Europe</h1>"
        f"<p class='muted'>{len(ports)} ports couverts · {len(generated)} avec bateaux en ligne · "
        "prix par personne et par jour, skipper inclus.</p>" + "".join(sections)
    )
    (out / "index.html").write_text(_page("Location à la couchette — ports d'Europe", index_body), encoding="utf-8")

    urls = [f"{base_url}/index.html"] + [f"{base_url}/port/{pid}.html" for pid in generated]
    (out / "sitemap.xml").write_text(
        "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"
        + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    return {"generated": generated, "skipped": skipped}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="./dist")
    ap.add_argument("--ports", default=str(HERE / "data" / "ports_europe.json"))
    ap.add_argument("--flotte", default=str(HERE / "data" / "flotte_fixture.json"))
    ap.add_argument("--extras", default=str(HERE / "data" / "extras.json"))
    ap.add_argument("--marge", type=float, default=0.25)
    ap.add_argument("--uplift", type=float, default=1.30)
    ap.add_argument("--base-url", default="https://example.com")
    args = ap.parse_args()

    ports = json.loads(Path(args.ports).read_text(encoding="utf-8"))["ports"]
    boats = json.loads(Path(args.flotte).read_text(encoding="utf-8"))["bateaux"]
    extras = json.loads(Path(args.extras).read_text(encoding="utf-8"))["extras"]
    report = build(Path(args.out), ports, boats, args.marge, args.uplift, args.base_url.rstrip("/"), extras=extras)

    print(
        f"[cabin-charter] {len(report['generated'])} pages port générées, "
        f"{len(report['skipped'])} ports sans bateau skippés (anti-doorway) : "
        + ", ".join(report["skipped"]),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
