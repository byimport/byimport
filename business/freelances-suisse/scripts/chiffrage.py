#!/usr/bin/env python3
"""Chiffrage d'une mission freelance FR -> client suisse.

Répond en une commande aux trois seules questions qui comptent avant de renvoyer
un prix : combien ça me coûte, combien je marge, est-ce que je suis au-dessus de
mon plancher.

Exemples
--------
  # Grille complète
  python3 chiffrage.py --liste

  # Un profil de la grille, prix de vente catalogue
  python3 chiffrage.py --profil fullstack-confirme --jours 60

  # Le client négocie à 950 CHF/j
  python3 chiffrage.py --profil fullstack-confirme --vente 950 --jours 60

  # Profil hors grille : achat négocié à 700 EUR/j, vendu 1200 CHF/j
  python3 chiffrage.py --achat-eur 700 --vente 1200 --jours 40

  # Régénérer le tableau markdown de GRILLE_TARIFAIRE.md
  python3 chiffrage.py --table

Sortie : données sur stdout, avertissements sur stderr.
Python 3.8+, stdlib uniquement.
"""

import argparse
import json
import os
import sys

GRILLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grille.json")


# --------------------------------------------------------------------------
# Chargement
# --------------------------------------------------------------------------

def charger_grille(path=GRILLE_PATH):
    with open(path, encoding="utf-8") as fh:
        grille = json.load(fh)
    grille["_index"] = {p["id"]: p for p in grille["profils"]}
    return grille


# --------------------------------------------------------------------------
# Calcul
# --------------------------------------------------------------------------

def chiffrer(achat_eur, vente_chf, jours, fx, plancher_chf=None,
             remise_pct=0.0, delai_client_j=45, delai_freelance_j=30):
    """Calcule l'économie d'une mission. Tous les montants de sortie en CHF."""
    vente_nette = vente_chf * (1 - remise_pct / 100.0)
    cout_chf = achat_eur * fx

    marge_jour = vente_nette - cout_chf
    marge_pct = (marge_jour / vente_nette * 100.0) if vente_nette else 0.0

    # Trésorerie : on paie le freelance avant d'être payé par le client. Le
    # besoin de fonds de roulement est le coût d'achat sur la durée du décalage,
    # plafonné à la durée de la mission.
    jours_decalage = max(delai_client_j - delai_freelance_j, 0)
    jours_ouvres_decalage = min(jours_decalage * 5.0 / 7.0, float(jours))
    bfr_chf = cout_chf * jours_ouvres_decalage

    res = {
        "achat_eur_jour": round(achat_eur, 2),
        "fx_eur_chf": fx,
        "cout_chf_jour": round(cout_chf, 2),
        "vente_chf_jour_catalogue": round(vente_chf, 2),
        "remise_pct": remise_pct,
        "vente_chf_jour_nette": round(vente_nette, 2),
        "marge_chf_jour": round(marge_jour, 2),
        "marge_pct": round(marge_pct, 1),
        "jours": jours,
        "ca_mission_chf": round(vente_nette * jours, 2),
        "cout_mission_chf": round(cout_chf * jours, 2),
        "marge_mission_chf": round(marge_jour * jours, 2),
        "bfr_estime_chf": round(bfr_chf, 2),
    }

    if plancher_chf is not None:
        res["plancher_chf_jour"] = round(plancher_chf, 2)
        res["au_dessus_du_plancher"] = vente_nette >= plancher_chf
        res["marge_vs_plancher_chf"] = round(vente_nette - plancher_chf, 2)

    return res


def verdict(res, marge_cible_pct, marge_plancher_pct):
    """Retourne (statut, message). Statut : OK | ATTENTION | REFUS."""
    if res.get("au_dessus_du_plancher") is False:
        manque = -res["marge_vs_plancher_chf"]
        return ("REFUS",
                "Sous le plancher de {:.0f} CHF/j (il manque {:.0f} CHF/j). "
                "Ne descends pas : remonte le prix ou passe ton chemin."
                .format(res["plancher_chf_jour"], manque))
    if res["marge_pct"] < marge_plancher_pct:
        return ("REFUS",
                "Marge {:.1f}% sous le plancher de {}%. Deal non rentable une "
                "fois les frais de structure absorbés."
                .format(res["marge_pct"], marge_plancher_pct))
    if res["marge_pct"] < marge_cible_pct:
        return ("ATTENTION",
                "Marge {:.1f}% sous la cible de {}%. Acceptable si mission "
                "longue, client récurrent ou compte à ouvrir. Pas en one-shot."
                .format(res["marge_pct"], marge_cible_pct))
    return ("OK",
            "Marge {:.1f}%, au-dessus de la cible de {}%. Envoie."
            .format(res["marge_pct"], marge_cible_pct))


# --------------------------------------------------------------------------
# Rendu
# --------------------------------------------------------------------------

def afficher_texte(res, libelle, statut, message, out):
    largeur = 62
    print("=" * largeur, file=out)
    print("CHIFFRAGE — {}".format(libelle), file=out)
    print("=" * largeur, file=out)
    print("Achat freelance      {:>10.0f} EUR/j  (FX {:.3f})"
          .format(res["achat_eur_jour"], res["fx_eur_chf"]), file=out)
    print("Coût                 {:>10.0f} CHF/j".format(res["cout_chf_jour"]), file=out)
    if res["remise_pct"]:
        print("Vente catalogue      {:>10.0f} CHF/j"
              .format(res["vente_chf_jour_catalogue"]), file=out)
        print("Remise accordée      {:>10.1f} %".format(res["remise_pct"]), file=out)
    print("Vente                {:>10.0f} CHF/j".format(res["vente_chf_jour_nette"]), file=out)
    if "plancher_chf_jour" in res:
        print("Plancher             {:>10.0f} CHF/j".format(res["plancher_chf_jour"]), file=out)
    print("-" * largeur, file=out)
    print("MARGE BRUTE          {:>10.0f} CHF/j   ({:.1f} %)"
          .format(res["marge_chf_jour"], res["marge_pct"]), file=out)
    print("-" * largeur, file=out)
    print("Mission {} jours".format(res["jours"]), file=out)
    print("  CA                 {:>10.0f} CHF".format(res["ca_mission_chf"]), file=out)
    print("  Coût               {:>10.0f} CHF".format(res["cout_mission_chf"]), file=out)
    print("  Marge              {:>10.0f} CHF".format(res["marge_mission_chf"]), file=out)
    print("  Trésorerie à avancer {:>8.0f} CHF".format(res["bfr_estime_chf"]), file=out)
    print("=" * largeur, file=out)
    print("[{}] {}".format(statut, message), file=out)


def afficher_table(grille, out):
    """Génère le tableau markdown de GRILLE_TARIFAIRE.md."""
    p = grille["parametres"]
    fx = p["fx_eur_chf_planification"]

    print("| Profil | Marché FR (€/j) | Achat (€/j) | Coût (CHF/j) | "
          "**Vente (CHF/j)** | Plancher (CHF/j) | Marge (CHF/j) | Marge % | "
          "Réf. ESN GE (CHF/j) | Écart |", file=out)
    print("|---|---|---|---|---|---|---|---|---|---|", file=out)

    for prof in grille["profils"]:
        cout = prof["achat_eur"] * fx
        marge = prof["vente_chf"] - cout
        marge_pct = marge / prof["vente_chf"] * 100.0
        esn_mid = sum(prof["ref_esn_chf"]) / 2.0
        ecart = (prof["vente_chf"] - esn_mid) / esn_mid * 100.0
        print("| {} | {}–{} | {} | {:.0f} | **{}** | {} | {:.0f} | {:.0f}% | "
              "{}–{} | {:.0f}% |".format(
                  prof["libelle"],
                  prof["marche_fr_eur"][0], prof["marche_fr_eur"][1],
                  prof["achat_eur"], cout, prof["vente_chf"], prof["plancher_chf"],
                  marge, marge_pct,
                  prof["ref_esn_chf"][0], prof["ref_esn_chf"][1], ecart), file=out)


def afficher_liste(grille, out):
    print("{:<24} {:<44} {:>10} {:>10}".format("ID", "PROFIL", "VENTE", "PLANCHER"),
          file=out)
    print("-" * 92, file=out)
    for prof in grille["profils"]:
        print("{:<24} {:<44} {:>10} {:>10}".format(
            prof["id"], prof["libelle"],
            "{} CHF".format(prof["vente_chf"]),
            "{} CHF".format(prof["plancher_chf"])), file=out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser():
    ap = argparse.ArgumentParser(
        description="Chiffrage mission freelance FR -> client suisse.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("--profil", help="ID de profil de la grille (voir --liste).")
    ap.add_argument("--achat-eur", type=float,
                    help="Prix d'achat freelance en EUR/jour (hors grille, ou "
                         "pour écraser celui de la grille).")
    ap.add_argument("--vente", type=float,
                    help="Prix de vente client en CHF/jour. Défaut : prix "
                         "catalogue du profil.")
    ap.add_argument("--jours", type=int, default=20,
                    help="Durée de la mission en jours facturés (défaut 20).")
    ap.add_argument("--remise", type=float, default=0.0,
                    help="Remise commerciale en %% appliquée au prix de vente.")
    ap.add_argument("--fx", type=float,
                    help="Taux EUR->CHF. Défaut : taux de planification de la grille.")
    ap.add_argument("--delai-client", type=int, default=45,
                    help="Délai de paiement client en jours calendaires (défaut 45).")
    ap.add_argument("--delai-freelance", type=int, default=30,
                    help="Délai de paiement freelance en jours calendaires (défaut 30).")
    ap.add_argument("--liste", action="store_true", help="Affiche la grille et sort.")
    ap.add_argument("--table", action="store_true",
                    help="Régénère le tableau markdown de GRILLE_TARIFAIRE.md.")
    ap.add_argument("--json", action="store_true", help="Sortie JSON.")
    ap.add_argument("--output", help="Écrit la sortie dans un fichier au lieu de stdout.")
    ap.add_argument("--grille", default=GRILLE_PATH, help="Chemin vers grille.json.")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        grille = charger_grille(args.grille)
    except (OSError, ValueError) as exc:
        print("Impossible de lire la grille ({}) : {}".format(args.grille, exc),
              file=sys.stderr)
        return 2

    params = grille["parametres"]
    out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout

    try:
        if args.liste:
            afficher_liste(grille, out)
            return 0
        if args.table:
            afficher_table(grille, out)
            return 0

        # --- résolution du profil
        prof = None
        if args.profil:
            prof = grille["_index"].get(args.profil)
            if prof is None:
                print("Profil inconnu : {}. Utilise --liste pour les IDs valides."
                      .format(args.profil), file=sys.stderr)
                return 2

        achat = args.achat_eur if args.achat_eur is not None else (
            prof["achat_eur"] if prof else None)
        if achat is None:
            print("Précise --profil ou --achat-eur.", file=sys.stderr)
            return 2

        vente = args.vente if args.vente is not None else (
            prof["vente_chf"] if prof else None)
        if vente is None:
            print("Précise --vente (aucun prix catalogue sans --profil).",
                  file=sys.stderr)
            return 2

        fx = args.fx if args.fx is not None else params["fx_eur_chf_planification"]
        plancher = prof["plancher_chf"] if prof else None
        libelle = prof["libelle"] if prof else "profil hors grille"

        if prof and args.achat_eur is not None and args.achat_eur != prof["achat_eur"]:
            print("Note : achat forcé à {:.0f} EUR/j (grille : {} EUR/j). Le "
                  "plancher de la grille reste appliqué."
                  .format(args.achat_eur, prof["achat_eur"]), file=sys.stderr)

        res = chiffrer(achat, vente, args.jours, fx, plancher_chf=plancher,
                       remise_pct=args.remise,
                       delai_client_j=args.delai_client,
                       delai_freelance_j=args.delai_freelance)
        statut, message = verdict(res, params["marge_brute_cible_pct"],
                                  params["marge_brute_plancher_pct"])
        res["profil"] = args.profil or None
        res["libelle"] = libelle
        res["statut"] = statut
        res["message"] = message

        if args.json:
            json.dump(res, out, ensure_ascii=False, indent=2)
            out.write("\n")
        else:
            afficher_texte(res, libelle, statut, message, out)

        return 0 if statut != "REFUS" else 1
    finally:
        if args.output:
            out.close()


if __name__ == "__main__":
    sys.exit(main())
