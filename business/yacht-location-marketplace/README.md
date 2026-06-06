# Place de marché — location & vente de yachts (modèle marge 20–50 %)

> ⚠️ **Note** : Ce dossier contient des documents business sans rapport avec le plugin Toprank. Conservé en branche, ne touche ni `VERSION` ni `CHANGELOG.md`. Peut être exporté (PDF, Drive) sans impact sur le plugin.

## Idée en une phrase

Construire un (ou plusieurs) **site(s) vitrine + réservation** qui mettent en avant des yachts en **location** (à la journée / à la semaine) et à la **vente**, **sans posséder les bateaux** : on les référence sous mandat auprès de propriétaires et de bases nautiques, on les commercialise avec de la pub et du contenu vidéo (carré, façon Reels/TikTok produit sous Canva), et on prend une **marge**.

## ⚠️ La vérité sur la marge « 20 % à 50 % » — à lire avant tout le reste

C'est le cœur de la demande, et c'est là qu'il faut être honnête, sinon tout le plan repose sur du sable :

- **Courtage classique (modèle MYBA)** : la commission standard du courtage de yacht de luxe est de **15 %** sur le prix de location, et **~8–10 %** sur la vente. Tu **n'atteindras pas 20–50 % en faisant du courtage pur**. Si quelqu'un te promet ça, c'est faux.
- **Place de marché P2P (Click&Boat, SamBoat, GetMyBoat)** : ces plateformes prennent **15–20 %** (part locataire + part propriétaire cumulées). C'est le plafond du modèle « pur intermédiaire ».
- **Comment atteindre réellement 20–50 %** → il faut sortir du courtage pur et choisir UN de ces trois modèles (détaillés dans `MODELE_ECONOMIQUE.md`) :
  1. **Achat-gros / revente-détail** : tu négocies un **tarif net** avec le propriétaire (ex. 800 €/jour net), tu revends en public à 1 100–1 200 € (marge 30–50 % sur le net). Tu portes le risque commercial (invendu = 0, pas une perte), pas le risque de possession.
  2. **Packaging d'expérience** : tu ne vends pas « un bateau », tu vends une **journée tout compris** (bateau + skipper + apéritif/traiteur + photographe + transferts). La marge se fait sur le **bundle** (les à-côtés se margent à 40–60 %), pas sur la coque.
  3. **Day-charter haute rotation** : petites unités (6–12 pers., zone touristique), créneaux demi-journée, forte demande estivale, prix dynamique. Marge atteignable 25–40 % en propre via mandats d'exclusivité locale.

**Conclusion honnête** : vise **20–35 % réaliste** en croisière, 50 % seulement sur les ventes additionnelles (extras) et les pics de saison. Construis le P&L sur 25 %, pas sur 50 %.

## 📂 Contenu du dossier

| Fichier | Usage |
|---------|-------|
| `DEMANDE_MARCHE.md` | **Point de départ.** Comment lire la demande réelle sur internet (Google Trends, volumes de recherche, marketplaces, social listening) pour choisir la zone, les bateaux et les prix sur des données — pas des intuitions. |
| `MODELE_ECONOMIQUE.md` | Les 3 modèles de marge, comment atteindre 20–50 % concrètement, unit economics par réservation, risques de chaque modèle. |
| `OFFRE_ET_YACHTS.md` | **Côté offre** : comment mettre des yachts en ligne sans les posséder — mandats propriétaires, bases nautiques, contrats de référencement, exclusivité, tarif net. C'est le vrai goulot d'étranglement. |
| `SITE_WEB.md` | Architecture du site : stack, pages, tunnel de réservation, paiement/acompte, **le site « vidéos carrées »**, SEO technique. |
| `CONTENU_VIDEO_CANVA.md` | L'usine à contenu : vidéos carrées 1:1 sous Canva, templates, cadence de production, réutilisation pub + organique. |
| `ACQUISITION_MARKETING.md` | Google Ads (intention « location bateau {ville} »), Meta/Instagram/TikTok (demande latente, visuel), SEO local, partenariats hôtels/conciergeries. |
| `CADRE_LEGAL.md` | **À lire avant de lancer.** Mandat de courtage, assurance RC, dépôt de garantie, responsabilité skipper, TVA, juridiction, statut d'intermédiaire. |
| `BUDGET_KPIS.md` | Budget de lancement 90 jours, CAC cible, taux de conversion, P&L par réservation et mensuel, seuils d'alerte. |
| `PLAN_90_JOURS.md` | Le plan A→Z, semaine par semaine, du choix de la niche jusqu'au scale. |

### 🛥️ Extension « Luxe » — Yachts & Jets privés, ciblage HNWI (couche ultra-technique)

Pour la montée en gamme (superyachts + jets privés, clientèle HNWI), 3 modules d'ingénierie data & growth, orientés développeur (code, schémas, étapes actionnables) :

| Fichier | Module |
|---------|--------|
| `LUXE_MODULE_1_SCRAPING.md` | **Scraping & mapping data** : sources yachts/jets, hiérarchie API→feed→JSON-LD→CSS, anti-bot gradué, empty legs temps réel, schéma JSON canonique + DDL PostgreSQL + Airtable, code Playwright/curl_cffi/Scrapy. |
| `LUXE_MODULE_2_LEADGEN.md` | **Lead gen outbound** : ciblage *indirect* des apporteurs (conciergeries, family offices, gestionnaires de patrimoine, event planners, immobilier de prestige), pipeline Sales Nav→enrichissement→séquenceur, 2 scripts cold email (marque blanche), conformité RGPD/ePrivacy. |
| `LUXE_MODULE_3_SEO.md` | **SEO ultra-intent** : 20 mots-clés long-tail transactionnels, cocon sémantique jets+yachts (pSEO routes/modèles/événements), template HTML on-page optimisé CRO + JSON-LD. |

> ⚠️ Ces modules touchent **scraping (ToS/IP-ban)**, **données personnelles (RGPD)** et **cold email (ePrivacy)**. Chaque fichier contient sa boîte de garde-fous légaux — à lire, ce ne sont pas des options.

## 🚀 Plan d'action 90 jours (résumé — détail dans `PLAN_90_JOURS.md`)

| Phase | Jours | Objectif | Livrable |
|-------|-------|----------|----------|
| **0. Demande + cadrage** | J0–J10 | **Étudier la demande internet** (`DEMANDE_MARCHE.md`), choisir LA zone (1 seul port pour commencer), valider le modèle de marge, cadre légal. | Rapport de demande, niche + modèle figés, mandat-type rédigé. |
| **1. Offre** | J10–J30 | Signer 5–10 bateaux sous mandat (tarif net), avant même le marketing. **Pas de site sans bateaux.** | 5–10 fiches yacht réelles, photos/vidéos. |
| **2. Site + contenu** | J20–J40 | Site réservation en ligne + 15 vidéos carrées Canva + acompte en ligne. | Site live, paiement testé, 15 vidéos. |
| **3. Lancement test** | J40–J60 | Google Ads + Meta sur 1 zone, budget contenu, premières réservations. | Premières ventes, premier rapport. |
| **4. Optimisation/scale** | J60–J90 | Couper ce qui ne convertit pas, doubler les gagnants, ajouter bateaux & 2e zone. | Pipeline récurrent, 2e port en préparation. |

## 💡 Conseils business honnêtes

- **Le goulot n'est PAS la demande, c'est l'offre.** Tout le monde croit que le dur c'est de trouver des clients. Faux : en zone touristique l'été, la demande de location de bateau existe déjà. Le dur, c'est d'avoir des **bateaux disponibles, bien tarifés, sous contrat fiable** quand le client veut réserver. Commence par signer les bateaux. Un site magnifique sans stock dispo = remboursements et avis 1 étoile.
- **La saisonnalité va te tuer si tu ne la budgètes pas.** En Méditerranée, **70–80 % du chiffre se fait de mai à septembre**, et ~50 % sur juillet-août seuls. Tu paies les frais fixes 12 mois, tu encaisses sur 4. Calibre la trésorerie pour passer l'hiver. Diversifie (Caraïbes l'hiver, événementiel, vente) si tu veux du récurrent.
- **Un avis négatif coûte une saison.** Le nautisme est un marché de réputation et de bouche-à-oreille. Un moteur en panne, un skipper en retard, un dépôt de garantie mal géré = avis Google/Tripadvisor dévastateur. La **qualité opérationnelle** prime sur le volume au début.
- **« Faire plusieurs sites » : non, pas tout de suite.** Un seul site, une seule zone, prouvé et rentable, AVANT de dupliquer. Multiplier les sites avant d'avoir un modèle qui tourne = multiplier un truc qui ne marche pas.
- **La vidéo carrée Canva est un excellent levier** (coût quasi nul, format parfait Reels/TikTok/pub Meta) **mais ce n'est pas une stratégie, c'est un outil.** Le contenu vend le rêve ; le tunnel de réservation et la dispo réelle convertissent. Ne confonds pas « faire de jolies vidéos » avec « avoir un business ».
- **Acompte en ligne obligatoire dès le départ.** Sinon tu remplis un agenda de réservations fantômes qui ne viennent pas. Un acompte de 30 % filtre les non-sérieux et sécurise ta marge.

## 📞 Ressources clés

- **MYBA (standard de courtage charter)** — https://www.myba-association.com
- **Click&Boat / SamBoat / GetMyBoat** — concurrents ET canaux de distribution potentiels (pour écouler tes mandats au début).
- **Stripe / Mangopay** — encaissement d'acompte + paiement marketplace (split propriétaire/commission).
- **Canva** — production des vidéos carrées (voir `CONTENU_VIDEO_CANVA.md`).
- **Réglementation transport de passagers** (selon pays/pavillon) — déterminante pour le day-charter avec skipper. Voir `CADRE_LEGAL.md`.
