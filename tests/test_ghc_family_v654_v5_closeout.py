"""Bounded closeout tests for Eiren Kestrel v654-v5."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v5"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
ROUTE_STATE = "PREPARED_NOT_SENT_ROUTE_UNRESOLVED"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V5Closeout(unittest.TestCase):
    def test_phase_truth(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcomes"], EXPECTED)
        self.assertEqual(truth["frozen_chain_total"], 1810)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], ROUTE_STATE)
        self.assertEqual(truth["canonical_exact_final_pass_state"], "PENDING_POSTCOMMIT")
        self.assertFalse(truth["independent_team_reproduction"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_retained_negatives(self):
        negatives = load("final/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 11322)
        self.assertEqual(negatives["x1_operational_count"], 8)
        self.assertEqual(negatives["x2_operational_count"], 0)
        self.assertEqual(negatives["closeout_operational_count"], 6)
        self.assertEqual(negatives["synthetic_mutation_negative_count"], 150)
        self.assertEqual(negatives["effective_total"], 11486)
        self.assertTrue(negatives["no_failure_erased"])

    def test_open_and_exact_gates(self):
        gates = load("final/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 84)
        self.assertEqual(gates["effective_exact_gates"], 83)
        self.assertEqual(gates["open_gap_closed_count"], 0)
        self.assertEqual(gates["exact_gate_closed_count"], 0)

    def test_method_flow_parity(self):
        ledger = load("method-flow/final-method-flow-ledger.json")
        states = Counter(row["recommendation_state"] for row in ledger["methods"])
        witnesses = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual(len(ledger["methods"]), 73)
        self.assertEqual(states, {"preferred": 73})
        self.assertEqual(witnesses, {"fail": 73, "pass": 73})
        closeout_ids = {
            item
            for row in ledger["methods"]
            for item in row.get("retained_negative_ids", [])
            if item.startswith("V6545-CLOSEOUT-")
        }
        self.assertEqual(
            closeout_ids,
            {
                "V6545-CLOSEOUT-N01",
                "V6545-CLOSEOUT-N02",
                "V6545-CLOSEOUT-N03",
                "V6545-CLOSEOUT-N04",
                "V6545-CLOSEOUT-N05",
                "V6545-CLOSEOUT-N06",
            },
        )

    def test_outcomes_and_mutations(self):
        outcomes = load("evidence/outcome-ledger.json")
        self.assertEqual(outcomes["counts"], EXPECTED)
        self.assertEqual(outcomes["mutation_rejected_total"], 150)
        self.assertTrue(all(row["acceptance_gate_passed"] for row in outcomes["rows"]))

    def test_exact_existing_task_route(self):
        route = load("route/terminal-existing-task-baton.json")
        self.assertEqual(route["state"], ROUTE_STATE)
        self.assertIsNone(route["recipient_title"])
        self.assertEqual(route["target_type"], "unresolved_existing_task_route")
        self.assertTrue(route["existing_task_only"])
        self.assertEqual(
            (
                route["task_created_count"],
                route["task_forked_count"],
                route["task_delegated_count"],
                route["task_contacted_count"],
            ),
            (0, 0, 0, 0),
        )
        self.assertEqual(route["message_limit"], 0)
        self.assertFalse(route["duplicate_confirmation_permitted"])

    def test_route_invariant(self):
        invariant = load("provenance/terminal-route-invariant-final.json")
        self.assertEqual(invariant["route_state"], ROUTE_STATE)
        self.assertIsNone(invariant["recipient_title"])
        self.assertEqual(
            (
                invariant["created"],
                invariant["forked"],
                invariant["delegated"],
                invariant["contacted"],
            ),
            (0, 0, 0, 0),
        )
        self.assertTrue(invariant["exact_existing_task_only"])
        self.assertEqual(invariant["terminal_message_limit"], 0)

    def test_baton_length_and_sanitized_state(self):
        baton = (
            ROOT / "handoffs/v654-v6-route-unresolved.md"
        ).read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("Eiren Kestrel", baton)
        self.assertIn(ROUTE_STATE, baton)
        self.assertNotIn("source_" + "thread_id", baton.casefold())
        self.assertNotIn("new user-visible main task", baton.casefold())

    def test_content_seal_does_not_preclaim_postcommit_facts(self):
        seal = load("final/seal-receipt.json")
        self.assertEqual(seal["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertFalse(seal["successor_task_created"])
        self.assertFalse(seal["successor_task_contacted"])
        self.assertIn("containing commit identifier", seal["postcommit_facts_not_preclaimed"])
        self.assertIn("unresolved-route retention at zero messages", seal["postcommit_facts_not_preclaimed"])

    def test_staged_manifests_and_privacy(self):
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        privacy = load("validation/final-staged-privacy.json")
        review = load("validation/final-staged-review.json")
        self.assertEqual(delta["entry_count"], len(delta["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))
        self.assertEqual(len(delta["self_exclusions"]), 5)
        self.assertEqual(len(owner["self_exclusions"]), 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(review["valid"])
        self.assertFalse(review["canonical_final_pass_run"])

    def test_document_and_owner_caps(self):
        documents = load("validation/document-cap-final.json")
        owners = load("validation/owner-file-threshold-final.json")
        self.assertTrue(documents["valid"])
        self.assertTrue(owners["valid"])
        self.assertLessEqual(documents["maximum_document"]["words"], 100000)
        self.assertLessEqual(owners["owner_file_count_before_lifecycle_manifests"], 2000)

    def test_stale_labels_and_diff_hygiene(self):
        stale = load("validation/stale-label-review-final.json")
        hygiene = load("validation/final-diff-hygiene.json")
        self.assertTrue(stale["valid"])
        self.assertEqual(stale["matches"], [])
        self.assertTrue(hygiene["valid"])
        self.assertEqual(hygiene["out_of_scope_paths"], [])
        self.assertEqual(hygiene["sibling_document_paths"], [])
        self.assertEqual(hygiene["x1_document_paths_changed"], [])
        self.assertEqual(hygiene["evidence_artifact_paths_changed"], [])

    def test_complete_incomplete_truth(self):
        checklist = load("final/complete-incomplete-checklist.json")
        self.assertIn("run one successful canonical full-repository pass", checklist["pending_postcommit"])
        self.assertIn(
            "retain the unresolved successor route without creating or contacting a task",
            checklist["pending_postcommit"],
        )
        self.assertIn(
            "real GMUT data, likelihoods, constraints, and independent review",
            checklist["incomplete_external"],
        )
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_validation_protocol(self):
        protocol = load("validation/final-validation-protocol.json")
        self.assertEqual(protocol["canonical_success_limit"], 1)
        self.assertFalse(protocol["post_success_replay_permitted"])
        self.assertTrue(protocol["full_repository_suite_required"])
        self.assertFalse(protocol["broad_test_exclusions_permitted"])
        self.assertEqual(
            protocol[
                "full_repository_suite_exact_lifecycle_exclusion_count"
            ],
            39,
        )
        self.assertEqual(len(protocol["current_and_source_test_modules"]), 6)
        self.assertIn("post-success replay", protocol["excluded"])


if __name__ == "__main__":
    unittest.main()
