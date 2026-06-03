# Solutions — prise de RDV qualifiés en remote avec agents IA (modèle apporteur)

> Répond au cas précisé : vous voulez **fournir des RDV qualifiés à des courtiers** (qui, eux,
> signent les clients) et être **rémunéré à la commission** — indicativement **1,1 % sur le
> 2e pilier**, le **3e pilier en cours de négociation**. Vous préférez travailler **à distance
> avec des agents IA**, plutôt que depuis le bureau physique gratuit qui vous a été proposé.
>
> ⚠️ Toute la conformité de `CONFORMITE_APPELS.md` s'applique **à l'identique** : une voix/chat
> IA ne contacte **que des leads opt-in**. Pas de démarchage à froid, IA ou pas.

## 1. Votre position dans la chaîne

```
VOUS = apporteur d'affaires (génération + qualification + RDV)
   │  livrez un RDV qualifié + fiche handoff (QUALIFICATION_ET_RDV.md)
   ▼
COURTIER(S) = conseil + signature du mandat (responsabilité LSFin)
   │  signe le client (transfert libre passage, rachat LPP, 3a, EPL…)
   ▼
COMMISSION pour vous : ~1,1 % (2e pilier) / 3a à négocier
```

Vous ne conseillez pas, vous ne signez pas → vous **vendez du RDV qualifié**. C'est un modèle
viable **et** plus léger juridiquement que d'être conseiller (mais pas exempt : voir §6).

## 2. Décoder la commission « 1,1 % » — et la sécuriser

« 1,1 % » ne veut rien dire tant qu'on n'a pas fixé **la base** et **le déclencheur**. À
verrouiller **par écrit** avant de produire le moindre RDV :

| Question | À clarifier | Pourquoi ça change tout |
|----------|-------------|-------------------------|
| **Base de calcul** | 1,1 % de **quoi** ? Du **capital de 2e pilier transféré** ? De la prime ? | 1,1 % de 100 000 CHF transférés = **1 100 CHF**. 1,1 % d'une prime annuelle de 3 000 CHF = 33 CHF. Énorme écart. |
| **Déclencheur de paiement** | À la **signature** ? Au **transfert effectif des fonds** ? | Payer à la signature = risque de reprise si le client annule. |
| **Clawback** | Remboursez-vous si le client se rétracte / le transfert capote ? | Standard dans l'assurance/prévoyance. À cadrer. |
| **3e pilier** | % de la prime ? forfait par contrat ? | Le 3a se commissionne souvent **sur la prime** (parfois plusieurs primes annuelles). Demander un **forfait/contrat** ou un % clair. |
| **Convention écrite** | Convention apporteur signée | Sans écrit, vous n'avez aucun recours sur vos commissions. |

**Ordre de grandeur réaliste (à valider) :** si « 1,1 % du capital de libre passage
transféré » et un panier moyen de **150 000 CHF**, c'est **~1 650 CHF par signature**. Avec un
taux RDV honoré → signature de ~30 %, **un RDV qualifié vaut ~500 CHF** en espérance. C'est
très bon — **à condition** que le coût d'acquisition + outils IA reste loin en dessous (voir
`BUDGET_ET_KPIS.md`).

> 🔎 **Honnêteté :** demandez au courtier des **chiffres réels** (panier moyen, taux de
> signature sur leurs RDV historiques) avant de vous engager. Une commission alléchante sur un
> taux de signature de 10 % vaut moins qu'une commission modeste à 35 %.

## 3. Bureau gratuit vs remote — le vrai arbitrage

La société de Genève qui vous propose une **place de bureau gratuite** est **SwissKap**
(Le Lignon, GE — services frontaliers/résidents, prévoyance/2e pilier via `mon2ekap.ch`,
investissement, création de société : profil cohérent avec vos cas d'usage). Arbitrage honnête :

| | Bureau gratuit chez le courtier | Remote + agents IA (votre préférence) |
|---|---|---|
| Démarrage | Immédiat, flux de deals chaud, formation sur place | À monter (stack IA, process) |
| Indépendance | ❌ lié à **un** courtier, leurs produits, leur cadence | ✅ vous pouvez alimenter **plusieurs** courtiers, mieux négocier |
| Scalabilité | Limitée à votre présence | ✅ l'IA tourne 24/7, capacité élastique |
| Coût | 0 loyer mais « coût caché » de dépendance | Coût outils (~quelques centaines CHF/mois) |
| Conformité | Portée par le courtier | ✅ **votre** responsabilité (sous-traitants IA) |

**Recommandation :** le remote IA est le bon choix **stratégique** (indépendance + scale), mais
ne crachez pas sur l'offre de bureau : utilisez-la comme **rampe de lancement** (apprendre les
produits, voir comment ils signent, obtenir vos premières commissions) pendant que vous montez
votre machine remote en parallèle. Ne signez pas d'exclusivité qui vous enchaîne.

> ✅ **Due diligence SwissKap — à faire AVANT de produire le moindre RDV :**
> 1. **Vérifier l'enregistrement** au registre FINMA des intermédiaires d'assurance
>    (https://www.finma.ch/en/authorisation/insurance-intermediaries/registersuche/) et/ou au
>    registre des conseillers LSFin ; vérifier l'absence de signalement sur la liste de mise en
>    garde FINMA. Le pied de page de leur site mentionne « Art. 45 LSA » → territoire
>    d'intermédiaire en assurance. Un apporteur qui alimente un courtier non enregistré s'expose.
> 2. **Commission 1,1 % (2e pilier)** : faire préciser par écrit la **base** (1,1 % du capital
>    de libre passage transféré ?), le **déclencheur** (signature / transfert effectif) et le
>    **clawback**. Si la prévoyance passe par de l'assurance-vie liée, les reprises de commission
>    en cas de résiliation précoce sont la norme — l'anticiper dans la convention.
> 3. **3e pilier** : obtenir un % de prime clair ou un forfait par contrat (négociation en cours).
> 4. **Pas d'exclusivité** qui vous empêche d'alimenter d'autres courtiers.

## 4. Stack remote « agents IA » — architecture concrète

```
ACQUISITION (opt-in)          QUALIFICATION IA            BOOKING            HANDOFF
Meta/Google lead forms  ─►   IA conversationnelle   ─►   Agenda en ligne ─► Fiche → courtier
Landing pages                (chat WhatsApp / web,        (créneaux GE/VD     (QUALIFICATION_
WhatsApp / SEO               ou voix IA sur rappel)        ou visio)           ET_RDV.md)
        │                            │                          │                  │
        └──────────── CRM central (tout est loggué, opt-in conservé) ─────────────┘
                          │
              Automatisation (Make / n8n) : routage, SMS rappel, relances, scoring
```

**Briques et options (toutes à tester en français — la qualité FR varie) :**

| Brique | Options | Notes |
|--------|---------|-------|
| **CRM tout-en-un** | GoHighLevel (pensé pour ce cas : CRM + funnels + IA conversation + SMS), HubSpot, Pipedrive | GHL séduit les apporteurs solo : beaucoup de briques intégrées. |
| **IA conversationnelle (chat/WhatsApp)** | GHL Conversation AI, chatbot WhatsApp Business API, Voiceflow | Qualifie par écrit avant l'appel humain → gain de temps énorme. |
| **Agent vocal IA (rappels/qualif)** | Vapi, Retell AI, Bland AI, Synthflow, PolyAI | ⚠️ tester la **voix française suisse** ; déclarer l'IA ; opt-in only. |
| **Prise de RDV** | Cal.com (open-source, hébergeable UE), Calendly | Routage GE/Lausanne/visio, buffers, rappels intégrés. |
| **SMS / rappels** | Twilio, MessageBird | Confirmations + rappel J-1 (anti-no-show). |
| **Orchestration** | Make (Integromat), n8n (auto-hébergeable), Zapier | Colle le tout : lead → scoring → routage → relance. |

> 🔌 **Note outils** : cet espace de travail a déjà des connecteurs **Calendly** et **Make**
> branchés (entre autres). Si vous voulez, je peux les utiliser pour **prototyper** le booking
> et une automatisation de relance — dites-le-moi (il faudra autoriser/connecter les comptes).

## 5. Où mettre l'IA — et où garder l'humain

Sur ce vertical, **« l'humain conclut »** (cf. `BUDGET_ET_KPIS.md`). L'IA doit **accélérer**, pas
remplacer le moment de confiance. Répartition recommandée pour démarrer :

- ✅ **IA fait très bien** : réponse instantanée (speed-to-lead), pré-qualification par chat
  WhatsApp/web, propositions de créneaux, confirmations + rappels J-1, relance des injoignables,
  nurturing des leads froids, scoring auto, remplissage de la fiche handoff.
- 🤝 **Humain (vous) garde** au début : **l'appel de qualification final** et le ton sur les cas
  sensibles (personnes sans emploi). Vous pouvez passer à la **voix IA** ensuite, sur les leads
  opt-in à plus faible enjeu, une fois la qualité FR validée et la conformité réglée.
- ❌ **Jamais l'IA (ni vous)** : conseiller un produit, citer un rendement, promettre un
  déblocage de 2e pilier. C'est le courtier, en RDV (`SCRIPTS_APPELS.md` §9).

**Phasage pragmatique :**
1. **Semaine 1–2** : CRM + booking (Cal.com/Calendly) + opt-in propre + SMS rappels. Vous
   qualifiez à la voix. → premiers RDV, premières commissions.
2. **Semaine 3–4** : IA chat WhatsApp/web qui pré-qualifie et propose les créneaux + relances
   auto (Make). → vous ne traitez plus que des leads pré-mâchés.
3. **Mois 2+** : test agent **vocal IA** sur rappels opt-in (déclaré, enregistré, conforme) si
   la valeur le justifie. Mesurer connect→RDV vs votre voix avant de basculer.

## 6. Conformité — points spécifiques à ce modèle (lire `CONFORMITE_APPELS.md`)

- **Opt-in only**, IA comprise. Une IA qui appelle un non-consentant = démarchage à froid illégal.
- **Transparence IA** : ne pas faire passer un agent IA pour un humain ; annoncer l'enregistrement.
- **Sous-traitants IA souvent aux US** (Vapi, Retell, Bland, GHL…) → transfert de données hors
  CH/UE : **DPA + clauses + mention** dans la politique de confidentialité. Préférer quand
  possible des briques hébergeables en UE (Cal.com, n8n auto-hébergé).
- **Statut apporteur & commission** : faites **valider votre statut par un avocat** (apporteur
  de RDV vs intermédiaire LSFin/LSA selon ce que vous faites réellement) et la **transparence de
  la rétribution** vis-à-vis du client final. C'est le point le plus important à sécuriser avant
  d'encaisser (`CONFORMITE_APPELS.md` §5).
- **Convention apporteur écrite** avec chaque courtier (base de commission, déclencheur,
  clawback, exclusivité ou non).

## 7. Prochaines étapes concrètes

1. **Verrouiller la commission par écrit** avec le(s) courtier(s) — base, déclencheur, clawback,
   3a (§2). Demander leurs taux de signature réels.
2. **Décider bureau vs remote** (§3) — recommandation : rampe de lancement au bureau, machine
   remote en parallèle, pas d'exclusivité piégeuse.
3. **Faire valider le statut apporteur** par un avocat (½ journée) — §6.
4. **Monter le socle minimal** : CRM + opt-in + Cal.com/Calendly + SMS rappels → vous qualifiez
   à la voix. Premiers RDV en jours, pas en mois.
5. **Ajouter l'IA par couches** (chat → relances → voix) en mesurant à chaque étape (§5).
6. (Optionnel) **Me dire** si je prototype le booking + une automatisation de relance avec les
   connecteurs Calendly/Make déjà disponibles ici, et **le nom exact de la société** de votre
   contact pour cadrer l'offre de bureau.
