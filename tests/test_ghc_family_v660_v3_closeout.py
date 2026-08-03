#!/usr/bin/env python3
"""Bounded closeout prerequisites for Elaren Kestrel v660-v3."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elaren-kestrel/v660-v3"
SOURCE = "6608caa62705bffd485e734e9b6a576c99b2862e"
X1 = "759c285c49ed95175437f0dd08aff403cfb38618"
EVIDENCE = "PENDING_EVIDENCE_COMMIT"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def clean(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


class ElarenV660V3CloseoutTests(unittest.TestCase):
    def test_final_truth_preserves_exact_counts(self) -> None:
        truth = load("final/final-phase-truth.json")
        self.assertEqual(3190, truth["effective_frozen"])
        self.assertEqual(20180, truth["effective_negatives"])
        self.assertEqual(6214, truth["effective_methods"])
        self.assertEqual(132, truth["effective_open_gaps"])
        self.assertEqual(131, truth["effective_exact_gates"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertFalse(truth["independent_reproduction"])

    def test_program_truth_is_twenty_selected_plus_twenty_new(self) -> None:
        truth = load("final/final-phase-truth.json")
        ledger = load("final/final-proposal-ledger.json")
        self.assertEqual(20, truth["selected_inherited_revalidated"])
        self.assertEqual(0, truth["selected_inherited_novelty_credit"])
        self.assertEqual(0, truth["selected_inherited_completion_credit"])
        self.assertEqual(20, truth["new_unique_executed"])
        self.assertEqual(40, len(ledger["program"]))
        self.assertEqual(
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            truth["observed_outcomes"],
        )

    def test_operational_failures_are_retained_without_predeclared_closeout_failures(self) -> None:
        register = load("final/final-retained-negative-register.json")
        self.assertEqual(20061, register["activation_baseline"])
        self.assertEqual(11, register["x1_operational"])
        self.assertEqual(100, register["x2_synthetic_mutations"])
        self.assertEqual(8, register["x2_operational"])
        self.assertEqual(0, register["closeout_operational"])
        self.assertEqual(20180, register["effective_negatives"])
        self.assertTrue(register["all_failures_retained"])
        signatures = [row["signature"] for row in register["operational_failures"]]
        self.assertTrue(any("workflow-validator-expected-a-composite" in row for row in signatures))

    def test_method_flow_summary_retains_closeout_method(self) -> None:
        summary = load("final/final-method-flow-summary.json")
        self.assertEqual(6214, summary["effective_methods"])
        self.assertEqual(39, summary["phase_counts"]["methods"])
        self.assertEqual(0, summary["closeout_method_count"])
        self.assertEqual([], summary["closeout_methods"])
        self.assertTrue(summary["all_failed_witnesses_retained"])

    def test_source_and_anchor_contracts_are_exact(self) -> None:
        source = load("final/final-source-ledger.json")
        anchors = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual(SOURCE, anchors["source"])
        self.assertEqual(X1, anchors["x1"])
        self.assertEqual(EVIDENCE, anchors["evidence"])
        self.assertEqual(EVIDENCE, anchors["expected_final_parent"])
        self.assertEqual(3, anchors["expected_phase_commits"])
        self.assertEqual(0, anchors["expected_merges"])
        self.assertEqual(SOURCE, source["source_anchors"]["final"])
        self.assertGreaterEqual(len(source["official_sources"]), 6)

    def test_overview_is_three_page_equivalent(self) -> None:
        overview = (PHASE / "deliverables/v660-v3-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 900)
        self.assertIn("Twenty selected inherited", overview)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("Māori authority", overview)

    def test_accessible_report_is_structural_and_reserves_manual_evaluation(self) -> None:
        report = (PHASE / "reports/accessible-static-report-final.html").read_text(encoding="utf-8")
        self.assertIn("<main id=\"main\">", report)
        self.assertIn("Skip to main evidence", report)
        self.assertIn("<caption>", report)
        self.assertIn("Manual keyboard", report)
        self.assertIn("affected-user evaluation remain reserved", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_baton_meets_floor_and_is_sanitized(self) -> None:
        baton = (PHASE / "handoffs/neris-solane-v660-v4-activation.md").read_text(encoding="utf-8")
        count = len(re.findall(r"\b\w+\b", baton))
        self.assertGreaterEqual(count, 10000)
        self.assertLessEqual(count, 100000)
        self.assertIn("Elaren Kestrel", baton)
        self.assertIn("Neris Solane", baton)
        self.assertIn("v660-v4", baton)
        self.assertIn("v660-v3", baton)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertNotRegex(baton, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
        self.assertNotRegex(baton, r"\b[A-Za-z]:[\\/]")
        self.assertNotRegex(baton, r"(?<![A-Za-z0-9])(?:sk-|ghp_)[A-Za-z0-9_-]{20,}")

    def test_route_is_exact_and_unsent(self) -> None:
        route = load("route/prepared-route.json")
        roster = load("orchestration/roster-route-state.json")
        self.assertEqual("Neris Solane", route["target_title"])
        self.assertEqual("v660-v4", route["target_phase"])
        self.assertEqual("NERIS_V660_V4_PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", route["state"])
        self.assertFalse(route["sent"])
        self.assertIn("Tavian Sol", route["forbidden_fallbacks"])
        self.assertEqual("ON_STANDBY_COLLABORATION_SUBAGENT_NOT_ROUTE_ENDPOINT", roster["tavian_sol"])
        self.assertEqual("ACTIVE_RECOVERABLE_MAIN_TASK_NOT_CURRENT_EDGE", roster["caelen_morrow"])
        self.assertTrue(roster["older_compatibility_cycle_conflict_preserved"])

    def test_checklist_keeps_protected_work_incomplete(self) -> None:
        checklist = load("final/complete-incomplete-checklist.json")
        self.assertIn("independent_team_reproduction", checklist["incomplete"])
        self.assertIn("legal_cultural_affected_party_or_maori_authority", checklist["incomplete"])
        self.assertIn("stage20", checklist["incomplete"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", checklist["terminal_verdict"])

    def test_environment_versions_are_observation_only(self) -> None:
        receipt = load("final/environment-version-receipt.json")
        self.assertTrue(receipt["verified_only"])
        self.assertEqual("0.146.0", receipt["versions"]["codex_cli"])
        self.assertEqual("26.727.6591.0", receipt["versions"]["codex_desktop"])
        self.assertIn("desktop_update", receipt["actions_not_taken"])
        self.assertIn("reboot", receipt["actions_not_taken"])

    def test_document_caps_pass(self) -> None:
        cap = load("validation/final-document-cap.json")
        self.assertTrue(cap["passes"])
        self.assertGreaterEqual(cap["baton_words"], 10000)
        self.assertLessEqual(cap["baton_words"], 100000)
        self.assertGreaterEqual(cap["overview_words"], 900)
        self.assertTrue(all(row["passes"] for row in cap["documents"]))

    def test_final_privacy_scan_has_zero_confirmed_hits(self) -> None:
        scan = load("validation/final-privacy-scan.json")
        self.assertEqual(5, len(scan["classes"]))
        self.assertEqual(0, scan["confirmed_hit_count"])
        self.assertEqual([], scan["confirmed_hits"])
        self.assertFalse(scan["privacy_complete"])

    def test_delta_manifest_replays_working_bytes(self) -> None:
        manifest = load("validation/final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            payload = clean(ROOT / row["path"])
            self.assertEqual(row["bytes"], len(payload), row["path"])
            self.assertEqual(row["sha256"], hashlib.sha256(payload).hexdigest(), row["path"])

    def test_owner_manifest_replays_working_bytes(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        self.assertLess(manifest["entry_count"] + len(manifest["exclusions"]), 2000)
        for row in manifest["entries"]:
            payload = clean(ROOT / row["path"])
            self.assertEqual(row["bytes"], len(payload), row["path"])
            self.assertEqual(row["sha256"], hashlib.sha256(payload).hexdigest(), row["path"])

    def test_final_staged_review_declares_exact_files(self) -> None:
        review = load("validation/final-staged-review.json")
        self.assertEqual(review["expected_staged_count"], len(review["intended_allowlist"]))
        self.assertEqual(len(review["intended_allowlist"]), len(set(review["intended_allowlist"])))
        self.assertTrue(all((ROOT / path).is_file() for path in review["intended_allowlist"]))
        observed = review["observed_exact_staged_review"]
        self.assertEqual(review["expected_staged_count"], observed["actual_staged_count"])
        self.assertEqual([], observed["missing_paths"])
        self.assertEqual([], observed["unexpected_paths"])
        self.assertEqual([], observed["x1_path_intersection"])
        self.assertEqual([], observed["x2_path_intersection"])

    def test_canonical_selection_is_one_shot_and_not_full_suite(self) -> None:
        selection = load("validation/final-canonical-selection.json")
        prereq = load("final/final-validation-prerequisites.json")
        self.assertTrue(selection["single_invocation_after_prerequisites"])
        self.assertTrue(selection["never_replay_after_complete_success"])
        self.assertFalse(selection["full_repository_suite"])
        self.assertEqual("NOT_RUN_EXACT_FINAL_REQUIRED", selection["state"])
        self.assertTrue(prereq["no_post_success_replay"])


if __name__ == "__main__":
    unittest.main()
