#!/usr/bin/env python3
"""Scoped x1-only checks for the Lyren Moss v658-v8 (2) remaster."""

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

import ghc_family_v658_v8_2_remaster_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LyrenV658V8RemasterX1Tests(unittest.TestCase):
    def test_source_is_exact_and_same_owner_only(self) -> None:
        source = load("startup/source-verification.json")
        self.assertEqual(d.SOURCE_FINAL, source["head_before_x1"])
        self.assertEqual(d.SOURCE_BRANCH, source["source_branch"])
        self.assertTrue(source["source_tracking_equal"])
        self.assertTrue(source["same_owner_only"])
        self.assertFalse(source["independent_reproduction"])

    def test_identity_language_is_relational_only(self) -> None:
        identity = load("identity/identity-and-boundary.json")
        self.assertEqual("Lyren Moss", identity["name"])
        self.assertEqual("they/them", identity["pronouns"])
        for term in ("consciousness", "personhood", "qualification", "authority", "independent agency"):
            self.assertIn(term, identity["boundary"])

    def test_portfolio_is_twenty_selected_plus_twenty_new(self) -> None:
        ledger = load("preregistration/proposal-ledger.json")
        rows = ledger["proposals"]
        self.assertEqual(40, ledger["proposal_count"])
        self.assertEqual(20, ledger["selected_inherited_count"])
        self.assertEqual(20, ledger["new_unique_count"])
        self.assertEqual(20, sum(row["origin"] == "selected_inherited_from_frozen_2890" for row in rows))
        self.assertEqual(20, sum(row["origin"] == "new_unique_remaster_proposal" for row in rows))
        self.assertEqual(40, len({row["proposal_id"] for row in rows}))
        self.assertEqual(40, len({row["title"] for row in rows}))

    def test_selected_rows_are_provenanced_and_not_reappended(self) -> None:
        rows = load("preregistration/proposal-ledger.json")["proposals"][:20]
        self.assertTrue(all(row["source_proposal_id"] for row in rows))
        self.assertTrue(all(row["source_slug"] for row in rows))
        self.assertTrue(all(row["append_to_frozen_chain"] is False for row in rows))
        self.assertEqual(list(range(1, 21)), [row["selection_rank"] for row in rows])

    def test_all_new_titles_are_checked_against_all_inherited_titles(self) -> None:
        audit = load("provenance/selection-and-novelty-audit.json")
        self.assertEqual(2890, audit["prior_title_count"])
        self.assertEqual(20, audit["new_unique_count"])
        self.assertTrue(audit["all_new_titles_pass"])
        for row in audit["new_unique_results"]:
            self.assertEqual(2890, row["inherited_titles_checked"])
            self.assertTrue(row["passes_bounded_threshold"])
            self.assertLess(row["max_token_jaccard"], audit["new_title_threshold"])

    def test_frozen_chain_grows_by_only_twenty(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(2890, chain["prior_count"])
        self.assertEqual(20, chain["selected_inherited_count"])
        self.assertEqual(0, chain["selection_rows_reappended"])
        self.assertEqual(20, chain["new_count"])
        self.assertEqual(2910, chain["effective_count"])
        self.assertEqual(2890, len(chain["prior_proposals"]))
        self.assertEqual(20, len(chain["new_proposals"]))

    def test_expected_distribution_uses_only_four_truth_labels(self) -> None:
        ledger = load("preregistration/proposal-ledger.json")
        observed = Counter(row["expected_disposition"] for row in ledger["proposals"])
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
            self.assertTrue(row["official_or_primary_source_needs"], row["proposal_id"])

    def test_task_portfolio_counts_are_exact(self) -> None:
        packet = load("preregistration/task-portfolios.json")
        self.assertEqual(
            {
                "lyren_safe_executed_x1": 30,
                "ilyra_safe_seeds": 20,
                "lyren_candidate_planned_x2": 10,
                "ilyra_candidate_seeds": 10,
                "lyren_exact_queued": 10,
                "lyren_blocked_queued": 5,
            },
            packet["counts"],
        )
        self.assertTrue(all(row["state"] == "completed_x1_validation_only" for row in packet["lyren_safe"]))
        self.assertTrue(all(row["state"] == "seed_only_not_executed_by_lyren" for row in packet["ilyra_safe_seeds"]))

    def test_skill_runner_and_cleanup_plans_are_frozen_not_built(self) -> None:
        tools = load("preregistration/skill-and-runner-plan.json")
        cleanup = load("preregistration/clean-fix-refine-plan.json")
        self.assertEqual(
            {"lyren_skills": 10, "ilyra_skill_seeds": 10, "lyren_runners": 10, "ilyra_runner_seeds": 5},
            tools["counts"],
        )
        self.assertFalse(tools["implemented_in_x1"])
        self.assertEqual({"lyren_planned_x2": 30, "ilyra_seed_only": 30, "total_planned": 60}, cleanup["counts"])
        self.assertFalse(cleanup["deletion_authorized"])

    def test_source_ledger_is_bounded_vocabulary_only(self) -> None:
        sources = load("sources/official-source-ledger.json")
        self.assertEqual(10, sources["row_count"])
        self.assertEqual(10, len(sources["rows"]))
        self.assertIn("no compliance", sources["boundary"])
        self.assertIn("Māori authority", sources["boundary"])

    def test_startup_failures_remain_zero_credit_with_paired_recovery(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        flow = load("method-flow/method-flow-state-x1.json")
        self.assertEqual(17857, negatives["activation_baseline"])
        self.assertEqual(12, len(negatives["current_negatives"]))
        self.assertEqual(17869, negatives["effective_negatives"])
        self.assertTrue(all(row["credit"] == 0 for row in negatives["current_negatives"]))
        self.assertEqual(12, flow["counts"]["methods"])
        self.assertEqual(4143, flow["cumulative_counts"]["effective_methods"])
        self.assertEqual(Counter({"fail": 12, "pass": 12}), Counter(row["result"] for row in flow["witnesses"]))

    def test_truth_preserves_gaps_gates_and_terminal_verdict(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(2910, truth["effective_frozen"])
        self.assertEqual(120, truth["effective_open_gaps"])
        self.assertEqual(119, truth["effective_exact_gates"])
        self.assertFalse(truth["outcomes_observed"])
        self.assertEqual("PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", truth["route_state"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_route_is_exact_terminally_gated_and_unsent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual("Ilyra Fen", route["next_exact_title"])
        self.assertEqual("v659-v1", route["next_phase"])
        self.assertEqual("Auren Lark", route["recipient_next_exact_title"])
        self.assertEqual("v659-v2", route["recipient_next_phase"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_x1_contains_no_remaster_x2_implementation_or_outcome(self) -> None:
        self.assertFalse((PHASE / "surfaces").exists())
        self.assertFalse((PHASE / "skills").exists())
        self.assertFalse((PHASE / "runners").exists())
        self.assertFalse((PHASE / "evidence").exists())
        self.assertFalse((PHASE / "closeout").exists())
        self.assertFalse(load("preregistration/proposal-ledger.json")["outcomes_observed"])

    def test_owner_packet_privacy_scan_has_zero_confirmed_hits(self) -> None:
        privacy = load("validation/x1-privacy-scan.json")
        self.assertEqual(5, len(privacy["classes"]))
        self.assertEqual([], privacy["confirmed_hits"])
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["privacy_complete"])

    def test_manifest_replays_exact_working_bytes(self) -> None:
        manifest = load("validation/x1-content-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertIn("validation/x1-content-manifest.json", manifest["exclusions"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(row["bytes"], path.stat().st_size, row["path"])
            self.assertEqual(row["sha256"], sha256(path), row["path"])

    def test_document_cap_and_overview_are_bounded(self) -> None:
        cap = load("validation/x1-document-cap.json")
        overview = (PHASE / "deliverables/v658-v8-2-remaster-x1-overview.md").read_text(encoding="utf-8")
        self.assertTrue(cap["passes"])
        self.assertLessEqual(cap["total_words"], cap["cap"])
        self.assertGreaterEqual(len(overview.split()), 900)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)

    def test_workflow_caps_and_interstitial_arithmetic_are_explicit(self) -> None:
        plan = load("workflow/live-workflow-plan.json")
        self.assertTrue(plan["interstitial_variant"])
        self.assertFalse(plan["changes_canonical_phase_arithmetic"])
        self.assertEqual(5000, plan["latest_tracked_file_scan_cap"])
        self.assertEqual(3, plan["commit_cap"]["total"])
        self.assertIn("no replay after success", plan["canonical_validation"])

    def test_family_current_tool_receipts_are_bounded_and_valid(self) -> None:
        workflow = load("workflow/refinement/workflow-plan-validation.json")
        roster = load("tooling/governance/roster-validation-x1.json")
        auth = load("tooling/governance/auth-validation-x1.json")
        method = load("tooling/method-flow/validation-x1.json")
        toolbox = load("tooling/meta-tool-box/validation.json")
        reflection = load("tooling/reflection-remaster/reflection-remaster-inventory.json")
        issues = load("tooling/reflection-remaster/reflection-remaster-issues.json")
        self.assertTrue(workflow["valid"])
        self.assertEqual(20, workflow["policy_checks_passed"])
        self.assertEqual(16, roster["seat_count"])
        self.assertTrue(roster["valid"])
        self.assertTrue(auth["valid"])
        self.assertEqual(15, auth["endpoint_counts"]["main_task"])
        self.assertTrue(method["valid"])
        self.assertEqual(12, method["method_count"])
        self.assertEqual(24, method["witness_count"])
        self.assertTrue(toolbox["valid"])
        self.assertEqual(4514, reflection["inventory_count"])
        self.assertEqual(7, reflection["scoped_count"])
        self.assertEqual(1, issues["issue_count"])

    def test_legacy_builder_is_gated_and_inherited_trace_restored(self) -> None:
        receipt = load("tooling/skill-applicability-x1.json")
        legacy = receipt["legacy_startup_builder"]
        self.assertTrue(legacy["invocation_owned_outputs_removed"])
        self.assertTrue(legacy["inherited_live_trace_diff_clean"])
        self.assertFalse(legacy["may_be_reused_for_this_phase"])
        self.assertEqual("ghc-family-solo-activation", receipt["missing_named_skill"])


if __name__ == "__main__":
    unittest.main()
