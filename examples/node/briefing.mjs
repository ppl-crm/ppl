/**
 * Fetch a ppl relationship briefing with the official MCP TypeScript SDK.
 * Run only when the account owner wants a briefing. The output is private.
 *
 * Requires Node.js 20+ and: npm install @modelcontextprotocol/sdk
 * Save an approved token securely, then expose it as PPL_API_TOKEN to this
 * process. Do not commit credentials or send the output to shared logs.
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const PPL_MCP_URL = "https://withppl.com/mcp";

async function main() {
  const token = process.env.PPL_API_TOKEN?.trim();
  if (!token) {
    throw new Error("missing_token");
  }

  const transport = new StreamableHTTPClientTransport(new URL(PPL_MCP_URL), {
    requestInit: {
      headers: { Authorization: `Bearer ${token}` },
    },
  });
  const client = new Client({ name: "ppl-briefing-example", version: "1.1.0" });

  try {
    // The SDK initializes the session and negotiates the MCP protocol.
    await client.connect(transport);
    const briefing = await client.callTool({
      name: "agent.briefing.get",
      arguments: {},
    });
    if (briefing.isError) {
      throw new Error("tool_failed");
    }

    if (briefing.structuredContent) {
      console.log(JSON.stringify(briefing.structuredContent, null, 2));
    } else {
      const text = briefing.content.filter((item) => item.type === "text");
      if (!text.length) {
        throw new Error("missing_result");
      }
      console.log(text.map((item) => item.text).join("\n"));
    }
  } finally {
    await client.close();
  }
}

main().catch((error) => {
  // Do not dump transport internals, headers or private response bodies.
  console.error(error.message === "missing_token"
    ? "Set PPL_API_TOKEN to an approved credential before running this example. See https://withppl.com/developers."
    : "The briefing could not be retrieved. Check the connection, permissions and recovery guidance at https://withppl.com/developers.");
  process.exitCode = 1;
});
