# OAuth for MCP clients

ppl supports OAuth 2.0 with Dynamic Client Registration (RFC 7591) for MCP clients like Claude and ChatGPT.

## Discovery

- Authorization server: `https://withppl.com/.well-known/oauth-authorization-server`
- Protected resource: `https://withppl.com/.well-known/oauth-protected-resource`

## Flow

1. Discover the authorization server from the protected resource metadata
2. `POST https://withppl.com/oauth/register` to register your client (PKCE S256)
3. Redirect the human to `https://withppl.com/oauth/authorize`
4. Exchange the code at `https://withppl.com/oauth/token`
5. Call `https://withppl.com/mcp` with the Bearer token

401 responses on `/mcp` include a `WWW-Authenticate` header pointing to the protected resource metadata, per the MCP authorization spec.

## Scopes

`agent:briefing`, `agent:actions`, `agent:search`, `read:contacts`, `write:contacts`, `read:journal`, `write:journal`, `read:tasks`, `write:tasks`
