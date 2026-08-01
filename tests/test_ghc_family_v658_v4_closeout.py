#!/usr/bin/env python3
"""Closeout-candidate checks for Eiren Kestrel v658-v4."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v4_closeout_config as c  # noqa: E402


PHASE = ROOT / c.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class EirenV658V4CloseoutTests(unittest.TestCase):
    def test_phase_truth_is_exact_and_not_ready(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual(c.SOURCE_COMMIT, truth["source_commit"])
        self.assertEqual(c.X1_COMMIT, truth["x1_commit"])
        self.assertEqual(c.EVIDENCE_COMMIT, truth["evidence_commit"])
        self.assertEqual(c.FROZEN_PROPOSALS, truth["frozen_proposals"])
        self.assertEqual(c.EXPECTED_OUTCOMES, truth["outcome_counts"])
        self.assertEqual(c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), truth["effective_negatives"])
        self.assertEqual(c.EFFECTIVE_OPEN_GAPS, truth["effective_open_gaps"])
        self.assertEqual(c.EFFECTIVE_EXACT_GATES, truth["effective_exact_gates"])
        self.assertEqual(c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), truth["effective_methods"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_final_negative_gate_and_method_flow_agree(self) -> None:
        negatives = load("truth/retained-negative-register-final-candidate.json")
        gates = load("truth/exact-open-gate-register-final-candidate.json")
        flow = load("method-flow/method-flow-state-final-candidate.json")
        self.assertEqual(c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), negatives["effective_count"])
        self.assertTrue(negatives["all_retained"])
        self.assertEqual(c.EFFECTIVE_OPEN_GAPS, gates["effective_open_gaps"])
        self.assertEqual(c.EFFECTIVE_EXACT_GATES, gates["effective_exact_gates"])
        self.assertTrue(gates["none_silently_closed"])
        self.assertEqual(c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), flow["counts"]["effective_methods"])
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_closeout_seal_and_prerequisites_are_candidates(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        seal = load("seal/seal-candidate.json")
        final = load("final/final-validation-prerequisites.json")
        self.assertEqual("CLOSEOUT_CANDIDATE_READY", closeout["state"])
        self.assertEqual("SEAL_CANDIDATE_READY_FOR_EXACT_FINAL_VALIDATION", seal["state"])
        self.assertEqual("READY_AFTER_COMMIT_PUSH_CLEAN_FRESH_EQUALITY", final["state"])
        self.assertFalse(final["canonical_aggregate_run"])

    def test_route_remains_unsent_until_terminal_gate(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual("Elaren Kestrel", route["next_exact_title"])
        self.assertEqual("v658-v5", route["next_phase"])
        self.assertEqual({"title": "Neris Solane", "phase": "v658-v6"}, route["next_successor_reminder"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])

    def test_roster_and_auth_are_sanitized_and_bounded(self) -> None:
        roster = load("tooling/roster-check-final.json")
        auth = load("tooling/auth-permission-state-final.json")
        self.assertEqual(16, roster["seat_count"])
        self.assertEqual(15, roster["main_task_count"])
        self.assertEqual(1, roster["collaboration_subagent_count"])
        self.assertEqual("Tavian Sol", roster["standby_seat"])
        self.assertEqual("Elaren Kestrel", roster["query"]["resolved_next_main_task"])
        self.assertTrue(auth["hamish_authorized_current_phase"])
        self.assertTrue(auth["terminal_send_authorized_if_gates_pass"])
        self.assertFalse(auth["precontact_authorized"])

    def test_activation_packet_is_sanitized_and_within_word_cap(self) -> None:
        receipt = load("handoffs/elaren-kestrel-v658-v5-activation-receipt.json")
        baton = PHASE / "handoffs/elaren-kestrel-v658-v5-activation.md"
        self.assertTrue(baton.is_file())
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertTrue(receipt["sanitized"])
        self.assertEqual("PREPARED_NOT_SENT", receipt["state"])
        self.assertEqual("Elaren Kestrel", receipt["recipient_exact_title"])
        self.assertEqual("v658-v5", receipt["recipient_phase"])

    def test_commit_local_manifests_have_expected_lifecycle_counts(self) -> None:
        x1 = load("validation/x1-commit-local-manifest.json")
        evidence = load("validation/evidence-commit-local-manifest.json")
        closeout = load("validation/closeout-content-manifest.json")
        owner = load("final/final-owner-manifest.json")
        self.assertEqual(40, x1["entry_count"])
        self.assertEqual(226, evidence["entry_count"])
        self.assertEqual(x1["entry_count"], len(x1["entries"]))
        self.assertEqual(evidence["entry_count"], len(evidence["entries"]))
        self.assertEqual(closeout["entry_count"], len(closeout["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))

    def test_closeout_review_has_no_deletion_or_evidence_rewrite(self) -> None:
        review = load("validation/closeout-staged-review.json")
        self.assertEqual([], review["evidence_changed_paths"])
        self.assertEqual([], review["x1_changed_paths"])
        self.assertEqual([], review["deletions"])
        self.assertTrue(review["valid"])

    def test_final_privacy_caps_and_wellbeing_are_bounded(self) -> None:
        privacy = load("validation/closeout-privacy-scan.json")
        caps = load("validation/final-caps.json")
        wellbeing = load("wellbeing/final-wellbeing-check.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(0, privacy["hit_count"])
        self.assertTrue(caps["owner_files_within_cap"])
        self.assertTrue(caps["documents_within_word_cap"])
        self.assertTrue(caps["commits_within_cap"])
        self.assertEqual(0, wellbeing["successor_contacts"])
        self.assertEqual(0, wellbeing["subagents"])

    def test_final_validator_is_read_only_and_one_shot(self) -> None:
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertTrue(prerequisites["validator_read_only_repository"])
        self.assertTrue(prerequisites["external_receipt_required"])
        self.assertEqual(1, prerequisites["successful_canonical_pass_cap"])
        self.assertTrue(prerequisites["refuse_replay_after_success"])


if __name__ == "__main__":
    unittest.main()
