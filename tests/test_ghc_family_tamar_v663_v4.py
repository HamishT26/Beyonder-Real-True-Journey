#!/usr/bin/env python3
"""Exact owner-delta tests for Tamar Vey v663-v4."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.ghc_family_owner_delta_toolkit as toolkit
from scripts.ghc_family_owner_delta_toolkit import (
    DeltaError,
    hardening_payload_for_profile,
    strict_json_loads,
    tamar_fixture_cases,
    tamar_hardening_payload,
    tamar_mutation_payload,
    validate_kite_accessibility_companion,
    validate_kite_component_topology,
    validate_kite_correction_lineage,
    validate_kite_custody_placeholder,
    validate_kite_external_cues,
    validate_kite_geometry_envelope,
    validate_kite_handover,
    validate_kite_material_cues,
    validate_kite_material_lots,
    validate_kite_privacy_notice,
    validate_kite_rights_hold,
    validate_kite_tool_reservation,
    validate_kite_workshop_packet,
    validate_kite_workshop_plan,
)

DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]
SOURCE = "fd51e672b4852867eb8733614580e7bd28b18351"
X1 = "2570467fa6e633ab7a6f53a70f552b738d1575b9"
PHASE_ROOT = "docs/tamar-vey/v663-v4"
VALIDATORS = {
    function.__name__: function
    for function in (
        validate_kite_workshop_packet,
        validate_kite_component_topology,
        validate_kite_material_lots,
        validate_kite_workshop_plan,
        validate_kite_geometry_envelope,
        validate_kite_material_cues,
        validate_kite_tool_reservation,
        validate_kite_privacy_notice,
        validate_kite_accessibility_companion,
        validate_kite_rights_hold,
        validate_kite_external_cues,
        validate_kite_custody_placeholder,
        validate_kite_correction_lineage,
        validate_kite_handover,
    )
}
CASES = tamar_fixture_cases()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def x1_json(name: str) -> dict:
    return strict_json_loads(
        git("show", f"{X1}:{PHASE_ROOT}/x1/{name}"),
        name,
    )


class TestImmutableX1(unittest.TestCase):
    def test_x1_is_direct_child_of_source(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").strip(), SOURCE)

    def test_x1_has_twelve_json_files_only(self) -> None:
        paths = git("ls-tree", "-r", "--name-only", X1, "--", f"{PHASE_ROOT}/x1").splitlines()
        self.assertEqual(len(paths), 12)
        self.assertTrue(all(path.endswith(".json") for path in paths))

    def test_x1_contains_no_x2_path(self) -> None:
        paths = git("diff", "--name-only", SOURCE, X1).splitlines()
        self.assertTrue(paths)
        self.assertTrue(all(path.startswith(f"{PHASE_ROOT}/x1/") for path in paths))

    def test_x1_all_strict_json(self) -> None:
        names = (
            "builder-profile.json",
            "novelty-audit.json",
            "phase-charter.json",
            "portfolio-freeze.json",
            "proposal-freeze.json",
            "source-verification.json",
            "sparse-lane-receipt.json",
            "startup-method-flow.json",
            "workflow-plan.json",
            "workflow-refinement-receipt.json",
            "x1-staged-review.json",
            "x1-validation-receipt.json",
        )
        for name in names:
            self.assertIsInstance(x1_json(name), dict)

    def test_x1_staged_manifest_is_exact(self) -> None:
        review = x1_json("x1-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["manifest_entry_count"], 11)
        self.assertEqual(len(review["entries"]), 11)
        self.assertEqual(len(review["lifecycle_self_exclusions"]), 1)
        self.assertEqual(review["expected_final_staged_path_count"], 12)

    def test_proposal_counts(self) -> None:
        proposal = x1_json("proposal-freeze.json")
        self.assertEqual(proposal["inherited_frozen_baseline"], 3730)
        self.assertEqual(proposal["new_frozen_total"], 3750)
        self.assertEqual(len(proposal["selected_inherited"]), 20)
        self.assertEqual(len(proposal["new_proposals"]), 20)

    def test_outcome_counts(self) -> None:
        counts = Counter(
            row["expected_disposition"]
            for row in x1_json("proposal-freeze.json")["new_proposals"]
        )
        self.assertEqual(
            counts,
            Counter(completed=14, represented=4, open_gap=1, exact_gate=1),
        )

    def test_core_proposal_fields(self) -> None:
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure",
            "approval_class",
            "execution_lane",
            "primary_source_needs",
            "concrete_artifacts",
            "acceptance_or_falsifier",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in x1_json("proposal-freeze.json")["new_proposals"]:
            self.assertEqual(set(row), required)
            self.assertTrue(all(row[field] for field in required))

    def test_novelty_corpus_and_collisions(self) -> None:
        novelty = x1_json("novelty-audit.json")
        self.assertTrue(novelty["valid"])
        self.assertEqual(novelty["reconstructed_row_count"], 3730)
        self.assertEqual(novelty["candidate_count"], 20)
        self.assertEqual(novelty["exact_candidate_collision_count"], 0)

    def test_portfolio_counts(self) -> None:
        packet = x1_json("portfolio-freeze.json")
        actual = {
            "safe_now": len(packet["safe_now"]["owner_execution"]) + len(packet["safe_now"]["successor_recommendation"]),
            "candidate": len(packet["candidate"]["owner_execution"]) + len(packet["candidate"]["successor_recommendation"]),
            "approval_gate": len(packet["approval_gates"]["exact"]) + len(packet["approval_gates"]["blocked"]),
            "skill": len(packet["skills"]["owner_build"]) + len(packet["skills"]["successor_recommendation"]),
            "runner": len(packet["runners"]["owner_build"]) + len(packet["runners"]["successor_recommendation"]),
            "clean_fix_refine": len(packet["clean_fix_refine"]["owner_execution"]) + len(packet["clean_fix_refine"]["successor_recommendation"]),
        }
        self.assertEqual(actual, packet["expected_counts"])
        self.assertEqual(
            actual,
            {"safe_now": 50, "candidate": 30, "approval_gate": 15, "skill": 20, "runner": 20, "clean_fix_refine": 60},
        )

    def test_profile_baseline_route_and_hardening(self) -> None:
        profile = x1_json("builder-profile.json")
        self.assertEqual(profile["activation_baseline"]["effective_negatives"], 23513)
        self.assertEqual(profile["activation_baseline"]["effective_methods"], 8107)
        self.assertEqual(profile["next_owner"], "Elowen Cairn")
        self.assertEqual(profile["next_phase"], "v663-v5")
        self.assertEqual(profile["hardening_profile"], "tamar-v663-v4")
        self.assertEqual(profile["runner_callables"], list(VALIDATORS))
        self.assertEqual(profile["planned_owner_delta"]["startup_operational_negatives"], 14)
        self.assertEqual(profile["planned_owner_delta"]["synthetic_rejected_mutations"], 70)

    def test_source_status_vocabulary(self) -> None:
        statuses = {row["status"] for row in x1_json("builder-profile.json")["source_records"]}
        self.assertEqual(statuses, {"current", "stable", "draft", "watch"})

    def test_sparse_contract(self) -> None:
        sparse = x1_json("sparse-lane-receipt.json")
        self.assertTrue(sparse["sparse_configured_before_materialization"])
        self.assertEqual(sparse["initial_materialized_files"], 4)
        self.assertEqual(sparse["pattern_count"], 6)
        self.assertEqual(len(sparse["patterns"]), 6)

    def test_startup_failures_preserved(self) -> None:
        flow = x1_json("startup-method-flow.json")
        self.assertEqual(flow["method_count"], 14)
        self.assertEqual(flow["retained_failed_witness_count"], 14)
        self.assertEqual(flow["bounded_passing_witness_count"], 14)
        self.assertEqual(flow["pending_witness_count"], 0)
        self.assertEqual(len(flow["records"]), 14)
        self.assertEqual(len({row["method_id"] for row in flow["records"]}), 14)

    def test_workflow_refinement_is_bounded(self) -> None:
        receipt = x1_json("workflow-refinement-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["retained_failures"], 14)
        self.assertEqual(receipt["retained_failures_rewritten_as_passes"], 0)
        self.assertFalse(receipt["same_owner_independent_reproduction"])
        self.assertFalse(receipt["canonical_replay_permitted"])

    def test_x1_validation_is_planning_only(self) -> None:
        receipt = x1_json("x1-validation-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["checks"]["lifecycle"]["x2_directory_exists"])
        self.assertFalse(receipt["checks"]["lifecycle"]["x2_implementation_or_outcome_present"])
        self.assertTrue(receipt["checks"]["lifecycle"]["x1_only"])


class TestTamarFixtureContracts(unittest.TestCase):
    """Dynamic methods expose one pass and five rejecting subtests per completion."""


def _positive_test(case: dict) -> object:
    def test(self: TestTamarFixtureContracts) -> None:
        self.assertTrue(VALIDATORS[case["validator"]](case["positive"])["valid"])
    return test


def _negative_test(case: dict) -> object:
    def test(self: TestTamarFixtureContracts) -> None:
        self.assertEqual(len(case["mutations"]), 5)
        for mutation in case["mutations"]:
            with self.subTest(mutation=mutation["label"]):
                with self.assertRaises(DeltaError):
                    VALIDATORS[case["validator"]](mutation["record"])
    return test


for index, fixture_case in enumerate(CASES, 1):
    setattr(TestTamarFixtureContracts, f"test_{index:02d}_positive", _positive_test(fixture_case))
    setattr(TestTamarFixtureContracts, f"test_{index:02d}_five_rejections", _negative_test(fixture_case))


class TestTamarMutationTruth(unittest.TestCase):
    def test_fixture_family_is_exact(self) -> None:
        self.assertEqual(len(CASES), 14)
        self.assertEqual(len({case["proposal_id"] for case in CASES}), 14)
        self.assertEqual(len({case["fixture_id"] for case in CASES}), 14)
        self.assertEqual({case["validator"] for case in CASES}, set(VALIDATORS))

    def test_mutation_matrix_counts(self) -> None:
        payload = tamar_mutation_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["proposal_count"], 14)
        self.assertEqual(payload["mutations_per_proposal"], 5)
        self.assertEqual(payload["negative_fixture_count"], 70)
        self.assertEqual(payload["rejected_fixture_count"], 70)
        self.assertEqual(payload["positive_fixture_count"], 14)
        self.assertEqual(payload["passing_fixture_count"], 14)
        self.assertEqual(payload["failed_witnesses_erased"], 0)

    def test_mutation_ids_and_per_proposal_counts(self) -> None:
        records = tamar_mutation_payload()["records"]
        self.assertEqual(len({row["mutation_id"] for row in records}), 70)
        self.assertEqual(len({row["fixture_id"] for row in records}), 70)
        self.assertEqual(set(Counter(row["proposal_id"] for row in records).values()), {5})
        self.assertTrue(all(row["rejected"] and row["zero_credit"] for row in records))

    def test_mutation_payload_is_strict_json(self) -> None:
        rendered = json.dumps(tamar_mutation_payload(), ensure_ascii=False, allow_nan=False, sort_keys=True)
        self.assertIsInstance(strict_json_loads(rendered, "Tamar mutation payload"), dict)

    def test_hardening_profile_counts(self) -> None:
        payload = tamar_hardening_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["negative_fixture_count"], 70)
        self.assertEqual(payload["rejected_fixture_count"], 70)
        self.assertEqual(payload["positive_fixture_count"], 14)
        self.assertEqual(payload["passing_fixture_count"], 14)
        self.assertEqual(payload["full_mutation_matrix_negative_count"], 70)

    def test_hardening_selector_is_exact(self) -> None:
        self.assertEqual(hardening_payload_for_profile("tamar-v663-v4")["profile"], "tamar-v663-v4")
        with self.assertRaises(DeltaError):
            hardening_payload_for_profile("tamar-v663-v4-unknown")

    def test_hardening_boundaries_stay_false(self) -> None:
        payload = tamar_hardening_payload()
        for field in (
            "real_person_present", "real_workshop_present", "real_kite_present",
            "real_material_present", "real_tool_present", "real_location_present",
            "real_measurement_present", "build_authorized", "flight_authorized",
            "airspace_cleared", "tool_use_released", "privacy_complete",
            "accessibility_complete", "professional_authority", "legal_authority",
            "cultural_authority", "maori_authority", "exhaustive_security",
        ):
            self.assertFalse(payload[field], field)


class TestGeneratedLocalTools(unittest.TestCase):
    def test_all_materialized_phase_json_is_strict(self) -> None:
        paths = sorted((ROOT / PHASE_ROOT).rglob("*.json"))
        self.assertGreaterEqual(len(paths), 50)
        for path in paths:
            self.assertIsInstance(strict_json_loads(path.read_text(encoding="utf-8"), path.name), dict)

    def test_ten_phase_local_skills_are_complete_and_smoke_bound(self) -> None:
        skill_root = ROOT / PHASE_ROOT / "skills"
        skill_dirs = sorted(path for path in skill_root.iterdir() if path.is_dir())
        self.assertEqual(len(skill_dirs), 10)
        for root in skill_dirs:
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            smoke = strict_json_loads((root / "smoke.json").read_text(encoding="utf-8"), root.name)
            normalized = " ".join(text.split())
            self.assertTrue(text.startswith("---\nname: ghc-family-tamar-vey-"))
            self.assertIn("hardening --profile tamar-v663-v4", normalized)
            self.assertEqual(smoke["name"], root.name)
            self.assertFalse(smoke["installed_globally"])
            self.assertTrue(smoke["valid"])

    def test_ten_family_runner_contracts_invoke_declared_callables(self) -> None:
        runner_root = ROOT / PHASE_ROOT / "runners"
        paths = sorted(runner_root.glob("*.json"))
        self.assertEqual(len(paths), 10)
        case_by_validator = {case["validator"]: case for case in CASES}
        for path in paths:
            contract = strict_json_loads(path.read_text(encoding="utf-8"), path.name)
            callable_name = contract["callable"]
            callback = getattr(toolkit, callable_name)
            if callable_name == "tamar_hardening_payload":
                result = callback()
                self.assertEqual(result["negative_fixture_count"], 70)
            else:
                result = callback(case_by_validator[callable_name]["positive"])
            self.assertTrue(result["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
