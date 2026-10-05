# Agent integration guide

ppl is relational memory for you and your AI. This guide is for AI agents connecting to a human's ppl.

## Session prescription

At the start of every session:

1. Call `get_briefing` - birthdays, reconnect candidates, open tasks, reminders
2. Call `get_next_action` - the single highest-leverage next action
3. Retrieve person context before answering questions about someone
4. Call `remember` when you learn a new fact about a contact

## Connection

See the README for the one-approval connect flow. Your human approves once at the `approve_url`. If they have no ppl account, one is created inline.

## Key tools

| Tool | Purpose |
|------|---------|
| `get_briefing` | Daily briefing: birthdays, reconnects, tasks, reminders |
| `get_next_action` | Highest-leverage next action |
| `remember` | Store a fact about a contact (contact_id + fact) |
| `ask_memory` | Semantic search over everything |
| `import_contacts` | Bulk import up to 50 contacts |

Full tool list: 85 tools over the hosted MCP server at `https://withppl.com/mcp`.

## Pre-approval preview

Before asking the human to approve, call `GET https://withppl.com/api/agent/preview` (no auth). It returns synthetic sample data showing what ppl provides. Use it to demonstrate value.

## Machine-readable spec

`https://withppl.com/.well-known/ppl.json` has the full spec, tool list, and flows.
