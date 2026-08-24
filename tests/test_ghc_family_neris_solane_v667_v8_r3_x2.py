from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r3_x2.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r3_x2", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load r3 x2 builder")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class NerisSolaneV667V8R3X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = builder.validate_tree()
        cls.root = builder.PHASE_ROOT
        cls.outcomes = json.loads((cls.root / "x2/proposals/proposal-outcomes.json").read_text(encoding="utf-8"))
        cls.mutations = json.loads((cls.root / "x2/proposals/negative-mutation-results.json").read_text(encoding="utf-8"))
        cls.tools = json.loads((cls.root / "x2/tooling/thirteen-tool-transaction-receipt.json").read_text(encoding="utf-8"))
        cls.method = json.loads((cls.root / "x2/method-flow/method-flow-ledger.json").read_text(encoding="utf-8"))

    def test_01_owner_tree_validation(self) -> None:
        self.assertEqual(self.summary["status"], "PASS")
        self.assertEqual(self.summary["privacy_candidates"], 0)
        self.assertLess(self.summary["owner_files"], 2000)

    def test_02_x1_is_zero_parent(self) -> None:
        line = subprocess.run(
            ["git", "-C", str(ROOT), "rev-list", "--parents", "-n", "1", builder.X1_HEAD],
            text=True, capture_output=True, check=True,
        ).stdout.strip().split()
        self.assertEqual(line, [builder.X1_HEAD])

    def test_03_outcomes_exact(self) -> None:
        self.assertEqual(
            Counter(row["outcome_label"] for row in self.outcomes["outcomes"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(self.outcomes["allowed_outcomes"], builder.ALLOWED_OUTCOMES)

    def test_04_negative_mutations(self) -> None:
        self.assertEqual(len(self.mutations["mutations"]), 100)
        self.assertTrue(self.mutations["all_rejected"])
        self.assertTrue(self.mutations["all_expected_rejections_observed"])

    def test_05_tool_transaction(self) -> None:
        self.assertEqual(self.tools["direct_tool_count"], 13)
        self.assertEqual(self.tools["positive_smoke_count"], 13)
        self.assertEqual(self.tools["negative_rejection_count"], 13)
        self.assertEqual(len(self.tools["operational_failures"]), 11)
        self.assertEqual(self.tools["python_audit"]["known_vulnerability_count"], 0)
        self.assertEqual(self.tools["npm_known_vulnerability_count"], 0)

    def test_06_numerical_fixtures(self) -> None:
        payload = json.loads((self.root / "x2/numerical/reproducibility-fixtures.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["count"], 8)
        self.assertTrue(payload["all_passed"])
        self.assertTrue(all(row["real_measurement_count"] == 0 for row in payload["fixtures"]))

    def test_07_flashcards(self) -> None:
        payload = json.loads((self.root / "x2/flashcards/four-tier-deck.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["count"], 320)
        self.assertEqual(payload["tier_counts"], {"1": 40, "2": 80, "3": 100, "4": 100})

    def test_08_skills_and_runners(self) -> None:
        skills = json.loads((self.root / "x2/skills/local-skill-validation.json").read_text(encoding="utf-8"))
        runners = json.loads((self.root / "x2/runners/runner-execution-results.json").read_text(encoding="utf-8"))
        self.assertEqual(skills["count"], 10)
        self.assertTrue(skills["all_passed"])
        self.assertEqual(runners["count"], 10)
        self.assertTrue(runners["all_passed"])

    def test_09_method_flow(self) -> None:
        self.assertEqual(self.method["effective_negatives"], 28733)
        self.assertEqual(self.method["methods"], 15319)
        self.assertEqual(self.method["open_gaps"], 203)
        self.assertEqual(self.method["exact_gates"], 201)
        self.assertEqual(self.method["failed_witnesses"], 1034)
        self.assertEqual(self.method["passing_witnesses"], 1875)

    def test_10_terminal_boundaries(self) -> None:
        self.assertEqual(self.method["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.method["same_owner_not_independent_reproduction"])

    def test_11_report_minimum(self) -> None:
        self.assertGreaterEqual(self.summary["report_words"], 3000)

    def test_12_no_successor_contact(self) -> None:
        receipt = json.loads((self.root / "x2/x2-build-receipt.json").read_text(encoding="utf-8"))
        self.assertFalse(receipt["successor_contacted"])


if __name__ == "__main__":
    unittest.main()
