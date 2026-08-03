#!/usr/bin/env python3
"""Scoped x1-only checks for Neris Solane v660-v4."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v660_v4_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class NerisV660V4X1Tests(unittest.TestCase):
    def test_source_is_exact_and_same_owner_only(self) -> None:
        source = load("startup/source-verification.json")
        self.assertEqual(d.SOURCE_FINAL, source["head_before_x1"])
        self.assertEqual(d.SOURCE_BRANCH, source["source_branch"])
        self.assertTrue(source["source_tracking_equal"])
        self.assertTrue(source["source_direct_chain_valid"])
        self.assertEqual(3, source["source_phase_commit_count"])
        self.assertEqual(0, source["source_merge_count"])
        self.assertEqual(1, source["source_parent_count"])
        self.assertTrue(source["same_owner_only"])
        self.assertFalse(source["independent_reproduction"])

    def test_identity_language_is_relational_only(self) -> None:
        identity = load("identity/identity-and-boundary.json")
        self.assertEqual(d.OWNER, identity["name"])
        self.assertEqual(d.PRONOUNS, identity["pronouns"])
        for term in ("consciousness", "personhood", "qualification", "authority", "independent agency"):
            self.assertIn(term, identity["boundary"])

    def test_portfolio_has_twenty_selected_no_credit_and_twenty_new(self) -> None:
        rows = load("preregistration/proposal-ledger.json")["proposals"]
        self.assertEqual(d.CURRENT_PORTFOLIO_COUNT, len(rows))
        selected = [row for row in rows if row["origin"].startswith("selected_inherited")]
        new = [row for row in rows if row["origin"] == "new_unique_v660_v4_proposal"]
        self.assertEqual(20, len(selected))
        self.assertEqual(20, len(new))
        self.assertTrue(all(row["completion_credit"] is False for row in selected))
        self.assertTrue(all(row["novelty_credit"] is False for row in selected))
        self.assertEqual(40, len({row["proposal_id"] for row in rows}))
        self.assertEqual(40, len({row["title"] for row in rows}))

    def test_only_new_rows_extend_the_append_only_chain(self) -> None:
        rows = load("preregistration/proposal-ledger.json")["proposals"]
        selected = [row for row in rows if row["origin"].startswith("selected_inherited")]
        new = [row for row in rows if row["origin"] == "new_unique_v660_v4_proposal"]
        self.assertTrue(all(row["append_to_frozen_chain"] is False for row in selected))
        self.assertTrue(all(row["append_to_frozen_chain"] is True for row in new))
        self.assertEqual(list(range(1, 21)), [int(row["proposal_id"].split("P")[-1]) for row in new])

    def test_all_new_titles_are_checked_against_all_inherited_titles(self) -> None:
        audit = load("provenance/selection-and-novelty-audit.json")
        self.assertEqual(d.PRIOR_FROZEN, audit["prior_title_count"])
        self.assertEqual(d.NEW_UNIQUE_COUNT, audit["new_unique_count"])
        self.assertTrue(audit["all_new_titles_pass"])
        for row in audit["new_unique_results"]:
            self.assertEqual(d.PRIOR_FROZEN, row["inherited_titles_checked"])
            self.assertTrue(row["passes_bounded_threshold"])
            self.assertLess(row["max_token_jaccard"], audit["new_title_threshold"])
            self.assertLess(row["max_peer_token_jaccard"], audit["peer_title_threshold"])
            self.assertTrue(row["mechanism_reviewed"])

    def test_frozen_chain_grows_by_exactly_twenty(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(d.PRIOR_FROZEN, chain["prior_count"])
        self.assertEqual(0, chain["selection_rows_reappended"])
        self.assertEqual(d.NEW_UNIQUE_COUNT, chain["new_count"])
        self.assertEqual(d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT, chain["effective_count"])
        self.assertEqual(d.PRIOR_FROZEN, len(chain["prior_proposals"]))

    def test_expected_distribution_uses_only_four_truth_labels(self) -> None:
        ledger = load("preregistration/proposal-ledger.json")
        observed = Counter(
            row["expected_disposition"]
            for row in ledger["proposals"]
            if row["origin"] == "new_unique_v660_v4_proposal"
        )
        self.assertEqual(d.EXPECTED_DISTRIBUTION, dict(observed))
        self.assertEqual(d.ALLOWED_OUTCOMES, set(observed))
        self.assertFalse(ledger["outcomes_observed"])

    def test_every_proposal_has_bounded_preregistration_fields(self) -> None:
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in load("preregistration/proposal-ledger.json")["proposals"]:
            self.assertTrue(required.issubset(row), row["proposal_id"])
            self.assertTrue(row["protected_gates"], row["proposal_id"])

    def test_task_portfolio_counts_are_exact(self) -> None:
        packet = load("preregistration/task-portfolios.json")
        self.assertEqual(30, packet["counts"]["owner_safe_executed_x1"])
        self.assertEqual(20, packet["counts"]["successor_safe_recommendations"])
        self.assertEqual(10, packet["counts"]["owner_candidate_planned_x2"])
        self.assertEqual(10, packet["counts"]["successor_candidate_recommendations"])
        self.assertEqual(10, packet["counts"]["owner_exact_queued"])
        self.assertEqual(5, packet["counts"]["owner_blocked_queued"])
        self.assertTrue(all(row["state"] == "completed_x1_validation_only" for row in packet["owner_safe"]))
        self.assertTrue(all(row["recipient"] == "Vesper Arlen" for row in packet["successor_safe_recommendations"]))

    def test_skill_runner_and_cleanup_plans_are_frozen_not_built(self) -> None:
        tools = load("preregistration/skill-and-runner-plan.json")
        cleanup = load("preregistration/clean-fix-refine-plan.json")
        self.assertEqual(10, tools["counts"]["owner_skills"])
        self.assertEqual(10, tools["counts"]["owner_runners"])
        self.assertEqual(10, tools["counts"]["successor_skill_recommendations"])
        self.assertEqual(5, tools["counts"]["successor_runner_recommendations"])
        self.assertFalse(tools["implemented_in_x1"])
        self.assertEqual(30, cleanup["counts"]["owner_planned_x2"])
        self.assertEqual(30, cleanup["counts"]["successor_recommendation_only"])
        self.assertFalse(cleanup["deletion_authorized"])

    def test_source_ledger_is_bounded_vocabulary_only(self) -> None:
        sources = load("sources/official-source-ledger.json")
        self.assertEqual(len(d.OFFICIAL_SOURCES), sources["row_count"])
        self.assertTrue(all(row["status"] in {"current", "stable", "released", "draft", "watch"} for row in sources["rows"]))
        self.assertIn("no compliance", sources["boundary"])
        self.assertIn("Māori authority", sources["boundary"])

    def test_startup_failures_remain_zero_credit_and_all_recoveries_are_preferred(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        flow = load("method-flow/method-flow-state-x1.json")
        self.assertEqual(d.ACTIVATION_NEGATIVES, negatives["activation_baseline"])
        self.assertEqual(len(d.STARTUP_FAILURES), len(negatives["current_negatives"]))
        self.assertEqual(d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES), negatives["effective_negatives"])
        self.assertTrue(all(row["credit"] == 0 for row in negatives["current_negatives"]))
        self.assertEqual(len(d.STARTUP_FAILURES), flow["counts"]["methods"])
        self.assertEqual(0, flow["counts"]["states"]["candidate"])
        self.assertEqual(len(d.STARTUP_FAILURES), flow["counts"]["states"]["preferred"])
        self.assertEqual(len(d.STARTUP_FAILURES), Counter(row["result"] for row in flow["witnesses"])["fail"])
        self.assertEqual(len(d.STARTUP_FAILURES), Counter(row["result"] for row in flow["witnesses"])["pass"])

    def test_source_failed_aggregate_and_composite_receipts_are_preserved(self) -> None:
        receipts = load("startup/source-external-receipts.json")
        self.assertEqual(d.SOURCE_FAILED_AGGREGATE_WITNESS_SHA256, receipts["source_failed_aggregate_witness_bundle_sha256"])
        self.assertEqual(d.SOURCE_COMPOSITE_RECEIPT_SHA256, receipts["source_composite_completion_sha256"])
        self.assertEqual(d.SOURCE_ROUTE_RECEIPT_SHA256, receipts["source_route_delivery_sha256"])
        self.assertEqual(1, receipts["source_aggregate_invocations"])
        self.assertEqual(0, receipts["source_aggregate_successes"])
        self.assertFalse(receipts["source_aggregate_replayed"])

    def test_truth_preserves_gaps_gates_and_terminal_verdict(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT, truth["effective_frozen"])
        self.assertEqual(d.SOURCE_OPEN_GAPS, truth["effective_open_gaps"])
        self.assertEqual(d.SOURCE_EXACT_GATES, truth["effective_exact_gates"])
        self.assertFalse(truth["outcomes_observed"])
        self.assertEqual("NERIS_V660_V4_PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", truth["route_state"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_route_is_exact_terminally_gated_and_unsent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual("Neris Solane", route["current_exact_title"])
        self.assertEqual("Vesper Arlen", route["next_exact_title"])
        self.assertEqual("v660-v5", route["next_phase"])
        self.assertIsNone(route["recipient_next_exact_title"])
        self.assertIsNone(route["recipient_next_phase"])
        self.assertFalse(route["later_endpoint_inferred"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])
        for key in ("task_lookup_performed", "message_sent", "task_created", "task_forked", "subagent_spawned"):
            self.assertFalse(route[key])

    def test_x1_contains_no_x2_implementation_or_outcome(self) -> None:
        for relative in ("surfaces", "skills", "runners", "evidence", "closeout"):
            self.assertFalse((PHASE / relative).exists(), relative)
        self.assertFalse(load("preregistration/proposal-ledger.json")["outcomes_observed"])

    def test_owner_packet_privacy_scan_has_zero_confirmed_hits(self) -> None:
        privacy = load("validation/x1-privacy-scan.json")
        self.assertEqual(5, len(privacy["classes"]))
        self.assertEqual([], privacy["confirmed_hits"])
        self.assertGreaterEqual(len(privacy["definition_candidates"]), 3)
        self.assertFalse(privacy["privacy_complete"])

    def test_manifest_replays_declared_git_clean_bytes(self) -> None:
        manifest = load("validation/x1-content-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual("text bytes after CRLF-to-LF Git-clean normalization", manifest["hash_domain"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(row["bytes"], len(path.read_bytes().replace(b"\r\n", b"\n")), row["path"])
            self.assertEqual(row["sha256"], sha256(path), row["path"])

    def test_document_cap_and_overview_are_bounded(self) -> None:
        cap = load("validation/x1-document-cap.json")
        overview = (PHASE / "deliverables/v660-v4-x1-overview.md").read_text(encoding="utf-8")
        self.assertTrue(cap["passes"])
        self.assertLessEqual(cap["total_words"], cap["cap"])
        self.assertGreaterEqual(len(overview.split()), 900)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)

    def test_workflow_caps_and_route_are_explicit(self) -> None:
        plan = load("workflow/live-workflow-plan.json")
        self.assertFalse(plan["interstitial_variant"])
        self.assertEqual(5000, plan["latest_tracked_file_scan_cap"])
        self.assertEqual(8, plan["commit_cap"]["authorization_ceiling_total"])
        self.assertEqual(3, plan["commit_cap"]["phase_plan_total"])
        self.assertEqual("Vesper Arlen", plan["terminal_successor"]["title"])
        self.assertEqual("v660-v5", plan["terminal_successor"]["phase"])
        self.assertEqual("terminal_gate_required_prepared_not_sent", plan["terminal_successor"]["state"])
        self.assertIn("no replay after success", plan["canonical_validation"])

    def test_governance_preflight_preserves_latest_activation_cursor(self) -> None:
        receipt = load("tooling/skill-applicability-x1.json")
        preflight = receipt["governance_preflight"]
        self.assertIsNone(preflight["failed_witness_retained"])
        self.assertTrue(preflight["passing_witness_present"])
        self.assertIn("passed", preflight["state"])

    def test_family_current_planning_receipts_are_bounded(self) -> None:
        workflow = load("workflow/refinement/workflow-plan-validation.json")
        failed_workflow = load("workflow/refinement-failed-attempt-1/workflow-plan-validation.json")
        failed_issues = load("workflow/refinement-failed-attempt-1/workflow-plan-issues.json")
        index = load("tooling/family-index/ghc-family-index.json")
        reflection = load("tooling/reflection-remaster/reflection-remaster-inventory.json")
        issues = load("tooling/reflection-remaster/reflection-remaster-issues.json")
        method = load("tooling/method-flow/validation-x1.json")
        self.assertTrue(workflow["valid"])
        self.assertEqual(20, workflow["policy_checks_passed"])
        self.assertFalse(failed_workflow["valid"])
        self.assertEqual("policy_messaging_boundary", failed_issues["issues"][0]["code"])
        self.assertEqual(d.PHASE, index["phase"])
        self.assertEqual(d.OWNER, index["owner"])
        self.assertGreater(reflection["inventory_count"], reflection["scoped_count"])
        self.assertGreaterEqual(issues["issue_count"], 0)
        self.assertTrue(method["valid"])
        self.assertEqual(len(d.STARTUP_FAILURES), method["method_count"])
        self.assertEqual(2 * len(d.STARTUP_FAILURES), method["witness_count"])

    def test_roster_auth_and_meta_tool_receipts_are_structural_only(self) -> None:
        roster = load("tooling/governance/roster-validation-x1.json")
        auth = load("tooling/governance/auth-validation-x1.json")
        catalogue = load("tooling/meta-tool-box/catalogue.json")
        validation = load("tooling/meta-tool-box/validation.json")
        collisions = load("tooling/meta-tool-box/collisions.json")
        self.assertTrue(roster["valid"])
        self.assertEqual(15, roster["main_task_count"])
        self.assertEqual(1, roster["collaboration_subagent_count"])
        self.assertTrue(auth["valid"])
        self.assertEqual({"main_task": 15, "collaboration_subagent": 1}, auth["endpoint_counts"])
        self.assertEqual(0, len(catalogue["cards"]))
        self.assertTrue(validation["valid"])
        self.assertEqual(0, collisions["finding_count"])
        self.assertFalse(collisions["selection_performed"])


if __name__ == "__main__":
    unittest.main()
