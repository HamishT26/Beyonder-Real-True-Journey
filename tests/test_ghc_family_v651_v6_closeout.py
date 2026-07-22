from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"
EVIDENCE = "94b9afc4f8289e8fdf1a304c90c0765e3beb055f"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class ElarenV651V6CloseoutTests(unittest.TestCase):
    def test_final_truth_and_outcomes(self) -> None:
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite_run"])

    def test_all_negatives_are_retained(self) -> None:
        negatives = load("final/retained-negative-register.json")
        self.assertEqual(negatives["effective"], 7327)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(negatives["failures_erased"], 0)

    def test_open_gaps_and_exact_gates_remain(self) -> None:
        gates = load("final/gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (57, 58))
        self.assertEqual(gates["silently_closed"], 0)

    def test_file_backed_baton_and_prepared_route(self) -> None:
        text = (ROOT / "handoffs/vesper-arlen-v651-v7-activation.md").read_text(encoding="utf-8")
        count = len(re.findall(r"\b[\w'-]+\b", text))
        self.assertGreaterEqual(count, 10000)
        self.assertLessEqual(count, 100000)
        self.assertIn("PREPARED_NOT_SENT_AT_COMMIT", text)
        route = load("orchestration/final-route-state.json")
        self.assertEqual((route["target_exact_title"], route["target_phase"], route["send_count"]), ("Vesper Arlen", "v651-v7", 0))

    def test_no_task_subagent_or_cli_sibling(self) -> None:
        route = load("orchestration/final-route-state.json")
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertFalse(route["cli_sibling_created"])

    def test_overview_and_static_report(self) -> None:
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 3000)
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8").casefold()
        for token in ('<html lang="en">', "<main>", '<nav aria-label="report">', "<caption>", '<th scope="col">', "manual accessibility review", "affected-user"):
            self.assertIn(token, report)
        self.assertNotIn("<script", report)

    def test_environment_is_observation_only(self) -> None:
        environment = load("final/environment-receipt.json")
        self.assertEqual(environment["codex_cli"], "0.144.5")
        self.assertTrue(environment["versions_verified_only"])
        self.assertFalse(environment["software_updated"])
        self.assertFalse(environment["host_security_changed"])

    def test_single_scoped_canonical_pass_plan(self) -> None:
        plan = load("validation/final-validation-plan.json")
        self.assertFalse(plan["full_repository_suite"])
        self.assertTrue(plan["eiren_owns_full_repository_suite"])
        self.assertEqual(plan["successful_canonical_pass_limit"], 1)
        self.assertFalse(plan["post_success_replay"])
        self.assertFalse(plan["detached_replay"])
        self.assertFalse(plan["named_replay"])

    def test_combined_closeout_and_seal_are_candidate_truth(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        seal = load("seal/seal-receipt.json")
        final = load("final/final-record.json")
        self.assertTrue(closeout["post_commit_validation_required"])
        self.assertFalse(seal["exact_final_commit_known_inside_own_tree"])
        self.assertIsNone(final["final_commit"])

    def test_anchor_contract_and_commit_cap(self) -> None:
        contract = load("lifecycle/anchor-contract.json")
        self.assertEqual((contract["source_commit"], contract["x1_commit"], contract["evidence_commit"]), (SOURCE, X1, EVIDENCE))
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO, check=True)
        count = int(subprocess.check_output(["git", "rev-list", "--count", f"{SOURCE}..HEAD"], cwd=REPO, text=True, encoding="utf-8"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 6)

    def test_exact_manifest_and_review_contracts(self) -> None:
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertGreater(delta["entry_count"], 0)
        self.assertGreater(owner["entry_count"], 0)
        self.assertEqual(len(delta["self_exclusions"]), 4)
        self.assertEqual(len(owner["self_exclusions"]), 4)
        self.assertTrue(review["valid"])

    def test_portfolio_and_owner_caps(self) -> None:
        portfolio = load("portfolios/x2-portfolio-outcomes.json")
        threshold = load("validation/final-owner-file-threshold.json")
        documents = load("validation/final-document-cap-receipt.json")
        self.assertTrue(portfolio["all_authorized_planned_items_resolved"])
        self.assertTrue(threshold["within_threshold"])
        self.assertTrue(documents["valid"])


if __name__ == "__main__":
    unittest.main()
