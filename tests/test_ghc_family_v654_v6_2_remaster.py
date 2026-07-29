"""Bounded x2 tests for Eiren Kestrel's v654-v6 (2) remaster."""

from __future__ import annotations

import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v6-2-remaster"
sys.path.insert(0, str(REPO / "scripts"))

import ghc_family_v654_v6_2_remaster_core as core  # noqa: E402


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V6RemasterEvidence(unittest.TestCase):
    def test_outcome_distribution(self):
        ledger = load("evidence/outcome-ledger.json")
        self.assertEqual(
            ledger["counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(ledger["proposal_count"], 30)

    def test_all_surfaces_and_mutations(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(len(rows), 30)
        self.assertEqual(sum(row["mutation_rejected_count"] for row in rows), 150)
        self.assertTrue(all(row["acceptance_gate_passed"] for row in rows))
        self.assertEqual(len(list((ROOT / "surfaces").rglob("contract.json"))), 30)

    def test_zero_real_world_counters(self):
        for path in (ROOT / "surfaces").rglob("bounded-receipt.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(
                all(value == 0 for value in receipt["real_world_counters"].values()),
                path,
            )

    def test_action_first_omega_passport(self):
        passport = load("surfaces/omega-evidence-passport/contract.json")
        fields = set(passport["mechanism_payload"]["passport_fields"])
        self.assertEqual(
            fields,
            {
                "source_action",
                "domain",
                "units",
                "degrees_of_freedom",
                "conservation",
                "stability",
                "causality",
                "observables",
                "bounds",
                "falsifier",
                "recovery",
            },
        )
        action = load("surfaces/omega-action-derivation/contract.json")
        self.assertIn("delta(Delta_S_Omega)", action["mechanism_payload"]["metric_variation"])
        self.assertEqual(
            action["mechanism_payload"]["tensor_promotion"],
            "held_for_model_specific_derivation",
        )

    def test_correlated_witnesses_are_discounted(self):
        receipt = load("surfaces/correlated-witness-discount/contract.json")
        payload = receipt["mechanism_payload"]
        self.assertEqual(payload["witness_count"], 16)
        self.assertLess(payload["effective_n_upper_bound"], 2)
        self.assertEqual(payload["independent_replication_count"], 0)
        self.assertAlmostEqual(core.effective_n(16, 0.75), 16 / 12.25)

    def test_erdos_straus_is_finite_and_exact(self):
        contract = load("surfaces/erdos-straus-bounded-checker/contract.json")
        bounded = contract["mechanism_payload"]
        self.assertEqual(bounded["domain"], {"start": 2, "end": 500, "integer_count": 499})
        self.assertEqual(bounded["counterexample_count"], 0)
        self.assertEqual(bounded["verified_count"], 499)
        self.assertFalse(bounded["universal_proof_claimed"])
        for row in bounded["sample_first"] + bounded["sample_last"]:
            x, y, z = row["solution"]
            self.assertEqual(
                Fraction(4, row["n"]),
                Fraction(1, x) + Fraction(1, y) + Fraction(1, z),
            )

    def test_mixed_endpoint_roster_and_live_route(self):
        roster = load("route/sixteen-seat-roster-x2.json")
        self.assertEqual(len(roster["seats"]), 16)
        tavian = next(row for row in roster["seats"] if row["relational_name"] == "Tavian Sol")
        elaren = next(row for row in roster["seats"] if row["relational_name"] == "Elaren Kestrel")
        self.assertEqual(tavian["endpoint_kind"], "collaboration_subagent")
        self.assertEqual(elaren["endpoint_kind"], "main_task")
        next_route = load("route/next-route-x2.json")
        self.assertEqual(next_route["route_basis"], "current_route")
        self.assertEqual(next_route["next"]["relational_name"], "Elaren Kestrel")
        self.assertEqual(
            next_route["delivery_state"],
            "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        )

    def test_skills_initialized_validated_and_smoked(self):
        ledger = load("skills/skill-suite-receipt.json")
        self.assertEqual(ledger["skill_count"], 10)
        self.assertEqual(ledger["global_install_count"], 1)
        self.assertEqual(ledger["phase_local_count"], 9)
        self.assertTrue(
            all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in ledger["rows"])
        )

    def test_runners_invoked(self):
        ledger = load("tools/runner-suite-receipt.json")
        self.assertEqual(ledger["runner_count"], 10)
        self.assertTrue(all(row["valid"] for row in ledger["rows"]))
        self.assertEqual(sum(row["proposal_count"] for row in ledger["rows"]), 30)

    def test_portfolios_resolved_without_destructive_work(self):
        ledger = load("evidence/portfolio-execution-ledger.json")
        self.assertEqual(
            ledger["counts"],
            {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30},
        )
        self.assertTrue(ledger["all_safe_now_resolved"])
        self.assertTrue(ledger["all_bounded_candidates_resolved"])
        self.assertTrue(ledger["all_authorized_prototypes_resolved"])
        self.assertEqual((ledger["destructive_cleanup_count"], ledger["sibling_mutation_count"]), (0, 0))

    def test_gaps_gates_and_negatives_are_preserved(self):
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        negatives = load("truth/retained-negative-register-x2.json")
        self.assertEqual((gaps["effective_count"], gates["effective_count"]), (86, 85))
        self.assertEqual(gaps["new_rows"][0]["real_rows"], 0)
        self.assertEqual(gates["new_rows"][0]["authority_decisions"], 0)
        self.assertEqual(negatives["x2_operational_count"], 12)
        self.assertEqual(negatives["synthetic_mutation_negative_count"], 150)
        self.assertEqual(negatives["effective_at_evidence"], 11870)
        self.assertTrue(negatives["no_failure_erased"])

    def test_method_flow_and_truth_boundaries(self):
        ledger = load("method-flow/method-flow-ledger-evidence.json")
        self.assertEqual(ledger["counts"]["methods"], 129)
        self.assertEqual(ledger["counts"]["witness_results"]["fail"], 129)
        self.assertEqual(ledger["counts"]["witness_results"]["pass"], 129)
        truth = load("truth/phase-truth-evidence.json")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertEqual(truth["real_row_count"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
