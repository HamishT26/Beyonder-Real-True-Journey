"""Bounded x2 evidence tests for Sylven Arc v650-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v650_v6_phase_data as d  # noqa: E402
import ghc_family_v650_v6_runtime as runtime  # noqa: E402
import ghc_family_v650_v6_x2_data as x2d  # noqa: E402


ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestSylvenV650V6X2(unittest.TestCase):
    def test_all_twenty_receipts_use_frozen_outcomes(self):
        ledger = load("evidence/x2-evidence-ledger.json")
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(
            ledger["distribution"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(
            Counter(row["outcome"] for row in ledger["proposals"]),
            Counter(ledger["distribution"]),
        )
        self.assertTrue(all(row["passed"] for row in ledger["proposals"]))

    def test_one_hundred_mutations_executed_and_rejected(self):
        results = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual(results["planned_count"], 100)
        self.assertEqual(results["executed_count"], 100)
        self.assertEqual(results["rejected_or_quarantined_count"], 100)
        self.assertEqual(results["completion_credit"], 0)
        self.assertEqual({row["result"] for row in results["mutations"]}, {"rejected"})

    def test_runtime_fails_closed_for_each_mutation_class(self):
        for proposal in d.PROPOSALS:
            proposal_id = proposal["proposal_id"]
            self.assertTrue(runtime.evaluate_fixture(proposal_id, runtime.canonical_fixture(proposal_id))["accepted"])
            for kind in runtime.MUTATION_KINDS:
                result = runtime.evaluate_fixture(proposal_id, runtime.mutated_fixture(proposal_id, kind))
                self.assertFalse(result["accepted"], (proposal_id, kind))

    def test_gmut_surfaces_do_not_promote_physics(self):
        for slug in ("modular-relative-entropy", "covariant-hamilton-jacobi"):
            witness = load(f"surfaces/{slug}/bounded-receipt.json")["witness"]
            self.assertFalse(witness["physical_state_claim"])
            self.assertFalse(witness["theory_of_everything"])
            self.assertEqual(witness["observation_rows"], 0)

    def test_swift_adapter_remains_zero_row_open_gap(self):
        receipt = load("surfaces/swift-bat-zero-row/bounded-receipt.json")
        self.assertEqual(receipt["outcome"], "open_gap")
        witness = receipt["witness"]
        self.assertEqual(witness["downloaded_rows"], 0)
        self.assertEqual(witness["likelihood_evaluations"], 0)
        self.assertEqual(witness["posterior_samples"], 0)
        self.assertEqual(witness["empirical_constraints"], 0)

    def test_thos_and_identity_proxies_have_zero_real_events(self):
        for slug in ("seed-bank-accession", "seed-bank-environment", "oidc-userinfo", "oidc-pairwise-subject"):
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["outcome"], "represented")
            witness = receipt["witness"]
            self.assertEqual(witness["real_entities"], 0)
            self.assertEqual(witness["real_events"], 0)
            self.assertEqual(witness["blind_matched_budget_arms"], 0)

    def test_seed_authority_surface_remains_exact_gate(self):
        receipt = load("surfaces/seed-sovereignty-authority/bounded-receipt.json")
        self.assertEqual(receipt["outcome"], "exact_gate")
        self.assertEqual(receipt["witness"]["software_decisions"], 0)
        self.assertEqual(receipt["witness"]["authority_state"], "reserved")

    def test_accessibility_surfaces_reserve_manual_evaluation(self):
        for slug in ("aria-error-details", "accessible-range"):
            witness = load(f"surfaces/{slug}/bounded-receipt.json")["witness"]
            self.assertTrue(witness["manual_evaluation_reserved"])
            self.assertTrue(witness["affected_user_evaluation_reserved"])
            self.assertFalse(witness["complete_accessibility_claim"])

    def test_nonconversion_and_stage20_stay_closed(self):
        thermo = load("surfaces/massieu-planck-nonconversion/bounded-receipt.json")["witness"]
        self.assertFalse(thermo["psyche_conversion"])
        self.assertFalse(thermo["agency_conversion"])
        self.assertFalse(thermo["consciousness_claim"])
        stage = load("surfaces/front-door-nonpromotion/bounded-receipt.json")["witness"]
        self.assertEqual(stage["participant_effect_estimates"], 0)
        self.assertFalse(stage["causal_effect_claim"])
        self.assertFalse(stage["stage20_promoted"])

    def test_portfolio_floors_are_new_and_completed_bounded(self):
        expected = {
            "safe-now-execution.json": 40,
            "candidate-execution.json": 30,
            "skill-execution.json": 20,
            "runner-execution.json": 10,
            "clean-fix-refine-execution.json": 40,
        }
        for name, count in expected.items():
            receipt = load(f"portfolios/{name}")
            self.assertEqual(receipt["count"], count)
            self.assertEqual(receipt["completed"], count)

    def test_candidates_are_built_tested_and_invoked(self):
        execution = load("portfolios/candidate-execution.json")
        self.assertFalse(execution["inherited_completion_credit"])
        for row in execution["items"]:
            prototype = load(row["prototype"])
            self.assertTrue(prototype["built"])
            self.assertTrue(prototype["tested"])
            self.assertTrue(prototype["invoked"])
            self.assertTrue(prototype["passed"])

    def test_phase_local_skills_use_official_workflow(self):
        execution = load("portfolios/skill-execution.json")
        self.assertFalse(execution["global_install"])
        self.assertEqual(len(execution["skills"]), 20)
        for row in execution["skills"]:
            package = ROOT / row["package"]
            self.assertTrue((package / "SKILL.md").is_file())
            self.assertTrue((package / "agents/openai.yaml").is_file())
            self.assertTrue((package / "references/contract.md").is_file())
            witness = load(row["witness"])
            self.assertTrue(witness["initialized_with_official_workflow"])
            self.assertTrue(witness["metadata_generated_with_official_workflow"])
            self.assertTrue(witness["smoke_passed"])
            self.assertFalse(witness["global_install"])

    def test_ten_family_current_runners_built_and_invoked(self):
        execution = load("portfolios/runner-execution.json")
        self.assertTrue(execution["caller_compatibility_preserved"])
        self.assertEqual(len(execution["runners"]), 10)
        for row in execution["runners"]:
            self.assertTrue(row["name"].startswith("ghc_family_"))
            self.assertTrue((REPO / "scripts" / row["name"]).is_file())
            self.assertTrue(row["built"] and row["invoked"] and row["passed"])

    def test_x1_paths_remain_blob_exact(self):
        source = d.SOURCE_HEAD
        paths = subprocess.check_output(
            ["git", "diff", "--name-only", "-z", source, X1_COMMIT], cwd=REPO
        ).decode("utf-8").split("\0")
        for path in (p for p in paths if p):
            frozen_oid = subprocess.check_output(
                ["git", "rev-parse", f"{X1_COMMIT}:{path}"], cwd=REPO, text=True
            ).strip()
            current_oid = subprocess.check_output(
                ["git", "hash-object", f"--path={path}", path], cwd=REPO, text=True
            ).strip()
            self.assertEqual(current_oid, frozen_oid, path)

    def test_evidence_manifest_matches_working_blobs(self):
        manifest = load("validation/evidence-staged-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for row in manifest["entries"]:
            blob = subprocess.check_output(["git", "cat-file", "blob", row["git_blob"]], cwd=REPO)
            self.assertEqual(len(blob), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])

    def test_method_flow_retains_x2_failure(self):
        ledger = load("method-flow/x2-method-flow-state.json")
        self.assertEqual(len(ledger["methods"]), len(x2d.X2_OPERATIONAL_NEGATIVES))
        self.assertEqual(
            Counter(row["result"] for row in ledger["witnesses"]),
            Counter({"fail": 3, "pass": 3}),
        )
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))

    def test_negative_and_gate_counts_are_additive(self):
        negatives = load("evidence/retained-negative-register.json")
        self.assertEqual(negatives["activation_baseline"], 6056)
        self.assertEqual(negatives["x1_operational"], 19)
        self.assertEqual(negatives["synthetic_executed_and_rejected"], 100)
        self.assertEqual(negatives["x2_operational"], 3)
        self.assertEqual(negatives["effective_at_evidence"], 6178)
        self.assertFalse(negatives["negative_erased"])
        gates = load("evidence/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 48)
        self.assertEqual(gates["effective_exact_gates"], 49)

    def test_evidence_is_not_sealed_and_route_is_not_sent(self):
        truth = load("evidence/phase-truth.json")
        self.assertEqual(truth["state"], "X2_EVIDENCE_COMPLETE_NOT_SEALED")
        self.assertIsNone(truth["evidence_commit"])
        self.assertEqual(truth["successful_exact_final_aggregates_used"], 0)
        self.assertFalse(truth["post_success_replay"])
        self.assertFalse(truth["full_repository_suite"])
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
