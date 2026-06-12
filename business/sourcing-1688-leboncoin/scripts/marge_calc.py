#!/usr/bin/env python3
"""Calculateur de marge 1688 -> Leboncoin.

Implémente le modèle de coûts de MARGES_ET_COUTS.md : coût de revient rendu
France (produit + agent + fret + douane + TVA import + livraison FR + provision
invendus), verdict GO/NO-GO selon le multiplicateur, et prix plancher pour un
multiplicateur cible.

Exemples :
    python3 marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39
    python3 marge_calc.py --prix-cny 35 --poids-kg 0.8 --multiplicateur-cible 3
    python3 marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39 --fret-kg 3 --livraison-fr 0

Stdlib uniquement (Python 3.8+).
"""

import argparse
import sys

# Valeurs par défaut documentées dans MARGES_ET_COUTS.md — à ajuster aux coûts constatés.
DEFAUTS = {
    "taux_cny_eur": 0.128,    # taux de change CNY -> EUR (spread agent inclus)
    "agent_pct": 5.0,         # commission agent d'achat, % du prix produit
    "fret_kg": 11.0,          # EUR/kg facturable (11 = air éco, 18 = express, 3 = maritime groupé)
    "douane_pct": 4.0,        # droits de douane, % de (produit + fret) — vérifier le code TARIC
    "tva_pct": 20.0,          # TVA import (coût sec en franchise de TVA)
    "livraison_fr": 4.50,     # EUR par vente (Mondial Relay ~4,50 ; 0 si remise en main propre)
    "provision_pct": 8.0,     # provision invendus / casse / SAV, % du coût avant livraison
}

SEUIL_GO = 3.0
SEUIL_GO_PRUDENT = 2.5
MARGE_ABSOLUE_MIN = 15.0  # EUR par vente, minimum pour payer le temps de gestion


def cout_revient(prix_cny, poids_kg, taux_cny_eur, agent_pct, fret_kg,
                 douane_pct, tva_pct, livraison_fr, provision_pct):
    """Coût de revient rendu France d'une unité, avec le détail des postes."""
    produit = prix_cny * taux_cny_eur
    agent = produit * agent_pct / 100.0
    fret = poids_kg * fret_kg
    douane = (produit + fret) * douane_pct / 100.0
    tva = (produit + fret + douane) * tva_pct / 100.0
    sous_total = produit + agent + fret + douane + tva
    provision = sous_total * provision_pct / 100.0
    total = sous_total + provision + livraison_fr
    return {
        "produit": produit,
        "agent": agent,
        "fret": fret,
        "douane": douane,
        "tva": tva,
        "provision": provision,
        "livraison_fr": livraison_fr,
        "total": total,
    }


def verdict(multiplicateur, marge_absolue):
    if multiplicateur >= SEUIL_GO and marge_absolue >= MARGE_ABSOLUE_MIN:
        return "GO"
    if multiplicateur >= SEUIL_GO_PRUDENT and marge_absolue >= MARGE_ABSOLUE_MIN:
        return "GO PRUDENT (lot test seulement)"
    return "NO-GO"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--prix-cny", type=float, required=True,
                   help="prix unitaire 1688 en CNY (au palier de quantité visé)")
    p.add_argument("--poids-kg", type=float, required=True,
                   help="poids facturable en kg : max(réel, volumétrique L*l*h/6000)")
    p.add_argument("--prix-vente", type=float,
                   help="prix de vente Leboncoin envisagé en EUR")
    p.add_argument("--multiplicateur-cible", type=float, default=SEUIL_GO,
                   help="multiplicateur cible pour le prix plancher (défaut: %(default)s)")
    for cle, val in DEFAUTS.items():
        p.add_argument("--" + cle.replace("_", "-"), type=float, default=val,
                       help="défaut: %(default)s")
    args = p.parse_args(argv)

    d = cout_revient(args.prix_cny, args.poids_kg, args.taux_cny_eur,
                     args.agent_pct, args.fret_kg, args.douane_pct,
                     args.tva_pct, args.livraison_fr, args.provision_pct)

    print("Coût de revient rendu France (par unité)")
    print(f"  Produit ({args.prix_cny:.0f} CNY)      : {d['produit']:7.2f} EUR")
    print(f"  Agent ({args.agent_pct:.0f} %)            : {d['agent']:7.2f} EUR")
    print(f"  Fret ({args.poids_kg:.2f} kg x {args.fret_kg:.0f}/kg)  : {d['fret']:7.2f} EUR")
    print(f"  Douane ({args.douane_pct:.0f} %)           : {d['douane']:7.2f} EUR")
    print(f"  TVA import ({args.tva_pct:.0f} %)      : {d['tva']:7.2f} EUR")
    print(f"  Provision ({args.provision_pct:.0f} %)        : {d['provision']:7.2f} EUR")
    print(f"  Livraison France      : {d['livraison_fr']:7.2f} EUR")
    print(f"  TOTAL                 : {d['total']:7.2f} EUR")
    print()

    plancher = d["total"] * args.multiplicateur_cible
    print(f"Prix plancher pour x{args.multiplicateur_cible:.1f} : {plancher:.2f} EUR")

    if args.prix_vente is not None:
        mult = args.prix_vente / d["total"] if d["total"] else 0.0
        marge = args.prix_vente - d["total"]
        print()
        print(f"Prix de vente           : {args.prix_vente:.2f} EUR")
        print(f"Marge nette par vente   : {marge:.2f} EUR")
        print(f"Multiplicateur          : x{mult:.2f}")
        print(f"Verdict                 : {verdict(mult, marge)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
