from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_x1 as builder


PHASE = ROOT / "docs/sable-rook/v664-v7"


def load(relative: str):
    raw = (PHASE / relative).read_bytes()
    return builder.strict_json(raw, relative)


class SableV664V7X1Tests(unittest.TestCase):
    def test_exact_source_anchors(self):
        source = load("x1/source-verification.json")
        self.assertTrue(source["valid"])
        self.assertEqual(source["source_final"], builder.SOURCE_FINAL)
        self.assertEqual(source["source_to_final_commit_count"], 3)
        self.assertEqual(source["source_to_final_merge_count"], 0)
        self.assertEqual(source["manifest_replay"]["entries"], 820)
        self.assertEqual(source["manifest_replay"]["mismatches"], 0)

    def test_corpus_and_novelty(self):
        audit = load("x1/novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["corpus_row_count"], 3_970)
        self.assertEqual(audit["new_title_count"], 20)
        self.assertEqual(audit["exact_inherited_collisions"], [])
        self.assertEqual(audit["new_pair_collisions_at_or_above_0_70"], [])
        self.assertLess(audit["maximum_inherited_token_jaccard_similarity"], 0.60)
        self.assertEqual(audit["practice_term_checks"]["microfilm_title_count_in_inherited_corpus"], 0)
        self.assertEqual(audit["practice_term_checks"]["microfiche_title_count_in_inherited_corpus"], 0)

    def test_proposal_freeze_is_planning_only(self):
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(freeze["inherited_frozen_baseline"], 3_970)
        self.assertEqual(freeze["new_frozen_total"], 3_990)
        self.assertEqual(freeze["new_proposal_count"], 20)
        self.assertEqual(freeze["new_expected_outcomes"], {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4})
        self.assertFalse(freeze["observed_outcomes_present"])
        self.assertFalse(freeze["x2_implementation_present"])
        self.assertEqual({row["expected_disposition"] for row in freeze["new_proposals"]}, builder.ALLOWED_OUTCOMES)

    def test_inherited_rows_receive_zero_credit(self):
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(len(freeze["selected_inherited"]), 20)
        self.assertEqual(freeze["selected_inherited_novelty_credit"], 0)
        self.assertEqual(freeze["selected_inherited_automatic_completion_credit"], 0)
        self.assertEqual(freeze["selected_inherited_new_outcome_credit"], 0)
        for row in freeze["selected_inherited"]:
            self.assertFalse(row["novelty_credit"])
            self.assertFalse(row["automatic_completion_credit"])
            self.assertFalse(row["sable_new_outcome_credit"])

    def test_each_new_proposal_has_required_fields(self):
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition",
            "approval_class", "execution_lane", "current_official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery",
            "protected_gates", "expected_disposition", "novelty_credit",
        }
        for row in load("x1/proposal-freeze.json")["new_proposals"]:
            self.assertTrue(required.issubset(row))
            self.assertEqual(row["protected_gates"], builder.PROTECTED_GATES)
            self.assertTrue(row["novelty_credit"])
            self.assertEqual(len(row["concrete_artifacts"]), 3)

    def test_source_ledger_is_zero_observation(self):
        ledger = load("x1/source-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["source_count"], 11)
        self.assertEqual({row["status"] for row in ledger["sources"]}, {"current", "stable", "watch"})
        self.assertTrue(all(row["live_data_calls"] == 0 for row in ledger["sources"]))
        self.assertTrue(all(row["downloaded_microform_rows"] == 0 for row in ledger["sources"]))
        self.assertTrue(all(row["target_measurements"] == 0 for row in ledger["sources"]))

    def test_portfolio_floor_and_protected_packets(self):
        portfolio = load("x1/portfolio-freeze.json")
        self.assertTrue(portfolio["valid"])
        expected = {
            "owner_safe_now": 30, "owner_candidates": 15, "owner_skill_ideas": 10,
            "owner_runner_ideas": 10, "owner_clean_fix_refine": 30,
            "exact_approval_packets": 10, "blocked_packets": 5,
            "successor_safe_now_recommendations": 20,
            "successor_candidate_recommendations": 15,
            "successor_skill_recommendations": 10,
            "successor_runner_recommendations": 10,
            "successor_clean_fix_refine_recommendations": 30,
        }
        self.assertEqual(portfolio["counts"], expected)
        self.assertTrue(all(row["status"] == "unexecuted" for row in portfolio["exact_approval_packets"]))
        self.assertTrue(all(row["status"] == "unexecuted" for row in portfolio["blocked_packets"]))

    def test_method_flow_retains_failures(self):
        flow = load("x1/startup-method-flow.json")
        self.assertTrue(flow["valid"])
        self.assertEqual(flow["failure_erasure_count"], 0)
        self.assertGreaterEqual(flow["new_method_count"], 13)
        self.assertEqual(flow["new_failed_witness_count"], flow["new_method_count"])
        self.assertEqual(flow["new_passing_witness_count"], flow["new_method_count"])
        self.assertTrue(all(row["failed_witness_credit"] == "zero" for row in flow["methods"]))

    def test_charter_boundaries_and_caps(self):
        charter = load("x1/phase-charter.json")
        self.assertTrue(charter["valid"])
        self.assertEqual(charter["owner"], "Sable Rook")
        self.assertEqual(charter["allowed_truth_labels"], sorted(builder.ALLOWED_OUTCOMES))
        self.assertEqual(charter["owned_lane"]["owner_file_ceiling"], 2_000)
        self.assertFalse(charter["owned_lane"]["private_absolute_path_recorded"])
        self.assertEqual(charter["successor"]["state"], "PREPARED_NOT_SENT")
        self.assertEqual(charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_threat_and_workflow_gates(self):
        threat = load("x1/threat-model-plan.json")
        plan = load("x1/workflow-plan.json")
        self.assertTrue(threat["valid"])
        self.assertEqual(len(threat["threats"]), 12)
        self.assertTrue(plan["valid"])
        statuses = {row["step_id"]: row["status"] for row in plan["steps"]}
        self.assertEqual(statuses["P5"], "blocked_until_x1_remote_equal")
        self.assertEqual(statuses["P8"], "blocked_until_terminal_gate")

    def test_flashcard_floor(self):
        cards = load("x1/flashcard-architecture-freeze.json")
        self.assertTrue(cards["valid"])
        self.assertGreaterEqual(cards["section_count"], 10)
        self.assertFalse(cards["x2_content_present"])

    def test_overview_preserves_nonpromotion(self):
        text = (PHASE / "x1/x1-overview.md").read_text(encoding="utf-8")
        for phrase in (
            "NOT_READY_FOR_STAGE_20", "planning-only", "no x2 implementation",
            "not evidence of consciousness", "Maori concepts remain under Maori authority",
            "zero phase observations", "PREPARED_NOT_SENT",
        ):
            self.assertIn(phrase, text)

    def test_all_written_x1_json_is_strict(self):
        paths = sorted((PHASE / "x1").glob("*.json"))
        self.assertGreaterEqual(len(paths), 9)
        for path in paths:
            builder.strict_json(path.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
