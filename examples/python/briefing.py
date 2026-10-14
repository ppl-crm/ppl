"""Read an authorized ppl briefing with the official MCP Python SDK.

Install: pip install 'mcp>=1,<2'
Set PPL_API_TOKEN through a protected credential mechanism. The briefing
output is private; do not put it in shared logs or source control.
"""

import asyncio
import json
import os
import sys

PPL_MCP_URL = "https://withppl.com/mcp"


async def fetch_briefing(token):
    # Import only after checking the credential; importing this module does
    # not connect to the service or require the optional SDK to be installed.
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    async with streamablehttp_client(
        PPL_MCP_URL,
        headers={"Authorization": f"Bearer {token}"},
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool("agent.briefing.get", {})


def format_briefing(result):
    if result.isError:
        raise ValueError("tool_failed")
    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        return json.dumps(structured, indent=2)
    text = [item.text for item in result.content if item.type == "text"]
    if not text:
        raise ValueError("missing_result")
    return "\n".join(text)


def main():
    token = os.environ.get("PPL_API_TOKEN", "").strip()
    if not token:
        print("Set PPL_API_TOKEN to an approved credential before running this example. "
              "See https://withppl.com/developers.", file=sys.stderr)
        return 1
    try:
        result = asyncio.run(fetch_briefing(token))
        print(format_briefing(result))
        return 0
    except Exception:
        # Avoid printing SDK transport details, headers or private response bodies.
        print("The briefing could not be retrieved. Check the connection, permissions "
              "and recovery guidance at https://withppl.com/developers.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
