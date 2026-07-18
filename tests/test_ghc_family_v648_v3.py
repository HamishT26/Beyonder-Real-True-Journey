from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_v648_v3_runtime import PHASE_DIR, SURFACES  # noqa: E402


def load(relative: str):
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


class V648V3EvidenceTests(unittest.TestCase):
    def test_exact_outcome_distribution(self) -> None:
        rows = load("x2-proposal-ledger.json")["rows"]
        self.assertEqual(len(rows), 10)
        self.assertEqual(
            Counter(row["outcome"] for row in rows),
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        )

    def test_all_seventy_mutations_rejected(self) -> None:
        payload = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((payload["count"], payload["executed"], payload["rejected"]), (70, 70, 70))
        self.assertTrue(all(row["retained"] and not row["completion_credit"] for row in payload["rows"]))

    def test_all_core_contracts_and_witnesses_exist(self) -> None:
        for proposal_id, spec in SURFACES.items():
            with self.subTest(proposal_id=proposal_id):
                self.assertTrue((PHASE_DIR / spec["contract"]).is_file())
                self.assertTrue((PHASE_DIR / spec["mutations"]).is_file())
                self.assertTrue((PHASE_DIR / "validation" / "runner-witnesses" / f"{spec['slug']}.json").is_file())
                self.assertEqual(load(spec["mutations"])["rejected"], 7)

    def test_context_budget_guard(self) -> None:
        fixture = load("tooling/context-budget-handoff-contract.json")["positive_fixture"]
        self.assertLessEqual(fixture["composer_characters"], fixture["composer_character_cap"])
        self.assertTrue(fixture["artifact_pointer_declared"] and fixture["sha256_declared"])
        self.assertTrue(fixture["duplicate_draft_guard"])
        self.assertFalse(fixture["inline_zip_or_folder"] or fixture["send_credit_before_ack"])

    def test_tomita_takesaki_remains_symbolic(self) -> None:
        fixture = load("gmut/tomita-takesaki-obligations.json")["positive_fixture"]
        self.assertTrue(fixture["tomita_operator_closable"])
        self.assertTrue(fixture["polar_decomposition_declared"])
        self.assertTrue(fixture["modular_automorphism_group_declared"])
        self.assertFalse(fixture["physical_state_claimed"] or fixture["empirical_claimed"])

    def test_desi_dr2_lya_remains_zero_row(self) -> None:
        fixture = load("empirical/desi-dr2-lya-study-contract.json")["positive_fixture"]
        for key in ("queries", "downloads", "spectra_rows", "correlation_bins", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_claims"):
            self.assertEqual(fixture[key], 0, key)

    def test_thos_remains_represented(self) -> None:
        contract = load("thos/identity-incident-handover-contract.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertEqual(
            (fixture["real_people"], fixture["real_accounts"], fixture["real_credentials"], fixture["real_breaches"], fixture["real_notifications"]),
            (0, 0, 0, 0, 0),
        )

    def test_freed_id_remains_draft_and_nonproduction(self) -> None:
        contract = load("freed-id/subordinate-events-profile.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertTrue(fixture["draft_status_declared"])
        self.assertEqual((fixture["real_keys"], fixture["live_federations"], fixture["real_events"]), (0, 0, 0))
        self.assertFalse(fixture["production"])

    def test_cbr_remains_exact_gate(self) -> None:
        contract = load("cbr/identity-incident-authority-reservation.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "exact_gate")
        reserved = [value for key, value in fixture.items() if key != "case_data"]
        self.assertTrue(reserved and all(value == "reserved" for value in reserved))

    def test_nexus_is_design_only(self) -> None:
        fixture = load("security/six-node-nexus-threat-model.json")["positive_fixture"]
        self.assertTrue(fixture["guest_admin_broker_human_controlled"])
        self.assertTrue(fixture["east_west_default_deny"])
        self.assertFalse(fixture["host_shares_writable"])
        self.assertEqual(fixture["host_changes_executed"], 0)

    def test_artifact_pointer_reserves_manual_evaluation(self) -> None:
        fixture = load("accessibility/artifact-pointer-contract.json")["positive_fixture"]
        self.assertTrue(fixture["link_purpose_in_context"])
        self.assertTrue(fixture["focus_preserved"])
        self.assertTrue(fixture["manual_evaluation_reserved"])

    def test_thermodynamic_length_category_barrier(self) -> None:
        fixture = load("thermo-psyche/thermodynamic-length-contract.json")["positive_fixture"]
        self.assertTrue(fixture["linear_response_regime_declared"])
        self.assertTrue(fixture["friction_tensor_positive_semidefinite"])
        self.assertFalse(fixture["psyche_or_agency_conversion"])

    def test_proximal_causal_nonpromotion(self) -> None:
        fixture = load("stage20/proximal-causal-contract.json")["positive_fixture"]
        self.assertTrue(fixture["completeness_assumptions_declared"])
        self.assertTrue(fixture["existence_and_uniqueness_distinguished"])
        self.assertFalse(fixture["participant_effect_estimated"] or fixture["stage20_ready"])

    def test_portfolio_floors_completed(self) -> None:
        safe = load("approval-packets/x2-portfolio-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["completed"], candidates["completed"], cleanup["completed"]), (30, 20, 60))
        self.assertEqual((safe["exact_or_blocked_execution_credit"], cleanup["destructive_actions"], cleanup["sibling_mutations"]), (0, 0, 0))

    def test_skills_and_runners_built_and_used(self) -> None:
        skills = load("skills/skill-build-receipt.json")
        runners = load("tooling/runner-execution.json")
        self.assertEqual((skills["count"], skills["quick_validated"], skills["smoke_used"]), (20, 20, 20))
        self.assertEqual((skills["global_installations"], skills["subagent_forward_tests"]), (0, 0))
        self.assertEqual((runners["planned_count"], runners["built_count"], runners["used_count"]), (10, 10, 10))

    def test_negative_arithmetic_gates_and_no_replay_credit(self) -> None:
        negatives = load("retained-negative-register.json")
        gates = load("exact-open-gate-register.json")
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(negatives["effective_total"], negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"])
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational"], negatives["preregistered_synthetic"], negatives["x2_operational"]), (4032, 10, 70, 3))
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (28, 29))
        self.assertFalse(route["requires_one_named_replay"])
        self.assertEqual(route["repeatability_credit"], 0)
        self.assertFalse(route["independent_reproduction"])

    def test_overview_and_report_boundaries(self) -> None:
        overview = (PHASE_DIR / "v648-v3-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE_DIR / "deliverables" / "v648-v3-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1200)
        for phrase in ("NOT_READY_FOR_STAGE_20", "repeatability credit is exactly zero", "Māori authority", "PREPARED_NOT_SENT"):
            self.assertIn(phrase, overview)
        for token in ('lang="en"', 'href="#main"', "<caption>", 'scope="col"'):
            self.assertIn(token, report)

    def test_method_flow_retains_fail_and_pass_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        results = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual((results["fail"], results["pass"]), (14, 14))
        self.assertGreaterEqual(results["fail"], ledger["counts"]["methods"])
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))


if __name__ == "__main__":
    unittest.main()
