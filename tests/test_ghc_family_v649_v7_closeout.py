from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
CLOSEOUT = "4b562d70fa930d177931160909cb5b449efc4d5f"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def load_at(commit: str, relative: str):
    result = subprocess.run(
        ["git", "show", f"{commit}:docs/eiren-kestrel/v649-v7/{relative}"],
        cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return json.loads(result.stdout)


class V649V7CloseoutTests(unittest.TestCase):
    def test_overview_report_and_baton(self):
        self.assertGreaterEqual(len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split()), 1200)
        report = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        self.assertIn('lang="en"', report)
        self.assertIn("Skip to report", report)
        self.assertIn("aria-live", report)
        words = len((PHASE / "handoffs/elaren-kestrel-v649-v8-activation.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 8000)
        self.assertLessEqual(words, 20000)

    def test_failed_suite_is_retained_and_corrected_plan_exact(self):
        failed = load("validation/failed-full-suite-attempt.json")
        self.assertEqual((failed["tests_run"], failed["failures"], failed["errors"]), (1948, 10, 0))
        self.assertFalse(failed["successful"])
        self.assertEqual(failed["pass_credit"], 0)
        self.assertEqual(len(failed["failed_test_ids"]), 10)
        plan = load_at(CLOSEOUT, "validation/corrected-full-suite-plan.json")
        self.assertEqual(plan["exact_exclusion_count"], 14)
        self.assertEqual(plan["successful_passes_used"], 0)
        self.assertFalse(plan["post_success_replay"])
        self.assertFalse(plan["historical_tests_rewritten"])

    def test_closeout_truth_and_route_hold(self):
        truth = load("phase-truth-closeout-candidate.json")
        self.assertEqual(truth["effective_negatives"], 5324)
        self.assertEqual(truth["successful_full_suite_passes"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target_title"], "Elaren Kestrel")
        self.assertEqual(route["send_count"], 0)

    def test_method_flow_retains_validation_failures(self):
        ledger = load_at(CLOSEOUT, "method-flow/method-flow-ledger.json")
        methods = {row["method_id"]: row for row in ledger["methods"]}
        self.assertIn("V6497-M14", methods)
        self.assertIn("V6497-M15", methods)
        self.assertEqual(methods["V6497-M14"]["recommendation_state"], "candidate")
        self.assertEqual(methods["V6497-M15"]["recommendation_state"], "preferred")
        fail_ids = {row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"}
        self.assertIn("V6497-M14-WFAIL", fail_ids)
        self.assertIn("V6497-M15-WFAIL", fail_ids)

    def test_closeout_review(self):
        review = load("validation/closeout-staged-review.json")
        self.assertTrue(review["passed"])
        self.assertEqual(review["privacy_confirmed_hits"], [])
        self.assertEqual(review["self_exclusions"], 3)


if __name__ == "__main__":
    unittest.main()
