#!/usr/bin/env python3
"""Precommit closeout-candidate tests for Vesper Arlen v658-v7."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v658-v7"
X1 = "f972f1c219de7169d0da3df2933d916434d488dd"
EVIDENCE = "fd3fbcb71e6c1e4edc46644c5ceb617009d20e84"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class VesperV658V7CloseoutTests(unittest.TestCase):
    def test_closeout_anchors_and_truth(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(X1, receipt["x1_commit"])
        self.assertEqual(EVIDENCE, receipt["evidence_commit"])
        self.assertEqual({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, receipt["outcomes"])
        self.assertEqual(17673, receipt["effective_negatives"])
        self.assertEqual(3947, receipt["effective_methods"])
        self.assertEqual((119, 118), (receipt["effective_open_gaps"], receipt["effective_exact_gates"]))
        self.assertEqual("NOT_READY_FOR_STAGE_20", receipt["terminal_verdict"])

    def test_closeout_does_not_preclaim_final_or_canonical(self) -> None:
        truth = load("truth/phase-truth.json")
        closeout = load("closeout/closeout-receipt.json")
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertIsNone(truth["final_commit"])
        self.assertFalse(closeout["canonical_validation_completed"])
        self.assertEqual("POSTCOMMIT_REQUIRED", prerequisites["state"])
        self.assertFalse(prerequisites["completed"])
        self.assertFalse(prerequisites["preclaims_exact_final"])

    def test_route_is_prepared_not_sent_to_lyren(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual("PREPARED_NOT_SENT", route["state"])
        self.assertEqual("Lyren Moss", route["next_exact_title"])
        self.assertEqual("v658-v8", route["next_phase"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_baton_is_sanitized_file_backed_and_elaborate(self) -> None:
        receipt = load("handoffs/lyren-moss-v658-v8-activation-receipt.json")
        path = PHASE / "handoffs/lyren-moss-v658-v8-activation.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual("PREPARED_NOT_SENT", receipt["state"])
        self.assertGreaterEqual(receipt["word_count"], 8000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertEqual(receipt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertIn("SENT_BY_VESPER_ARLEN = false", text)
        self.assertNotIn("thread://", text)

    def test_manifests_are_nonempty_and_cardinality_bound(self) -> None:
        evidence = load("validation/evidence-commit-local-manifest.json")
        delta = load("validation/final-delta-manifest.json")
        owner = load("final/final-owner-manifest.json")
        self.assertEqual(210, evidence["entry_count"])
        self.assertEqual(evidence["entry_count"], len(evidence["entries"]))
        self.assertEqual(delta["entry_count"], len(delta["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))
        self.assertTrue(owner["below_threshold"])

    def test_closeout_privacy_and_caps(self) -> None:
        privacy = load("validation/closeout-privacy-scan.json")
        caps = load("validation/final-caps.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(0, privacy["hit_count"])
        self.assertTrue(caps["within_commit_cap_if_direct_final"])
        self.assertLessEqual(caps["expected_phase_commits_after_final"], caps["maximum_total_phase_commits"])

    def test_checklist_preserves_external_incompleteness(self) -> None:
        checklist = load("final-complete-incomplete-checklist.json")
        self.assertTrue(checklist["complete_now"])
        self.assertTrue(checklist["pending_postcommit"])
        self.assertTrue(checklist["incomplete_external"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", checklist["terminal_verdict"])

    def test_final_owner_index_auth_and_roster_are_consistent(self) -> None:
        index = load("tooling/ghc-family-index-final.json")
        auth = load("tooling/auth-permission-state-final.json")
        roster = load("tooling/roster-check-final.json")
        self.assertEqual("Lyren Moss", index["next_exact_title"])
        self.assertEqual("Vesper Arlen", auth["active_owner"])
        self.assertEqual("Lyren Moss", roster["terminal_successor_exact_title"])
        self.assertFalse(roster["successor_resolved"])
        self.assertFalse(roster["successor_contacted"])


if __name__ == "__main__":
    unittest.main()
