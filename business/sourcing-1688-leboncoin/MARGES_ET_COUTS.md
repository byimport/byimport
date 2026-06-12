# Étape 4 — Structure de coûts complète et seuils de rentabilité

Le calculateur `scripts/marge_calc.py` implémente exactement ce modèle. Ce document explique
chaque poste pour que les paramètres par défaut puissent être ajustés à la réalité constatée.

## 1. Le coût de revient rendu France (par unité)

```
coût de revient = prix 1688 (CNY→EUR)
                + commission agent (% du prix produit)
                + fret international (€/kg × poids facturable)
                + droits de douane (% sur valeur produit + fret)
                + TVA à l'import (20 % sur valeur + fret + droits)   [récupérable si assujetti]
                + livraison France par vente (Mondial Relay / Colissimo)
                + provision invendus & SAV (% du coût)
```

### Détail des postes

| Poste | Valeur par défaut | Notes |
|---|---|---|
| Taux CNY → EUR | 0,128 | Vérifier le taux du jour ; les agents prennent souvent 1-2 % de spread |
| Commission agent | 5 % | CSSBuy/Superbuy ~3-5 % + frais fixes mineurs |
| Fret air économique | 11 €/kg | 10-15 jours, le bon choix pour les lots tests < 20 kg |
| Fret express (échantillons) | 18 €/kg | 5-8 jours |
| Fret maritime groupé | 3 €/kg | 35-50 jours, minimum ~20-30 kg, pour les réassorts |
| Poids facturable | max(réel, volumétrique) | Volumétrique = L×l×h (cm) / 6000 en aérien |
| Droits de douane | 4 % | Varie de 0 à 12 % selon le code SH du produit — vérifier sur la base TARIC |
| TVA import | 20 % | Due dès le 1er € depuis juillet 2021 (plus d'exonération < 22 €). Assiette : valeur + fret + droits |
| Livraison France | 4,50 € | Mondial Relay ~4-5 € jusqu'à 1 kg ; 0 € si remise en main propre |
| Provision invendus/SAV | 8 % | Casse, retours, unités bradées en fin de lot |

### Sur la TVA — deux situations

- **Micro-entrepreneur en franchise de TVA** (cas de départ) : la TVA d'import est un **coût
  sec** non récupérable. C'est le défaut du calculateur.
- **Assujetti à la TVA** (au-delà des seuils de franchise, ou sur option) : la TVA d'import se
  récupère, mais il faut alors **collecter 20 % sur les ventes**. Sur Leboncoin face à des
  particuliers, c'est généralement perdant — le prix affiché est TTC dans la tête de l'acheteur.
  Rester sous la franchise tant que le CA le permet (seuil franchise TVA ventes de biens :
  vérifier le seuil de l'année en cours, ~85 000 €).

## 2. Côté revenus : ce que Leboncoin coûte

- **Annonce de base particulier** : gratuite — mais ce modèle exige un compte PRO (voir
  `CADRE_LEGAL.md`), donc prévoir le **forfait pro** (de l'ordre de quelques dizaines d'€/mois
  selon le volume d'annonces — devis Leboncoin PRO) amorti sur les ventes du mois.
- **Options de visibilité** ("À la une", remontée) : 2-7 € par annonce. À n'utiliser que sur les
  produits dont la marge absolue dépasse ~30 €.
- **Paiement sécurisé Leboncoin** : la commission de protection est payée par **l'acheteur** ;
  le vendeur reçoit le prix affiché. L'expédition est soit incluse dans le prix, soit payée par
  l'acheteur selon le réglage de l'annonce.

## 3. Les seuils de décision (implémentés dans `marge_calc.py`)

| Indicateur | Seuil | Décision |
|---|---|---|
| Multiplicateur (prix de vente ÷ coût de revient) | ≥ 3,0 | GO |
| | 2,5 – 3,0 | GO prudent (lot test seulement) |
| | < 2,5 | NO-GO — chercher un autre produit ou un meilleur palier de prix |
| Marge nette absolue par vente | ≥ 15 € | Minimum pour payer le temps de gestion (photos, messages, colis) |
| Délai d'écoulement estimé du lot | ≤ 8 semaines | Au-delà, le cash dort et le risque de démodage monte |

## 4. Exemple chiffré complet

Organiseur de coffre auto, 35 CNY sur 1688, 0,8 kg, vendu 39 € sur Leboncoin (médiane constatée
des annonces) :

```
Produit : 35 CNY × 0,128            =  4,48 €
Agent 5 %                            =  0,22 €
Fret air éco : 0,8 kg × 11 €/kg      =  8,80 €
Droits 4 % × (4,48 + 8,80)           =  0,53 €
TVA 20 % × (4,48 + 8,80 + 0,53)      =  2,76 €
Provision 8 % (hors livraison FR)    =  1,34 €
Livraison France                     =  4,50 €
                                      --------
Coût de revient rendu                ≈ 22,64 €
Prix de vente                        = 39,00 €  → multiplicateur ≈ 1,7  → NO-GO en aérien
```

Le même produit en **maritime groupé** (3 €/kg) tombe à ≈ 14,0 € de coût de revient
(multiplicateur 2,8 → GO prudent), et avec **remise en main propre** (économie de 4,50 €)
à ≈ 9,5 € (multiplicateur 4,1 → GO). Conclusion type : sur les produits ≤ 50 €, c'est le mode
de transport et la livraison qui décident de la rentabilité, pas le prix 1688. D'où la séquence
échantillon (air express, marge ignorée) → lot test (air éco) → réassort (maritime) décrite dans
`SOURCING_1688.md`.

Vérification en une commande :

```bash
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39                 # air éco
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39 --fret-kg 3     # maritime
python3 scripts/marge_calc.py --prix-cny 35 --poids-kg 0.8 --prix-vente 39 --fret-kg 3 --livraison-fr 0
```
