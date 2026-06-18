# Génération de leads & call center 2e / 3e pilier — Suisse romande

> ⚠️ **Note** : Ce dossier contient des documents business sans rapport avec le plugin Toprank. Conservé en branche, ne touche ni `VERSION` ni `CHANGELOG.md`. Peut être exporté (PDF, Drive) sans impact sur le plugin.

> 📍 **Périmètre** : le nom du dossier (`leads-pilier-geneve`) est historique. La cible visée est désormais **toute la Suisse romande** (GE, VD, Valais, Fribourg, Neuchâtel, Jura), via des **RDV en visio**. Les fichiers marketing (`GOOGLE_ADS_PLAN.md`, `META_ADS_PLAN.md`, `SEO_CONTENU.md`, `PARTENARIATS.md`) restent **calibrés Genève** et devront être répliqués canton par canton avant d'y lancer du paid — voir la note en bas de page. La **couche call center** (6 fichiers `CALL_CENTER_*` / `SCRIPTS_*` / `QUALIFICATION_*` / `CONFORMITE_APPELS` / `KPIS_CALL_CENTER` / `SOLUTIONS_IA_REMOTE`) couvre, elle, **toute la Romandie en visio** dès maintenant.

## Hypothèse de travail

**Cible primaire :** particuliers résidant à Genève (ou frontaliers travaillant à Genève), 35–55 ans, avec **≥100 000 CHF d'avoirs prévoyance cumulés** :

- LPP (2e pilier) actif chez l'employeur courant, ou
- compte de libre passage (suite à un changement d'employeur, départ à l'étranger, indépendance), ou
- 3e pilier 3a accumulé (banque ou assurance).

**Offre :** conseil personnalisé pour optimiser ces avoirs — retrait anticipé pour résidence principale, rachats LPP fiscalement déductibles, transfert vers fondation de libre passage performante, ouverture / consolidation 3a, planification retraite, optimisation fiscale annuelle.

**Si l'hypothèse est fausse** (le "100000" voulait dire budget acquisition, volume de leads, ou autre), tout le dossier doit être recalibré — la cible change tout : keywords, créatifs, prix, partenaires.

## 📂 Contenu du dossier

| Fichier | Usage |
|---------|-------|
| `CIBLE_PERSONA.md` | Trois personas types + tableau d'éligibilité par produit + déclencheurs d'achat. |
| `GOOGLE_ADS_PLAN.md` | Structure de campagnes par intention, mots-clés avec CPC estimés, ad copies, négatifs, structure landing pages. |
| `META_ADS_PLAN.md` | Audiences Meta, angles créatifs, structure du lead form, plan de qualification téléphonique. |
| `SEO_CONTENU.md` | Plan SEO local 12 mois : pages piliers, articles, schémas, GMB. |
| `PARTENARIATS.md` | Apporteurs d'affaires : fiduciaires, courtiers immobiliers, RH PME, banques privées. Commissions, mode de rétribution. |
| `CADRE_LEGAL_LPD.md` | Conformité nLPD, FINMA, LSFin, démarchage téléphonique. Ce qu'on peut faire, ce qui est interdit. À lire avant de lancer quoi que ce soit. |
| `BUDGET_ET_KPIS.md` | Allocation budget 90 jours par canal, CPL/CPA cibles, taux de conversion attendus, payback period, modèle de P&L lead → client. |
| **`CALL_CENTER_PRESTATAIRE.md`** | **[Call center]** Modèle opérationnel avec prestataire externalisé romand : flux lead → RDV, sélection/brief/contrat du prestataire, SLA, tarification, sous-traitance nLPD, capacité GE + Lausanne. |
| **`SCRIPTS_APPELS.md`** | **[Call center]** Scripts d'appel complets par cas d'usage (libre passage sans emploi, rachat LPP, 3a, EPL logement, société), objections, prise de RDV, anti-no-show, disqualification polie. |
| **`QUALIFICATION_ET_RDV.md`** | **[Call center]** Définition contractuelle du « RDV qualifié », grille de scoring, critères de rejet/remplacement, fiche de handoff prestataire → conseiller. |
| **`CONFORMITE_APPELS.md`** | **[Call center]** Conformité spécifique aux appels : interdiction du démarchage à froid, preuve d'opt-in, consentement enregistrement, devoirs LSFin, sous-traitance nLPD, formulations interdites. |
| **`KPIS_CALL_CENTER.md`** | **[Call center]** KPIs du centre d'appels, scorecard prestataire, monitoring qualité, rémunération et garde-fous anti-RDV-poubelle, seuils d'alerte. |
| **`SOLUTIONS_IA_REMOTE.md`** | **[Call center]** Modèle apporteur (RDV qualifiés → courtiers, commission), exécution **en remote avec agents IA** : stack concrète, où mettre l'IA vs l'humain, décodage/sécurisation de la commission (1,1 % 2e pilier), conformité IA, RDV visio, garde-fou Lombard Odier. |
| **`MODELE_FICHE_RDV.md`** | **[Call center]** Dossier de RDV qualifié **prêt à remplir** (1 par prospect) : modèle vierge + exemple, champs en questions de formulaire Calendly/CRM, checklist avant transmission au conseiller SwissKap. |
| **`rdv/`** | **[Call center]** Dossier des **RDV pris** : `registre-rdv.csv` (1 ligne/RDV, automatisable) + fiches `*.rdv` (email, préférence 2e/3e pilier, travail, adresse, opt-in…). Exemples fictifs — les vraies données restent dans le CRM privé. |

## 🚀 Plan d'action 90 jours

| Jour | Action | Livrable |
|------|--------|----------|
| J0–J7 | Cadrage : valider persona, offre, conformité (`CADRE_LEGAL_LPD.md`), tracking GA4 + conversions hors-ligne. | Document de cadrage signé. |
| J7–J21 | Production : landing pages par intention (4), ad copies Google + Meta, lead form, séquence email de relance, script de qualification. | LPs en ligne, copies prêtes, formulaire publié. |
| J7–J21 | **Stand-up call center** : sélection du prestataire romand (`CALL_CENTER_PRESTATAIRE.md`), brief + scripts (`SCRIPTS_APPELS.md`), définition du RDV qualifié et fiche handoff (`QUALIFICATION_ET_RDV.md`), DPA + consentement enregistrement (`CONFORMITE_APPELS.md`). | Prestataire signé, scripts certifiés, routage CRM → prestataire actif. |
| J21–J30 | Lancement test : Google Ads 5k CHF, Meta 2k CHF, A/B 2 LPs par intention ; **premiers rappels prestataire + suivi KPIs** (`KPIS_CALL_CENTER.md`). | Premiers leads, premiers RDV qualifiés, premier rapport. |
| J30–J60 | Optimisation : pause des mots-clés/audiences qui dépassent CPL cible, scale sur les vainqueurs, ouverture SEO + partenariats. | CPA stabilisé, premiers RDV signés. |
| J60–J90 | Scale : tripler le budget sur les canaux rentables, sortir une campagne saisonnière (fin d'année 3a), activer 2–3 partenariats apporteurs. | Pipeline mensuel récurrent. |

## 💡 Conseils business honnêtes

- **Le vertical prévoyance est saturé en haut du funnel.** Tout le monde fait du Google Ads sur "3e pilier comparaison". La différenciation ne se joue pas sur le CPC mais sur la **qualification du lead** et la **vitesse de rappel** (sous 5 minutes en heures ouvrées, sinon le taux de conversion s'effondre de 30–40%).
- **Les "comparateurs" (Comparis, Bonus.ch, Moneyland) absorbent énormément de trafic SEO**. Tu ne battras pas leur référencement frontalement — soit tu paies pour être listé chez eux, soit tu vises des angles long-tail qu'ils ne couvrent pas (cas frontaliers, départ à l'étranger, indépendants nouvellement installés à GE).
- **L'optimisation fiscale 3a est saisonnière** : 70% des ouvertures se font entre octobre et décembre. Calibre ton budget en conséquence ; pousse fort en Q4, réduis en Q1.
- **Les frontaliers (~85 000 actifs à Genève en provenance de France voisine)** sont une niche très rentable et peu travaillée — le 2e pilier libre passage à la sortie de Suisse est un cas d'usage à forte commission et faible compétition publicitaire.
- **FINMA + LSFin** : si tu vends des produits d'assurance ou de placement liés (3a assurance, libre passage en titres), tu dois être affilié à un OAR ou avoir une licence. Ne pas confondre avec du simple conseil indépendant. Voir `CADRE_LEGAL_LPD.md`.
- **Le démarchage téléphonique à froid B2C est interdit en Suisse** (art. 3 al. 1 let. u LCD) sauf consentement préalable. Le lead form Meta avec opt-in clair coche cette case. Acheter une liste et appeler ne la coche pas.

## 🗺️ Extension Suisse romande — ce qui est fait et ce qui reste

Honnêteté de périmètre, pour ne pas créer d'illusion de couverture :

- **Couvert pour toute la Romandie** : la couche call center (rappel, qualification, RDV **en visio**, conformité d'appel, KPIs, stack IA remote). En visio, un seul agenda suffit ; on étiquette le canton du prospect dans le CRM. Le prestataire/agent traite GE, VD, VS, FR, NE, JU indistinctement.
- **Encore calibré Genève uniquement** : les plans d'acquisition payante (`GOOGLE_ADS_PLAN.md`, `META_ADS_PLAN.md`), le SEO local (`SEO_CONTENU.md`) et la liste de partenaires (`PARTENARIATS.md`). Avant de pousser du budget hors GE, il faut :
  - dupliquer le ciblage géo par bassin (Lausanne + agglo, Sion/Valais, Fribourg, Neuchâtel),
  - adapter les **spécificités fiscales cantonales** (barème de l'impôt cantonal pour la déductibilité des rachats LPP et du 3a — le mécanisme fédéral IFD est identique, l'impôt cantonal diffère selon le canton),
  - refaire la liste partenaires par canton (fiduciaires, régies, RH PME locales).
- **Cas frontalier surtout genevois** : la niche frontalière (forte à GE) est marginale ailleurs en Romandie — ne pas copier-coller l'angle « frontalier » sur VD/VS/FR/NE.

## 📞 Ressources clés

- **FINMA** — https://www.finma.ch
- **OFAS (prévoyance fédérale)** — https://www.bsv.admin.ch
- **Administration fiscale cantonale GE** — https://www.ge.ch/impots
- **Plafonds 3a année courante** — https://www.ahv-iv.ch (chercher "montants 3a")
- **Préposé fédéral à la protection des données (PFPDT)** — https://www.edoeb.admin.ch
- **Comparis (concurrent + canal partenaire potentiel)** — https://www.comparis.ch
