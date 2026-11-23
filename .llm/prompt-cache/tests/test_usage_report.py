"""Offline CLI checks with synthetic, content-free events."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

CACHE_ROOT = Path(__file__).resolve().parents[1]
REPORT = CACHE_ROOT / "scripts" / "analyze-usage-events.py"


def event(**fields):
    return {
        "timestamp": "2026-11-15T12:00:00+00:00",
        "request_type": "kaoyan_plan",
        "template_id": "claude_code_session",
        "template_version": "transcript-v1",
        "model": "deepseek-v4-flash",
        "input_tokens": 10,
        "cache_read_tokens": 90,
        **fields,
    }


class UsageReportTest(unittest.TestCase):
    def setUp(self):
        temp = self.enterContext(TemporaryDirectory())
        self.events = Path(temp) / "events.jsonl"

    def run_report(self, events, *args):
        self.events.write_text("".join(json.dumps(row) + "\n" for row in events), encoding="utf-8")
        return subprocess.check_output([sys.executable, "-I", str(REPORT), "--events-file", str(self.events), *args], text=True)

    def test_no_default_model_filter_and_no_cross_model_baseline(self):
        rows = [event(), event(model="deepseek-v4.1-flash"), event(model="gpt-6-luna")]
        report = self.run_report(rows)
        self.assertIn("events: 3 of 3 (models: all)", report)
        self.assertEqual(report.count("vs snapshot:"), 1)
        new_model_line = next(line for line in report.splitlines() if "deepseek-v4.1-flash" in line)
        self.assertEqual(new_model_line.split()[7:9], ["N/A", "N/A"])
        filtered = self.run_report(rows, "--model", "deepseek-v4.1-flash")
        self.assertIn("[no-matching-data] kaoyan_plan_daily", filtered)
        self.assertNotIn("vs snapshot:", filtered)

    def test_new_collector_and_template_version_do_not_share_legacy_baseline(self):
        report = self.run_report([
            event(metadata={"collector_version": 2, "cache_semantics": "unknown"}),
            event(template_version="transcript-v2"),
        ])
        self.assertIn("[no-matching-data] kaoyan_plan_daily", report)
        self.assertNotIn("vs snapshot:", report)

    def test_declared_anthropic_accounts_for_cache_writes(self):
        report = self.run_report([event(
            model="sample",
            cache_write_tokens=20,
            metadata={"collector_version": 2, "cache_semantics": "anthropic"},
        )], "--no-baseline")
        line = next(line for line in report.splitlines() if "2/anthropic" in line)
        self.assertEqual(line.split()[7:9], ["120", "75.0"])

    def test_missing_cache_field_differs_from_zero(self):
        meta = {"collector_version": 2, "cache_semantics": "anthropic"}
        zero = event(model="zero", cache_read_tokens=0, cache_write_tokens=0, metadata=meta)
        missing = event(model="missing", cache_write_tokens=0, metadata=meta)
        del missing["cache_read_tokens"]
        report = self.run_report([zero, missing], "--no-baseline")
        parsed = {line.split()[2]: line.split()[6:9] for line in report.splitlines() if "2/anthropic" in line}
        self.assertEqual(parsed, {"zero": ["0", "10", "0.0"], "missing": ["N/A", "N/A", "N/A"]})

    def test_snapshot_day_and_earlier_events_are_excluded_from_delta(self):
        old = event(timestamp="2026-08-10T12:00:00+00:00")
        self.assertIn("[no-post-snapshot-data] kaoyan_plan_daily", self.run_report([old]))
        report = self.run_report([old, event()])
        delta = next(line for line in report.splitlines() if "vs snapshot:" in line)
        self.assertRegex(delta, r"n=\s+1\b")

    def test_single_file_date_filter_uses_event_timestamp(self):
        report = self.run_report([event(), event(timestamp="2026-10-31T23:59:59+00:00")], "--since", "2026-11-01")
        self.assertIn("events: 1 of 1", report)


if __name__ == "__main__":
    unittest.main()
