"""Scoped closeout tests for Sylven Arc v656-v3."""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/sylven-arc/v656-v3"
SOURCE = "b18aab36fd8193fce55df3d5b7055b94354dda7e"
X1 = "ae46f611f3b13b2ae77d0f0a13d35f13049ef75d"
EVIDENCE = "f0de53a52e9f4e99e6dda1ee6d02de8cfb4e7da6"
FINAL_CODE = {
    "scripts/build_ghc_family_v656_v3_closeout.py",
    "scripts/ghc_family_v656_v3_final_staged_review.py",
    "scripts/ghc_family_v656_v3_final_validate.py",
    "tests/test_ghc_family_v656_v3_closeout.py",
}


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class SylvenArcV656V3CloseoutTests(unittest.TestCase):
    def test_exact_anchors_and_candidate_lifecycle(self) -> None:
        anchors = load("lifecycle/phase-anchor-contract.json")
        record = load("lifecycle/final-record.json")
        self.assertEqual(anchors["source"], SOURCE)
        self.assertEqual(anchors["x1_freeze"], X1)
        self.assertEqual(anchors["evidence"], EVIDENCE)
        self.assertEqual(anchors["expected_phase_commits_after_final"], 3)
        self.assertTrue(anchors["zero_merges_required"])
        self.assertTrue(anchors["final_parent_must_equal_evidence"])
        self.assertIsNone(record["final_commit"])
        self.assertEqual(
            record["record_state"],
            "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
        )

    def test_outcomes_negatives_gaps_and_gates(self) -> None:
        truth = load("truth/phase-truth-final.json")
        negatives = load("truth/retained-negative-register-final.json")
        gaps = load("truth/open-gap-register-final.json")
        gates = load("truth/exact-gate-register-final.json")
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(truth["effective_negative_count"], 14_183)
        self.assertEqual(negatives["effective_final"], 14_183)
        self.assertEqual(negatives["final_operational_count"], 12)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(gaps["effective_count"], 99)
        self.assertEqual(gaps["closed_count"], 0)
        self.assertEqual(gates["effective_count"], 98)
        self.assertEqual(gates["closed_count"], 0)

    def test_method_flow_retains_paired_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-ledger-final.json")
        validation = load("method-flow/method-flow-validation-final.json")
        counts = ledger["counts"]
        self.assertEqual(counts["methods"], 470)
        self.assertEqual(counts["witness_results"]["fail"], 470)
        self.assertEqual(counts["witness_results"]["pass"], 470)
        self.assertEqual(len(ledger["current_phase_final_method_ids"]), 12)
        self.assertTrue(validation["valid"])

    def test_roster_and_route_are_single_valued(self) -> None:
        roster = load("orchestration/roster-state.json")
        auth = load("orchestration/auth-permission-state.json")
        active = [row["name"] for row in roster["active"]]
        self.assertEqual(roster["active_count"], 15)
        self.assertEqual(len(set(active)), 15)
        self.assertIn("Caelen Morrow", active)
        self.assertIn("Elaren Kestrel", active)
        self.assertEqual(roster["standby"][0]["name"], "Tavian Sol")
        self.assertEqual(roster["standby"][0]["state"], "ON_STANDBY")
        self.assertEqual(auth["authorized_next_exact_title"], "Caelen Morrow")
        self.assertEqual(auth["authorized_next_phase"], "v656-v4")
        self.assertEqual(len(auth["authorized_route"]), 160)
        self.assertEqual(
            auth["authorized_route"][3],
            {"phase": "v656-v4", "seat": "Caelen Morrow"},
        )
        self.assertEqual(
            auth["authorized_route"][4],
            {"phase": "v656-v5", "seat": "Eiren Kestrel"},
        )
        self.assertEqual(
            auth["authorized_route"][5],
            {"phase": "v656-v6", "seat": "Elaren Kestrel"},
        )
        self.assertEqual(auth["authorized_route"][-1]["phase"], "v675-v8")

    def test_route_is_prepared_not_sent(self) -> None:
        truth = load("truth/phase-truth-final.json")
        route = load("orchestration/terminal-route-state.json")
        preparation = load("orchestration/successor-baton-preparation.json")
        self.assertEqual(truth["contact_count"], 0)
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT_TERMINAL_GATE")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(preparation["exact_title"], "Caelen Morrow")
        self.assertEqual(preparation["state"], "PREPARED_NOT_SENT")

    def test_sanitized_baton_contract(self) -> None:
        text = (
            PHASE / "handoffs/caelen-morrow-v656-v4-activation.md"
        ).read_text(encoding="utf-8")
        words = len(text.split())
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertIn("Caelen Morrow", text)
        self.assertIn("Eiren Kestrel", text)
        self.assertIn("Elaren Kestrel", text)
        self.assertIn("Tavian Sol", text)
        self.assertIn("v675-v8", text)
        self.assertIn("relational working language only", text)
        self.assertNotRegex(
            text,
            re.compile(
                r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
                r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
                re.I,
            ),
        )
        self.assertNotRegex(text, re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"))
        self.assertNotIn("source_thread_id", text)
        self.assertNotIn("private_callable", text)
        self.assertNotIn("session_stream", text)

    def test_manifest_and_staged_review_contracts(self) -> None:
        owner = load("validation/final-owner-manifest.json")
        delta = load("validation/final-staged-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertGreater(owner["entry_count"], 190)
        self.assertGreater(delta["entry_count"], 20)
        self.assertEqual(len(owner["self_exclusions"]), 3)
        self.assertEqual(len(delta["self_exclusions"]), 3)
        self.assertTrue(review["valid"])
        self.assertEqual(review["privacy_confirmed_hits"], [])
        self.assertEqual(review["json_errors"], [])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_evidence_paths_changed"], [])
        self.assertEqual(set(FINAL_CODE), set(review["missing_final_code_paths"]) | FINAL_CODE)
        self.assertEqual(review["missing_final_code_paths"], [])

    def test_closeout_candidate_and_seal_do_not_preclaim_final(self) -> None:
        candidate = load("validation/closeout-candidate-validation.json")
        closeout = load("closeout/closeout-receipt.json")
        seal = load("seal/seal-receipt.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertTrue(candidate["valid"])
        self.assertFalse(candidate["postcommit_canonical_pass_run"])
        self.assertFalse(closeout["postcommit_canonical_pass_completed"])
        self.assertTrue(seal["postcommit_exact_final_validation_required"])
        self.assertFalse(seal["exact_final_commit_known_inside_own_tree"])
        self.assertEqual(protocol["state"], "POSTCOMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["replay_after_success_allowed"])

    def test_no_evidence_or_x1_path_is_rewritten(self) -> None:
        rows = git("diff", "--name-status", EVIDENCE).splitlines()
        self.assertTrue(rows)
        for row in rows:
            status, _path = row.split("\t", 1)
            self.assertEqual(status, "A")
        self.assertEqual(git("rev-parse", f"{X1}:docs/sylven-arc/v656-v3/preregistration/proposals.json"), git("rev-parse", f"{EVIDENCE}:docs/sylven-arc/v656-v3/preregistration/proposals.json"))

    def test_terminal_boundaries_remain_false_or_zero(self) -> None:
        truth = load("truth/phase-truth-final.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        false_fields = [
            "accessibility_complete_claimed",
            "agi_or_asi_claimed",
            "consciousness_or_personhood_claimed",
            "exhaustive_security_claimed",
            "independent_reproduction_claimed",
            "privacy_complete_claimed",
            "professional_validation_claimed",
            "theory_of_everything_claimed",
        ]
        self.assertTrue(all(truth[field] is False for field in false_fields))
        zero_fields = [
            "real_people",
            "real_data_rows",
            "real_likelihoods",
            "real_keys_or_proofs",
            "live_identity_resolutions",
            "production_deployments",
            "authority_decisions",
            "cultural_or_community_decisions",
        ]
        self.assertTrue(all(truth[field] == 0 for field in zero_fields))


if __name__ == "__main__":
    unittest.main()
