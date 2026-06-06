# Module 3 — SEO Ultra-Intent (contourner les géants, ranker sur l'intention d'achat)

> **Thèse : ne combats pas les géants (ACS, VistaJet, YachtCharterFleet) sur les têtes de requêtes** (« private jet charter », « yacht charter »). Ils ont 15 ans de domaine et des millions de backlinks. **Attaque la longue traîne transactionnelle** : routes précises, modèles précis, événements datés. Faible volume unitaire, **intention d'achat maximale, concurrence quasi nulle, conversion élevée.**

## 3.1 Les 20 mots-clés Long-Tail High-Intent

> Volume faible mais qualifié. Le panier moyen (10k-500k €) rend rentable une page qui convertit **1 visiteur sur 50**. Vérifie volumes/concurrence dans Keyword Planner/Ahrefs avant prod, mais le pattern prime sur le volume exact.

### Jets — routes transfrontalières & datées (intention « prix/réserver »)
1. `private jet charter Geneva to Nice price`
2. `empty leg flights Paris to Ibiza`
3. `private jet London to Monaco cost`
4. `Citation XLS charter price Côte d'Azur`
5. `private jet to Saint-Tropez summer 2026`
6. `Dubai to Maldives private jet charter price`
7. `last minute private jet Cannes Film Festival`
8. `Gulfstream G650 charter rate per hour Europe`
9. `private jet charter Milan to Olbia (Sardinia)`
10. `empty leg Geneva to London this weekend`

### Yachts — modèles, zones & événements (intention « louer/semaine »)
11. `rent superyacht Monaco Grand Prix 2026`
12. `superyacht charter Cannes Film Festival price`
13. `weekly yacht charter Porto Cervo August`
14. `Sunseeker 88 charter French Riviera price`
15. `catamaran charter Ibiza Formentera with crew`
16. `luxury yacht rental Saint-Tropez weekend`
17. `motor yacht charter Amalfi Coast 12 guests`
18. `superyacht charter Mykonos with jacuzzi`
19. `day charter yacht Antibes to Monaco`
20. `crewed yacht charter Sardinia low season deal`

**Pourquoi ça marche :** chaque requête contient **lieu(x) + (modèle|événement|date) + signal commercial (price/cost/rent/charter)**. C'est le bas du funnel pur. Les géants ratissent le haut ; ils ne créent pas 500 pages « ville A → ville B ».

## 3.2 Architecture en Topic Clusters (cocon sémantique)

Deux cocons, structure pilier → clusters → pages transactionnelles programmatiques.

```
PILIER JETS  /private-jet-charter/
  ├─ Cluster route          /private-jet-charter/routes/
  │    ├─ {from}-to-{to}            ← PAGE PROGRAMMATIQUE (×N routes)
  │    │     ex: /routes/geneva-to-nice/   "...Geneva to Nice price"
  │    └─ /empty-legs/{from}-{to}/  ← alimentée en TEMPS RÉEL par Module 1
  ├─ Cluster appareil       /private-jet-charter/aircraft/{model}/
  │    ex: /aircraft/citation-xls/  "...charter price per hour"
  └─ Cluster destination/événement /private-jet-charter/{destination}/{event}/
       ex: /nice/cannes-film-festival/

PILIER YACHTS  /yacht-charter/
  ├─ Cluster destination    /yacht-charter/{destination}/
  │    ex: /yacht-charter/saint-tropez/
  ├─ Cluster événement      /yacht-charter/{destination}/{event}/  ← FORT
  │    ex: /yacht-charter/monaco/grand-prix/  "rent superyacht Monaco GP"
  ├─ Cluster modèle         /yacht-charter/models/{builder}-{model}/
  │    ex: /models/sunseeker-88/
  └─ Cluster saison/deal    /yacht-charter/{destination}/low-season-deals/
```

**Maillage interne (le moteur du cocon) :**
- Chaque **page transactionnelle** (route/événement/modèle) lie **vers son pilier** (ancre exacte) et **vers 3-5 pages sœurs** pertinentes (mêmes destination/saison).
- Le **pilier** lie vers ses meilleures pages cluster (les plus converties).
- Les pages **empty-legs (Module 1)** lient vers la route équivalente plein tarif (et inversement) → capture l'utilisateur flexible ET le pressé.

**Génération programmatique (pSEO) :**
- Template unique + dataset (routes, modèles, événements, destinations × dates).
- **Garde-fou Google** : pas de pages vides en masse (doorway pages = pénalité). Chaque page DOIT avoir du **contenu unique réel** : prix indicatif réel (← Module 1), temps de vol, appareils dispo, FAQ spécifique. Pas de « {ville} » substitué dans un gabarit creux.

**Données structurées (obligatoire pour ce vertical) :**
- `Service` / `Product` + `Offer` (`priceCurrency`, `price`/`priceRange`).
- `FAQPage` (capte les People-Also-Ask, gagne du SERP réel estate).
- `BreadcrumbList`.
- `AggregateRating` si avis réels (jamais fake — pénalité + risque légal).
- Jets : `Flight` / `Trip` quand pertinent.

## 3.3 Template HTML On-Page optimisé CRO (client pressé & fortuné)

> Principes CRO pour cette cible : **devis/prix immédiat above the fold**, **friction zéro** (1 clic → WhatsApp/appel/quote), **réassurance discrète** (24/7, discrétion, opérateurs certifiés), **0 mur de texte**. Le riche pressé veut un prix et un humain réactif, pas un blog.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Private Jet Charter Geneva to Nice — Price & Availability | {{BRAND}}</title>
  <meta name="description" content="Charter a private jet from Geneva to Nice. Indicative price from €{{PRICE_FROM}}, 55 min flight. Quote in under 2 hours, 24/7. Empty legs available.">
  <link rel="canonical" href="https://{{DOMAIN}}/private-jet-charter/routes/geneva-to-nice/">

  <!-- Données structurées : Service + Offer -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org","@type":"Service",
    "serviceType":"Private jet charter",
    "areaServed":["Geneva","Nice"],
    "provider":{"@type":"Organization","name":"{{BRAND}}","url":"https://{{DOMAIN}}"},
    "offers":{"@type":"Offer","priceCurrency":"EUR","price":"{{PRICE_FROM}}",
              "priceSpecification":{"@type":"PriceSpecification","minPrice":"{{PRICE_FROM}}"}}
  }
  </script>
  <!-- FAQ structurée -->
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":"How much is a private jet from Geneva to Nice?",
     "acceptedAnswer":{"@type":"Answer","text":"From €{{PRICE_FROM}} for a light jet, one way. Final price depends on aircraft and date."}},
    {"@type":"Question","name":"How long is the flight Geneva to Nice by private jet?",
     "acceptedAnswer":{"@type":"Answer","text":"About 55 minutes."}}
  ]}
  </script>
</head>
<body>

<!-- ░░ ABOVE THE FOLD : prix + CTA immédiats ░░ -->
<header class="hero">
  <nav class="trust-bar">
    <span>✓ Quote in &lt; 2h</span><span>✓ 24/7</span><span>✓ Certified operators</span><span>✓ Full discretion</span>
  </nav>
  <h1>Private Jet Charter — Geneva → Nice</h1>
  <p class="subhead">Indicative price from <strong>€{{PRICE_FROM}}</strong> · 55 min flight · light to midsize jets</p>

  <!-- Quote form ultra-court : 4 champs max -->
  <form class="quote" action="/api/quote" method="post" data-route="geneva-nice">
    <input type="date" name="date" required aria-label="Date">
    <input type="number" name="pax" min="1" max="19" placeholder="Passengers" required>
    <input type="tel"   name="phone" placeholder="Phone (for instant callback)" required>
    <button type="submit">Get my price →</button>
  </form>

  <!-- CTA secondaires : friction zéro pour le pressé -->
  <div class="cta-instant">
    <a class="btn-wa" href="https://wa.me/{{WA_NUMBER}}?text=Quote%20Geneva-Nice">WhatsApp now</a>
    <a class="btn-call" href="tel:{{PHONE}}">Call {{PHONE}}</a>
  </div>
</header>

<!-- ░░ Empty legs (live, Module 1) : urgence + deal ░░ -->
<section class="empty-legs" aria-label="Empty legs">
  <h2>Empty legs Geneva ⇄ Nice</h2>
  <ul>{{#EMPTY_LEGS}}<li><b>{{date}}</b> {{aircraft}} · {{pax}} pax · <s>€{{full}}</s> <strong>€{{price}}</strong> (-{{discount}}%) <a href="/book/{{id}}">Reserve</a></li>{{/EMPTY_LEGS}}</ul>
</section>

<!-- ░░ Preuve sociale concise ░░ -->
<section class="proof">
  <blockquote>"Aircraft confirmed in 40 minutes on a Friday in July." — Family office, Geneva</blockquote>
  <div class="logos">{{OPERATOR_BADGES}}</div>
</section>

<!-- ░░ Tableau appareils + prix (contenu unique = anti-doorway) ░░ -->
<section class="aircraft">
  <h2>Aircraft & indicative prices — Geneva to Nice</h2>
  <table>
    <thead><tr><th>Category</th><th>Example</th><th>Pax</th><th>From</th></tr></thead>
    <tbody>
      <tr><td>Light jet</td><td>Citation CJ3</td><td>6</td><td>€{{P_LIGHT}}</td></tr>
      <tr><td>Midsize</td><td>Citation XLS+</td><td>8</td><td>€{{P_MID}}</td></tr>
      <tr><td>Heavy</td><td>Challenger 605</td><td>12</td><td>€{{P_HEAVY}}</td></tr>
    </tbody>
  </table>
</section>

<!-- ░░ FAQ (matche le schema FAQPage) ░░ -->
<section class="faq">
  <h2>FAQ</h2>
  <details open><summary>How much is a private jet Geneva to Nice?</summary><p>From €{{PRICE_FROM}}…</p></details>
  <details><summary>Flight time?</summary><p>~55 minutes.</p></details>
  <details><summary>Last-minute / same-day?</summary><p>Yes, subject to availability — call us.</p></details>
</section>

<!-- ░░ Maillage interne (cocon) ░░ -->
<nav class="related">
  <a href="/private-jet-charter/">← All private jet charters</a>
  <a href="/private-jet-charter/routes/geneva-to-ibiza/">Geneva → Ibiza</a>
  <a href="/private-jet-charter/aircraft/citation-xls/">Citation XLS+</a>
  <a href="/private-jet-charter/empty-legs/geneva-nice/">Empty legs GVA-NCE</a>
</nav>

<!-- ░░ Sticky CTA mobile (toujours visible) ░░ -->
<div class="sticky-cta">
  <a href="https://wa.me/{{WA_NUMBER}}">WhatsApp</a>
  <a href="tel:{{PHONE}}">Call</a>
  <a href="#top">Get price</a>
</div>
</body>
</html>
```

### Règles CRO appliquées dans ce template
| Élément | Raison |
|---|---|
| Prix « from €X » **above the fold** | La cible veut un ordre de grandeur **immédiat**, sinon elle part |
| Form **4 champs** (date, pax, tel) | Chaque champ en plus = -10/20 % de complétion |
| **WhatsApp + Call** en CTA primaires | Le HNWI/assistant **appelle**, il ne remplit pas de long form |
| **Empty legs live** | Urgence réelle + deal = conversion + différenciation vs géants |
| **Sticky CTA mobile** | 60 %+ du trafic mobile ; le contact doit être à 1 pouce en permanence |
| **Tableau prix par appareil** | Contenu **unique** (anti-doorway) + répond à l'intention « price » |
| Trust bar (2h, 24/7, certified, discretion) | Réassurance **sans** pavé de texte |

## 3.4 Performance & E-E-A-T (facteurs de ranking ET de conversion)
- **Core Web Vitals** : LCP < 2,5 s. Hero en HTML/CSS (pas une grosse vidéo bloquante au-dessus). Images WebP, `loading="lazy"` hors écran.
- **E-E-A-T** : page « About/Operators » (certifications AOC, assurances, NDA), auteurs réels, adresse, n° d'enregistrement courtier. Google récompense la légitimité sur YMYL-adjacent (gros montants).
- **Index management** : empty-legs expirées → `noindex` ou 301 vers la route plein tarif (évite le contenu mort indexé).
- **i18n** : `hreflang` en/fr/it/de/ar selon les hubs (Genève=fr/en, Dubaï=en/ar).

## 3.5 Roadmap d'exécution SEO
1. **S1-2** : valider 20-40 patterns de requêtes (volumes/concurrence), figer l'arbo des 2 cocons.
2. **S2-4** : 2 pages piliers + 1 template programmatique + 10 pages cluster « manuelles » de haute valeur (les events : Monaco GP, Cannes, Porto Cervo août).
3. **S4-8** : génération pSEO des routes/modèles **avec données réelles du Module 1** (prix indicatifs, empty legs). Maillage interne automatisé.
4. **S8+** : netlinking ciblé (presse luxe, partenaires apporteurs du Module 2 = backlinks naturels), suivi positions, itération sur les pages qui convertissent.

> 🔌 Les skills **Toprank** du repo accélèrent ce module : `seo:keyword-research` (clusters), `seo:content-planner` (cocon), `seo:seo-page` + `seo:schema-markup-generator` (template + JSON-LD), `seo:geo-optimizer` (i18n/local), connectés à Google Search Console pour le suivi.

## 3.6 Erreurs qui tuent ce module
1. **Attaquer les head terms** (« private jet charter »). → Argent et temps brûlés contre des géants imbattables. Longue traîne uniquement.
2. **pSEO en pages creuses** (gabarit + variable, 0 contenu réel). → **Pénalité doorway pages**. Chaque page = données réelles (prix/appareils/FAQ).
3. **Cacher le prix.** → La cible part. Donne un « from €X » même indicatif.
4. **Form à 10 champs.** → Conversion effondrée. 4 champs + WhatsApp/Call.
5. **Faux avis / faux AggregateRating.** → Pénalité Google + risque légal. Avis réels only.
6. **Empty legs expirées laissées indexées.** → Contenu mort, mauvaise UX, dilution. `noindex`/301 automatique à expiration.
```
