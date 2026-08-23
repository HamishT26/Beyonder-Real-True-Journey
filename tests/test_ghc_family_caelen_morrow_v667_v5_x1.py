from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class CaelenMorrowV667V5X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load("x1/proposal-freeze.json")
        cls.novelty = load("x1/novelty-audit.json")
        cls.portfolio = load("x1/portfolio-freeze.json")
        cls.source = load("x1/source-verification.json")
        cls.sources = load("x1/source-ledger.json")
        cls.charter = load("x1/phase-charter.json")
        cls.flow = load("method-flow/startup-method-flow.json")
        cls.architecture = load("x1/flashcard-architecture-freeze.json")
        cls.checklist = load("x1/complete-incomplete-checklist.json")

    def test_exact_twenty_new_proposals_and_frozen_total(self) -> None:
        rows = self.freeze["new_proposals"]
        self.assertEqual(20, len(rows))
        self.assertEqual(20, self.freeze["genuinely_new_proposal_count"])
        self.assertEqual(4410, self.freeze["inherited_proposal_count"])
        self.assertEqual(4430, self.freeze["new_frozen_total"])
        self.assertEqual(20, len({row["proposal_id"] for row in rows}))

    def test_every_proposal_has_complete_preregistration_contract(self) -> None:
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition",
            "approval_class", "execution_lane", "current_official_or_primary_source_needs",
            "concrete_artifact", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
            "distinctive_invariant", "practice_lens", "preregistered_mutations",
        }
        for row in self.freeze["new_proposals"]:
            self.assertFalse(required - set(row), row["proposal_id"])
            self.assertEqual(5, len(row["preregistered_mutations"]))
            self.assertEqual(0, row["network_calls_planned"])
            self.assertEqual(0, row["participant_count_planned"])
            self.assertEqual(0, row["real_data_rows_planned"])
            self.assertFalse(row["outcomes_observed"])
            self.assertEqual(0, row["x2_implementation_count"])

    def test_expected_outcomes_use_only_four_labels(self) -> None:
        counts = Counter(row["expected_disposition"] for row in self.freeze["new_proposals"])
        self.assertEqual({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, dict(counts))
        self.assertEqual({"completed", "represented", "open_gap", "exact_gate"}, set(self.freeze["allowed_core_outcomes"]))

    def test_complete_4410_row_novelty_audit_is_valid(self) -> None:
        self.assertEqual(4410, self.novelty["corpus_row_count"])
        self.assertEqual(20, self.novelty["new_proposal_count"])
        self.assertEqual(4430, self.novelty["new_frozen_total"])
        self.assertEqual([], self.novelty["exact_title_collisions"])
        self.assertEqual([], self.novelty["pair_collisions_at_or_above_threshold"])
        self.assertLess(self.novelty["maximum_inherited_similarity"], 0.6)
        self.assertTrue(self.novelty["valid"])

    def test_domain_novelty_and_rejected_horology_are_visible(self) -> None:
        domain = self.novelty["domain_review"]
        self.assertEqual(0, domain["exact_domain_phrase_match_count"])
        self.assertGreater(domain["related_generic_match_count"], 0)
        rejected = self.novelty["rejected_draft_practices"]
        self.assertEqual("rejected_before_freeze_zero_credit", rejected[0]["disposition"])
        self.assertGreater(rejected[0]["term_counts"]["clock"], 0)
        self.assertGreater(rejected[0]["term_counts"]["calibration"], 0)

    def test_primary_pillar_practice_and_relational_boundary(self) -> None:
        self.assertEqual("GMUT Mind", self.charter["primary_pillar"])
        self.assertIn("celestial-navigation", self.charter["bounded_practice"])
        self.assertIn("relational working language only", self.charter["identity_boundary"])
        self.assertIn("not evidence of consciousness", self.charter["identity_boundary"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.charter["terminal_verdict"])
        self.assertTrue(self.charter["solo"])
        self.assertEqual(0, self.charter["delegated_or_spawned_agents"])

    def test_source_chain_manifest_and_validation_truth(self) -> None:
        self.assertEqual("08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93", self.source["source_exact_final"])
        self.assertEqual(3, self.source["source_to_final_commit_count"])
        self.assertEqual(0, self.source["source_to_final_merge_count"])
        self.assertEqual(1, self.source["source_final_parent_count"])
        self.assertTrue(self.source["source_direct_chain_valid"])
        self.assertTrue(self.source["source_four_way_equal"])
        self.assertEqual(816, self.source["source_manifest_replay"]["total"])
        self.assertEqual(0, self.source["source_manifest_replay"]["mismatches"])
        self.assertTrue(self.source["source_canonical_succeeded_once"])
        self.assertFalse(self.source["source_canonical_replayed"])
        self.assertFalse(self.source["full_repository_suite_run"])

    def test_lifecycle_scoped_compile_counts_remain_distinct(self) -> None:
        scopes = self.source["source_python_compile_scopes"]
        self.assertEqual(18, scopes["x2_prestage"])
        self.assertEqual(21, scopes["exact_final_canonical"])
        self.assertIn("neither count rewrites", scopes["interpretation"])

    def test_inherited_counts_and_eight_caelen_startup_failures(self) -> None:
        self.assertEqual(27536, self.flow["inherited_effective_negatives"])
        self.assertEqual(13113, self.flow["inherited_effective_methods"])
        self.assertEqual(8, self.flow["startup_failed_method_count"])
        self.assertEqual(27544, self.flow["effective_x1_baseline_negatives"])
        self.assertEqual(13121, self.flow["effective_x1_baseline_methods"])
        self.assertEqual(8, len(self.flow["failed_witnesses"]))
        self.assertTrue(all(row["success_credit"] == 0 and not row["erased"] for row in self.flow["failed_witnesses"]))

    def test_portfolio_counts_and_holds(self) -> None:
        self.assertEqual(30, len(self.portfolio["owner_safe_now"]))
        self.assertEqual(15, len(self.portfolio["owner_candidates"]))
        self.assertEqual(10, len(self.portfolio["owner_skill_ideas"]))
        self.assertEqual(10, len(self.portfolio["owner_runner_ideas"]))
        self.assertEqual(30, len(self.portfolio["owner_clean_fix_refine"]))
        self.assertEqual(10, len(self.portfolio["exact_approval_packets"]))
        self.assertEqual(5, len(self.portfolio["blocked_packets"]))
        self.assertEqual(0, self.portfolio["x2_implementation_count"])
        self.assertFalse(self.portfolio["outcomes_observed"])
        self.assertTrue(all(row["completion_credit"] == 0 for key, rows in self.portfolio.items() if isinstance(rows, list) for row in rows))

    def test_source_ledger_uses_current_official_or_primary_surfaces(self) -> None:
        rows = self.sources["sources"]
        self.assertEqual(13, len(rows))
        self.assertEqual(13, len({row["source_id"] for row in rows}))
        self.assertTrue(all(row["url"].startswith("https://") for row in rows))
        self.assertTrue(all("reviewed" in row["status"] for row in rows))
        self.assertEqual(0, self.sources["network_actions_by_phase_software"])
        self.assertIn("grant no navigation", self.sources["boundary"])

    def test_flashcard_architecture_is_four_tier_thirteen_section_and_nonidentity(self) -> None:
        self.assertEqual(4, len(self.architecture["four_tiers"]))
        self.assertEqual(13, len(self.architecture["required_deck_sections"]))
        self.assertFalse(self.architecture["cache_effect_measured"])
        self.assertFalse(self.architecture["identity_continuity_claim"])
        self.assertFalse(self.architecture["successor_route"]["contacted"])

    def test_x1_tree_contains_no_x2_or_outcomes(self) -> None:
        self.assertFalse((PHASE_ROOT / "x2").exists())
        forbidden_names = {"outcome-ledger.json", "evidence-receipt.json", "seal-candidate.json", "final-validation.json"}
        self.assertFalse(forbidden_names & {path.name for path in PHASE_ROOT.rglob("*") if path.is_file()})
        for path in PHASE_ROOT.rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "outcomes_observed" in data:
                self.assertFalse(data["outcomes_observed"], path)

    def test_overview_checklist_privacy_and_caps(self) -> None:
        overview = (PHASE_ROOT / "x1" / "x1-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(overview.count("\n## "), 10)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.checklist["terminal_verdict"])
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLessEqual(len(files), 2000)
        joined = "\n".join(path.read_text(encoding="utf-8") for path in files)
        for forbidden in ["source_thread_id", "C:\\Users\\", "D:\\GHC-Archives", "session_stream", "private_callable"]:
            self.assertNotIn(forbidden, joined)


if __name__ == "__main__":
    unittest.main()
