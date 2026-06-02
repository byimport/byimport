# Agents — Systeme leads 2e/3e pilier Geneve

> Trois agents conversationnels qui pilotent ensemble la generation de **20 RDV qualifies dans le canton de Geneve**. Compatibles format sous-agent Claude Code. Lisent les .md du dossier `business/leads-pilier-geneve/` comme source de verite — ne dupliquent pas la logique, ne la dérivent pas, ne l'oublient pas.

## Les trois agents

| Agent | Mission | Quand l'invoquer |
|---|---|---|
| **`lead-pilier-orchestrator`** | Point d'entree. Tient le compteur 20 RDV, route les questions, produit les digests transverses. | "Ou en sommes-nous ?", "etat des leads", "qui rappeler ?", "alerte conformite" |
| **`lead-pilier-marketing`** | Opere Google Ads, Meta Ads, SEO, partenariats. Audit hebdo, RSA copy, briefs SEO, e-mails outreach. | "audite ma semaine Google Ads", "genere RSA pour AdGroup X", "brief SEO article Y", "e-mail outreach fiduciaire" |
| **`lead-pilier-qa-briefing`** | Qualifie chaque lead du CSV, complete les manques, genere la fiche briefing vendeur. | "prepare RDV LP-2026-0003", "score ce lead", "demande Centrale pour ..." |

Chaque agent demarre par lire les fichiers qui le concernent (.md de strategie + CSV de tracking) — pas de mise en cache, pas de duplication. Si le `.md` source change, l'agent absorbe la modification a la session suivante.

## Architecture

```
business/leads-pilier-geneve/
├── README.md, CIBLE_PERSONA.md, GOOGLE_ADS_PLAN.md, ...    Source de verite strategique
├── tableurs/                                                Donnees prospects
│   ├── prospects_orphan_lpp.csv
│   ├── prospects_3a.csv
│   └── TABLEURS_CRM.md
└── agents/                                                  ← VOUS ETES ICI
    ├── README.md
    ├── lead-pilier-orchestrator.md
    ├── lead-pilier-marketing.md
    ├── lead-pilier-qa-briefing.md
    └── templates/
        ├── briefing_client_template.md
        ├── rapport_marketing_hebdo_template.md
        └── email_partenaire_template.md
```

## Trois modes d'utilisation

### Mode 1 — Sous-agents Claude Code (recommande)

Copier les trois fichiers d'agent dans le répertoire des sous-agents Claude Code :

```bash
# User-level (disponible dans toutes les sessions)
mkdir -p ~/.claude/agents
cp business/leads-pilier-geneve/agents/lead-pilier-*.md ~/.claude/agents/

# OU project-level (disponible uniquement dans ce repo)
mkdir -p .claude/agents
cp business/leads-pilier-geneve/agents/lead-pilier-*.md .claude/agents/
```

Dans une session Claude Code, les agents seront detectes automatiquement et invocables :

```
> @lead-pilier-orchestrator ou en sommes-nous des 20 RDV ?
> @lead-pilier-marketing audite ma semaine Google Ads (voici l'export ...)
> @lead-pilier-qa-briefing prepare RDV LP-2026-0003
```

### Mode 2 — Prompt-as-document dans n'importe quel LLM

Ouvrir le fichier d'agent dans Claude.ai / ChatGPT / Mistral, coller le **corps** (apres le frontmatter) comme premier message systeme, puis converser. Les chemins de fichiers sont lus relativement au repo — donc à exécuter idéalement depuis Claude Code, sinon coller manuellement le contenu des .md de strategie.

### Mode 3 — Wrapper Python (extension future, hors scope)

Encapsuler chaque agent dans un script `bin/run_agent.py` qui pipe le prompt + les .md sources vers l'API LLM via `requests`. Permet l'execution sans Claude Code, en cron, ou en CI. A faire seulement si besoin reel — la version interactive suffit pour 20 RDV.

## Boussole : 20 RDV qualifies Geneve

**Definition** (utilisee par l'orchestrateur et le QA/briefing) :
- `consentement_lpd` = "Oui"
- `statut_commercial` IN ("RDV pris", "Mandat signe")
- ET (`canton_residence` = "GE" OR `statut_fiscal` IN ("Frontalier", "Quasi-resident"))
- ET (LPP avoirs >= 50k OR salaire >= 60k selon segment)

**Mathematique de funnel** (depuis `BUDGET_ET_KPIS.md`) :
- Lead brut → RDV qualifie : ~30%
- → **67 leads bruts a generer pour 20 RDV qualifies**
- Budget media estime : **2 400 – 3 500 CHF**
- Fenetre cible : 30 jours pour pic, 90 jours pour palier de croisiere

## Limites assumees

- **Pas d'autonomie** : les agents ne s'invoquent pas eux-memes. C'est un humain qui dit "ou en sommes-nous", "audit Google Ads", "prepare RDV X".
- **Pas de CRM live** : les agents lisent les CSV statiques. Integration HubSpot/Pipedrive = phase 2.
- **Pas de retours automatiques** : les fiches briefing ne se stockent que si l'utilisateur le demande (`mkdir briefings/`).
- **Pas d'auto-publication** : les ads, articles, e-mails outreach sont generes, jamais postes/envoyes par les agents.
- **Pas de validation conformite a la place de l'avocat** : les agents appliquent les regles de `CADRE_LEGAL_LPD.md` mais ne remplacent pas la consultation juridique au lancement.

## Comment etendre

- **Nouveau persona** : ajouter dans `CIBLE_PERSONA.md`, les agents le voient au prochain demarrage.
- **Nouveau canal** (LinkedIn, TikTok, podcast) : ajouter section dans `META_ADS_PLAN.md` ou créer `<CANAL>_PLAN.md` + le référencer dans `lead-pilier-marketing.md` (Setup obligatoire).
- **Nouveau script automatique** : creer `bin/<nom>.py`, l'agent peut le lancer via `Bash`.
- **Nouveau template** : ajouter sous `templates/` et le référencer dans l'agent qui le produit.

## Conformite et donnees personnelles

Les CSV contiennent des donnees sensibles (avoirs financiers, situation fiscale). Les agents :
- Ne **transmettent jamais** ces donnees a un service externe sans consentement explicite.
- Ne **stockent jamais** de copie ailleurs que dans le repo (briefings/ local).
- **Refusent** toute action commerciale sur un lead sans consentement LPD valide.

Pour le detail, voir `business/leads-pilier-geneve/CADRE_LEGAL_LPD.md`.
