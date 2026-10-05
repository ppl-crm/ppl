"""Minimal ppl MCP client example.

Connects to the hosted ppl MCP server and fetches the daily briefing.
Requires: pip install mcp
"""

import asyncio
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

PPL_MCP_URL = "https://withppl.com/mcp"
TOKEN = os.environ["PPL_API_TOKEN"]


async def main():
    async with streamablehttp_client(
        PPL_MCP_URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"Available tools: {len(tools.tools)}")

            briefing = await session.call_tool("get_briefing", {})
            print(briefing.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
