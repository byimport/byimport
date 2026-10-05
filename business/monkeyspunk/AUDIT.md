# monkeyspunk.io — audit de page et de mint

**Date de l'audit :** 4 octobre 2026
**Portée :** page d'accueil `https://monkeyspunk.io/` (version EN + FR) et contrats Ethereum mainnet associés.
**Méthode :** récupération du HTML/JS servi, puis lecture directe des contrats via `eth_call` sur un nœud Ethereum public. Tous les chiffres ci-dessous sont vérifiés on-chain, pas déclaratifs.

---

## 1. Conclusion en une phrase

Le site est bien construit et ses affirmations techniques sont vraies, mais **le mint est structurellement cassé** : les 8 phases de prix sont déclenchées par des *dates*, pas par les *ventes*. Les phases bon marché ont expiré sans être vendues, et un visiteur qui arrive aujourd'hui se voit demander **0,5 ETH (~1 350 $) pour le token #3**, alors que la page lui promet encore un mint gratuit.

**Priorité absolue : reconfigurer les claim conditions avant de dépenser un euro de plus en publicité.**

---

## 2. Preuve on-chain

Contrat NFT : [`0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84`](https://etherscan.io/address/0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84)
`name() = "Monkeys Punk"` · `symbol() = "MPNK"` · `nextTokenIdToMint() = 10000` · **`totalSupply() = 2`**

Les 8 phases de mint, décodées via `getClaimConditionById(uint256)` (prix convertis à 2 702 $/ETH) :

| # | Ouverture (UTC) | État | Offre | **Mintés** | Prix ETH | ≈ USD |
|---|---|---|---|---|---|---|
| 0 | 2026-09-01 22:00 | expirée | 1 000 | **2** | 0 | gratuit |
| 1 | 2026-09-04 22:00 | expirée | 7 699 | **0** | 0,005 | 14 $ |
| 2 | 2026-09-10 22:00 | expirée | 700 | **0** | 0,05 | 135 $ |
| 3 | 2026-09-18 22:00 | expirée | 300 | **0** | 0,15 | 405 $ |
| 4 | 2026-09-28 22:00 | **ACTIVE** | 250 | **0** | 0,50 | **1 351 $** |
| 5 | 2026-10-05 22:00 | à venir | 45 | 0 | 10 | 27 023 $ |
| 6 | 2026-10-17 22:00 | à venir | 5 | 0 | 100 | 270 232 $ |
| 7 | 2026-10-30 22:00 | à venir | 1 | 0 | 1 111 | 3 002 278 $ |

Somme des offres : 10 000 ✅ · Total minté depuis le lancement : **2**

---

## 3. Ce que ça implique concrètement

### 3.1 Le mint ne peut plus aboutir (bloquant)

thirdweb active toujours **la dernière phase dont la date d'ouverture est passée**. Les phases ne s'enchaînent donc pas quand une marche est vendue — elles s'enchaînent quand l'horloge tourne. Résultat :

- **998 NFT gratuits ont été détruits par l'horloge.** La phase 0 a vécu 3 jours et a été réclamée 2 fois. C'était tout le budget d'acquisition de communauté.
- **La phase principale — 7 699 NFT à 14 $, soit 77 % de la collection — a expiré en 6 jours avec 0 vente.** Elle est désormais inatteignable.
- **Demain 5 octobre, le prix passe à 10 ETH (~27 000 $)** pour minter le token #3. Puis 270 000 $. Puis, le 30 octobre, le seul token disponible coûtera **3,0 M$**.
- Le dénouement du récit (« The First, token #10000, le 30 octobre ») est **mathématiquement inatteignable** : il faudrait que les tokens #3 à #9 999 soient mintés d'abord, et leurs phases sont expirées.

### 3.2 La page contredit le contrat (risque juridique)

La page affiche toujours :

> 🟢 1 000 gratuits (allowlist) → 0.005 → 0.05 → 0.15 → 0.5 → 10 → 100 → **1 111 ETH**

Le contrat, lui, facture **0,5 ETH tout de suite**. Un visiteur venu de la publicité Facebook lit « mint gratuit » et se voit demander ~1 350 $. Avec du trafic payant et une audience européenne, c'est une exposition en publicité trompeuse, pas seulement un problème de conversion.

### 3.3 Il n'y a jamais eu d'allowlist

Les 8 phases ont un **merkle root nul**. La phase « 1 000 gratuits (allowlist) » était en réalité un mint public ouvert, 1 par wallet, pendant 3 jours, sans annonce. Le mot « allowlist » dans la copie n'a aucune contrepartie technique.

### 3.4 L'économie $PUNK tourne à vide

Les 4 pools de staking sont réellement financés (vérifié) : 70 M + 15 M + 10 M + 5 M = **100 M $PUNK**, soit 40 % du supply de 250 M. Mais ils ne servent que **2 NFT éligibles**. Par ailleurs, aux taux affichés et à 100 % de staking, les pools premium s'épuisent vite :

| Pool | Financé | Émission/jour | Autonomie |
|---|---|---|---|
| Common + Uncommon | 70 M | 86 990 | ~804 j |
| Rare + Vis. + Epic | 15 M | 125 000 | **~120 j** |
| Legendary + Mythic | 10 M | 100 000 | **~100 j** |
| The First | 5 M | 50 000 | **~100 j** |

Les tiers vendus comme les plus désirables ont la plus courte autonomie, et 1 250 Rare se partagent un pool plus petit que 8 699 Commons. À corriger (refill par les royalties, ou émission dégressive, ou durée de programme annoncée) avant que quelqu'un ne publie le calcul.

---

## 4. Ce qui est bon et qu'il faut garder

- **Les affirmations « already live » sont vraies et vérifiables.** Contrat déployé, 10 000 tokens lazy-mintés, métadonnées sur IPFS, pools de staking réellement approvisionnés. C'est rare, et c'est le meilleur actif de confiance du projet — il est enterré au milieu de la page.
- **Le propriétaire garde le contrôle :** `owner()` = `0x0f4d…536d`, également `primarySaleRecipient()`. La reconfiguration est donc possible immédiatement.
- **Technique propre :** 106 Ko d'HTML → 34 Ko gzippé, aucun JS externe au chargement initial, les 11 visuels d'art inlinés en PNG de ~1 Ko (256²/512²), `alt` sur 100 % des images, un seul `<h1>`, `loading="lazy"`.
- **SEO de base carré :** canonical, hreflang EN/FR réciproque, sitemap, robots.txt, 5 blocs JSON-LD valides. Les 8 raretés totalisent exactement 10 000 et les pourcentages sont justes.
- **Le compteur gère proprement son expiration** (il remplace le bloc par le CTA au lieu d'afficher des négatifs).
- Le bouton **MINT NOW** existe bien et pointe vers la page de claim thirdweb — il est injecté par JS, donc invisible dans le HTML source.

---

## 5. Plan d'action, par ordre de priorité

| # | Action | Où | Urgence |
|---|---|---|---|
| 1 | **Couper la publicité Facebook** tant que le prix affiché ≠ prix facturé | Meta Ads | immédiat |
| 2 | **Reconfigurer les claim conditions** : une seule phase active, prix d'entrée réel, `maxClaimableSupply` = offre restante. Avancer la marche *manuellement* quand elle est vendue, jamais par date. Configuration exacte et vérifiée : `patches/00-fix-claim-conditions.md` | dashboard thirdweb (`setClaimConditions`, `onlyOwner`) | immédiat |
| 3 | **Brancher la copie sur le contrat** pour que la divergence ne puisse plus réapparaître | `patches/01-live-mint-price.html` | immédiat |
| 4 | Retirer le mot « allowlist » ou implémenter un vrai merkle root | copie + contrat | 24 h |
| 5 | SRI sur ethers.js + logos de wallet inlinés | `patches/02-security.md` | 24 h |
| 6 | Capture d'e-mail/wallet pour la prochaine phase | `patches/03-phase-capture.html` | 48 h |
| 7 | Nettoyage SEO (footer bourré de mots-clés, `meta keywords`), polices auto-hébergées, mentions légales + CGU + confidentialité | `patches/04-seo-legal.md` | 1 semaine |
| 8 | Revoir l'économie de staking (autonomie des pools premium) | whitepaper + contrats | avant la reprise du mint |
| 9 | Remonter le bloc « DEPLOYED & VERIFIED » juste sous le hero | copie | 1 semaine |
| 10 | Ajouter un lien X/Twitter (le `meta twitter:site = @MonkeysPunk` existe, le lien non) | copie | 1 semaine |

### Précision de vocabulaire à corriger

La page écrit « ERC-721, audited ». Le contrat est un proxy minimal pointant vers l'implémentation partagée `0xf685…e097` : c'est un *template* audité, pas un audit du déploiement. Écrire « built on an audited ERC-721 drop standard » — aussi rassurant, et exact. Un lecteur technique qui repère la nuance perd confiance sur tout le reste.

---

## 6. Reproduire les mesures

```bash
RPC=https://ethereum-rpc.publicnode.com
A=0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84

# offre mintée à ce jour
curl -s -X POST $RPC -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"'$A'","data":"0x18160ddd"},"latest"]}'

# phase active (getActiveClaimConditionId)
curl -s -X POST $RPC -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"'$A'","data":"0xc68907de"},"latest"]}'
```

`scripts/read-claim-conditions.py` dans ce dossier décode les 8 phases et reproduit le tableau de la section 2.
