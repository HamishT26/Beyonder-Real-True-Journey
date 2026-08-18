#!/usr/bin/env python3
"""Exact owner-delta tests for Caelen Ash v663-v1."""

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

from scripts.ghc_family_owner_delta_toolkit import (
    DeltaError,
    caelen_fixture_cases,
    caelen_hardening_payload,
    caelen_mutation_payload,
    hardening_payload_for_profile,
    strict_json_loads,
    validate_cave_accessible_companion,
    validate_cave_atmosphere_sensor,
    validate_cave_callout_state,
    validate_cave_condition_cue,
    validate_cave_equipment_observation,
    validate_cave_handover,
    validate_cave_incident_lineage,
    validate_cave_instrument_lineage,
    validate_cave_location_minimization,
    validate_cave_loop_closure,
    validate_cave_measurement_domain,
    validate_cave_passage_lrud,
    validate_cave_sensitive_feature,
    validate_cave_station_shot_topology,
)


DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]

SOURCE = "ab7af77d45444288f63f88083dbdd117171ef11b"
X1 = "0d33b91288f0d56cb17ab271d4fbfe00956edd66"
PHASE_ROOT = "docs/caelen-ash/v663-v1"
VALIDATORS = {
    function.__name__: function
    for function in (
        validate_cave_station_shot_topology,
        validate_cave_measurement_domain,
        validate_cave_instrument_lineage,
        validate_cave_passage_lrud,
        validate_cave_loop_closure,
        validate_cave_location_minimization,
        validate_cave_sensitive_feature,
        validate_cave_equipment_observation,
        validate_cave_condition_cue,
        validate_cave_atmosphere_sensor,
        validate_cave_callout_state,
        validate_cave_incident_lineage,
        validate_cave_accessible_companion,
        validate_cave_handover,
    )
}
CASES = caelen_fixture_cases()


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
    raw = git("show", f"{X1}:{PHASE_ROOT}/x1/{name}")
    return strict_json_loads(raw, name)


class TestImmutableX1(unittest.TestCase):
    def test_x1_is_direct_child_of_source(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").strip(), SOURCE)

    def test_x1_has_eleven_json_files_only(self) -> None:
        paths = git("ls-tree", "-r", "--name-only", X1, "--", f"{PHASE_ROOT}/x1").splitlines()
        self.assertEqual(len(paths), 11)
        self.assertTrue(all(path.endswith(".json") for path in paths))

    def test_x1_contains_no_x2_path(self) -> None:
        paths = git("diff", "--name-only", SOURCE, X1).splitlines()
        self.assertTrue(paths)
        self.assertTrue(all("/x1/" in f"/{path}/" for path in paths))

    def test_x1_all_strict_json(self) -> None:
        for name in (
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
            "x1-validation-receipt.json",
        ):
            self.assertIsInstance(x1_json(name), dict)

    def test_proposal_counts(self) -> None:
        proposal = x1_json("proposal-freeze.json")
        self.assertEqual(proposal["inherited_frozen_baseline"], 3670)
        self.assertEqual(proposal["new_frozen_total"], 3690)
        self.assertEqual(len(proposal["selected_inherited"]), 20)
        self.assertEqual(len(proposal["new_proposals"]), 20)

    def test_outcome_counts(self) -> None:
        proposal = x1_json("proposal-freeze.json")
        counts = Counter(row["expected_disposition"] for row in proposal["new_proposals"])
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
        self.assertEqual(novelty["reconstructed_row_count"], 3670)
        self.assertEqual(novelty["candidate_count"], 20)
        self.assertEqual(novelty["exact_candidate_collision_count"], 0)

    def test_portfolio_counts(self) -> None:
        packet = x1_json("portfolio-freeze.json")
        actual = {
            "safe_now": len(packet["safe_now"]["owner_execution"])
            + len(packet["safe_now"]["successor_recommendation"]),
            "candidate": len(packet["candidate"]["owner_execution"])
            + len(packet["candidate"]["successor_recommendation"]),
            "approval_gate": len(packet["approval_gates"]["exact"])
            + len(packet["approval_gates"]["blocked"]),
            "skill": len(packet["skills"]["owner_build"])
            + len(packet["skills"]["successor_recommendation"]),
            "runner": len(packet["runners"]["owner_build"])
            + len(packet["runners"]["successor_recommendation"]),
            "clean_fix_refine": len(packet["clean_fix_refine"]["owner_execution"])
            + len(packet["clean_fix_refine"]["successor_recommendation"]),
        }
        self.assertEqual(actual, packet["expected_counts"])
        self.assertEqual(actual, {"safe_now": 50, "candidate": 30, "approval_gate": 15, "skill": 20, "runner": 20, "clean_fix_refine": 60})

    def test_profile_baseline_and_route(self) -> None:
        profile = x1_json("builder-profile.json")
        self.assertEqual(profile["activation_baseline"]["effective_negatives"], 23236)
        self.assertEqual(profile["activation_baseline"]["effective_methods"], 7830)
        self.assertEqual(profile["next_owner"], "Orin Thale")
        self.assertEqual(profile["next_phase"], "v663-v2")
        self.assertEqual(profile["hardening_profile"], "caelen-v663-v1")
        self.assertEqual(profile["runner_callables"], list(VALIDATORS))

    def test_sparse_contract(self) -> None:
        sparse = x1_json("sparse-lane-receipt.json")
        self.assertTrue(sparse["sparse_initialized_before_checkout"])
        self.assertEqual(sparse["initial_materialized_file_count"], 4)
        self.assertEqual(sparse["hard_rotation_threshold"], 2000)
        self.assertEqual(len(sparse["patterns"]), 6)

    def test_startup_failures_preserved(self) -> None:
        flow = x1_json("startup-method-flow.json")
        self.assertEqual(flow["retained_operational_negative_count"], 11)
        self.assertEqual(flow["passing_witness_count"], 11)
        self.assertEqual(len(flow["records"]), 11)
        self.assertEqual(len({row["method_id"] for row in flow["records"]}), 11)

    def test_workflow_refinement_is_bounded(self) -> None:
        receipt = x1_json("workflow-refinement-receipt.json")
        self.assertTrue(receipt["runner_valid"])
        self.assertEqual(receipt["policy_checks"], 20)
        self.assertEqual(receipt["policy_checks_passed"], 20)
        self.assertEqual(receipt["privacy_findings"], 0)
        self.assertFalse(receipt["independent_reproduction"])

    def test_x1_validation_manifest_is_exact(self) -> None:
        receipt = x1_json("x1-validation-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["manifest_count"], 10)
        self.assertFalse(receipt["x2_outcomes_executed"])
        self.assertFalse(receipt["canonical_invoked"])


class TestCaelenFixtureContracts(unittest.TestCase):
    """Dynamic methods below expose one pass and five rejecting subtests per proposal."""


def _positive_test(case: dict) -> object:
    def test(self: TestCaelenFixtureContracts) -> None:
        result = VALIDATORS[case["validator"]](case["positive"])
        self.assertTrue(result["valid"])

    return test


def _negative_test(case: dict) -> object:
    def test(self: TestCaelenFixtureContracts) -> None:
        self.assertEqual(len(case["mutations"]), 5)
        for mutation in case["mutations"]:
            with self.subTest(mutation=mutation["label"]):
                with self.assertRaises(DeltaError):
                    VALIDATORS[case["validator"]](mutation["record"])

    return test


for index, fixture_case in enumerate(CASES, 1):
    setattr(
        TestCaelenFixtureContracts,
        f"test_{index:02d}_positive",
        _positive_test(fixture_case),
    )
    setattr(
        TestCaelenFixtureContracts,
        f"test_{index:02d}_five_rejections",
        _negative_test(fixture_case),
    )


class TestCaelenMutationTruth(unittest.TestCase):
    def test_fixture_family_is_exact(self) -> None:
        self.assertEqual(len(CASES), 14)
        self.assertEqual(len({case["proposal_id"] for case in CASES}), 14)
        self.assertEqual(len({case["fixture_id"] for case in CASES}), 14)
        self.assertEqual({case["validator"] for case in CASES}, set(VALIDATORS))

    def test_mutation_matrix_counts(self) -> None:
        payload = caelen_mutation_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["proposal_count"], 14)
        self.assertEqual(payload["mutations_per_proposal"], 5)
        self.assertEqual(payload["negative_fixture_count"], 70)
        self.assertEqual(payload["rejected_fixture_count"], 70)
        self.assertEqual(payload["positive_fixture_count"], 14)
        self.assertEqual(payload["passing_fixture_count"], 14)
        self.assertEqual(payload["failed_witnesses_erased"], 0)

    def test_mutation_ids_and_per_proposal_counts(self) -> None:
        records = caelen_mutation_payload()["records"]
        self.assertEqual(len({row["mutation_id"] for row in records}), 70)
        self.assertEqual(set(Counter(row["proposal_id"] for row in records).values()), {5})
        self.assertTrue(all(row["rejected"] and row["zero_credit"] for row in records))

    def test_mutation_payload_is_strict_json(self) -> None:
        rendered = json.dumps(caelen_mutation_payload(), ensure_ascii=False, allow_nan=False, sort_keys=True)
        self.assertIsInstance(strict_json_loads(rendered, "Caelen mutation payload"), dict)

    def test_hardening_profile_counts(self) -> None:
        payload = caelen_hardening_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["negative_fixture_count"], 14)
        self.assertEqual(payload["rejected_fixture_count"], 14)
        self.assertEqual(payload["positive_fixture_count"], 14)
        self.assertEqual(payload["full_mutation_matrix_negative_count"], 70)

    def test_hardening_selector_is_exact(self) -> None:
        self.assertEqual(hardening_payload_for_profile("caelen-v663-v1")["profile"], "caelen-v663-v1")
        with self.assertRaises(DeltaError):
            hardening_payload_for_profile("caelen-v663-v1-unknown")

    def test_hardening_boundaries_stay_false(self) -> None:
        payload = caelen_hardening_payload()
        for field in (
            "real_cave_accessed",
            "survey_computed",
            "measurement_claimed",
            "real_location_present",
            "live_sensor_used",
            "safety_assessed",
            "entry_authorized",
            "emergency_dispatched",
            "privacy_complete",
            "accessibility_complete",
            "professional_authority",
            "cultural_authority",
            "maori_authority",
            "exhaustive_security",
        ):
            self.assertFalse(payload[field], field)


if __name__ == "__main__":
    unittest.main(verbosity=2)
