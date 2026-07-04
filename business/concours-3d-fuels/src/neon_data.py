"""Acquisition des données NEON pour le concours 3D Surface Fuels.

Deux produits nous intéressent :
  - DP1.30003.001 : nuage de points lidar discret (reconstruction du sous-étage 3D).
  - DP1.10098.001 : structure de végétation ligneuse (vérité terrain pour la validation).

L'API NEON est publique et sans clé. Les tuiles lidar sont volumineuses (~plusieurs Go par
site) : lancer ce module sur une machine avec du disque, pas dans un conteneur éphémère.

Réf : https://data.neonscience.org/data-api  (endpoint /data/{productCode}/{siteCode}/{month})
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import requests

NEON_API = "https://data.neonscience.org/api/v0"
LIDAR_DPID = "DP1.30003.001"          # Discrete return LiDAR point cloud
VEG_STRUCT_DPID = "DP1.10098.001"     # Woody plant vegetation structure


def list_available_months(product: str, site: str) -> list[str]:
    """Retourne les mois (YYYY-MM) disponibles pour un produit/site donné."""
    r = requests.get(f"{NEON_API}/products/{product}", timeout=60)
    r.raise_for_status()
    for s in r.json()["data"]["siteCodes"]:
        if s["siteCode"] == site:
            return sorted(s["availableMonths"])
    return []


def download_product(product: str, site: str, month: str, dest: pathlib.Path) -> list[pathlib.Path]:
    """Télécharge tous les fichiers d'un produit NEON pour un site/mois."""
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(f"{NEON_API}/data/{product}/{site}/{month}", timeout=120)
    r.raise_for_status()
    files = r.json()["data"]["files"]
    saved: list[pathlib.Path] = []
    for f in files:
        out = dest / f["name"]
        if out.exists() and out.stat().st_size == int(f.get("size", 0)):
            saved.append(out)
            continue
        print(f"  ↓ {f['name']} ({int(f.get('size', 0)) / 1e6:.1f} MB)", file=sys.stderr)
        with requests.get(f["url"], stream=True, timeout=600) as resp:
            resp.raise_for_status()
            with open(out, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=1 << 20):
                    fh.write(chunk)
        saved.append(out)
    return saved


def main() -> None:
    p = argparse.ArgumentParser(description="Télécharge lidar + structure végétation NEON")
    p.add_argument("--site", default="SOAP", help="Code site NEON (ex. SOAP, TALL, JORN)")
    p.add_argument("--month", help="YYYY-MM ; si absent, prend le plus récent disponible")
    p.add_argument("--product", choices=["lidar", "veg", "both"], default="both")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("data"))
    args = p.parse_args()

    targets = {"lidar": LIDAR_DPID, "veg": VEG_STRUCT_DPID}
    if args.product != "both":
        targets = {args.product: targets[args.product]}

    for label, dpid in targets.items():
        months = list_available_months(dpid, args.site)
        if not months:
            print(f"[!] Aucun mois disponible pour {dpid} @ {args.site}", file=sys.stderr)
            continue
        month = args.month if args.month in months else months[-1]
        print(f"[{label}] {dpid} @ {args.site} {month}", file=sys.stderr)
        download_product(dpid, args.site, month, args.out / label / args.site / month)


if __name__ == "__main__":
    main()
