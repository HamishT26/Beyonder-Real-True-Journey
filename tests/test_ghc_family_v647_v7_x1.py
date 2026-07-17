from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v647-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V7X1Tests(unittest.TestCase):
    def test_exactly_ten_distinct_proposals(self):
        data = load("x1-proposals.json")
        self.assertEqual(10, len(data["proposals"]))
        self.assertEqual(10, len({row["title"].casefold() for row in data["proposals"]}))
        self.assertEqual(530, data["prior_frozen_proposal_count"])
        self.assertEqual(540, data["frozen_chain_count_after_x1"])

    def test_expected_distribution_only(self):
        data = load("x1-proposals.json")
        self.assertFalse(data["x2_execution_present"])
        self.assertEqual(Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), Counter(row["expected_disposition"] for row in data["proposals"]))

    def test_novelty_audits_pass(self):
        self.assertTrue(load("provenance/prior-proposal-collision-audit.json")["valid"])
        self.assertTrue(load("provenance/prior-portfolio-collision-audit.json")["valid"])

    def test_portfolio_floors_and_gates(self):
        approval = load("approval-packets/x1-approval-portfolio.json")
        plan = load("prototypes/x1-skill-runner-plan.json")
        clean = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((30, 20, 20, 10, 30), (approval["safe_now_count"], approval["candidate_count"], plan["skill_count"], plan["runner_count"], clean["task_count"]))
        self.assertEqual((10, 5), (approval["exact_approval_count"], approval["blocked_count"]))
        self.assertFalse(approval["inherited_exact_and_blocked_receive_new_completion_credit"])

    def test_negatives_and_method_flow_are_retained(self):
        negatives = load("retained-negative-register.json")
        methods = load("method-flow/method-flow-state.json")
        self.assertEqual(3669, negatives["inherited_effective_negatives"])
        self.assertEqual(3, negatives["x1_operational_negative_count"])
        self.assertEqual({"fail": 3, "pass": 3}, methods["counts"]["witness_results"])

    def test_route_and_authority_are_held(self):
        route = load("orchestration/terminal-route-plan.json")
        sources = load("sources/source-ledger.json")
        self.assertEqual("PREPARED_NOT_SENT", route["state"])
        self.assertFalse(route["task_creation_authorized"])
        self.assertEqual(0, sources["real_rows"])
        self.assertEqual(0, sources["real_people_or_operations"])
        self.assertEqual(0, sources["real_keys_or_tokens"])
        self.assertFalse(sources["authority_delegated"])


if __name__ == "__main__":
    unittest.main()
