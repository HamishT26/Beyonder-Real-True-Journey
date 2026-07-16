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

from ghc_family_v647_v3_runtime import PHASE_DIR, SURFACES  # noqa: E402


def load(relative: str):
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


class V647V3EvidenceTests(unittest.TestCase):
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

    def test_child_process_lifecycle_guard(self) -> None:
        fixture = load("method-flow/child-process-lifecycle-contract.json")["positive_fixture"]
        self.assertTrue(fixture["parent_write_ends_closed_before_read"])
        self.assertTrue(fixture["all_descendants_joined"])
        self.assertTrue(fixture["teardown_confined"])

    def test_heat_kernel_remains_symbolic(self) -> None:
        fixture = load("gmut/heat-kernel-obligations.json")["positive_fixture"]
        self.assertTrue(fixture["eft_truncation_declared"])
        self.assertFalse(fixture["anomaly_freedom_proved"])
        self.assertFalse(fixture["physical_observable_claimed"])

    def test_hsc_remains_zero_row(self) -> None:
        fixture = load("empirical/hsc-pdr3-study-contract.json")["positive_fixture"]
        for key in ("queries", "downloads", "catalog_rows", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_claims"):
            self.assertEqual(fixture[key], 0, key)

    def test_thos_remains_represented(self) -> None:
        contract = load("thos/telecom-change-handover-contract.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertEqual((fixture["real_operators"], fixture["real_networks"], fixture["real_customers"], fixture["real_changes"]), (0, 0, 0, 0))

    def test_freed_id_remains_nonproduction(self) -> None:
        contract = load("freed-id/vc-related-resource-profile.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "represented")
        self.assertFalse(fixture["live_retrieval"])
        self.assertFalse(fixture["real_credential"])
        self.assertFalse(fixture["real_key"])
        self.assertFalse(fixture["production"])

    def test_cbr_remains_exact_gate(self) -> None:
        contract = load("cbr/telecom-outage-authority-reservation.json")
        fixture = contract["positive_fixture"]
        self.assertEqual(contract["outcome"], "exact_gate")
        reserved = [value for key, value in fixture.items() if key != "case_data"]
        self.assertTrue(reserved)
        self.assertTrue(all(value == "reserved" for value in reserved))

    def test_structured_fields_guard(self) -> None:
        fixture = load("tooling/http-structured-fields-contract.json")["positive_fixture"]
        self.assertEqual(fixture["top_level_types"], ["item", "list", "dictionary"])
        self.assertTrue(fixture["keys_unique"])
        self.assertTrue(fixture["trailing_input_rejected"])
        self.assertEqual(fixture["network_requests"], 0)

    def test_breadcrumb_reserves_manual_evaluation(self) -> None:
        fixture = load("accessibility/breadcrumb-contract.json")["positive_fixture"]
        self.assertEqual(fixture["current_page_count"], 1)
        self.assertEqual(fixture["aria_current"], "page")
        self.assertTrue(fixture["manual_evaluation_reserved"])

    def test_nernst_category_barrier(self) -> None:
        fixture = load("thermo-psyche/nernst-third-law-contract.json")["positive_fixture"]
        self.assertTrue(fixture["residual_entropy_exception_preserved"])
        self.assertFalse(fixture["absolute_zero_attained_in_finite_steps"])
        self.assertFalse(fixture["psyche_conversion"])

    def test_prequential_nonpromotion(self) -> None:
        fixture = load("stage20/prequential-drift-contract.json")["positive_fixture"]
        self.assertTrue(fixture["forecast_before_outcome"])
        self.assertTrue(fixture["retraining_decision_logged"])
        self.assertFalse(fixture["stage20_ready"])

    def test_portfolio_floors_completed(self) -> None:
        safe = load("approval-packets/x2-portfolio-execution.json")
        candidate = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["completed"], candidate["completed"], cleanup["completed"]), (30, 20, 30))
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
        self.assertEqual(
            negatives["effective_total"],
            negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"],
        )
        self.assertEqual(negatives["effective_total"], 3417)
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (20, 21))

    def test_overview_and_report_boundaries(self) -> None:
        overview = (PHASE_DIR / "v647-v3-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE_DIR / "deliverables" / "v647-v3-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        for phrase in ("NOT_READY_FOR_STAGE_20", "same-owner", "independent-team", "Māori authority"):
            self.assertIn(phrase, overview)
        for token in ('lang="en"', 'href="#main"', 'aria-label="Report sections"', "<caption>", 'scope="col"'):
            self.assertIn(token, report)

    def test_method_flow_retains_fail_and_pass_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-state.json")
        results = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual(results, Counter({"fail": 17, "pass": 17}))
        self.assertEqual(ledger["counts"]["methods"], 16)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))


if __name__ == "__main__":
    unittest.main()
