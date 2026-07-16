from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ghc_family_v646_v6_definitions as d  # noqa: E402


PHASE = ROOT / "docs/sylven-arc/v646-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V6X1Tests(unittest.TestCase):
    def test_exact_ten_and_chain_count(self):
        data = load("x1-proposals.json")
        self.assertEqual(data["prior_frozen_proposal_count"], 440)
        self.assertEqual(data["new_frozen_proposal_count"], 10)
        self.assertEqual(data["frozen_chain_count_after_x1"], 450)
        self.assertEqual([row["proposal_id"] for row in data["proposals"]], [f"V6466-P{i:02d}" for i in range(1, 11)])
        self.assertFalse(data["x2_execution_present"])

    def test_required_proposal_fields(self):
        required = {
            "hypothesis",
            "null_or_failure",
            "approval_class",
            "execution_lane",
            "current_primary_or_official_source_needs",
            "concrete_artifacts",
            "test_falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
            "novelty_against_440_frozen_proposals",
        }
        for row in load("x1-proposals.json")["proposals"]:
            self.assertFalse([key for key in required if not row.get(key)], row["proposal_id"])

    def test_expected_distribution(self):
        rows = load("x1-proposals.json")["proposals"]
        counts = {name: sum(row["expected_disposition"] == name for row in rows) for name in d.OUTCOME_CLASSES}
        self.assertEqual(counts, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_portfolio_floors(self):
        approval = load("approval-packets/x1-approval-portfolio.json")
        plan = load("prototypes/x1-skill-runner-plan.json")
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((approval["safe_now_count"], approval["candidate_count"], plan["skill_count"], plan["runner_count"], cleanup["task_count"]), (30, 20, 20, 10, 30))
        self.assertEqual(approval["completion_credit_before_x2"], 0)
        self.assertEqual(plan["completion_credit_before_x2"], 0)
        self.assertEqual(cleanup["completion_credit_before_x2"], 0)

    def test_collision_audits(self):
        proposals = load("provenance/prior-proposal-collision-audit.json")
        portfolio = load("provenance/prior-portfolio-collision-audit.json")
        self.assertTrue(proposals["valid"])
        self.assertEqual(proposals["exact_collision_count"], 0)
        self.assertTrue(portfolio["valid"])
        self.assertEqual(portfolio["exact_collisions"], [])
        self.assertEqual(portfolio["within_current_duplicates"], [])

    def test_negative_and_method_flow_retention(self):
        negatives = load("validation/x1-operational-negatives.json")
        method = load("method-flow/method-flow-state.json")
        self.assertEqual(negatives["count"], 10)
        self.assertEqual(negatives["observed_effective_after_x1"], 2894)
        self.assertEqual(method["counts"]["methods"], 10)
        self.assertEqual(method["counts"]["witness_results"]["fail"], 10)
        self.assertEqual(method["counts"]["witness_results"]["pass"], 10)
        self.assertEqual(sum(row["result"] == "fail" for row in method["witnesses"]), 10)
        self.assertEqual(sum(row["result"] == "pass" for row in method["witnesses"]), 10)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in method["methods"]))

    def test_source_and_authority_boundaries(self):
        source = load("sources/source-ledger.json")
        self.assertEqual(source["real_rows"], 0)
        self.assertEqual(source["real_people_or_operations"], 0)
        self.assertEqual(source["real_keys_or_tokens"], 0)
        self.assertFalse(source["authority_delegated"])
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]))

    def test_route_prepared_not_sent(self):
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(route["current_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertEqual(route["target_title"], "Eiren Kestrel")

    def test_x2_absent(self):
        x1_commit = "147aab7fd2f2805f119968dd30ab9c7996306d3a"
        for relative in ("x2-proposal-ledger.json", "phase-truth.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
            repository_relative = f"docs/sylven-arc/v646-v6/{relative}"
            result = subprocess.run(["git", "cat-file", "-e", f"{x1_commit}:{repository_relative}"], cwd=ROOT, capture_output=True)
            self.assertNotEqual(result.returncode, 0, relative)


if __name__ == "__main__":
    unittest.main()
