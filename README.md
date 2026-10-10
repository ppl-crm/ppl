# ppl

**Relational memory for you and your AI.**

ppl is the personal CRM for humans with AI agents. Your relationships, notes, journal, tasks, and reminders live here. Your AI reads from it before acting, and writes to it after acting.

Read about [ppl](https://withppl.com/about), [choosing a personal CRM](https://withppl.com/personal-crm), or [importing your contacts](https://withppl.com/blog/import-contacts-into-a-personal-crm).

## Connect your AI

**Hosted MCP server:** `https://withppl.com/mcp`

The hosted service is available now. A self-hosted version is coming soon. Your agent connects over Streamable HTTP with a Bearer token.

### One-click setup

Send your human to [withppl.com/agents](https://withppl.com/agents). If they use Cursor and are logged in, it's one click. New users get an account created inline, no signup form first.

### Agent connection flow

1. `POST https://withppl.com/api/agent/connect/request` with `{"client_name": "Your agent"}`
2. Show the human the `approve_url`. They approve once (creating an account inline if needed).
3. Poll the `poll_url` until approved and save the `api_token`.
4. Use the token with the MCP server or REST API.

MCP clients that support OAuth (Claude, ChatGPT, and others) can connect with standard OAuth 2.0: dynamic client registration, PKCE, and refresh tokens. See [docs/oauth.md](docs/oauth.md).

Machine-readable: [ppl.json](https://withppl.com/.well-known/ppl.json), [llms.txt](https://withppl.com/llms.txt), and the [OpenAPI spec](https://withppl.com/openapi.json) for the REST API.

## MCP registry

Registered as `io.github.ppl-crm/ppl` in the official MCP registry. See [server.json](server.json).

## Examples

- [Python briefing examples](examples/python/) - a dependency-free REST client and an MCP SDK client
- [Node MCP client](examples/node/) - connect with the MCP TypeScript SDK
- [ppl-memory PyPI package](https://pypi.org/project/ppl-memory/) - LangGraph, CrewAI, and AutoGen adapters

## Docs

- [Agent integration guide](docs/agents.md) - session prescription, tools, and patterns
- [OAuth for MCP clients](docs/oauth.md) - Dynamic Client Registration flow

## License

MIT. See [LICENSE](LICENSE).
