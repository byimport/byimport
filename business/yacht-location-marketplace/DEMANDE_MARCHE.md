# Étude de la demande réelle — partir de ce que les gens cherchent

> Principe : **ne choisis ni la zone, ni les bateaux, ni les prix à l'intuition.** Lis la demande réelle sur internet d'abord, signe les mandats ensuite, construis le site en dernier. L'ordre inverse (joli site → on verra bien) est la première cause d'échec.

## Pourquoi commencer par là

Le nautisme donne une fausse impression d'évidence (« l'été, les gens veulent louer un bateau »). Mais la demande est **très concentrée** :
- par **zone** (un port marche, le port d'à côté à 20 km ne marche pas),
- par **type de bateau** (semi-rigide 6 pers. vs voilier 10 pers. vs yacht 20 m : marchés différents),
- par **moment** (pic de recherche 2–6 semaines avant la date, explosion en juin-juillet),
- par **intention** (« avec ou sans skipper », « pas de permis », « anniversaire », « coucher de soleil »).

Tu veux signer **les bateaux que les gens cherchent vraiment**, pas ceux qu'un propriétaire veut bien te confier.

## Les 5 sources de signal, de la plus fiable à la plus molle

### 1. Volumes de recherche Google (le signal le plus dur)
Ce que les gens tapent = intention d'achat la plus forte.

- **Outils** : Google Keyword Planner (gratuit avec un compte Google Ads), Google Trends (gratuit), et payants : Ahrefs / Semrush / Ubersuggest si budget.
- **Requêtes à mesurer** (décliner par ville) :
  - `location bateau {ville}`, `louer bateau {ville}`, `location yacht {ville}`
  - `location bateau sans permis {ville}`, `bateau avec skipper {ville}`
  - `location bateau journée {ville}`, `coucher de soleil bateau {ville}`
  - `anniversaire bateau {ville}`, `enterrement vie de garçon bateau`, `EVJF bateau`
  - `prix location yacht {ville}`, `location catamaran {ville}`
- **Ce que tu cherches** : une ville avec **>1 000 recherches/mois cumulées** sur le cluster « location bateau » et un **CPC raisonnable** (voir `ACQUISITION_MARKETING.md`). En dessous, le marché est trop petit pour vivre d'un seul port.
- **Astuce** : le Keyword Planner donne aussi la **saisonnalité mensuelle** — capture-la, elle pilote ton budget pub et ta trésorerie.

> 🔌 Ce repo héberge le plugin **Toprank** : les skills `seo:keyword-research`, `seo:seo-analysis` et la connexion **Google Search Console** sont exactement faites pour produire ce rapport de volumes/saisonnalité. Si tu travailles depuis cet environnement, utilise-les plutôt que de tout faire à la main.

### 2. Google Trends — saisonnalité & géographie
- Compare 3–5 villes candidates sur la requête `location bateau` → tu vois laquelle a le plus de momentum et **où** (sous-régions).
- Regarde la courbe sur 5 ans : début de montée (souvent **mars-avril**), pic (**juin-juillet**), chute (**septembre**). Ça te dit **quand** lancer la pub et **quand** signer les mandats (avant la montée, soit **février-mars**).
- Onglet « Requêtes associées / en hausse » = idées d'angles et de niches émergentes.

### 3. Les marketplaces existantes (Click&Boat, SamBoat, GetMyBoat, Samboat, Boatsetter)
C'est de l'**or** : ce sont des données de demande **déjà monétisée**.
- Sur la zone visée, regarde : combien d'annonces, quels **types de bateaux dominent**, quelles **fourchettes de prix**, quels bateaux affichent **« souvent réservé » / beaucoup d'avis** (= demande prouvée).
- Lis les **avis** : ce que les gens adorent (skipper sympa, apéro inclus, propreté) et ce qui les déçoit (retard, bateau différent des photos, frais cachés). C'est ton cahier des charges qualité **gratuit**.
- Repère les **trous** : type de bateau très cherché mais peu d'offre = ta niche d'entrée.

### 4. Social listening (demande latente + esthétique qui marche)
- **Instagram / TikTok** : cherche `#locationbateau{ville}`, `#yacht{ville}`, `#boatrental{ville}`. Regarde les vues et l'engagement — ça dit quel **visuel** déclenche le désir (coucher de soleil, crique turquoise, apéro à bord). Ça nourrit directement `CONTENU_VIDEO_CANVA.md`.
- **Groupes Facebook locaux / forums** (tourisme, EVJF/EVG, mariages) : les gens y demandent « quelqu'un connaît une loc de bateau pas chère à {ville} ? ». Demande réelle, non captée, à la source.

### 5. Demande directe (le test ultime, presque gratuit)
Avant de signer 10 bateaux, **teste la demande avec un mini-test** :
- Une **landing page** simple (1 page, 3 bateaux fictifs ou réels sous accord verbal) + un petit budget Google Ads (200–300 €) sur `location bateau {ville}`.
- Tu ne factures pas encore : tu mesures **taux de clic, demandes de devis, créneaux demandés**. Si personne ne remplit le formulaire à 300 € de pub, le problème n'est pas le bateau — c'est la zone ou l'offre.
- Ce **smoke test** te coûte un week-end et 300 € ; il t'évite de signer des mandats et bâtir un site pour rien.

## Du signal à la décision — ce que tu en fais concrètement

| Signal collecté | Décision qu'il pilote |
|-----------------|----------------------|
| Cluster de mots-clés le plus volumineux par ville | **Choix de la zone n°1** |
| Types de bateaux les plus cherchés / les mieux notés | **Quels bateaux signer en priorité** (`OFFRE_ET_YACHTS.md`) |
| Fourchettes de prix des marketplaces + « souvent réservé » | **Ton pricing public et ton tarif net cible** (`MODELE_ECONOMIQUE.md`) |
| Saisonnalité Google Trends | **Calendrier budget pub + trésorerie** (`BUDGET_KPIS.md`) |
| Angles/visuels qui buzzent (TikTok/IG) | **Briefs des vidéos carrées** (`CONTENU_VIDEO_CANVA.md`) |
| Plaintes récurrentes dans les avis | **Tes engagements qualité** (= ton avantage concurrentiel) |
| Résultat du smoke test 300 € | **Go / No-go sur la zone** |

## Boucle continue (ne pas faire qu'une fois)
La demande bouge (météo, événements, tendances). Mets en place une **revue mensuelle** :
- export Keyword Planner + Google Trends (volumes, nouvelles requêtes),
- top recherches internes de ton propre site (Search Console + barre de recherche interne),
- nouveaux bateaux/prix chez les concurrents,
- mots-clés convertisseurs de tes campagnes (les vrais gagnants viennent souvent de requêtes longues que tu n'avais pas anticipées).

→ Tu réinjectes ça dans les **bateaux à signer**, le **pricing** et les **angles de contenu**. C'est ce qui « améliore la demande client » dans le temps : tu fais coïncider de plus en plus finement ton offre avec ce que les gens cherchent vraiment.

## Honnêteté
- **Un gros volume de recherche ≠ business rentable** s'il y a 200 concurrents et des CPC à 4 €. Croise toujours volume **et** concurrence **et** marge possible.
- **La donnée oriente, elle ne décide pas seule.** Le smoke test réel (étape 5) tranche les cas ambigus mieux que n'importe quel outil de volume.
- **Ne te noie pas dans l'analyse.** 1 semaine de recherche sérieuse suffit pour choisir une zone. Le reste s'apprend en vendant.
