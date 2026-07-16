from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v646-v3")
PHASE = ROOT / PHASE_REL


def x1_commit() -> str | None:
    result = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%H", "--", (PHASE_REL / "x1-proposals.json").as_posix()],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    rows = [row for row in result.stdout.splitlines() if row]
    return rows[-1] if rows else None


def read(relative: str) -> str:
    commit = x1_commit()
    path = (PHASE_REL / relative).as_posix()
    if commit:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True, encoding="utf-8")
    return (PHASE / relative).read_text(encoding="utf-8")


def load(relative: str) -> dict:
    return json.loads(read(relative))


class V646V3X1Tests(unittest.TestCase):
    def test_exactly_ten_distinct_proposals_and_four_labels(self) -> None:
        payload = load("x1-proposals.json")
        rows = payload["proposals"]
        self.assertEqual(payload["prior_frozen_proposal_count"], 410)
        self.assertEqual(payload["new_frozen_proposal_count"], 10)
        self.assertEqual(payload["frozen_chain_count_after_x1"], 420)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 10)
        self.assertEqual(len({row["title"] for row in rows}), 10)
        self.assertEqual(set(payload["outcome_classes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(Counter(row["expected_disposition"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertFalse(payload["expected_counts_are_results"])
        self.assertFalse(payload["x2_execution_present"])

    def test_semantic_novelty_audit_covers_all_410(self) -> None:
        audit = load("provenance/prior-proposal-collision-audit.json")
        self.assertEqual(audit["prior_frozen_proposal_count"], 410)
        self.assertEqual(audit["new_proposal_count"], 10)
        self.assertEqual(audit["exact_title_collision_count"], 0)
        self.assertEqual(len(audit["comparisons"]), 10)
        self.assertTrue(all(row["manual_result"] == "distinct" for row in audit["comparisons"]))

    def test_expanded_portfolios_have_no_completion_credit(self) -> None:
        portfolio = load("approval-packets/x1-approval-portfolio.json")
        self.assertEqual(
            portfolio["counts"],
            {
                "safe_now": 30,
                "safe_reviewed_after_rewrite": 15,
                "safe_new_sable": 15,
                "candidates": 20,
                "candidate_reviewed_after_rewrite": 10,
                "candidate_new_sable": 10,
                "inherited_exact": 10,
                "inherited_blocked": 5,
            },
        )
        self.assertEqual(portfolio["completion_credit_before_x2"], 0)
        self.assertTrue(all(row["x1_state"] == "preregistered_no_completion_credit" for row in portfolio["safe_now"] + portfolio["candidates"]))
        self.assertTrue(all(row["x2_execution"] in {"do_not_execute", "prohibited_without_new_evidence"} for row in portfolio["inherited_exact_packets"] + portfolio["inherited_blocked_packets"]))

    def test_skill_runner_cleanup_and_source_freeze(self) -> None:
        plan = load("prototypes/x1-skill-runner-plan.json")
        self.assertEqual(len(plan["skills"]), 20)
        self.assertEqual(len(plan["runners"]), 10)
        self.assertTrue(all(row["x2_state"] == "preregistered_not_built_or_used" for row in plan["skills"] + plan["runners"]))
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual(len(cleanup["tasks"]), 30)
        self.assertEqual(cleanup["destructive_task_count"], 0)
        self.assertEqual(cleanup["completion_credit_before_x2"], 0)
        sources = load("sources/source-ledger.json")
        self.assertEqual(len(sources["sources"]), 19)
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in sources["sources"]))
        self.assertEqual(sum(sources[key] for key in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs")), 0)

    def test_negative_and_gate_carry_forward(self) -> None:
        negatives = load("validation/x1-operational-negatives.json")
        self.assertEqual(negatives["inherited_effective"], 2619)
        self.assertEqual(negatives["new_x1_operational"], 5)
        self.assertEqual(negatives["preregistered_synthetic"], 70)
        self.assertEqual(negatives["effective_after_x1"], 2694)
        gates = load("x1-gate-carry-forward.json")
        self.assertEqual(gates["inherited_open_gaps"], 11)
        self.assertEqual(gates["inherited_exact_gates"], 12)
        self.assertEqual(gates["closed_in_x1"], 0)

    def test_method_flow_and_index_are_valid(self) -> None:
        method = load("method-flow/runner-validation.json")
        self.assertTrue(method["valid"])
        self.assertEqual(method["method_count"], 4)
        self.assertEqual(method["witness_count"], 9)
        self.assertIsInstance(load("tooling/x1-index/ghc-family-index.json"), dict)

    def test_x1_tree_contains_no_x2_or_closeout_lifecycle(self) -> None:
        commit = x1_commit()
        forbidden = ["phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"]
        for relative in forbidden:
            if commit:
                result = subprocess.run(["git", "cat-file", "-e", f"{commit}:{(PHASE_REL / relative).as_posix()}"], cwd=ROOT, capture_output=True)
                self.assertNotEqual(result.returncode, 0, relative)
            else:
                self.assertFalse((PHASE / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
