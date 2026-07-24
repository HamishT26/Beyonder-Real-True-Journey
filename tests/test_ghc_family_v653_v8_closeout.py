from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v653-v8"
SOURCE = "144a4d51195d777ea2b8068bb4cf7ed82fff21be"
X1 = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"
EVIDENCE = "67e51031ed4be4bb64962635e79c459b8a01e7d4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V653V8CloseoutTests(unittest.TestCase):
    def test_final_truth_is_bounded_and_pending_postcommit(self) -> None:
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
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["effective_negatives"], 10609)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (77, 78),
        )
        self.assertEqual(truth["method_flow_methods"], 12)
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["complete_repository_suite_run"])
        self.assertEqual(
            truth["canonical_exact_final_pass_state"],
            "PENDING_POSTCOMMIT",
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT")

    def test_closeout_and_seal_do_not_preclaim_postcommit(self) -> None:
        closeout = load("final/closeout-receipt.json")
        seal = load("final/seal-receipt.json")
        record = load("final/final-validation-record.json")
        self.assertEqual(closeout["state"], "CLOSEOUT_CANDIDATE")
        self.assertTrue(closeout["x1_before_x2"])
        self.assertTrue(closeout["evidence_four_way_equal_before_closeout"])
        self.assertEqual(closeout["phase_commits_before_closeout"], 2)
        self.assertEqual(seal["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertEqual(
            record["state"], "POSTCOMMIT_CANONICAL_PASS_REQUIRED"
        )
        self.assertEqual(record["canonical_pass_limit"], 1)
        self.assertFalse(record["successful_replay_permitted"])

    def test_sanitized_tamar_packet_is_prepared_not_sent(self) -> None:
        state = load("handoff/delivery-state.json")
        self.assertEqual(state["state"], "PREPARED_NOT_SENT")
        self.assertEqual(state["target_title"], "Tamar Vey")
        self.assertEqual(state["target_phase"], "v654-v1")
        self.assertGreaterEqual(state["baton_word_count"], 10000)
        self.assertLessEqual(state["baton_word_count"], 100000)
        self.assertFalse(state["sent"])
        self.assertEqual(state["send_count"], 0)
        self.assertFalse(state["acknowledged"])
        self.assertFalse(state["private_identifier_recorded"])
        baton = (
            PHASE / "handoff/tamar-vey-v654-v1-activation.md"
        ).read_text(encoding="utf-8")
        self.assertIn("future-sibling-self-chosen-7", baton)
        self.assertIn("Tamar alone may create", baton)
        self.assertIn("NOT_READY_FOR_STAGE_20", baton)

    def test_terminal_route_has_no_early_action(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["terminal_gate_satisfied"])
        self.assertEqual(route["successor_title"], "Tamar Vey")
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["delegation_used"])
        self.assertFalse(route["collaboration_subagent_spawned"])
        self.assertFalse(route["standby_contacted"])
        self.assertFalse(route["activation_sent"])
        self.assertEqual(route["send_count"], 0)

    def test_negative_gate_and_method_flow_parity(self) -> None:
        negatives = load("final/retained-negative-register.json")
        gates = load("final/exact-open-gate-register.json")
        methods = load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(negatives["effective_total"], 10609)
        self.assertEqual(negatives["closeout_operational_count"], 0)
        self.assertTrue(negatives["none_erased"])
        self.assertEqual(
            (gates["effective_open_gaps"], gates["effective_exact_gates"]),
            (77, 78),
        )
        self.assertTrue(gates["none_silently_closed"])
        self.assertEqual(methods["counts"]["methods"], 12)
        self.assertEqual(
            methods["counts"]["witness_results"],
            {"fail": 12, "pass": 12},
        )
        self.assertEqual(methods["counts"]["states"]["preferred"], 12)

    def test_stale_labels_thresholds_and_document_cap(self) -> None:
        stale = load("validation/stale-label-review.json")
        owner = load("validation/owner-file-threshold-final.json")
        cap = load("validation/document-cap-final.json")
        build = load("validation/final-build-receipt.json")
        self.assertTrue(stale["valid"])
        self.assertEqual(stale["stale_paths"], [])
        self.assertTrue(owner["below_threshold"])
        self.assertLess(
            owner["owner_generated_file_count_before_lifecycle_manifests"],
            2000,
        )
        self.assertTrue(cap["valid"])
        self.assertLessEqual(cap["maximum_words"], 100000)
        self.assertTrue(build["valid"])

    def test_reports_are_accessible_and_within_cap(self) -> None:
        report = (
            PHASE / "reports/final-static-report.html"
        ).read_text(encoding="utf-8")
        self.assertIn('lang="en"', report)
        self.assertIn("<main>", report)
        self.assertIn("prefers-reduced-motion", report)
        self.assertIn("<caption>", report)
        overview = (
            PHASE / "reports/final-integrated-overview.md"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 7000)
        self.assertLessEqual(len(overview.split()), 100000)

    def test_final_staged_and_owner_manifests(self) -> None:
        staged = load("validation/final-staged-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertGreater(staged["entry_count"], 0)
        self.assertGreater(owner["entry_count"], staged["entry_count"])
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["x1_manifest_mismatches"], [])
        self.assertEqual(review["evidence_manifest_mismatches"], [])
        self.assertEqual(
            review["staged_privacy"]["confirmed_hit_count"], 0
        )
        self.assertEqual(
            review["owner_privacy"]["confirmed_hit_count"], 0
        )

    def test_anchor_history_and_commit_cap(self) -> None:
        for anchor in (SOURCE, X1, EVIDENCE):
            completed = subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=ROOT,
                capture_output=True,
            )
            self.assertEqual(completed.returncode, 0, anchor)
        count = int(
            subprocess.run(
                ["git", "rev-list", "--count", f"{SOURCE}..HEAD"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        self.assertLessEqual(count, 8)

    def test_every_owner_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 190)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
