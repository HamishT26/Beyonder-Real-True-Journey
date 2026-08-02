#!/usr/bin/env python3
"""Scoped x2 evidence checks for Ilyra Fen v659-v1."""

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

import ghc_family_v659_v1_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class IlyraV659V1X2Tests(unittest.TestCase):
    def test_x1_to_x2_gate_is_exact(self) -> None:
        gate = load("evidence/x1-to-x2-gate.json")
        self.assertEqual(d.SOURCE_FINAL, gate["source_final"])
        self.assertEqual(d.X1_FREEZE, gate["x1_freeze"])
        self.assertEqual(d.SOURCE_FINAL, gate["x1_parent"])
        self.assertEqual(1, gate["x1_parent_count"])
        self.assertEqual(1, gate["x1_commit_count_from_source"])
        self.assertEqual(0, gate["x1_merge_count_from_source"])
        self.assertTrue(gate["local_upstream_tracking_equal"])
        self.assertTrue(gate["x2_started_after_remote_equal_x1"])

    def test_forty_outcomes_match_the_frozen_distribution(self) -> None:
        payload = load("evidence/proposal-outcomes.json")
        self.assertEqual(40, payload["proposal_count"])
        self.assertEqual(20, payload["selected_inherited_count"])
        self.assertEqual(20, payload["new_unique_count"])
        counts = Counter(row["observed_outcome"] for row in payload["outcomes"])
        self.assertEqual(d.EXPECTED_DISTRIBUTION, dict(counts))
        self.assertEqual(d.ALLOWED_OUTCOMES, set(counts))
        self.assertTrue(all(row["expected_outcome"] == row["observed_outcome"] for row in payload["outcomes"]))

    def test_selected_revalidations_do_not_extend_the_chain(self) -> None:
        rows = load("evidence/proposal-outcomes.json")["outcomes"][:20]
        self.assertTrue(all(row["origin_class"] == "selected_inherited_revalidation" for row in rows))
        for row in rows:
            receipt = load(f"surfaces/{row['slug']}/bounded-receipt.json")
            self.assertFalse(receipt["append_to_frozen_chain"])
            self.assertTrue(receipt["source_proposal_id"])
            self.assertTrue(receipt["same_owner_only"])
            self.assertFalse(receipt["independent_reproduction"])

    def test_new_surfaces_remain_synthetic_and_append_only(self) -> None:
        rows = load("evidence/proposal-outcomes.json")["outcomes"][20:]
        self.assertTrue(all(row["origin_class"] == "new_unique_execution" for row in rows))
        for row in rows:
            contract = load(f"surfaces/{row['slug']}/contract.json")
            receipt = load(f"surfaces/{row['slug']}/bounded-receipt.json")
            self.assertTrue(receipt["append_to_frozen_chain"])
            self.assertTrue(contract["fixture"]["synthetic_only"])
            self.assertFalse(contract["fixture"]["real_people_observatories_instruments_observations_measurements_identifiers_or_authority_cases_used"])
            self.assertFalse(contract["fixture"]["authority_action_executed"])
            self.assertFalse(contract["fixture"]["operation_release_or_suitability_decision"])

    def test_every_surface_passes_one_valid_and_rejects_five_mutations(self) -> None:
        outcomes = load("evidence/proposal-outcomes.json")["outcomes"]
        for row in outcomes:
            receipt = load(f"surfaces/{row['slug']}/bounded-receipt.json")
            mutations = load(f"surfaces/{row['slug']}/mutation-results.json")
            self.assertTrue(receipt["valid_fixture_passed"], row["proposal_id"])
            self.assertEqual(5, receipt["rejected_mutation_count"], row["proposal_id"])
            self.assertTrue(receipt["all_mutations_rejected"], row["proposal_id"])
            self.assertEqual(5, mutations["mutation_count"], row["proposal_id"])
            self.assertTrue(all(item["rejected"] and item["retained"] and item["credit"] == 0 for item in mutations["results"]))

    def test_mutation_register_preserves_two_hundred_negatives(self) -> None:
        register = load("evidence/mutation-register.json")
        self.assertEqual(200, register["mutation_count"])
        self.assertEqual(200, register["rejected_count"])
        self.assertTrue(register["all_retained"])
        self.assertEqual(200, len({row["mutation_id"] for row in register["mutations"]}))

    def test_x2_method_flow_pairs_every_failure_and_recovery(self) -> None:
        flow = load("method-flow/method-flow-state-x2.json")
        expected = len(d.X2_FAILURES) + 200
        self.assertEqual(expected, flow["counts"]["methods"])
        self.assertEqual(expected * 2, flow["counts"]["witnesses"])
        self.assertEqual(expected * 2, flow["counts"]["state_events"])
        self.assertEqual(Counter({"fail": expected, "pass": expected}), Counter(row["result"] for row in flow["witnesses"]))
        self.assertEqual(d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES) + expected, flow["cumulative_counts"]["effective_methods"])

    def test_negative_arithmetic_is_additive(self) -> None:
        negatives = load("truth/retained-negative-register-x2.json")
        expected = d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES) + len(d.X2_FAILURES) + 200
        self.assertEqual(d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES), negatives["x1_effective_negatives"])
        self.assertEqual(len(d.X2_FAILURES), len(negatives["x2_operational_negatives"]))
        self.assertEqual(200, negatives["x2_mutation_count"])
        self.assertEqual(expected, negatives["effective_negatives"])
        self.assertTrue(negatives["all_failures_retained"])

    def test_latest_file_scan_is_exactly_bounded_and_non_exhaustive(self) -> None:
        scan = load("tooling/runner-smoke/ghc_family_observation_provenance_scan.json")
        self.assertEqual(d.X1_FREEZE, scan["head"])
        self.assertEqual(5000, scan["selected_file_count"])
        self.assertGreaterEqual(scan["tracked_path_count"], 5000)
        self.assertEqual(64, len(scan["ordered_path_sha256"]))
        self.assertEqual(0, scan["missing_path_count"])
        self.assertEqual(0, scan["truncated_file_count"])
        self.assertEqual(0, scan["confirmed_high_risk_count"])
        self.assertFalse(scan["matched_values_published"])
        self.assertFalse(scan["privacy_complete"])
        self.assertFalse(scan["security_complete"])

    def test_ten_skills_are_creator_validated_and_bound(self) -> None:
        payload = load("tooling/skill-validation.json")
        self.assertEqual(10, payload["skill_count"])
        self.assertEqual(10, payload["valid_skill_count"])
        self.assertTrue(payload["all_valid"])
        self.assertFalse(payload["subagent_forward_test_used"])
        for row in payload["skills"]:
            self.assertTrue(row["valid"])
            self.assertTrue(all(row["checks"].values()))
            skill = (PHASE / "skills" / row["skill_name"] / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", skill)

    def test_ten_runners_are_built_tested_and_used(self) -> None:
        payload = load("tooling/runner-aggregate.json")
        self.assertEqual(10, payload["runner_count"])
        self.assertEqual(10, payload["valid_runner_count"])
        self.assertTrue(payload["all_built_tested_used"])
        self.assertTrue(all(row["valid"] and row["used"] for row in payload["runners"]))

    def test_global_skill_installation_is_additive_and_hash_equal(self) -> None:
        payload = load("tooling/global-skill-installation.json")
        self.assertEqual(10, payload["skill_count"])
        self.assertEqual(10, payload["valid_skill_count"])
        self.assertTrue(payload["all_valid"])
        self.assertFalse(payload["existing_skill_replaced"])
        self.assertFalse(payload["plugin_cache_mutated"])
        self.assertTrue(all(row["valid"] and row["hash_mismatch_count"] == 0 for row in payload["rows"]))

    def test_x2_family_index_reflection_and_toolbox_are_current(self) -> None:
        index = load("tooling/family-index-x2/ghc-family-index.json")
        reflection = load("tooling/reflection-remaster-x2/reflection-remaster-inventory.json")
        toolbox = load("tooling/meta-tool-box-x2/validation.json")
        skills = load("tooling/meta-tool-box-x2/skill-query.json")
        runners = load("tooling/meta-tool-box-x2/runner-query.json")
        collisions = load("tooling/meta-tool-box-x2/collisions.json")
        self.assertEqual("v659-v1-x2", index["phase"])
        self.assertGreaterEqual(index["counts"]["skills"]["family_current"], 129)
        self.assertGreaterEqual(index["counts"]["scripts"]["family_current"], 922)
        self.assertEqual(10, reflection["scoped_count"])
        self.assertTrue(toolbox["valid"])
        self.assertEqual(20, toolbox["card_count"])
        self.assertEqual(10, skills["result_count"])
        self.assertEqual(10, runners["result_count"])
        self.assertEqual(0, collisions["finding_count"])

    def test_family_method_flow_validator_accepts_x2_ledger(self) -> None:
        receipt = load("tooling/method-flow/validation-x2.json")
        expected = len(d.X2_FAILURES) + 200
        self.assertTrue(receipt["valid"])
        self.assertEqual(0, receipt["issue_count"])
        self.assertEqual(expected, receipt["method_count"])
        self.assertEqual(expected * 2, receipt["witness_count"])

    def test_ten_candidate_prototypes_are_completed_without_external_state(self) -> None:
        payload = load("tooling/candidate-prototype-aggregate.json")
        self.assertEqual(10, payload["count"])
        self.assertTrue(payload["all_completed"])
        for row in payload["rows"]:
            self.assertEqual("completed_bounded_synthetic_prototype", row["state"])
            self.assertFalse(row["external_state_changed"])
            self.assertFalse(row["authority_action_executed"])

    def test_thirty_cleanup_reviews_are_additive_and_non_destructive(self) -> None:
        payload = load("cleanup/cleanup-aggregate.json")
        self.assertEqual(30, payload["count"])
        self.assertEqual(30, payload["completed_count"])
        self.assertEqual(0, payload["deletion_count"])
        for row in payload["rows"]:
            self.assertFalse(row["deletion_performed"])
            self.assertFalse(row["sibling_or_shared_lane_mutated"])
            self.assertFalse(row["external_platform_mutated"])

    def test_truth_keeps_open_gap_exact_gate_and_not_ready(self) -> None:
        truth = load("truth/x2-phase-truth.json")
        self.assertEqual(2930, truth["effective_frozen"])
        self.assertEqual(122, truth["effective_open_gaps"])
        self.assertEqual(121, truth["effective_exact_gates"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertTrue(truth["same_owner_only"])
        self.assertFalse(truth["independent_reproduction"])

    def test_route_remains_terminally_gated_and_unsent(self) -> None:
        truth = load("truth/x2-phase-truth.json")
        route = load("orchestration/route-state-x1.json")
        self.assertEqual("PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", truth["route_state"])
        self.assertEqual("Auren Lark", truth["next_exact_title"])
        self.assertEqual("v659-v2", truth["next_phase"])
        self.assertEqual("Sable Rook", truth["recipient_next_exact_title"])
        self.assertEqual("v659-v3", truth["recipient_next_phase"])
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["message_sent"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])

    def test_global_roster_and_auth_receipts_validate_x2_state(self) -> None:
        roster = load("tooling/governance/roster-validation-x2.json")
        auth = load("tooling/governance/auth-validation-x2.json")
        self.assertTrue(roster["valid"])
        self.assertTrue(auth["valid"])
        self.assertEqual(
            "ghc-family-roster-v659-v1-ilyra-activation-acknowledged",
            roster["state_id"],
        )
        self.assertEqual(
            "ghc-family-v659-v1-ilyra-activation-acknowledged",
            auth["state_id"],
        )
        self.assertEqual([], roster["issues"])
        self.assertEqual([], auth["errors"])
        self.assertEqual(15, auth["endpoint_counts"]["main_task"])
        self.assertEqual(1, auth["endpoint_counts"]["collaboration_subagent"])

    def test_owner_packet_privacy_scan_has_zero_confirmed_hits(self) -> None:
        privacy = load("validation/x2-owner-privacy-scan.json")
        self.assertEqual(5, len(privacy["classes"]))
        self.assertEqual([], privacy["confirmed_hits"])
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["privacy_complete"])
        self.assertFalse(privacy["security_complete"])

    def test_x2_manifest_replays_declared_git_clean_bytes(self) -> None:
        manifest = load("validation/x2-content-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual("text bytes after CRLF-to-LF Git-clean normalization", manifest["hash_domain"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(row["bytes"], len(path.read_bytes().replace(b"\r\n", b"\n")), row["path"])
            self.assertEqual(row["sha256"], sha256(path), row["path"])

    def test_document_cap_and_x2_overview_are_bounded(self) -> None:
        cap = load("validation/x2-document-cap.json")
        overview = (PHASE / "deliverables/v659-v1-x2-overview.md").read_text(encoding="utf-8")
        self.assertTrue(cap["passes"])
        self.assertLessEqual(cap["total_words"], cap["cap"])
        self.assertGreaterEqual(len(overview.split()), 1000)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("Ilyra Fen", overview)
        self.assertIn("Auren Lark", overview)


if __name__ == "__main__":
    unittest.main()
