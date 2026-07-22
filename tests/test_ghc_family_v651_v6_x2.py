from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class ElarenV651V6X2Tests(unittest.TestCase):
    def test_core_distribution(self) -> None:
        self.assertEqual(load("outcomes/core-outcomes.json")["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_mutation_execution(self) -> None:
        receipt = load("validation/mutation-execution-receipt.json")
        self.assertEqual((receipt["executed"], receipt["rejected"], receipt["accepted"]), (100, 100, 0))

    def test_negative_accounting(self) -> None:
        negatives = load("truth/retained-negative-register-x2.json")
        self.assertEqual(negatives["effective_total"], 7325)
        self.assertEqual(negatives["failures_erased"], 0)

    def test_gate_accounting(self) -> None:
        gates = load("gates/exact-open-gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (57, 58))
        self.assertEqual(gates["silently_closed"], 0)

    def test_empirical_and_authority_abstention(self) -> None:
        truth = load("truth/evidence-phase-truth.json")
        self.assertEqual((truth["real_data_rows"], truth["participants"], truth["real_keys_or_proofs"], truth["authority_decisions"], truth["production_actions"]), (0, 0, 0, 0, 0))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_portfolio_completion(self) -> None:
        portfolio = load("portfolios/x2-portfolio-outcomes.json")
        self.assertEqual(portfolio["counts"], {"safe_now_completed": 40, "candidate_resolved": 30, "skills_built_validated_used": 20, "runners_built_invoked": 10, "clean_fix_refine_completed": 40})
        self.assertTrue(portfolio["all_authorized_planned_items_resolved"])

    def test_skill_receipt(self) -> None:
        receipt = load("tooling/skill-build-receipt.json")
        self.assertEqual((receipt["skill_count"], receipt["initialized"], receipt["quick_validated"], receipt["smoke_used"], receipt["global_installs"]), (20, 20, 20, 20, 0))
        self.assertTrue(all(row["valid"] and row["smoke_valid"] for row in receipt["skills"]))

    def test_runner_receipt(self) -> None:
        receipt = load("tooling/runner-use-receipt.json")
        self.assertEqual((receipt["runner_count"], receipt["invoked_count"], receipt["surface_coverage_count"]), (10, 10, 30))
        self.assertFalse(receipt["independent_implementations_claimed"])

    def test_static_report_structure(self) -> None:
        text = (ROOT / "reports/accessible-static-report.html").read_text(encoding="utf-8").casefold()
        for token in ('<html lang="en">', '<main>', '<nav aria-label=', '<caption>', '<th scope="col">', 'manual accessibility review', 'not_ready_for_stage_20'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text)

    def test_overview_length_and_boundary(self) -> None:
        text = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 3000)
        self.assertLessEqual(len(text.split()), 100000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_source_ids_resolve(self) -> None:
        sources = {row["source_id"] for row in load("sources/source-ledger.json")["entries"]}
        self.assertTrue(all(set(row["official_or_primary_source_needs"]) <= sources for row in load("preregistration/proposals.json")["proposals"]))

    def test_method_flow_x1_preserved(self) -> None:
        ledger = load("method-flow/x2-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 6)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 6, "pass": 6})

    def test_x1_commit_is_ancestor(self) -> None:
        subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=REPO, check=True)

    def test_caps_are_not_quotas(self) -> None:
        plan = load("portfolios/x1-portfolio-plan.json")
        self.assertTrue(plan["caps_are_ceilings_not_quotas"])
        self.assertLessEqual(len(plan["safe_now"]) + len(plan["candidate"]), 1000)

    def test_only_four_core_labels(self) -> None:
        outcomes = load("outcomes/core-outcomes.json")
        self.assertEqual(set(row["truth_label"] for row in outcomes["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})


def make_surface_test(slug: str):
    def test(self: ElarenV651V6X2Tests) -> None:
        proposal = next(row for row in load("preregistration/proposals.json")["proposals"] if row["slug"] == slug)
        evidence = load(f"proposals/{slug}.json")
        self.assertEqual(evidence["proposal_id"], proposal["proposal_id"])
        self.assertEqual(evidence["truth_label"], proposal["expected_disposition"])
        self.assertTrue(evidence["valid_fixture_passed"])
        self.assertIn(evidence["rejected_mutation_count"], {3, 4})
        self.assertEqual(evidence["rejected_mutation_count"], len(evidence["rejecting_mutation_ids"]))
        self.assertFalse(evidence["independent_reproduction"])
        self.assertTrue(all(value is False for value in evidence["protected_claims"].values()))
    return test


for _row in load("preregistration/proposals.json")["proposals"]:
    setattr(ElarenV651V6X2Tests, f"test_surface_{_row['proposal_id'].lower().replace('-', '_')}", make_surface_test(_row["slug"]))


if __name__ == "__main__":
    unittest.main()
