from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v688-v5"


class ElowenCairnV688V5Correction1Tests(unittest.TestCase):
    def test_failed_case_literal_is_bound_to_immutable_report(self) -> None:
        overview = (BASE / "final" / "final-integrated-overview.md").read_text(encoding="utf-8")
        truth = json.loads((BASE / "correction1" / "phase-truth.json").read_text(encoding="utf-8"))
        binding = json.loads((BASE / "correction1" / "failed-canonical-binding.json").read_text(encoding="utf-8"))
        self.assertIn("same-owner", overview)
        self.assertEqual(truth["correction_scope"], "case-sensitive final-test literal only")
        self.assertFalse(truth["original_overview_mutated"])
        self.assertEqual(binding["sole_failed_predicate"], "final_tests_pass")
        self.assertEqual(binding["canonical_success_count"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
