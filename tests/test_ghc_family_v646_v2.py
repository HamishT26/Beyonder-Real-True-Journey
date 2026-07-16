from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V2EvidenceTests(unittest.TestCase):
    def test_core_distribution_and_bounded_artifacts(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        rows = ledger["proposals"]
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter(ledger["distribution"]))
        self.assertEqual(set(ledger["allowed_outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertFalse(ledger["independent_reproduction"])
        for row in rows:
            self.assertTrue(row["acceptance_gate_passed_within_scope"], row["proposal_id"])
            for key in ("primary_artifact", "vector_artifact"):
                self.assertTrue((PHASE / row[key]).is_file(), (row["proposal_id"], key))
            artifact = load(row["primary_artifact"])
            self.assertTrue(artifact["passed"], row["proposal_id"])
            self.assertEqual(artifact["outcome"], row["outcome"])

    def test_zero_real_evidence_counters_and_scientific_boundaries(self) -> None:
        gm = load("gmut/microscope-zero-row-receipt.json")
        self.assertEqual(gm["contract"]["observed_rows"], 0)
        self.assertEqual(gm["outcome"], "open_gap")
        thos = load("thos/seismic-catalogue-handover-contract.json")
        self.assertEqual(thos["real_analysts"], 0)
        self.assertEqual(thos["real_events"], 0)
        freed = load("freed-id/haip-profile-contract.json")
        self.assertEqual(freed["real_keys"], 0)
        self.assertEqual(freed["real_proofs"], 0)
        cbr = load("cbr/earthquake-alert-authority-matrix.json")
        self.assertEqual(cbr["real_people"], 0)
        self.assertEqual(cbr["cultural_or_maori_authority_claims"], 0)

    def test_expanded_portfolios_complete_only_within_scope(self) -> None:
        safe = load("approval-packets/x2-safe-now-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["count"], safe["completed"], len(safe["tasks"])), (30, 30, 30))
        self.assertEqual((candidates["count"], candidates["completed"], len(candidates["tasks"])), (20, 20, 20))
        self.assertEqual((cleanup["count"], cleanup["completed"], len(cleanup["tasks"])), (30, 30, 30))
        self.assertEqual(safe["unsafe_reclassification_count"], 0)
        self.assertEqual(cleanup["destructive_actions"], 0)
        for payload in (safe, candidates, cleanup):
            for row in payload["tasks"]:
                self.assertEqual(row["state"], "completed")
                self.assertTrue((PHASE / row["artifact"]).is_file(), row)

    def test_twenty_skills_and_ten_runners_built_used(self) -> None:
        skills = load("prototypes/skill-build-receipt.json")
        self.assertTrue(skills["valid"])
        self.assertEqual(skills["skill_count"], 20)
        self.assertEqual(skills["validated_count"], 20)
        self.assertEqual(skills["smoke_use_pass_count"], 20)
        self.assertEqual(skills["newly_initialized_count"], 19)
        self.assertEqual(skills["compatible_reused_count"], 1)
        self.assertEqual(skills["subagent_forward_tests"], 0)
        runners = load("prototypes/runner-build-use-receipt.json")
        self.assertTrue(runners["valid"])
        self.assertEqual((runners["runner_count"], runners["built_count"], runners["invoked_count"], runners["passed_count"]), (10, 10, 10, 10))
        self.assertTrue(all(row["family_current"] and row["passed"] for row in runners["runners"]))

    def test_negatives_and_gates_are_append_only(self) -> None:
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 2508)
        self.assertEqual(negatives["x1_operational"], 15)
        self.assertEqual(negatives["preregistered_synthetic_executed_and_rejected"], 70)
        self.assertGreaterEqual(negatives["x2_operational"], 10)
        self.assertEqual(
            negatives["effective_total"],
            negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic_executed_and_rejected"] + negatives["x2_operational"],
        )
        self.assertTrue(negatives["no_negative_erased"])
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["inherited_open_gaps"], gates["new_open_gaps"], gates["effective_open_gaps"]), (10, 1, 11))
        self.assertEqual((gates["inherited_exact_gates"], gates["new_exact_gates"], gates["effective_exact_gates"]), (11, 1, 12))
        self.assertEqual(gates["closed_without_exact_evidence"], 0)

    def test_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        protected = load("approval-packets/x2-protected-packet-register.json")
        self.assertEqual((protected["inherited_exact_count"], protected["inherited_blocked_count"]), (10, 5))
        self.assertEqual(protected["executed"], 0)
        self.assertEqual(protected["relabelled_safe_now"], 0)
        self.assertTrue(all(row["x2_execution"] == "do_not_execute" for row in protected["exact_packets"]))
        self.assertTrue(all(row["x2_execution"] == "prohibited_without_new_evidence" for row in protected["blocked_packets"]))

    def test_method_flow_retains_failures(self) -> None:
        method = load("method-flow/runner-validation.json")
        summary = load("method-flow/method-flow-summary.json")
        self.assertTrue(method["valid"])
        self.assertEqual(method["method_count"], summary["counts"]["methods"])
        self.assertEqual(method["witness_count"], summary["counts"]["witnesses"])
        self.assertGreaterEqual(summary["counts"]["witness_results"]["fail"], 25)
        self.assertGreaterEqual(summary["counts"]["witness_results"]["pass"], 17)
        self.assertEqual(summary["counts"]["states"]["candidate"], 0)

    def test_report_and_manual_evaluation_reservations(self) -> None:
        report = (PHASE / "deliverables/v646-v2-static-report.html").read_text(encoding="utf-8")
        for token in ("Skip to main content", "<caption>", 'scope="col"', "scope='row'", 'aria-labelledby="chart-title chart-desc"', 'data-table-ref="#outcome-table"', 'tabindex="0"'):
            self.assertIn(token, report)
        reservation = load("accessibility/svg-chart-contract.json")
        self.assertFalse(reservation["manual_keyboard_review"])
        self.assertFalse(reservation["assistive_technology_review"])
        self.assertFalse(reservation["affected_user_review"])

    def test_terminal_truth_remains_closed_and_unsent(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertTrue(truth["runners_built_and_used"])
        self.assertFalse(truth["runners_aggregate_use_pending"])
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(route["current_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)


if __name__ == "__main__":
    unittest.main()
