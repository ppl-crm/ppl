# ppl

The personal CRM for AI agents.

ppl is a personal CRM designed to be operated by AI agents. Your AI is the intelligence layer. ppl is the memory and data layer. The agent reads relationship context before acting, and writes back after.

The hosted service runs at [ppl.gift](https://ppl.gift). This repo holds the public agent interface: the MCP server contract, integration docs, and examples. The application itself is private.

## Connect your agent

ppl exposes a [Model Context Protocol](https://modelcontextprotocol.io) server at:

```
https://ppl.gift/mcp
```

Transport: Streamable HTTP. Auth: Bearer token (per-user API token from ppl.gift settings).

80 tools covering: daily briefings, semantic search, person digests, suggested actions, interaction logging, and full CRUD for contacts, notes, tasks, reminders, calls, gifts, journal entries, addresses, relationships, places, debts, documents, and life events.

See [docs/agents.md](docs/agents.md) for the full integration guide.

## Examples

- [examples/python](examples/python) — minimal MCP client in Python
- [examples/node](examples/node) — minimal MCP client in Node.js

## Registry

`server.json` is the MCP registry manifest for this server.

## License

MIT. See [LICENSE](LICENSE).
