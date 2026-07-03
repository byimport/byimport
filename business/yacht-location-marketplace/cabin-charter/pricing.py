"""Moteur de tarification à la couchette (cabin charter).

Principe : au lieu de louer le bateau entier à un seul client, chaque
couchette est vendue individuellement, avec un léger sur-prix unitaire.
Vendu complet, le bateau rapporte 20–40 % de plus que la location entière —
c'est le levier « diviser par couchette pour augmenter le chiffre d'affaires ».

Toute la logique tient dans `price_berths()` ; stdlib pure, aucune dépendance.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BerthPricing:
    """Résultat de tarification pour un bateau donné (par jour)."""

    tarif_net_jour_eur: int          # ce qu'on doit au propriétaire (tarif net mandat)
    prix_bateau_entier_eur: int      # prix public location entière (net + marge)
    prix_couchette_eur: int          # prix public d'UNE couchette
    couchettes: int
    ca_plein_eur: int                # CA si toutes les couchettes sont vendues
    uplift_vs_bateau_entier: float   # ex. 0.32 = +32 % vs location entière
    couchettes_seuil_rentabilite: int  # couchettes vendues pour couvrir le tarif net
    couchettes_min_depart: int       # seuil de départ (rentabilité + remplissage min)


def _round_to(value: float, step: int) -> int:
    return int(round(value / step) * step)


def _ceil_to(value: float, step: int) -> int:
    return int(math.ceil(value / step) * step)


def price_berths(
    tarif_net_jour_eur: int,
    couchettes: int,
    *,
    marge: float = 0.25,
    uplift_couchette: float = 1.30,
    remplissage_min: float = 0.5,
) -> BerthPricing:
    """Calcule les prix publics entier + à la couchette pour un bateau.

    - ``marge`` : marge cible sur le tarif net (0.25 = prix public entier à net × 1,25).
    - ``uplift_couchette`` : sur-prix unitaire de la couchette vs sa quote-part du
      bateau entier. 1.30 → un bateau vendu complet à la couchette rapporte ~30 %
      de plus que loué en entier. Rester ≤ 1.4 : au-delà, le client compare avec
      la location entière à plusieurs et l'écart devient visible.
    - ``remplissage_min`` : fraction de couchettes vendues en dessous de laquelle
      on ne confirme pas la sortie (on rembourse ou reporte).
    """
    if tarif_net_jour_eur <= 0:
        raise ValueError("tarif_net_jour_eur doit être > 0")
    if couchettes <= 0:
        raise ValueError("couchettes doit être > 0")
    if marge < 0 or uplift_couchette < 1 or not 0 < remplissage_min <= 1:
        raise ValueError("paramètres hors bornes (marge ≥ 0, uplift ≥ 1, 0 < remplissage ≤ 1)")

    prix_entier = _round_to(tarif_net_jour_eur * (1 + marge), 10)
    prix_couchette = _ceil_to(prix_entier / couchettes * uplift_couchette, 5)
    ca_plein = prix_couchette * couchettes
    uplift = ca_plein / prix_entier - 1

    seuil_rentabilite = min(couchettes, math.ceil(tarif_net_jour_eur / prix_couchette))
    min_depart = min(couchettes, max(seuil_rentabilite, math.ceil(couchettes * remplissage_min)))

    return BerthPricing(
        tarif_net_jour_eur=tarif_net_jour_eur,
        prix_bateau_entier_eur=prix_entier,
        prix_couchette_eur=prix_couchette,
        couchettes=couchettes,
        ca_plein_eur=ca_plein,
        uplift_vs_bateau_entier=round(uplift, 4),
        couchettes_seuil_rentabilite=seuil_rentabilite,
        couchettes_min_depart=min_depart,
    )
