#!/usr/bin/env python3
"""Classement automatique des produits candidats 1688 -> Leboncoin.

Lit un CSV de produits candidats (voir produits_candidats.csv pour le format),
calcule pour chacun le coût de revient et le multiplicateur via le moteur de
marge_calc.py, puis attribue un score 0-100 combinant :

  - demande   (volume de recherche mensuel France, échelle log)        30 %
  - marge     (multiplicateur prix de vente / coût de revient)          35 %
  - marge abs (EUR nets par vente)                                      15 %
  - concurrence (1 = personne, 5 = saturé — inversé)                    10 %
  - risque conformité (1 = aucun, 5 = CE complexe — inversé)            10 %

Disqualification automatique (score forcé à 0, verdict NO-GO) :
  multiplicateur < 2,5, marge absolue < 15 EUR, ou risque_conformite >= 4.

Une colonne "Cible" marque les produits dont la marge nette par vente tombe
dans la bande visée sur Leboncoin (par défaut 20-40 EUR, réglable avec
--marge-min / --marge-max).

Usage :
    python3 score_produits.py produits_candidats.csv [--fret-kg 11] [--marge-min 20 --marge-max 40]

Stdlib uniquement (Python 3.8+).
"""

import argparse
import csv
import math
import sys

from marge_calc import DEFAUTS, MARGE_ABSOLUE_MIN, SEUIL_GO, SEUIL_GO_PRUDENT, cout_revient

COLONNES = ["produit", "volume_recherche_mensuel", "prix_1688_cny", "poids_kg",
            "prix_marche_lbc_eur", "concurrence", "risque_conformite"]

POIDS = {"demande": 0.30, "mult": 0.35, "marge_abs": 0.15, "concurrence": 0.10, "conformite": 0.10}


def score_demande(volume):
    """0-1 sur échelle log : 1 000/mois -> 0, 100 000/mois -> 1."""
    if volume <= 0:
        return 0.0
    return max(0.0, min(1.0, (math.log10(volume) - 3.0) / 2.0))


def score_mult(mult):
    """0-1 linéaire : x2,5 -> 0, x5 -> 1."""
    return max(0.0, min(1.0, (mult - SEUIL_GO_PRUDENT) / 2.5))


def score_marge_abs(marge):
    """0-1 linéaire : 15 EUR -> 0, 60 EUR -> 1."""
    return max(0.0, min(1.0, (marge - MARGE_ABSOLUE_MIN) / 45.0))


def score_inverse_1_5(note):
    """Note 1-5 (1 = favorable) -> 1-0."""
    return max(0.0, min(1.0, (5.0 - note) / 4.0))


def evaluer(ligne, fret_kg, tva_import_pct, tva_vente_pct):
    couts = cout_revient(
        prix_cny=float(ligne["prix_1688_cny"]),
        poids_kg=float(ligne["poids_kg"]),
        taux_cny_eur=DEFAUTS["taux_cny_eur"],
        agent_pct=DEFAUTS["agent_pct"],
        fret_kg=fret_kg,
        douane_pct=DEFAUTS["douane_pct"],
        tva_pct=tva_import_pct,
        livraison_fr=DEFAUTS["livraison_fr"],
        provision_pct=DEFAUTS["provision_pct"],
    )
    prix_vente = float(ligne["prix_marche_lbc_eur"])
    prix_ht = prix_vente / (1.0 + tva_vente_pct / 100.0)
    cout = couts["total"]
    mult = prix_ht / cout if cout else 0.0
    marge_abs = prix_ht - cout
    conformite = float(ligne["risque_conformite"])

    disqualifie = mult < SEUIL_GO_PRUDENT or marge_abs < MARGE_ABSOLUE_MIN or conformite >= 4
    if disqualifie:
        score = 0.0
    else:
        score = 100.0 * (
            POIDS["demande"] * score_demande(float(ligne["volume_recherche_mensuel"]))
            + POIDS["mult"] * score_mult(mult)
            + POIDS["marge_abs"] * score_marge_abs(marge_abs)
            + POIDS["concurrence"] * score_inverse_1_5(float(ligne["concurrence"]))
            + POIDS["conformite"] * score_inverse_1_5(conformite)
        )
    return {
        "produit": ligne["produit"],
        "score": score,
        "cout": cout,
        "mult": mult,
        "marge_abs": marge_abs,
        "prix_marche": prix_vente,
        "prix_conseille": cout * SEUIL_GO * (1.0 + tva_vente_pct / 100.0),
        "verdict": "NO-GO" if disqualifie else ("GO" if mult >= 3.0 else "GO PRUDENT"),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv_path", help="CSV des produits candidats")
    p.add_argument("--fret-kg", type=float, default=DEFAUTS["fret_kg"],
                   help="EUR/kg de fret pour le scénario (défaut: %(default)s, air éco)")
    p.add_argument("--marge-min", type=float, default=20.0,
                   help="bas de la bande de marge cible par vente en EUR (défaut: %(default)s)")
    p.add_argument("--marge-max", type=float, default=40.0,
                   help="haut de la bande de marge cible par vente en EUR (défaut: %(default)s)")
    p.add_argument("--tva-pct", type=float, default=DEFAUTS["tva_pct"],
                   help="TVA import en %% du coût : 20 en franchise (micro), 0 si société assujettie "
                        "qui la récupère (défaut: %(default)s)")
    p.add_argument("--tva-vente-pct", type=float, default=0.0,
                   help="TVA collectée sur les ventes en %% : 0 en franchise, 20 si société assujettie "
                        "(défaut: %(default)s)")
    args = p.parse_args(argv)

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        manquantes = [c for c in COLONNES if c not in (lecteur.fieldnames or [])]
        if manquantes:
            print(f"Colonnes manquantes dans {args.csv_path}: {', '.join(manquantes)}",
                  file=sys.stderr)
            return 1
        resultats = [evaluer(ligne, args.fret_kg, args.tva_pct, args.tva_vente_pct)
                     for ligne in lecteur]

    resultats.sort(key=lambda r: r["score"], reverse=True)

    entete = (f"{'#':>2}  {'Produit':<38} {'Score':>5}  {'Coût':>7}  {'Prix x3':>8}  "
              f"{'Marché':>7}  {'Mult':>5}  {'Marge':>7}  {'Cible':>5}  Verdict")
    print(entete)
    print("-" * len(entete))
    dans_cible = 0
    for i, r in enumerate(resultats, 1):
        cible = (r["verdict"] != "NO-GO"
                 and args.marge_min <= r["marge_abs"] <= args.marge_max)
        dans_cible += cible
        print(f"{i:>2}  {r['produit'][:38]:<38} {r['score']:5.1f}  "
              f"{r['cout']:6.2f}€  {r['prix_conseille']:7.2f}€  "
              f"{r['prix_marche']:6.2f}€  x{r['mult']:4.2f}  "
              f"{r['marge_abs']:6.2f}€  {'OUI' if cible else '—':>5}  {r['verdict']}")
    print()
    ligne_fret = f"Scénario fret : {args.fret_kg:.0f} EUR/kg"
    if args.fret_kg > 3:
        ligne_fret += " — relancer avec --fret-kg 3 pour le scénario maritime."
    print(ligne_fret)
    print("Coût = coût de revient complet par unité, TOUTE la livraison incluse (fret Chine + livraison France).")
    print("Prix x3 = prix de vente conseillé pour la marge cible ; Marché = prix médian Leboncoin constaté.")
    print(f"Cible = marge nette par vente dans la bande {args.marge_min:.0f}-{args.marge_max:.0f} EUR "
          f"({dans_cible}/{len(resultats)} produits).")
    print("Les 2-3 produits de tête marqués OUI sont les candidats à échantillonner (SOURCING_1688.md §3).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
