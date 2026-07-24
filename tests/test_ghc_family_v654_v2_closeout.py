"""Bounded closeout tests for Elowen Cairn v654-v2."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elowen-cairn/v654-v2"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V2Closeout(unittest.TestCase):
    def test_final_truth_distribution_and_verdict(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "NO_SUCCESSOR_AUTHORIZED")
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["independent_team_reproduction"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_negative_and_gate_retention(self):
        negatives = load("final/retained-negative-register.json")
        gates = load("final/exact-open-gate-register.json")
        self.assertEqual(negatives["effective_total"], 10963)
        self.assertEqual(negatives["inherited_effective"], 10797)
        self.assertEqual(negatives["x1_operational_count"], 13)
        self.assertEqual(negatives["x2_and_closeout_operational_count"], 3)
        self.assertEqual(negatives["synthetic_mutation_negative_count"], 150)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(
            (gates["effective_open_gaps"], gates["effective_exact_gates"]),
            (79, 80),
        )
        self.assertEqual(
            (gates["open_gap_closed_count"], gates["exact_gate_closed_count"]),
            (0, 0),
        )

    def test_final_method_flow_fail_pass_parity(self):
        ledger = load("method-flow/final-method-flow-ledger.json")
        states = Counter(row["recommendation_state"] for row in ledger["methods"])
        witnesses = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual(len(ledger["methods"]), 20)
        self.assertEqual(states, {"preferred": 20})
        self.assertEqual(witnesses, {"fail": 20, "pass": 20})

    def test_successor_is_not_authorized_or_prepared(self):
        route = load("route/no-successor-authorized.json")
        invariant = load("provenance/no-successor-invariant-final.json")
        self.assertEqual(route["state"], "NO_SUCCESSOR_AUTHORIZED")
        self.assertIsNone(route["successor_title"])
        self.assertIsNone(route["successor_placeholder"])
        self.assertEqual(
            (
                route["task_created_count"],
                route["task_forked_count"],
                route["task_delegated_count"],
                route["task_contacted_count"],
            ),
            (0, 0, 0, 0),
        )
        self.assertFalse(route["this_closeout_authorizes_successor"])
        self.assertEqual(
            (
                invariant["created"],
                invariant["forked"],
                invariant["delegated"],
                invariant["contacted"],
                invariant["prepared"],
                invariant["titled"],
            ),
            (0, 0, 0, 0, 0, 0),
        )

    def test_closeout_and_seal_do_not_preclaim_postcommit(self):
        closeout = load("final/closeout-receipt.json")
        seal = load("final/seal-receipt.json")
        validation = load("final/final-validation-record.json")
        self.assertEqual(closeout["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertEqual(closeout["planned_phase_commit_count"], 3)
        self.assertEqual(seal["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertFalse(seal["successor_task_created"])
        self.assertEqual(validation["state"], "POSTCOMMIT_CANONICAL_PASS_REQUIRED")
        self.assertFalse(validation["successful_replay_permitted"])

    def test_overview_is_bounded_and_complete(self):
        text = (
            ROOT / "overview/v654-v2-final-integrated-overview.md"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1000)
        self.assertLessEqual(len(text.split()), 6000)
        for phrase in (
            "Scope and relational boundary",
            "Source continuity and x1-before-x2",
            "Trinity Mandala truth",
            "Retained negatives, open gaps, and exact gates",
            "Validation and stopping rule",
            "Terminal truth",
        ):
            self.assertIn(phrase, text)

    def test_static_report_has_accessible_structure(self):
        text = (ROOT / "reports/v654-v2-static-report.html").read_text(
            encoding="utf-8"
        )
        for token in (
            "<main>",
            "<h1>",
            'scope="col"',
            'scope="row"',
            'aria-label="Scrollable proposal outcomes"',
            'tabindex="0"',
            "prefers-reduced-motion",
            "@media print",
        ):
            self.assertIn(token, text)

    def test_final_manifests_and_privacy_are_exact(self):
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        review = load("validation/final-staged-review.json")
        privacy = load("validation/final-privacy-receipt.json")
        self.assertEqual(delta["entry_count"], len(delta["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))
        self.assertEqual(len(delta["self_exclusions"]), 4)
        self.assertEqual(len(owner["self_exclusions"]), 4)
        self.assertTrue(review["valid"])
        self.assertEqual(review["privacy_confirmed_hit_count"], 0)
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_checklist_preserves_external_incompleteness(self):
        checklist = load("final/complete-incomplete-checklist.json")
        self.assertTrue(checklist["complete_bounded"])
        self.assertTrue(checklist["pending_postcommit"])
        self.assertTrue(checklist["incomplete_external"])
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_owner_json_parses(self):
        paths = sorted(ROOT.rglob("*.json"))
        self.assertGreater(len(paths), 200)
        for path in paths:
            with self.subTest(path=path.relative_to(REPO).as_posix()):
                json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
