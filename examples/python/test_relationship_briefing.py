import contextlib
import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import relationship_briefing as client


class BriefingTests(unittest.TestCase):
    def test_reads_json_with_header_not_token_in_url(self):
        response = contextlib.nullcontext(io.BytesIO(b'{"data":{"birthdays":[]}}'))
        with patch.object(client, "urlopen", return_value=response) as open_url:
            self.assertEqual(client.get_briefing("test-secret"), {"data": {"birthdays": []}})
        request = open_url.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url, client.BRIEFING_URL)
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(open_url.call_args.kwargs["timeout"], 30)

    def run_cli(self, token, error=None):
        stderr, stdout = io.StringIO(), io.StringIO()
        with patch.dict(client.os.environ, {"PPL_API_TOKEN": token}), \
                patch.object(client, "get_briefing", side_effect=error) as read, \
                contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
            code = client.main()
        return code, stderr.getvalue(), stdout.getvalue(), read

    def test_missing_token_does_not_make_a_request(self):
        code, error, output, read = self.run_cli(" ")
        self.assertEqual(code, 1)
        self.assertIn("Set PPL_API_TOKEN", error)
        self.assertEqual(output, "")
        read.assert_not_called()

    def test_denied_requests_do_not_expose_credentials_or_error_body(self):
        for status in (401, 403):
            with self.subTest(status=status):
                error = HTTPError(client.BRIEFING_URL, status, "private-detail", {}, None)
                code, message, output, _ = self.run_cli("test-secret", error)
                self.assertEqual(code, 1)
                self.assertIn("denied access", message)
                self.assertNotIn("test-secret", message)
                self.assertNotIn("private-detail", message)
                self.assertEqual(output, "")

    def test_network_failure_returns_a_useful_error(self):
        code, error, output, _ = self.run_cli("test-secret", URLError("private-detail"))
        self.assertEqual(code, 1)
        self.assertIn("Check the connection", error)
        self.assertNotIn("private-detail", error)
        self.assertEqual(output, "")

    def test_server_failure_reports_status(self):
        code, error, _, _ = self.run_cli("test-secret", HTTPError(client.BRIEFING_URL, 503, "private-detail", {}, None))
        self.assertEqual(code, 1)
        self.assertIn("HTTP 503", error)

    def test_malformed_json_is_handled(self):
        code, error, _, _ = self.run_cli("test-secret", ValueError("private-detail"))
        self.assertEqual(code, 1)
        self.assertIn("Could not read", error)


if __name__ == "__main__":
    unittest.main()
