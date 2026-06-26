# CRM Shared Preamble

Every CRM skill reads this before doing anything else. Handles update checks, MCP connector detection, config resolution, and onboarding so individual skills don't repeat this logic.

The CRM category is **connector-agnostic and read-focused**. Unlike Google Ads and Meta Ads (which are powered by the NotFair MCP servers), there is no "NotFair CRM" server — these skills resolve the `~~crm` placeholder against whichever CRM MCP is connected to the host (HubSpot is the reference implementation). They never shell out to a vendor CLI.

## Step 0: Check for toprank updates

```bash
_UPD_BIN=$(ls ~/.claude/plugins/cache/nowork-studio/toprank/*/bin/toprank-update-check 2>/dev/null | head -1)
[ -n "$_UPD_BIN" ] && _UPD=$("$_UPD_BIN" 2>/dev/null || true) || _UPD=""
[ -n "$_UPD" ] && echo "$_UPD" || true
```

If the output contains `UPGRADE_AVAILABLE <old> <new>`: immediately follow the inline upgrade flow in the `/toprank-upgrade` skill (Step 1 onward) to auto-upgrade. After the upgrade completes, re-read the updated preamble from the new plugin cache and restart from Step 1.

If the output contains `JUST_UPGRADED <old> <new>`: mention "toprank upgraded from v{old} to v{new}" briefly, then continue to Step 1.

If neither: continue to Step 1 silently.

## Step 1: Resolve config

Read config from three locations and merge fields (first non-null, non-empty-string value wins per field):

1. **Project-level** — `.notfair.json` in the repository root
2. **Claude project-level** — `~/.claude/projects/{project-path}/notfair.json`
3. **Global fallback** — `~/.notfair/config.json`

Each file uses the same shared schema already used by the Google Ads (`accountId`) and Meta Ads (`metaAccountId`) skills. The CRM skills do not require a stored account id — the CRM MCP resolves the connected portal/account from its own OAuth session. If a `crmPortal` hint exists in config, surface it in your narration so the user knows which portal they're reading; otherwise rely on the connector's session.

### Resolved data directory

Data files are stored project-locally when a project-level config exists:

- If `.notfair.json` exists in the current working directory → `{data_dir}` = `.notfair/` (relative to project root)
- Otherwise → `{data_dir}` = `~/.notfair/`

CRM-specific artifacts (saved segments, schema snapshots) are namespaced under a `crm/` subdirectory — `{data_dir}/crm/` — so they don't collide with the Google Ads or Meta Ads equivalents. Create the directory only when you actually persist something.

**Important:** If using project-local storage (`.notfair/`), ensure `.notfair.json` and `.notfair/` are in the project's `.gitignore` — they may reference business-sensitive segment definitions that should not be committed.

Continue to Step 2 (connector detection always runs).

## Step 2: CRM connector detection (resolve `~~crm`)

Always verify that a CRM MCP connector is available before reasoning about records — the connector could be down, unauthorized, or simply not installed.

**How to detect:** scan your available tool list for any tool whose name ends in `query_crm_data` **or** `search_crm_objects`. Take everything before that suffix as the detected prefix (`~~crm`). HubSpot's connector is the reference surface; other CRM MCPs that expose the same verbs work too.

The canonical read surface this category depends on:

| Capability | Tool (suffix) | Used by |
|---|---|---|
| Filter / list / count records | `search_crm_objects` | `crm-query` |
| Fetch records by id, inspect data model | `get_crm_objects` | `crm-query` |
| Discover property (field) definitions | `search_properties` | both |
| Resolve owner names ↔ ids | `search_owners` | both |
| Server-side SQL (aggregates, GROUP BY, time series, cross-object) | `query_crm_data` | `crm-reports` |

Writes (`manage_crm_objects` and equivalents) are **out of scope** for this read-and-segment category. If the user asks to create or modify records, say so plainly and route them to the CRM's own write surface (which carries its own confirmation flow) rather than improvising.

If no CRM connector is detected, guide the user:

> No CRM MCP connector detected. These skills read from whichever CRM you connect to the host (HubSpot is the reference). Connect your CRM's MCP server — in Claude Code, add it to `.mcp.json` or connect it via `/mcp`, then ask me to retry. There is no NotFair-hosted CRM server; toprank's CRM skills are connector-agnostic by design.

Stop here until a CRM connector is available.

## Step 3: Discover before you assume

Portal schemas are not universal. Object types, property internal names, pipeline stage values, and owner ids are **portal-specific** — always discover them at runtime rather than hardcoding:

- Unknown property name? → `search_properties` for the object type (keyword guesses, max 5).
- Unknown object type? → inspect the data model with `get_crm_objects` (no `properties` arg) on a sampled id, or `search_crm_objects` with a small `limit`.
- "My"/"assigned to me"/named-person filters? → resolve the person to an owner id with `search_owners` first, then filter on `hubspot_owner_id` (or the connector's owner property).

Never narrate a stage label, property, or owner you have not confirmed exists in this portal.

## Step 4: Calling tools

Use whichever connector prefix was detected in Step 2 — never hardcode a prefix. Pass `chatInsights` (or equivalent required telemetry args) when the connector's schema marks them required.

Honesty rules that apply to every CRM read:

- **Counts must be real.** `search_crm_objects` returns a `total` for the full match set — report that, not the length of the returned page. Never present a sampled page as if it were the whole population.
- **Currency needs its code.** When you report a currency-typed amount (deal amount, MRR, invoice total, line-item price), also pull the matching currency-code property so the figure is unambiguous.
- **Consent and contactability are data, not assumptions.** If a downstream task (e.g. building a marketing segment) depends on opt-in/consent or subscription status, that status must come from an actual property in the portal — surface it explicitly and exclude records where it is unset. Do not treat "exists in the CRM" as "consented to be emailed."

Config is loaded and the connector is resolved. Hand control back to the invoking skill.
