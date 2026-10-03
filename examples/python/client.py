"""Minimal ppl MCP client in Python.

Get your API token from ppl.gift settings, then:

    export PPL_TOKEN=your-token-here
    python client.py
"""
import json
import os
import urllib.request

BASE = "https://ppl.gift/mcp"
TOKEN = os.environ["PPL_TOKEN"]


def call(method, params=None, msg_id=1):
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "method": method,
        "params": params or {},
    }).encode()
    req = urllib.request.Request(
        BASE,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


if __name__ == "__main__":
    # 1. Initialize
    init = call("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "ppl-example", "version": "1.0"},
    })
    print("Server:", init["result"]["serverInfo"])

    # 2. List tools
    tools = call("tools/list", msg_id=2)
    names = [t["name"] for t in tools["result"]["tools"]]
    print(f"{len(names)} tools. First five: {names[:5]}")

    # 3. Get the daily briefing
    briefing = call("tools/call", {
        "name": "get_briefing",
        "arguments": {},
    }, msg_id=3)
    text = briefing["result"]["content"][0]["text"]
    print("Briefing:", text[:300])
