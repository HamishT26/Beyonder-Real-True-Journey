from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V4EvidenceTests(unittest.TestCase):
    def test_core_distribution_and_bounded_artifacts(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        expected = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["distribution"], expected)
        self.assertEqual(Counter(row["outcome"] for row in ledger["proposals"]), Counter(expected))
        self.assertEqual(set(ledger["allowed_outcomes"]), set(expected))
        self.assertFalse(ledger["independent_reproduction"])
        for row in ledger["proposals"]:
            self.assertTrue(row["acceptance_gate_passed_within_scope"], row["proposal_id"])
            for key in ("primary_artifact", "vector_artifact"):
                self.assertTrue((PHASE / row[key]).is_file(), (row["proposal_id"], key))
            artifact = load(row["primary_artifact"])
            self.assertTrue(artifact["passed"], row["proposal_id"])
            self.assertEqual(artifact["outcome"], row["outcome"])

    def test_zero_real_evidence_counters_and_boundaries(self) -> None:
        act = load("gmut/act-dr6-lensing-adapter-contract.json")
        self.assertEqual((act["products_downloaded"], act["maps_ingested"], act["rows_ingested"], act["likelihood_evaluations"], act["posterior_samples"], act["constraints"]), (0, 0, 0, 0, 0, 0))
        self.assertEqual(act["outcome"], "open_gap")
        thos = load("thos/pharmacy-compounding-handover-contract.json")
        self.assertEqual((thos["real_preparations"], thos["real_patients"], thos["real_pharmacists"], thos["real_pharmacies"], thos["blind_matched_budget_real_arms"]), (0, 0, 0, 0, 0))
        freed = load("freed-id/bbs-derived-proof-profile.json")
        self.assertEqual((freed["real_keys"], freed["real_proofs"], freed["real_credentials"], freed["interoperability_events"]), (0, 0, 0, 0))
        recall = load("cbr/medicine-recall-authority-matrix.json")
        self.assertEqual((recall["real_people"], recall["real_recalls"], recall["health_decisions"], recall["legal_decisions"], recall["cultural_or_maori_authority_claims"]), (0, 0, 0, 0, 0))

    def test_expanded_portfolios_complete_only_within_scope(self) -> None:
        safe = load("approval-packets/x2-safe-now-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["count"], safe["completed"], len(safe["tasks"])), (30, 30, 30))
        self.assertEqual((candidates["count"], candidates["completed"], len(candidates["tasks"])), (20, 20, 20))
        self.assertEqual((cleanup["count"], cleanup["completed"], len(cleanup["tasks"])), (30, 30, 30))
        self.assertEqual(cleanup["destructive_actions"], 0)
        for payload in (safe, candidates, cleanup):
            for row in payload["tasks"]:
                self.assertEqual(row["state"], "completed")
                self.assertTrue((PHASE / row["artifact"]).is_file(), row)

    def test_twenty_skills_and_ten_runner_surfaces(self) -> None:
        skills = load("prototypes/skill-build-receipt.json")
        self.assertTrue(skills["valid"])
        self.assertEqual((skills["skill_count"], skills["validated_count"], skills["smoke_use_pass_count"]), (20, 20, 20))
        self.assertEqual(skills["subagent_forward_tests"], 0)
        runners = load("prototypes/runner-build-use-receipt.json")
        self.assertEqual((runners["runner_count"], runners["built_count"]), (10, 10))
        self.assertTrue(runners["valid"] or runners["preflight_valid"])
        self.assertTrue(all(row["family_current"] and row["built"] for row in runners["runners"]))

    def test_negatives_and_gates_are_append_only(self) -> None:
        negatives = load("retained-negative-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational"], negatives["preregistered_synthetic_executed_and_rejected"]), (2704, 16, 70))
        self.assertGreaterEqual(negatives["x2_operational"], 3)
        self.assertEqual(negatives["effective_total"], negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic_executed_and_rejected"] + negatives["x2_operational"])
        self.assertTrue(negatives["no_negative_erased"])
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["inherited_open_gaps"], gates["new_open_gaps"], gates["effective_open_gaps"]), (12, 1, 13))
        self.assertEqual((gates["inherited_exact_gates"], gates["new_exact_gates"], gates["effective_exact_gates"]), (13, 1, 14))
        self.assertEqual(gates["closed_without_exact_evidence"], 0)

    def test_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        protected = load("approval-packets/x2-protected-packet-register.json")
        self.assertEqual((protected["inherited_exact_count"], protected["inherited_blocked_count"]), (10, 5))
        self.assertEqual((protected["executed"], protected["relabelled_safe_now"]), (0, 0))

    def test_method_flow_retains_failures_and_recoveries(self) -> None:
        method = load("method-flow/runner-validation.json")
        summary = load("method-flow/method-flow-summary.json")
        self.assertTrue(method["valid"])
        self.assertEqual(method["method_count"], summary["counts"]["methods"])
        self.assertEqual(method["witness_count"], summary["counts"]["witnesses"])
        self.assertGreaterEqual(summary["counts"]["witness_results"]["fail"], 19)
        self.assertGreaterEqual(summary["counts"]["witness_results"]["pass"], 19)
        ledger = load("method-flow/method-flow-state.json")
        candidates = {row["method_id"] for row in ledger["methods"] if row["recommendation_state"] == "candidate"}
        self.assertTrue(candidates <= {"V6464-M21"}, candidates)

    def test_report_and_manual_evaluation_reservations(self) -> None:
        report = (PHASE / "deliverables/v646-v4-static-report.html").read_text(encoding="utf-8")
        for token in ("Skip to main content", "<caption>", 'scope="col"', "scope='row'", 'aria-labelledby="chart-title chart-desc"', 'data-table-ref="#outcome-table"', 'tabindex="0"', "Download the proposal outcome data", "sonification"):
            self.assertIn(token, report)
        reservation = load("accessibility/form-error-contract.json")
        self.assertFalse(reservation["manual_keyboard_review"])
        self.assertFalse(reservation["assistive_technology_review"])
        self.assertFalse(reservation["affected_user_review"])

    def test_git_fixture_and_environment_board_are_bounded(self) -> None:
        git_fixture = load("tooling/git-alternate-tribunal.json")
        self.assertTrue(git_fixture["passed"])
        self.assertTrue(git_fixture["fixture_removed"])
        environment = load("stage20/environment-lock-contract.json")
        self.assertTrue(environment["passed"])
        self.assertFalse(environment["independent_reproduction"])
        self.assertEqual(environment["stage20_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_terminal_truth_remains_closed_and_unsent(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual((route["current_state"], route["send_count"]), ("PREPARED_NOT_SENT", 0))


if __name__ == "__main__":
    unittest.main()
