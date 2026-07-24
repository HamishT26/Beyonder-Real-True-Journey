from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v653-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V653V7CloseoutTests(unittest.TestCase):
    def test_final_truth(self) -> None:
        truth = load("final/phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(truth["effective_negatives"], 10444)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (76, 77),
        )
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_terminal_route_is_a_stop(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "STOP_AFTER_TRUTHFUL_CLOSEOUT")
        self.assertFalse(route["downstream_authorized"])
        self.assertIsNone(route["successor_title"])
        self.assertIsNone(route["successor_phase"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["delegation_used"])
        self.assertFalse(route["collaboration_subagent_spawned"])
        self.assertFalse(route["standby_contacted"])
        self.assertFalse(route["activation_sent"])
        self.assertEqual(route["send_count"], 0)

    def test_final_method_flow_preserves_parity(self) -> None:
        ledger = load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 14)
        self.assertEqual(
            ledger["counts"]["witness_results"],
            {"fail": 14, "pass": 14},
        )
        self.assertEqual(ledger["counts"]["states"]["preferred"], 14)

    def test_negative_and_gate_registers(self) -> None:
        negatives = load("final/retained-negative-register.json")
        gates = load("final/exact-open-gate-register.json")
        self.assertEqual(negatives["effective_total"], 10444)
        self.assertTrue(negatives["none_erased"])
        self.assertEqual(gates["effective_open_gaps"], 76)
        self.assertEqual(gates["effective_exact_gates"], 77)
        self.assertTrue(gates["none_silently_closed"])

    def test_final_overview_and_accessible_report(self) -> None:
        overview = (
            PHASE / "reports/final-integrated-overview.md"
        ).read_text(encoding="utf-8")
        report = (
            PHASE / "reports/final-static-report.html"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        self.assertLessEqual(len(overview.split()), 100000)
        self.assertIn("<main>", report)
        self.assertIn("<table>", report)
        self.assertIn("prefers-reduced-motion", report)
        self.assertIn(
            "Manual, assistive-technology", report
        )

    def test_final_manifests_and_review(self) -> None:
        owner = load("validation/final-owner-manifest.json")
        delta = load("validation/final-staged-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertGreater(owner["entry_count"], 200)
        self.assertGreater(delta["entry_count"], 10)
        self.assertEqual(len(owner["self_exclusions"]), 3)
        self.assertEqual(len(delta["self_exclusions"]), 3)
        self.assertTrue(review["valid"])
        self.assertEqual(review["x1_manifest_mismatches"], [])
        self.assertEqual(review["evidence_manifest_mismatches"], [])
        self.assertEqual(
            review["owner_privacy"]["confirmed_hit_count"], 0
        )

    def test_closeout_and_seal_are_candidates(self) -> None:
        closeout = load("final/closeout-receipt.json")
        seal = load("final/seal-receipt.json")
        record = load("final/final-validation-record.json")
        self.assertEqual(closeout["state"], "CLOSEOUT_CANDIDATE")
        self.assertEqual(
            seal["state"], "CONTENT_SEAL_CORRECTION_CANDIDATE"
        )
        self.assertEqual(
            record["state"], "CORRECTED_POSTCOMMIT_CANONICAL_PASS_REQUIRED"
        )
        self.assertFalse(record["successful_replay_permitted"])

    def test_owner_growth_and_document_cap(self) -> None:
        owner = load("validation/owner-file-threshold-final.json")
        cap = load("validation/document-cap-final.json")
        self.assertTrue(owner["below_threshold"])
        self.assertLess(
            owner["owner_generated_file_count_before_lifecycle_manifests"],
            owner["threshold"],
        )
        self.assertTrue(cap["valid"])
        self.assertLessEqual(cap["maximum_words"], cap["cap"])

    def test_stale_label_review(self) -> None:
        receipt = load("validation/stale-label-review.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["stale_paths"], [])

    def test_complete_incomplete_checklist_keeps_external_gates(self) -> None:
        checklist = load("final/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete_bounded"]), 6)
        self.assertEqual(len(checklist["pending_until_postcommit"]), 2)
        self.assertGreaterEqual(len(checklist["incomplete_external"]), 6)
        self.assertEqual(
            checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20"
        )

    def test_final_protocol_is_one_pass_and_scoped(self) -> None:
        protocol = load("validation/final-validation-protocol.json")
        self.assertEqual(protocol["canonical_pass_limit"], 1)
        self.assertTrue(protocol["no_replay_after_success"])
        self.assertEqual(
            protocol["full_repository_suite_owner"],
            "Eiren-only inherited policy",
        )
        self.assertEqual(len(protocol["scoped_test_groups"]), 4)


if __name__ == "__main__":
    unittest.main()
