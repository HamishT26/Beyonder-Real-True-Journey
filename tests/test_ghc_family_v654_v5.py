"""Bounded x2 tests for Eiren Kestrel v654-v5."""
import json
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v5"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV654V5Evidence(unittest.TestCase):
    def test_outcome_distribution(self):
        ledger = load("evidence/outcome-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(ledger["proposal_count"], 30)
    def test_all_surfaces_and_mutations(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(len(rows), 30)
        self.assertEqual(sum(row["mutation_rejected_count"] for row in rows), 150)
        self.assertTrue(all(row["acceptance_gate_passed"] for row in rows))
        self.assertEqual(len(list((ROOT / "surfaces").rglob("contract.json"))), 30)
    def test_zero_real_world_counters(self):
        for path in (ROOT / "surfaces").rglob("bounded-receipt.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(receipt["real_world_counters"].values()), {0}, path)
    def test_skills_initialized_validated_and_smoked(self):
        ledger = load("skills/skill-suite-receipt.json")
        self.assertEqual(ledger["skill_count"], 10)
        self.assertTrue(all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in ledger["rows"]))
        self.assertTrue(all(not row["smoke"]["global_installation"] for row in ledger["rows"]))
    def test_runners_invoked(self):
        ledger = load("tools/runner-suite-receipt.json")
        self.assertEqual(ledger["runner_count"], 10)
        self.assertTrue(all(row["valid"] for row in ledger["rows"]))
        self.assertEqual(sum(row["proposal_count"] for row in ledger["rows"]), 30)
    def test_portfolios_resolved(self):
        ledger = load("evidence/portfolio-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(ledger["all_safe_now_resolved"])
        self.assertTrue(ledger["all_bounded_candidates_resolved"])
    def test_open_and_exact_gates(self):
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual((gaps["effective_count"], gates["effective_count"]), (84, 83))
        self.assertEqual((gaps["new_rows"][0]["real_rows"], gates["new_rows"][0]["authority_decisions"]), (0, 0))
    def test_truth_boundaries(self):
        truth = load("truth/phase-truth-evidence.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertFalse(truth["full_repository_suite_run"])
    def test_successor_remains_conditionally_held(self):
        row = load("provenance/successor-authority-invariant.json")
        self.assertEqual((row["created_count"], row["forked_count"], row["delegated_count"], row["contacted_count"]), (0, 0, 0, 0))
        self.assertEqual(row["state"], "ACTIVE_CURRENT_PHASE_SUCCESSOR_CONTACT_PROHIBITED")
    def test_allowed_outcomes_only(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(set(row["observed_outcome"] for row in rows), {"completed", "represented", "open_gap", "exact_gate"})

if __name__ == "__main__":
    unittest.main()
