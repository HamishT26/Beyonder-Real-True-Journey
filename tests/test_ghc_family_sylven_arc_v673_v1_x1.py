"""Owner-scoped planning-only tests for Sylven Arc v673-v1 x1."""

from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "sylven-arc" / "v673-v1"
X1 = OWNER / "x1"
SOURCE = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
BRANCH = "codex/GHC-Family/sylven-arc-v673-v1-full-tools"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


class TestSylvenArcV673V1X1(unittest.TestCase):
    def test_01_exact_source_head(self):
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)

    def test_02_exact_owner_branch(self):
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_03_x2_and_closeout_absent(self):
        self.assertFalse((OWNER / "x2").exists())
        self.assertFalse((OWNER / "closeout").exists())

    def test_04_activation_is_solo_and_additive(self):
        row = load("activation-intake.json")
        self.assertEqual(row["task_creation_count"], 0)
        self.assertEqual(row["fork_count"], 0)
        self.assertEqual(row["subagent_count"], 0)
        self.assertEqual(row["standby_contact_count"], 0)

    def test_05_source_lineage_is_exact(self):
        row = load("activation-intake.json")["source_verification"]
        self.assertEqual(row["source_final"], SOURCE)
        self.assertEqual(row["source_to_final_phase_commits"], 3)
        self.assertEqual(row["merge_commits"], 0)
        self.assertTrue(row["single_parent_chain"])

    def test_06_source_canonical_not_replayed(self):
        row = load("activation-intake.json")["source_verification"]
        self.assertEqual(row["canonical_invocations"], 1)
        self.assertEqual(row["canonical_successes"], 1)
        self.assertEqual(row["canonical_replays"], 0)
        self.assertFalse(row["source_canonical_replayed_by_sylven"])

    def test_07_exactly_forty_new_proposals(self):
        row = load("new-proposal-freeze.json")
        self.assertEqual(len(row["rows"]), 40)
        self.assertEqual(len({item["proposal_id"] for item in row["rows"]}), 40)
        self.assertEqual(len({item["title"] for item in row["rows"]}), 40)

    def test_08_proposal_outcomes_are_exact(self):
        rows = load("new-proposal-freeze.json")["rows"]
        self.assertEqual(Counter(item["expected_disposition"] for item in rows), Counter(OUTCOMES))
        self.assertEqual(set(OUTCOMES), {"completed", "represented", "open_gap", "exact_gate"})

    def test_09_every_proposal_has_required_contract(self):
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_need", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition",
        }
        for row in load("new-proposal-freeze.json")["rows"]:
            self.assertTrue(required <= row.keys(), row["proposal_id"])
            self.assertTrue(all(row[key] for key in required), row["proposal_id"])

    def test_10_mutations_are_preregistered(self):
        row = load("new-proposal-freeze.json")
        self.assertEqual(row["planned_invalid_mutations_per_proposal"], 4)
        self.assertEqual(row["planned_invalid_mutations"], 160)
        self.assertTrue(all(len(item["planned_invalid_mutations"]) == 4 for item in row["rows"]))

    def test_11_inherited_selection_has_zero_credit(self):
        row = load("inherited-proposal-revalidation.json")
        self.assertEqual(row["selection_count"], 20)
        self.assertEqual(row["novelty_credit"], 0)
        self.assertEqual(row["completion_credit"], 0)
        self.assertTrue(all(item["sylven_novelty_credit"] == 0 for item in row["rows"]))

    def test_12_declared_chain_is_not_universally_claimed(self):
        row = load("semantic-neighbor-audit.json")
        corpus = row["exact_source_tree_corpus"]
        self.assertEqual(row["declared_source_chain"], 6230)
        self.assertFalse(row["universal_novelty_claim"])
        self.assertTrue(row["canonical_row_mapping_open_gap"])
        self.assertFalse(corpus["exact_canonical_row_mapping"])

    def test_13_source_bounded_semantic_gate_passes(self):
        row = load("semantic-neighbor-audit.json")
        self.assertEqual(row["new_titles"], 40)
        self.assertEqual(row["collisions"], 0)
        self.assertLess(row["max_jaccard"], row["collision_threshold"])
        self.assertEqual(len(row["rows"]), 40)

    def test_14_corpus_blobs_decode_cleanly(self):
        corpus = load("semantic-neighbor-audit.json")["exact_source_tree_corpus"]
        self.assertGreater(corpus["candidate_git_blob_paths"], 0)
        self.assertGreater(corpus["unique_titles"], 0)
        self.assertEqual(corpus["malformed_or_missing_blobs"], 0)

    def test_15_portfolio_counts_are_exact(self):
        counts = load("portfolio-freeze.json")["counts"]
        expected = {
            "safe_now": 60, "candidates": 30, "exact_approval": 20, "blocked": 10,
            "skills": 20, "runners": 10, "clean_fix_refine": 60,
            "successor_skills": 10, "successor_runners": 10,
            "successor_clean_fix_refine": 30,
        }
        self.assertEqual(counts, expected)

    def test_16_exact_and_blocked_are_unexecuted(self):
        rows = load("portfolio-freeze.json")["rows"]
        self.assertTrue(all(item["x1_state"] == "held_unexecuted" for item in rows["exact_approval"]))
        self.assertTrue(all(item["x1_state"] == "held_unexecuted" for item in rows["blocked"]))

    def test_17_successor_rows_are_recommendations_only(self):
        rows = load("portfolio-freeze.json")["rows"]
        for key in ("successor_skills", "successor_runners", "successor_clean_fix_refine"):
            self.assertTrue(all(item["x1_state"] == "recommendation_only" for item in rows[key]))

    def test_18_thirteen_failures_are_retained(self):
        row = load("method-flow-startup.json")
        self.assertEqual(row["counts"]["methods"], 13)
        self.assertEqual(row["counts"]["witness_results"], {"fail": 13, "pass": 13})
        self.assertEqual(Counter(item["result"] for item in row["witnesses"]), Counter({"fail": 13, "pass": 13}))

    def test_19_recoveries_never_erase_failures(self):
        row = load("method-flow-startup.json")
        witnesses = row["witnesses"]
        for method in row["methods"]:
            linked = [item for item in witnesses if item["method_id"] == method["method_id"]]
            self.assertEqual({item["result"] for item in linked}, {"fail", "pass"})
            self.assertTrue(method["retained_negative_ids"])

    def test_20_count_overlay_is_additive(self):
        row = load("source-count-overlay.json")
        self.assertEqual(row["repository_sealed"]["effective_negatives"], 36160)
        self.assertEqual(row["activation_baseline"]["effective_negatives"], 36161)
        self.assertEqual(row["sylven_x1_overlay"]["effective_negatives"], 36174)
        self.assertFalse(row["sylven_x1_overlay"]["repository_seal_rewritten"])

    def test_21_no_external_source_or_action_occurred(self):
        row = load("source-ledger.json")
        self.assertEqual(row["api_calls"], 0)
        self.assertEqual(row["dataset_or_media_downloads"], 0)
        self.assertEqual(row["real_rows"], 0)
        self.assertEqual(row["external_writes"], 0)

    def test_22_route_is_only_provisional(self):
        row = load("route-plan.json")
        self.assertEqual(row["delivery_state"], "PROVISIONAL_NOT_CONTACTED_REQUIRES_TERMINAL_REFRESH")
        self.assertEqual(row["prospective_recipient_exact_title"], "Caelen Morrow")
        self.assertEqual(row["successor_contact_count"], 0)
        self.assertEqual(row["standby_contact_count"], 0)

    def test_23_phase_truth_is_planning_only(self):
        row = load("phase-truth.json")
        self.assertEqual(row["new_proposals"], 40)
        self.assertEqual(row["planned_proposal_chain_after"], 6270)
        self.assertFalse(row["x2_exists"])
        self.assertEqual(row["x2_completion_claims"], 0)
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_24_identity_scientific_and_authority_boundaries_hold(self):
        identity = load("identity-and-boundary.json")
        threat = load("threat-model.json")
        overview = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("working language only", identity["identity_boundary"])
        self.assertTrue(threat["not_exhaustive_security"])
        for phrase in ("not empirical confirmation", "NOT_READY_FOR_STAGE_20", "Māori concepts remain under Māori authority"):
            self.assertIn(phrase, overview)


if __name__ == "__main__":
    unittest.main()
