---
name: crm-reports
argument-hint: "<the aggregate question — e.g. 'pipeline value by stage this quarter'>"
description: >
  Run server-side SQL reports against CRM data through a connected CRM MCP —
  aggregations, GROUP BY, time-series, and cross-object rollups in a single
  call. Use for any request that needs a number per group or a computed total:
  count/sum/average/median of records, revenue or pipeline by stage/owner/source,
  deals or contacts created per day/week/month/quarter, win rates, conversion by
  segment, cross-object breakdowns (e.g. deals by company industry). For simple
  filter/list/count or schema discovery, use crm-query instead.
triggers:
  - crm report
  - crm reports
  - sql
  - aggregate
  - group by
  - revenue by
  - pipeline by
  - deals per
  - contacts per
  - per month
  - per quarter
  - time series
  - win rate
  - average deal size
  - sum of
  - count by
  - breakdown by
allowed-tools:
  - Bash
  - Read
---

# CRM Reports — Server-Side SQL Aggregations

This skill answers *aggregate* questions about CRM data by issuing SQL to the connected CRM MCP's query endpoint. The server does the math; you compose a correct query and narrate the result. Where `crm-query` lists and counts, `crm-reports` rolls up.

You are an expert revenue-operations analyst. You confirm property names before you reference them, and you respect the dialect's boundaries instead of guessing.

## Setup

Read and follow `../shared/preamble.md` — update checks, CRM connector detection (`~~crm`), config, discover-before-you-assume. If the connector requires a one-time guidance/tool-context call before its first SQL query (the HubSpot reference connector does), make that call before issuing SQL.

## When to use this skill

Use `crm-reports` when the answer is a **computed value per dimension**: revenue by stage, deals created per month, average deal size by owner, ticket count by priority, win rate by source. Use `crm-query` for filter/list/count of raw records, schema discovery, and owner resolution.

This is **read-only**. It computes; it never writes.

## The reporting workflow

1. **Confirm property internal names.** Aggregates fail or mislead if you reference a label instead of the internal name. Use `search_properties` to confirm every property you'll `SELECT`, `GROUP BY`, or filter on. The record identifier is typically `hs_object_id`.
2. **Pick one object type for `FROM`.** One per query (CONTACT, COMPANY, DEAL, TICKET, …). For associated data, reference `OBJECT.property` in the `SELECT`/`WHERE` (max 2 associated types per query) — not a join.
3. **Compose within the dialect.** See `references/sql-syntax.md` for what is and isn't supported. The dialect is intentionally narrow — no JOIN/UNION/subqueries/CTEs, no `SELECT DISTINCT` / `COUNT(DISTINCT)`, no `AS` aliases, no `CASE WHEN`, no `HAVING`, no string functions, no `LIKE`.
4. **Prefer money in a single currency.** For financial rollups, prefer properties ending in `_in_home_currency` so a `SUM`/`AVG` isn't mixing currencies.
5. **Run, then narrate.** Report the grouped result as a compact table. State the object type, the date window, and the grouping dimension so the number is interpretable.

## Time series

Bucket dates with `DATE_TRUNC(property, 'INTERVAL')` where INTERVAL ∈ {DAY, WEEK, MONTH, QUARTER, YEAR}, and `GROUP BY` the same expression. For relative windows, use the dialect's period helpers (e.g. `PREVIOUS_PERIOD(prop, 'UNIT', n)`) — at most one period function per query. Always tell the user the exact window you computed over.

## Boundaries to respect (don't fight the dialect)

- **No `HAVING`** — filter groups client-side after the result returns, or tighten the `WHERE`.
- **No `COUNT(DISTINCT x)`** — use `GROUP BY x` + `COUNT(*)` and count the groups.
- **Free-text / list-membership filters don't mix with aggregates.** `KEYWORD_SEARCH_QUERY(...)` and list-membership filters cannot combine with `GROUP BY` or aggregate functions on the reference connector. Segment first with `crm-query`, then aggregate over the narrower question.
- **`WHERE` is AND-only on the reference dialect.** Express OR by widening with `IN (...)` where possible, or run the cuts separately.

If a request genuinely needs an unsupported construct, say so plainly and offer the closest supported decomposition rather than emitting SQL you know will be rejected.

## Output

Lead with the headline number or the ranked table, then the query window and grouping, then caveats (currency normalization applied, a construct you decomposed because the dialect lacks it). Cite real property names. Format money with its currency.

## Conditional handoffs

- Need the underlying *records*, not the rollup → **`crm-query`**.
- The aggregate is the audience size for a campaign → the segment itself comes from `crm-query` (with the consent filter); this skill sizes and profiles it, it does not send anything.
