# Recherche de prix Alibaba — validation du shortlist (juin 2026)

Vérification des prix d'achat réels pour les produits du shortlist
(`scripts/produits_candidats.csv`), faite sur les pages grossistes d'Alibaba.com.
Règle de conversion : **les prix 1688 sont en général 20 à 40 % sous Alibaba.com**
pour le même produit (1688 est le canal domestique chinois, Alibaba.com le canal
export avec marge intermédiaire). Les CNY du CSV visent donc le bas de la
fourchette Alibaba constatée.

**Limite assumée :** les prix ci-dessous sont des fourchettes de pages
"showroom" Alibaba au moment de la recherche — le prix réel dépend de la
variante, du palier de quantité et du fournisseur. Avant tout achat de lot,
confirmer le prix exact sur la fiche 1688 via l'agent (SOURCING_1688.md §2),
au palier de quantité visé. Mise à jour à refaire à chaque réassort.

## Constats par produit

| Produit | Prix Alibaba constaté | MOQ constaté | Estimation 1688 retenue (CSV) |
|---|---|---|---|
| Organiseur de coffre pliable | 1,86–2,75 $ (MOQ 50) ; 3,23–4,25 $ (MOQ 500, imperméable) ; 0,80–0,88 $ (non-tissé entrée de gamme) | dès 50 pcs | **16 CNY (~2,05 €)** — milieu de gamme Oxford |
| Fontaine à eau chat 2 L | entrée 1,89 $ ; gamme courante jusqu'à ~16 $ ; modèles 2 L CE inox/plastique au milieu | dès 1–16 pcs | **38 CNY (~4,85 €)** — 2 L plastique pompe silencieuse |
| Harnais chien réfléchissant no-pull | 3,05–3,55 $ (MOQ 30) ; 4,10–5,20 $ (MOQ 10) ; MOQ usine standard 100–500 | dès 10–50 pcs | **20 CNY (~2,55 €)** |
| Sangles de musculation (suspension) | sets ~3,69 $ ; fourchette large 0,21–11,50 $ selon qualité | dès 1–20 sets | **28 CNY (~3,60 €)** — set complet sangles + ancrage |
| Lampe d'atelier LED USB | 10–20 $ pour les modèles puissants (MOQ 10) ; petits modèles COB nettement moins | dès 2–10 pcs | **28 CNY (~3,60 €)** — petit modèle COB, à confirmer sur 1688 |

Côté marché France : les fontaines 2 L se vendent couramment 25–40 € neuves sur
Amazon.fr (best-sellers de la catégorie "fontaines pour chats") — le prix médian
Leboncoin retenu dans le CSV est ajusté à 39 € pour rester sous Amazon tout en
gardant la marge.

## Effet sur le classement (scénario maritime 3 €/kg, livraison FR incluse)

Après mise à jour des prix, sortie de `score_produits.py` :

1. **Organiseur de coffre auto** — coût complet 10,61 €, prix conseillé x3 = 31,82 €,
   marché 35 € → **GO** (x3,30, ~24 € de marge par vente). Le prix Alibaba réel
   (~2 $ au lieu de l'estimation initiale ~4,9 $) fait passer ce produit de
   GO PRUDENT à GO.
2. **Fontaine à eau chat 2 L** — coût 14,15 €, prix conseillé 42,45 €, marché 39 €
   → GO PRUDENT (x2,76, ~25 € de marge). Vendre à 39-42 €.
3. **Organiseur de visserie** — coût 17,43 €, prix conseillé 52,28 €, marché 49 €
   → GO PRUDENT (x2,81, ~32 € de marge — la meilleure marge absolue du panel).

Rappel : en aérien (11 €/kg), tous ces produits repassent NO-GO. La totalité de
la livraison (fret Chine + livraison France) est ce qui décide de la marge —
d'où l'importance du maritime groupé et de la remise en main propre.

## Sources

- [Alibaba — showroom pet drinking water fountain](https://www.alibaba.com/showroom/pet-drinking-water-fountain.html)
- [Alibaba — fiche 2L Cat Water Fountain (usine)](https://www.alibaba.com/product-detail/Factory-Wholesale-2L-Cat-Water-Fountain_1601397891120.html)
- [Alibaba — showroom folding car trunk organizer](https://www.alibaba.com/showroom/folding-car-trunk-organizer.html)
- [Alibaba — showroom wholesale foldable car trunk organizer](https://www.alibaba.com/showroom/wholesale-foldable-car-trunk-organizer.html)
- [Alibaba — fiche harnais chien réfléchissant no-pull](https://www.alibaba.com/product-detail/Wholesale-Dog-Harness-Adjustable-Reflective-No_1600743030531.html)
- [Alibaba — showroom dog harness low MOQ](https://www.alibaba.com/showroom/dog-harness-low-moq.html)
- [Made-in-China — recherche dog harness (prix 3,05–3,55 $ MOQ 30)](https://www.made-in-china.com/products-search/hot-china-products/Dog_Harness.html)
- [Alibaba — showroom suspension trainer](https://www.alibaba.com/showroom/suspension-trainer.html)
- [Alibaba — showroom TRX suspension trainer](https://www.alibaba.com/showroom/trx-suspension-trainer.html)
- [Alibaba — showroom rechargeable LED work lights](https://www.alibaba.com/showroom/rechargeable-led-work-lights.html)
- [Amazon.fr — best-sellers fontaines pour chats](https://www.amazon.fr/gp/bestsellers/pet-supplies/2036596031)
