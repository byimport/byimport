# Monkeys Punk — audit de page (monkeyspunk.io)

Dossier autonome, **sans rapport avec le plugin Toprank**. Conformément à `CLAUDE.md`,
rien ici n'est référencé depuis un skill, `AGENTS.md`, `plugin.json` ou le README racine,
et ni `VERSION` ni `CHANGELOG.md` ne sont touchés.

## Contenu

| Fichier | Rôle |
|---|---|
| [`AUDIT.md`](AUDIT.md) | L'audit : constats vérifiés on-chain, conséquences, plan d'action priorisé |
| [`patches/00-fix-claim-conditions.md`](patches/00-fix-claim-conditions.md) | **Le correctif bloquant** : configuration exacte des claim conditions, vérifiée par simulation |
| [`patches/01-live-mint-price.html`](patches/01-live-mint-price.html) | Branche la copie du mint sur le contrat — **le correctif le plus important** |
| [`patches/02-security.md`](patches/02-security.md) | SRI sur ethers.js, logos de wallet inlinés, CSP |
| [`patches/03-phase-capture.html`](patches/03-phase-capture.html) | Compteur piloté par le contrat + capture d'intérêt |
| [`patches/04-seo-legal.md`](patches/04-seo-legal.md) | Footer, `meta keywords`, polices, pages légales |
| [`scripts/read-claim-conditions.py`](scripts/read-claim-conditions.py) | Rejoue les mesures de l'audit depuis Ethereum mainnet |
| [`scripts/simulate-claim-fix.py`](scripts/simulate-claim-fix.py) | Encode et simule le correctif sans envoyer de transaction |

## Le constat en une ligne

Les 8 phases de mint avancent par **date**, pas par **ventes**. Les phases bon marché ont
expiré sans être vendues : **2 NFT mintés sur 10 000**, et un visiteur se voit aujourd'hui
demander 0,5 ETH (~1 350 $) alors que la page lui promet un mint gratuit.

## Vérifier soi-même

```bash
python3 scripts/read-claim-conditions.py --eth-usd <taux>
```

Lecture seule, stdlib uniquement, aucune clé privée. Le script interroge un nœud Ethereum
public et réimprime le tableau des phases de `AUDIT.md` section 2.

## Ordre d'intervention

1. Couper la publicité Facebook (prix affiché ≠ prix facturé).
2. Rejouer `setClaimConditions()` depuis le dashboard thirdweb — c'est la cause racine,
   et aucun correctif web ne la contourne. La configuration exacte, vérifiée par
   simulation on-chain, est dans [`patches/00-fix-claim-conditions.md`](patches/00-fix-claim-conditions.md).
3. Poser le patch 01 pour que la divergence copie/contrat ne puisse plus réapparaître.
4. Patches 02 à 04 dans la semaine.
