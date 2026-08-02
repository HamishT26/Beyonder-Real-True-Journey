from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elowen-cairn/v659-v8"
EVIDENCE = "38c529d2aaa6387830d06102ab19ed9735d5f0af"
CLOSEOUT = EVIDENCE


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def clean(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


class ElowenV659V8CloseoutTests(unittest.TestCase):
    def test_final_truth_counts_and_verdict(self) -> None:
        truth = load("final/final-truth.json")
        self.assertEqual("Elowen Cairn", truth["owner"])
        self.assertEqual("v659-v8", truth["phase"])
        flow = load("final/lifecycle-method-flow.json")
        self.assertEqual(3130, truth["effective_frozen"])
        self.assertEqual(19771 + flow["method_count"], truth["effective_negatives"])
        self.assertEqual(6045 + flow["method_count"], truth["effective_methods"])
        self.assertEqual(129, truth["effective_open_gaps"])
        self.assertEqual(128, truth["effective_exact_gates"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_evidence_anchor_is_immutable(self) -> None:
        truth = load("final/final-truth.json")
        receipt = load("final/evidence-receipt.json")
        self.assertEqual(EVIDENCE, truth["x2_evidence"])
        self.assertEqual(EVIDENCE, receipt["x2_evidence"])
        self.assertEqual(40, receipt["valid_fixtures"])
        self.assertEqual(40, receipt["selected_inherited_revalidations"])
        self.assertEqual(200, receipt["retained_mutations"])

    def test_route_is_unresolved_and_unsent(self) -> None:
        route = load("route/prepared-route.json")
        self.assertEqual((None, None), (route["next_exact_title"], route["next_phase"]))
        self.assertEqual((None, None), (route["recipient_next_exact_title"], route["recipient_next_phase"]))
        self.assertFalse(route["later_endpoint_inferred"])
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["direct_reread_performed"])
        self.assertFalse(route["message_sent"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])

    def test_baton_is_long_prepared_and_unsent(self) -> None:
        baton = (PHASE / "handoffs/terminal-route-pending-live-reread.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)), 10_000)
        self.assertIn("PREPARED_BY_ELOWEN_CAIRN = true", baton)
        self.assertIn("SENT_BY_ELOWEN_CAIRN = false", baton)
        self.assertIn("ACTIVATION_TARGET_EXACT_TITLE = UNRESOLVED_PENDING_NEWEST_LIVE_ROUTE_REREAD", baton)
        self.assertIn("ACTIVATION_TARGET_PHASE = UNRESOLVED_PENDING_NEWEST_LIVE_ROUTE_REREAD", baton)
        self.assertNotRegex(baton, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")

    def test_baton_has_forty_new_elowen_dossiers(self) -> None:
        baton = (PHASE / "handoffs/terminal-route-pending-live-reread.md").read_text(encoding="utf-8")
        for number in range(1, 41):
            self.assertIn(f"### {number:02d}. `V6598-P{number:03d}`", baton)

    def test_baton_has_no_trailing_whitespace(self) -> None:
        baton = (PHASE / "handoffs/terminal-route-pending-live-reread.md").read_text(encoding="utf-8")
        self.assertTrue(all(line == line.rstrip() for line in baton.splitlines()))

    def test_outcomes_remain_exactly_four_labels(self) -> None:
        rows = load("evidence/proposal-outcomes.json")["outcomes"]
        counts = {label: sum(row["observed_outcome"] == label for row in rows) for label in {row["observed_outcome"] for row in rows}}
        self.assertEqual({"completed": 30, "represented": 8, "open_gap": 1, "exact_gate": 1}, counts)

    def test_lifecycle_preserves_all_failures(self) -> None:
        lifecycle = load("final/lifecycle-summary.json")
        flow = load("final/lifecycle-method-flow.json")
        self.assertEqual(30 + flow["method_count"], lifecycle["operational_failure_count"])
        self.assertEqual(200, lifecycle["retained_mutation_failure_count"])
        self.assertTrue(all(row["credit"] == 0 and row["retained"] for row in lifecycle["operational_failures"]))

    def test_final_method_flow_pairs_every_closeout_failure(self) -> None:
        flow = load("final/lifecycle-method-flow.json")
        self.assertGreaterEqual(flow["method_count"], 0)
        self.assertEqual(flow["method_count"] * 2, flow["witness_count"])
        if flow["method_count"]:
            self.assertEqual({"fail", "pass"}, {row["result"] for row in flow["witnesses"]})

    def test_open_gate_register_closes_nothing(self) -> None:
        gates = load("final/open-gate-register.json")
        self.assertEqual(0, gates["closed_by_phase"])
        self.assertEqual(129, gates["current_open_gaps"])
        self.assertEqual(128, gates["current_exact_gates"])

    def test_completion_checklist_keeps_terminal_work_incomplete(self) -> None:
        checklist = load("final/completion-checklist.json")
        self.assertIn("one_canonical_aggregate", checklist["incomplete"])
        self.assertIn("single_acknowledged_send", checklist["incomplete"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", checklist["terminal_verdict"])

    def test_closeout_seal_is_precommit_candidate(self) -> None:
        seal = load("final/closeout-seal-receipt.json")
        self.assertEqual("PRECOMMIT_CANDIDATE", seal["state"])
        self.assertEqual(CLOSEOUT, seal["planned_final_parent"])
        self.assertEqual(3, seal["expected_phase_commits"])
        self.assertTrue(seal["canonical_pass_required_after_commit"])
        self.assertTrue(seal["route_held"])

    def test_accessible_static_report_has_table_structure(self) -> None:
        report = (PHASE / "deliverables/v659-v8-accessible-static-report.html").read_text(encoding="utf-8")
        self.assertIn("<caption>Forty bounded Elowen proposal outcomes</caption>", report)
        self.assertIn('scope="col"', report)
        self.assertIn('scope="row"', report)
        self.assertIn("not complete accessibility conformance", report)

    def test_final_overview_is_three_page_equivalent(self) -> None:
        overview = (PHASE / "deliverables/v659-v8-final-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview, flags=re.UNICODE)), 1_000)
        self.assertIn("Elowen Cairn", overview)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)

    def test_document_cap_and_packet_minimum(self) -> None:
        cap = load("validation/final-document-cap.json")
        self.assertTrue(cap["passes"])
        self.assertLessEqual(cap["total_words"], 100_000)
        self.assertGreaterEqual(cap["activation_packet_words"], 10_000)

    def test_privacy_scan_has_zero_confirmed_hits(self) -> None:
        privacy = load("validation/closeout-privacy-scan.json")
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["privacy_complete"])
        self.assertFalse(privacy["security_complete"])

    def test_final_delta_manifest_replays_working_bytes(self) -> None:
        manifest = load("validation/final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(5, len(manifest["self_exclusions"]))
        for row in manifest["entries"]:
            data = clean(ROOT / row["path"])
            self.assertEqual(row["bytes"], len(data), row["path"])
            self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest(), row["path"])

    def test_final_owner_manifest_replays_working_bytes(self) -> None:
        manifest = load("final/final-owner-manifest.json")
        self.assertEqual(3, len(manifest["self_exclusions"]))
        self.assertTrue(manifest["below_threshold"])
        self.assertLess(manifest["owner_path_count_including_exclusions"], 2000)
        for row in manifest["entries"]:
            data = clean(ROOT / row["path"])
            self.assertEqual(row["bytes"], len(data), row["path"])
            self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest(), row["path"])

    def test_staged_review_names_exact_closeout_surface(self) -> None:
        review = load("validation/closeout-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertGreater(review["staged_path_count"], 0)
        self.assertTrue(review["all_owner_closeout_updates"])
        self.assertEqual([], review["outside_declared_final_surface"])
        self.assertEqual([], review["manifest_mismatches"])

    def test_canonical_plan_excludes_full_suite_and_replay(self) -> None:
        plan = load("validation/canonical-pass-plan.json")
        self.assertEqual("Eiren Kestrel", plan["full_repository_suite_owner"])
        self.assertFalse(plan["full_repository_suite_selected"])
        self.assertTrue(plan["one_successful_pass"])
        self.assertTrue(plan["post_success_replay_forbidden"])

    def test_canonical_budget_is_unspent_and_route_is_not_inferred(self) -> None:
        plan = load("validation/canonical-pass-plan.json")
        route = load("route/prepared-route.json")
        self.assertEqual("NOT_RUN_FINAL_CANDIDATE_REQUIRED", plan["state"])
        self.assertTrue(route["newest_live_exact_title_required"])
        self.assertFalse(route["historical_successor_inference_authorized"])

    def test_wellbeing_receipt_preserves_human_control(self) -> None:
        wellbeing = load("wellbeing/final-wellbeing-check.json")
        self.assertTrue(wellbeing["solo"])
        self.assertEqual(0, wellbeing["subagents_spawned"])
        self.assertTrue(wellbeing["human_control_preserved"])
        self.assertTrue(wellbeing["pause_redirect_rename_stop_preserved"])

    def test_every_phase_json_file_parses(self) -> None:
        files = list(PHASE.rglob("*.json"))
        self.assertGreater(len(files), 200)
        for path in files:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
