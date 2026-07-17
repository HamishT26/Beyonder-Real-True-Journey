from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V6X1Tests(unittest.TestCase):
    def test_exact_ten_proposals(self) -> None:
        payload = load("x1-proposals.json")
        self.assertEqual(len(payload["proposals"]), 10)
        self.assertEqual(payload["prior_frozen_proposal_count"], 520)
        self.assertEqual(payload["frozen_chain_count_after_x1"], 530)

    def test_expected_distribution_only(self) -> None:
        proposals = load("x1-proposals.json")["proposals"]
        self.assertEqual(
            Counter(row["expected_disposition"] for row in proposals),
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(
            set(row["expected_disposition"] for row in proposals),
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_required_proposal_fields(self) -> None:
        required = {
            "hypothesis", "null_or_failure", "approval_class", "execution_lane",
            "current_primary_or_official_source_needs", "concrete_artifacts",
            "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
            "protected_gates", "expected_disposition",
        }
        for row in load("x1-proposals.json")["proposals"]:
            self.assertTrue(required.issubset(row))
            self.assertTrue(row["protected_gates"])

    def test_x1_has_no_execution_credit(self) -> None:
        self.assertFalse(load("x1-proposals.json")["x2_execution_present"])
        approval = load("approval-packets/x1-approval-portfolio.json")
        self.assertEqual(approval["x2_completion_credit"], 0)
        for category in ("safe_now", "candidates", "exact_approval", "blocked"):
            self.assertTrue(all(not row["x2_completion_credit"] for row in approval[category]))

    def test_expanded_portfolio_cardinality(self) -> None:
        approval = load("approval-packets/x1-approval-portfolio.json")
        plan = load("prototypes/x1-skill-runner-plan.json")
        clean = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((approval["safe_now_count"], approval["candidate_count"]), (30, 20))
        self.assertEqual((plan["skill_count"], plan["runner_count"]), (20, 10))
        self.assertEqual(clean["task_count"], 30)
        self.assertEqual((approval["exact_approval_count"], approval["blocked_count"]), (10, 5))

    def test_proposal_novelty_audit(self) -> None:
        audit = load("provenance/prior-proposal-collision-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual((audit["prior_count"], audit["new_count"], audit["exact_collision_count"]), (520, 10, 0))

    def test_portfolio_novelty_audit(self) -> None:
        audit = load("provenance/prior-portfolio-collision-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertEqual(audit["within_current_duplicates"], [])

    def test_source_status_vocabulary(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertEqual(ledger["source_count"], 20)
        self.assertTrue(set(row["status"] for row in ledger["sources"]) <= {"current", "stable", "draft", "watch"})
        self.assertEqual(ledger["real_rows"], 0)
        self.assertFalse(ledger["authority_delegated"])

    def test_method_flow_retains_failures_and_passes(self) -> None:
        flow = load("method-flow/method-flow-state.json")
        self.assertEqual(flow["counts"]["methods"], 5)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 5, "pass": 5})
        self.assertEqual(flow["counts"]["states"]["preferred"], 5)

    def test_retained_negative_baseline(self) -> None:
        ledger = load("retained-negative-register.json")
        self.assertEqual(ledger["inherited_effective_negatives"], 3579)
        self.assertEqual(ledger["x1_operational_negative_count"], 6)
        self.assertEqual(ledger["effective_x1_total"], 3585)
        self.assertEqual(ledger["erased_negative_count"], 0)

    def test_gate_carry_forward(self) -> None:
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["inherited_open_gaps"], gates["inherited_exact_gates"]), (22, 23))
        self.assertEqual(gates["closed_in_x1"], 0)

    def test_route_is_not_sent(self) -> None:
        route = load("orchestration/terminal-route-plan.json")
        update = load("orchestration/phase-update.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(update["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(update["task_created"])
        self.assertFalse(update["subagent_spawned"])

    def test_no_private_local_path_or_raw_uuid(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
            re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
            re.compile(r"\b(?:app|plugin)://", re.I),
            re.compile(r"<codex_delegation|source_thread_id", re.I),
        ]
        for path in PHASE.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for pattern in patterns:
                    self.assertIsNone(pattern.search(text), path.as_posix())

    def test_documents_under_word_cap(self) -> None:
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html"}:
                self.assertLessEqual(len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"))), 6000, path.as_posix())


if __name__ == "__main__":
    unittest.main()
