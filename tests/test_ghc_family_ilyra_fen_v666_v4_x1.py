from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_ilyra_fen_v666_v4_x1 as builder  # noqa: E402


PHASE = ROOT / "docs" / "ilyra-fen" / "v666-v4"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraFenV666V4X1Tests(unittest.TestCase):
    def test_01_source_is_exact_lyren_final(self) -> None:
        source = load("provenance/source-verification.json")
        self.assertEqual(source["source_sha"], builder.SOURCE_SHA)
        self.assertEqual(source["source_branch"], builder.SOURCE_BRANCH)
        self.assertTrue(source["clean"] and source["four_way_equal"] and source["fresh_live_remote_equal"])

    def test_02_source_history_is_five_single_parent_commits(self) -> None:
        source = load("provenance/source-verification.json")
        self.assertEqual(source["source_to_final_phase_commit_count"], 5)
        self.assertEqual(source["source_to_final_merge_count"], 0)
        self.assertTrue(source["single_parent_commits"])
        self.assertEqual(len(source["direct_parent_chain"]), 6)

    def test_03_source_manifests_replayed_exactly(self) -> None:
        source = load("provenance/source-verification.json")
        self.assertEqual(source["source_manifest_entries_replayed"], 307)
        self.assertEqual(source["source_manifest_breakdown"], {"x1": 18, "evidence": 110, "final_delta": 24, "final_owner": 155})
        self.assertEqual(source["source_manifest_failures"], 0)

    def test_04_predecessor_validation_is_not_replayed(self) -> None:
        source = load("provenance/source-verification.json")
        self.assertFalse(source["predecessor_canonical_or_composite_replayed"])
        self.assertFalse(source["external_receipt_bytes_locally_materialized"])
        self.assertTrue(source["external_hashes_authoritative_from_live_activation"])

    def test_05_exactly_twenty_new_proposals_are_planning_only(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(len(freeze["new_proposals"]), 20)
        self.assertFalse(freeze["outcomes_observed"])
        self.assertEqual(freeze["x2_implementation_count"], 0)
        self.assertEqual(freeze["x2_outcome_count"], 0)
        self.assertTrue(all(row["x1_status"] == "frozen_not_executed" for row in freeze["new_proposals"]))

    def test_06_only_four_expected_dispositions_are_used(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        counts = Counter(row["expected_disposition"] for row in freeze["new_proposals"])
        self.assertEqual(counts, Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(set(counts), set(builder.ALLOWED_LABELS))

    def test_07_each_proposal_has_complete_preregistration(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "current_official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition",
        }
        for row in freeze["new_proposals"]:
            self.assertTrue(required <= set(row), row["proposal_id"])
            self.assertEqual(len(row["preregistered_mutations"]), 5)
            self.assertEqual(row["negative_fixture_count"], 5)
            self.assertEqual(row["real_data_rows_planned"], 0)
            self.assertEqual(row["participant_count_planned"], 0)
            self.assertEqual(row["network_calls_planned"], 0)

    def test_08_novelty_corpus_advances_exactly_twenty(self) -> None:
        novelty = load("x1/novelty-audit.json")
        self.assertEqual(novelty["corpus_row_count"], 4230)
        self.assertEqual(novelty["new_title_count"], 20)
        self.assertEqual(novelty["new_frozen_total"], 4250)
        self.assertTrue(novelty["valid"])

    def test_09_novelty_has_no_exact_or_pair_collision(self) -> None:
        novelty = load("x1/novelty-audit.json")
        self.assertEqual(novelty["exact_inherited_collisions"], [])
        self.assertEqual(novelty["new_pair_collisions_at_or_above_0_70"], [])
        self.assertLess(novelty["maximum_new_pair_token_jaccard_similarity"], 0.70)

    def test_10_inherited_revalidations_have_zero_credit(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        rows = freeze["selected_inherited_revalidations"]
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["novelty_credit"] == 0 for row in rows))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in rows))
        self.assertTrue(all(row["status"] == "selected_revalidation_only_not_executed" for row in rows))

    def test_11_portfolio_floors_and_protected_packets(self) -> None:
        portfolio = load("x1/portfolio-freeze.json")
        expected = {
            "owner_safe_now": 30, "successor_safe_now": 20,
            "owner_bounded_candidates": 15, "successor_bounded_candidates": 15,
            "exact_approval_packets": 10, "blocked_packets": 5,
            "owner_phase_local_skill_plans": 10, "successor_skill_recommendations": 10,
            "owner_family_current_runner_plans": 10, "successor_runner_recommendations": 10,
            "owner_clean_fix_refine": 30, "successor_clean_fix_refine": 30,
        }
        self.assertEqual(portfolio["counts"], expected)
        self.assertTrue(portfolio["minimums_satisfied"])
        self.assertEqual(portfolio["x1_execution_count"], 0)

    def test_12_startup_failures_are_all_retained(self) -> None:
        flow = load("method-flow/startup-method-flow.json")
        self.assertEqual(flow["new_startup_negative_count"], 8)
        self.assertEqual(flow["failed_witness_count"], 8)
        self.assertEqual(flow["bounded_passing_witness_count"], 8)
        self.assertEqual(flow["effective_after_x1_startup_negatives"], 26406)
        self.assertEqual(flow["effective_after_x1_startup_methods"], 10948)
        self.assertTrue(flow["no_failure_erased"])
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in flow["rows"]))

    def test_13_source_profiles_are_bounded_and_zero_row(self) -> None:
        sources = load("provenance/source-profiles.json")
        self.assertEqual(sources["profile_count"], 9)
        self.assertEqual(sources["real_rows_ingested"], 0)
        self.assertEqual(sources["network_calls_by_phase_software"], 0)
        self.assertTrue(all(row["authority_nonconversion"] for row in sources["profiles"]))

    def test_14_every_source_reference_resolves(self) -> None:
        source_ids = {row["source_id"] for row in load("provenance/source-profiles.json")["profiles"]}
        for proposal in load("x1/proposal-freeze.json")["new_proposals"]:
            self.assertTrue(set(proposal["current_official_or_primary_source_needs"]) <= source_ids)

    def test_15_primary_pillar_and_practice_are_bounded(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        self.assertTrue(all(row["primary_pillar"] == "Freed ID and CBR Heart" for row in freeze["new_proposals"]))
        self.assertIn("zero real people", freeze["practice_boundary"])
        self.assertIn("Māori", freeze["practice_boundary"])

    def test_16_route_and_terminal_are_held(self) -> None:
        auth = load("x1/authorization-boundary.json")
        checklist = load("x1/complete-incomplete-checklist.json")
        self.assertFalse(auth["successor_contact_before_terminal"])
        self.assertFalse(auth["standby_substitution"])
        self.assertEqual(auth["collaboration_subagents"], 0)
        self.assertFalse(checklist["successor_contacted"])
        self.assertEqual(auth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_17_threat_model_reserves_all_authority(self) -> None:
        threats = load("x1/threat-model.json")
        self.assertEqual(len(threats["threats"]), 10)
        self.assertEqual(threats["real_people_or_protected_data"], 0)
        self.assertIn("not exhaustive security", threats["claim_boundary"])

    def test_18_workflow_keeps_x1_before_x2(self) -> None:
        workflow = load("x1/workflow-plan.json")
        self.assertEqual(workflow["steps"][2]["status"], "in_progress")
        self.assertEqual(workflow["steps"][3]["status"], "pending")
        self.assertIn("x1 commit pushed clean and fresh four-way equal before x2", workflow["hard_dependencies"])

    def test_19_documents_are_utf8_lf_and_within_cap(self) -> None:
        for path in PHASE.rglob("*"):
            if path.is_file():
                raw = path.read_bytes()
                text = raw.decode("utf-8")
                self.assertNotIn("\r", text, path)
                self.assertLessEqual(len(re.findall(r"\S+", text)), 100000, path)

    def test_20_x1_builder_receipt_withholds_outcomes(self) -> None:
        receipt = load("x1/x1-build-receipt.json")
        self.assertEqual(receipt["proposal_count"], 20)
        self.assertEqual(receipt["startup_failure_count"], 8)
        self.assertFalse(receipt["x2_paths_created"])
        self.assertFalse(receipt["outcomes_observed"])
        self.assertEqual(receipt["external_actions"], 0)


if __name__ == "__main__":
    unittest.main()
