from __future__ import annotations

import json
import unittest

from view_counter import record_supabase_view


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class ViewCounterTests(unittest.TestCase):
    def test_records_and_parses_counts(self):
        captured = {}

        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse([{"total_views": 42, "today_views": 7}])

        counts = record_supabase_view(
            "https://example.supabase.co/",
            "test-anon-key",
            opener=opener,
        )

        self.assertEqual(counts, (42, 7))
        self.assertEqual(
            captured["request"].full_url,
            "https://example.supabase.co/rest/v1/rpc/record_page_view",
        )
        self.assertEqual(captured["request"].method, "POST")
        self.assertEqual(captured["request"].data, b"{}")
        self.assertEqual(captured["timeout"], 5)

    def test_rejects_non_https_configuration(self):
        with self.assertRaises(ValueError):
            record_supabase_view("http://example.test", "key")

    def test_rejects_invalid_counts(self):
        def opener(_request, timeout):
            return FakeResponse([{"total_views": 2, "today_views": 3}])

        with self.assertRaises(ValueError):
            record_supabase_view(
                "https://example.supabase.co",
                "key",
                opener=opener,
            )


if __name__ == "__main__":
    unittest.main()
