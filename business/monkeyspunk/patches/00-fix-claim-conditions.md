# PATCH 00 — Réparer le mint (action bloquante, vérifiée par simulation)

> **C'est le seul correctif qui débloque réellement le projet.** Les patches 01 à 04
> rendent la page honnête ; celui-ci répare la cause racine. Il demande la clé du
> propriétaire : aucun agent, aucun connecteur ne peut l'exécuter à ta place.

**Vérifié le 5 octobre 2026 à 12:32 UTC** — phase active n°4 (0,5 ETH), `totalSupply` = 2.

## La cause racine en une phrase

Les 8 phases avancent sur `startTimestamp` (par **date**), alors que l'échelle de prix
annoncée est une échelle de **rareté par numéro de token** (par **vente**). thirdweb
active toujours la dernière phase dont la date est passée, donc l'horloge a doublé les
ventes et abandonné l'invendu de chaque phase.

**On ne change pas l'économie du projet — on change seulement le déclencheur.**

## Étape 1 — Urgence : un seul appel, tout de suite

Un `setClaimConditions` avec un tableau d'**un** élément remplace les 8 phases.
Effet immédiat : le prix redevient celui annoncé, et la marche à 10 ETH disparaît.

| Champ | Valeur | Pourquoi |
|---|---|---|
| `startTimestamp` | `0` | toujours ouverte — **ne peut plus jamais expirer** |
| `maxClaimableSupply` | `8697` | bande Common+Uncommon (8 699) moins les 2 déjà mintés |
| `quantityLimitPerWallet` | `5` | identique à leur phase 1 d'origine |
| `merkleRoot` | `0x00…00` | pas d'allowlist (voir la note plus bas) |
| `pricePerToken` | `5000000000000000` | 0,005 ETH — le prix réellement annoncé |
| `currency` | `0xEeee…eEeE` | sentinel ETH natif, identique aux conditions existantes |
| `metadata` | `ipfs://QmVvUrbnwT1FMhkvFyvxwsTE5kFbLohsGEj7qK2YWHvzuq/0` | repris de la phase 1 |

Et `_resetClaimEligibility = true` (la nouvelle condition prend l'id 8 ; les quotas
par wallet des anciennes phases ne bloquent personne).

### Voie recommandée : le dashboard thirdweb

Contrat `0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84`, onglet **Claim Conditions** :
supprimer les 8 phases, en créer **une seule** avec les valeurs du tableau, publier.
La transaction est signée par le wallet propriétaire `0x0f4d…536d`.

### Voie experte : la calldata déjà encodée et simulée

```
to:   0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84
from: 0x0f4d3ea5525046254a2b58c23f694eb1c781536d
gas:  ~600913
data: 0x74bc7db70000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000021f90000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011c37937e08000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000037697066733a2f2f516d56765572626e775431464d686b764679767877735445356b46624c6f687347456a37714b32595748767a75712f30000000000000000000
```

## Preuve de la simulation (aucune transaction envoyée)

`eth_simulateV1` exécute l'appel sur l'état réel de la chaîne sans l'écrire :

| Contrôle | Résultat |
|---|---|
| `setClaimConditions` depuis le propriétaire | `status = 0x1` (réussit) |
| le même appel depuis `0x…dEaD` | `execution reverted` → `onlyOwner` confirmé |
| `getActiveClaimConditionId()` après | `8` |
| `claimCondition()` après | `currentStartId = 8`, `count = 1` |
| condition 8 après | start `0`, supply `8697`, claimed `0`, 5/wallet, `0.005 ETH`, merkle nul |
| **condition 5 (10 ETH) après** | **start 0, supply 0, prix 0 → phase supprimée** |

Reproduire : `scripts/simulate-claim-fix.py`.

## Étape 2 — Les marches suivantes, à l'avancement par vente

Quand `supplyClaimed` atteint `maxClaimableSupply`, rejouer `setClaimConditions` avec
**une seule** condition, la suivante. Jamais de date : on avance quand c'est vendu.

| Marche | Tokens | `maxClaimableSupply` | Prix | /wallet |
|---|---|---|---|---|
| A (en cours) | #3 → #8699 | 8 697 | 0,005 ETH | 5 |
| B | #8700 → #9399 | 700 | 0,05 ETH | 3 |
| C | #9400 → #9699 | 300 | 0,15 ETH | 2 |
| D | #9700 → #9949 | 250 | 0,5 ETH | 2 |
| E | #9950 → #9994 | 45 | 10 ETH | 1 |
| F | #9995 → #9999 | 5 | 100 ETH | 1 |
| G | #10000 — The First | 1 | 1 111 ETH | 1 |

Somme : 8 697 + 700 + 300 + 250 + 45 + 5 + 1 = **9 998**, plus les 2 mintés = 10 000. ✅

C'est exactement leur échelle d'origine, moins la phase gratuite, avec un déclencheur
sain. La promesse « le prix grimpe avec la rareté » devient vraie, et « The First le
30 octobre » devient un objectif au lieu d'une date intenable.

## Deux décisions à prendre, pas des détails

**1. Les 1 000 mints gratuits.** 998 n'ont jamais été réclamés et la page les promet
toujours. Soit on les honore avec un **vrai merkle root** (une allowlist n'a jamais
existé : les 8 phases ont un merkle nul), soit on retire la promesse de la copie.
Une phase gratuite ouverte à 1/wallet sans allowlist sera vidée par des bots.

**2. Le prix d'entrée.** 0,005 ETH (~14 $) est ce que la page annonce. Si l'objectif est
d'écouler du volume plutôt que de tenir l'échelle, une variante consiste à ouvrir une
seule condition à 0,005 ETH sur les **9 998** restants et à abandonner l'échelle : plus
simple, zéro intervention manuelle, mais le récit de « l'ascension » disparaît.

## Ordre d'exécution

1. **Couper la pub Facebook** — tant que le prix affiché ≠ le prix facturé, chaque clic payé est une exposition.
2. **Étape 1 ci-dessus** — avant 22:00 UTC, sinon la phase à 10 ETH s'active.
3. **Patch 01** — brancher la copie sur le contrat pour que la divergence ne revienne pas.
4. Aligner la copie : prix d'entrée réel, mot « allowlist », date du 30 octobre.
