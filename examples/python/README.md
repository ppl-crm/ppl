# Read your ppl briefing with Python

A morning briefing is a useful first step for an assistant: read the people,
reminders and follow-ups that need attention before suggesting what to do.
These examples read your briefing. They do not create contacts or send messages.

## A client without dependencies

Use Python 3.10 or later. Follow the connection guide at
[withppl.com/agents](https://withppl.com/agents), approve your agent, and store the
returned token in `PPL_API_TOKEN` using your environment or secret manager.
Keep the token private; do not commit it or put it in a URL.

Run from this directory:

```sh
python3 relationship_briefing.py
```

The script sends one authenticated GET request to the hosted REST API and prints
its JSON response. The response contains private relationship information. Keep
that output in your own workspace and share it only with an assistant you trust.
The token needs permission to read briefings. HTTP 401 or 403 means the token or
its permissions need checking; the script does not print the token or the error
response body.

Use `get_briefing(token)` from another Python program to work with the parsed
response. A daily briefing could be a scheduled local task or the first step of
an authorized assistant session. Review suggestions before acting on them.

## MCP client

`briefing.py` demonstrates the MCP Python SDK's v1 client API:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install 'mcp>=1,<2'
python3 briefing.py
```

This example lists the tools and calls `get_briefing`. Pinning the SDK's major
version keeps these imports consistent. OAuth-capable MCP clients can instead
connect to `https://withppl.com/mcp` through the normal approval flow; see
[the OAuth guide](../../docs/oauth.md).

## Verification

The REST example has tests for successful JSON responses, missing credentials,
authorization failures, and connection failures. They use mocked HTTP responses
and make no requests to a real account:

```sh
python3 -m unittest discover -s examples/python -p 'test_*.py'
```

Run the test command from the repository root. An approved token is required to
verify your own account end to end.
