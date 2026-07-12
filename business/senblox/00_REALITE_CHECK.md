# 00 — Réalité check : ce que le CTO doit dire avant tout

Un plan qui ne nomme pas ses risques est un pitch, pas un plan. Voici les faits inconfortables, puis la manière dont la stratégie Senblox les contourne (ou pas).

## 1. Le cimetière des « Roblox killers »

Core (Manticore Games), Crayta (racheté puis fermé par Meta), Rec Room (pivot permanent), Hiber3D, Struckd, Yahaha... La liste des plateformes UGC mieux financées que nous et aujourd'hui mortes ou zombies est longue. Leur erreur commune : **attaquer Roblox sur le contenu au lieu d'attaquer sur la distribution et l'économie**. Roblox ne gagne pas parce que ses jeux sont bons ; il gagne parce que (a) les enfants y sont déjà avec leurs amis (effet réseau social), et (b) les créateurs y gagnent de l'argent, même mal payés, parce que l'audience y est.

**Conséquence stratégique :** Senblox ne doit jamais se vendre comme « un meilleur Roblox ». Il doit créer sa propre boucle de distribution (le lien instantané, voir [01](01_POSITIONNEMENT_STRATEGIQUE.md) §4) et acheter l'offre de contenu avec de l'économie (70 % créateurs), pas avec des promesses de trafic qu'on n'a pas encore.

## 2. L'effet réseau ne s'achète pas, il se démarre en niche

Roblox a 80M+ DAU. On ne rattrape pas ça frontalement. La seule voie documentée est celle de Discord vs Skype ou de TikTok vs YouTube : **dominer un segment étroit que le géant néglige**, puis s'étendre. Candidats de niche pour Senblox : les créateurs 13–20 ans frustrés par le style visuel Roblox et le DevEx (segment vocal, sur-représenté sur X/YouTube), et les joueurs mobiles/marchés émergents où le client Roblox de 500 Mo et ses exigences de stockage sont une vraie barrière.

## 3. Le coût réel

Ordres de grandeur honnêtes (équipe basée Europe, hors marketing payant) :

| Phase | Durée | Équipe | Burn estimé |
|---|---|---|---|
| Prototype | 3 mois | 3–4 ing. fondateurs | 150–250 k€ |
| MVP fermé | 6 mois | 8–10 (dont 2 infra, 1 sécurité/modération) | 700 k€–1 M€ |
| Lancement public | 9 mois | 15–20 | 2,5–3,5 M€ |
| Échelle pré-exit | 18 mois | 30–45 | 8–15 M€ |

**Total avant exit : 12–20 M€ levés (pre-seed → série A/B).** Quiconque annonce moins ment ou n'a jamais opéré de serveurs de jeu temps réel. Le poste caché : l'infra multi-joueurs et la modération 24/7, qui ne se « féature-flag » pas.

## 4. La modération n'est pas un module, c'est un passif juridique

Une plateforme sociale pour mineurs déclenche : COPPA (US), DSA + espaces « minor safety » (UE), Online Safety Act (UK), obligations KYC pour les paiements sortants vers créateurs (DAC7, 1099). Roblox dépense des centaines de millions par an en trust & safety et se fait quand même attaquer. **Décision structurante :** la modération IA (voir [01](01_POSITIONNEMENT_STRATEGIQUE.md) §3) est traitée comme un produit cœur avec son propre roadmap et son propre budget (~15 % de l'ingénierie), pas comme une feature. C'est aussi ce qui la rend revendable séparément à l'exit.

## 5. L'exit n'est pas un plan, c'est une option

Construire « pour vendre » produit des entreprises invendables : les acquéreurs achètent des courbes de rétention et des équipes, pas des pitch decks. La stratégie exit ([04](04_STRATEGIE_EXIT.md)) est donc formulée ainsi : **construire une entreprise autonome viable dont les KPIs se trouvent être exactement ceux que les corp-dev de Microsoft/Epic/Meta/Sony screener**. Si l'exit ne vient pas, l'entreprise doit pouvoir vivre de son take rate de 30 %.

## 6. Hypothèses à tuer en priorité (fail fast)

Dans l'ordre, les hypothèses dont l'invalidation tue le projet — à tester au coût minimum :

1. **H1 — Techniquement** : peut-on faire tourner un monde 3D multi-joueurs à 60 fps sur un téléphone Android milieu de gamme dans Chrome via WebGPU/WebGL2 fallback ? → Prototype, mois 1–2. Si non : pivot cloud-streaming (coût/utilisateur x10) ou natif léger, et la thèse « zéro download » s'affaiblit.
2. **H2 — Offre** : 20 créateurs Roblox de milieu de classement acceptent-ils de porter/créer un jeu chez nous pour 70 % + garantie de revenu minimum ? → 30 entretiens, mois 1–3, avant d'écrire le Studio.
3. **H3 — Demande** : le taux de clic→jeu→retour J1 d'un lien Senblox partagé sur Discord/TikTok dépasse-t-il 25 % ? → Alpha fermée, mois 6–9.
4. **H4 — Économie** : ARPDAU ≥ 0,05 $ atteignable sans dark patterns interdits par les régulations mineurs ? → MVP, mois 9–12.

Si H1 et H2 tiennent, le projet mérite la série A. Sinon, on arrête ou on pivote avant d'avoir brûlé plus de 1 M€.
