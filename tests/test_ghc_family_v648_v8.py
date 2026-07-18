from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.ghc_family_v648_v8_runtime import DISPOSITIONS, SPECS, evaluate, mutated_fixture, valid_fixture


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"


class SylvenV648V8EvidenceTests(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_all_valid_core_fixtures_pass(self) -> None:
        for proposal_id in sorted(SPECS):
            self.assertTrue(evaluate(proposal_id, valid_fixture(proposal_id))["accepted"], proposal_id)

    def test_all_seventy_mutations_reject(self) -> None:
        for proposal_id in sorted(SPECS):
            for index in range(1, 8):
                self.assertFalse(evaluate(proposal_id, mutated_fixture(proposal_id, index))["accepted"], f"{proposal_id}:{index}")
        result = self.load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual((result["count"], result["executed_count"], result["rejected_count"]), (70, 70, 70))
        self.assertTrue(result["all_rejected"])

    def test_core_distribution(self) -> None:
        ledger = self.load("x2/core-outcome-ledger.json")
        self.assertEqual(ledger["count"], 10)
        self.assertEqual(ledger["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual({row["proposal_id"]: row["disposition"] for row in ledger["outcomes"]}, DISPOSITIONS)

    def test_mightee_remains_zero_row(self) -> None:
        row = self.load("empirical/mightee-dr1-zero-row-receipt.json")
        for field in ["queries", "downloads", "real_rows", "catalogue_matches", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_gmut_claims"]:
            self.assertEqual(row[field], 0)
        self.assertEqual(row["status"], "open_gap")

    def test_thos_is_synthetic_proxy(self) -> None:
        row = self.load("thos/water-treatment-reality-boundary.json")
        self.assertTrue(all(row[field] == 0 for field in ["real_workers", "real_suppliers", "real_treatment_plants", "real_samples", "real_incidents", "blind_matched_budget_arms", "effectiveness_estimates"]))
        self.assertEqual(row["status"], "represented")

    def test_freed_id_is_nonproduction(self) -> None:
        row = self.load("freed-id/resource-indicator-reality-boundary.json")
        self.assertTrue(all(value == 0 for key, value in row.items() if key != "status"))
        self.assertEqual(row["status"], "represented")

    def test_cbr_authority_is_reserved(self) -> None:
        row = self.load("cbr/water-authority-reservation.json")
        self.assertEqual(row["status"], "exact_gate")
        self.assertTrue(all(row[field] == 0 for field in ["real_notices", "real_disclosures", "real_remedy_allocations", "real_authority_decisions"]))
        self.assertIn("Maori authority", row["reserved_for"])

    def test_expanded_portfolios_complete(self) -> None:
        row = self.load("x2/portfolio-ledger.json")
        self.assertEqual((row["safe_completed"], row["candidates_completed"], row["skills_completed"], row["runners_completed"], row["clean_refine_completed"]), (30, 20, 20, 10, 30))
        self.assertEqual(row["inherited_completion_credit"], 0)

    def test_phase_local_skills_validated_and_not_installed(self) -> None:
        row = self.load("x2/skill-use-ledger.json")
        self.assertEqual((row["skill_count"], row["completed_count"]), (20, 20))
        self.assertFalse(row["global_install"])
        self.assertFalse(row["subagent_forward_test"])
        self.assertTrue(all(item["quick_validate_passed"] and item["smoke_used"] for item in row["skills"]))

    def test_all_runners_invoked_on_pass_and_reject(self) -> None:
        row = self.load("x2/runner-use-ledger.json")
        self.assertEqual((row["runner_count"], row["completed_count"]), (10, 10))
        self.assertTrue(all(item["valid_passed"] and item["mutation_rejected"] for item in row["runners"]))

    def test_negative_and_gate_counts(self) -> None:
        negatives = self.load("retained-negative-register-x2.json")
        gates = self.load("exact-open-gate-register-x2.json")
        self.assertEqual(negatives["effective_total"], 4656)
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual((gates["open_gaps"], gates["exact_gates"], gates["silently_closed"]), (34, 35, 0))

    def test_phase_truth_boundaries(self) -> None:
        row = self.load("phase-truth-x2.json")
        self.assertFalse(row["full_suite_used"])
        self.assertFalse(row["replay_used"])
        self.assertFalse(row["independent_reproduction"])
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
