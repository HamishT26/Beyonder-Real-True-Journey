from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class ElarenV651V6X1Tests(unittest.TestCase):
    def test_source_and_identity(self) -> None:
        self.assertEqual(load("source/source-truth.json")["source_head"], SOURCE)
        identity = load("identity/relational-identity.json")
        self.assertEqual(identity["owner"], "Elaren Kestrel")
        self.assertIn("Relational working language only", identity["identity_boundary"])

    def test_exactly_thirty_proposals(self) -> None:
        packet = load("preregistration/proposals.json")
        self.assertEqual((packet["inherited_frozen_rows"], packet["new_proposal_count"], packet["frozen_rows_after_x1"]), (1030, 30, 1060))
        self.assertEqual(len(packet["proposals"]), 30)
        self.assertEqual(len({row["proposal_id"] for row in packet["proposals"]}), 30)
        self.assertEqual(len({row["title"] for row in packet["proposals"]}), 30)

    def test_complete_proposal_contract(self) -> None:
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(row) for row in load("preregistration/proposals.json")["proposals"]))

    def test_expected_truth_vocabulary(self) -> None:
        packet = load("preregistration/proposals.json")
        self.assertEqual(packet["expected_outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual({row["expected_disposition"] for row in packet["proposals"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_novelty_audit(self) -> None:
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertEqual((audit["inherited_rows_compared"], audit["new_rows_compared"], audit["frozen_rows_after_x1"]), (1030, 30, 1060))
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertLessEqual(audit["maximum_token_jaccard"], 0.25)

    def test_x1_is_outcome_free(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        self.assertTrue(truth["strict_x1_before_x2"])
        self.assertEqual(truth["x2_implementations"], 0)
        self.assertEqual(truth["observed_core_outcomes"], 0)
        self.assertEqual(truth["cli_siblings_spawned"], 0)

    def test_portfolio_plan(self) -> None:
        plan = load("portfolios/x1-portfolio-plan.json")
        self.assertEqual({key: len(plan[key]) for key in ("safe_now", "candidate", "skill_ideas", "runner_ideas", "clean_fix_refine")}, {"safe_now": 40, "candidate": 30, "skill_ideas": 20, "runner_ideas": 10, "clean_fix_refine": 40})
        self.assertEqual(plan["x1_implementation_count"], 0)
        self.assertTrue(plan["caps_are_ceilings_not_quotas"])

    def test_focus_preserves_all_pillars(self) -> None:
        focus = load("focus/primary-focus.json")
        self.assertEqual(focus["primary_pillar"], "GMUT Mind")
        self.assertEqual(set(focus["visible_pillars"]), {"GMUT Mind", "THOS Body", "Freed ID and CBR Heart"})
        self.assertIn("scientific-computing verification", focus["bounded_human_practice"])

    def test_source_ledger_is_attributable(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertGreaterEqual(ledger["entry_count"], 15)
        self.assertEqual(ledger["entry_count"], len(ledger["entries"]))
        self.assertTrue(all(row["url"].startswith("https://") for row in ledger["entries"]))
        self.assertTrue(set(row["status"] for row in ledger["entries"]) <= {"current", "stable", "draft", "watch"})

    def test_negative_and_method_flow_parity(self) -> None:
        negatives = load("truth/retained-negative-register.json")
        methods = load("method-flow/method-flow-ledger.json")
        self.assertEqual(negatives["new_x1_operational"], 5)
        self.assertEqual(negatives["effective_after_x1"], 7224)
        self.assertEqual(methods["counts"]["methods"], 5)
        self.assertEqual(methods["counts"]["witness_results"], {"fail": 5, "pass": 5})

    def test_live_plan_is_not_legacy_projection(self) -> None:
        live = load("workflow/workflow-plan-request.json")
        projection = load("workflow/workflow-plan-runner-compatible-request.json")
        override = load("workflow/live-policy-override.json")
        self.assertEqual(live["requirements"]["core_proposal_minimum"], 30)
        self.assertEqual(live["requirements"]["commit_cap"]["total"], 6)
        self.assertEqual(projection["requirements"]["commit_cap"]["total"], 4)
        self.assertTrue(override["authoritative"])
        self.assertFalse(override["legacy_projection_authoritative"])

    def test_route_and_exact_gate(self) -> None:
        route = load("orchestration/x1-phase-state.json")
        held = load("approvals/held-packets.json")
        self.assertEqual((route["immediate_successor"], route["successor_phase"]), ("Vesper Arlen", "v651-v7"))
        self.assertFalse(route["x2_started"])
        self.assertFalse(held["new_exact_gate"]["executed"])

    def test_environment_is_read_only(self) -> None:
        receipt = load("environment/environment-version-receipt.json")
        self.assertEqual(receipt["codex_cli"], "0.144.5")
        self.assertTrue(receipt["versions_verified_only"])
        self.assertFalse(receipt["desktop_updated"])
        self.assertFalse(receipt["host_security_changed"])

    def test_stage20_abstains(self) -> None:
        self.assertEqual(load("truth/x1-phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
