# Install ppl in Cline

ppl is a hosted-only MCP server. There is nothing to clone, build, or run
locally. Setup is one config entry pointing at the remote endpoint.

## One-step config

In Cline, open MCP Servers settings (the plug icon) and add this server:

```json
{
  "mcpServers": {
    "ppl": {
      "type": "streamableHttp",
      "url": "https://withppl.com/mcp"
    }
  }
}
```

## First connection (OAuth)

ppl uses OAuth 2.0 with Dynamic Client Registration. On the first tool call,
Cline will open a browser window asking the user to sign in at withppl.com
and approve the connection. New users get an account created inline during
approval, no separate signup needed. After approval, the token is stored by
Cline and reused automatically.

## Verify it works

After adding the server, ask Cline to list the ppl tools. You should see 86
tools covering contacts, notes, journal, tasks, reminders, calls, gifts, and
briefings (for example `get_briefing`, `search_contacts`, `log_interaction`).

A read-only smoke check: call `get_briefing` with no arguments. It returns
the user's morning briefing (birthdays, reconnect reminders, open tasks).

## Troubleshooting

- If Cline shows the server as disconnected, remove it and re-add the entry
  above, then trigger one tool call to restart the OAuth flow.
- Token-based alternative: the human can run the agent connect flow at
  https://withppl.com/agents to get an API token, then use it as a Bearer
  token against https://withppl.com/mcp.

Docs: https://withppl.com/agents
