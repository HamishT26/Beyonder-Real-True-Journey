from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v647-v4"
X1_FINAL = "5e5bc09f5173c00c7674b7868e3c7e5e8af80053"
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v647_v4_definitions as d  # noqa: E402


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def load_x1(relative: str):
    payload = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{X1_FINAL}:docs/sylven-arc/v647-v4/{relative}"],
        text=True,
        encoding="utf-8",
    )
    return json.loads(payload)


class V647V4X1Tests(unittest.TestCase):
    def test_exact_ten_complete_preregistrations(self):
        data = load("x1-proposals.json")
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure", "approval_class", "execution_lane",
            "current_primary_or_official_source_needs", "concrete_artifacts", "test_falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition", "novelty_against_prior_frozen_proposals",
        }
        self.assertEqual(len(data["proposals"]), 10)
        self.assertTrue(all(required <= set(row) for row in data["proposals"]))
        self.assertEqual(data["frozen_chain_count_after_x1"], 510)
        self.assertFalse(data["x2_execution_present"])

    def test_expected_distribution_is_not_result(self):
        data = load("x1-proposals.json")
        self.assertEqual(data["expected_distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertFalse(data["expected_counts_are_results"])
        self.assertTrue(all(row["expected_disposition"] in d.OUTCOME_CLASSES for row in data["proposals"]))

    def test_500_proposal_novelty_audit(self):
        frozen = load("provenance/frozen-chain-proposal-index.json")
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(frozen["count"], 500)
        self.assertEqual((audit["prior_count"], audit["candidate_count"], audit["passed"]), (500, 10, 10))
        self.assertTrue(audit["valid"])
        self.assertTrue(all(not row["exact_title_collision"] and row["maximum_jaccard"] < 0.5 for row in audit["audits"]))

    def test_portfolio_floors_are_new_plans(self):
        portfolio = load("approval-packets/x1-approval-portfolio.json")
        self.assertEqual((portfolio["safe_now_count"], portfolio["candidate_count"], portfolio["exact_count"], portfolio["blocked_count"]), (30, 20, 10, 5))
        self.assertTrue(all(not row["completion_credit"] for key in ("safe_now", "candidates", "exact", "blocked") for row in portfolio[key]))
        self.assertFalse(portfolio["x2_execution_present"])

    def test_skill_runner_and_cleanup_floors(self):
        plan = load("prototypes/x1-skill-runner-plan.json")
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((plan["skill_count"], plan["runner_count"], cleanup["count"]), (20, 10, 30))
        self.assertTrue(all(row["build_state"] == "planned_for_x2" for row in plan["skills"] + plan["runners"]))
        self.assertTrue(all(row["execution_state"] == "planned_for_x2" for row in cleanup["tasks"]))

    def test_seventy_mutations_are_only_preregistered(self):
        data = load("validation/x1-synthetic-mutation-plan.json")
        self.assertEqual((data["count"], data["executed"], data["rejected"]), (70, 0, 0))
        self.assertTrue(all(row["execution_state"] == "preregistered_not_executed" and row["accepted"] is None for row in data["mutations"]))

    def test_negative_and_gate_inheritance(self):
        negatives = load_x1("retained-negative-register.json")
        gates = load_x1("exact-open-gate-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational"], negatives["effective_total"]), (3417, 1, 3418))
        self.assertTrue(negatives["no_negative_erased"])
        self.assertEqual((gates["current_effective_open_gaps"], gates["current_effective_exact_gates"]), (20, 21))
        self.assertEqual((gates["expected_after_x2_open_gaps"], gates["expected_after_x2_exact_gates"]), (21, 22))
        self.assertEqual(gates["silently_closed"], 0)

    def test_method_flow_retains_failure_and_pass(self):
        ledger = load_x1("method-flow/method-flow-state.json")
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 1, "pass": 1})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 1)
        self.assertEqual(len(ledger["methods"]), 1)

    def test_source_status_and_nonconversion(self):
        data = load("sources/source-ledger.json")
        self.assertEqual(data["source_count"], 14)
        self.assertTrue(all(row["status"] in data["allowed_statuses"] for row in data["sources"]))
        self.assertTrue(all(row["url"].startswith("https://") and not row["observation_credit"] and not row["authority_delegated"] for row in data["sources"]))

    def test_identity_focus_and_environment_boundaries(self):
        identity = load("identity-receipt.json")
        truth = load_x1("phase-truth.json")
        versions = load("environment/version-receipt.json")
        self.assertEqual(identity["owner"], "Sylven Arc")
        self.assertTrue(identity["corrigible_by_hamish"])
        self.assertEqual(truth["primary_focus"] if "primary_focus" in truth else d.PRIMARY_FOCUS, "THOS Body")
        self.assertEqual(truth["lifecycle"], "x1_frozen_uncommitted")
        self.assertFalse(truth["x2_execution_present"])
        self.assertTrue(versions["verified_only"])
        self.assertEqual((versions["updates_or_installs"], versions["security_or_feature_changes"]), (0, 0))

    def test_preregistration_word_limit(self):
        words = (PHASE / "x1-preregistration.md").read_text(encoding="utf-8").split()
        self.assertLessEqual(len(words), 6000)
        self.assertGreaterEqual(len(words), 1000)


if __name__ == "__main__":
    unittest.main()
