from datetime import datetime, timezone
import unittest

from value_watch.report import render
from value_watch.scoring import score
from value_watch.watchlist import WatchItem


class ReportTests(unittest.TestCase):
    def test_report_labels_missing_fields_explicitly(self):
        content = render([(WatchItem("TEST", "A test operating company."), score({}, {}), {})], datetime(2026, 7, 20, tzinfo=timezone.utc))
        self.assertIn("## Insufficient data", content)
        self.assertIn("| Earnings yield | N/A | N/A | Schwab P/E unavailable |", content)
