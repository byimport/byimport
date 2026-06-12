# Étape 3 — Acheter sur 1688 depuis la France

1688.com est la plateforme B2B domestique d'Alibaba : prix usine réels (souvent 30-60 % sous
AliExpress et 20-40 % sous Alibaba.com), mais une plateforme **en chinois, pensée pour des
acheteurs en Chine**. Trois conséquences pratiques :

1. Les fournisseurs ne livrent qu'à une **adresse en Chine** → il faut un agent d'achat.
2. Le paiement passe par Alipay/WeChat Pay côté chinois → l'agent paie pour vous.
3. Pas de protection acheteur internationale → l'inspection qualité de l'agent est votre seule
   protection avant expédition.

## 1. Les agents d'achat (la voie normale)

L'agent fournit : adresse d'entrepôt en Chine, achat pour votre compte, consolidation de
plusieurs fournisseurs en un seul colis, photos/inspection, choix du transporteur, déclaration
export. Agents établis utilisés par les acheteurs francophones :

| Agent | Commission | Points forts |
|---|---|---|
| CSSBuy | ~3-5 % | Interface 1688 intégrée (coller l'URL produit), entrepôt consolidation |
| Superbuy | ~5 % | Inspection photo détaillée incluse, bon support |
| KakoBuy / CNFans / Mulebuy | ~3-5 % | Alternatifs récents, vérifier la réputation au moment de l'achat |
| Agent privé (via contact) | 5-8 % négociable | Pertinent à partir de ~2 000 €/mois d'achats : sourcing actif, négociation MOQ, contrôle qualité renforcé |

Process type avec un agent web :
1. Trouver le produit sur 1688 (recherche par image — coller une photo — marche très bien,
   ou traduire la requête en chinois via Google Translate / l'app 1688).
2. Coller l'URL 1688 dans l'interface de l'agent, choisir variante et quantité, payer en CB/PayPal.
3. L'agent achète, reçoit sous 2-7 jours dans son entrepôt, envoie photos de contrôle.
4. Vous validez, choisissez la ligne de transport, payez le fret au poids volumétrique.
5. Réception en France 10-30 jours selon la ligne (voir `MARGES_ET_COUTS.md`).

## 2. Choisir le fournisseur sur 1688

Indicateurs fiables sur la fiche fournisseur :
- **诚信通 (Cheng Xin Tong)** + ancienneté ≥ 3 ans : abonnement vérifié Alibaba, gage de sérieux minimal.
- **Note ≥ 4.5** sur les 3 axes (description, livraison, service).
- **Taux de réachat (回头率) ≥ 15-20 %** : le meilleur signal — d'autres revendeurs recommandent en achetant à nouveau.
- **实力商家 ("Super Factory" / badge force)** : usine auditée, pas un simple négociant.
- Préférer une **usine (工厂)** à un **grossiste (经销商)** dès que le volume dépasse quelques
  centaines d'unités ; au début, le grossiste est acceptable et a des MOQ plus bas.

Pièges classiques :
- Prix d'appel affiché = palier de quantité le plus haut (ex. ≥ 1000 pcs). Le vrai prix pour
  20-100 pcs est dans le tableau des paliers (起批量).
- Photos volées : demander à l'agent des photos réelles avant validation d'un gros lot.
- Variante par défaut = la moins chère (mauvaise couleur/taille). Toujours préciser la variante
  exacte à l'agent, en capture d'écran.

## 3. Séquence d'achat anti-risque

**Jamais de gros lot d'entrée.** La séquence qui protège la trésorerie :

1. **Échantillon (1-3 unités)** — coût total rendu France souvent 15-40 € avec le fret express.
   Objectif : vérifier qualité réelle, poids réel, rendu photo. C'est aussi votre première
   annonce test sur Leboncoin.
2. **Lot test (20-50 unités)** — uniquement si l'échantillon est bon ET que l'annonce test a
   généré des contacts/une vente en < 2 semaines. Fret : ligne économique air (10-15 j) ou
   maritime groupé si > 20 kg.
3. **Réassort (100+ unités)** — uniquement quand le lot test tourne à ≥ 5 ventes/semaine.
   Négocier le palier de prix supérieur et passer au maritime pour diviser le fret par 3-4.

À chaque étape, recalculer la marge réelle avec `scripts/marge_calc.py` en remplaçant les
estimations par les coûts constatés (poids réel, fret facturé, prix de vente effectif).

## 4. Alternatives à 1688 selon le cas

- **Alibaba.com** : interface anglaise, paiement Trade Assurance, fournisseurs habitués à
  l'export — 20-40 % plus cher que 1688 mais sans agent. Bon pour démarrer si le chinois rebute.
- **AliExpress** : pour les échantillons uniquement (unité chère, mais zéro friction).
- **Grossistes UE (BigBuy, vidaXL B2B…)** : marge plus faible mais produits déjà conformes CE,
  livraison 3-5 jours, pas de douane. Pertinent pour tester la demande avant d'importer soi-même.
