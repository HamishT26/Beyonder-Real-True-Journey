"""Strict x1-only tests for Tamar Vey v646-v5."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V5X1Tests(unittest.TestCase):
    def test_exactly_ten_proposals(self):
        self.assertEqual(len(load("x1-proposals.json")["proposals"]), 10)

    def test_430_to_440_chain(self):
        row = load("x1-proposals.json")
        self.assertEqual((row["prior_frozen_proposal_count"], row["frozen_chain_count_after_x1"]), (430, 440))

    def test_expected_distribution(self):
        rows = load("x1-proposals.json")["proposals"]
        self.assertEqual(Counter(row["expected_disposition"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_only_four_truth_labels(self):
        self.assertEqual(set(load("x1-proposals.json")["allowed_outcome_classes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_x2_absent(self):
        self.assertFalse(load("x1-proposals.json")["x2_execution_present"])

    def test_proposal_novelty(self):
        self.assertTrue(load("provenance/prior-proposal-collision-audit.json")["valid"])
        self.assertEqual(load("provenance/prior-proposal-collision-audit.json")["exact_collision_count"], 0)

    def test_portfolio_novelty(self):
        self.assertTrue(load("provenance/prior-portfolio-collision-audit.json")["valid"])

    def test_expanded_portfolio_floors(self):
        approvals = load("approval-packets/x1-approval-portfolio.json")
        plan = load("prototypes/x1-skill-runner-plan.json")
        clean = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((len(approvals["safe_now"]), len(approvals["candidates"]), len(plan["skills"]), len(plan["runners"]), len(clean["tasks"])), (30, 20, 20, 10, 30))

    def test_no_completion_credit(self):
        approvals = load("approval-packets/x1-approval-portfolio.json")
        self.assertEqual(approvals["completion_credit_before_x2"], 0)
        self.assertTrue(all(row["x1_state"] == "preregistered_no_completion_credit" for row in approvals["safe_now"] + approvals["candidates"]))

    def test_inherited_protected_packets_unexecuted(self):
        row = load("approval-packets/x1-approval-portfolio.json")
        self.assertEqual((row["inherited_exact_packets_preserved"], row["inherited_blocked_packets_preserved"], row["inherited_packets_executed"]), (10, 5, 0))

    def test_source_status_vocabulary(self):
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in load("sources/source-ledger.json")["sources"]))

    def test_negative_continuity(self):
        row = load("validation/x1-operational-negatives.json")
        self.assertEqual((row["inherited_baton_time"], row["inherited_post_baton"], row["inherited_effective"], row["count"]), (2799, 1, 2800, 4))
        self.assertEqual(row["failure_erasure_count"], 0)

    def test_method_flow_retains_failure_and_pass(self):
        row = load("method-flow/method-flow-state.json")
        self.assertEqual((row["counts"]["methods"], row["counts"]["witness_results"]["fail"], row["counts"]["witness_results"]["pass"], row["counts"]["states"]["preferred"]), (4, 4, 4, 4))

    def test_route_unsent(self):
        row = load("orchestration/terminal-route-plan.json")
        self.assertEqual((row["current_state"], row["send_count"]), ("PREPARED_NOT_SENT", 0))

    def test_no_host_change(self):
        version = load("environment/version-receipt.json")
        sandbox = load("environment/sandbox-readonly-audit.json")
        self.assertFalse(any(version["host_actions"].values()))
        self.assertFalse(sandbox["sandbox_launched"] or sandbox["elevation"] or sandbox["feature_changed"] or sandbox["rebooted"])

    def test_all_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
