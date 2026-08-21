from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_terminal_correction as correction


PHASE = ROOT / "docs/sable-rook/v664-v7"


def load(relative: str):
    return correction.closeout.strict_json((PHASE / relative).read_bytes(), relative)


class SableV664V7TerminalCorrectionTests(unittest.TestCase):
    def test_failed_canonical_is_preserved_at_zero_credit(self):
        failure = load("correction/canonical-failure-receipt.json")
        self.assertFalse(failure["valid"])
        self.assertEqual(failure["external_receipt_sha256"], correction.FAILED_CANONICAL_SHA256)
        self.assertEqual(failure["tests"], 35)
        self.assertEqual(failure["passed_checks"], 26)
        self.assertEqual(failure["confirmed_privacy_candidates"], 2)
        self.assertEqual(failure["completion_credit"], 0)

    def test_method_flow_adds_failure_without_erasure(self):
        methods = load("correction/method-flow-overlay.json")
        self.assertTrue(methods["valid"])
        self.assertEqual(methods["effective_negatives"], 24_936)
        self.assertEqual(methods["effective_methods"], 8_950)
        self.assertEqual(methods["new_failed_witness_count"], 2)
        self.assertEqual(methods["new_passing_witness_count"], 1)
        self.assertEqual(methods["failure_erasure_count"], 0)
        self.assertTrue(all(row["failed_witness_credit"] == "zero" for row in methods["failures"]))

    def test_scanner_adjudication_is_exact(self):
        raw = correction.closeout.commit_blob(correction.BASE_FINAL, correction.closeout.evidence.EVIDENCE_BUILDER)
        rows = correction.corrected_scan(correction.closeout.evidence.EVIDENCE_BUILDER, raw)
        exact = [row for row in rows if row["excerpt_sha256"] in correction.SCANNER_DEFINITION_DIGESTS]
        self.assertEqual(len(exact), 2)
        self.assertTrue(all(row["disposition"] == "scanner_definition" for row in exact))
        self.assertFalse(any(row["disposition"] == "confirmed_issue" for row in rows))

    def test_correction_truth_and_route_fail_closed(self):
        truth = load("correction/phase-truth.json")
        route = load("orchestration/terminal-route-state-correction.json")
        self.assertTrue(truth["valid"])
        self.assertEqual(truth["base_final"], correction.BASE_FINAL)
        self.assertEqual(truth["phase_commit_count_candidate"], 4)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertIsNone(route["successor_title"])
        self.assertEqual(route["send_count"], 0)

    def test_correction_inventory_and_contract(self):
        inventory = load("correction/correction-inventory.json")
        contract = load("validation/correction-canonical-contract.json")
        self.assertEqual(inventory["paths"], correction.CORRECTION_PATHS)
        self.assertTrue(inventory["within_2000_file_guard"])
        self.assertEqual(contract["base_failed_receipt_sha256"], correction.FAILED_CANONICAL_SHA256)
        self.assertEqual(set(contract["exact_scanner_definition_allowlist"]), correction.SCANNER_DEFINITION_DIGESTS)
        self.assertTrue(contract["one_successful_invocation"])
        self.assertFalse(contract["post_success_replay"])

    def test_all_correction_json_is_strict(self):
        paths = sorted((PHASE / "correction").glob("*.json"))
        paths += sorted((PHASE / "validation").glob("correction-*.json"))
        self.assertGreaterEqual(len(paths), 10)
        for path in paths:
            correction.closeout.strict_json(path.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
