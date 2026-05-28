# Toprank — Public AI-Agent Plugin (Claude Code, OpenClaw, Codex, Hermes)

**This is the public, open-source repository that ships to all customers and the community.**

Toprank is a host-agnostic plugin providing SEO, Google Ads, and Meta Ads skills for AI coding agents. It is distributed via the `nowork-studio` Claude Code marketplace and via direct agent install on OpenClaw, Codex, and Hermes. Every change here is user-facing.

## Engineering Execution Standard

**Surgical, verified, minimum-change engineering.** Make the smallest scoped change that solves the real problem, verify it, and do not disturb anything else.

- **Understand before changing.** Inspect the relevant code, current state, and failure mode before editing.
- **State material assumptions.** If ambiguity changes the implementation, risk, or user-visible behavior, clarify before acting.
- **Prefer the smallest correct change.** No speculative features, premature abstractions, or unrelated "while I'm here" refactors.
- **Scope cleanup tightly.** Match existing style. Clean up only mess introduced by the change. Mention unrelated issues; do not silently fix them.
- **Make success verifiable.** For bugs, reproduce when practical. For features, define expected behavior. Run the narrowest meaningful validation, then broader checks if risk warrants.
- **Protect high-risk boundaries.** Before destructive, public, production, billing, credential, or communication side effects: verify actor, target, scope, approval, blast radius, and resulting state.
- **Leave the system easier to operate.** If the workflow recurs or the bug pattern is reusable, encode it as a test, guardrail, skill, or automation.

## Working style: brutal honesty, relentless quality

This code ships to real users. Sycophancy and rubber-stamping cost us credibility every time a bad skill lands in someone's Claude. Hold the line:

- **Be brutally honest.** If a request is a bad idea, say so with reasoning — don't soften it, don't bury it in caveats, don't implement it anyway because the user asked. "This won't work because X" is more useful than a polite attempt that fails in production.
- **Critically think about every request.** Before implementing, challenge the premise: Is this the right problem to solve? Does it match an existing skill? Will it make the plugin better for users, or just bigger? Push back when the answer is no.
- **Relentless about quality.** High quality, reliable, and maintainable — non-negotiable. No half-finished skills, no untested prompts, no "we'll fix it later." If it's not ready to land in a customer's environment, it's not ready to commit.
- **Surface tradeoffs explicitly.** When a request has hidden costs (complexity, maintenance burden, user confusion, prompt fragility), name them before writing code. Let the user make the call with full information.
- **Disagree when warranted.** Agreement is not the goal; the best outcome for users is. If the user is wrong, say so — with evidence.

## Repository purpose

- Home of the `toprank` plugin — the public artifact customers install.
- Contains host-agnostic skills under `google-ads/`, `seo/`, `meta-ads/`, `gemini/`, and `toprank-upgrade-skill/`.
- Contains OpenClaw-specific multi-site orchestrators under `openclaw/skills/` that compose the host-agnostic skills above.
- Registered via `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (Claude Code) and `AGENTS.md` (every other host).
- Paired with the NotFair-GoogleAds and NotFair-MetaAds MCP servers (OAuth at notfair.co) for ad-platform writes, and Google Search Console for SEO reads.

## Critical: this ships to users

- Treat every commit as a release candidate. Broken skills, bad prompts, or missing files become customer bug reports.
- Never add internal-only notes, secrets, credentials, dev scratch files, or references to private infra. This repo is public.
- Test skills end-to-end before shipping — `SKILL.md` frontmatter (`name`, `description`, triggers) is how Claude decides to invoke them; typos or stale descriptions break discovery.

## Agent entry points (single sources of truth)

- **`AGENTS.md`** — the universal skill resolver. Every host reads this to route user intents to the right skill. Update it whenever a skill is added, removed, or its purpose changes.
- **`INSTALL_FOR_AGENTS.md`** — the single paste-URL target that walks an AI agent through host detection and install.
- **`install/README.md`** — convention for adding per-host install adapters (Codex, Hermes, etc.) without duplicating skills.

## Repository layout

```
.
├── .claude-plugin/
│   ├── plugin.json              Claude Code plugin manifest (skills array — must list every shipped skill)
│   └── marketplace.json         Marketplace registry entry for `nowork-studio`
├── .mcp.json                    Registers NotFair-GoogleAds + NotFair-MetaAds as native HTTP MCP servers
├── server-google-ads.json       MCP registry publication metadata for the Google Ads server
├── server-meta-ads.json         MCP registry publication metadata for the Meta Ads server
├── AGENTS.md                    Universal intent → skill resolver (the file every non-Claude host reads)
├── INSTALL_FOR_AGENTS.md        End-to-end install walkthrough for any AI agent
├── README.md / CHANGELOG.md / CONTRIBUTING.md / LICENSE
├── VERSION                      Single source of truth for plugin version
├── google-ads/
│   ├── manage|audit|copy|landing/  Four host-agnostic Google Ads skills
│   └── shared/                  preamble.md, analysis-principles.md, ppc-math.md, policy-registry.json, industry-templates.json
├── meta-ads/
│   ├── manage|audit/            Two host-agnostic Meta Ads skills
│   └── shared/                  preamble.md, meta-math.md, policy-registry.json
├── seo/
│   ├── seo-analysis|seo-page|content-writer|content-planner|keyword-research|
│   │   meta-tags-optimizer|schema-markup-generator|broken-link-checker|
│   │   geo-optimizer|setup-cms/   Ten host-agnostic SEO skills
│   └── shared/                  preamble.md, seo-best-practices.md, business-context.md
├── gemini/                      Cross-model second-opinion skill (Google Gemini)
├── toprank-upgrade-skill/       Self-updater skill (/toprank-upgrade)
├── openclaw/                    OpenClaw adaptive layer — multi-site orchestrators + runtime
│   ├── README.md                Surface description and install guide
│   ├── skills/                  Five orchestrator skills (toprank-site-onboard, toprank-portfolio-review,
│   │                              toprank-weekly-review, toprank-improve-page, toprank-investigate-drop)
│   ├── shared/                  adapter-rules.md, artifact-contract.md, policy.md, recommendation-quality.md, triggers.md
│   ├── bin/                     Python helpers: weekly_review.py, persist_run.py, run_scheduler.py, publish_pending.py, etc.
│   ├── install/                 install.sh, install-openclaw-cron.sh, install-launchd.sh, notfair-publisher.md
│   ├── artifacts/               schemas/, examples/, visuals/ for the runtime JSON contract
│   ├── workspace-template/      Skeleton portfolio.json + schedule.json copied into a fresh workspace
│   └── tests/                   pytest suites for scheduler, publisher, weekly-review scoring
├── install/                     Per-host install adapter convention (README explains; Claude Code needs none)
├── bin/                         Plugin-level helper scripts (preamble.md + four tools, see below)
├── docs/                        Long-form architectural docs (currently: openclaw-adaptive-layer.md)
├── test/                        Top-level test suite (see "Testing" below)
├── business/                    Off-topic business artifacts that are not part of the plugin (see warning below)
├── conftest.py                  pytest root config — makes test/helpers/ importable as helpers.*
├── requirements.txt             Runtime deps (google-auth, google-auth-httplib2, requests, google-genai)
└── requirements-test.txt        Test deps (pytest, pytest-timeout)
```

### About `business/`

The `business/` directory contains business-domain artifacts (e.g., `business/huile-olive-tunisie-chine/`, a Tunisian olive oil export proposal) that are **unrelated to the Toprank plugin**. It is allowed to exist on side branches but must never be referenced from any shipped skill, the plugin manifest, `AGENTS.md`, or the README. If you are modifying the plugin, ignore `business/`. If a user asks for changes inside `business/`, treat it as standalone document work — do not bump `VERSION` or touch `CHANGELOG.md`.

## SKILL.md conventions

Every skill is a directory whose `SKILL.md` is a Markdown file with YAML frontmatter:

```yaml
---
name: skill-name                  # required — becomes /toprank:skill-name
argument-hint: "<short>"          # optional but recommended — what the user types after the slash
description: >                    # required — Claude uses this to decide whether to invoke the skill
  One paragraph stating what the skill does and *every* phrase that should trigger it.
  Lists of phrases in prose work better than terse summaries; if in doubt, broaden the trigger surface.
triggers:                         # optional — explicit phrase list (Google Ads / Meta Ads use this)
  - keyword 1
  - keyword 2
allowed-tools:                    # optional — restrict the skill to a tool subset
  - Bash
  - Read
---
```

After frontmatter, the body is imperative instructions — written in the voice of an expert practitioner — followed by references and procedures the skill should follow.

- **Shared logic lives under `<category>/shared/`** (`preamble.md`, math notes, policy registries). Skills `Read` these at runtime; never inline the logic.
- **Scripts** live under `<skill>/scripts/` and use Python 3.8+ stdlib only, with `requests` allowed. Accept `--output` for file output, write progress to stderr and data to stdout.
- **Reference docs** live under `<skill>/references/` and are loaded lazily — only when the skill needs the depth.

## Runtime state (never commit, never reference from code paths the user shares)

- **Plugin state:** `~/.toprank/` — `config.yaml`, `last-update-check`, `just-upgraded-from`, `update-snoozed`, etc. Override with `TOPRANK_STATE_DIR` for tests.
- **Per-project Google Ads + Meta config:** `.notfair.json` at the project root holds `accountId` (Google Ads) and `metaAccountId` (Meta) — same file, no double-prompting. Per-account data dirs are resolved by `<category>/shared/preamble.md` and persisted under `~/.toprank/ads/<account>/` (or the legacy `.notfair/` data dir if migrated).
- **OpenClaw runtime:** `~/.toprank/openclaw/` (override with `TOPRANK_OPENCLAW_HOME`). Contains `portfolio.json`, `schedule.json`, and per-site state under `sites/<domain>/`. The schema lives at `openclaw/artifacts/schemas/`.
- **Connector placeholders:** SKILLs reference external tools as `~~google-ads`, `~~meta-ads`, `~~search-console`, `~~cms`. The `shared/preamble.md` of each category resolves the placeholder against whichever MCP prefix is connected (`mcp__NotFair-GoogleAds__*`, `mcp__notfair__*`, `mcp__google_ads_mcp__*`, etc.). Do not hardcode a single MCP prefix in skill bodies — go through the preamble.

## Helper scripts in `bin/`

These are plugin-level shell + Python tools, installed alongside the skills:

- `bin/toprank-update-check` — reads remote `VERSION`, returns `UPGRADE_AVAILABLE` / `JUST_UPGRADED` / nothing. Wired into the skill preamble in `bin/preamble.md` and invoked at the top of every skill so users get inline upgrade prompts.
- `bin/toprank-upgrade` flow lives in `toprank-upgrade-skill/SKILL.md` (no separate binary — the skill drives it).
- `bin/toprank-config` — `get | set | list` against `~/.toprank/config.yaml`.
- `bin/toprank-content-calendar` — stdlib-only local HTTP viewer for `content-calendar.json` produced by `/content-planner`.
- `bin/toprank-change-watch` — SessionStart hook that surfaces pending Google Ads change-impact reviews; supports `.ics` export for calendar reminders.

## Testing

Set up once: `pip install -r requirements-test.txt`.

| What | How | When |
|---|---|---|
| Plugin structure | `./test/install.test.sh` | Any change touching `.claude-plugin/`, skill registration, or shared preambles |
| Unit tests for scripts | `pytest test/unit -q` | Any script edit under `seo/*/scripts/`, `google-ads/*/scripts/`, etc. |
| End-to-end skill harness | `pytest test/test_skill_e2e.py test/test_skill_routing_e2e.py -q` | Touching SKILL.md frontmatter, triggers, or shared preambles |
| LLM-judge evals | `pytest test/test_skill_llm_eval.py test/test_ads_skill_llm_eval.py -q` | Substantive prompt edits — these call a real model and are slow |
| OpenClaw layer | `pytest openclaw/tests -q` | Anything under `openclaw/` |
| Whole repo | `pytest -q` from repo root | Before `/ship` |

`conftest.py` at repo root puts `test/helpers/` on `sys.path` so unit tests can import `helpers.eval_store`, `helpers.llm_judge`, etc.

## When adding or modifying a skill

1. Create/edit the skill directory under the appropriate category (`google-ads/`, `seo/`, `meta-ads/`, etc.) with a `SKILL.md` containing valid frontmatter.
2. **Register it in `AGENTS.md`** under the matching intent table. A skill that isn't in `AGENTS.md` is invisible to OpenClaw, Codex, Hermes, and any non-Claude host.
3. **Register it in `.claude-plugin/plugin.json`** under the `skills` array. A skill that exists on disk but isn't listed here will NOT appear in the installed Claude Code plugin — this has already bitten us once with `ads-landing`. (OpenClaw orchestrator skills under `openclaw/skills/` are the only exception: they are explicitly **not** registered in `plugin.json`.)
4. Bump the version in three places so upgrades propagate:
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → both `metadata.version` and `plugins[0].version`
   - `VERSION` file at repo root
5. Update `CHANGELOG.md` with a user-facing note.
6. Verify locally (at minimum: `./test/install.test.sh` and any relevant `pytest test/...`), then ship via `/ship`. Users pick up the new version through `toprank:toprank-upgrade`.

## Versioning

Semantic-ish: bump patch for skill additions / fixes, minor for new categories or meaningful capability jumps, major for breaking skill API changes. Keep `VERSION`, `plugin.json`, and `marketplace.json` in lockstep — drift causes upgrade detection bugs.

The two MCP server registry files (`server-google-ads.json`, `server-meta-ads.json`) version **independently** from the plugin — they track the server's API surface, not the plugin's skill surface. Only bump them when the server side of NotFair publishes a new MCP version that toprank consumes.

## Branding: NotFair

The product is **NotFair**. All user-facing text, documentation, skill descriptions, and config namespaces use NotFair / `notfair.co` / `.notfair/` / `mcp__notfair__*` / `mcp__NotFair-GoogleAds__*` / `mcp__NotFair-MetaAds__*`. The prior brand (AdsAgent) has been fully removed from active code as of v0.23.0 — do not reintroduce any of its strings (names, config paths, MCP prefixes, URI schemes, or domains) in new code, new docs, or rewrites of existing files. CHANGELOG history before v0.23.0 is intentionally preserved verbatim.

## Related repos

- **NotFair MCP server** — private, powers the Google Ads and Meta Ads tool calls the skills depend on. Endpoint contracts live at `notfair.co/api/mcp/google_ads` and `notfair.co/api/mcp/meta_ads`.
- **`openclaw/install/notfair-publisher.md`** — the source-of-truth webhook contract between the opt-in OpenClaw publisher cron job and the NotFair Next.js side. Keep `openclaw/bin/publish_pending.py` and the Next.js handler in lockstep via that doc.
