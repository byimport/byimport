# 03 — Growth hacking : offre, demande, économie interne

Sans budget marketing, il n'y a que trois moteurs possibles : **payer l'offre (créateurs), rendre la demande virale par construction (le lien), et faire de l'économie un produit** en soi. Les trois sont détaillés ici avec leurs métriques de pilotage.

## 1. La première vague de créateurs : on ne les attire pas, on les recrute

Erreur classique des plateformes UGC mortes : lancer un outil et attendre les créateurs. Les créateurs vont où est l'audience ; sans audience, il faut remplacer l'audience par du cash et du statut.

### Programme « Founding 100 » (mois 3–12)

- **Cible** : créateurs Roblox de milieu de classement — assez bons pour produire un hit, pas assez gros pour être verrouillés par leurs revenus Roblox (les studios top 50 ne bougeront pas ; les 500 suivants sont sous-payés et frustrés). Sourcing direct : DevForum, X/Twitter #RobloxDev, Discords de dev Roblox, jams itch.io.
- **Offre** : 85 % de partage à vie (vs 70 % standard) + **garantie de revenu minimum 500–2 000 $/mois pendant 6 mois** (selon track record) contre un engagement : 1 monde exclusif ou porté + itérations. Coût total du programme : ~600 k€–1 M€ — c'est **le vrai budget marketing**, et chaque euro produit du contenu permanent au lieu d'ads évaporées.
- **Statut** : badge fondateur permanent, accès direct à l'équipe (canal privé), leur nom dans les crédits de la plateforme, gouvernance consultative (vote sur le roadmap Studio). Le statut retient mieux que le cash à moyen terme.
- **Le pitch en une ligne** : « Chez Roblox tu touches 25 % et tu es un numéro. Ici tu touches 85 %, tu parles aux fondateurs, et ton jeu se partage comme un lien TikTok. »

### Boucle contenu-créateur

- **Game jams mensuelles dotées** (5–10 k$ de prix pool) sur un thème — le format le moins cher au monde pour générer du contenu, du bouche-à-oreille dev et des candidats au Founding 100.
- Le Studio IA abaisse le coût du premier monde (< 30 min, voir [02](02_ARCHITECTURE_TECHNIQUE_MVP.md) §3.1) : chaque joueur est un créateur potentiel. Métrique : **% de joueurs qui publient un monde dans leurs 30 premiers jours** (cible : 3–5 % ; Roblox est < 1 %).

## 2. La première vague de joueurs : la boucle URL

Le produit EST le canal d'acquisition. Chaque monde est une URL jouable en 15 s sans compte ([01](01_POSITIONNEMENT_STRATEGIQUE.md) §4). Trois boucles, par ordre de priorité :

1. **Boucle streamer/créateur de contenu** : un YouTubeur/TikTokeur/streamer Twitch met son lien en bio/description → ses viewers jouent instantanément (pas de « téléchargez Roblox d'abord »). Programme d'affiliation mesurable : lien tracké, le streamer touche 5 % des dépenses des joueurs qu'il amène (à vie). On recrute les streamers Roblox moyens (10–100 k abonnés) avec le même playbook que les créateurs.
2. **Boucle Discord** : SDK Discord Activities — jouer à un monde Senblox *dans* un salon vocal Discord. Le public cœur (10–20 ans) vit sur Discord ; être jouable dans Discord = distribution native dans des millions de serveurs.
3. **Boucle sociale in-game** : inviter un ami = lien profond vers *ta session en cours* (il apparaît à côté de toi). K-factor mesuré dès l'alpha ; cible K > 0,4 au lancement public (au-dessus, chaque cohorte payée ou organique s'auto-amplifie).

**Anti-pattern assumé :** pas d'achat d'installs mobiles, pas d'ads TikTok au lancement. Si la boucle URL ne fonctionne pas organiquement sur 10 000 joueurs, l'acheter à l'échelle ne la réparera pas — ça brûlerait la série A pour maquiller un problème produit.

### Le contenu propriétaire d'amorçage

Deux à trois mondes développés en interne (par l'équipe + Founding 100 en contrat) pour garantir la qualité au jour 1 — le « Nintendo model » minimal. Ils servent aussi de référence de qualité et de tutoriels vivants du Studio.

## 3. L'économie interne : SenBucks

### Design

- **SenBucks (SBX)** : monnaie unique d'achat. Taux d'achat fixe et public : 100 SBX = 1 $ (des paliers avec bonus légers, jamais de taux opaques). **Pas de crypto, pas de blockchain, pas de spéculation** — c'est une monnaie de magasin, régulée comme telle, point.
- **Côté créateur, la conversion est directe** : 1 000 SBX dépensés dans ton monde = 7,00 $ de payout (70 %), affiché en dollars/euros dans le dashboard en temps réel. La transparence EST la feature (vs le double taux de change opaque de Roblox, qui est le cœur du grief DevEx).
- **Sources de dépense saines** : passes d'accès, cosmétiques d'avatar (interopérables entre mondes → valeur perçue élevée), boosts non pay-to-win (les mondes classés compétitifs interdisent les boosts payants par policy), abonnement plateforme optionnel (SenPlus : allocation mensuelle de SBX + avantages cosmétiques).
- **Marketplace secondaire d'items limités : NON au MVP.** C'est le vecteur n°1 de fraude, de RMT (real-money trading) et de gambling adjacent chez Roblox. Réévaluation post-série A avec l'infra anti-fraude mûre.

### Stabilité & conformité (le travail ennuyeux qui évite la mort)

- Ledger double-entrée append-only ([02](02_ARCHITECTURE_TECHNIQUE_MVP.md) §2.3) ; l'émission de SBX est 1:1 avec les encaissements — **jamais** d'émission gratuite massive (les récompenses gratuites sont en monnaie secondaire non convertible, « étoiles », pour ne pas diluer le SBX ni créer un passif de remboursement).
- Mineurs & dépenses : plafonds par défaut selon l'âge, confirmation parentale au-delà, remboursement sans friction sous 48 h (la politique anti-chargeback la plus efficace ET l'argument parents).
- Anti-fraude : vélocité, empreinte device, graphe de comptes (mules de payout) — règles + modèle dès que les données existent. Les payouts créateurs sont retenus 30 jours glissants (standard marketplace) pour absorber les chargebacks.
- Juridique : SBX non remboursable en cash côté joueur (sinon e-money license), payout créateur = revenu de service via Stripe Connect. Cartographie réglementaire (UE DSA/DMA, COPPA, UK OSA) tenue par un conseil spécialisé dès le pre-seed — voir [00](00_REALITE_CHECK.md) §4.

## 4. Tableau de bord growth (les seuls chiffres qui comptent)

| Boucle | Métrique | Cible mois 12 | Cible mois 24 |
|---|---|---|---|
| Acquisition | Clic lien → en jeu (taux de conversion) | > 60 % | > 70 % |
| Activation | Invité → compte créé | > 35 % | > 45 % |
| Rétention | D1 / D7 / D30 | 40 / 20 / 10 % | 45 / 25 / 13 % |
| Viralité | K-factor | > 0,4 | > 0,5 |
| Offre | Créateurs actifs monétisés (> 100 $/mois) | 150 | 1 000 |
| Offre | % joueurs publiant un monde (30 j) | 3 % | 5 % |
| Monétisation | ARPDAU | 0,04 $ | 0,07 $ |
| Économie | Payout créateurs cumulé | 500 k$ | 5 M$ |

Ces cibles ne sont pas décoratives : ce sont les mêmes que la grille d'acquisition de [04_STRATEGIE_EXIT.md](04_STRATEGIE_EXIT.md) — le growth et l'exit sont le même tableau de bord.
