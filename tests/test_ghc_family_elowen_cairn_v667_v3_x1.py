from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class ElowenCairnV667V3X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load("x1/proposal-freeze.json")
        cls.novelty = load("x1/novelty-audit.json")
        cls.portfolios = load("x1/portfolio-freeze.json")
        cls.source = load("x1/source-verification.json")
        cls.method = load("method-flow/startup-method-flow.json")

    def test_01_exact_twenty_new_proposals(self):
        self.assertEqual(len(self.freeze["new_proposals"]), 20)
        self.assertEqual(self.freeze["genuinely_new_proposal_count"], 20)

    def test_02_ids_are_unique_and_exact(self):
        ids = [row["proposal_id"] for row in self.freeze["new_proposals"]]
        self.assertEqual(ids, [f"EC6673-N{i:03d}" for i in range(1, 21)])

    def test_03_every_required_field_is_present(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in self.freeze["new_proposals"]:
            self.assertFalse(required - set(row), row["proposal_id"])

    def test_04_only_four_expected_labels_are_used(self):
        labels = {row["expected_disposition"] for row in self.freeze["new_proposals"]}
        self.assertEqual(labels, {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(
            self.freeze["expected_disposition_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )

    def test_05_x1_has_no_observed_outcome_or_implementation(self):
        self.assertFalse(self.freeze["outcomes_observed"])
        self.assertEqual(self.freeze["x2_implementation_count"], 0)
        self.assertTrue(
            all(not row["outcomes_observed"] and row["x2_implementation_count"] == 0 for row in self.freeze["new_proposals"])
        )
        self.assertFalse((PHASE_ROOT / "x2").exists())

    def test_06_each_proposal_has_five_named_mutations(self):
        for row in self.freeze["new_proposals"]:
            self.assertEqual(row["negative_fixture_count"], 5)
            self.assertEqual(len(row["preregistered_mutations"]), 5)
            self.assertEqual(len({m["mutation_id"] for m in row["preregistered_mutations"]}), 5)

    def test_07_novelty_corpus_is_exact(self):
        self.assertEqual(self.novelty["corpus_row_count"], 4370)
        self.assertEqual(self.novelty["new_frozen_total"], 4390)
        self.assertTrue(self.novelty["valid"])

    def test_08_no_novelty_collisions(self):
        self.assertEqual(self.novelty["exact_title_collisions"], [])
        self.assertEqual(self.novelty["pair_collisions_at_or_above_0_25"], [])
        self.assertLess(self.novelty["maximum_inherited_similarity"], 0.5)

    def test_09_change_ringing_distinction_is_explicit(self):
        review = self.novelty["domain_review"]
        self.assertIn("change-ringing", review["nearest_relevant_prior_phase"])
        self.assertIn("foundry", review["substantive_distinction"])

    def test_10_source_anchors_and_chain_are_exact(self):
        self.assertTrue(self.source["valid"])
        self.assertEqual(self.source["source_to_final_commit_count"], 3)
        self.assertEqual(self.source["source_to_final_merge_count"], 0)
        self.assertEqual(self.source["final_parent_count"], 1)
        self.assertTrue(self.source["direct_chain_valid"])

    def test_11_source_canonical_is_not_replayed(self):
        self.assertFalse(self.source["source_successful_canonical_replayed"])
        self.assertEqual(self.source["source_canonical_summary"]["attributable_tests"], 102)
        self.assertEqual(self.source["source_manifest_replay"]["mismatches"], 0)

    def test_12_portfolio_minimums_are_frozen(self):
        self.assertTrue(self.portfolios["frozen"])
        self.assertTrue(self.portfolios["minimums_satisfied"])
        self.assertEqual(self.portfolios["x1_execution_count"], 0)
        self.assertEqual(self.portfolios["counts"]["owner_safe_now"], 30)
        self.assertEqual(self.portfolios["counts"]["successor_safe_now"], 20)
        self.assertEqual(self.portfolios["counts"]["owner_clean_fix_refine"], 30)
        self.assertEqual(self.portfolios["counts"]["successor_clean_fix_refine"], 30)

    def test_13_exact_and_blocked_packets_are_unexecuted(self):
        for key in ("exact_approval_packets", "blocked_packets"):
            for row in self.portfolios["portfolios"][key]:
                self.assertEqual(row["x1_status"], "planned_not_executed")
                self.assertEqual(row["completion_credit"], 0)

    def test_14_startup_failures_and_recoveries_are_retained(self):
        self.assertEqual(self.method["activation_overlay_failed_method_count"], 6)
        self.assertEqual(len(self.method["failed_witnesses"]), 6)
        self.assertEqual(len(self.method["passing_witnesses"]), 6)
        self.assertTrue(all(not row["erased"] for row in self.method["failed_witnesses"]))

    def test_15_effective_activation_counts_are_additive(self):
        self.assertEqual(self.method["inherited_repository_sealed_negatives"], 27223)
        self.assertEqual(self.method["inherited_repository_sealed_methods"], 12570)
        self.assertEqual(self.method["effective_activation_negatives"], 27229)
        self.assertEqual(self.method["effective_activation_methods"], 12576)

    def test_16_every_phase_json_parses_and_boundaries_remain(self):
        documents = []
        for path in PHASE_ROOT.rglob("*.json"):
            documents.append(json.loads(path.read_text(encoding="utf-8")))
        self.assertGreaterEqual(len(documents), 13)
        charter = load("x1/phase-charter.json")
        self.assertEqual(charter["primary_pillar"], "GMUT Mind")
        self.assertEqual(charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertIn("relational working language only", charter["identity_boundary"])
        self.assertIn("zero real people", charter["practice_boundary"])


if __name__ == "__main__":
    unittest.main()
