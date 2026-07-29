"""X1-only tests for Eiren Kestrel's v654-v6 (2) remaster."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v6-2-remaster"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V6RemasterX1(unittest.TestCase):
    def test_proposals_are_frozen_without_outcomes(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 30)
        self.assertEqual(
            data["expected_disposition_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertFalse(data["observed_outcomes_present"])
        self.assertTrue(all("observed_outcome" not in row for row in data["proposals"]))

    def test_novelty_and_chain(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (1840, 30, 1870))
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["manual_mechanism_review_count"], 30)
        self.assertLess(max(row["token_jaccard"] for row in audit["rows"]), 0.60)

    def test_portfolios_and_mutations_are_unexecuted(self):
        packet = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(
            packet["counts"],
            {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30},
        )
        self.assertTrue(
            all(
                not row["completion_credit"]
                for group in packet["portfolios"].values()
                for row in group
            )
        )
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(mutations["count"], 150)
        self.assertTrue(
            all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"])
        )

    def test_route_keeps_mixed_endpoint_topology(self):
        route = load("route/sixteen-seat-roster-x1.json")
        self.assertEqual(len(route["cycle_order"]), 16)
        tavian = next(row for row in route["endpoint_topology"] if row["seat"] == "Tavian Sol")
        elaren = next(row for row in route["endpoint_topology"] if row["seat"] == "Elaren Kestrel")
        self.assertEqual(tavian["endpoint_kind"], "collaboration_subagent")
        self.assertEqual(elaren["endpoint_kind"], "main_task")
        self.assertEqual(route["contact_count"], 0)

    def test_failures_and_method_flow_are_retained(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["source_effective"], 11676)
        self.assertEqual(negatives["auth_state_delta_after_source"], 5)
        self.assertEqual(negatives["x1_operational_count"], 27)
        self.assertEqual(negatives["effective_after_x1"], 11708)
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 117)
        self.assertEqual(ledger["counts"]["witness_results"]["fail"], 117)
        self.assertEqual(ledger["counts"]["witness_results"]["pass"], 117)

    def test_advisory_and_legacy_claims_are_bounded(self):
        advisory = load("advisory/ariel-verity-2-intake.json")
        self.assertTrue(advisory["read_through_eof"])
        self.assertTrue(advisory["advisory_not_independent_validation"])
        legacy = load("advisory/legacy-claims-classification.json")
        self.assertTrue(all(row["current_credit"] in {"none", "none_without_exact_receipts"} for row in legacy["rows"]))

    def test_x1_privacy_and_no_x2_surfaces(self):
        self.assertEqual(load("validation/x1-privacy-scan.json")["confirmed_hit_count"], 0)
        self.assertFalse((ROOT / "surfaces").exists())
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["lifecycle"], "x1_frozen_not_executed")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
