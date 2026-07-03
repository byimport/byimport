#!/usr/bin/env python3
"""Générateur de propositions sur-mesure — une offre adaptée à chaque demande.

Entrée : la demande du client (port, nombre de personnes, nombre de jours,
options souhaitées). Sortie : une proposition en Markdown prête à envoyer
(WhatsApp / e-mail), avec systématiquement DEUX options chiffrées :

  1. À la couchette — prix par personne (le bateau part avec d'autres passagers).
  2. Privatisation — le bateau entier rien que pour le groupe.

L'upsell des extras (chef, batelier, photographe…) est intégré au devis.

Usage :
    python3 propose.py --port nice --personnes 4 --jours 1 --extras chef,aperitif
    python3 propose.py --port split --personnes 10 --jours 3 --client "Famille Martin" --output offre.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pricing import price_berths, price_extra  # noqa: E402

HERE = Path(__file__).resolve().parent


def _load(name: str, key: str) -> list[dict]:
    return json.loads((HERE / "data" / name).read_text(encoding="utf-8"))[key]


def compose(
    port_id: str,
    personnes: int,
    jours: int,
    extra_ids: list[str],
    *,
    client: str = "",
    ports: list[dict] | None = None,
    boats: list[dict] | None = None,
    extras_catalogue: list[dict] | None = None,
    marge: float = 0.25,
    uplift: float = 1.30,
) -> str:
    """Construit la proposition Markdown. Lève SystemExit si la demande est insatisfiable."""
    if personnes <= 0 or jours <= 0:
        raise SystemExit("personnes et jours doivent être > 0")

    ports = ports if ports is not None else _load("ports_europe.json", "ports")
    boats = boats if boats is not None else _load("flotte_fixture.json", "bateaux")
    catalogue = {e["id"]: e for e in (extras_catalogue if extras_catalogue is not None else _load("extras.json", "extras"))}

    port = next((p for p in ports if p["id"] == port_id), None)
    if port is None:
        raise SystemExit(f"port inconnu « {port_id} »")
    inconnus = [e for e in extra_ids if e not in catalogue]
    if inconnus:
        raise SystemExit(f"extras inconnus {inconnus} — dispo : {', '.join(sorted(catalogue))}")

    candidats = [b for b in boats if b["port_id"] == port_id and b["couchettes"] >= personnes]
    if not candidats:
        dispo = sorted({b["port_id"] for b in boats})
        raise SystemExit(
            f"aucun bateau de {personnes} couchettes ou plus à {port['nom']} — "
            f"ports avec flotte : {', '.join(dispo)}"
        )

    # Meilleur bateau = le plus petit qui suffit (remplissage plus facile), prix départageant.
    bateau = min(candidats, key=lambda b: (b["couchettes"], b["tarif_net_jour_eur"]))
    p = price_berths(bateau["tarif_net_jour_eur"], bateau["couchettes"], marge=marge, uplift_couchette=uplift)

    total_couchettes = p.prix_couchette_eur * personnes * jours
    total_privatisation = p.prix_bateau_entier_eur * jours

    lignes_extras, total_extras = [], 0
    for eid in extra_ids:
        e = catalogue[eid]
        prix = price_extra(e["prix_net_eur"], marge=e.get("marge", 0.5))
        quantite = jours if e["unite"] == "jour" else 1
        montant = prix * quantite
        total_extras += montant
        lignes_extras.append(
            f"| {e['nom']} | {prix} € / {e['unite']} × {quantite} | **{montant} €** |"
        )

    dest = f" — pour {client}" if client else ""
    md = [
        f"# Votre journée en mer à {port['nom']}{dest}",
        "",
        f"**{personnes} personne{'s' if personnes > 1 else ''} · {jours} jour{'s' if jours > 1 else ''} · "
        f"embarquement : {port['nom']} ({port['region']})**",
        "",
        f"À bord de **« {bateau['nom']} »** ({bateau['modele']}, {bateau['cabines']} cabines / "
        f"{bateau['couchettes']} couchettes), skipper professionnel inclus.",
        "",
        "## Option 1 — À la couchette (prix par personne)",
        "",
        f"- {p.prix_couchette_eur} € / personne / jour × {personnes} pers. × {jours} j = "
        f"**{total_couchettes} €**",
        f"- Vous partagez le bateau avec d'autres passagers (cabine par groupe de 2). "
        f"Départ confirmé dès {p.couchettes_min_depart} couchettes vendues au total.",
        "",
        "## Option 2 — Privatisation totale",
        "",
        f"- Bateau entier : {p.prix_bateau_entier_eur} € / jour × {jours} j = **{total_privatisation} €**",
        "- Le bateau rien que pour vous — horaires et itinéraire à votre main.",
        "",
    ]
    if lignes_extras:
        md += [
            "## Vos options à bord",
            "",
            "| Option | Détail | Montant |",
            "|---|---|---|",
            *lignes_extras,
            "",
            f"**Total options : {total_extras} €**",
            "",
            f"### Totaux tout compris",
            f"- Option couchettes + options : **{total_couchettes + total_extras} €**",
            f"- Option privatisation + options : **{total_privatisation + total_extras} €**",
            "",
        ]
    md += [
        "## Réserver",
        "",
        "Acompte de **30 %** par facture PayPal pour bloquer la date (solde à l'embarquement). "
        "Annulation sans frais jusqu'à J-7. Offre valable 72 h — les disponibilités d'été partent vite.",
        "",
        f"*Saison à {port['nom']} : {port['saison']}. Carburant selon usage ; taxes portuaires incluses.*",
    ]
    return "\n".join(md)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", required=True)
    ap.add_argument("--personnes", type=int, required=True)
    ap.add_argument("--jours", type=int, default=1)
    ap.add_argument("--extras", default="", help="ids séparés par des virgules (ex. chef,aperitif)")
    ap.add_argument("--client", default="", help="nom du client, pour personnaliser l'en-tête")
    ap.add_argument("--output", default="-")
    args = ap.parse_args()

    extra_ids = [e.strip() for e in args.extras.split(",") if e.strip()]
    md = compose(args.port, args.personnes, args.jours, extra_ids, client=args.client)
    if args.output == "-":
        print(md)
    else:
        Path(args.output).write_text(md + "\n", encoding="utf-8")
        print(f"[propose] écrit : {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
