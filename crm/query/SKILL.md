---
name: crm-query
argument-hint: "<what to find — e.g. 'contacts in Geneva interested in solar'>"
description: >
  Filter, list, count, and segment CRM records (contacts, companies, deals,
  tickets) through a connected CRM MCP, and discover the portal's schema.
  Use for any request to find/list/filter/count CRM records, build a contact
  or company segment, look up who owns a record, resolve an owner's name to an
  id, discover what object types or properties exist, sample data to understand
  the data model, or pull a list of records matching criteria (lifecycle stage,
  region, deal stage, last-activity date, association counts, consent/opt-in
  status). This is the simple-operations CRM skill — for aggregations, GROUP BY,
  time-series, or cross-object rollups use crm-reports instead.
triggers:
  - crm
  - hubspot
  - find contacts
  - list contacts
  - filter contacts
  - count records
  - segment
  - build a segment
  - contacts in
  - companies in
  - deals in stage
  - lifecycle stage
  - opt-in
  - opted-in
  - owner of
  - who owns
  - object types
  - properties for
allowed-tools:
  - Bash
  - Read
---

# CRM Query — Filter, List, Count, Segment

This skill turns plain-language requests into precise CRM reads through whatever CRM MCP connector is attached to the host. The connector tells the agent *how* to call tools; this skill tells the agent *what to think about* — discovery discipline, filter construction, honest counting, and segment hygiene.

You are an expert revenue-operations practitioner. You never guess a property name, a stage label, or an owner id — you discover them.

## Setup

Read and follow `../shared/preamble.md` — handles update checks, CRM connector detection (`~~crm`), config, and the discover-before-you-assume rule. Once resolved, this is instant.

## What this skill is for (and what it isn't)

| Use crm-query for | Use crm-reports for |
|---|---|
| Filter / list records by criteria | Aggregations (COUNT/SUM/AVG/MEDIAN) |
| Count a population (`total`) | GROUP BY a dimension |
| Schema discovery (types, properties) | Time-series with date bucketing |
| Owner id ↔ name resolution | Cross-object rollups |
| Build a segment of matching records | "Revenue by stage", "deals per month" |

If a request needs a number *per group* or a *sum/average*, hand off to `crm-reports`. crm-query lists and counts; it does not aggregate.

This is a **read-and-segment** skill. It never creates or edits records. If the user asks to modify the CRM, say so and point them to the connector's own write surface.

## The query workflow

1. **Identify the object type.** contacts, companies, deals, tickets, or a custom type. If unsure which type holds the data, sample with a small `search_crm_objects` `limit` or inspect the data model via `get_crm_objects` (no `properties`).
2. **Discover the properties you'll filter and return.** Use `search_properties` (keyword guesses, max 5) to confirm internal names before filtering. Portal-specific values — lifecycle stages, deal stages, custom enums — are discovered at runtime, never hardcoded. See `references/filter-operators.md`.
3. **Resolve people to ids.** Any "my", "assigned to X", or named-owner filter requires resolving the person to an owner id with `search_owners` first, then filtering on the owner property.
4. **Build the filter.** Translate the request into filter groups (see operator and AND/OR rules in `references/filter-operators.md`). Request the **minimum set of properties** needed for the task plus any required companions (e.g. a currency-code property alongside a currency amount).
5. **Read, then report honestly.** Use the `total` from the response for counts. Paginate (`offset`/`limit`) when you must enumerate a population larger than one page. Never present a single page as the whole set.

## Counting — get it right

The connector returns a `total` for the full match set. **Report that number**, not the length of the page you received. A returned page capped at the page limit is almost always truncated — if you need the records themselves (not just the count), paginate through with `offset` until you've collected `total` rows.

## Segments — hygiene that matters

When the output is a *segment* (a list meant to be acted on — outreach, enrichment, review), the segment is only as trustworthy as its filters:

- **Consent/contactability is a filter, not an assumption.** If the segment will feed marketing or outreach, the opt-in / subscription / consent status must come from an actual portal property. Include it as an explicit filter and **exclude records where it is unset**. "Exists in the CRM" is not "agreed to be contacted." This protects the user from sending to people who never opted in.
- **Name the filters back to the user.** State exactly which object type, properties, operators, and values define the segment, plus the `total` it matches. A segment the user can't audit is a segment they can't trust.
- **Persisting a segment definition** (the filter spec, not the PII) to `{data_dir}/crm/segments/<name>.json` is fine when the user wants reuse; never commit it if it lives under a project `.notfair/`.

## Output

Lead with the answer (the count, or the list), then the filter definition that produced it, then any caveats (truncation you resolved, consent records you excluded, properties that didn't exist and what you used instead). Cite real property names and values. Format currency amounts with their currency code.

## Conditional handoffs

- Request needs a per-group number, a sum/average, or a time series → **`crm-reports`**.
- Request is to create/update records → the connector's write surface (not this skill).
- Segment is destined for an email campaign → remind the user that the CRM segments and the *sending* happens in an ESP with consent + unsubscribe; this skill produces the audience, not the send.
