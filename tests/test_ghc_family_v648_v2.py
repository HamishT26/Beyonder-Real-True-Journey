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

from ghc_family_v648_v2_runtime import PHASE_DIR, SURFACES  # noqa: E402


def load(relative: str):
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


class V648V2EvidenceTests(unittest.TestCase):
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

    def test_advisory_lock_guard(self) -> None:
        fixture = load("method-flow/advisory-lock-contract.json")["positive_fixture"]
        self.assertTrue(fixture["owner_token_bound"])
        self.assertTrue(fixture["pid_reuse_checked"])
        self.assertFalse(fixture["pid_only_ownership"])
        self.assertFalse(fixture["unowned_break_allowed"])

    def test_kms_remains_symbolic(self) -> None:
        fixture = load("gmut/kms-obligations.json")["positive_fixture"]
        self.assertTrue(fixture["analytic_strip_declared"])
        self.assertTrue(fixture["operator_order_preserved"])
        self.assertFalse(fixture["physical_state_claimed"])
        self.assertFalse(fixture["empirical_claimed"])

    def test_lotss_dr2_remains_zero_row(self) -> None:
        fixture = load("empirical/lotss-dr2-study-contract.json")["positive_fixture"]
        for key in ("queries", "downloads", "images", "catalog_rows", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_claims"):
            self.assertEqual(fixture[key], 0, key)

    def test_thos_remains_represented(self) -> None:
        contract = load("thos/machining-handover-contract.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertEqual(
            (fixture["real_workers"], fixture["real_employers"], fixture["real_machines"], fixture["real_jobs"], fixture["real_parts"], fixture["real_measurements"], fixture["real_incidents"]),
            (0, 0, 0, 0, 0, 0, 0),
        )

    def test_freed_id_remains_nonproduction(self) -> None:
        contract = load("freed-id/jarm-profile.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertEqual((fixture["real_keys"], fixture["real_clients"], fixture["live_authorization_servers"], fixture["real_tokens"], fixture["interoperability_events"]), (0, 0, 0, 0, 0))
        self.assertFalse(fixture["production"])

    def test_cbr_remains_exact_gate(self) -> None:
        contract = load("cbr/machining-authority-reservation.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "exact_gate")
        reserved = [value for key, value in fixture.items() if key != "case_data"]
        self.assertTrue(reserved)
        self.assertTrue(all(value == "reserved" for value in reserved))

    def test_zstandard_frame_guard(self) -> None:
        fixture = load("tooling/zstd-frame-contract.json")["positive_fixture"]
        self.assertEqual(fixture["magic"], "28b52ffd")
        self.assertTrue(fixture["window_bounded"])
        self.assertTrue(fixture["last_block_required"])
        self.assertFalse(fixture["user_material_decoded"])

    def test_progressbar_reserves_manual_evaluation(self) -> None:
        fixture = load("accessibility/progressbar-contract.json")["positive_fixture"]
        self.assertTrue(fixture["role_declared"])
        self.assertTrue(fixture["indeterminate_omits_value_now"])
        self.assertTrue(fixture["manual_evaluation_reserved"])

    def test_gibbs_adsorption_category_barrier(self) -> None:
        fixture = load("thermo-psyche/gibbs-adsorption-contract.json")["positive_fixture"]
        self.assertTrue(fixture["dividing_surface_declared"])
        self.assertTrue(fixture["surface_excess_defined"])
        self.assertFalse(fixture["psyche_or_agency_conversion"])

    def test_synthetic_control_nonpromotion(self) -> None:
        fixture = load("stage20/synthetic-control-contract.json")["positive_fixture"]
        self.assertTrue(fixture["pre_treatment_fit_required"])
        self.assertTrue(fixture["placebos_required"])
        self.assertFalse(fixture["participant_effect_estimated"])
        self.assertFalse(fixture["stage20_ready"])

    def test_portfolio_floors_completed(self) -> None:
        safe = load("approval-packets/x2-portfolio-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["completed"], candidates["completed"], cleanup["completed"]), (30, 20, 30))
        self.assertEqual((safe["exact_or_blocked_execution_credit"], cleanup["destructive_actions"], cleanup["sibling_mutations"]), (0, 0, 0))

    def test_skills_and_runners_built_and_used(self) -> None:
        skills = load("skills/skill-build-receipt.json")
        runners = load("tooling/runner-execution.json")
        self.assertEqual((skills["count"], skills["quick_validated"], skills["smoke_used"]), (20, 20, 20))
        self.assertEqual((skills["global_installations"], skills["subagent_forward_tests"]), (0, 0))
        self.assertEqual((runners["planned_count"], runners["built_count"], runners["used_count"]), (10, 10, 10))

    def test_negative_arithmetic_and_gates(self) -> None:
        negatives = load("retained-negative-register.json")
        gates = load("exact-open-gate-register.json")
        self.assertEqual(negatives["effective_total"], negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"])
        x2_failures = load("validation/x2-operational-negatives.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational"], negatives["preregistered_synthetic"]), (3938, 7, 70))
        self.assertEqual(negatives["x2_operational"], x2_failures["count"])
        self.assertGreaterEqual(negatives["x2_operational"], 8)
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (27, 28))

    def test_overview_and_report_boundaries(self) -> None:
        overview = (PHASE_DIR / "v648-v2-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE_DIR / "deliverables" / "v648-v2-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        for phrase in ("NOT_READY_FOR_STAGE_20", "same-owner", "independent-team", "Māori authority"):
            self.assertIn(phrase, overview)
        for token in ('lang="en"', 'href="#main"', 'aria-label="Report sections"', "<caption>", 'scope="col"'):
            self.assertIn(token, report)

    def test_method_flow_retains_fail_and_pass_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-state.json")
        results = Counter(row["result"] for row in ledger["witnesses"])
        self.assertGreaterEqual(results["fail"], 13)
        self.assertEqual(results["fail"], results["pass"])
        self.assertGreaterEqual(results["fail"], ledger["counts"]["methods"])
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))


if __name__ == "__main__":
    unittest.main()
