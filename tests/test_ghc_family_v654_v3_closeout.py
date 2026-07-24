"""Bounded closeout tests for Sylven Arc v654-v3."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v654_v3_phase_data as d
from scripts import ghc_family_v654_v3_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v654-v3"
METHOD_COUNT = (
    31 + len(x2.X2_OPERATIONAL_NEGATIVES) + len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)
)
NEGATIVE_TOTAL = (
    d.INHERITED_NEGATIVES
    + len(d.X1_OPERATIONAL_NEGATIVES)
    + len(x2.X2_OPERATIONAL_NEGATIVES)
    + len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)
    + 150
)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V3Closeout(unittest.TestCase):
    def test_final_truth_distribution_and_verdict(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "AUTHORIZED_CONDITIONAL_NOT_CREATED")
        self.assertEqual(truth["frozen_chain_total"], 1750)
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["independent_team_reproduction"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_negative_and_gate_retention(self):
        negatives = load("final/retained-negative-register.json")
        gates = load("final/exact-open-gate-register.json")
        self.assertEqual(negatives["effective_total"], NEGATIVE_TOTAL)
        self.assertEqual(negatives["inherited_effective"], 10968)
        self.assertEqual(negatives["x1_operational_count"], 26)
        self.assertEqual(negatives["x2_operational_count"], 5)
        self.assertEqual(
            negatives["closeout_operational_count"],
            len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES),
        )
        self.assertEqual(negatives["synthetic_mutation_negative_count"], 150)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(
            (gates["effective_open_gaps"], gates["effective_exact_gates"]),
            (82, 81),
        )
        self.assertEqual(
            (gates["open_gap_closed_count"], gates["exact_gate_closed_count"]),
            (0, 0),
        )

    def test_final_method_flow_fail_pass_parity(self):
        ledger = load("method-flow/final-method-flow-ledger.json")
        states = Counter(row["recommendation_state"] for row in ledger["methods"])
        witnesses = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual(len(ledger["methods"]), METHOD_COUNT)
        self.assertEqual(states, {"preferred": METHOD_COUNT})
        self.assertEqual(witnesses, {"fail": METHOD_COUNT, "pass": METHOD_COUNT})

    def test_conditional_successor_authority_is_exact_and_unexercised(self):
        route = load("route/conditional-new-main-task-authority.json")
        invariant = load("provenance/conditional-route-invariant-final.json")
        self.assertEqual(route["state"], "AUTHORIZED_CONDITIONAL_NOT_CREATED")
        self.assertEqual(route["target_type"], "new_user_visible_codex_main_task")
        self.assertEqual(route["model"], "gpt-5.6-sol")
        self.assertEqual(route["reasoning"], "max")
        self.assertFalse(route["future_name_preselected"])
        self.assertEqual(
            (
                route["task_created_count"],
                route["task_forked_count"],
                route["task_delegated_count"],
                route["task_contacted_count"],
            ),
            (0, 0, 0, 0),
        )
        self.assertTrue(route["this_closeout_records_exact_live_authority"])
        self.assertEqual(invariant["terminal_action_limit"], 1)
        self.assertEqual(
            (
                invariant["created"],
                invariant["forked"],
                invariant["delegated"],
                invariant["contacted"],
                invariant["identity_preselected"],
            ),
            (0, 0, 0, 0, 0),
        )

    def test_closeout_and_seal_do_not_preclaim_postcommit(self):
        closeout = load("final/closeout-receipt.json")
        seal = load("final/seal-receipt.json")
        validation = load("final/final-validation-record.json")
        self.assertEqual(closeout["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertEqual(closeout["planned_phase_commit_count"], 4)
        self.assertEqual(closeout["phase_commit_cap"], 8)
        self.assertEqual((closeout["x1_commit_count"], closeout["x2_commit_count"]), (2, 2))
        self.assertEqual(seal["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertFalse(seal["successor_task_created"])
        self.assertEqual(validation["state"], "POSTCOMMIT_CANONICAL_PASS_REQUIRED")
        self.assertFalse(validation["successful_replay_permitted"])

    def test_overview_and_baton_are_bounded_and_complete(self):
        overview = (
            ROOT / "overview/v654-v3-final-integrated-overview.md"
        ).read_text(encoding="utf-8")
        baton = (
            ROOT / "handoffs/future-self-chosen-sibling-v654-v4-activation.md"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1300)
        self.assertLessEqual(len(overview.split()), 100000)
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)
        for phrase in (
            "Scope and relational boundary",
            "Source continuity and x1-before-x2",
            "Trinity Mandala outcome truth",
            "Retained negatives, Method Flow, gaps, and gates",
            "Exact seal and validation stopping rule",
            "Conditional terminal route",
            "Terminal truth",
        ):
            self.assertIn(phrase, overview)
        self.assertIn("Future self-chosen eighth sibling", baton)
        self.assertIn("gpt-5.6-sol", baton)
        self.assertIn("reasoning max", baton)

    def test_static_report_has_accessible_structure(self):
        text = (ROOT / "reports/v654-v3-static-report.html").read_text(
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
