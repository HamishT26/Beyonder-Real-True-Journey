#!/usr/bin/env python3
"""Owner-scoped x2 evidence checks for Elowen Cairn v661-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v661_v6_runtime as runtime  # noqa: E402
import ghc_family_v661_v6_x2_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


class ElowenCairnV661V6X2Tests(unittest.TestCase):
    def test_x1_gate_is_exact_and_four_way_equal(self) -> None:
        gate = load("evidence/x1-to-x2-gate.json")
        self.assertEqual(d.X1_FREEZE, gate["x1_freeze"])
        self.assertEqual(d.X1_FREEZE, gate["local"])
        self.assertEqual(d.X1_FREEZE, gate["upstream"])
        self.assertEqual(d.X1_FREEZE, gate["tracking"])
        self.assertEqual(d.X1_FREEZE, gate["fresh_live_remote"])
        self.assertEqual({"ahead": 0, "behind": 0}, gate["divergence"])
        self.assertTrue(gate["four_way_equal"])
        self.assertEqual([], gate["x1_owned_path_drift"])

    def test_x1_preregistration_bytes_are_immutable(self) -> None:
        paths = [
            f"{d.PHASE_ROOT}/preregistration/proposal-ledger.json",
            f"{d.PHASE_ROOT}/provenance/frozen-chain-proposal-index.json",
            "scripts/ghc_family_v661_v6_data.py",
            "scripts/build_ghc_family_v661_v6_x1.py",
            "tests/test_ghc_family_v661_v6_x1.py",
        ]
        for relative in paths:
            self.assertEqual(
                git_bytes("show", f"{d.X1_FREEZE}:{relative}"),
                git_bytes("show", f":{relative}") if relative in subprocess.check_output(
                    ["git", "-C", str(ROOT), "diff", "--cached", "--name-only"],
                    text=True,
                    encoding="utf-8",
                ).splitlines() else (ROOT / relative).read_bytes().replace(b"\r\n", b"\n"),
                relative,
            )

    def test_x1_only_absence_contract_is_recovered_from_immutable_tree(self) -> None:
        receipt = load("validation/immutable-x1-lifecycle-recovery.json")
        self.assertEqual(d.X1_FREEZE, receipt["x1_freeze"])
        self.assertEqual([], receipt["present_in_x1_tree"])
        self.assertTrue(receipt["historical_assertion_found_in_exact_x1_test_blob"])
        self.assertEqual(0, receipt["advanced_tree_assertion_credit"])
        self.assertTrue(receipt["immutable_x1_recovery_passed"])
        self.assertFalse(receipt["x1_files_modified"])

    def test_twenty_new_outcomes_use_only_allowed_labels(self) -> None:
        payload = load("evidence/proposal-outcomes.json")
        self.assertEqual(40, payload["proposal_count"])
        self.assertEqual(20, payload["selected_inherited_count"])
        self.assertEqual(20, payload["new_unique_count"])
        self.assertEqual(0, payload["selected_inherited_novelty_credit"])
        self.assertEqual(0, payload["selected_inherited_completion_credit"])
        self.assertEqual(d.EXPECTED_DISTRIBUTION, payload["observed_outcome_counts"])
        self.assertEqual(d.ALLOWED_OUTCOMES, set(payload["observed_outcome_counts"]))

    def test_every_new_surface_passes_and_rejects_five_mutations(self) -> None:
        outcomes = load("evidence/proposal-outcomes.json")["outcomes"]
        self.assertEqual(20, len(outcomes))
        for row in outcomes:
            self.assertTrue(row["valid_fixture_passed"], row["proposal_id"])
            self.assertTrue(row["all_mutations_rejected"], row["proposal_id"])
            self.assertEqual(5, row["mutation_count"])
            contract = load(f"surfaces/{row['slug']}/contract.json")
            accepted, errors = runtime.validate_contract(contract)
            self.assertTrue(accepted, (row["proposal_id"], errors))
            self.assertEqual(0, contract["fixture"]["real_world_rows"])
            self.assertEqual(0, contract["fixture"]["external_actions"])

    def test_all_one_hundred_mutations_are_rejected_zero_credit(self) -> None:
        register = load("evidence/mutation-register.json")
        self.assertEqual(100, register["mutation_count"])
        self.assertEqual(100, register["rejected_count"])
        self.assertEqual(0, register["accepted_count"])
        self.assertEqual(0, register["completion_credit"])
        self.assertTrue(all(row["credit"] == 0 for row in register["mutations"]))

    def test_selected_inherited_revalidation_is_zero_credit(self) -> None:
        rows = sorted((PHASE / "evidence/selected-revalidation").glob("*.json"))
        self.assertEqual(20, len(rows))
        for path in rows:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(receipt["source_title_equal"])
            self.assertTrue(receipt["source_valid_fixture_passed"])
            self.assertTrue(receipt["source_mutations_rejected"])
            self.assertEqual("Tamar Vey", receipt["source_owner"])
            self.assertEqual(0, receipt["source_novelty_credit"])
            self.assertEqual(0, receipt["source_completion_credit"])
            self.assertFalse(receipt["reappended"])
            self.assertFalse(receipt["source_mutations_reexecuted"])

    def test_open_gap_and_exact_gate_increase_once(self) -> None:
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual(d.SOURCE_OPEN_GAPS + 1, gaps["effective_open_gaps"])
        self.assertEqual(d.SOURCE_EXACT_GATES + 1, gates["effective_exact_gates"])
        self.assertFalse(gaps["closed"])
        self.assertFalse(gates["closed"])

    def test_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        register = load("truth/exact-and-blocked-register-x2.json")
        self.assertEqual(10, register["exact_count"])
        self.assertEqual(5, register["blocked_count"])
        self.assertEqual(0, register["executed_count"])
        self.assertTrue(all(row["state"] == "exact_gate_unexecuted" for row in register["exact_rows"]))
        self.assertTrue(all(row["state"] == "blocked_unexecuted" for row in register["blocked_rows"]))

    def test_negative_register_preserves_x1_and_mutations(self) -> None:
        register = load("truth/retained-negative-register-x2.json")
        self.assertEqual(d.ACTIVATION_NEGATIVES, register["activation_baseline"])
        self.assertEqual(len(d.STARTUP_FAILURES), register["x1_operational"])
        self.assertEqual(100, register["x2_synthetic_mutations"])
        self.assertEqual(len(d.X2_OPERATIONAL_FAILURES), register["x2_operational"])
        self.assertEqual(
            d.ACTIVATION_AFTER_X1_NEGATIVES + 100 + len(d.X2_OPERATIONAL_FAILURES),
            register["effective_negatives"],
        )
        self.assertTrue(register["all_failures_retained"])

    def test_method_flow_retains_x1_and_x2_witnesses(self) -> None:
        flow = load("method-flow/method-flow-state-x2.json")
        method_count = len(d.STARTUP_FAILURES) + len(d.NEW_PROPOSAL_SPECS) + len(d.X2_OPERATIONAL_FAILURES)
        fail_count = len(d.STARTUP_FAILURES) + len(d.NEW_PROPOSAL_SPECS) * 5 + len(d.X2_OPERATIONAL_FAILURES)
        self.assertEqual(method_count, flow["counts"]["methods"])
        self.assertEqual(fail_count, flow["counts"]["witness_results"]["fail"])
        self.assertEqual(method_count, flow["counts"]["witness_results"]["pass"])
        self.assertEqual(fail_count + method_count, flow["counts"]["witnesses"])
        self.assertEqual(method_count, flow["counts"]["states"]["preferred"])
        self.assertEqual(d.ACTIVATION_METHODS + method_count, flow["cumulative_counts"]["effective_methods"])

    def test_ten_skills_and_ten_runners_are_validated_and_used(self) -> None:
        aggregate = load("tooling/skill-runner-aggregate.json")
        creator = load("validation/phase-local-skill-creator-validation.json")
        self.assertEqual(10, aggregate["skills_built_validated_smoke_used"])
        self.assertEqual(10, aggregate["runners_built_invoked"])
        self.assertEqual(0, aggregate["global_installs"])
        self.assertTrue(aggregate["all_valid"])
        self.assertEqual(10, creator["first_invocation_count"])
        self.assertEqual(0, creator["first_invocation_pass_count"])
        self.assertEqual(10, creator["recovery_invocation_count"])
        self.assertEqual(10, creator["recovery_pass_count"])
        self.assertTrue(creator["all_recovery_validations_passed"])
        self.assertEqual([f"V6616-X2-N{index:03d}" for index in range(4, 14)], creator["first_invocation_negative_ids"])
        self.assertFalse(creator["recovery"]["bounded_external_parser_shim"])
        self.assertTrue(creator["recovery"]["python_utf8_process_local"])
        self.assertFalse(creator["recovery"]["skill_files_modified_for_recovery"])
        self.assertFalse(creator["global_install"])
        for (name, _purpose), _spec in zip(d.SELF_RUNNER_SPECS, d.NEW_PROPOSAL_SPECS[:10], strict=True):
            self.assertTrue((ROOT / "scripts" / name).is_file())
        for name, _purpose in d.SELF_SKILL_SPECS:
            self.assertTrue((PHASE / "skills" / name / "SKILL.md").is_file())
            self.assertTrue((PHASE / "skills" / name / "examples/smoke.json").is_file())

    def test_family_governance_and_reflection_tools_have_bounded_x2_receipts(self) -> None:
        method = load("tooling/method-flow/validation-x2.json")
        workflow = load("workflow/refinement-x2/workflow-plan-validation.json")
        inventory = load("tooling/reflection-remaster-x2/reflection-remaster-inventory.json")
        issues = load("tooling/reflection-remaster-x2/reflection-remaster-issues.json")
        toolbox = load("tooling/meta-tool-box-x2/validation.json")
        collisions = load("tooling/meta-tool-box-x2/collisions.json")
        self.assertTrue(method["valid"])
        self.assertEqual(
            len(d.STARTUP_FAILURES) + len(d.NEW_PROPOSAL_SPECS) + len(d.X2_OPERATIONAL_FAILURES),
            method["method_count"],
        )
        self.assertEqual([], method["privacy_hits"])
        self.assertTrue(workflow["valid"])
        self.assertEqual(20, workflow["policy_checks_passed"])
        self.assertEqual(0, workflow["privacy_findings"])
        self.assertGreater(inventory["inventory_count"], inventory["scoped_count"])
        self.assertGreaterEqual(inventory["scoped_count"], 0)
        self.assertGreaterEqual(issues["issue_count"], 0)
        self.assertTrue(toolbox["valid"])
        self.assertEqual(20, toolbox["card_count"])
        self.assertGreaterEqual(collisions["finding_count"], 0)
        self.assertFalse(collisions["selection_performed"])

    def test_candidates_and_cleanups_are_bounded(self) -> None:
        candidates = load("evidence/candidate-task-receipts.json")
        cleanup = load("evidence/clean-fix-refine-receipts.json")
        self.assertEqual(10, candidates["count"])
        self.assertEqual(0, candidates["successor_recommendations_executed"])
        self.assertTrue(all(row["state"] == "completed_bounded_reversible_view" for row in candidates["rows"]))
        self.assertEqual(30, cleanup["count"])
        self.assertEqual(0, cleanup["successor_recommendations_executed"])
        self.assertFalse(cleanup["deletion_authorized"])
        self.assertTrue(all(row["deletions"] == 0 for row in cleanup["rows"]))

    def test_phase_truth_keeps_route_and_terminal_gate(self) -> None:
        truth = load("truth/x2-phase-truth.json")
        self.assertEqual("Elowen Cairn", truth["authorized_current_owner"])
        self.assertEqual("v661-v6", truth["authorized_current_phase"])
        self.assertIsNone(truth["explicit_successor"]["title"])
        self.assertIsNone(truth["explicit_successor"]["phase"])
        self.assertEqual("UNRESOLVED_REQUIRES_FRESH_TERMINAL_ROUTE_CHECK", truth["explicit_successor"]["state"])
        self.assertIsNone(truth["prospective_cycle_next"]["title"])
        self.assertIsNone(truth["prospective_cycle_next"]["phase"])
        self.assertEqual("not_inferred_or_contacted", truth["prospective_cycle_next"]["state"])
        self.assertEqual("CURRENT_OWNER_ACTIVE_LATER_EDGE_UNRESOLVED_NOT_CONTACTED", truth["route_state"])
        self.assertFalse(truth["message_sent"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertFalse(truth["independent_reproduction"])

    def test_privacy_scan_has_zero_confirmed_hits(self) -> None:
        privacy = load("validation/x2-privacy-scan.json")
        self.assertEqual(5, len(privacy["classes"]))
        self.assertEqual([], privacy["confirmed_hits"])
        self.assertFalse(privacy["privacy_complete"])

    def test_manifest_replays_changed_file_bytes(self) -> None:
        manifest = load("validation/x2-content-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            payload = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(row["bytes"], len(payload), row["path"])
            self.assertEqual(row["sha256"], hashlib.sha256(payload).hexdigest(), row["path"])

    def test_documents_and_static_report_are_bounded(self) -> None:
        cap = load("validation/x2-document-cap.json")
        self.assertTrue(cap["passes"])
        overview = (PHASE / "deliverables/v661-v6-x2-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "reports/accessible-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 900)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("<main id=\"main\">", report)
        self.assertIn("Manual keyboard", report)

    def test_outcome_counter_matches_all_surface_receipts(self) -> None:
        rows = load("evidence/proposal-outcomes.json")["outcomes"]
        observed = Counter(row["observed_outcome"] for row in rows)
        self.assertEqual(d.EXPECTED_DISTRIBUTION, dict(observed))


if __name__ == "__main__":
    unittest.main()
