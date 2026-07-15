#!/usr/bin/env python3
"""Collecteur de leads B2B — partenaires apporteurs autour d'un port.

Cible les APPORTEURS D'AFFAIRES (hôtels, maisons d'hôtes, agences de voyage,
marinas) dans un rayon autour du port : eux parlent chaque jour à nos clients
finals. Source : OpenStreetMap via l'API Overpass — données ouvertes (licence
ODbL), coordonnées professionnelles publiques, zéro donnée personnelle.

⚖️ Garde-fous (non optionnels) :
- B2B uniquement. Ne JAMAIS utiliser ce script pour collecter des particuliers :
  la prospection B2C à froid sur données scrapées est illégale (RGPD/ePrivacy).
- La prospection B2B reste soumise au droit local (opt-out, mentions, LCD suisse,
  ePrivacy par pays) — voir LUXE_MODULE_2_LEADGEN.md pour les règles d'envoi.
- Attribution ODbL : « © les contributeurs d'OpenStreetMap » sur toute
  republication des données.

Usage :
    python3 collect_partners.py --port nice --rayon 3000 --output leads_nice.csv
    python3 collect_partners.py --port nice --fixture tests/fixtures/overpass_nice.json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORTS_JSON = HERE.parent / "data" / "ports_europe.json"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CATEGORIES = {  # tag OSM -> libellé lead
    ("tourism", "hotel"): "hôtel",
    ("tourism", "guest_house"): "maison d'hôtes",
    ("office", "travel_agent"): "agence de voyage",
    ("leisure", "marina"): "marina",
}


def _query(lat: float, lon: float, rayon_m: int) -> str:
    clauses = "".join(
        f'  node["{k}"="{v}"](around:{rayon_m},{lat},{lon});\n'
        f'  way["{k}"="{v}"](around:{rayon_m},{lat},{lon});\n'
        for k, v in CATEGORIES
    )
    return f"[out:json][timeout:60];\n(\n{clauses});\nout center tags;\n"


def _distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return int(2 * r * math.asin(math.sqrt(a)))


def parse_elements(payload: dict, port_lat: float, port_lon: float) -> list[dict]:
    """Transforme la réponse Overpass en leads triés par distance au port."""
    leads = []
    for el in payload.get("elements", []):
        tags = el.get("tags", {})
        nom = tags.get("name")
        if not nom:
            continue  # sans nom = inexploitable pour un premier contact
        categorie = next(
            (label for (k, v), label in CATEGORIES.items() if tags.get(k) == v), None
        )
        if categorie is None:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        adresse = " ".join(
            filter(None, (tags.get("addr:housenumber"), tags.get("addr:street"), tags.get("addr:city")))
        )
        leads.append(
            {
                "nom": nom,
                "categorie": categorie,
                "site_web": tags.get("website") or tags.get("contact:website") or "",
                "telephone": tags.get("phone") or tags.get("contact:phone") or "",
                "adresse": adresse,
                "distance_m": _distance_m(port_lat, port_lon, float(lat), float(lon)),
                "source": "OpenStreetMap (ODbL) — © les contributeurs d'OpenStreetMap",
            }
        )
    leads.sort(key=lambda x: (x["distance_m"], x["nom"]))
    return leads


def fetch_overpass(lat: float, lon: float, rayon_m: int) -> dict:
    req = urllib.request.Request(
        OVERPASS_URL,
        data=("data=" + urllib.parse.quote(_query(lat, lon, rayon_m))).encode(),
        headers={"User-Agent": "cabin-charter-partners/1.0 (prospection B2B partenaires)"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def write_csv(leads: list[dict], out) -> None:
    fields = ["nom", "categorie", "site_web", "telephone", "adresse", "distance_m", "source"]
    w = csv.DictWriter(out, fieldnames=fields)
    w.writeheader()
    w.writerows(leads)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", required=True, help="id du port (voir data/ports_europe.json)")
    ap.add_argument("--rayon", type=int, default=3000, help="rayon en mètres (défaut 3000)")
    ap.add_argument("--output", default="-", help="CSV de sortie (défaut stdout)")
    ap.add_argument("--fixture", help="réponse Overpass JSON locale (mode hors-ligne)")
    args = ap.parse_args()

    ports = {p["id"]: p for p in json.loads(PORTS_JSON.read_text(encoding="utf-8"))["ports"]}
    if args.port not in ports:
        raise SystemExit(f"port inconnu « {args.port} » — ids valides : {', '.join(sorted(ports))}")
    port = ports[args.port]

    if args.fixture:
        payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    else:
        payload = fetch_overpass(port["lat"], port["lon"], args.rayon)

    leads = parse_elements(payload, port["lat"], port["lon"])
    print(f"[leads] {port['nom']} : {len(leads)} partenaires potentiels (rayon {args.rayon} m)", file=sys.stderr)

    if args.output == "-":
        write_csv(leads, sys.stdout)
    else:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            write_csv(leads, f)
        print(f"[leads] écrit : {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
