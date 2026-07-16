from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v647_v5_definitions as d  # noqa: E402

PHASE = ROOT / "docs/eiren-kestrel/v647-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V5EvidenceTests(unittest.TestCase):
    def test_core_distribution_and_artifacts(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len(ledger["outcomes"]), 10)
        for row in ledger["outcomes"]:
            self.assertIn(row["disposition"], d.OUTCOME_CLASSES)
            for relative in row["artifacts"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_priority_backpressure_and_adm_boundaries(self):
        queue = load("method-flow/priority-backpressure-contract.json")
        adm = load("gmut/adm-constraint-obligations.json")
        self.assertEqual(queue["external_side_effects"], 0)
        self.assertFalse(queue["production_scheduler_claim"])
        self.assertFalse(queue["distributed_consensus_claim"])
        self.assertFalse(adm["likelihood_evaluated"])
        self.assertFalse(adm["quantum_completion"])
        self.assertFalse(adm["theory_of_everything"])

    def test_pantheon_plus_zero_row(self):
        receipt = load("empirical/pantheon-plus-zero-row-receipt.json")
        self.assertEqual((receipt["archive_queries"], receipt["real_rows"], receipt["covariance_rows"], receipt["likelihood_evaluations"], receipt["posterior_samples"], receipt["parameter_constraints"], receipt["gmut_empirical_claims"]), (0, 0, 0, 0, 0, 0, 0))

    def test_thos_is_proxy(self):
        contract = load("thos/library-digital-handover-contract.json")
        self.assertEqual((contract["real_patrons"], contract["real_workers"], contract["real_accounts"], contract["real_borrowing_records"], contract["real_search_records"], contract["real_libraries"], contract["real_outages"]), (0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(contract["blind_matched_budget_arms"], 0)
        self.assertFalse(contract["operational_effectiveness_claim"])

    def test_freed_id_is_synthetic(self):
        profile = load("freed-id/oauth-par-profile.json")
        self.assertEqual((profile["real_clients"], profile["real_users"], profile["real_authorization_servers"], profile["real_tokens"], profile["real_keys"], profile["network_exchanges"]), (0, 0, 0, 0, 0, 0))
        self.assertFalse(profile["production_ready"])

    def test_cbr_remains_exact_gate(self):
        gate = load("cbr/library-authority-reservation.json")
        matrix = load("cbr/library-remedy-matrix.json")
        self.assertFalse(gate["authority_granted"])
        self.assertEqual((gate["affected_parties_consulted"], gate["tangata_whenua_iwi_hapu_maori_authority_participation"], gate["real_access_or_remedy_decisions"], gate["real_records_disclosed"]), (0, 0, 0, 0))
        self.assertEqual(matrix["decisions_made"], 0)
        self.assertTrue(all(row["decision"] == "reserved" for row in matrix["matrix"]))

    def test_protocol_accessibility_thermo_and_conformal_boundaries(self):
        protocol = load("tooling/git-protocol-v2-contract.json")
        access = load("accessibility/sortable-table-contract.json")
        thermo = load("thermo-psyche/helmholtz-domain-contract.json")
        conformal = load("stage20/conformal-prediction-contract.json")
        self.assertEqual(protocol["network_requests"], 0)
        self.assertFalse(access["complete_accessibility_conformance"])
        self.assertEqual(access["affected_user_evaluation"], "reserved")
        self.assertFalse(thermo["psyche_conversion"])
        self.assertFalse(thermo["fundamental_psyche_law"])
        self.assertFalse(conformal["stage20_promotion"])
        self.assertFalse(conformal["conditional_coverage_claim"])

    def test_expanded_portfolios_completed_and_gates_held(self):
        execution = load("approval-packets/x2-portfolio-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((execution["safe_completed"], execution["candidate_completed"], execution["exact_executed"], execution["blocked_executed"]), (30, 20, 0, 0))
        self.assertEqual(cleanup["completed_count"], 30)
        self.assertEqual(cleanup["files_deleted"], 0)
        self.assertFalse(cleanup["history_rewritten"])

    def test_twenty_phase_local_skills(self):
        receipt = load("prototypes/skill-build-use-receipt.json")
        self.assertEqual((receipt["skill_count"], receipt["built_count"], receipt["validated_count"], receipt["invoked_count"]), (20, 20, 20, 20))
        self.assertEqual(receipt["global_skill_changes"], 0)
        for row in receipt["skills"]:
            self.assertTrue((PHASE / row["path"]).is_file())

    def test_ten_family_current_runners(self):
        receipt = load("prototypes/runner-build-use-receipt.json")
        self.assertEqual((receipt["runner_count"], receipt["built_count"]), (10, 10))
        self.assertIn(receipt["invoked_count"], {9, 10})
        self.assertTrue(receipt["compatibility_preserved"])
        for row in receipt["runners"]:
            self.assertTrue((ROOT / row["path"]).is_file())

    def test_seventy_synthetic_negatives(self):
        data = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((data["count"], data["executed_count"], data["rejected_or_quarantined_count"], data["erased_count"]), (70, 70, 70, 0))
        self.assertEqual(len({row["negative_id"] for row in data["negatives"]}), 70)

    def test_negative_gate_and_truth_counts(self):
        negative = load("retained-negative-register.json")
        x2 = load("validation/x2-operational-negatives.json")
        gates = load("exact-open-gate-register.json")
        truth = load("phase-truth.json")
        self.assertEqual(negative["effective_total"], 3493 + len(d.X1_OPERATIONAL_NEGATIVES) + 70 + x2["count"])
        self.assertEqual(negative["failure_erasure_count"], 0)
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]), (22, 23, 0))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_method_flow_preserves_failures_and_recoveries(self):
        method = load("method-flow/method-flow-state.json")
        x2 = load("validation/x2-operational-negatives.json")
        unique_new_methods = {row["method_id"] for row in x2["negatives"]} - {row["method_id"] for row in d.X1_OPERATIONAL_NEGATIVES}
        self.assertEqual(method["counts"]["methods"], len(d.X1_OPERATIONAL_NEGATIVES) + len(unique_new_methods))
        self.assertEqual(method["counts"]["witness_results"]["fail"], method["counts"]["witness_results"]["pass"])
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], method["counts"]["methods"])
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in method["methods"]))

    def test_static_report_structure(self):
        report = (PHASE / "deliverables/v647-v5-evidence-report.html").read_text(encoding="utf-8").lower()
        for marker in ("<html lang=", "<main", "<h1", "<table", "<caption", "scope=\"col\"", "not_ready_for_stage_20", "manual", "affected-user"):
            self.assertIn(marker, report)
        self.assertNotIn("<script", report)

    def test_overview_and_wellbeing_word_limits(self):
        for relative in ("v647-v5-integrated-overview.md", "deliverables/v647-v5-x2-wellbeing.md"):
            count = len((PHASE / relative).read_text(encoding="utf-8").split())
            self.assertLessEqual(count, 6000)
        self.assertGreaterEqual(len((PHASE / "v647-v5-integrated-overview.md").read_text(encoding="utf-8").split()), 900)

    def test_no_closeout_before_evidence_commit(self):
        result = subprocess.run(["git", "log", "-1", "--format=%H", "--", "docs/eiren-kestrel/v647-v5/evidence-receipt.json"], cwd=ROOT, capture_output=True, text=True, check=True)
        evidence_commit = result.stdout.strip()
        if not evidence_commit:
            self.assertFalse((PHASE / "closeout-receipt.json").exists())
            return
        for relative in ("closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
            repository_relative = f"docs/eiren-kestrel/v647-v5/{relative}"
            result = subprocess.run(["git", "cat-file", "-e", f"{evidence_commit}:{repository_relative}"], cwd=ROOT, capture_output=True)
            self.assertNotEqual(result.returncode, 0, relative)


if __name__ == "__main__":
    unittest.main()
