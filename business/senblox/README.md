# Senblox — Plateforme de jeu & création UGC (dossier stratégique)

**Thèse :** construire une plateforme de jeux créés par les utilisateurs (UGC gaming) qui corrige les quatre défauts structurels de Roblox — graphismes datés, partage de revenus punitif (~30 % aux créateurs), modération défaillante, client lourd — puis la positionner comme cible d'acquisition pour Epic Games, Microsoft, Meta ou Sony dans une fenêtre de 24 à 36 mois.

## Structure du dossier

| Fichier | Contenu |
|---|---|
| [00_REALITE_CHECK.md](00_REALITE_CHECK.md) | Ce qu'un CTO honnête doit dire avant de dépenser un euro : les vrais obstacles, les hypothèses à valider, le capital requis |
| [01_POSITIONNEMENT_STRATEGIQUE.md](01_POSITIONNEMENT_STRATEGIQUE.md) | Les 4 axes de différenciation vs Roblox : moteur/graphismes, DevEx créateurs, modération IA temps réel, accessibilité zéro-download |
| [02_ARCHITECTURE_TECHNIQUE_MVP.md](02_ARCHITECTURE_TECHNIQUE_MVP.md) | Architecture complète : client WebGPU, serveurs de jeu Agones/K8s, données, réseau QUIC/WebTransport, et Senblox Studio (création no-code assistée par IA) |
| [03_GROWTH_HACKING.md](03_GROWTH_HACKING.md) | Acquisition des 100 premiers créateurs et 100 000 premiers joueurs sans budget marketing ; conception de l'économie SenBucks |
| [04_STRATEGIE_EXIT.md](04_STRATEGIE_EXIT.md) | KPIs cibles par phase, packaging technologique par acquéreur, déroulé du processus M&A |

## Résumé exécutif (5 points)

1. **Le produit** : des mondes 3D jouables instantanément dans le navigateur (WebGPU, < 15 s entre le clic et le jeu), créés par des développeurs indépendants via un studio no-code/low-code où l'IA génère scripts, assets et textures à partir de prompts.
2. **Le levier économique** : reverser **70 % des revenus nets aux créateurs** (vs ~24–30 % effectifs chez Roblox). C'est le mécanisme d'acquisition de l'offre — les meilleurs créateurs Roblox sont économiquement rationnels et sous-payés.
3. **Le levier confiance** : une pile de modération IA multimodale temps réel (texte, voix, assets 3D, comportements) conçue *avant* le lancement, pas rattrapée après scandale. C'est l'argument décisif auprès des parents et des régulateurs — et un actif technologique revendable seul.
4. **Le levier distribution** : zéro téléchargement. Un lien = un jeu. Chaque monde Senblox est une URL partageable sur TikTok, Discord, YouTube — la boucle virale que Roblox (client de 500 Mo) ne peut pas répliquer.
5. **L'exit** : ne pas viser « devenir Roblox » (capitalisation ~30 Md$, 15 ans d'avance) mais devenir **la brique manquante évidente** d'un géant : runtime metaverse web pour Meta, pipeline UGC-IA pour Microsoft/Xbox, couche sociale jeune pour Sony, canal de distribution instantané pour Epic.

## Séquencement global

- **Phase 0 (mois 0–3)** — Prototype technique : un monde jouable multi-joueurs dans le navigateur + démo Studio IA. Objectif : lever un pre-seed sur la démo.
- **Phase 1 (mois 3–9)** — MVP fermé : 20–50 créateurs partenaires payés, 10 000 joueurs en alpha, boucle économie/paiement fonctionnelle.
- **Phase 2 (mois 9–18)** — Lancement public : croissance organique via la boucle URL-virale, 100+ créateurs actifs monétisés, série A.
- **Phase 3 (mois 18–36)** — Échelle & exit : KPIs d'acquisition atteints (voir [04](04_STRATEGIE_EXIT.md)), process M&A avec 2+ acquéreurs en compétition.

---
*Document de travail interne. Aucun lien avec le plugin Toprank ; ce dossier vit dans `business/` conformément aux conventions du dépôt.*
