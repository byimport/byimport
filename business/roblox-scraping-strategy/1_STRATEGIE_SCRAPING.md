# Étape 1 — Stratégie de scraping ciblé

> Objectif : obtenir des signaux **fiables et croisables** sur (a) la santé d'une expérience, (b) la santé du marché UGC, (c) ce que les joueurs demandent et reprochent. On ne scrape pas « tout » — on scrape ce qui pilote une décision.

## A. Roblox Web API & Marketplace (la source primaire, faits durs)

Roblox expose des API web publiques par sous-domaines. Ce sont des données **structurées et fiables** : à privilégier comme socle. Toujours respecter les quotas (HTTP 429 = backoff exponentiel) et un `User-Agent` identifiable.

| Donnée | Endpoint type | Métrique clé extraite | Pourquoi c'est business-critique |
|---|---|---|---|
| Joueurs simultanés (CCU) | `games.roblox.com/v1/games?universeIds=...` → champ `playing` | CCU instantané, à échantillonner toutes les 5–15 min | Proxy n°1 de la traction temps réel ; sa **courbe horaire/journalière** révèle les pics et le churn |
| Visites & favoris | même endpoint → `visits`, `favoritedCount` | Visites cumulées, ratio favoris/visites | Favoris/visites = intention de revenir (signal de rétention douce) |
| Votes | `games.roblox.com/v1/games/votes?universeIds=...` → `upVotes`/`downVotes` | **Ratio d'approbation** = up / (up+down) | < 70 % = problème de qualité perçue ; sous 80 % il faut enquêter |
| Classements / découverte | `games.roblox.com/v1/games/list` (tris « popular », « top-rated »), pages de tri | Rang par catégorie, présence dans « Up-and-Coming » | Mesure la dépendance à l'algo de découverte vs. trafic organique |
| Items UGC (catalogue) | `catalog.roblox.com/v1/search/items/details`, `economy.roblox.com/v2/assets/{id}/details` | Prix (Robux), `sales` (volume de ventes), `favoritedCount`, dispo limitée/quantité | Volume de ventes UGC = quels **styles cosmétiques** se vendent réellement |
| Reventes / collector | `economy.roblox.com` (resellers, prix plancher) sur items limités | Prix plancher, volume de reventes | Détecte la demande spéculative sur un style/cosmétique |
| Passes & produits | `games.roblox.com/v1/games/{universeId}/game-passes`, détails produit | Liste des Gamepasses, prix | Cartographie l'offre de monétisation existante (la sienne **et celle des concurrents**) |
| Groupe / communauté | `groups.roblox.com/v1/groups/{id}` | Membres, croissance | Taille de l'audience captive (canal de re-engagement gratuit) |

**Rétention — la nuance importante.** Le taux de rétention « jour 1 / jour 7 » **n'est pas exposé par les API publiques** ; il vit dans le tableau de bord créateur (Roblox Creator Analytics / Open Cloud Analytics API, accessibles seulement au propriétaire de l'expérience avec une clé API). Pour une expérience **tierce** (concurrent), la rétention se **reconstruit par proxy** :
- échantillonnage CCU longitudinal → forme de la courbe de rétro-engagement (un jeu qui retient a un plancher de CCU élevé hors pic) ;
- ratio favoris/visites et croissance des membres du groupe ;
- vélocité des votes dans le temps.

Pour **sa propre** expérience, on branche directement l'**Open Cloud Analytics API** (D1/D7 retention, session time, funnels) — c'est la vraie source, pas du scraping.

## B. Sites communautaires sérieux & analytics tiers

Ces sources agrègent et historisent ce que les API ne gardent pas (séries temporelles longues, classements de marché).

| Source | Donnée extraite | Usage |
|---|---|---|
| **RoMonitor Stats** | Historique CCU, courbes de croissance, milestones par expérience | Tendance long terme + benchmark vs. concurrents directs |
| **Rolimon's** | Valeurs/volumes des items limités, demande collector | Pricing UGC et détection des styles à forte demande |
| **DevForum Roblox** (sections *Bug Reports* & *Feature Requests*) | Bugs plateforme confirmés, demandes de fonctionnalités API | Anticiper les pannes plateforme et les capacités Luau à venir |
| **Roblox Status / DevForum Announcements** | Incidents plateforme, changements d'API | Distinguer « notre bug » de « bug Roblox » avant de coder un correctif |
| **Bloxlink** (et bots de vérification) | Lien compte Discord ↔ Roblox, taille des serveurs communautaires | Mesurer la communauté Discord réellement rattachée au jeu |

> Garde-fou : RoMonitor / Rolimon's ont leurs propres CGU et certaines pages se chargent en JavaScript (données via leurs endpoints internes). Privilégier une API publique officielle quand elle existe, mettre en cache, et ne pas marteler le site.

## C. Plateformes de feedback externe (la demande latente, texte non structuré)

C'est ici qu'on capte ce que les joueurs **ressentent** mais ne mettent pas dans un vote. Données textuelles → traitées à l'étape 2.

| Source | Quoi extraire | Pattern recherché |
|---|---|---|
| **Discord** du jeu + serveurs concurrents majeurs | Messages des salons `#bug-report`, `#suggestions`, `#general` | Fréquence et récurrence d'une plainte (signal = répétition, pas un message isolé) |
| **r/robloxgamedev** | Discussions techniques, ce que les devs concurrents implémentent | Tendances de game design, mécaniques qui marchent |
| **r/Roblox** + subreddits du jeu | Plaintes joueurs, comparaisons entre jeux | Frustrations de gameplay, attentes non satisfaites |
| **Avis / commentaires in-experience** & réseaux (TikTok/YouTube commentaires) | Verbatims spontanés | Le « pourquoi j'ai arrêté de jouer » |

**Méthode d'extraction des patterns :**
1. Collecte des verbatims (export Discord via API bot autorisé sur **ses propres** serveurs ; API Reddit officielle avec clé).
2. Normalisation (langue, déduplication, suppression du spam/bots).
3. Comptage de fréquence par thème + pondération par **portée** (un message vu par 5 000 membres pèse plus qu'un message isolé).
4. Sortie : une liste de plaintes/demandes **classées par récurrence**, prête pour le protocole d'analyse (étape 2).

## D. Cadence & architecture de collecte

- **CCU / votes** : échantillonnage toutes les **5–15 min** (séries temporelles → détection de churn et d'effet d'événement).
- **Catalogue UGC / ventes** : **quotidien** (le volume de ventes bouge à l'échelle du jour).
- **Feedback texte** : collecte continue, **agrégation hebdomadaire** pour lisser le bruit.
- **Stockage** : base time-series (CCU/votes) + table relationnelle (items, ventes) + index texte (verbatims). Horodatage UTC systématique.

## E. Garde-fous légaux & éthiques (non négociable)

- **API officielles d'abord**, dans les limites de débit ; backoff sur 429 ; jamais de contournement d'authentification ni de scraping de données privées/de mineurs.
- **CGU des sites tiers** (RoMonitor, Rolimon's, Reddit, Discord) respectées ; utiliser leurs API officielles quand elles existent.
- **Discord** : un bot ne lit que les serveurs où il est **invité et autorisé** ; pas d'aspiration de DM ni de serveurs tiers sans consentement.
- **Données personnelles** : on agrège des signaux produit, pas des profils individuels. Pas de PII stockée.
- **Open Cloud (sa propre expérience)** : clé API scoppée, en variable d'environnement, jamais commitée.

> En résumé : la donnée *dure* (API Roblox + Open Cloud sur son propre jeu) fonde les décisions ; la donnée *molle* (feedback texte) explique le « pourquoi » et alimente les specs. Aucune décision ne repose sur une seule métrique.
