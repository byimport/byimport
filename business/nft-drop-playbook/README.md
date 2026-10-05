# Playbook — lancer un drop NFT sans se tirer dessus

Tiré d'un audit réel : un drop de 10 000 NFT qui a vendu **2 unités**, non par manque
de demande, mais parce que son échelle de prix avançait au **calendrier** au lieu
d'avancer aux **ventes**. Les constats chiffrés sont dans
[`../monkeyspunk/AUDIT.md`](../monkeyspunk/AUDIT.md).

Chaque règle ici existe parce que ce drop l'a violée, et `preflight.py` refuse
mécaniquement la configuration correspondante. Le but n'est pas d'être vigilant :
c'est de rendre l'erreur impossible à expédier.

## La règle qui compte plus que toutes les autres

> **Une marche de prix se franchit quand l'offre est vendue, jamais quand une date arrive.**

Sur thirdweb `DropERC721`, `getActiveClaimConditionId()` renvoie la **dernière** condition
dont `startTimestamp` est passé. Si tu encodes ton échelle de prix comme 8 phases datées,
l'horloge avance le prix que tu aies vendu 0 ou 8 000 unités — et l'invendu de chaque phase
est abandonné définitivement.

Ce que ça a coûté au drop audité :

| Phase | Offre | Vendu | Prix | Issue |
|---|---|---|---|---|
| 0 | 1 000 | **2** | gratuit | expirée en 3 jours — 998 gratuits détruits par l'horloge |
| 1 | 7 699 | **0** | 0,005 ETH | expirée en 6 jours — 77 % de la collection, inatteignable |
| 4 | 250 | **0** | 0,5 ETH | devenue active sans qu'une seule unité se soit vendue |

**À faire à la place :** une seule condition active, `startTimestamp = 0` (ne peut pas
expirer), `maxClaimableSupply` = l'offre de la marche en cours. Quand `supplyClaimed`
atteint ce plafond, tu rejoues `setClaimConditions` avec la marche suivante. C'est une
action manuelle par palier — et c'est précisément ce qui t'évite de perdre ta collection.

## Les autres règles

**2. Ne jamais écrire un prix en dur dans la page.** Le drop audité annonçait « 1 000
gratuits » pendant que le contrat facturait 0,5 ETH (~1 350 $). Lis la condition active
on-chain et affiche-la. Implémentation fonctionnelle :
[`../monkeyspunk/patches/01-live-mint-price.html`](../monkeyspunk/patches/01-live-mint-price.html).
Avec du trafic payant, cette divergence n'est pas un manque à gagner, c'est une exposition
en publicité trompeuse.

**3. « Allowlist » est un merkle root, pas un mot sur une page.** Les 8 phases du drop
audité avaient un merkle root nul, alors que la page promettait une allowlist. La phase
« gratuite » était donc un mint public ouvert, 1 par wallet, pendant 3 jours, non annoncé.
L'erreur inverse est tout aussi grave : un root posé par erreur sur un mint censé être
ouvert fait croire que le mint est cassé. `preflight.py` teste les deux sens.

**4. Simuler avant de signer.** `eth_simulateV1` exécute ta transaction sur l'état réel de
la chaîne sans l'écrire : tu vois l'état résultant, le gas, et tu vérifies qu'un non-propriétaire
est bien rejeté. Exemple travaillé :
[`../monkeyspunk/scripts/simulate-claim-fix.py`](../monkeyspunk/scripts/simulate-claim-fix.py).
Ça coûte une minute et ça remplace l'espoir par une preuve.

**5. Dimensionner les récompenses de staking sur l'adoption réelle.** Le drop audité avait
réellement financé ses pools (100 M de jetons, vérifié), mais aux taux affichés les paliers
premium s'épuisaient en **100 à 120 jours** — et 1 250 NFT « Rare » se partageaient un pool
plus petit que 8 699 « Common ». Calcule l'autonomie à 100 % de staking avant de publier un
taux, et prévois le réapprovisionnement (royalties) ou une émission dégressive.

**6. Ne pas suspendre le dénouement à ce que tu ne contrôles pas.** Le drop promettait son
unique pièce maîtresse « le 30 octobre » à 1 111 ETH (~3 M$), ce qui exigeait d'avoir minté
les 9 997 tokens précédents. Une date que tu ne maîtrises pas devient un objectif, pas un
rendez-vous.

**7. Surveiller, parce que le silence est le vrai mode de défaillance.** Personne n'a vu
pendant 5 semaines que le mint avait vendu 0. Un cron qui lit `supplyClaimed` et
`getActiveClaimConditionId` l'aurait détecté en une heure.
[`../monkeyspunk/scripts/read-claim-conditions.py`](../monkeyspunk/scripts/read-claim-conditions.py)
fait cette lecture ; branche-le sur une alerte.

## Le contrôle pré-lancement

```bash
python3 preflight.py --expect mon-drop.json
```

Il lit les claim conditions réelles et les confronte à ce que ta page promet. Code de
sortie 1 si un contrôle échoue — à brancher en CI avant tout déploiement de la landing.

Les 9 contrôles : une seule condition active · aucune phase datée dans le futur · la phase
active est ouverte · le prix on-chain égale celui de la copie · l'allowlist promise existe
vraiment (et réciproquement) · l'échelle couvre exactement la collection · l'offre active
ne dépasse pas la collection · les métadonnées sont lazy-mintées · la devise est celle attendue.

Décris ton drop dans un JSON (voir
[`monkeyspunk-as-counterexample.json`](monkeyspunk-as-counterexample.json)) :

```json
{
  "contract": "0x…",
  "total_supply_planned": 10000,
  "copy_claims": { "entry_price_eth": 0.005, "has_allowlist": false },
  "ladder": [ {"units": 8697}, {"units": 700}, {"units": 1} ]
}
```

### Preuve que le contrôle fonctionne

Lancé contre le drop audité, tel que sa propre page le décrit, il rejette la configuration :

```
[FAIL] single active condition   count = 8
[FAIL] no future-dated phase     ids [5, 6, 7] activate later
[FAIL] price matches the copy    chain 0.5 ETH vs copy 0.005 ETH
[FAIL] allowlist is real         merkleRoot is ZERO
4 of 9 checks FAILED - do not launch in this state.
```

Et `test_preflight.py` (10 tests, stdlib + pytest) prouve l'autre moitié : les contrôles
**passent** sur une configuration saine, et chacun attrape sa faute précise, sans contrat live.

```bash
python3 -m pytest test_preflight.py -q
```

## Portée

Écrit et testé contre **thirdweb `DropERC721` sur Ethereum**, le contrat que l'audit a
disséqué. Les principes valent pour n'importe quel contrat de drop ; les sélecteurs et le
décodage de `preflight.py` sont spécifiques à celui-là. Dis-moi ta stack si elle diffère et
je porte les contrôles.
