from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v649-v3"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v649_v3_runtime import OUTCOMES, accepting_fixture, evaluate, execute_mutations


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SableV649V3X2Tests(unittest.TestCase):
    def test_exact_core_outcome_distribution(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["outcome_counts"], {"completed": 6, "exact_gate": 1, "open_gap": 1, "represented": 2})
        self.assertEqual({row["observed_outcome"] for row in ledger["proposals"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_all_accepting_fixtures_pass_their_bounded_contract(self) -> None:
        for proposal_id in OUTCOMES:
            result = evaluate(proposal_id, accepting_fixture(proposal_id))
            self.assertTrue(result["passed"], (proposal_id, result["issues"]))
            self.assertEqual(result["observed_outcome"], OUTCOMES[proposal_id])

    def test_all_seventy_preregistered_mutations_reject(self) -> None:
        rows = execute_mutations()
        self.assertEqual(len(rows), 70)
        self.assertEqual(sum(row["status"] == "rejected" for row in rows), 70)
        self.assertTrue(all(row["issue_count"] >= 1 for row in rows))

    def test_atnf_adapter_preserves_zero_row_and_likelihood_refusal(self) -> None:
        payload = load("empirical/atnf-psrcat-zero-row-receipt.json")
        fixture = payload["accepting_fixture"]
        for key in ("queries", "downloads", "catalogue_rows", "timing_rows", "covariance_rows", "likelihood_evaluations", "posterior_samples", "parameter_constraints", "force_detections"):
            self.assertEqual(fixture[key], 0)
        self.assertEqual(payload["observed_outcome"], "open_gap")

    def test_thos_and_did_profiles_remain_represented(self) -> None:
        thos = load("thos/food-bank-handover-contract.json")
        did = load("freed-id/did-resolution-profile.json")
        self.assertEqual((thos["observed_outcome"], did["observed_outcome"]), ("represented", "represented"))
        self.assertEqual((thos["real_participants_or_operators"], did["real_keys_or_proofs"]), (0, 0))

    def test_cbr_authority_matrix_stays_exact_gated(self) -> None:
        matrix = load("cbr/food-access-authority-matrix.json")
        self.assertEqual(matrix["observed_outcome"], "exact_gate")
        self.assertEqual(matrix["authority_decisions"], 0)
        self.assertTrue(all(value == "exact_gate" for value in matrix["accepting_fixture"]["decision_cells"].values()))

    def test_completed_formal_and_structural_surfaces_keep_boundaries(self) -> None:
        for relative in (
            "provenance/ro-crate-contract.json",
            "gmut/haag-kastler-contract.json",
            "security/fits-tribunal.json",
            "accessibility/risk-matrix-audit.json",
            "thermo-psyche/stefan-boltzmann-classifier.json",
            "stage20/equivalence-nonpromotion-board.json",
        ):
            payload = load(relative)
            self.assertEqual(payload["observed_outcome"], "completed")
            self.assertTrue(payload["accepting_result"]["passed"])
            self.assertEqual((payload["real_data_rows"], payload["real_participants_or_operators"], payload["real_keys_or_proofs"], payload["authority_decisions"]), (0, 0, 0, 0))

    def test_expanded_portfolios_meet_frozen_floors(self) -> None:
        safe = load("portfolios/safe-now-execution.json")
        candidates = load("portfolios/candidate-execution.json")
        skills = load("portfolios/skill-execution.json")
        runners = load("portfolios/runner-execution.json")
        cleanup = load("portfolios/clean-fix-refine-execution.json")
        self.assertEqual((safe["completed_bounded"], candidates["completed_bounded"], skills["valid_count"], runners["valid_count"], cleanup["completed_additive"]), (30, 20, 20, 10, 30))
        self.assertFalse(skills["global_install"])
        self.assertEqual(skills["subagent_forward_test"], "prohibited_not_run")

    def test_phase_local_skills_have_instructions_metadata_and_two_smoke_uses(self) -> None:
        skills = load("portfolios/skill-execution.json")
        for row in skills["skills"]:
            package = PHASE / "skills" / row["name"]
            self.assertTrue((package / "SKILL.md").is_file())
            self.assertTrue((package / "agents" / "openai.yaml").is_file())
            self.assertTrue((package / "scripts" / "check.py").is_file())
            self.assertEqual((row["quick_validation"], row["accepting_smoke_use"], row["rejecting_smoke_use"]), ("passed", "passed", "passed"))

    def test_family_runners_have_accepting_and_rejecting_witnesses(self) -> None:
        runners = load("portfolios/runner-execution.json")
        self.assertEqual(runners["valid_count"], 10)
        for row in runners["runners"]:
            self.assertTrue((ROOT / "scripts" / row["name"]).is_file())
            self.assertEqual((row["accepting_witness"], row["rejecting_witness"]), ("passed", "passed"))

    def test_retained_negatives_and_gates_are_not_compensated(self) -> None:
        negatives = load("retained-negative-register-evidence.json")
        gates = load("exact-open-gate-register-evidence.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational"], negatives["x2_operational"], negatives["synthetic_executed_rejected"]), (4840, 10, 4, 70))
        self.assertEqual(negatives["current_effective"], 4924)
        self.assertTrue(negatives["none_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (37, 38))
        self.assertTrue(gates["none_silently_closed"])

    def test_method_flow_x2_preserves_fail_and_pass_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-ledger-x2.json")
        receipt = load("method-flow/method-flow-validation-x2.json")
        self.assertEqual(ledger["counts"]["methods"], 11)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 14, "pass": 11})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 11)
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["issue_count"], 0)

    def test_accessible_report_reserves_manual_and_affected_user_review(self) -> None:
        report = (PHASE / "report" / "index.html").read_text(encoding="utf-8")
        reservation = load("accessibility/manual-reservation.json")
        self.assertIn('<html lang="en">', report)
        self.assertIn("<caption>", report)
        self.assertNotIn("autoplay", report.lower())
        self.assertFalse(reservation["complete_conformance_claim"])
        self.assertEqual((reservation["assistive_technology"], reservation["affected_user_review"]), ("reserved", "reserved"))

    def test_terminal_route_remains_held_and_stage20_not_ready(self) -> None:
        truth = load("phase-truth-evidence.json")
        route = load("orchestration/terminal-route-hold-evidence.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["canonical_successful_x2_passes_used"], 0)
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)


if __name__ == "__main__":
    unittest.main()
