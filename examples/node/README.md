# Fetch a relationship briefing with Node.js

This small example uses the official MCP TypeScript SDK to connect to ppl and fetch the account owner's briefing. It reads relationship information; it does not write records or send messages.

Use Node.js 20 or newer. Install the SDK in this directory:

```sh
npm install @modelcontextprotocol/sdk
```

Follow [the ppl developer guide](https://withppl.com/developers) to obtain an approved credential. Configure `PPL_API_TOKEN` using your local credential store or a private environment configuration, then run:

```sh
node briefing.mjs
```

The script stops before connecting when the credential is missing. It calls the canonical `agent.briefing.get` tool, checks for a tool error, prints the returned briefing and closes the client. Treat that output as private. Do not put credentials in source control or send relationship information to shared logs.

If the token is revoked, expired or missing the required `agent:briefing` scope, review access with the owner and reconnect when appropriate. Paused installations must be resumed by the owner in [My agents](https://withppl.com/settings/agents). Connecting does not schedule this script or give it permission to read every account record.

For tool schemas, use the [public server card](https://withppl.com/.well-known/mcp/server-card.json). The [developer guide](https://withppl.com/developers#recipes) explains optional discovery profiles and pagination. Those filters describe tools; they do not grant permissions.
