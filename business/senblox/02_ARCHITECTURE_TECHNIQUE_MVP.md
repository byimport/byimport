# 02 — Architecture technique du MVP

Principe directeur : **tout ce qui n'est pas différenciant est managé, tout ce qui est différenciant est propriétaire.** Différenciant : le runtime client, la couche réseau, Guardian (modération), Studio IA. Non différenciant : bases de données, files, auth, paiements, observabilité — on prend du managé et on avance.

## 1. Vue d'ensemble

```
                                  ┌──────────────────────────────┐
   Joueur (navigateur)            │        PLAN DE CONTRÔLE       │
   ┌────────────────┐   HTTPS     │  API GW (Cloudflare)          │
   │ Runtime WASM   │────────────▶│  Services (Rust/axum) :       │
   │ (Rust + wgpu,  │             │   auth · profils · mondes ·   │
   │  WebGPU/WebGL2)│             │   matchmaking · économie ·    │
   └───────┬────────┘             │   social · Guardian API       │
           │ WebTransport (QUIC)  └──────┬───────────────┬────────┘
           │ fallback WebSocket          │               │
           ▼                             ▼               ▼
   ┌────────────────────┐        ┌──────────────┐  ┌────────────────┐
   │  PLAN DE JEU        │        │ PostgreSQL   │  │ Pipeline async │
   │  GKE/EKS multi-rég. │        │ (Neon/Cloud  │  │ NATS JetStream │
   │  Agones : pods      │        │  SQL) +      │  │ → Guardian     │
   │  serveur de jeu     │        │ Redis/       │  │ → analytics    │
   │  (Rust, ECS, 60 Hz) │        │ Dragonfly +  │  │   (ClickHouse) │
   │  1 pod = 1 instance │        │ ClickHouse   │  └────────────────┘
   │  de monde (≤100 j.) │        └──────────────┘
   └─────────┬──────────┘         ┌──────────────────────────────┐
             │                    │ ASSETS : R2/S3 + CDN          │
             └───────────────────▶│ (meshes/textures/audio,       │
               snapshots état     │  versionnés, immutables)      │
                                  └──────────────────────────────┘
```

## 2. Backend & scalabilité

### 2.1 Serveurs de jeu (le cœur)

- **Langage/modèle** : Rust, ECS partagé avec le client (même crate de simulation compilée nativement côté serveur, en WASM côté client). Simulation autoritaire serveur à 30–60 Hz, client-side prediction + réconciliation, interpolation d'entités. Le partage de code sim client/serveur élimine la classe de bugs « le client et le serveur ne calculent pas pareil ».
- **Orchestration** : **Agones sur Kubernetes** (GKE en premier, multi-cloud plus tard). Chaque instance de monde = 1 `GameServer` pod. `Fleet` + autoscaling sur buffer de pods « ready » → démarrage d'une instance < 3 s. Nœuds spot/preemptible pour les fleets de débordement (−60 % de coût), nœuds standard pour la base.
- **Multi-région dès le MVP public** : us-east, eu-west, sa-east (Brésil), asia-se (Singapour). Le matchmaking route sur la latence mesurée (ping beacons côté client), pas sur la géo IP.
- **Densité** : cible 4 instances de monde (jusqu'à 100 joueurs chacune) par nœud 8 vCPU. À 0,20 $/h le nœud spot → **~0,0005–0,001 $/heure-joueur à pleine charge** ; cible blended (charge réelle 40–60 %) < 0,01 $/heure-joueur, la métrique d'exit n°3 (voir [04](04_STRATEGIE_EXIT.md)).
- **« Millions de joueurs simultanés »** — soyons précis : pas un monde de 1 M de joueurs (personne ne fait ça), mais 1 M de joueurs répartis sur ~20 000 instances de mondes. C'est un problème d'orchestration (résolu par Agones + cell-based architecture : régions → cellules de ~50 000 CCU indépendantes, aucune dépendance synchrone inter-cellule) et non de moteur.

### 2.2 Réseau

- **WebTransport (QUIC)** comme transport principal : datagrammes non fiables pour l'état de jeu (position, physique), streams fiables pour les événements (chat, inventaire). Fallback WebSocket (TCP) automatique pour les navigateurs/réseaux d'entreprise récalcitrants — dégradation acceptée (interp buffer plus grand).
- Protocole binaire maison sur FlatBuffers (zéro-copy, schéma versionné). Snapshot delta-compressé + interest management (le client ne reçoit que ce que son avatar peut percevoir) : budget 20–40 kbps par joueur.
- Voix : WebRTC SFU (LiveKit self-hosted) par zone spatiale, tappé par Guardian (couche voix).

### 2.3 Données

| Donnée | Store | Justification |
|---|---|---|
| Comptes, mondes (métadonnées), économie, transactions | **PostgreSQL** managé, schéma double-entrée pour le ledger | ACID non négociable pour l'argent ; un ledger append-only à double entrée, jamais d'UPDATE de solde |
| Sessions, presence, matchmaking, rate-limits | **Redis/Dragonfly** | Latence sub-ms, TTL naturels |
| État persistant des mondes (progression joueur par monde) | PostgreSQL (JSONB par joueur×monde) au MVP ; ScyllaDB si > 50 k écritures/s | Ne pas payer la complexité Scylla avant d'en avoir besoin |
| Télémétrie, analytics, logs de modération | **ClickHouse** (via NATS JetStream) | Volumétrie ; alimente les KPIs d'exit et le réentraînement Guardian |
| Assets UGC | **R2/S3 immutable + CDN**, adressés par hash de contenu | Cache infini, rollback trivial, dédup naturelle |

- **Bus d'événements : NATS JetStream** (plus simple d'exploitation que Kafka à notre échelle ; migration Kafka possible si un acquéreur l'exige, les producteurs sont abstraits).
- Sauvegarde d'état de monde : snapshots incrémentaux toutes les 30 s vers R2 + write-through des événements économiques (jamais d'achat perdu même si le pod meurt).

### 2.4 Plan de contrôle

- Services Rust (axum) ou Go — monolithe modulaire au départ (un binaire, modules découplés par interfaces), découpage en services uniquement quand une équipe dédiée existe par domaine. Ne pas jouer aux microservices à 10 ingénieurs.
- Auth : OIDC (Ory/Auth0), comptes invités promus, âge progressif (voir Guardian).
- Paiements : Stripe (achats SenBucks) + **Stripe Connect Express** (payouts créateurs, KYC/DAC7/1099 délégués).
- Observabilité : OpenTelemetry partout dès le jour 1, Grafana/Loki/Tempo managés. La courbe « coût infra / heure-joueur » est un dashboard permanent — c'est une métrique de board.

## 3. Senblox Studio : création no-code/low-code boostée IA

### 3.1 Philosophie produit

Trois étages de créateurs, un seul artefact :

1. **Prompt-to-world (no-code)** — « un obby dans un temple aztèque avec des pièges de lave » → l'IA compose un monde jouable à partir de la bibliothèque d'assets + terrain généré + logique standard (checkpoints, timer, leaderboard). L'utilisateur édite ensuite par manipulation directe et par conversation (« rends la 3e section plus dure »). Cible : premier monde publié en < 30 minutes.
2. **Blocs logiques (low-code)** — graphe d'événements type Scratch/Blueprint pour les comportements custom. Chaque graphe est compilable vers le langage de script (étage 3) : le créateur qui grandit **voit** le code que ses blocs génèrent — c'est l'escalier d'apprentissage.
3. **Script (code)** — **Luau** (le Lua typé open-sourcé par Roblox). Choix assumé et cynique : (a) langage excellent, sandboxable, (b) **des millions de créateurs Roblox le connaissent déjà** — coût de migration vers Senblox ≈ zéro, (c) l'outillage (luau-lsp, analyse statique) existe. L'API monde (`world.*`, événements, services) est propre et documentée, sans clone des ROBLOX API pour éviter tout terrain juridique glissant.

### 3.2 Le copilote IA (l'agent « Forge »)

Architecture : agent LLM (API Claude ; abstraction provider pour négociabilité) outillé sur le Studio via un protocole de commandes — le modèle ne « génère pas une scène », il appelle des outils (`spawn_asset`, `set_terrain`, `write_script`, `run_playtest`) et itère.

- **Génération de scripts** : prompt → code Luau typé + tests de comportement auto-exécutés dans une sandbox headless du serveur de jeu (le même binaire ECS). Le code livré a tourné, pas juste été généré. Explication en langage simple pour les créateurs de l'étage 1–2.
- **Génération d'assets 3D** : pipeline hybride honnête — (a) **retrieval-first** : chercher dans la bibliothèque/marketplace avant de générer (moins cher, plus cohérent), (b) génération text-to-3D (APIs type Meshy/Tripo au MVP, modèles maison seulement si les volumes le justifient) suivie d'un **repasse qualité automatique** : retopologie, LODs, atlas de textures, budget polygones par classe d'objet. Aucun mesh généré n'entre dans un monde sans passer ce pipeline — sinon le contenu IA détruit la perf, et la perf est notre produit.
- **Textures/matériaux** : diffusion (SDXL/Flux via API) → conversion PBR (albedo/normal/roughness) automatique, tuilage vérifié.
- **NPC & dialogues** : personnages conversationnels sandboxés (persona + garde-fous Guardian sur les sorties) — feature de différenciation forte vs Roblox pour les mondes narratifs.
- **Coût** : le no-code IA est facturé en « énergie de forge » incluse par palier (gratuit : quota mensuel ; abonnement créateur : plus) — l'IA générative à volonté gratuite est un gouffre, on le dit et on le price dès le MVP.

### 3.3 Studio : décisions d'implémentation

- **Le Studio EST un monde Senblox** en mode édition : même runtime, mêmes assets, collaboration multi-utilisateurs en temps réel via CRDT (Yjs ou Loro) sur le scene graph — deux ados éditent le même monde ensemble, l'app web est le seul outil. Édition collaborative = feature sociale = croissance.
- Versionnage : chaque publication est un snapshot immutable (hash d'assets + script bundle), rollback en un clic. Pipeline de publication = passage Guardian couche 1 obligatoire.
- Playtest instantané : bouton « jouer » → instance éphémère Agones en < 3 s, lien de test partageable.

## 4. Ce que le MVP ne fait PAS (périmètre négatif, aussi important que le reste)

- Pas de mondes > 100 joueurs par instance (pas de sharding intra-monde).
- Pas d'app native (PWA seulement) tant que la traction web n'est pas prouvée.
- Pas de modèles IA maison (fine-tunes légers de classifieurs Guardian exceptés) — APIs partout où c'est possible.
- Pas de crypto/blockchain. Jamais. (Voir [03](03_GROWTH_HACKING.md) §3 — et c'est aussi un critère d'acquérabilité : aucun grand acquéreur ne veut d'un passif token.)
- Pas d'éditeur natif desktop : le Studio web est le pari ; s'il échoue en test utilisateur, on réévalue (Tauri wrap du même code).
