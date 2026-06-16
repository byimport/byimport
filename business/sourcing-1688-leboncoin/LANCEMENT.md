# Plan de lancement — de zéro à la première vente (~30 jours)

Tout ce qui suit est dans l'ordre exact d'exécution. Budget total de lancement :
**~250-300 €** (échantillons + statut gratuit + compte pro). Les seules étapes que
personne ne peut faire à ta place : créer le statut, payer les échantillons,
photographier, cliquer « Publier ».

## Semaine 1 — Statut + commandes échantillons (2 h de travail)

### J1 — Micro-entreprise (30 min, gratuit)
1. Sur autoentrepreneur.urssaf.fr → « Créer mon auto-entreprise ».
2. Activité : **« Achat-revente de marchandises »** (commerce de détail hors magasin, BIC).
3. Option versement libératoire selon ta situation fiscale.
4. Le SIREN arrive sous 1-3 semaines — la suite ne l'attend pas.

### J1 — Commande des échantillons (45 min, ~120-160 €)
Créer un compte sur **CSSBuy** (ou Superbuy). Pour chaque produit : coller le terme
de recherche ci-dessous dans la recherche 1688 de l'agent, trier par taux de réachat
(回头率), choisir un vendeur ≥ 4.5 avec ≥ 3 ans d'ancienneté (SOURCING_1688.md §2),
commander **2 unités** en fret express.

| Produit | Recherche 1688 (coller tel quel) | Cible prix unitaire | Échantillon ×2 rendu (estim.) |
|---|---|---|---|
| Organiseur de coffre | `汽车后备箱收纳箱 折叠 大容量` | ≤ 16 CNY | ~35 € |
| Fontaine à eau chat 2L | `宠物饮水机 2L 静音 过滤` | ≤ 38 CNY | ~40 € |
| Organiseur visserie 24 tiroirs | `零件柜 抽屉式 24格 收纳` | ≤ 45 CNY | ~45 € |
| Sangles suspension | `悬挂训练带 家用 健身 拉力绳` | ≤ 28 CNY | ~35 € |

Consignes à l'agent : variante exacte en capture d'écran, photos d'inspection à
réception, **déclaration en valeur réelle** (CADRE_LEGAL.md §3).

### J2-J3 — Pendant que ça arrive
- [ ] Relever les prix médians réels Leboncoin de ta région pour les 4 produits
      (15 min/produit, DEMANDE_FRANCE.md §1) → ajuster la colonne `prix_marche_lbc_eur`
      du CSV et relancer `score_produits.py`.
- [ ] Préparer le coin photo : drap neutre, fenêtre, mètre ruban (PHOTOS_ANNONCES.md §2).
- [ ] Copier les 4 annonces d'ANNONCES_PRETES.md dans tes notes, remplacer `[VILLE]`.

## Semaine 2-3 — Réception, contrôle, photos (2 h)

- [ ] À réception : contrôle qualité de chaque échantillon — solidité, odeur, finitions,
      poids réel à la balance (→ recalculer la marge avec le poids constaté :
      `python3 scripts/marge_calc.py --prix-cny X --poids-kg RÉEL --prix-vente Y --fret-kg 3`).
- [ ] Un produit déçoit → il sort de la liste, point. C'est le rôle de l'échantillon.
- [ ] Séance photo : 5 photos par produit retenu, check-list PHOTOS_ANNONCES.md §5.
- [ ] SIREN reçu → passer le compte Leboncoin en **compte PRO** avec le SIREN.

## Semaine 3 — Mise en ligne test (30 min)

- [ ] Publier les annonces des produits validés un **jeudi ou dimanche soir**
      (ANNONCES_PRETES.md, photos réelles, prix du scoring).
- [ ] Activer paiement sécurisé + remise en main propre + envoi Mondial Relay.
- [ ] Ouvrir le tableur de suivi : produit, date, vues, contacts, prix.

Les 2 unités d'échantillon SONT le stock de test : l'objectif n'est pas la marge
(le fret express l'a mangée), c'est de **prouver que ça se vend** — un contact ou
une vente sous 14 jours = demande confirmée.

## Semaine 4-5 — Décision lot test

Pour chaque produit, au 14e jour d'annonce :

| Signal | Décision |
|---|---|
| Vendu, ou ≥ 3 contacts sérieux | **Lot test 30-50 unités** en fret maritime/air éco (SOURCING_1688.md §3) — la vraie marge commence ici |
| 1-2 contacts, des vues | Retravailler titre/photos/prix (-10 %), prolonger 7 jours |
| Aucun contact, peu de vues | Abandonner la référence, passer au produit suivant du scoring |

## Récap budget de lancement

| Poste | Montant |
|---|---|
| Micro-entreprise | 0 € |
| Échantillons ×2 des 4 produits, express rendu | ~155 € |
| Compte Leboncoin PRO (1er mois) | ~30-50 € selon formule |
| Matériel photo (drap, rien d'autre) | ~10 € |
| **Total avant première vente** | **~200-220 €** |
| Lot test n°1 (30 u. maritime, déclenché seulement si validation) | ~270-430 € selon produit |

## Ce qu'on ne fait PAS au lancement

- Publier avant d'avoir le produit en main et photographié (litiges + ban).
- Commander un lot avant validation de l'échantillon ET de la demande réelle.
- Vendre en volume sur un compte particulier « en attendant le SIREN ».
- Brader sous le prix plancher du scoring pour « faire du volume » — la marge
  20-40 € par vente est le modèle, pas le chiffre d'affaires.
