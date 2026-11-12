from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class AppViewCounterTests(unittest.TestCase):
    def test_counter_is_recorded_once_per_streamlit_session(self):
        with (
            patch.dict(
                os.environ,
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_ANON_KEY": "test-key",
                },
                clear=False,
            ),
            patch("view_counter.record_supabase_view", return_value=(42, 7)) as record,
        ):
            app = AppTest.from_file("app_public.py", default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertEqual(record.call_count, 1)
            rendered = "\n".join(markdown.value for markdown in app.markdown)
            self.assertIn("累計瀏覽 <b>42</b> 次", rendered)
            self.assertIn("今日 7 次", rendered)

            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(record.call_count, 1)


if __name__ == "__main__":
    unittest.main()
