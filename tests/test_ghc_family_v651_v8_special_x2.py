from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SpecialX2Tests(unittest.TestCase):
    def test_core_distribution(self):
        self.assertEqual(load("x2/core-outcome-ledger.json")["distribution"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_future_seats_are_unnamed_and_unlaunched(self):
        seats = load("cli/future-seat-placeholders.json")
        batch = load("cli/cli-batch-receipt.json")
        self.assertEqual((seats["named_cli_siblings"], seats["launched_cli_siblings"]), (0, 0))
        self.assertTrue(batch["all_unnamed"] and batch["all_unlaunched"])

    def test_all_prepare_and_launch_refusals(self):
        row = load("cli/cli-batch-receipt.json")
        self.assertEqual((row["prepare_passes"], row["launch_refusals"]), (8, 8))

    def test_mutation_tribunal(self):
        row = load("cli/mutation-tribunal.json")
        self.assertEqual((row["mutation_count"], row["rejected_count"]), (100, 100))

    def test_safe_now_portfolio(self):
        row = load("x2/safe-now-execution-ledger.json")
        self.assertEqual(row["count"], 40)
        self.assertTrue(all(item["state"] == "completed" for item in row["rows"]))

    def test_candidate_portfolio(self):
        row = load("x2/candidate-execution-ledger.json")
        self.assertEqual(row["count"], 30)
        self.assertTrue(all(item["state"] == "completed" for item in row["rows"]))

    def test_skill_portfolio(self):
        row = load("skills/skill-use-ledger.json")
        self.assertEqual((row["count"], row["validated"], row["smoke_used"], row["global_promotions"]), (20, 20, 20, 0))

    def test_runner_portfolio(self):
        row = load("runners/runner-use-ledger.json")
        self.assertEqual((row["count"], row["accept_passes"], row["reject_passes"]), (12, 12, 12))

    def test_cleanup_portfolio(self):
        row = load("maintenance/clean-fix-refine-ledger.json")
        self.assertEqual((row["count"], row["destructive_actions"]), (40, 0))

    def test_retained_negative_arithmetic(self):
        row = load("truth/retained-negative-register.json")
        self.assertEqual(row["effective_total"], 7855)
        self.assertEqual(row["effective_total"], row["inherited_ordinary"] + row["x1_operational"] + row["post_x1_lifecycle_operational"] + row["x2_operational"] + row["synthetic_cli_mutations"])

    def test_open_and_exact_gates(self):
        row = load("truth/open-exact-gate-register.json")
        self.assertEqual((row["effective_open_gaps"], row["effective_exact_gates"]), (61, 62))

    def test_terminal_truth(self):
        row = load("truth/phase-truth.json")
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(row["terminal_delivery_state"], "PREPARED_NOT_SENT")

    def test_sable_rollover(self):
        row = load("truth/phase-truth.json")
        self.assertEqual((row["immediate_successor"], row["immediate_successor_phase"]), ("Sable Rook", "v652-v1"))

    def test_method_flow_preserves_failures(self):
        row = load("method-flow/method-flow-ledger.json")
        self.assertEqual(row["counts"]["witness_results"], {"fail": 10, "pass": 8})
        self.assertEqual(row["counts"]["states"]["preferred"], 8)

    def test_meta_tool_catalogue(self):
        self.assertEqual(load("tooling/meta-tool-box-x2/meta-tool-catalogue.json")["card_count"], 20)
        self.assertTrue(load("tooling/meta-tool-box-x2/validation.json")["valid"])

    def test_baton_budget(self):
        row = load("handoffs/baton-word-budget.json")
        self.assertTrue(row["valid"])
        self.assertGreaterEqual(row["words"], 10_000)

    def test_primary_focus(self):
        row = load("truth/phase-truth.json")
        self.assertEqual(row["primary_focus"], "THOS Body")

    def test_no_global_installation(self):
        self.assertEqual(load("skills/skill-use-ledger.json")["global_promotions"], 0)

    def test_no_desktop_or_host_mutation(self):
        row = load("environment/environment-version-receipt.json")
        self.assertFalse(row["desktop_updated"] or row["elevation"] or row["host_security_weakened"] or row["windows_feature_changed"] or row["rebooted"])

    def test_zero_real_gmut_rows(self):
        row = load("gmut/radio-timing-zero-row-adapter.json")
        self.assertEqual(row["outcome"], "open_gap")
        self.assertEqual(row["details"]["real_rows"], 0)

    def test_authority_matrix_stays_exact_gate(self):
        row = load("freed-id-cbr/future-seat-authority-matrix.json")
        self.assertEqual(row["outcome"], "exact_gate")
        self.assertEqual(row["details"]["authority_decisions"], 0)


if __name__ == "__main__":
    unittest.main()
