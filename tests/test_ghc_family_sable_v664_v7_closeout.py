from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_closeout as closeout


PHASE = ROOT / "docs/sable-rook/v664-v7"


def load(relative: str):
    return closeout.strict_json((PHASE / relative).read_bytes(), relative)


class SableV664V7CloseoutTests(unittest.TestCase):
    def test_final_phase_truth_preserves_evidence(self):
        truth = load("closeout/phase-truth.json")
        self.assertTrue(truth["valid"])
        self.assertEqual(truth["source"], closeout.SOURCE)
        self.assertEqual(truth["x1"], closeout.X1)
        self.assertEqual(truth["evidence"], closeout.EVIDENCE)
        self.assertEqual(truth["frozen_proposal_count"], 3990)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 24_934)
        self.assertEqual(truth["effective_methods"], 8_948)
        self.assertEqual(truth["closeout_operational_negatives"], 1)
        self.assertEqual(truth["effective_open_gaps"], 173)
        self.assertEqual(truth["effective_exact_gates"], 171)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_closeout_method_flow_retains_failed_replay(self):
        methods = load("closeout/lifecycle-method-flow.json")
        self.assertTrue(methods["valid"])
        self.assertEqual(methods["new_failed_witness_count"], 1)
        self.assertEqual(methods["new_passing_witness_count"], 1)
        self.assertEqual(methods["effective_negatives"], 24_934)
        self.assertEqual(methods["effective_methods"], 8_948)
        self.assertEqual(methods["failure_erasure_count"], 0)
        self.assertEqual(methods["failures"][0]["failed_witness_credit"], "zero")

    def test_route_remains_prepared_not_sent(self):
        route = load("orchestration/terminal-route-state-final.json")
        self.assertTrue(route["valid"])
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertIsNone(route["successor_title"])
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        handoff = (PHASE / "handoffs/next-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_SABLE_ROOK = false", handoff)
        self.assertNotIn("SENT_BY_SABLE_ROOK = true", handoff)

    def test_closeout_inventory_is_exact_and_bounded(self):
        inventory = load("closeout/closeout-inventory.json")
        self.assertTrue(inventory["valid"])
        self.assertTrue(inventory["within_guard"])
        self.assertEqual(inventory["path_count"], len(closeout.CLOSEOUT_PATHS))
        self.assertEqual(inventory["paths"], closeout.CLOSEOUT_PATHS)
        self.assertLess(inventory["owner_generated_closeout_paths"], 2000)

    def test_candidate_reserves_exact_final_and_canonical_pass(self):
        receipt = load("closeout/closeout-receipt.json")
        candidate = load("closeout/final-validation-candidate.json")
        contract = load("validation/canonical-validation-contract.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["final"], "assigned_after_commit")
        self.assertEqual(receipt["canonical_receipt"], "external_exclusive_receipt_pending")
        self.assertEqual(candidate["successful_invocations"], 0)
        self.assertFalse(candidate["post_success_replay_allowed"])
        self.assertFalse(candidate["full_repository_suite_claimed"])
        self.assertTrue(contract["exclusive_external_receipt"])
        self.assertTrue(contract["one_successful_invocation"])
        self.assertFalse(contract["post_success_replay"])
        self.assertFalse(contract["full_repository_suite"])

    def test_authority_and_security_boundaries_remain_explicit(self):
        security = load("closeout/bounded-security-review.json")
        checklist = load("closeout/complete-incomplete-checklist.json")
        wellbeing = load("closeout/wellbeing-closeout.json")
        self.assertTrue(security["valid"])
        self.assertFalse(security["production_penetration_test"])
        self.assertFalse(security["exhaustive_security"])
        self.assertFalse(security["privacy_complete"])
        self.assertEqual(len(checklist["open_gap"]), 1)
        self.assertEqual(len(checklist["exact_gate"]), 1)
        self.assertIn("Relational working language only", wellbeing["identity_boundary"])
        self.assertTrue(wellbeing["ready_to_stop_on_gate"])

    def test_final_overview_is_three_page_equivalent(self):
        text = (PHASE / "reports/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1500)
        self.assertLessEqual(len(text.split()), 100000)
        for phrase in (
            "NOT_READY_FOR_STAGE_20",
            "Māori authority",
            "zero-row",
            "PREPARED_NOT_SENT",
            "same-owner",
        ):
            self.assertIn(phrase, text)

    def test_all_closeout_json_is_strict(self):
        paths = sorted((PHASE / "closeout").rglob("*.json"))
        paths += sorted((PHASE / "validation").glob("final-*.json"))
        self.assertGreaterEqual(len(paths), 10)
        for path in paths:
            closeout.strict_json(path.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
