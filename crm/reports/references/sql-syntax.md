# CRM Reports — SQL Dialect Reference

Loaded on demand by `crm-reports`. Grammar follows the HubSpot reference connector's `query_crm_data`. Other CRM MCPs may differ — when in doubt, read the connector's own tool guidance/schema rather than assuming.

## SELECT

- `SELECT prop1, prop2, ... FROM OBJECT_TYPE`
- Property names must be **internal names**, confirmed via `search_properties`. The identifier is usually `hs_object_id`.
- For money, prefer `*_in_home_currency` properties so aggregates stay single-currency.
- **Unsupported:** `SELECT DISTINCT`, `COUNT(DISTINCT x)`, `AS` aliases, `CASE WHEN`, `IF()`, `COALESCE`, string functions (`CONCAT`, `UPPER`, …).

## Aggregates

`COUNT(*)`, `SUM(prop)`, `AVG(prop)`, `MIN(prop)`, `MAX(prop)`, `MEDIAN(prop)`.

For a distinct count, use `GROUP BY x` + `COUNT(*)` and count the returned groups — `COUNT(DISTINCT x)` is not available.

## FROM

- Exactly **one** object type per query (CONTACT, COMPANY, DEAL, TICKET, …). Discover supported types from the connector (user/details guidance).
- **Unsupported:** `JOIN`, `UNION`, subqueries, CTEs.

## WHERE

- Operators: `=`, `!=`, `<`, `<=`, `>`, `>=`, `IN (...)`, `NOT IN (...)`, `BETWEEN x AND y`, `IS NULL`, `IS NOT NULL`.
- **AND-only** — no `OR`. Express alternatives with `IN (...)`, or run separate queries.
- Dates: compare against date strings (`'2026-01-01'`), not timestamps. Use `BETWEEN 'start' AND 'end'` for ranges.
- Free text: `KEYWORD_SEARCH_QUERY('term', 'prop1', ...)` — at least one property required.
- List membership: the portal's list property (reference connector: `hs_crm_search.ilsListIds = 'LIST_ID'`).
- **`KEYWORD_SEARCH_QUERY` and list-membership cannot be combined with aggregates or `GROUP BY`.** Segment first with `crm-query`, then aggregate.
- **Unsupported:** `LIKE` / `ILIKE`.

## GROUP BY

- Plain dimensions: `GROUP BY dealstage, hubspot_owner_id`.
- Time bucketing: `GROUP BY DATE_TRUNC(createdate, 'MONTH')` — INTERVAL ∈ {DAY, WEEK, MONTH, QUARTER, YEAR}.
- **Unsupported:** `HAVING` — filter the grouped result client-side after it returns.

## Date period helpers (at most one per query)

- `CURRENT_PERIOD(prop, 'UNIT')` — the current calendar unit.
- `PREVIOUS_PERIOD(prop, 'UNIT', count, isFiscal)` — the last N units.
- `NEXT_PERIOD(prop, 'UNIT', count, isFiscal)` — the next N units.

## Cross-object

- Retrieve associated data with `OBJECT.property` (e.g. `SELECT COMPANY.industry, COUNT(*) FROM DEAL GROUP BY COMPANY.industry`).
- For existence checks only, `associations.OBJECT IS NULL` / `IS NOT NULL` in `WHERE` — never in `SELECT` or `GROUP BY`.
- At most **2** different associated object types per query.

## Decomposition cheatsheet (when the dialect says no)

| You want | Dialect lacks | Do instead |
|---|---|---|
| `HAVING count > N` | HAVING | filter the grouped rows client-side |
| `COUNT(DISTINCT owner)` | distinct count | `GROUP BY owner` + count groups |
| OR across properties | `OR` in WHERE | `IN (...)`, or separate queries merged client-side |
| Free-text + GROUP BY | combination | `crm-query` to segment, then aggregate the narrower set |
| substring match | `LIKE` | `KEYWORD_SEARCH_QUERY` (non-aggregate), or post-filter |
