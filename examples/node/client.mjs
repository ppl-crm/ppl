/**
 * Minimal ppl MCP client in Node.js.
 *
 * Get your API token from ppl.gift settings, then:
 *
 *     PPL_TOKEN=your-token-here node client.mjs
 */
const BASE = "https://ppl.gift/mcp";
const TOKEN = process.env.PPL_TOKEN;

async function call(method, params = {}, id = 1) {
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${TOKEN}`,
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
  });
  return res.json();
}

const init = await call("initialize", {
  protocolVersion: "2024-11-05",
  capabilities: {},
  clientInfo: { name: "ppl-example", version: "1.0" },
});
console.log("Server:", init.result.serverInfo);

const tools = await call("tools/list", {}, 2);
const names = tools.result.tools.map((t) => t.name);
console.log(`${names.length} tools. First five: ${names.slice(0, 5).join(", ")}`);

const briefing = await call("tools/call", { name: "get_briefing", arguments: {} }, 3);
console.log("Briefing:", briefing.result.content[0].text.slice(0, 300));
