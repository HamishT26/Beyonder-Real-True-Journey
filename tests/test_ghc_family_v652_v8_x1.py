from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v652-v8"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V652V8X1Tests(unittest.TestCase):
    def test_identity_boundary(self) -> None:
        identity = load("identity/relational-identity.json")
        self.assertEqual(identity["owner"], "Neris Solane")
        self.assertIn("Relational working language only", identity["boundary"])
        self.assertIn("Māori authority", identity["boundary"])
        self.assertTrue(identity["hamish_may_rename_pause_redirect_or_stop"])

    def test_source_anchor(self) -> None:
        source = load("provenance/source-anchor-ledger.json")
        self.assertEqual(source["source_final"], "c39461888fa4db827616214f11c893fc6b0d40a3")
        self.assertEqual(source["source_to_final_commits"], 3)
        self.assertEqual(source["source_to_final_merges"], 0)
        self.assertTrue(source["all_single_parent"])
        self.assertEqual(source["verified_manifest_contracts"], 4)
        self.assertEqual(source["verified_manifest_entries"], 640)

    def test_exactly_thirty_proposals(self) -> None:
        ledger = load("preregistration/proposals.json")
        self.assertEqual(ledger["proposal_count"], 30)
        self.assertEqual(len(ledger["proposals"]), 30)

    def test_proposal_identifiers_unique(self) -> None:
        rows = load("preregistration/proposals.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in rows}), 30)
        self.assertEqual(len({row["title"] for row in rows}), 30)

    def test_required_proposal_fields(self) -> None:
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(required <= set(row), row["proposal_id"])

    def test_only_four_truth_labels(self) -> None:
        rows = load("preregistration/proposals.json")["proposals"]
        self.assertEqual(
            {row["expected_disposition"] for row in rows},
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_expected_distribution(self) -> None:
        ledger = load("preregistration/proposals.json")
        self.assertEqual(
            ledger["expected_outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )

    def test_frozen_chain_count(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((chain["prior_count"], chain["new_count"], chain["count"]), (1390, 30, 1420))
        self.assertEqual(len(chain["prior_proposals"]), 1390)
        self.assertEqual(len(chain["new_proposals"]), 30)

    def test_novelty_audit(self) -> None:
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["all_pass"])
        self.assertTrue(audit["all_manual_mechanism_distinct"])
        self.assertLess(audit["maximum_token_jaccard"], audit["threshold"])
        self.assertEqual(len(audit["rejected_collisions"]), 14)
        self.assertEqual(audit["inherited_unique_identifier_count"], 1370)
        self.assertEqual(audit["inherited_reused_identifier_count"], 20)
        self.assertEqual(audit["inherited_title_count"], 1390)
        self.assertFalse(audit["inherited_rows_rewritten"])

    def test_source_integrity(self) -> None:
        ledger = load("sources/source-ledger.json")
        source_ids = {row["source_id"] for row in ledger["sources"]}
        self.assertEqual(set(ledger["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        for proposal in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(set(proposal["official_or_primary_source_needs"]) <= source_ids)

    def test_exactly_150_unexecuted_mutations(self) -> None:
        plan = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(plan["mutation_count"], 150)
        self.assertEqual(plan["mutations_per_proposal"], 5)
        self.assertEqual(plan["executed_count"], 0)
        self.assertTrue(all(row["state"] == "preregistered_not_executed" for row in plan["mutations"]))

    def test_skill_and_runner_plans(self) -> None:
        skills = load("portfolios/skill-plan.json")
        runners = load("portfolios/runner-plan.json")
        self.assertEqual((skills["count"], runners["count"]), (10, 10))
        self.assertEqual((skills["state"], runners["state"]), ("frozen_not_built", "frozen_not_built"))

    def test_task_caps_are_not_quotas(self) -> None:
        safe = load("portfolios/safe-now-plan.json")
        candidate = load("portfolios/candidate-plan.json")
        self.assertLessEqual(safe["count"], safe["cap"])
        self.assertLessEqual(candidate["count"], candidate["cap"])
        self.assertGreaterEqual(safe["count"], 30)
        self.assertGreaterEqual(candidate["count"], 30)

    def test_x1_truth_is_unexecuted(self) -> None:
        truth = load("x1-phase-truth.json")
        self.assertEqual(truth["state"], "FROZEN_X1_NOT_EXECUTED")
        self.assertEqual(truth["mutation_executed_count"], 0)
        self.assertEqual(truth["skill_built_count"], 0)
        self.assertEqual(truth["runner_built_count"], 0)
        self.assertFalse(truth["x2_outcomes_present"])
        self.assertEqual(truth["frozen_chain_count"], 1420)
        self.assertEqual(truth["inherited_negatives"], 9098)
        self.assertEqual((truth["inherited_open_gaps"], truth["inherited_exact_gates"]), (68, 69))

    def test_method_flow_pairs(self) -> None:
        ledger = load("method-flow/x1-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 15)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 15, "pass": 15})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 15)

    def test_workflow_refinement_keeps_exact_existing_route_gated(self) -> None:
        request = load("workflow/workflow-plan-request.json")
        self.assertIn("Vesper Arlen", request["route"]["terminal_successor_resolution"])
        self.assertIn("only after the exact-final canonical gate", request["route"]["terminal_successor_resolution"])
        self.assertEqual(request["requirements"]["messaging"]["codex_route"], "existing_task_only_after_terminal_gate")
        self.assertEqual(request["requirements"]["commit_cap"], {"x1": 5, "x2": 5, "total": 8})
        overlay = load("workflow/current-live-route-overlay.json")
        self.assertFalse(overlay["tool_result_promoted_to_activation_authority"])
        self.assertIn("after_terminal_gate", overlay["live_request_authorizes"])

    def test_accessible_report_reserves_manual_evaluation(self) -> None:
        report = (PHASE / "reports/x1-accessible-report.html").read_text(encoding="utf-8")
        self.assertIn("<main>", report)
        self.assertIn("Manual and affected-user accessibility evaluation is reserved", report)
        self.assertIn("prefers-reduced-motion", report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = len((PHASE / "reports/x1-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 100000)

    def test_no_x2_output_files(self) -> None:
        names = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()]
        forbidden = ("evidence-receipt", "closeout-receipt", "seal-receipt", "final-validation-record", "mutation-results")
        self.assertFalse(any(any(token in name for token in forbidden) for name in names))

    def test_terminal_verdict_stays_not_ready(self) -> None:
        truth = load("x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()
