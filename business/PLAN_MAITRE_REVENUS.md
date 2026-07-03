# Plan maître — Premiers revenus (portefeuille complet)

> ⚠️ **Note** : document business, sans rapport avec le plugin Toprank. Conservé en branche,
> ne touche ni `VERSION` ni `CHANGELOG.md`. Rédigé le 2 juillet 2026.

Ce document est le **plan de pilotage unique** des 5 projets du dépôt. Chaque projet a déjà
son dossier détaillé ; ici on répond à trois questions seulement :

1. **Dans quel ordre** attaquer les projets pour encaisser le premier franc/euro/dollar le plus vite ?
2. **Qu'est-ce qui est déjà terminé**, et que reste-t-il à faire, projet par projet ?
3. **Qu'est-ce que seul toi peux débloquer** (argent, identité légale, comptes) ?

---

## 1. État des lieux vérifié (2 juillet 2026)

| Projet | Dossier | État réel | Premier revenu possible |
|---|---|---|---|
| **Leads 2e/3e pilier Genève** | `business/leads-pilier-geneve/` | Plans complets (personas, Google Ads, Meta, SEO, légal, budget). **Rien n'est en ligne.** | **3–6 semaines** après lancement |
| **MonQR (app QR sociale)** | `qr-social-app/` | **MVP fonctionnel et testé** (21 vérifications ✅). Aucune monétisation, pas hébergé. | **2–3 semaines** (petits montants) |
| **Yachts — location/vente** | `business/yacht-location-marketplace/` | Plans complets + pipeline luxe exécutable (13 tests ✅). Aucun mandat signé, pas de site. | **4–8 semaines** en version allégée (voir §3.3) |
| **Huile d'olive Tunisie → Chine** | `business/huile-olive-tunisie-chine/` | Dossier commercial complet (plaquette, marges, financement, 16 importateurs ciblés). Aucune démarche lancée. | **3–6 mois** (cycle incompressible) |
| **Toprank / NotFair (plugin)** | racine du dépôt | **Livré** (v0.23.0, marketplace + MCP). Le canal d'acquisition existe ; le revenu passe par notfair.co. | Continu — dépend de la distribution |

**Constat honnête** : quatre projets sur cinq sont au stade « plans excellents, exécution zéro ».
Le risque n°1 du portefeuille n'est pas la qualité des plans — c'est la **dispersion**. Un seul
opérateur ne peut pas lancer 5 business en même temps. Ce plan impose donc un ordre.

---

## 2. Priorisation — matrice honnête

Critères : délai jusqu'au premier encaissement, capital requis, dépendance à des tiers
(licences, enregistrements), et saisonnalité au 2 juillet.

| Rang | Projet | Délai 1er cash | Capital requis | Blocage tiers | Pourquoi ce rang |
|---|---|---|---|---|---|
| **1** | Leads Genève | 3–6 sem. | 7–10 kCHF (budget test, pas les 46 kCHF du plan complet) | Conformité LSFin/OAR **ou** modèle revente de leads (sans licence) | Meilleur ratio cash/délai. La demande existe, les plans média sont prêts, il ne manque que les landing pages et le budget. |
| **2** | Yachts (version allégée) | 4–8 sem. | < 2 kEUR | Mandats propriétaires | **Nous sommes en pleine saison** (juillet = ~25 % du CA annuel méditerranéen). Trop tard pour un site complet, pas trop tard pour encaisser des commissions via les plateformes existantes. Version complète → saison 2027. |
| **3** | Huile d'olive | 3–6 mois | 65–120 k$ par conteneur (ou 0 si modèle commissionnaire) | **GACC obligatoire** — cause n°1 de blocage douane | Marge par affaire la plus grosse (26–47 k$/conteneur) mais cycle long. On lance les démarches administratives **maintenant, en parallèle**, précisément parce qu'elles durent des mois. |
| **4** | MonQR | 2–3 sem. | ~10 €/mois (hébergement) — encaissement via PayPal existant | Aucun | Revenu vite encaissable mais **plafond bas** (marché saturé par Linktree). À traiter comme un produit d'appoint : 2 jours de travail pour le mettre en ligne avec un paiement, puis on n'y touche plus. |
| **5** | Toprank/NotFair | continu | 0 (déjà construit) | — | C'est l'actif le plus abouti. Le levier revenu n'est pas du développement mais de la **distribution** (registres MCP, contenu, upgrade des installés). Effort marketing récurrent, pas un sprint. |

**Décision recommandée** : concentrer 80 % de l'énergie sur **Genève (rang 1)** et **Yachts allégé
(rang 2)**, lancer les démarches longues de l'huile d'olive en tâche de fond, expédier MonQR en
2 jours, et caler 2 h/semaine de distribution NotFair. Ne rien lancer d'autre avant le premier
encaissement Genève.

---

## 3. Plans d'exécution par projet — de « terminé » à « encaissé »

### 3.1 Leads 2e/3e pilier Genève — le moteur de cash principal

**Ce qui est terminé** : personas, plans Google Ads + Meta complets (mots-clés, copies, lead
form), plan SEO 12 mois, cadre légal nLPD/LSFin, budget et KPIs (CPL cible ≤ 100 CHF payback
année 1, alerte à 150).

**Décision préalable obligatoire — choisir le modèle de revenu (semaine 1) :**

- **Modèle A — Conseiller** : tu vends le conseil toi-même. Exige affiliation OAR / conformité
  LSFin si produits liés (voir `CADRE_LEGAL_LPD.md`). Revenu/client élevé (commissions rachats
  LPP, 3a), mais démarrage plus lent.
- **Modèle B — Revendeur de leads** : tu vends les leads qualifiés 80–150 CHF pièce à 2–3
  cabinets genevois. Pas de licence requise (tu ne conseilles pas), cash immédiat, marge plus
  faible. **Recommandé pour le premier encaissement** — rien n'empêche de basculer vers A ensuite.

**Séquence (déclenchable dès validation du budget) :**

| Sem. | Action | Livrable |
|---|---|---|
| 1 | Choisir modèle A/B. Si B : signer 2 cabinets acheteurs de leads (prix/lead écrit). Créer GA4 + compte Google Ads + Meta Business. | Accords acheteurs, tracking prêt |
| 2 | Monter 2 landing pages (une « frontaliers libre passage », une « rachat LPP déductible » — les 2 angles les moins concurrentiels du plan). Lead form + rappel < 5 min. | LPs en ligne |
| 3 | Lancer Google Ads 3 kCHF + Meta 1,5 kCHF sur ces 2 angles uniquement. | Premiers leads |
| 4–6 | Vendre/traiter les leads, couper ce qui dépasse CPL × 1,5, réinvestir. | **Premier encaissement** |

**Point de vigilance saisonnier** : le gros du 3a se joue oct–déc. Lancer maintenant sur les
angles frontaliers/LPP (non saisonniers), et garder du budget pour pousser fort en Q4.

### 3.2 MonQR — expédier en 2 jours, puis ne plus y toucher

**Ce qui est terminé** : app complète et testée (création carte, QR imprimable, page publique,
avis, likes). **Ce qui manque pour un revenu** : hébergement public + un paiement.

**Plan (2 jours de travail, < 3 h chacun) :**

1. **Jour 1 — mise en ligne** : déployer sur un VPS ou service Node (l'app est sans dépendance,
   `node server.js` suffit) + nom de domaine + sauvegarde du dossier `data/`.
2. **Jour 2 — monétisation minimale** : un seul palier payant « Carte Pro » à **9 € une fois**
   (bouton/lien de paiement **PayPal** — zéro code de checkout, le compte PayPal existe déjà) :
   carte sans marque MonQR + QR haute résolution pour imprimeur + statistiques de scans.
   La version gratuite reste telle quelle et sert d'acquisition.
3. **Distribution passive** : page destinée aux indépendants/commerçants (coiffeurs, restaurants,
   artisans) — « vos avis et réseaux sur le comptoir » ; c'est le seul angle où un QR imprimé bat Linktree.

**Honnêteté** : n'espère pas plus de quelques centaines d'euros/mois sans effort marketing dédié,
et cet effort serait mieux investi dans Genève. L'intérêt est d'avoir un produit qui encaisse
sans maintenance.

### 3.3 Yachts — encaisser CETTE saison en allégé, construire pour 2027

**Ce qui est terminé** : tous les plans (modèle économique, offre, site, contenu, acquisition,
légal, budget, plan 90 jours) + pipeline data/pSEO luxe exécutable et testé.

**Réalité calendaire** : on est le 2 juillet. Le plan 90 jours complet (mandats → site → ads)
livrerait un site fin septembre — **après la saison**. Le lancer maintenant tel quel, c'est payer
des frais fixes 8 mois avant les premiers clients sérieux.

**Plan « saison 2026 allégée » (objectif : premières commissions en 4–8 semaines, < 2 kEUR engagés) :**

1. **Semaines 1–2** : choisir UN port (voir `DEMANDE_MARCHE.md`), signer 3–5 mandats simples à
   tarif net avec skippers/bases locales pour le day-charter d'août (leur creux = nos créneaux).
2. **Semaines 2–3** : publier ces bateaux sur Click&Boat / SamBoat / GetMyBoat (elles apportent
   la demande, on prend l'écart entre tarif net et prix public) + 10 vidéos carrées Canva sur
   Instagram/TikTok local pour capter la demande directe (WhatsApp + acompte 30 % encaissé
   par **facture PayPal** — envoyable directement depuis ces sessions une fois le connecteur
   ré-autorisé, sans site ni intégration).
3. **Août** : opérer, encaisser, collecter les avis 5 étoiles — ils sont le capital de départ de 2027.
4. **Sept–oct (bilan)** : si ≥ 5 réservations rentables → lancer le plan 90 jours complet en
   janvier 2027 pour être en ligne en avril. Sinon → tuer ou pivoter, on n'aura perdu que 2 kEUR.

**Levier chiffre d'affaires — vente à la couchette** : chaque bateau est aussi vendu
**couchette par couchette** (prix par personne, sur-prix unitaire ~30 %) : un bateau complet
rapporte +25–35 % vs la location entière, et capte le segment solos/couples. Modèle, math et
garde-fous légaux : `yacht-location-marketplace/CABIN_CHARTER_COUCHETTES.md` ; outillage
exécutable (49 ports d'Europe, moteur de prix, générateur de pages port avec localisation
et tarifs) : `yacht-location-marketplace/cabin-charter/`.

Les modules luxe (scraping, leadgen HNWI, pSEO) restent au congélateur jusqu'à validation du
modèle de base — c'est de l'outillage de scale, pas de démarrage.

### 3.4 Huile d'olive Tunisie → Chine — lancer le chrono administratif maintenant

**Ce qui est terminé** : plaquette, 3 modèles de proposition, liste fournisseurs (CHO, Mahjoub,
Olivko…), 16 importateurs chinois ciblés, calculs de marge (premium 500 ml : +47 k$/conteneur ;
vrac : +26 k$), 7 solutions de financement.

**Réalité** : cycle de 3–6 mois, et **rien ne passe sans enregistrement GACC**. Chaque semaine de
retard sur les démarches = une semaine de plus avant le premier conteneur. Donc on démarre les
étapes longues tout de suite, mais on n'y consacre que ~1 jour/semaine :

| Mois | Action | Note |
|---|---|---|
| Juillet | Personnaliser la plaquette (société, coordonnées, photos) → PDF. Contacter 3–5 fournisseurs (privilégier ceux **déjà enregistrés GACC** — élimine le blocage n°1). Vérifier leur statut sur ciferquery.singlewindow.cn. | Le financement le plus sûr pour un premier deal : **modèle commissionnaire/agent** (5–8 % du FOB, zéro capital) plutôt que porter 65–120 k$ d'achat. |
| Août | Compte fournisseur Alibaba + Made-in-China (plaquette = fiche produit). Répondre aux RFQ Alibaba (acheteurs déjà en recherche active = cycle le plus court). | Trade Assurance Alibaba règle la question de confiance du premier deal. |
| Sept–oct | Outreach : 30–50 importateurs (liste `IMPORTATEURS_CHINOIS_CIBLE.md` + 21food + RFQ), relance J+5. Envoi d'échantillons aux 3–5 sérieux. | Timing idéal : les acheteurs préparent le Nouvel An chinois (février). |
| Nov–déc | Négociation → premier contrat 30 %/70 %. | Petit premier conteneur = normal, accepter. |

### 3.5 Toprank / NotFair — distribution, pas développement

**Ce qui est terminé** : le produit entier (16 skills + couche OpenClaw, v0.23.0, tests en place,
marketplace `nowork-studio`, fichiers registre MCP prêts).

**Levier revenu** (2 h/semaine, récurrent) : publier les serveurs sur les registres MCP publics
(`server-google-ads.json` / `server-meta-ads.json` sont prêts), un contenu/démo par semaine
(cas d'usage audit Google Ads en 5 min), et s'assurer que le tunnel notfair.co (OAuth → offre
payante) convertit. Le plugin est le produit d'appel gratuit ; chaque installation est un
prospect NotFair.

---

## 4. Ce que seul toi peux débloquer (à faire cette semaine)

Sans ces éléments, aucun plan ci-dessus ne peut s'exécuter — c'est la vraie liste de blocage :

1. **Budget Genève** : valider 7–10 kCHF de budget test (ou décider de réduire/attendre).
2. **Modèle Genève A ou B** : conseiller licencié (OAR/LSFin) ou revendeur de leads ?
3. **Comptes** : **PayPal = solution d'encaissement retenue** (MonQR + acomptes yachts +
   facturation leads). Le compte est connecté à Claude mais l'autorisation a expiré —
   la ré-autoriser dans les paramètres de connecteurs claude.ai pour permettre l'envoi de
   factures et le suivi des paiements directement depuis les sessions. Restent à ouvrir :
   Google Ads + Meta Business (Genève), Alibaba fournisseur (huile d'olive).
4. **Structure légale et facturation** : quelle entité encaisse quoi (CH pour Genève,
   EUR pour yachts/MonQR, USD pour l'huile) — à valider avec ta fiduciaire.
5. **Yachts** : choix du port unique pour l'été 2026.
6. **Huile d'olive** : décision capital — commissionnaire (0 $) ou négociant (65–120 k$/conteneur).

## 5. Tableau de bord — objectifs 90 jours

| Échéance | Jalon | Projet |
|---|---|---|
| Sem. 2 | MonQR en ligne avec paiement | MonQR |
| Sem. 3 | 2 landing pages + campagnes lancées | Genève |
| Sem. 4 | 3–5 mandats signés, bateaux publiés sur plateformes | Yachts |
| Sem. 6 | **Premier encaissement leads** | Genève |
| Sem. 8 | **Premières commissions charter** | Yachts |
| Sem. 8 | Fournisseur GACC confirmé + compte Alibaba actif | Huile d'olive |
| Sem. 12 | CPL Genève stabilisé sous cible ; décision go/no-go site yachts 2027 | Genève, Yachts |
| Mois 5–6 | **Premier contrat conteneur signé** | Huile d'olive |

**Règle de pilotage** : chaque vendredi, 30 minutes — mettre à jour ce tableau, couper ce qui
dépasse ses seuils (définis dans les `BUDGET_*` de chaque dossier), et ne **jamais** démarrer un
nouveau projet tant que le jalon « premier encaissement Genève » n'est pas atteint.
