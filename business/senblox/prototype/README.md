# Senblox — prototype 3D multijoueur (test de H1)

Un monde 3D partagé jouable dans le navigateur **sans téléchargement ni compte** : on ouvre un lien, on joue. Serveur autoritatif Node (30 Hz), client three.js avec prédiction/réconciliation. Il sert à **mesurer** l'hypothèse H1 de `../00_REALITE_CHECK.md`, pas à être une démo : lire d'abord **[H1_RESULTS.md](H1_RESULTS.md)** (H1 reste ouvert, avec le protocole à exécuter sur un vrai téléphone).

## Lancer

```bash
cd business/senblox/prototype
npm ci
npm run build          # client -> dist/client
npm start              # http://localhost:8787  (PORT / HOST pour changer)
```

Ouvrir `http://localhost:8787/w/<salle>` : chaque salle est un monde (graine dérivée du nom). **Copier le lien** invite quelqu'un dans la même salle.

Contrôles : ZQSD/WASD ou flèches, Espace pour sauter, Q/E pour tourner la caméra, clic pour capturer la souris. Sur mobile : joystick flottant à gauche, glisser à droite pour regarder, bouton SAUT.

Paramètres d'URL : `?renderer=webgpu` (WebGPU, repli WebGL ; contexte sécurisé requis), `?adaptive=0` (désactive la résolution dynamique), `?bench=1&dur=30&warm=3` (benchmark + rapport JSON).

## Vérifier

```bash
npm run typecheck      # tsc
npm test               # 15 tests unitaires (simulation, protocole, gestion d'intérêt)
npm run e2e            # 11 contrôles dans un vrai Chromium (nécessite le build)
npm run bots -- --n 100 --duration 60 [--cluster 25]   # charge serveur (serveur lancé à part)
npm run bench          # temps jusqu'au premier affichage sous 4G émulée + frames avec bots
npx tsx tools/screenshot.ts out.png                    # capture du rendu
```

`e2e`, `bench` et `screenshot` utilisent le Chromium préinstallé (`CHROMIUM_PATH` pour en changer) en rendu logiciel : leurs fps ne prouvent rien sur un GPU mobile.

Endpoints serveur : `GET /health`, `GET /metrics` (`?reset=1` remet la fenêtre à zéro), `POST /report` (enregistre un rapport de benchmark dans `reports/`).

## Architecture

```
shared/   simulation + monde + protocole, importés à l'identique par client et serveur
server/   boucle 30 Hz par salle, gestion d'intérêt, HTTP statique + WebSocket, métriques
client/   rendu three.js (instanciation), réseau (prédiction, interpolation), entrées, HUD
tools/    bots de charge, e2e Playwright, benchmark, capture d'écran
test/     vitest
```

Choix clés : simulation à pas fixe **déterministe et partagée** (le client rejoue ses entrées non acquittées sur l'état serveur) ; protocole binaire quantifié (entités de 11 octets, snapshots à 15 Hz par client) ; gestion d'intérêt par grille avec hystérésis ; aucun asset externe (monde procédural) ; décor et avatars en `InstancedMesh` (13 draw calls).

## Limites connues

Pas d'authentification, d'anti-triche, de persistance ni de modération. Bande passante hors budget en foule dense (voir H1_RESULTS.md). Les entités absentes d'un snapshot sont supprimées côté client : toute réduction de fréquence par distance demandera un message de retrait explicite.
