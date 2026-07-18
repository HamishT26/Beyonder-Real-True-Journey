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

from ghc_family_v648_v6_runtime import CONTRACTS  # noqa: E402

PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"
X1 = "3f6a64d239bdde1c38fea166db5eff0f2f3e1d89"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class TestGhcFamilyV648V6Evidence(unittest.TestCase):
    def test_core_distribution_and_vocabulary(self) -> None:
        ledger = load("x2/core-outcome-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["outcome_classes"], ["completed", "represented", "open_gap", "exact_gate"])
        self.assertEqual(ledger["distribution"], {"completed":6,"represented":2,"open_gap":1,"exact_gate":1})
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_every_proposal_has_two_bounded_artifacts(self) -> None:
        for proposal_id, spec in CONTRACTS.items():
            first = load(spec["paths"][0])
            second = load(spec["paths"][1])
            self.assertEqual(first["proposal_id"], proposal_id)
            self.assertEqual(second["proposal_id"], proposal_id)
            self.assertTrue(first["acceptance_gate_passed"])
            self.assertEqual(second["mutation_count"], 7)
            self.assertEqual(second["executed_count"], 7)
            self.assertEqual(second["rejected_count"], 7)

    def test_all_seventy_synthetic_mutations_execute_and_reject(self) -> None:
        results = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual(results["count"], 70)
        self.assertEqual(results["executed_count"], 70)
        self.assertEqual(results["rejected_count"], 70)
        self.assertEqual(len({row["mutation_id"] for row in results["mutations"]}), 70)
        self.assertTrue(all(row["retained_negative"] for row in results["mutations"]))
        self.assertFalse(results["production_security_credit"])
        self.assertFalse(results["scientific_truth_credit"])

    def test_json_sequence_tribunal_is_bounded(self) -> None:
        row = load("formats/json-text-sequence-contract.json")
        names = {item["check"] for item in row["checks"]}
        self.assertTrue({"record_separator","utf8","truncated_scalar","resynchronization","record_budget"}.issubset(names))
        self.assertIn("exhaustive_security", row["absent_or_reserved"])

    def test_jld_board_is_symbolic_not_empirical(self) -> None:
        row = load("gmut/jost-lehmann-dyson-obligations.json")
        names = {item["check"] for item in row["checks"]}
        self.assertTrue({"commutator_support","spectral_support","causal_cone","analyticity_domain","observation_firewall"}.issubset(names))
        self.assertTrue({"real_data","likelihood","force","theory_of_everything"}.issubset(row["absent_or_reserved"]))

    def test_xrism_is_zero_row_open_gap(self) -> None:
        row = load("empirical/xrism-zero-row-receipt.json")
        self.assertEqual(row["outcome"], "open_gap")
        self.assertEqual(row["real_rows"], 0)
        self.assertEqual(row["likelihood_evaluations"], 0)
        self.assertIn("constraints", load("empirical/xrism-study-contract.json")["absent_or_reserved"])

    def test_theatre_protocol_remains_proxy(self) -> None:
        row = load("thos/theatre-handover-contract.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertTrue({"real_workers","real_audiences","real_productions","effectiveness"}.issubset(row["absent_or_reserved"]))

    def test_rich_authorization_remains_nonproduction(self) -> None:
        row = load("freed-id/rich-authorization-profile.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertTrue({"real_keys","accounts","tokens","interoperability","trust_governance"}.issubset(row["absent_or_reserved"]))

    def test_cbr_authority_matrix_stays_exact_gate(self) -> None:
        row = load("cbr/live-performance-remedy-matrix.json")
        self.assertEqual(row["outcome"], "exact_gate")
        self.assertTrue({"affected_party_acceptance","legal_authority","cultural_ratification","maori_authority"}.issubset(row["absent_or_reserved"]))

    def test_tiff_tribunal_is_not_exhaustive_security(self) -> None:
        row = load("formats/tiff-contract.json")
        self.assertIn("resource_budget", {item["check"] for item in row["checks"]})
        self.assertTrue({"user_files","production_decoder","exhaustive_security"}.issubset(row["absent_or_reserved"]))

    def test_complex_table_reserves_manual_evaluation(self) -> None:
        row = load("accessibility/complex-table-contract.json")
        self.assertTrue({"multilevel_header","scope_id_headers","sort_announcement","linear_fallback"}.issubset({item["check"] for item in row["checks"]}))
        self.assertTrue({"assistive_technology_review","maori_language_review","affected_user_evaluation","complete_accessibility"}.issubset(row["absent_or_reserved"]))

    def test_planck_classifier_rejects_psyche_conversion(self) -> None:
        row = load("thermo-psyche/planck-spectral-contract.json")
        self.assertIn("psyche_value_nonconversion", {item["check"] for item in row["checks"]})
        self.assertTrue({"psyche_measure","agency_measure","moral_value","consciousness","personhood"}.issubset(row["absent_or_reserved"]))

    def test_principal_stratification_does_not_promote_stage20(self) -> None:
        row = load("stage20/principal-stratification-contract.json")
        self.assertEqual(row["outcome"], "completed")
        self.assertTrue({"real_participants","causal_effect","independent_review","stage20_authority"}.issubset(row["absent_or_reserved"]))

    def test_expanded_portfolios_reach_declared_bounded_floors(self) -> None:
        safe = load("approval-packets/x2-safe-now-results.json")
        candidates = load("prototypes/x2-candidate-results.json")
        cleanup = load("maintenance/x2-clean-refine-results.json")
        held = load("approval-packets/inherited-held-packets.json")
        self.assertEqual((safe["count"], safe["completed_count"]), (30,30))
        self.assertEqual((candidates["count"], candidates["completed_count"]), (20,20))
        self.assertEqual((cleanup["count"], cleanup["completed_count"]), (30,30))
        self.assertEqual(cleanup["destructive_actions"], 0)
        self.assertEqual((held["exact_approval_count"], held["blocked_count"], held["executed_count"]), (10,5,0))

    def test_skill_packages_validate_and_stay_phase_local(self) -> None:
        ledger = load("x2/skill-validation-ledger.json")
        self.assertEqual(ledger["skill_count"], 20)
        self.assertEqual(ledger["quick_validate_passed"], 20)
        self.assertEqual(ledger["smoke_used"], 19)
        self.assertEqual(ledger["pending_closeout_use"], 1)
        self.assertFalse(ledger["global_installation"])
        self.assertFalse(ledger["subagent_forward_test"])

    def test_runners_are_built_and_nine_are_evidence_used(self) -> None:
        ledger = load("x2/runner-use-ledger.json")
        self.assertEqual(ledger["runner_count"], 10)
        self.assertEqual(ledger["completed_count"], 9)
        self.assertEqual(ledger["pending_closeout_count"], 1)
        self.assertTrue(all(row["built"] for row in ledger["items"]))
        self.assertTrue(all(row["caller_compatible"] for row in ledger["items"]))

    def test_negatives_and_gates_are_preserved(self) -> None:
        negatives = load("x2/retained-negative-register.json")
        gates = load("x2/gate-register.json")
        self.assertEqual(negatives["effective_at_evidence"], 4471)
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (32,33))
        self.assertEqual(gates["silently_closed"], 0)

    def test_x1_tree_is_immutable_and_evidence_manifest_matches(self) -> None:
        evidence = load("x2/evidence-ledger.json")
        self.assertEqual(evidence["x1_commit"], X1)
        self.assertEqual(evidence["x1_frozen_drift_count"], 0)
        self.assertFalse(evidence["full_repository_suite_run"])
        self.assertFalse(evidence["canonical_successful_pass_used"])
        manifest = load("validation/evidence-staged-manifest.json")
        for entry in manifest["entries"]:
            self.assertEqual(git("hash-object", f"--path={entry['path']}", entry["path"]), entry["git_blob"])


if __name__ == "__main__":
    unittest.main()
