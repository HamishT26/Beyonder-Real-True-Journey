"""Scoped evidence tests for Ilyra Fen v646-v8; not the complete repository suite."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
X1 = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestV646V8Evidence(unittest.TestCase):
    def test_distribution_is_exact(self):
        self.assertEqual(read("x2-proposal-ledger.json")["distribution"], {"completed": 6, "exact_gate": 1, "open_gap": 1, "represented": 2})

    def test_only_four_outcome_labels(self):
        ledger = read("x2-proposal-ledger.json")
        self.assertEqual(set(row["disposition"] for row in ledger["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_negative_arithmetic(self):
        register = read("retained-negative-register.json")
        self.assertEqual(register["effective_total"], register["inherited_effective"] + register["x1_operational"] + register["preregistered_synthetic"] + register["x2_operational"])

    def test_70_mutations_rejected(self):
        rows = read("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((rows["count"], rows["executed_count"], rows["rejected_or_quarantined_count"], rows["erased_count"]), (70, 70, 70, 0))

    def test_gate_arithmetic(self):
        gates = read("exact-open-gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]), (17, 18, 0))

    def test_empirical_counters_zero(self):
        truth = read("phase-truth.json")
        self.assertEqual((truth["real_rows"], truth["likelihood_evaluations"], truth["gmut_empirical_claims"]), (0, 0, 0))

    def test_people_and_operation_counters_zero(self):
        truth = read("phase-truth.json")
        self.assertEqual((truth["real_people"], truth["real_aircraft"], truth["real_operations"], truth["authority_decisions"]), (0, 0, 0, 0))

    def test_identity_and_key_counters_zero(self):
        truth = read("phase-truth.json")
        self.assertEqual((truth["real_keys_or_signatures"], truth["production_identity_events"], truth["interoperability_events"]), (0, 0, 0))

    def test_stage20_abstention(self):
        self.assertEqual(read("phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_safe_and_candidate_portfolios(self):
        portfolio = read("approval-packets/x2-portfolio-execution.json")
        self.assertEqual((portfolio["safe_completed"], portfolio["candidate_completed"], portfolio["exact_executed"], portfolio["blocked_executed"]), (30, 20, 0, 0))

    def test_skill_portfolio(self):
        receipt = read("prototypes/skill-build-use-receipt.json")
        self.assertEqual((receipt["built_count"], receipt["validated_count"], receipt["smoke_used_count"]), (20, 20, 20))

    def test_runner_portfolio(self):
        receipt = read("prototypes/runner-build-use-receipt.json")
        self.assertEqual((receipt["built_count"], receipt["invoked_count"]), (10, 10))

    def test_method_failures_preserved(self):
        method = read("method-flow/method-flow-state.json")
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], 8)
        self.assertEqual(method["counts"]["witness_results"]["pass"], method["counts"]["states"]["preferred"])

    def test_report_reserves_manual_evaluation(self):
        report = (PHASE / "deliverables/v646-v8-static-report.html").read_text(encoding="utf-8")
        for text in ("Manual keyboard", "assistive-technology", "affected-user", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(text, report)

    def test_source_status_vocabulary(self):
        rows = read("sources/source-ledger.json")["sources"]
        self.assertEqual(len(rows), 18)
        self.assertTrue(set(row["status"] for row in rows) <= {"current", "stable", "draft", "watch"})

    def test_x1_commit_is_ancestor(self):
        result = subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT, check=False)
        self.assertEqual(result.returncode, 0)

    def test_x1_freeze_has_no_x2_credit(self):
        raw = subprocess.check_output(["git", "show", f"{X1}:docs/ilyra-fen/v646-v8/x1-proposals.json"], cwd=ROOT, text=True, encoding="utf-8")
        self.assertFalse(json.loads(raw)["x2_execution_present"])


def _proposal_test(index: int):
    def test(self):
        ledger = read("x2-proposal-ledger.json")
        row = next(item for item in ledger["outcomes"] if item["proposal_id"] == f"V6468-P{index:02d}")
        self.assertTrue(row["evidence_permitted_execution"])
        self.assertEqual(row["protected_gates_crossed"], [])
        for artifact in row["artifacts"]:
            self.assertTrue((PHASE / artifact).is_file(), artifact)
    return test


def _skill_test(index: int):
    def test(self):
        row = read("prototypes/skill-build-use-receipt.json")["skills"][index - 1]
        self.assertTrue(row["built"] and row["validated"] and row["smoke_used"])
        self.assertTrue((PHASE / row["path"]).is_file())
    return test


def _candidate_test(index: int):
    def test(self):
        row = read("prototypes/x2-candidate-execution.json")["candidates"][index - 1]
        self.assertTrue(row["x2_completion_credit"] and row["test_passed"])
        self.assertTrue((PHASE / row["witness_receipt"]).is_file())
    return test


for _index in range(1, 11):
    setattr(TestV646V8Evidence, f"test_proposal_{_index:02d}", _proposal_test(_index))
for _index in range(1, 21):
    setattr(TestV646V8Evidence, f"test_skill_{_index:02d}", _skill_test(_index))
    setattr(TestV646V8Evidence, f"test_candidate_{_index:02d}", _candidate_test(_index))


if __name__ == "__main__":
    unittest.main()
