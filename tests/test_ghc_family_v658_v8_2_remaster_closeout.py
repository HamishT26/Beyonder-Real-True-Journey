from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/lyren-moss/v658-v8-2-remaster"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LyrenV658V8RemasterCloseoutTests(unittest.TestCase):
    def test_final_truth_preserves_exact_counts(self) -> None:
        truth = load("final/final-truth.json")
        self.assertEqual(2910, truth["effective_frozen"])
        self.assertEqual(18078, truth["effective_negatives"])
        self.assertEqual(4352, truth["effective_methods"])
        self.assertEqual(121, truth["effective_open_gaps"])
        self.assertEqual(120, truth["effective_exact_gates"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_four_allowed_outcomes_survive(self) -> None:
        truth = load("final/final-truth.json")
        self.assertEqual(
            {"completed": 33, "represented": 5, "open_gap": 1, "exact_gate": 1},
            truth["observed_outcomes"],
        )

    def test_final_truth_is_same_owner_not_independent(self) -> None:
        truth = load("final/final-truth.json")
        self.assertTrue(truth["same_owner_only"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual("e08a7bb24c9fc9c442374d251b985437a88ade11", truth["x2_evidence"])

    def test_route_is_prepared_and_unsent(self) -> None:
        route = load("route/prepared-route.json")
        self.assertEqual("PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", route["state"])
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["direct_reread_performed"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["bulk_or_parallel_activation_authorized"])

    def test_route_is_ilyra_then_auren(self) -> None:
        route = load("route/prepared-route.json")
        self.assertEqual(("Ilyra Fen", "v659-v1"), (route["next_exact_title"], route["next_phase"]))
        self.assertEqual(
            ("Auren Lark", "v659-v2"),
            (route["recipient_next_exact_title"], route["recipient_next_phase"]),
        )
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])

    def test_activation_packet_is_substantial_and_prepared(self) -> None:
        baton = (PHASE / "handoffs/ilyra-fen-v659-v1-activation.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", baton)), 10000)
        self.assertIn("PREPARED_BY_LYREN_MOSS = true", baton)
        self.assertIn("SENT_BY_LYREN_MOSS = false", baton)
        self.assertIn("TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20", baton)
        self.assertIn("NEXT_EXACT_TITLE = Ilyra Fen", baton)
        self.assertIn("RECIPIENT_NEXT_EXACT_TITLE = Auren Lark", baton)

    def test_activation_packet_has_forty_proposal_dossiers(self) -> None:
        baton = (PHASE / "handoffs/ilyra-fen-v659-v1-activation.md").read_text(encoding="utf-8")
        for number in range(1, 41):
            self.assertIn(f"### {number:02d}. `V6588R2-P{number:03d}`", baton)

    def test_activation_packet_is_sanitized(self) -> None:
        baton = (PHASE / "handoffs/ilyra-fen-v659-v1-activation.md").read_text(encoding="utf-8")
        self.assertNotIn("C:\\Users\\", baton)
        self.assertNotIn("D:\\GHC-Archives\\", baton)
        self.assertNotIn("codex_delegation", baton)
        self.assertTrue(all(line == line.rstrip() for line in baton.splitlines()))
        self.assertIsNone(
            re.search(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", baton)
        )

    def test_lifecycle_retains_twenty_one_operational_failures(self) -> None:
        lifecycle = load("final/lifecycle-summary.json")
        method_flow = load("final/lifecycle-method-flow.json")
        self.assertEqual(21, lifecycle["operational_failure_count"])
        self.assertEqual(200, lifecycle["retained_mutation_failure_count"])
        self.assertTrue(all(row["credit"] == 0 and row["retained"] for row in lifecycle["operational_failures"]))
        self.assertEqual(6, method_flow["method_count"])
        self.assertEqual(["fail", "pass"] * 6, [row["result"] for row in method_flow["witnesses"]])

    def test_closeout_privacy_receipt_has_five_classes_and_zero_hits(self) -> None:
        privacy = load("validation/closeout-privacy-scan.json")
        self.assertEqual(5, len(privacy["classes"]))
        self.assertEqual(0, privacy["hit_count"])
        self.assertEqual([], privacy["hits"])
        self.assertFalse(privacy["privacy_complete"])
        self.assertFalse(privacy["security_complete"])

    def test_final_document_cap_and_baton_floor(self) -> None:
        receipt = load("validation/final-document-cap.json")
        self.assertTrue(receipt["passes"])
        self.assertLessEqual(receipt["total_words"], receipt["cap"])
        self.assertGreaterEqual(receipt["activation_packet_words"], receipt["activation_packet_minimum"])

    def test_final_overview_is_at_least_three_pages_equivalent(self) -> None:
        overview = (PHASE / "deliverables/v658-v8-2-remaster-final-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1000)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("Ilyra Fen", overview)

    def test_final_delta_manifest_replays_working_bytes(self) -> None:
        manifest = load("validation/final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(row["bytes"], path.stat().st_size, row["path"])
            self.assertEqual(row["sha256"], sha256(path), row["path"])

    def test_owner_manifest_replays_working_bytes(self) -> None:
        manifest = load("final/final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertTrue(manifest["below_threshold"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(row["bytes"], path.stat().st_size, row["path"])
            self.assertEqual(row["sha256"], sha256(path), row["path"])

    def test_staged_review_declares_exact_additive_closeout(self) -> None:
        review = load("validation/closeout-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["expected_staged_path_count"], len(review["expected_staged_paths"]))
        self.assertEqual([], review["deletions"])
        self.assertEqual([], review["x1_or_x2_changed_paths"])
        self.assertEqual([], review["outside_owner_paths"])

    def test_canonical_pass_is_not_preclaimed(self) -> None:
        plan = load("validation/canonical-pass-plan.json")
        truth = load("final/final-truth.json")
        self.assertEqual("NOT_RUN_FINAL_CANDIDATE_REQUIRED", plan["state"])
        self.assertEqual("NOT_RUN_FINAL_CANDIDATE_REQUIRED", truth["canonical_pass_state"])
        self.assertTrue(plan["one_successful_pass"])
        self.assertTrue(plan["post_success_replay_forbidden"])

    def test_final_workload_receipt_preserves_solo_and_human_control(self) -> None:
        receipt = load("wellbeing/final-wellbeing-check.json")
        self.assertTrue(receipt["solo"])
        self.assertEqual(0, receipt["subagents_spawned"])
        self.assertEqual(3, receipt["commit_cap"])
        self.assertEqual(5000, receipt["latest_files_scanned"])
        self.assertTrue(receipt["human_control_preserved"])
        self.assertTrue(receipt["pause_redirect_rename_stop_preserved"])


if __name__ == "__main__":
    unittest.main()
