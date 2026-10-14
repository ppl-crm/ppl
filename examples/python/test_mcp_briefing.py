import contextlib
import io
import types
import unittest
from unittest.mock import AsyncMock, patch

import briefing as client


class FormattingTests(unittest.TestCase):
    def test_structured_response_is_preferred(self):
        result = types.SimpleNamespace(isError=False, structuredContent={"birthdays": []}, content=[])
        self.assertEqual(client.format_briefing(result), '{\n  "birthdays": []\n}')

    def test_mixed_content_uses_text_not_first_item(self):
        result = types.SimpleNamespace(isError=False, content=[
            types.SimpleNamespace(type="image"),
            types.SimpleNamespace(type="text", text="First part"),
            types.SimpleNamespace(type="text", text="Second part"),
        ])
        self.assertEqual(client.format_briefing(result), "First part\nSecond part")

    def test_tool_error_and_missing_result_are_rejected(self):
        for result in [types.SimpleNamespace(isError=True),
                       types.SimpleNamespace(isError=False, content=[])]:
            with self.subTest(result=result), self.assertRaises(ValueError):
                client.format_briefing(result)


class CommandTests(unittest.TestCase):
    def run_cli(self, token, result=None, error=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.dict(client.os.environ, {"PPL_API_TOKEN": token}), \
             patch.object(client, "fetch_briefing", new=AsyncMock(return_value=result, side_effect=error)) as fetch, \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = client.main()
        return code, stdout.getvalue(), stderr.getvalue(), fetch

    def test_missing_token_stops_before_connection(self):
        code, output, error, fetch = self.run_cli("  ")
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("Set PPL_API_TOKEN", error)
        fetch.assert_not_called()

    def test_failure_does_not_print_private_transport_details(self):
        code, output, error, fetch = self.run_cli("test-secret", error=RuntimeError("private-detail test-secret"))
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("Check the connection", error)
        self.assertNotIn("test-secret", error)
        self.assertNotIn("private-detail", error)
        fetch.assert_awaited_once_with("test-secret")

    def test_success_prints_only_briefing(self):
        result = types.SimpleNamespace(isError=False, structuredContent={"birthdays": []})
        code, output, error, _ = self.run_cli("test-secret", result=result)
        self.assertEqual(code, 0)
        self.assertEqual(error, "")
        self.assertIn('"birthdays": []', output)
        self.assertNotIn("test-secret", output)

    def test_tool_error_is_a_failed_cli_run(self):
        code, output, error, _ = self.run_cli("test-secret", result=types.SimpleNamespace(isError=True))
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("could not be retrieved", error)


class LifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def test_sdk_initializes_calls_canonical_tool_and_closes_on_failure(self):
        events = []
        class FakeSession:
            async def __aenter__(self):
                events.append("session_enter")
                return self
            async def __aexit__(self, *_):
                events.append("session_exit")
            async def initialize(self):
                events.append("initialize")
            async def call_tool(self, name, arguments):
                self_test.assertEqual(name, "agent.briefing.get")
                self_test.assertEqual(arguments, {})
                events.append("call")
                raise RuntimeError("private-detail")
        self_test = self
        @contextlib.asynccontextmanager
        async def transport(url, headers):
            self.assertEqual(url, client.PPL_MCP_URL)
            self.assertEqual(headers, {"Authorization": "Bearer test-secret"})
            events.append("transport_enter")
            try:
                yield ("read", "write", None)
            finally:
                events.append("transport_exit")
        sdk = types.ModuleType("mcp")
        sdk.ClientSession = lambda read, write: FakeSession()
        http = types.ModuleType("mcp.client.streamable_http")
        http.streamablehttp_client = transport
        with patch.dict("sys.modules", {"mcp": sdk, "mcp.client.streamable_http": http}), self.assertRaises(RuntimeError):
            await client.fetch_briefing("test-secret")
        self.assertEqual(events, ["transport_enter", "session_enter", "initialize", "call", "session_exit", "transport_exit"])


if __name__ == "__main__":
    unittest.main()
