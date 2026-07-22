from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v651-v8-special-cli-prep"


def load(rel: str):
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


class SpecialX1Tests(unittest.TestCase):
    def test_exact_core_proposals_and_distribution(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["count"], 30)
        self.assertEqual(
            Counter(p["expected_disposition"] for p in data["proposals"]),
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )

    def test_novelty_chain(self):
        audit = load("provenance/semantic-novelty-audit.json")
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertTrue(audit["all_novel"])
        self.assertEqual((chain["prior_count"], chain["new_count"], chain["count"]), (1150, 30, 1180))

    def test_expanded_portfolios(self):
        counts = load("portfolios/x1-portfolio-plan.json")["counts"]
        self.assertEqual(counts, {"candidate_tasks": 30, "clean_fix_refine_tasks": 40, "runner_ideas": 12, "safe_now_tasks": 40, "skill_ideas": 20})

    def test_future_seats_are_placeholders_only(self):
        data = load("cli/future-seat-placeholders.json")
        self.assertEqual(len(data["placeholders"]), 8)
        self.assertEqual((data["named_cli_siblings"], data["created_tasks"], data["launched_cli_siblings"]), (0, 0, 0))
        self.assertTrue(all(p["name"] is None and p["state"] == "planned_only" for p in data["placeholders"]))

    def test_sable_rollover_and_route_hold(self):
        route = load("route/candidate-immediate-route.json")
        self.assertEqual(route["immediate_successor"], {"phase": "v652-v1", "seat": "Sable Rook"})
        self.assertEqual(route["terminal_send_state"], "HELD_UNTIL_SPECIAL_FINAL_PROOF")

    def test_special_budget_and_no_replay(self):
        request = load("workflow/workflow-plan-request.json")
        self.assertEqual(request["requirements"]["commit_cap"], {"total": 12, "x1": 6, "x2": 6})
        self.assertEqual(request["requirements"]["validation"]["replay_policy"], "skip_when_first_passes")

    def test_x1_has_no_x2_outcome_files(self):
        names = {p.name for p in PHASE.rglob("*") if p.is_file()}
        self.assertTrue({"outcome-ledger.json", "execution-ledger.json", "final-record.json", "seal-receipt.json"}.isdisjoint(names))


if __name__ == "__main__":
    unittest.main()
