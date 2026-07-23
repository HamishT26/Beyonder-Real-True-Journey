from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV652V2Closeout(unittest.TestCase):
    def test_final_truth_and_stage20_board(self):
        truth = load("final/phase-truth.json")
        board = load("final/terminal-stage20-board.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((truth["effective_negatives"], truth["open_gaps"], truth["exact_gates"]), (8202, 63, 64))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(board["ready"])

    def test_route_and_future_seats_are_held(self):
        route = load("route/terminal-route-state.json")
        seats = load("provenance/future-cli-placeholder-invariant.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual((route["send_count"], route["create_or_fork_count"], route["standby_contact_count"]), (0, 0, 0))
        self.assertEqual((seats["prepared_placeholder_count"], seats["named_count"], seats["created_count"], seats["launched_count"]), (8, 0, 0, 0))

    def test_method_flow_and_negative_retention(self):
        method = load("method-flow/method-flow-ledger.json")
        negatives = load("final/retained-negative-register.json")
        self.assertEqual((method["counts"]["methods"], method["counts"]["witnesses"]), (27, 56))
        self.assertEqual(method["counts"]["witness_results"], {"fail": 29, "pass": 27})
        self.assertEqual(negatives["effective_at_closeout"], 8202)
        self.assertEqual(negatives["closeout_operational_count"], 6)
        self.assertTrue(negatives["no_failure_erased"])

    def test_baton_overview_and_report(self):
        baton = (ROOT / "handoffs/tamar-vey-v652-v3-activation.md").read_text(encoding="utf-8")
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", baton)), 10000)
        self.assertLessEqual(len(re.findall(r"\b\w+\b", baton)), 100000)
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1500)
        for token in ("Skip to main content", "<caption>", "scope='col'", "tabindex='0'", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, report)

    def test_open_and_exact_gates_remain_open(self):
        gaps = load("final/open-gap-register.json")
        gates = load("final/exact-gate-register.json")
        self.assertEqual((gaps["effective_count"], gaps["closed_count"], gaps["real_rows"], gaps["likelihoods"]), (63, 0, 0, 0))
        self.assertEqual((gates["effective_count"], gates["closed_count"], gates["authority_decisions"]), (64, 0, 0))

    def test_closeout_and_seal_candidates(self):
        closeout = load("final/closeout-receipt.json")
        seal = load("final/seal-candidate.json")
        self.assertEqual(closeout["expected_phase_commits"], 3)
        self.assertEqual(closeout["expected_merges"], 0)
        self.assertEqual(seal["expected_final_parent"], "d185405470b9205a21d9b018bc0d3f7f44f49444")
        self.assertEqual(seal["canonical_validation_state"], "PENDING_SINGLE_PASS")
        self.assertTrue(closeout["valid_candidate"] and seal["valid_candidate"])

    def test_environment_and_authority_boundaries(self):
        env = load("final/environment-version-receipt.json")
        self.assertTrue(env["versions_verified_only"] and env["d_first"])
        for field in ("desktop_updated", "sandbox_or_hyperv_launched", "elevation", "host_security_changed", "windows_features_changed", "unrelated_install", "reboot"):
            self.assertFalse(env[field])
        truth = load("final/phase-truth.json")
        self.assertFalse(truth["full_repository_suite_run"] or truth["independent_reproduction_claimed"])

    def test_manifest_contracts_exist(self):
        for relative in (
            "validation/x1-staged-manifest.json",
            "validation/evidence-staged-manifest.json",
            "validation/closeout-delta-manifest.json",
            "validation/final-owner-manifest.json",
            "validation/closeout-staged-privacy.json",
            "validation/closeout-staged-review.json",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
