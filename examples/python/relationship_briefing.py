"""Read a ppl briefing without an AI provider or third-party dependencies."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BRIEFING_URL = "https://withppl.com/api/agent/briefing"


def get_briefing(token):
    """Make one read-only request. Keep the token out of URLs and output."""
    request = Request(
        BRIEFING_URL,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    token = os.environ.get("PPL_API_TOKEN", "").strip()
    if not token:
        print("Set PPL_API_TOKEN to your approved ppl token first.", file=sys.stderr)
        return 1
    try:
        briefing = get_briefing(token)
    except HTTPError as error:
        if error.code in (401, 403):
            message = "ppl denied access. Check your token and its briefing permissions."
        else:
            message = f"ppl returned HTTP {error.code}. Try again later."
        print(message, file=sys.stderr)
        return 1
    except (URLError, TimeoutError, ValueError):
        print("Could not read the ppl briefing. Check the connection and try again.", file=sys.stderr)
        return 1
    print(json.dumps(briefing, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
