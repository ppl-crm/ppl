# AGENTS.md: Working with ppl

This file is for AI agents that help users work with ppl, the personal CRM.
Read this before calling the ppl API or MCP tools on a user's behalf.

## What ppl is

ppl is a personal CRM: it tracks the people in a user's life, their
relationships, conversations, tasks, reminders, gifts, journal entries, and
life events. The product thesis: the user's AI agent remembers everyone, so
the user does not have to.

Key concepts:

- **Contact**: a person. Has names, avatar, birthday, job, tags, relationships
  to other contacts, and related records (notes, calls, tasks, reminders,
  gifts, debts, documents, activities, life events).
- **Account**: the tenant. Every user belongs to one account; all data is
  scoped to it. Never mix data across accounts.
- **Journal**: dated free-text entries, optionally linked to contacts.
- **Reminder**: a nudge about a contact (birthday, follow-up, generic).
- **Interaction**: a logged touchpoint (call, email, meeting, message).

## Authentication

All API calls need a Bearer token:

```
Authorization: Bearer <personal-access-token>
```

Users create scoped tokens at **Settings > API > Agent API Keys**
(`/settings/api/keys`). Scopes include `read:contacts`, `write:contacts`,
`agent:briefing`, `agent:actions`, `read:journal`, `write:journal`.

Base URL: `https://ppl.gift/api` (hosted) or the user's `APP_URL/api`
(self-hosted).

## The agent endpoints (start here)

These exist specifically for agents. Prefer them over raw CRUD when they fit:

| Endpoint | Purpose |
|----------|---------|
| `GET /api/agent/briefing` | One call: birthdays, reconnect candidates, open tasks, reminders |
| `GET /api/agent/actions?limit=20` | Ranked suggested actions with scores, reasons, contact refs, deep links |
| `GET /api/search/semantic?q=` | Semantic search over contacts, notes, journal (keyword fallback included) |
| `GET /api/contacts/{id}/digest` | Person digest: summary, last interaction, open tasks, milestones, trajectory |
| `POST /api/interactions/log` | Log an interaction (requires opt-in at `GET /api/interactions/settings`) |

## Conventions

- **Idempotency**: send `Idempotency-Key: <uuid>` on POST/PUT/DELETE. Keys are
  stored 24h; replays return the original response.
- **Sparse fieldsets**: `?fields=id,first_name,last_name` (dot notation for
  nested: `?fields=contact.first_name`). Use this to keep payloads small.
- **Pagination**: cursor-based. Responses include `links.next`; follow it.
  Default limit 25, max 100. Error 30 if the limit is too big.
- **Delta sync**: list endpoints accept `?updated_since=<ISO-8601>` to fetch
  only changed records. Invalid values return error 41.
- **Dates**: `Y-m-d` format unless noted. Reminder dates must be in the future
  (error 38).
- **Errors**: JSON with numeric `error_code`. Common ones: 31 (not found),
  41 (invalid parameters), 42 (not authorized), 43 (interaction capture
  disabled for this account).
- **Rate limit**: 60 requests/minute per token (HTTP 429, error 34).
- **Webhooks**: `POST /api/webhooks/interactions` receives signed interaction
  events for agents that want push instead of poll. See
  `docs/api/interaction-capture.md`.

## Working with contacts

- Search first (`GET /api/search?q=` unified, or `/api/search/semantic?q=`).
  Do not create a duplicate: `POST /api/contacts/check-duplicates` exists.
- Merging: `POST /api/contacts/{id}/merge` with `other_contact_id`;
  `POST /api/contacts/{id}/unmerge` undoes it.
- Timeline: `GET /api/contacts/{id}/timeline` gives chronological history.
- Inactive contacts: `GET /api/contacts?inactive_days=90` finds quiet ones.
- Deleting is soft (archive). Respect `is_active`.

## What not to do

- Never invent contact IDs, tokens, or URLs. Copy them from API responses.
- Never store a user's API token in files, logs, or chat. It is shown once
  at creation for a reason.
- Never act across accounts. One token, one account.
- Do not retry 429s aggressively. Back off.
- Do not use the API to spam contacts or send bulk messages; ppl has no
  bulk-messaging feature and that is intentional.

## Discovery

Machine-readable: `GET https://ppl.gift/.well-known/ppl.json`
Install guide for agents: `docs/agents/INSTALL.md`
OpenAPI spec: `docs/api/openapi.yaml`
