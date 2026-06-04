# Acquisition — faire venir les clients

> Deux moteurs complémentaires : **l'intention** (Google : le client cherche déjà à louer → tu captes) et **la demande latente** (Meta/TikTok : tu crées l'envie avec le visuel). Le contenu (`CONTENU_VIDEO_CANVA.md`) alimente le second ; les pages SEO (`SITE_WEB.md`) le premier.

## 1. Google Ads — capter l'intention (priorité court terme)

C'est là que se trouve l'argent prêt à être dépensé : quelqu'un qui tape « location bateau {ville} » veut louer **maintenant**.

- **Structure par intention** (issue de `DEMANDE_MARCHE.md`) :
  - Campagne « location générique » : `location bateau {ville}`, `louer bateau {ville}`
  - Campagne « sans permis » : `location bateau sans permis {ville}` (souvent moins chère, forte conversion)
  - Campagne « avec skipper / luxe » : `location yacht {ville}`, `bateau avec skipper {ville}`
  - Campagne « occasion » : `EVJF bateau`, `anniversaire bateau`, `coucher de soleil bateau {ville}`
- **Mots-clés négatifs** indispensables : `permis`, `achat`, `vente`, `prix d'un yacht`, `emploi`, `formation`, `pas cher` (selon ta cible), `croisière {compagnie}`.
- **Annonces** : prix d'appel (« dès X €/journée »), « skipper inclus », « réservation en ligne », « annulation flexible ». Extensions : lieu, appel, liens vers Expériences.
- **Landing** : envoie vers la **page locale dédiée**, pas l'accueil. `location bateau Cannes` → `/location-bateau-cannes`.
- **CPC à attendre** : très variable selon zone (souvent **0,80–3 €** sur le loisir, plus cher sur « yacht » luxe). Mesure-le dans le Keyword Planner avant de budgéter.
- **Budget test** : 1 500–3 000 € sur 30 jours, 1 zone. Coupe les mots-clés au-dessus du CPA cible (cf. `BUDGET_KPIS.md`).

> 🔌 Le plugin **Toprank** de ce repo (skills `google-ads:manage`, `google-ads:audit`, `google-ads:landing` + MCP NotFair-GoogleAds) gère la création, l'audit et l'optimisation de ces campagnes. Idem `google-ads:copy` pour les annonces.

## 2. Meta (Instagram/Facebook) + TikTok — créer l'envie

La location de bateau est un **achat émotionnel et visuel** → c'est le terrain idéal du social.

- **Créatifs = le levier n°1.** Tes vidéos carrées (`CONTENU_VIDEO_CANVA.md`) sont le carburant. Teste 3–5 créatifs, garde les gagnants.
- **Structure simple au début** : 1 campagne conversion (objectif : réservation/lead), 1 audience large géolocalisée (laisse l'algo trouver), retargeting des visiteurs site + vues vidéo.
- **Audiences** :
  - **Géo** : touristes présents dans la zone (ciblage « voyage récent » / visiteurs) + locaux aisés.
  - **Centres d'intérêt** : voyage, luxe, sorties, mariage (EVJF/EVG), yachting.
  - **Retargeting** : visiteurs fiche bateau non convertis, abandons de tunnel, vues vidéo > 50 %.
  - **Lookalike** des acheteurs une fois que tu as ~50–100 réservations.
- **Formats** : Reels/feed carré + vertical, collection, et **lead form** pour les demandes de devis (gros paniers / luxe).
- **Budget test** : 1 000–2 000 € / 30 jours.

> 🔌 Skills `meta-ads:manage` / `meta-ads:audit` + MCP NotFair-MetaAds pour piloter et auditer ces campagnes.

## 3. Organique social — coût marginal nul, effet cumulatif

- Poste **3–5 vidéos carrées/semaine** sur IG + TikTok + FB (cf. cadence `CONTENU_VIDEO_CANVA.md`).
- **Géolocalise** et hashtag local (`#locationbateau{ville}`).
- **UGC clients** : repartage des vidéos clients (preuve sociale + portée gratuite).
- L'organique ne paie pas tout de suite mais **baisse ton CAC dans le temps** et nourrit le retargeting.

## 4. SEO local — rentabilité long terme

- **Pages locales** par zone et par intention (cf. `SITE_WEB.md`).
- **Google Business Profile** par port : avis, photos, posts → capte le « près de moi » et la Map.
- **Contenu** : guides (« Que faire en bateau à {ville} », « Louer un bateau sans permis : le guide »), schémas, maillage interne.
- Le SEO met 3–6 mois à payer mais devient ta **source la moins chère** une fois installé.

> 🔌 Skills `seo:keyword-research`, `seo:content-planner`, `seo:content-writer`, `seo:seo-page`, `seo:geo-optimizer` + Google Search Console.

## 5. Partenariats & distribution — du volume rapide, peu de cash

- **Hôtels, conciergeries, Airbnb hosts, agences de voyage locales, wedding planners** : ils ont les clients, pas le service bateau. Commission d'apporteur (10–20 %).
- **Offices de tourisme, clubs de plage, hôtels haut de gamme** : présentoirs, QR codes, codes promo traçables.
- **Marketplaces (Click&Boat, SamBoat, GetMyBoat)** : double usage —
  1. **canal de vente** au début (tu écoules tes mandats là où le trafic est déjà),
  2. **filet** : les demandes que tu ne peux pas honorer, tu les renvoies en affiliation plutôt que de perdre le lead.

## Mix recommandé par phase

| Phase | Google Ads | Meta/TikTok | Organique | SEO | Partenariats |
|---|---|---|---|---|---|
| Test (M1) | 55 % | 35 % | 5 % | 0 % | 5 % |
| Optim (M2–3) | 45 % | 35 % | 5 % | 10 % | 5 % |
| Croisière (M6+) | 35 % | 30 % | 5 % | 20 % | 10 % |

## Honnêteté
- **Ne lance pas 5 canaux en même temps.** Démarre Google + Meta sur **1 zone**. Maîtrise-les, puis ajoute SEO/partenariats. Sinon tu dilues le budget et tu ne sais pas ce qui marche.
- **Le CAC en haute saison ≠ basse saison.** La concurrence publicitaire explose en juin-août → CPC plus chers mais conversion plus haute. Budgète en conséquence (cf. saisonnalité, `DEMANDE_MARCHE.md`).
- **Sans tracking propre, tu pilotes à l'aveugle.** GA4 + conversions + valeur de réservation **avant** de dépenser le premier euro de pub.
