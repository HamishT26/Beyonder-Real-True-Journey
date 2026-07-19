from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_v649_v4_runtime import CONTRACTS  # noqa: E402

PHASE = ROOT / "docs" / "orin-thale" / "v649-v4"
SOURCE = "e7998c7ee6fb4a5dccc9e3a09a50aecc8a10b956"
X1 = "9882fb936e404796cd4aeb847ff41bd3ec28b5d6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def evidence_commit() -> str:
    commits = git("rev-list", "--reverse", f"{SOURCE}..HEAD").splitlines()
    if len(commits) < 2:
        raise RuntimeError("evidence commit is not present")
    return commits[1]


class TestGhcFamilyV649V4Evidence(unittest.TestCase):
    def test_core_distribution_and_vocabulary(self) -> None:
        ledger = load("x2/core-outcome-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["outcome_classes"], ["completed", "represented", "open_gap", "exact_gate"])
        self.assertEqual(ledger["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_every_proposal_has_two_bounded_artifacts(self) -> None:
        for proposal_id, spec in CONTRACTS.items():
            contract = load(spec["paths"][0])
            evidence = load(spec["paths"][1])
            self.assertEqual(contract["proposal_id"], proposal_id)
            self.assertEqual(evidence["proposal_id"], proposal_id)
            self.assertTrue(contract["acceptance_gate_passed"])
            self.assertEqual((evidence["mutation_count"], evidence["executed_count"], evidence["rejected_count"]), (7, 7, 7))

    def test_all_seventy_synthetic_mutations_execute_and_reject(self) -> None:
        results = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual((results["count"], results["executed_count"], results["rejected_count"]), (70, 70, 70))
        self.assertEqual(len({row["mutation_id"] for row in results["mutations"]}), 70)
        self.assertTrue(all(row["retained_negative"] for row in results["mutations"]))
        self.assertFalse(results["production_security_credit"])
        self.assertFalse(results["scientific_truth_credit"])

    def test_future_completion_tribunal_is_bounded(self) -> None:
        row = load("method-flow/future-completion-contract.json")
        names = {item["check"] for item in row["checks"]}
        self.assertTrue({"single_assignment", "cancellation_race", "exception_propagation", "callback_order", "waiter_notification", "executor_shutdown", "duplicate_credit"}.issubset(names))
        self.assertIn("production_executor", row["absent_or_reserved"])

    def test_ope_board_is_symbolic_not_empirical(self) -> None:
        row = load("gmut/operator-product-expansion-obligations.json")
        names = {item["check"] for item in row["checks"]}
        self.assertTrue({"short_distance_domain", "coefficient_distribution", "scaling_degree", "associativity", "microlocal_spectrum", "observation_firewall"}.issubset(names))
        self.assertTrue({"real_data", "likelihood", "force", "quantum_completion", "theory_of_everything"}.issubset(row["absent_or_reserved"]))

    def test_einstein_toolkit_protocol_is_zero_solver_run_open_gap(self) -> None:
        evidence = load("empirical/einstein-toolkit-zero-solver-run-receipt.json")
        contract = load("empirical/einstein-toolkit-study-contract.json")
        self.assertEqual(evidence["outcome"], "open_gap")
        self.assertEqual((evidence["real_rows"], evidence["likelihood_evaluations"]), (0, 0))
        self.assertTrue({"toolkit_checkout", "gmut_thorn", "solver_runs", "constraint_traces", "refinement_triplets", "measured_convergence", "independent_review"}.issubset(contract["absent_or_reserved"]))

    def test_seed_germination_protocol_remains_proxy(self) -> None:
        row = load("thos/seed-germination-assay-contract.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertTrue({"real_people", "real_seed_lots", "real_germination_assays", "real_biological_results", "effectiveness"}.issubset(row["absent_or_reserved"]))

    def test_registration_management_remains_nonproduction(self) -> None:
        row = load("freed-id/registration-management-profile.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertTrue({"real_keys", "accounts", "tokens", "interoperability", "trust_governance"}.issubset(row["absent_or_reserved"]))

    def test_seed_passport_dsi_gate_stays_exact(self) -> None:
        row = load("cbr/seed-passport-dsi-risk-gate.json")
        self.assertEqual(row["outcome"], "exact_gate")
        self.assertTrue({"affected_party_acceptance", "legal_authority", "cultural_ratification", "maori_authority", "dsi_governance_authority", "benefit_sharing_authority"}.issubset(row["absent_or_reserved"]))

    def test_netcdf_tribunal_is_not_exhaustive_security(self) -> None:
        row = load("formats/netcdf-classic-contract.json")
        self.assertIn("resource_budget", {item["check"] for item in row["checks"]})
        self.assertTrue({"user_files", "production_decoder", "external_retrieval", "exhaustive_security"}.issubset(row["absent_or_reserved"]))

    def test_error_summary_reserves_manual_evaluation(self) -> None:
        row = load("accessibility/error-summary-contract.json")
        self.assertTrue({"heading", "focus_target", "error_links", "field_association", "linear_fallback"}.issubset({item["check"] for item in row["checks"]}))
        self.assertTrue({"assistive_technology_review", "maori_language_review", "affected_user_evaluation", "complete_accessibility"}.issubset(row["absent_or_reserved"]))

    def test_lippmann_classifier_rejects_psyche_conversion(self) -> None:
        row = load("thermo-psyche/lippmann-electrocapillary-contract.json")
        self.assertIn("agency_nonconversion", {item["check"] for item in row["checks"]})
        self.assertTrue({"psyche_measure", "agency_measure", "moral_value", "consciousness", "personhood"}.issubset(row["absent_or_reserved"]))

    def test_pattern_mixture_board_does_not_promote_stage20(self) -> None:
        row = load("stage20/pattern-mixture-contract.json")
        self.assertEqual(row["outcome"], "completed")
        self.assertTrue({"real_participants", "causal_effect", "independent_review", "stage20_authority"}.issubset(row["absent_or_reserved"]))

    def test_expanded_portfolios_reach_declared_bounded_floors(self) -> None:
        safe = load("approval-packets/x2-safe-now-results.json")
        candidates = load("prototypes/x2-candidate-results.json")
        cleanup = load("maintenance/x2-clean-refine-results.json")
        held = load("approval-packets/inherited-held-packets.json")
        self.assertEqual((safe["count"], safe["completed_count"]), (30, 30))
        self.assertEqual((candidates["count"], candidates["completed_count"]), (20, 20))
        self.assertEqual((cleanup["count"], cleanup["completed_count"], cleanup["destructive_actions"]), (30, 30, 0))
        self.assertEqual((held["exact_approval_count"], held["blocked_count"], held["executed_count"]), (10, 5, 0))

    def test_skill_packages_validate_and_stay_phase_local(self) -> None:
        ledger = load("x2/skill-validation-ledger.json")
        self.assertEqual((ledger["skill_count"], ledger["quick_validate_passed"], ledger["smoke_used"], ledger["pending_closeout_use"]), (20, 20, 19, 1))
        self.assertFalse(ledger["global_installation"])
        self.assertFalse(ledger["subagent_forward_test"])

    def test_runners_are_built_and_evidence_used(self) -> None:
        ledger = load("x2/runner-use-ledger.json")
        self.assertEqual((ledger["runner_count"], ledger["completed_count"], ledger["pending_closeout_count"]), (10, 9, 1))
        self.assertTrue(all(row["built"] and row["caller_compatible"] for row in ledger["items"]))

    def test_negatives_and_gates_are_preserved(self) -> None:
        negatives = load("x2/retained-negative-register.json")
        operational = load("validation/x2-operational-negatives.json")
        gates = load("x2/gate-register.json")
        expected = 4929 + 17 + 70 + operational["count"]
        self.assertEqual(negatives["effective_at_evidence"], expected)
        self.assertEqual(negatives["x2_operational"], operational["count"])
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (38, 39))
        self.assertEqual(gates["silently_closed"], 0)

    def test_x1_tree_is_immutable_and_evidence_manifest_matches(self) -> None:
        evidence = load("x2/evidence-ledger.json")
        self.assertEqual(evidence["x1_commit"], X1)
        self.assertEqual(evidence["x1_frozen_drift_count"], 0)
        self.assertFalse(evidence["full_repository_suite_run"])
        self.assertFalse(evidence["canonical_successful_pass_used"])
        commit = evidence_commit()
        manifest = load("validation/evidence-staged-manifest.json")
        for entry in manifest["entries"]:
            self.assertEqual(git("rev-parse", f"{commit}:{entry['path']}"), entry["git_blob"])


if __name__ == "__main__":
    unittest.main()
