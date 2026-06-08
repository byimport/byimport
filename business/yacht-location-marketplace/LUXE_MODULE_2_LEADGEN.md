# Module 2 — Lead Gen Outbound (ciblage indirect des apporteurs d'affaires HNWI)

> **Thèse stratégique : on ne cible PAS le HNWI directement.** Un milliardaire ne répond pas à un cold email. On cible **ceux qui ont déjà sa confiance et son agenda** — conciergeries, family offices, gestionnaires de patrimoine, event planners VIP, agents immobiliers de prestige. On leur propose une **marque blanche** : ils gardent la relation client, on opère le charter, ils touchent une commission. Acquisition B2B, pas B2C.

## 2.0 Boîte de conformité (lire avant de prospecter)

| Sujet | Règle | Implication concrète |
|---|---|---|
| **ToS LinkedIn** | Scraper via un compte connecté (Phantombuster/PhantomBuster) **viole les ToS** → risque de **ban de compte** | Volumes humains (< 80-100 actions/j/compte), comptes « warm », jamais le compte principal de la boîte |
| **RGPD (contacts UE)** | Base légale = **intérêt légitime B2B** (Art. 6-1-f) possible, mais : finalité documentée, données pro uniquement, **opt-out facile**, registre de traitement | Pas de données sensibles, pas de perso ; e-mail pro nominatif OK en B2B avec opt-out |
| **ePrivacy / cold email** | B2B toléré dans bcp d'États UE avec opt-out clair ; **plus strict** dans certains (DE, AT). US = CAN-SPAM (opt-out + adresse physique) | Toujours : lien de désinscription, identité réelle, pas de sujet trompeur |
| **Enrichissement** | Préfère des fournisseurs **RGPD-compliant** (Dropcontact, Societeinfo) à du scraping perso brut | Traçabilité de la source de chaque email |

➡️ **Architecture « safe » recommandée** : Sales Navigator pour **identifier** → export **manuel/raisonné** des comptes/leads → **enrichissement compliant** (email pro) → séquence cold email **B2B avec opt-out** + connexion LinkedIn légère. Le scraping massif automatisé LinkedIn est l'approche fragile/risquée ; documente-le mais minimise-le.

## 2.1 Ciblage — les 5 segments d'apporteurs & filtres Sales Navigator

| Segment | Pourquoi | Filtres Sales Nav clés |
|---|---|---|
| **Conciergeries de luxe** | Demandes charter régulières de leurs membres | Industry: *Hospitality / Luxury Goods*; Title: *Lifestyle Manager, Concierge, Member Relations*; Keywords: `"luxury concierge" OR "private concierge"` |
| **Family Offices** | Gèrent voyages/actifs des familles UHNWI | Industry: *Financial Services*; Title: *Family Office, Principal, Chief of Staff, Executive Assistant to*; Keywords: `"family office" OR "single family office"` |
| **Gestionnaires de patrimoine / Private Bankers** | Clients HNWI, voyagent | Industry: *Banking, Investment Management*; Title: *Private Banker, Wealth Manager, Relationship Manager*; Seniority: Director+ |
| **Event planners VIP / corporate** | Incentives, séminaires, mariages de prestige | Industry: *Events Services*; Title: *Event Director, Production*; Keywords: `"luxury events" OR "VIP" OR "incentive"` |
| **Agents immobiliers haut de gamme** | Clients qui achètent villa + veulent le yacht | Industry: *Real Estate*; Keywords: `"prime" OR "luxury real estate" OR "sotheby" OR "knight frank"`; Geo: Monaco, Côte d'Azur, Genève, Dubaï, Londres |

**Requêtes booléennes (champ Keywords Sales Nav) — exemples :**
```
("family office" OR "single family office") AND ("chief of staff" OR "principal" OR "executive assistant")
("luxury concierge" OR "private concierge" OR "lifestyle management") NOT (intern OR student)
("private bank" OR "wealth management") AND ("relationship manager" OR "private banker")
```
**Géo prioritaire** (là où les charters se concluent) : Monaco, Nice/Cannes/Antibes, Genève, Londres (Mayfair), Dubaï, Miami, Saint-Tropez, Ibiza, Porto Cervo.

## 2.2 Le pipeline outbound (de l'identification à la réponse)

```
[Sales Navigator]  → recherches sauvegardées par segment × géo
        │  (lead lists)
        ▼
[Extraction raisonnée]  → Phantombuster "Sales Nav Search Export" (volumes humains)
        │                  OU export manuel des comptes prioritaires
        ▼
[Enrichissement email]  → Dropcontact / Hunter / Apollo  (email pro + vérif MX)
        │                  + waterfall : si A échoue → B → C
        ▼
[CRM / séquenceur]      → Instantly / Lemlist / la Growth Machine / HubSpot
        │                  - dédup, blacklist, opt-out global
        ▼
[Séquence multicanal]   → J0 email · J2 visite+connexion LinkedIn · J4 relance · J9 relance valeur · J16 breakup
        ▼
[RDV]                   → Calendly/Cal.com → démo marque blanche → contrat apporteur
```

**Cadence & délivrabilité (cold email) :**
- Domaine d'envoi **dédié** (`go.tamarque.com`, pas le domaine principal), **SPF + DKIM + DMARC** configurés, **warm-up** 2-3 semaines (Instantly/Mailwarm).
- **30-50 emails/j/boîte** max au départ, plusieurs boîtes pour scaler. Plain text, **pas d'images ni de liens trackés agressifs** (tue la délivrabilité).
- 1 seul lien (Calendly) max, opt-out en clair.

## 2.3 Schéma de données — table `partner_lead`

```sql
CREATE TABLE partner_lead (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    segment       TEXT NOT NULL,         -- concierge|family_office|wealth|events|realestate
    full_name     TEXT, first_name TEXT,
    title         TEXT, company TEXT, company_domain TEXT,
    linkedin_url  TEXT,
    email         TEXT, email_status TEXT,      -- valid|risky|unknown
    geo_city      TEXT, geo_country CHAR(2),
    source        TEXT,                         -- salesnav|referral|event
    enrichment_src TEXT,                        -- dropcontact|hunter...
    icp_score     INT,                          -- voir scoring
    consent_basis TEXT DEFAULT 'legitimate_interest_b2b',
    opted_out     BOOLEAN DEFAULT false,
    stage         TEXT DEFAULT 'new',           -- new|contacted|replied|meeting|partner|lost
    last_touch    TIMESTAMPTZ,
    created_at    TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX uq_partner_email ON partner_lead(lower(email)) WHERE email IS NOT NULL;
```

**ICP score (priorisation d'envoi) :**
| Critère | Points |
|---|---|
| Segment family office / conciergerie | +30 |
| Seniority Director+ / Principal / Chief of Staff | +20 |
| Géo hub charter (Monaco, Genève, Dubaï, Londres, Côte d'Azur) | +20 |
| Email pro vérifié (valid) | +15 |
| Société > 10 employés (vraie structure) | +10 |
| Signal récent (post sur voyage/luxe, levée, nouveau rôle) | +15 |
| Email générique (info@) | −20 |

→ Score ≥ 60 : séquence prioritaire + perso poussée. 40-59 : séquence standard. < 40 : nurturing léger / pas d'envoi.

## 2.4 Script Cold Email #1 — Conciergerie de luxe

> Ton : minimaliste, ultra-pro, axé réactivité + marque blanche. Pas d'adjectifs creux. Court.

**Objet :** `Charter jet & yacht — backup réactif pour vos demandes`

```
Bonjour {{first_name}},

Chez {{company}}, vous recevez sûrement des demandes de jet ou de yacht
en dernière minute — souvent quand la dispo se fait rare.

Nous opérons ces charters en marque blanche pour des conciergeries :
vous gardez la relation et votre marque, nous sécurisons l'appareil ou
le bateau et gérons la logistique. Réponse fermée sous 2 h, 7j/7.

Vous touchez une commission sur chaque dossier, sans rien avancer.

15 min cette semaine pour voir si ça vous est utile ?
{{calendly_link}}

{{sender_name}}
{{company_name}} — {{phone}}
Se désinscrire : {{unsub_link}}
```

**Relances :**
- **J+4** : `Un exemple concret` → mini cas (« Nice→Ibiza, appareil confirmé en 90 min un vendredi de juillet »).
- **J+9** : `Le bon réflexe pour août` → angle saisonnalité (la dispo se ferme, ayez un backup).
- **J+16 (breakup)** : `Je referme votre dossier ?` → court, sort proprement.

## 2.5 Script Cold Email #2 — Directeur de Family Office

> Ton encore plus sobre. Le family office déteste qu'on lui « vende ». Angle : déléguer un irritant opérationnel, discrétion, fiabilité.

**Objet :** `Logistique jet/yacht — un interlocuteur unique`

```
Bonjour {{first_name}},

Pour un family office, l'organisation des déplacements privés (jet,
yacht, transferts) est chronophage et rarement votre cœur de métier.

Nous agissons comme interlocuteur unique : sourcing de l'appareil ou
du yacht, négociation, contrats, équipage — vous validez, nous exécutons.
Discrétion totale, facturation consolidée, disponibilité 24/7.

Plusieurs family offices à {{geo_city}} nous délèguent déjà ce poste.

Seriez-vous ouvert à un échange de 15 min ? {{calendly_link}}

{{sender_name}}
{{company_name}}
Se désinscrire : {{unsub_link}}
```

**Relances :**
- **J+5** : `Discrétion & conformité` → rassure sur NDA, KYC, traçabilité des paiements.
- **J+11** : `Empty legs` → angle valeur concrète (accès à des repositionnements -50/-70 % pour les trajets flexibles de la famille). **C'est le pont avec le Module 1** : tes empty legs scrapés deviennent l'accroche.
- **J+18 (breakup)** : sortie propre.

## 2.6 Personnalisation à l'échelle (le « hyper-perso » sans y passer la vie)
- **Variable {{icebreaker}}** générée par LLM à partir d'un signal réel (poste récent, post LinkedIn, ville, type de clientèle). 1 phrase max, vérifiée. Jamais de perso fausse/robotique (pire que pas de perso).
- **Snippets par segment** (douleur spécifique) injectés via le séquenceur.
- **Règle anti-spam** : 1 variable factuelle vérifiable > 5 compliments génériques. Si tu ne peux pas personnaliser vrai, reste générique propre.

## 2.7 KPIs outbound & seuils
| Métrique | Cible saine | Alerte |
|---|---|---|
| Taux d'ouverture | 45-65 % | < 35 % → délivrabilité/objet |
| Taux de réponse | 6-12 % (B2B luxe ciblé) | < 3 % → ciblage/offre |
| Réponses positives | 2-4 % | — |
| RDV bookés / 100 leads | 2-5 | — |
| Bounce rate | < 3 % | > 5 % → enrichissement à revoir (stop l'envoi, ça brûle le domaine) |
| Plaintes spam | < 0,1 % | toute plainte = revoir liste/copy |

## 2.8 Erreurs qui tuent ce module
1. **Cibler le HNWI en direct.** → 0 réponse. Cible les apporteurs.
2. **Envoyer depuis le domaine principal sans warm-up.** → Domaine grillé, emails en spam, réputation détruite.
3. **Scraper LinkedIn agressivement.** → Compte banni, et tu perds l'outil de ciblage. Volumes humains.
4. **Cold email UE sans opt-out ni base légale.** → Risque CNIL. La conformité n'est pas optionnelle.
5. **Fausse personnalisation à l'IA.** → « J'ai adoré votre post » sur un compte sans post = mort instantanée de la crédibilité.
6. **Pas de marque blanche claire dans le pitch.** → L'apporteur a peur que tu lui voles son client. Le White Label lève ce frein n°1.
