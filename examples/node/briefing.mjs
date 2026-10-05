/**
 * Minimal ppl MCP client example.
 *
 * Connects to the hosted ppl MCP server and fetches the daily briefing.
 * Requires: npm install @modelcontextprotocol/sdk
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const PPL_MCP_URL = "https://withppl.com/mcp";
const TOKEN = process.env.PPL_API_TOKEN;

async function main() {
  const transport = new StreamableHTTPClientTransport(new URL(PPL_MCP_URL), {
    requestInit: {
      headers: { Authorization: `Bearer ${TOKEN}` },
    },
  });

  const client = new Client({ name: "ppl-example", version: "1.0.0" });
  await client.connect(transport);

  const tools = await client.listTools();
  console.log(`Available tools: ${tools.tools.length}`);

  const briefing = await client.callTool({ name: "get_briefing", arguments: {} });
  console.log(briefing.content[0].text);

  await client.close();
}

main().catch(console.error);
