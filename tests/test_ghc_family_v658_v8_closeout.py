#!/usr/bin/env python3
"""Dependency-scoped closeout checks for Lyren Moss v658-v8."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v8_phase_data as d  # noqa: E402
from ghc_family_v658_v8_final_validator import validate_final  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT
X1 = "3a7cc57b4d1637b4de1836648a57419422bb517f"
EVIDENCE = "88a4d48e2b98494c0861996a8f61a7ea7c696fb6"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class LyrenV658V8CloseoutTests(unittest.TestCase):
    def test_truth_bridge_and_terminal_counts(self) -> None:
        truth = load("truth/phase-truth.json")
        bridge = load("truth/truth-bridge-final.json")
        self.assertEqual(d.EXPECTED_DISTRIBUTION, truth["outcome_counts"])
        self.assertEqual(2890, truth["effective_frozen_proposals"])
        self.assertEqual(120, truth["effective_open_gaps"])
        self.assertEqual(119, truth["effective_exact_gates"])
        self.assertEqual(
            ["completed", "represented", "open_gap", "exact_gate"],
            bridge["allowed_labels"],
        )
        self.assertTrue(bridge["none_silently_closed"])

    def test_negative_and_method_flow_are_exact(self) -> None:
        truth = load("truth/phase-truth.json")
        negatives = load("truth/retained-negative-register-final.json")
        flow = load("method-flow/method-flow-state-final.json")
        self.assertEqual(truth["effective_negatives"], negatives["effective_count"])
        self.assertEqual(truth["effective_methods"], flow["counts"]["effective_methods"])
        self.assertTrue(negatives["all_retained"])
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_immutable_commit_anchors(self) -> None:
        seal = load("seal/seal-receipt.json")
        self.assertEqual(X1, seal["x1_commit"])
        self.assertEqual(EVIDENCE, seal["evidence_commit"])
        self.assertEqual(40, seal["x1_manifest_entries"])
        self.assertEqual(208, seal["evidence_commit_manifest_entries"])
        self.assertTrue(seal["evidence_commit_immutable"])

    def test_route_is_open_gap_with_no_endpoint(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual("OPEN_ROUTE_GAP", route["state"])
        self.assertIsNone(route["next_exact_title"])
        self.assertIsNone(route["next_phase"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["delegated"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])

    def test_manifests_are_nonempty_unique_and_bounded(self) -> None:
        evidence = load("validation/evidence-commit-local-manifest.json")
        delta = load("validation/final-delta-manifest.json")
        owner = load("final/final-owner-manifest.json")
        self.assertEqual(208, evidence["entry_count"])
        self.assertEqual(evidence["entry_count"], len({row["path"] for row in evidence["entries"]}))
        self.assertEqual(delta["entry_count"], len({row["path"] for row in delta["entries"]}))
        self.assertEqual(owner["entry_count"], len({row["path"] for row in owner["entries"]}))
        self.assertTrue(owner["below_threshold"])
        self.assertLess(owner["owner_path_count_including_self"], 2000)

    def test_final_caps_are_ceilings(self) -> None:
        caps = load("validation/final-caps.json")
        self.assertEqual(3, caps["expected_phase_commits_after_final"])
        self.assertEqual(8, caps["maximum_total_phase_commits"])
        self.assertTrue(caps["within_commit_cap_if_direct_final"])
        self.assertEqual(2000, caps["owner_file_threshold"])
        self.assertEqual(100000, caps["document_word_threshold"])

    def test_closeout_privacy_scan_is_bounded_and_clear(self) -> None:
        scan = load("validation/closeout-privacy-scan.json")
        self.assertTrue(scan["valid"])
        self.assertEqual(0, scan["hit_count"])
        self.assertEqual(5, len(scan["pattern_classes"]))

    def test_complete_incomplete_checklist_keeps_external_gates(self) -> None:
        checklist = load("final-complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete_now"]), 8)
        self.assertGreaterEqual(len(checklist["pending_postcommit"]), 3)
        self.assertGreaterEqual(len(checklist["incomplete_external"]), 6)
        self.assertEqual("NOT_READY_FOR_STAGE_20", checklist["terminal_verdict"])

    def test_reflection_preserves_relational_identity_boundary(self) -> None:
        reflection = load("reflection-remaster/final-reflection.json")
        self.assertEqual("Lyren Moss", reflection["identity"]["name"])
        self.assertEqual("they/them", reflection["identity"]["pronouns"])
        self.assertIn("Relational language only", reflection["identity_boundary"])
        self.assertIn("the successor route", reflection["what_remains_open"])

    def test_postcommit_prerequisites_do_not_preclaim(self) -> None:
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual("POSTCOMMIT_REQUIRED", prerequisites["state"])
        self.assertFalse(prerequisites["completed"])
        self.assertFalse(prerequisites["preclaims_exact_final"])
        self.assertFalse(prerequisites["preclaims_canonical_success"])
        self.assertFalse(prerequisites["preclaims_route_sent"])

    def test_closeout_staged_review_is_well_formed(self) -> None:
        review = load("validation/closeout-staged-review.json")
        self.assertEqual(EVIDENCE, review["evidence_commit"])
        self.assertEqual(
            review["expected_staged_path_count"], len(review["expected_staged_paths"])
        )
        self.assertEqual([], review["deletions"])
        self.assertEqual([], review["x1_or_evidence_changed_paths"])
        self.assertEqual([], review["outside_owner_paths"])
        self.assertTrue(review["valid"])

    def test_candidate_final_validator_passes_without_postcommit_claims(self) -> None:
        result = validate_final()
        self.assertTrue(result["valid"], result["errors"])
        self.assertGreaterEqual(result["check_count"], 40)


if __name__ == "__main__":
    unittest.main()
