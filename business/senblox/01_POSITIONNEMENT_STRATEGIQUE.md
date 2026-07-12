# 01 — Positionnement stratégique : les 4 axes de différenciation vs Roblox

Chaque axe cible un défaut **structurel** de Roblox — un défaut qu'il ne peut pas corriger sans casser son propre modèle (dette technique du moteur maison, dépendance financière au take rate de 70 %, client natif historique). C'est ce qui rend la fenêtre défendable.

## 1. Graphismes & moteur : sortir du « blocs » sans sortir du navigateur

### Le diagnostic

Le moteur Roblox est un moteur propriétaire de 2006 modernisé par couches. Son rendu plafonne (matériaux PBR partiels, éclairage « Future » coûteux, pas de global illumination praticable) et surtout son **style est verrouillé** : avatars R6/R15, physique et outils qui poussent vers le low-poly bloc. Les créateurs ambitieux partent vers Fortnite UEFN (Unreal) — mais UEFN n'est ni web, ni vraiment UGC-first (pas de scripting libre, publication contrôlée par Epic).

### La position Senblox : « qualité Fortnite-lite, distribution web »

**Choix moteur — décision arrêtée : runtime custom sur wgpu/WebGPU, pas un pont Unreal/Unity.**

| Option | Verdict |
|---|---|
| **Pont Unreal (Pixel Streaming)** | Rendu superbe mais 100 % cloud-streamé : 0,10–0,30 $/h/utilisateur d'infra GPU. Économiquement mort pour de l'UGC gratuit grand public. Rejeté comme cœur ; gardé comme option premium « mondes cinématiques » post-série A. |
| **Unity Web (WebGL/WebGPU export)** | Runtime lourd (20–40 Mo de download initial), licence et gouvernance Unity = risque plateforme (cf. crise pricing 2023). Rejeté. |
| **Godot 4 (export web)** | Open source, séduisant, mais export web encore lourd et single-threaded par défaut (SharedArrayBuffer requis) ; on ne contrôle pas le roadmap. Utilisable pour prototyper le Studio desktop, pas comme runtime client. |
| **Bevy (Rust) → WASM** | Excellente base ECS, mais Bevy est un moteur généraliste en évolution rapide (breaking changes) et son rendu web n'est pas optimisé « first paint ». On en réutilise les idées (ECS, wgpu) plus que le framework. |
| **Runtime custom : Rust + wgpu, compilé WASM, rendu WebGPU avec fallback WebGL2** | **Retenu.** ~5–8 Mo de runtime téléchargé une fois puis mis en cache, ECS data-oriented, streaming d'assets progressif. C'est la seule option qui atteint « clic → jeu < 15 s » sur mobile. |

**Pourquoi c'est défendable :** un runtime WASM/WebGPU propriétaire optimisé pour le streaming d'assets UGC est précisément le genre d'actif qu'un acquéreur ne peut pas assembler vite — c'est 2–3 ans d'ingénierie spécialisée (voir [04](04_STRATEGIE_EXIT.md)).

**Cibles de rendu MVP (réalistes, pas marketing) :**
- PBR metallic-roughness complet, shadow maps en cascade, SSAO, bloom, tone mapping ACES — « stylisé haute qualité » type Fortnite/Valorant, PAS du photoréalisme.
- 60 fps sur Pixel 6a / iPhone 12 en WebGPU ; 30 fps garanti en fallback WebGL2.
- Budget par monde : 50 Mo d'assets streamés par priorité (le joueur entre dans le monde à 10 % du téléchargement, le reste arrive pendant qu'il joue).
- Avatars : rig humanoïde unique standardisé (compatible export VRM) avec morphs — interopérables entre tous les mondes, stylisation continue du « toon » au « semi-réaliste » par monde.

### VR

WebXR est supporté par le même runtime (wgpu → WebXR sur Quest Browser). La VR n'est **pas** un pilier du MVP (marché trop petit) mais le support WebXR de démonstration coûte peu et vaut très cher dans le narratif d'acquisition Meta. Une démo Quest fonctionnelle sera prête pour les due diligences, pas pour les utilisateurs.

## 2. Partage des revenus : le DevEx comme arme d'acquisition de talents

### Le diagnostic

Chez Roblox, un créateur touche ~24,5 % de ce que dépense le joueur en cash réel (30 % du Robux, après la marge plateforme sur l'achat de Robux et le taux DevEx de 0,0038 $/Robux). Le seuil de retrait (30 000 Robux gagnés) et les délais aggravent le tout. C'est le grief n°1 de la communauté créateurs — documenté, public, viral.

### Le modèle Senblox : 70/30 inversé, transparent, sans seuil punitif

- **70 % des revenus nets** (après frais de paiement et TVA) reversés au créateur sur tout achat in-world et vente d'items. Le calcul est publié : `payout = (prix payé − frais PSP − taxes) × 0,70`. Pas de monnaie-écran opaque entre le joueur et le payout (les SenBucks ont un taux de conversion fixe et public, voir [03](03_GROWTH_HACKING.md) §3).
- **Seuil de retrait : 50 $**, paiement mensuel automatique via Stripe Connect (KYC intégré, DAC7/1099 gérés par Stripe Tax).
- **Marketplace d'assets 80/20** en faveur du créateur d'asset : un modeleur 3D qui vend un pack de bâtiments à d'autres créateurs touche 80 %. Objectif : faire émerger une économie B2B créateur→créateur qui densifie l'écosystème.
- **Programme fondateurs (100 premiers créateurs)** : 85 % à vie + revenu minimum garanti (voir [03](03_GROWTH_HACKING.md) §1).

### La soutenabilité (il faut être honnête sur ce point)

Roblox garde 70+ % parce que ses coûts sont énormes : infra, modération, stores mobiles (Apple/Google prennent 30 % avant tout). Senblox peut payer 70 % **uniquement parce que** :
1. **Distribution web** : pas de commission Apple/Google sur les achats effectués dans le navigateur (c'est un avantage structurel du choix web, pas un détail).
2. Infra cloud moderne + serveurs mutualisés (voir [02](02_ARCHITECTURE_TECHNIQUE_MVP.md)) visant < 0,01 $/heure-joueur.
3. Modération majoritairement automatisée (le coût humain de Roblox est en grande partie de la modération).

Marge plateforme cible : 30 % de take rate dont ~12 points de coûts directs (PSP, infra, modération) → ~18 points de marge brute. Serré mais viable ; c'est un modèle « place de marché », pas un modèle « casino ».

## 3. Sécurité & modération IA : le point faible historique de Roblox devient notre produit

### Le diagnostic

La modération Roblox est réactive, sous-traitée, contournée en permanence (leet speak, condos, contournements audio). Chaque scandale de presse (grooming, contenus sexuels) érode la confiance des parents — le vrai décideur d'installation chez les 8–13 ans.

### L'architecture « Guardian » : 4 couches, temps réel, budget latence explicite

**Couche 1 — Ingestion à la création (asynchrone, avant publication) :**
- Tout asset uploadé (mesh, texture, audio, script) passe un pipeline de classification : CLIP/SigLIP fine-tuné pour textures et rendus multi-angles des meshes 3D (détection de contenus sexuels/haineux cachés dans la géométrie — le vecteur d'attaque classique des « condos »), Whisper + classifieur pour l'audio, analyse statique + LLM pour les scripts (exfiltration, phishing intégré au gameplay).
- Score de risque → publication auto (< 0,2), revue IA approfondie par LLM multimodal (0,2–0,7), file humaine (> 0,7). Cible : < 2 % du volume en file humaine.

**Couche 2 — Chat texte temps réel (budget : < 80 ms p95) :**
- Étage 1 : classifieur distillé (DeBERTa-v3-small ou équivalent, ONNX, CPU) inline sur chaque message — toxicité, PII, sollicitation, contournements unicode/leet. ~2 ms.
- Étage 2 : les messages ambigus (5–10 %) partent en parallèle vers un LLM léger (type Claude Haiku) avec **le contexte de la conversation** (fenêtre de 20 messages) — c'est le contexte qui détecte le grooming, jamais le message isolé. Le message est affiché puis rétro-supprimé si condamné (< 800 ms) ; en conversation adulte↔mineur détectée, on passe en mode « hold » (le message n'apparaît qu'après validation).
- Étage 3 : un agent superviseur par session analyse les **motifs longitudinaux** (adulte qui isole un mineur, demandes de contact hors plateforme, gifting inhabituel) et déclenche escalade humaine + snapshot légal.

**Couche 3 — Voix (budget : < 2 s) :** ASR en streaming (Whisper distillé sur GPU mutualisé) → même pipeline que le texte. La voix est opt-in, réservée aux 13+, désactivable par les parents.

**Couche 4 — Comportemental :** détection d'anomalies sur les graphes d'interaction (un compte adulte qui « suit » systématiquement des comptes mineurs à travers les mondes) — modèle de graphe entraîné sur les signaux des couches 1–3.

**Principes non négociables :**
- Âge : vérification progressive (déclaratif < signaux comportementaux < vérification forte pour la voix et les payouts). Comptes < 13 ans : chat restreint à un vocabulaire autorisé, pas de DM libres.
- Tableau de bord parents avec contrôles réels (temps, dépenses, contacts, mondes).
- Transparence : rapport de modération trimestriel public (volumes, taux, temps de réponse). Roblox ne le fait pas ; c'est un différenciateur de confiance ET un actif réglementaire (DSA-ready).
- Chaque décision de modération est loggée avec le contexte pour l'audit et le réentraînement.

**Pourquoi c'est un actif d'exit :** « Guardian » packagé en API est vendable seul (trust & safety as a service pour plateformes sociales). Dans une due diligence, c'est la réponse à la première question que posera le board de n'importe quel acquéreur coté : « quel est le risque réputationnel mineurs ? ».

## 4. Accessibilité : zéro téléchargement, l'URL comme unité virale

### Le diagnostic

Roblox = 500 Mo+ de client, un compte obligatoire avant de jouer, pas de version web jouable. Chaque étape perd 30–50 % de l'entonnoir. Sur mobile bas de gamme et marchés émergents (Brésil, Indonésie, Inde — les marchés de croissance UGC), le stockage est la barrière n°1.

### La position Senblox : « si tu peux ouvrir un lien, tu peux jouer »

- **`senblox.com/w/<monde>` → en jeu en < 15 s**, sans compte (session invité, progression rattachable a posteriori à un compte). Runtime WASM ~5–8 Mo mis en cache ; assets streamés.
- **Cross-platform par construction** : PC/Mac/Chromebook (navigateur), mobile (navigateur + PWA installable ; app native « coquille » vers les stores plus tard pour la découvrabilité, avec achats redirigés web quand la régulation le permet), VR (WebXR, voir §1).
- **Embeds** : un monde Senblox s'intègre en iframe/Activity dans Discord (SDK Activities), en lien riche sur X/TikTok. Le créateur qui streame son monde donne un lien cliquable → ses viewers jouent pendant le stream. **C'est la boucle de croissance n°1** (voir [03](03_GROWTH_HACKING.md) §2).
- **Cloud streaming = option ciblée, pas défaut** : réservé aux mondes « premium » et aux devices incapables (vieux iOS sans WebGPU) — pour maîtriser le coût/utilisateur.

### Ce qu'on assume comme limite

Le web impose des contraintes (mémoire ~2–4 Go par onglet, pas d'accès disque massif, throttling en arrière-plan). Senblox ne fera pas tourner un open-world de 8 km². C'est un choix : des mondes de 20–100 joueurs, denses, à sessions de 10–40 minutes — exactement le format des hits Roblox (Adopt Me, Blox Fruits sont des expériences bornées, pas des MMO).
