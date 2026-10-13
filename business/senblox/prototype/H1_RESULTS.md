# H1 — Résultats du prototype

> **Verdict : H1 reste OUVERT.**
> Ce prototype prouve que l'architecture tient (serveur autoritatif, prédiction, jeu instantané par lien, 191 Kio de téléchargement). Il **ne prouve pas** le point décisif de H1 : *60 fps sur un téléphone Android milieu de gamme*. Cet environnement n'a pas de GPU ; ce chiffre ne peut venir que d'un vrai appareil. Le protocole est en §4, avec un tableau à remplir.

H1 (de `00_REALITE_CHECK.md` §6) : *« un monde 3D multi-joueurs à 60 fps sur un téléphone Android milieu de gamme, dans Chrome, via WebGPU/WebGL2 »*. Si H1 échoue, la thèse « zéro téléchargement » est menacée.

## 1. Ce qui a été mesuré ici

Environnement : conteneur Linux 4 cœurs, Node 22, Chromium headless **sans GPU (rasteriseur logiciel SwiftShader)**, tout sur `localhost`. Chiffres reproductibles avec les commandes de `README.md`.

### Serveur autoritatif — 100 bots, 60 s chacun

| | Déplacement libre | Foule dense (63 visibles en permanence) | Cible du dossier |
|---|---|---|---|
| Bande passante descendante par joueur | **35,6 kbit/s** | **85,7 kbit/s** | 20–40 kbit/s |
| Joueurs visibles (moyenne) | 25 | 63 (plafond) | — |
| Temps de tick, moyenne | 1,3 ms | 2,7 ms | — |
| Temps de tick, p99 | **9,2 ms** | **19,1 ms** | < 10 ms |
| Temps de tick, max | 24 ms | **52 ms** | < 33 ms (période) |
| CPU serveur | 9 % d'un cœur | 13 % d'un cœur | — |
| Dérive mémoire (60 s, après échauffement) | ≈ 0 Mo | 0,1 Mo | aucune |
| Déconnexions | 0 | 0 | 0 |

Lecture honnête :
- **Déplacement libre** : dans le budget. Le p99 passe de justesse.
- **Foule dense** : **hors budget**. 86 kbit/s est le double de la cible, et le maximum de 52 ms dépasse la période de tick (33 ms), donc des ticks prennent du retard. Un monde où 60+ joueurs se tassent au même endroit (un événement, un spawn) n'est pas tenu par cette version.
- Le p99 élevé ne vient pas de la simulation : `Room.step()` mesuré seul (100 joueurs, sans socket) donne p99 = 2,4 ms. Il vient des écritures réseau et de la gigue de la VM. Le ramasse-miettes n'est pas en cause (2 pauses sur 205 dépassent 3 ms).
- Leviers connus, **non implémentés** : fréquence réduite pour les entités lointaines (exige un message de retrait explicite, car aujourd'hui « absent du snapshot » signifie « supprimé »), compression delta, écriture groupée des sockets.
- Un premier essai de 20 s donnait 58 kbit/s : les bots démarrent tous au point d'apparition et se dispersent. Les 60 s sont plus représentatifs ; le biais d'un essai court est réel.

### Client — taille et temps jusqu'au jeu

| | Mesure |
|---|---|
| Téléchargement total, chemin par défaut (WebGL2) | **191 Kio** transférés (three.js inclus, gzip) |
| Chunk WebGPU (`?renderer=webgpu` uniquement) | +197 Ko gzip, chargé à la demande |
| Clic → première image jouable, sans bridage | 0,49 s |
| … réseau « Fast 4G » émulé (9 Mbit/s, 40 ms) | 0,71 s |
| … « Slow 4G » émulé (1,6 Mbit/s, 150 ms) | **1,80 s** |
| … « Slow 4G » + CPU ralenti ×4 | 2,04 s |

Médiane de 3 essais, cache désactivé, viewport mobile. La promesse « < 15 s » est tenue avec une très large marge **dans ces conditions**. Limites : l'émulation réseau de Chromium ne bride pas les trames WebSocket (seulement les téléchargements HTTP) ; la latence réelle vers un serveur distant s'ajoute ; ce n'est pas un vrai téléphone.

### Correction fonctionnelle

- 15 tests unitaires : simulation déterministe, collisions, atterrissage sur plateforme, **la réconciliation client rejoue exactement l'état prédit**, aller-retour du protocole, gestion d'intérêt (hystérésis, plafond).
- 11 contrôles de bout en bout dans un vrai navigateur : le rendu n'est pas vide, le clavier déplace l'avatar, la position serveur égale la prédiction client (0,00 m d'écart), le saut décolle, deux navigateurs se voient, un joueur déconnecté disparaît, aucune erreur console.

### Frames dans le navigateur — **non exploitable pour H1**

Rendu logiciel, 60 bots, viewport 390×780 @2x : 10 fps, p50 83 ms, p95 217 ms, 13 draw calls. Le rapport se marque lui-même `valid: false` / `not-measurable`. C'est le coût du rasteriseur CPU, **pas** celui d'un GPU mobile. Ce chiffre ne dit ni que H1 est tenu, ni qu'il est perdu. La seule information utile : 13 draw calls pour toute la scène, grâce à l'instanciation.

## 2. Ce que ce prototype ne prouve pas

1. **60 fps sur Android milieu de gamme** — le point central de H1. Non mesuré.
2. WebGPU réel. Il est implémenté (`?renderer=webgpu`, repli WebGL) mais jamais exécuté sur un GPU ici ; il requiert un contexte sécurisé (HTTPS ou `localhost`).
3. Le comportement sous latence internet réelle et perte de paquets (tout est local ; WebSocket/TCP, pas WebTransport).
4. Le « runtime propriétaire Rust/wgpu » de `01_` et `02_` : ce prototype est TypeScript + three.js (voir §5).
5. Tout ce qui est hors périmètre : comptes, économie, modération, Studio, anti-triche (un client malveillant peut tricher sur la cadence d'entrées dans les limites de `MAX_INPUTS_PER_TICK`).

## 3. Écarts par rapport au plan approuvé

- **Rendu par défaut : WebGL2, WebGPU en option.** Le plan disait « WebGPURenderer avec repli WebGL2 automatique ». `three/webgpu` ajoute ~197 Ko gzip : le charger par défaut aurait doublé le téléchargement pour un gain non démontré. Les deux sont à comparer sur appareil (`?renderer=webgpu`).
- **Snapshots à 15 Hz et interpolation à 150 ms** (le plan disait 100 ms) : 15 Hz est nécessaire pour la bande passante ; 150 ms donne deux snapshots à blender.
- **Bande passante hors cible en foule dense** (§1), alors que le plan visait 20–40 kbit/s.

## 4. Protocole à exécuter sur un vrai téléphone

Objectif : remplir le tableau ci-dessous avec un appareil **milieu de gamme** (ex. Pixel 6a, Galaxy A5x, ou plus modeste), Chrome, batterie > 50 %, mode économie d'énergie désactivé, écran allumé.

1. Sur un poste : `cd business/senblox/prototype && npm ci && npm run build && npm start`.
2. Exposer le serveur au téléphone :
   - même Wi-Fi : `http://<IP-du-poste>:8787` (WebGL2 fonctionne ; **WebGPU exige HTTPS**) ;
   - ou tunnel HTTPS (ex. `cloudflared tunnel --url http://localhost:8787`) pour tester aussi `renderer=webgpu`.
3. Dans un second terminal, remplir la salle : `npm run bots -- --n 60 --duration 120 --room h1 --cluster 30`.
4. Sur le téléphone, ouvrir **`/w/h1?bench=1&dur=30`** (WebGL2), puis **`/w/h1?bench=1&dur=30&renderer=webgpu`**. Ne pas toucher l'écran pendant 35 s.
5. Un rapport JSON s'affiche à l'écran (bouton **Copier**) et est sauvegardé dans `reports/` sur le serveur. L'envoyer ou le coller dans le tableau.
6. Répéter 3 fois par rendu et garder la **médiane** ; noter la température du téléphone (les mobiles ralentissent à chaud).

Critères du rapport : `meets-60fps` = p50 ≤ 17,5 ms et p95 ≤ 20 ms ; `playable-30fps` = p95 ≤ 36 ms ; sinon `below-30fps`. Un rapport `valid: false` (rendu logiciel détecté) ne compte pas.

| Appareil | Chrome | Rendu | fps | p50 ms | p95 ms | Échelle finale | Signal H1 | Date |
|---|---|---|---|---|---|---|---|---|
| _à remplir_ | | WebGL2 | | | | | | |
| _à remplir_ | | WebGPU | | | | | | |

**Règle de décision (à confirmer avec vous) :** si le milieu de gamme tient `meets-60fps` ou au minimum `playable-30fps` avec une résolution ≥ 0,75, H1 tient et la thèse web-first est confortée. Si p95 > 36 ms même à échelle 0,5, H1 échoue : le plan prévoit alors un pivot (streaming cloud ou client natif léger), donc ne rien construire de plus avant cette réponse.

## 5. Conséquence pour le dossier stratégique

Ce prototype est du TypeScript/three.js, pas du Rust/wgpu. Il valide la **catégorie** (un monde multijoueur en navigateur sur un lien), pas le **fossé technologique** décrit dans `01_` et `02_`. Si le profilage sur appareil montre que three.js est le goulot, alors seulement le runtime propriétaire est justifié ; sinon c'est de l'ingénierie coûteuse pour un gain non prouvé, et l'argument d'exit « runtime introuvable ailleurs » serait à réécrire.
