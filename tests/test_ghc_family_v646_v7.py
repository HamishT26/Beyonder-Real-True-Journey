from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v646_v7_definitions as d  # noqa: E402

PHASE = ROOT / "docs/eiren-kestrel/v646-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V7EvidenceTests(unittest.TestCase):
    def test_core_distribution_and_artifacts(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len(ledger["outcomes"]), 10)
        for row in ledger["outcomes"]:
            self.assertIn(row["disposition"], d.OUTCOME_CLASSES)
            for relative in row["artifacts"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_fencing_and_functional_rg_boundaries(self):
        fence = load("method-flow/fencing-token-contract.json")
        rg = load("gmut/wetterich-flow-obligations.json")
        self.assertEqual(fence["external_side_effects"], 0)
        self.assertFalse(fence["production_consensus_claim"])
        self.assertFalse(fence["exactly_once_claim"])
        self.assertFalse(rg["likelihood_evaluated"])
        self.assertFalse(rg["ultraviolet_completion"])
        self.assertFalse(rg["theory_of_everything"])

    def test_icecube_zero_row(self):
        receipt = load("empirical/icecube-zero-row-receipt.json")
        self.assertEqual((receipt["real_rows"], receipt["likelihood_evaluations"], receipt["posterior_samples"], receipt["constraints"], receipt["gmut_empirical_claims"]), (0, 0, 0, 0, 0))

    def test_thos_is_proxy(self):
        contract = load("thos/wildfire-handover-contract.json")
        self.assertEqual((contract["real_incidents"], contract["real_firefighters"], contract["real_residents"], contract["real_alerts"]), (0, 0, 0, 0))
        self.assertEqual(contract["blind_matched_budget_arms"], 0)
        self.assertFalse(contract["operational_effectiveness_claim"])

    def test_freed_id_is_synthetic(self):
        profile = load("freed-id/oauth-rar-profile.json")
        self.assertEqual((profile["real_clients"], profile["real_authorization_servers"], profile["real_tokens"], profile["real_keys"], profile["network_exchanges"]), (0, 0, 0, 0, 0))
        self.assertFalse(profile["production_ready"])

    def test_cbr_remains_exact_gate(self):
        gate = load("cbr/wildfire-authority-reservation.json")
        matrix = load("cbr/wildfire-remedy-matrix.json")
        self.assertFalse(gate["authority_granted"])
        self.assertEqual((gate["affected_parties_consulted"], gate["maori_authority_participation"], gate["real_alert_or_zone_decision"]), (0, 0, 0))
        self.assertEqual(matrix["decisions_made"], 0)
        self.assertTrue(all(row["decision"] == "reserved" for row in matrix["matrix"]))

    def test_http_accessibility_thermo_and_mnar(self):
        http = load("tooling/http-resume-contract.json")
        access = load("accessibility/authentication-contract.json")
        thermo = load("thermo-psyche/le-chatelier-contract.json")
        mnar = load("stage20/mnar-sensitivity-contract.json")
        self.assertEqual(http["network_requests"], 0)
        self.assertFalse(access["complete_accessibility_conformance"])
        self.assertEqual(access["affected_user_evaluation"], "reserved")
        self.assertFalse(thermo["psyche_conversion"])
        self.assertFalse(thermo["fundamental_psyche_law"])
        self.assertFalse(mnar["stage20_promotion"])
        self.assertFalse(mnar["causal_identification"])

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
        gates = load("exact-open-gate-register.json")
        truth = load("phase-truth.json")
        self.assertEqual(negative["effective_total"], 2977 + len(d.X1_OPERATIONAL_NEGATIVES) + 70 + len(d.X2_OPERATIONAL_NEGATIVES))
        self.assertEqual(negative["failure_erasure_count"], 0)
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]), (16, 17, 0))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_method_flow_preserves_failures_and_recoveries(self):
        method = load("method-flow/method-flow-state.json")
        self.assertEqual(method["counts"]["methods"], len(d.X1_OPERATIONAL_NEGATIVES) + len(d.X2_OPERATIONAL_NEGATIVES))
        self.assertEqual(method["counts"]["witness_results"]["fail"], method["counts"]["witness_results"]["pass"])
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], method["counts"]["methods"])
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in method["methods"]))

    def test_static_report_structure(self):
        report = (PHASE / "deliverables/v646-v7-evidence-report.html").read_text(encoding="utf-8").lower()
        for marker in ("<html lang=", "<main", "<h1", "<table", "<caption", "scope=\"col\"", "not_ready_for_stage_20", "manual", "affected-user"):
            self.assertIn(marker, report)
        self.assertNotIn("<script", report)

    def test_overview_and_wellbeing_word_limits(self):
        for relative in ("v646-v7-integrated-overview.md", "deliverables/v646-v7-x2-wellbeing.md"):
            count = len((PHASE / relative).read_text(encoding="utf-8").split())
            self.assertLessEqual(count, 6000)
        self.assertGreaterEqual(len((PHASE / "v646-v7-integrated-overview.md").read_text(encoding="utf-8").split()), 900)

    def test_no_closeout_before_evidence_commit(self):
        for relative in ("closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
            self.assertFalse((PHASE / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
