#!/usr/bin/env python3
"""Modèle de marge à deux étages — fourniture de modules PV (montage Voie C).

ByImport fournit des modules à un installateur suisse qui porte l'offre publique.
Ce script chiffre la marge de ByImport sur le poste module et vérifie la
compétitivité de son prix de vente face au prix module marché de l'installateur.

Usage :
    python3 modele_marge.py --puissance-wc 200000 --cout-rendu 0.13 \
            --marge-pct 20 --prix-marche 0.25
    python3 modele_marge.py --aide-hypotheses

Tous les prix sont en CHF par Watt-crête (CHF/Wc), hors TVA, sauf indication.
Stdlib uniquement (Python 3.8+).
"""
import argparse
import sys

HYPOTHESES = """\
Hypothèses et ordres de grandeur (2025-2026 — À RECONFIRMER, marché volatil)
---------------------------------------------------------------------------
  Coût rendu module ByImport    ~0,10–0,15 CHF/Wc
      = prix usine + transport + douane + assurance, TVA import récupérable.
      À établir avec tes devis fournisseurs et ton transitaire.

  Prix module marché installateur CH   ~0,20–0,30 CHF/Wc
      = ce que ton partenaire paie aujourd'hui à son distributeur.
      C'est ton ÉTALON de compétitivité. Demande-le à 2-3 installateurs.

  Marge ByImport cible          15–25 %
  Part module dans le clé en main   ~25–40 %

Stratégie de prix (recommandée) : vise JUSTE SOUS le prix marché de
l'installateur (par défaut 15 % en dessous), pas le prix cassé. Tu maximises
ta marge, tu restes crédible (un prix absurdement bas inquiète sur la qualité),
et tu laisses à l'installateur une vraie économie (~10-20 %).

Règle d'or : Prix vente ByImport < Prix module marché installateur.
Au-dessus, l'installateur achète ailleurs → pas d'offre.

Garde-fou produit : modules Tier-1 certifiés IEC 61215 / 61730 + CE, éligibles
Pronovo. La confiance B2B vient des certifs + garantie, pas d'un prix élevé.
"""


def calcul(puissance_wc, cout_rendu, prix_marche, marge_pct=None, prix_vente=None):
    """Indicateurs financiers du poste module.

    Deux modes de fixation du prix de vente ByImport → installateur :
      - prix_vente (CHF/Wc) : on vise directement un prix, idéalement JUSTE SOUS
        le prix marché de l'installateur (recommandé — maximise la marge tout en
        restant crédible et compétitif) ;
      - marge_pct (%) : on applique une marge sur le coût rendu.
    prix_vente l'emporte s'il est fourni.
    """
    cout_total = puissance_wc * cout_rendu
    if prix_vente is not None:
        prix_vente_wc = prix_vente
    else:
        prix_vente_wc = cout_rendu * (1 + (marge_pct or 0) / 100.0)
    ca_byimport = puissance_wc * prix_vente_wc
    marge_brute = ca_byimport - cout_total
    marge_brute_pct = (marge_brute / ca_byimport * 100.0) if ca_byimport else 0.0

    cout_marche_total = puissance_wc * prix_marche
    economie_installateur = cout_marche_total - ca_byimport
    economie_pct = (economie_installateur / cout_marche_total * 100.0) if cout_marche_total else 0.0
    competitif = prix_vente_wc < prix_marche

    return {
        "puissance_wc": puissance_wc,
        "cout_rendu": cout_rendu,
        "cout_total": cout_total,
        "prix_vente_wc": prix_vente_wc,
        "ca_byimport": ca_byimport,
        "marge_brute": marge_brute,
        "marge_brute_pct": marge_brute_pct,
        "prix_marche": prix_marche,
        "cout_marche_total": cout_marche_total,
        "economie_installateur": economie_installateur,
        "economie_pct": economie_pct,
        "competitif": competitif,
    }


def chf(x):
    return f"CHF {x:,.0f}".replace(",", "'")


def rapport(r):
    lignes = []
    a = lignes.append
    kwc = r["puissance_wc"] / 1000.0
    a("=" * 60)
    a(f"  MODÈLE MARGE 2 ÉTAGES — poste module ({kwc:,.0f} kWc)".replace(",", "'"))
    a("=" * 60)
    a("")
    a("Étage 1 — ByImport (fournisseur module)")
    a(f"  Coût rendu module        {r['cout_rendu']:.3f} CHF/Wc   → {chf(r['cout_total'])}")
    a(f"  Prix vente → installateur {r['prix_vente_wc']:.3f} CHF/Wc   → {chf(r['ca_byimport'])}  (CA ByImport)")
    a(f"  >> Marge brute ByImport  {chf(r['marge_brute'])}  ({r['marge_brute_pct']:.1f} %)")
    a("")
    a("Étage 2 — Compétitivité vs marché installateur")
    a(f"  Prix module marché CH    {r['prix_marche']:.3f} CHF/Wc   → {chf(r['cout_marche_total'])}")
    a(f"  Économie offerte à l'installateur  {chf(r['economie_installateur'])}  ({r['economie_pct']:.1f} %)")
    a("")
    if r["competitif"]:
        a(f"  VERDICT : ✅ COMPÉTITIF — ton prix ({r['prix_vente_wc']:.3f}) < marché ({r['prix_marche']:.3f})")
        a("  L'installateur gagne en compétitivité ET tu prends ta marge.")
    else:
        a(f"  VERDICT : ❌ NON COMPÉTITIF — ton prix ({r['prix_vente_wc']:.3f}) >= marché ({r['prix_marche']:.3f})")
        a("  Renégocie l'usine, change de fournisseur, ou passe ce marché.")
    a("=" * 60)
    return "\n".join(lignes)


def main(argv=None):
    p = argparse.ArgumentParser(description="Modèle de marge à deux étages (modules PV, Voie C).")
    p.add_argument("--puissance-wc", type=float, help="Puissance totale du lot module, en Wc (ex. 200000 = 200 kWc).")
    p.add_argument("--cout-rendu", type=float, help="Coût rendu ByImport, CHF/Wc (prix usine + appro + douane).")
    p.add_argument("--prix-vente", type=float, help="Prix de vente cible ByImport → installateur, CHF/Wc (recommandé : viser juste sous le prix marché).")
    p.add_argument("--marge-pct", type=float, help="Alternative : marge ByImport en %% sur le coût rendu (ignoré si --prix-vente est fourni).")
    p.add_argument("--prix-marche", type=float, help="Prix module marché installateur CH, CHF/Wc (étalon = plafond).")
    p.add_argument("--aide-hypotheses", action="store_true", help="Affiche les hypothèses et ordres de grandeur.")
    args = p.parse_args(argv)

    if args.aide_hypotheses:
        print(HYPOTHESES)
        return 0

    manquants = [n for n, v in (("--puissance-wc", args.puissance_wc),
                                ("--cout-rendu", args.cout_rendu),
                                ("--prix-marche", args.prix_marche)) if v is None]
    if manquants:
        print(f"Paramètres requis manquants : {', '.join(manquants)}", file=sys.stderr)
        print("Lance `python3 modele_marge.py --aide-hypotheses` pour les ordres de grandeur.", file=sys.stderr)
        return 2

    prix_vente = args.prix_vente
    marge_pct = args.marge_pct
    if prix_vente is None and marge_pct is None:
        # Défaut recommandé : prix cible 15 % SOUS le prix marché (juste sous le plafond).
        prix_vente = round(args.prix_marche * 0.85, 4)
        print(f"(défaut : prix cible fixé à 15 % sous le marché = {prix_vente:.3f} CHF/Wc)", file=sys.stderr)

    r = calcul(args.puissance_wc, args.cout_rendu, args.prix_marche,
               marge_pct=marge_pct, prix_vente=prix_vente)
    print(rapport(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
