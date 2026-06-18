# CRM Query — Filter Operators & Logic

Loaded on demand by `crm-query` when constructing a filter. The canonical surface is the connected CRM MCP's `search_crm_objects`; operator *names* below follow the HubSpot reference connector. If your connector exposes different operator tokens, discover them from the tool schema rather than assuming these.

## Operators

| Intent | Operator | Notes |
|---|---|---|
| Equals | `EQ` | string, enum, boolean (as `'true'`/`'false'`), numeric, owner id |
| Not equals | `NEQ` | excludes exact matches |
| Less / less-or-equal | `LT` / `LTE` | numeric, or ISO date (`YYYY-MM-DD`) |
| Greater / greater-or-equal | `GT` / `GTE` | numeric, or ISO date |
| Range | `BETWEEN` | provide `value` (low) and `highValue` (high) |
| One of | `IN` | provide `values` array |
| None of | `NOT_IN` | provide `values` array |
| Property is set | `HAS_PROPERTY` | non-null; no value needed |
| Property is unset | `NOT_HAS_PROPERTY` | null; no value needed |
| Token match | `CONTAINS_TOKEN` | whole-word/token match, **not** substring |
| Token excluded | `NOT_CONTAINS_TOKEN` | |

Substring matching is not a filter operator — if you truly need "contains text", use the free-text `query` argument (matches the object type's default searchable properties) and verify the hits, or post-filter the returned rows.

## AND / OR logic

The reference connector groups filters into **filter groups**:

- Filters **within the same group** are combined with **AND**.
- **Separate groups** are combined with **OR**.
- Limits on the reference connector: up to 5 filter groups, up to 6 filters per group, 18 filters total.

Worked examples:

- `lifecyclestage = lead` **AND** `hs_lead_status = NEW` → one group, two filters.
- `region = Geneva` **OR** `region = Vaud` → two groups, one filter each (or a single `IN` filter — prefer `IN` for the same property).
- `(stage = qualified AND amount > 5000)` **OR** `(stage = demo AND amount > 10000)` → two groups, two filters each.

## Associations

To filter by relationship ("contacts associated with company X", "deals linked to any company"), use the connector's association filter (`associatedWith` on the reference connector) — `EQUAL`/`IN` against target object ids — rather than a pseudo-property. To filter by *number* of associations, use the dedicated count properties the portal exposes (e.g. `num_associated_deals`, `num_associated_contacts`) and discover the exact name with `search_properties`.

## Dates, booleans, and owners

- **Dates** in comparisons are ISO strings (`YYYY-MM-DD`), not epoch timestamps.
- **Booleans** are stored as strings — compare against `'true'` / `'false'`.
- **Owners**: resolve a person to an owner id with `search_owners` first, then filter the owner property (commonly `hubspot_owner_id`) by that id. Owner ids and user ids are distinct.

## Consent / opt-in as a filter

When the result feeds outreach, treat contactability as a hard filter:

- Discover the portal's consent/subscription property (`search_properties` with keywords like `opt_in`, `subscription`, `consent`, `marketing`, `email_status`).
- Filter to the value that means *opted-in*, and add `HAS_PROPERTY` so records with an unset status are excluded.
- Report how many records were dropped for missing/negative consent — that number is a feature, not noise.
