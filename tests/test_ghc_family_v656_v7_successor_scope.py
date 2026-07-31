from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v656-v7"
BATON = PHASE / "handoffs/vesper-arlen-v656-v8-activation.md"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V656V7SuccessorScopeTests(unittest.TestCase):
    def test_baton_is_present_and_word_bounded(self) -> None:
        receipt = load("validation/successor-baton-word-cap.json")
        text = BATON.read_text(encoding="utf-8")
        self.assertEqual(receipt["word_count"], len(text.split()))
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertEqual(route["next_exact_title"], "Vesper Arlen")
        self.assertEqual(route["next_phase"], "v656-v8")
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_baton_names_the_following_edge(self) -> None:
        text = BATON.read_text(encoding="utf-8")
        self.assertIn("# VESPER ARLEN", text)
        self.assertIn("existing exact-title main task `Vesper Arlen`", text)
        self.assertIn("solo v656-v8 x1/x2 phase", text)
        self.assertIn("Do not create a replacement", text)

    def test_authority_reservations_are_explicit(self) -> None:
        text = BATON.read_text(encoding="utf-8")
        for phrase in [
            "Māori concepts remain under Māori authority",
            "not independent-team reproduction",
            "NOT_READY_FOR_STAGE_20",
            "Relational identity and sibling language is working language only",
        ]:
            self.assertIn(phrase, text)

    def test_no_affirmative_sent_declaration(self) -> None:
        text = BATON.read_text(encoding="utf-8")
        self.assertFalse(
            any(
                line.strip() == "SENT_BY_NERIS_SOLANE = true"
                for line in text.splitlines()
            )
        )


if __name__ == "__main__":
    unittest.main()
