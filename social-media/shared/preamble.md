# Social Media Preamble — Connector Detection & Account Setup

Run this at the start of every social-media skill invocation. It is fast when the state is already cached.

---

## Step 1 — Resolve connectors

The social-media skill is connector-agnostic. Detect which of the following are available and note the resolved prefix for use in the rest of the skill.

### A. Meta (Facebook + Instagram — organic posts)

Check whether `mcp__NotFair-MetaAds__runScript` is callable:
- **Yes** → alias `~~meta-social` resolves to `mcp__NotFair-MetaAds__runScript` with Graph API calls
- **No** → fall back to `~~ifttt` or `~~zapier` for Facebook/Instagram

Organic Facebook / Instagram calls go through the same NotFair Meta MCP server as ads — just different Graph API endpoints:
- Facebook Page post: `POST /{page-id}/feed  { message, access_token }`
- Instagram image post: `POST /{ig-user-id}/media  { image_url, caption }` then `POST /{ig-user-id}/media_publish  { creation_id }`

### B. IFTTT (Twitter/X, LinkedIn, Pinterest, Threads, Reddit, Tumblr, YouTube community)

Check whether `mcp__IFTTT__run_action` is callable:
- **Yes** → alias `~~ifttt` resolves to `mcp__IFTTT__*`
- Before any posting action, call `mcp__IFTTT__get_services` to list connected services so you know which platforms are live.

### C. Zapier (enterprise fallback or TikTok)

Check whether `mcp__Zapier__execute_zapier_write_action` is callable:
- **Yes** → alias `~~zapier` resolves to `mcp__Zapier__*`
- Call `mcp__Zapier__list_enabled_zapier_actions` to see which Zaps are live before attempting a write.

### Platform routing (use this order)

| Platform | Primary | Fallback |
|---|---|---|
| Facebook (organic) | `~~meta-social` | `~~ifttt` → `~~zapier` |
| Instagram (organic) | `~~meta-social` | `~~ifttt` → `~~zapier` |
| Twitter / X | `~~ifttt` | `~~zapier` |
| LinkedIn | `~~ifttt` | `~~zapier` |
| TikTok | `~~zapier` | `~~ifttt` |
| Pinterest | `~~ifttt` | `~~zapier` |
| Threads | `~~meta-social` | `~~ifttt` |
| YouTube community | `~~ifttt` | `~~zapier` |

If **no connector is available** for a platform, tell the user which one to connect (IFTTT at https://ifttt.com or Zapier at https://zapier.com / NotFair at https://notfair.co) and skip that platform rather than failing silently.

---

## Step 2 — Load account state

Read `.notfair.json` at the project root (create it if missing). Look for the `social` key:

```json
{
  "social": {
    "facebook_page_id": "",
    "instagram_account_id": "",
    "twitter_username": "",
    "linkedin_company_id": "",
    "tiktok_username": "",
    "pinterest_username": "",
    "connected_platforms": []
  }
}
```

If `social` is missing or `connected_platforms` is empty, run the onboarding flow (Step 3). Otherwise proceed.

---

## Step 3 — Onboarding (first run only)

Ask the user which platforms they want managed. For each:
1. Collect the account identifier (page ID, username, company ID, etc.)
2. Verify the connector is available (Step 1)
3. Write the identifiers into `.notfair.json` under `social`
4. Add the platform to `connected_platforms`

Persist and confirm before proceeding to the actual task.

---

## Step 4 — Rate-limit awareness

| Platform | Typical limit |
|---|---|
| Facebook | 200 calls / hour per app |
| Instagram | 200 calls / hour per app |
| Twitter / X | 50 posts / 24h (standard API) |
| LinkedIn | 100 posts / day (company page) |
| IFTTT | no hard post limit; respect reasonable pacing |
| Zapier | task limits per Zapier plan |

If a session is about to exceed a limit, warn the user and batch the remaining items.
