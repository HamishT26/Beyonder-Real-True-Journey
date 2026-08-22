from __future__ import annotations

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "auren-lark" / "v666-v5"
BUILDER_PATH = ROOT / "scripts" / "build_ghc_family_auren_lark_v666_v5_x1.py"
SPEC = importlib.util.spec_from_file_location("auren_v666_v5_x1", BUILDER_PATH)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def load(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class AurenV666V5X1Tests(unittest.TestCase):
    def test_exact_source_and_owner(self) -> None:
        self.assertEqual(BUILDER.SOURCE_SHA, "e4548a5447996f09087644a4a03e77dea8045ee4")
        self.assertEqual(BUILDER.SOURCE_X1_SHA, "7926a46fa309f180cb996dacbea7ae849a3cf507")
        self.assertEqual(BUILDER.SOURCE_PARENT_SHA, "ce4bb6a288edc71d3916a098d6db4d61995fc60c")
        self.assertEqual(BUILDER.INHERITED_LYREN_SHA, "764d3bdfb199e91a5574a904a99ff4e95825fed9")

    def test_twenty_distinct_planning_only_proposals(self) -> None:
        proposals = BUILDER.build_proposals()
        self.assertEqual(len(proposals), 20)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 20)
        self.assertEqual(len({row["title"].casefold() for row in proposals}), 20)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in proposals),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertTrue(all(row["x1_status"] == "frozen_not_executed" for row in proposals))
        self.assertTrue(all(row["x2_implementation_count"] == 0 for row in proposals))
        self.assertTrue(all(not row["outcomes_observed"] for row in proposals))
        self.assertTrue(all(len(row["preregistered_mutations"]) == 5 for row in proposals))

    def test_full_inherited_corpus_and_novelty(self) -> None:
        corpus, construction = BUILDER.build_corpus()
        proposals = BUILDER.build_proposals()
        novelty = BUILDER.build_novelty(corpus, construction, proposals)
        self.assertEqual(len(corpus), 4250)
        self.assertEqual(novelty["corpus_row_count"], 4250)
        self.assertEqual(novelty["new_frozen_total"], 4270)
        self.assertEqual(novelty["exact_inherited_collisions"], [])
        self.assertEqual(novelty["new_pair_collisions_at_or_above_0_70"], [])
        self.assertLess(novelty["maximum_new_pair_token_jaccard_similarity"], 0.70)
        self.assertTrue(novelty["valid"])

    def test_source_verification_is_lifecycle_bound(self) -> None:
        source = load("provenance/source-verification.json")
        replay = source["lifecycle_manifest_replay"]
        self.assertTrue(replay["initial_wrong_domain_failure_retained"])
        self.assertEqual(replay["total_observed"], 932)
        self.assertEqual(replay["total_expected"], 932)
        self.assertTrue(replay["valid"])
        self.assertTrue(source["local_equals_upstream_tracking_and_fresh_live"])
        self.assertTrue(source["source_validation_not_replayed"])

    def test_identity_and_practice_boundaries(self) -> None:
        identity = load("identity/relational-identity.json")
        boundary = identity["boundary"]
        for phrase in (
            "relational working language only",
            "not evidence of consciousness",
            "legal personhood",
            "identity continuity",
            "independent agency",
            "Māori authority",
        ):
            self.assertIn(phrase, boundary)
        charter = load("x1/phase-charter.json")
        self.assertIn("zero real people", charter["practice_boundary"])
        self.assertIn("no perfumery", charter["practice_boundary"])
        self.assertEqual(charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_sources_are_vocabulary_only(self) -> None:
        sources = load("provenance/source-profiles.json")
        self.assertEqual(sources["source_count"], 8)
        self.assertTrue(all(row["authority_nonconversion"] for row in sources["sources"]))
        self.assertTrue(all(row["real_rows_ingested"] == 0 for row in sources["sources"]))
        self.assertTrue(all(row["network_calls_by_phase_software"] == 0 for row in sources["sources"]))
        self.assertIn("no safety", sources["claim_boundary"])

    def test_portfolio_freeze_exact_counts(self) -> None:
        portfolio = load("x1/portfolio-freeze.json")
        self.assertTrue(portfolio["frozen"])
        self.assertTrue(portfolio["minimums_satisfied"])
        self.assertEqual(
            portfolio["counts"],
            {
                "owner_safe_now": 30,
                "successor_safe_now": 20,
                "owner_bounded_candidates": 15,
                "successor_bounded_candidates": 15,
                "exact_approval_packets": 10,
                "blocked_packets": 5,
                "owner_phase_local_skill_plans": 10,
                "successor_skill_recommendations": 10,
                "owner_family_current_runner_plans": 10,
                "successor_runner_recommendations": 10,
                "owner_clean_fix_refine": 30,
                "successor_clean_fix_refine": 30,
            },
        )
        self.assertEqual(portfolio["x1_execution_count"], 0)

    def test_startup_method_flow_preserves_every_failure(self) -> None:
        flow = load("method-flow/startup-method-flow.json")
        self.assertEqual(flow["inherited_repository_sealed_negatives"], 26519)
        self.assertEqual(flow["inherited_repository_sealed_methods"], 11176)
        self.assertEqual(flow["inherited_external_overlay_negatives"], 1)
        self.assertEqual(flow["activation_baseline_negatives"], 26520)
        self.assertEqual(flow["new_startup_negative_count"], 9)
        self.assertEqual(flow["new_startup_method_count"], 9)
        self.assertEqual(flow["effective_after_x1_startup_negatives"], 26529)
        self.assertEqual(flow["effective_after_x1_startup_methods"], 11186)
        self.assertTrue(flow["no_failure_erased"])
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in flow["rows"]))
        self.assertTrue(all(row["status"] == "recovered_failure_retained" for row in flow["rows"]))

    def test_generated_x1_has_no_x2_or_outcomes(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        checklist = load("x1/complete-incomplete-checklist.json")
        receipt = load("x1/x1-build-receipt.json")
        self.assertFalse(freeze["outcomes_observed"])
        self.assertEqual(freeze["x2_implementation_count"], 0)
        self.assertEqual(freeze["x2_outcome_count"], 0)
        self.assertFalse(checklist["x2_paths_created"])
        self.assertFalse(checklist["successor_contacted"])
        self.assertFalse(receipt["outcomes_observed"])
        self.assertFalse((PHASE_ROOT / "x2").exists())
        self.assertFalse((PHASE_ROOT / "evidence").exists())
        self.assertFalse((PHASE_ROOT / "closeout").exists())
        self.assertFalse((PHASE_ROOT / "handoffs").exists())

    def test_all_owner_json_is_utf8_lf_and_parseable(self) -> None:
        json_paths = sorted(PHASE_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 12)
        for path in json_paths:
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw, str(path))
            json.loads(raw.decode("utf-8"))

    def test_workflow_and_flashcard_freezes_are_nonterminal(self) -> None:
        workflow = load("x1/workflow-plan.json")
        flashcards = load("x1/flashcard-architecture-freeze.json")
        self.assertEqual(workflow["current_stage"], "x1_freeze_candidate")
        self.assertEqual(workflow["steps"][2]["status"], "in_progress")
        self.assertTrue(flashcards["frozen"])
        self.assertEqual(flashcards["x2_cards_created"], 0)


if __name__ == "__main__":
    unittest.main()
