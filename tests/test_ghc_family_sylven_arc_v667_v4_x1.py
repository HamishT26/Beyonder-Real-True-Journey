"""Owner-local planning-only checks for Sylven Arc v667-v4 x1."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class TestSylvenArcV667V4X1(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.charter = load("x1/phase-charter.json")
        cls.source = load("x1/source-verification.json")
        cls.ledger = load("x1/source-ledger.json")
        cls.freeze = load("x1/proposal-freeze.json")
        cls.novelty = load("x1/novelty-audit.json")
        cls.portfolio = load("x1/portfolio-freeze.json")
        cls.architecture = load("x1/flashcard-architecture-freeze.json")
        cls.flow = load("method-flow/startup-method-flow.json")
        cls.identity = load("identity/relational-identity.json")
        cls.checklist = load("x1/complete-incomplete-checklist.json")
        cls.build = load("x1/x1-build-receipt.json")

    def test_phase_and_source_are_exact(self) -> None:
        self.assertEqual(self.charter["canonical_phase_id"], "v667-v4")
        self.assertEqual(self.charter["owner"], "Sylven Arc")
        self.assertEqual(
            self.source["source_exact_final"],
            "9625026b09860c8964dd818e8d1f81ee6e2eed57",
        )
        self.assertTrue(self.source["source_direct_chain_valid"])
        self.assertTrue(self.source["source_four_way_equal"])
        self.assertEqual(self.source["source_to_final_commit_count"], 3)
        self.assertEqual(self.source["source_to_final_merge_count"], 0)
        self.assertFalse(self.source["failed_canonical_replayed"])
        self.assertFalse(self.source["successful_composite_replayed"])

    def test_x1_has_twenty_new_and_no_selected_inherited_rows(self) -> None:
        self.assertEqual(self.freeze["inherited_proposal_count"], 4390)
        self.assertEqual(self.freeze["selected_inherited_count"], 0)
        self.assertEqual(self.freeze["selected_inherited"], [])
        self.assertEqual(self.freeze["genuinely_new_proposal_count"], 20)
        self.assertEqual(len(self.freeze["new_proposals"]), 20)
        self.assertEqual(self.freeze["new_frozen_total"], 4410)

    def test_expected_outcome_partition_is_exact(self) -> None:
        expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(self.freeze["expected_outcomes"], expected)
        observed = Counter(row["expected_disposition"] for row in self.freeze["new_proposals"])
        self.assertEqual(dict(observed), expected)

    def test_each_proposal_has_the_full_contract(self) -> None:
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifact",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
            "distinctive_invariant",
        }
        ids = []
        for row in self.freeze["new_proposals"]:
            self.assertTrue(required.issubset(row))
            self.assertTrue(all(row[key] for key in required))
            self.assertEqual(row["x1_status"], "frozen_not_executed")
            self.assertEqual(row["x2_implementation_count"], 0)
            self.assertFalse(row["outcomes_observed"])
            self.assertEqual(row["network_calls_planned"], 0)
            self.assertEqual(row["participant_count_planned"], 0)
            self.assertEqual(row["real_data_rows_planned"], 0)
            ids.append(row["proposal_id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_proposal_freezes_five_distinct_rejecting_mutations(self) -> None:
        expected_classes = {
            "missing_required_field",
            "wrong_type_or_invalid_range",
            "provenance_or_authority_smuggling",
            "real_world_or_production_action",
            "outcome_or_conformance_promotion",
        }
        mutation_ids = []
        for row in self.freeze["new_proposals"]:
            mutations = row["preregistered_mutations"]
            self.assertEqual(len(mutations), 5)
            self.assertEqual({item["class"] for item in mutations}, expected_classes)
            mutation_ids.extend(item["mutation_id"] for item in mutations)
        self.assertEqual(len(mutation_ids), 100)
        self.assertEqual(len(mutation_ids), len(set(mutation_ids)))

    def test_semantic_novelty_audit_is_complete_and_bounded(self) -> None:
        self.assertTrue(self.novelty["valid"])
        self.assertEqual(self.novelty["corpus_row_count"], 4390)
        self.assertEqual(self.novelty["corpus_unique_proposal_id_count"], 4370)
        self.assertEqual(self.novelty["corpus_duplicate_proposal_id_count"], 20)
        self.assertEqual(self.novelty["corpus_duplicate_occurrence_overage"], 20)
        self.assertEqual(len(self.novelty["corpus_duplicate_proposal_ids"]), 20)
        self.assertEqual(self.novelty["new_proposal_count"], 20)
        self.assertEqual(self.novelty["new_frozen_total"], 4410)
        self.assertEqual(self.novelty["exact_title_collisions"], [])
        self.assertEqual(self.novelty["pair_collisions_at_or_above_0_25"], [])
        self.assertEqual(self.novelty["domain_review"]["exact_neon_term_match_count"], 0)
        self.assertLess(self.novelty["maximum_inherited_similarity"], 0.6)
        self.assertEqual(self.novelty["high_similarity_reviews"], [])
        self.assertEqual(len(self.novelty["nearest_inherited_matches"]), 20)
        self.assertEqual(len(self.novelty["rejected_draft_proposals"]), 4)

    def test_portfolio_counts_and_contract_fields_are_exact(self) -> None:
        counts = {
            "owner_safe_now": 30,
            "successor_safe_now_recommendations": 20,
            "owner_candidates": 15,
            "successor_candidate_recommendations": 15,
            "exact_approval_packets": 10,
            "blocked_packets": 5,
            "owner_skill_ideas": 10,
            "successor_skill_recommendations": 10,
            "owner_runner_ideas": 10,
            "successor_runner_recommendations": 10,
            "owner_clean_fix_refine": 30,
            "successor_clean_fix_refine_recommendations": 30,
        }
        required = {
            "portfolio_ref",
            "title",
            "approval_class",
            "execution_lane",
            "expected_execution_disposition",
            "credit_boundary",
        }
        references = []
        for group, count in counts.items():
            rows = self.portfolio[group]
            self.assertEqual(len(rows), count, group)
            for row in rows:
                self.assertTrue(required.issubset(row), (group, row))
                self.assertEqual(row["x1_status"], "planned_not_executed")
                self.assertEqual(row["completion_credit"], 0)
                references.append(row["portfolio_ref"])
        self.assertEqual(len(references), len(set(references)))
        self.assertEqual(self.portfolio["x2_implementation_count"], 0)
        self.assertFalse(self.portfolio["outcomes_observed"])

    def test_flashcard_architecture_freezes_four_tiers_and_thirteen_sections(self) -> None:
        self.assertEqual(
            self.architecture["four_tiers"],
            ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        )
        self.assertEqual(len(self.architecture["required_deck_sections"]), 13)
        self.assertEqual(len(set(self.architecture["required_deck_sections"])), 13)
        self.assertFalse(self.architecture["cache_effect_measured"])
        self.assertFalse(self.architecture["identity_continuity_claim"])
        self.assertTrue(self.architecture["x1_planning_only"])
        self.assertFalse(self.architecture["successor_route"]["contacted"])

    def test_startup_method_flow_retains_every_failure_and_recovery(self) -> None:
        self.assertEqual(self.flow["inherited_effective_negatives"], 27337)
        self.assertEqual(self.flow["inherited_effective_methods"], 12799)
        self.assertEqual(self.flow["startup_failed_method_count"], 26)
        self.assertEqual(self.flow["effective_x1_baseline_negatives"], 27363)
        self.assertEqual(self.flow["effective_x1_baseline_methods"], 12825)
        self.assertEqual(len(self.flow["failed_witnesses"]), 26)
        self.assertEqual(len(self.flow["passing_witnesses"]), 26)
        self.assertTrue(all(not row["erased"] for row in self.flow["failed_witnesses"]))
        self.assertTrue(all(row["outcome"] == "failed_retained_zero_credit" for row in self.flow["failed_witnesses"]))
        self.assertTrue(all(not row["promotes_failed_witness"] for row in self.flow["passing_witnesses"]))

    def test_identity_and_practice_boundaries_are_explicit(self) -> None:
        text = json.dumps(self.identity, ensure_ascii=False).casefold()
        for token in ("relational", "not evidence of consciousness", "māori", "no real people"):
            self.assertIn(token, text)
        self.assertEqual(self.charter["primary_pillar"], "THOS Body")
        self.assertIn("neon-signmaking", self.charter["bounded_practice"])
        self.assertEqual(self.charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_sources_are_bounded_and_current_read_only_inputs(self) -> None:
        sources = self.ledger["sources"]
        self.assertEqual(len(sources), 11)
        self.assertEqual(len({row["source_id"] for row in sources}), 11)
        for row in sources:
            self.assertTrue(row["url"].startswith("https://"))
            self.assertTrue(row["bounded_use"])
            self.assertIn("2026-08-23", row["status"])
        serialized = json.dumps(self.ledger, ensure_ascii=False).casefold()
        self.assertIn("zero downloaded spectral rows", serialized)
        self.assertIn("zero-call zero-row adapter", serialized)

    def test_x1_build_receipt_and_checklist_are_planning_only(self) -> None:
        self.assertEqual(self.build["status"], "FROZEN_NOT_EXECUTED")
        self.assertEqual(self.build["new_proposal_count"], 20)
        self.assertEqual(self.build["startup_failure_count"], 26)
        self.assertEqual(self.build["x2_implementation_count"], 0)
        self.assertFalse(self.build["outcomes_observed"])
        self.assertTrue(self.build["valid"])
        serialized = json.dumps(self.checklist, ensure_ascii=False)
        self.assertIn("NOT_READY_FOR_STAGE_20", serialized)

    def test_no_x2_directory_or_outcome_artifact_exists(self) -> None:
        self.assertFalse((PHASE_ROOT / "x2").exists())
        files = [path.relative_to(PHASE_ROOT).as_posix() for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertFalse(any(path.startswith("x2/") for path in files))
        self.assertTrue(self.freeze["x1_planning_only"])
        self.assertEqual(self.freeze["x2_implementation_count"], 0)
        self.assertFalse(self.freeze["outcomes_observed"])

    def test_overview_is_structured_and_not_a_completion_claim(self) -> None:
        overview = (PHASE_ROOT / "x1" / "x1-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(overview.count("\n## "), 10)
        self.assertIn("planning-only", overview.casefold())
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertNotIn("Stage 20 ready", overview)


if __name__ == "__main__":
    unittest.main()
