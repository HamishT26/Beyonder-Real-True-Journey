from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V649V7EvidenceTests(unittest.TestCase):
    def test_outcomes_and_negative_retention(self):
        outcomes = load("x2/core-outcome-ledger.json")
        self.assertEqual(outcomes["proposal_count"], 20)
        self.assertEqual(outcomes["distribution"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(outcomes["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        negatives = load("x2/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 5199)
        self.assertEqual(negatives["x1_operational"], 9)
        self.assertEqual(negatives["synthetic_executed_and_rejected"], 100)
        self.assertEqual(negatives["x2_operational"], 4)
        self.assertEqual(negatives["effective_at_evidence"], 5312)
        self.assertFalse(negatives["negative_erased"])

    def test_expanded_portfolios_completed(self):
        self.assertEqual(load("x2/safe-now-results.json")["completed_count"], 40)
        self.assertEqual(load("x2/candidate-results.json")["completed_count"], 30)
        self.assertEqual(load("x2/clean-fix-refine-results.json")["completed_count"], 40)
        skills = load("x2/skill-use-ledger.json")
        self.assertEqual(skills["completed_count"], 20)
        self.assertEqual(skills["pending_count"], 0)
        self.assertFalse(skills["global_installation"])
        self.assertTrue(all(row["smoke_used"] and row["quick_validate_returncode"] == 0 for row in skills["skills"]))
        runners = load("x2/runner-use-ledger.json")
        self.assertEqual(runners["completed_count"], 10)
        self.assertTrue(all(row["passing_fixture"] and row["rejecting_fixture"] for row in runners["runners"]))

    def test_core_artifacts_and_mutations(self):
        outcomes = load("x2/core-outcome-ledger.json")["outcomes"]
        self.assertEqual(len(outcomes), 20)
        for row in outcomes:
            root = PHASE / row["artifact_root"]
            self.assertTrue((root / "contract.json").is_file())
            mutation = json.loads((root / "mutation-results.json").read_text(encoding="utf-8"))
            self.assertEqual(mutation["count"], 5)
            self.assertEqual(mutation["rejected_count"], 5)
            self.assertTrue(all(item["negative_retained"] for item in mutation["mutations"]))
        all_mutations = load("x2/synthetic-mutation-results.json")
        self.assertEqual(all_mutations["count"], 100)
        self.assertEqual(all_mutations["rejected_count"], 100)

    def test_gates_workflow_and_stage20(self):
        gates = load("x2/gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 41)
        self.assertEqual(gates["effective_exact_gates"], 42)
        self.assertEqual(gates["silently_closed"], 0)
        general = load("workflow/general-validator-receipt.json")
        self.assertTrue(general["passed"])
        self.assertFalse(general["authority_credit"])
        truth = load("phase-truth-evidence.json")
        self.assertFalse(truth["full_repository_suite"])
        self.assertFalse(truth["replay_used"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_skills_are_phase_local_and_valid(self):
        skills = load("x2/skill-use-ledger.json")["skills"]
        for row in skills:
            folder = PHASE / "skills" / row["name"]
            self.assertTrue((folder / "SKILL.md").is_file())
            self.assertTrue((folder / "agents" / "openai.yaml").is_file())
            self.assertNotIn("TODO", (folder / "SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
