from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_auren_lark_v666_v5_runtime import PHASE_ROOT, X1_SHA, load_json, replay_manifest  # noqa: E402


def load(relative: str) -> dict:
    return load_json(PHASE_ROOT / relative)


class AurenLarkV666V5EvidenceTests(unittest.TestCase):
    def test_evidence_summary_exact(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["proposal_chain_total"], 4270)
        self.assertEqual(summary["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(summary["rejected_negative_mutations"], 100)
        self.assertEqual(summary["core_x2_method_count"], 215)
        self.assertEqual(summary["operational_failure_count"], 8)
        self.assertEqual(summary["effective_negatives"], 26637)
        self.assertEqual(summary["effective_methods"], 11409)
        self.assertEqual(summary["open_gaps"], 187)
        self.assertEqual(summary["exact_gates"], 185)
        self.assertEqual(summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_x2_test_receipt_is_attributable_and_noncanonical(self) -> None:
        receipt = load("evidence/evidence-test-receipt.json")
        self.assertEqual(receipt["observed_test_count"], 66)
        self.assertEqual(receipt["expected_test_count"], 66)
        self.assertEqual(receipt["returncode"], 0)
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["canonical_aggregate"])

    def test_failed_mixed_lifecycle_invocation_is_retained(self) -> None:
        receipt = load("evidence/evidence-test-recovery-receipt.json")
        self.assertEqual(receipt["failed_observed_tests"], 77)
        self.assertEqual(receipt["failed_observed_failures"], 1)
        self.assertEqual(receipt["failed_aggregate_credit"], 0)
        self.assertEqual(receipt["failure_retained_as"], "AL6665-OPS-N002")
        self.assertTrue(receipt["recovery_valid"])

    def test_privacy_and_security_receipts_are_bounded(self) -> None:
        privacy = load("evidence/privacy-scan-receipt.json")
        security = load("evidence/security-scan-receipt.json")
        self.assertEqual(len(privacy["classes"]), 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(privacy["valid"])
        self.assertGreaterEqual(security["scanned_python_count"], 16)
        self.assertEqual(security["finding_count"], 0)
        self.assertTrue(security["valid"])
        self.assertIn("not privacy-complete", privacy["claim_boundary"])
        self.assertIn("not exhaustive security", security["claim_boundary"])

    def test_x1_manifest_replays_exactly(self) -> None:
        receipt = load("evidence/x1-immutability-receipt.json")
        replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
        self.assertEqual(replay["entry_count"], 20)
        self.assertEqual(replay["failure_count"], 0)
        self.assertTrue(replay["valid"])
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["x1_modified"])

    def test_evidence_seal_binds_core_ledgers_without_terminal_claim(self) -> None:
        seal = load("seal/evidence-seal.json")
        for key in (
            "ledger_canonical_sha256",
            "method_flow_canonical_sha256",
            "operational_overlay_canonical_sha256",
            "gate_register_canonical_sha256",
            "evidence_summary_canonical_sha256",
        ):
            self.assertRegex(seal[key], r"^[0-9a-f]{64}$")
        self.assertFalse(seal["canonical_aggregate_invoked"])
        self.assertFalse(seal["successor_contacted"])
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_toolbox_and_deck_receipts_are_bounded(self) -> None:
        toolbox = load("evidence/meta-toolbox-receipt.json")
        cards = load("evidence/flashcard-evidence-receipt.json")
        self.assertEqual(toolbox["skills"]["count"], 10)
        self.assertEqual(toolbox["runners"]["count"], 10)
        self.assertTrue(toolbox["skills"]["all_built_tested_used_bounded"])
        self.assertTrue(toolbox["runners"]["all_smoke_passed"])
        self.assertTrue(toolbox["closeout_runner_probe_only"])
        self.assertTrue(toolbox["canonical_runner_probe_only"])
        self.assertEqual(cards["card_count"], 25)
        self.assertTrue(cards["model_valid"])
        self.assertFalse(cards["successor_contacted"])

    def test_no_closeout_final_or_handoff_materialized(self) -> None:
        self.assertFalse((PHASE_ROOT / "closeout").exists())
        self.assertFalse((PHASE_ROOT / "final").exists())
        self.assertFalse((PHASE_ROOT / "handoffs").exists())
        self.assertFalse(load("evidence/evidence-build-receipt.json")["canonical_aggregate_invoked"])

    def test_authority_gaps_and_terminal_verdict_remain(self) -> None:
        gaps = load("evidence/authority-and-evidence-gaps.json")
        self.assertEqual(gaps["open_gap_count"], 187)
        self.assertEqual(gaps["exact_gate_count"], 185)
        self.assertGreaterEqual(len(gaps["protected_domains"]), 6)
        self.assertEqual(gaps["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_evidence_json_parses(self) -> None:
        paths = sorted((PHASE_ROOT / "evidence").glob("*.json")) + [PHASE_ROOT / "seal" / "evidence-seal.json"]
        self.assertGreaterEqual(len(paths), 12)
        for path in paths:
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw)
            json.loads(raw.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
