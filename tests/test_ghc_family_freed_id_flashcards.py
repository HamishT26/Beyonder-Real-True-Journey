#!/usr/bin/env python3
"""Owner-delta tests for the GHC Freed ID flashcard remaster."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import ghc_family_freed_id_flashcards as flashcards

DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_freed_id_flashcards.py",
]

PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v663-v6-r2"
DECK = PHASE_ROOT / "deck"
SKILL = PHASE_ROOT / "skill-source" / "ghc-freed-id-flashcards"
X1 = "0e895970d3a198a601db3128330c06378fe2bdc6"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestDeckModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _, cls.model = flashcards.load_deck(ROOT, DECK.relative_to(ROOT).as_posix())
        cls.by_id = {row["card_id"]: row for row in cls.model["cards"]}

    def test_model_validation(self) -> None:
        result = flashcards.validate_model(self.model)
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["card_count"], 253)

    def test_exact_tier_counts(self) -> None:
        self.assertEqual(Counter(row["tier"] for row in self.model["cards"]), Counter({1: 1, 2: 3, 3: 1, 4: 248}))

    def test_card_types_match_tiers(self) -> None:
        for row in self.model["cards"]:
            self.assertEqual(flashcards.TIER_FOR_TYPE[row["card_type"]], row["tier"])

    def test_single_owner_anchor(self) -> None:
        roots = [row for row in self.model["cards"] if row["tier"] == 1]
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0]["card_type"], "freed_id_anchor")
        self.assertEqual(roots[0]["parent_ids"], [])

    def test_parent_tiers(self) -> None:
        for row in self.model["cards"]:
            if row["tier"] == 1:
                continue
            self.assertEqual(len(row["parent_ids"]), 1)
            self.assertEqual(self.by_id[row["parent_ids"][0]]["tier"], row["tier"] - 1)

    def test_stable_volatile_partition(self) -> None:
        stable = self.model["stable_prefix"]["card_ids"]
        volatile = self.model["volatile_index"]["card_ids"]
        self.assertEqual(len(stable), 4)
        self.assertFalse(set(stable) & set(volatile))
        self.assertEqual(set(stable) | set(volatile), set(self.by_id))

    def test_exact_sections(self) -> None:
        sections = self.model["baton_index"]["sections"]
        self.assertEqual([row["section"] for row in sections], flashcards.REQUIRED_SECTIONS)
        self.assertEqual(len(sections), 13)
        self.assertTrue(all(row["card_ids"] for row in sections))

    def test_new_core_outcomes(self) -> None:
        outcomes = Counter(self.by_id[value]["outcome"] for value in self.model["new_proposal_card_ids"])
        self.assertEqual(outcomes, Counter(completed=14, represented=4, open_gap=1, exact_gate=1))

    def test_inherited_cards_have_zero_credit(self) -> None:
        inherited = [row for row in self.model["cards"] if row.get("content", {}).get("program_class") == "selected_inherited_revalidation"]
        self.assertEqual(len(inherited), 20)
        self.assertTrue(all(row["content"]["novelty_credit"] is False for row in inherited))
        self.assertTrue(all(row["content"]["automatic_completion_credit"] is False for row in inherited))

    def test_new_proposal_cards(self) -> None:
        self.assertEqual(len(self.model["new_proposal_card_ids"]), 20)
        self.assertTrue(all(self.by_id[value]["content"]["novelty_credit"] for value in self.model["new_proposal_card_ids"]))

    def test_outcomes_are_closed_vocabulary(self) -> None:
        self.assertTrue(all(row["outcome"] in flashcards.ALLOWED_OUTCOMES for row in self.model["cards"]))

    def test_relational_boundary_present(self) -> None:
        self.assertTrue(all("not consciousness" in row["relational_boundary"] for row in self.model["cards"]))


class TestDeckArtifacts(unittest.TestCase):
    def test_full_deck_validation(self) -> None:
        result = flashcards.validate_deck(ROOT, DECK.relative_to(ROOT).as_posix())
        self.assertTrue(result["valid"])
        self.assertTrue(result["manual_evaluation_reserved"])
        self.assertEqual(result["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_manifest_parity(self) -> None:
        result = flashcards.manifest_status(DECK)
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual((result["expected_entries"], result["observed_entries"]), (260, 260))

    def test_privacy_scan(self) -> None:
        result = flashcards.privacy_status(DECK)
        self.assertTrue(result["valid"], result["candidates"])
        self.assertEqual(result["candidate_count"], 0)

    def test_compact_message(self) -> None:
        text = (DECK / "compact-activation.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.split()), 600)
        self.assertFalse(flashcards.private_candidates(text))
        self.assertIn("Caelen Morrow", text)
        self.assertIn("Eiren Kestrel", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_accessible_structure(self) -> None:
        text = (DECK / "accessible-report.html").read_text(encoding="utf-8")
        for marker in ('<!doctype html>', '<html lang="en">', '<main id="main">', '<nav', '<table>', '<caption>'):
            self.assertIn(marker, text)
        self.assertIn("Manual browser, assistive-technology", text)

    def test_manifest_self_exclusion(self) -> None:
        manifest = load(DECK / "card-manifest.json")
        self.assertEqual(manifest["self_excluded_paths"], ["card-manifest.json"])
        self.assertEqual(manifest["entry_count"], 260)

    def test_deck_source_and_x1(self) -> None:
        index = load(DECK / "deck-index.json")
        self.assertEqual(index["source_exact_final"], "81bef3ba75740d9f42b9a0bf5cd2f6bc4e2e58c9")
        self.assertEqual(index["x1_head"], X1)

    def test_mutations(self) -> None:
        receipt = load(PHASE_ROOT / "x2" / "mutation-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual((receipt["mutation_count"], receipt["rejected_count"]), (60, 60))
        self.assertEqual(receipt["positive_proposal_fixture_count"], 20)
        self.assertTrue(receipt["positive_deck_valid"])
        self.assertEqual(receipt["failure_credit"], 0)

    def test_all_card_json_strict(self) -> None:
        paths = sorted((DECK / "cards").rglob("*.json"))
        self.assertEqual(len(paths), 253)
        for path in paths:
            self.assertIsInstance(flashcards.strict_json(path), dict)


class TestRunnerAndSkill(unittest.TestCase):
    def test_in_memory_smoke(self) -> None:
        model = flashcards.build_model(PHASE_ROOT, X1)
        result = flashcards.validate_model(model)
        self.assertTrue(result["valid"])

    def test_runner_commands_declared(self) -> None:
        actions = flashcards.parser()._subparsers._group_actions[0].choices
        self.assertEqual(set(actions), {"build", "validate", "manifest", "graph", "privacy", "render-html", "diff", "compact-message", "mutations", "smoke", "install-receipt"})

    def test_skill_frontmatter(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: ghc-freed-id-flashcards\n"))
        self.assertNotIn("TODO", text)
        self.assertIn("Use the four-tier hierarchy", text)
        self.assertIn("Refuse destructive context management", text)

    def test_skill_interface(self) -> None:
        text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("GHC Freed ID Flashcards", text)
        self.assertIn("$ghc-freed-id-flashcards", text)

    def test_skill_references(self) -> None:
        paths = sorted(path.name for path in (SKILL / "references").glob("*.md"))
        self.assertEqual(paths, ["deck-schema.md", "failure-shields.md", "workflow.md"])

    def test_x1_repair_is_prospective(self) -> None:
        text = (PHASE_ROOT / "x1" / "portfolio-freeze.json").read_text(encoding="utf-8")
        self.assertEqual(text.count('"expected_execution_disposition"'), 195)
        self.assertNotIn('"planning_state"', text)

    def test_x1_repair_receipt(self) -> None:
        receipt = load(PHASE_ROOT / "x1" / "x1-repair-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["x2_implementation_present"])
        self.assertFalse(receipt["history_rewritten"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
