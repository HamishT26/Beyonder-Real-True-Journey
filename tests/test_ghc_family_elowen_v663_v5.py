#!/usr/bin/env python3
"""Exact owner-delta tests for Elowen Cairn v663-v5."""

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
    elowen_fixture_cases,
    elowen_hardening_payload,
    elowen_mutation_payload,
    hardening_payload_for_profile,
    strict_json_loads,
    validate_print_accessibility_companion,
    validate_print_component_topology,
    validate_print_correction_lineage,
    validate_print_custody_placeholder,
    validate_print_edition_dependencies,
    validate_print_equipment_reservations,
    validate_print_external_cues,
    validate_print_handover,
    validate_print_material_cues,
    validate_print_material_lots,
    validate_print_privacy_notice,
    validate_print_rights_hold,
    validate_print_si_placeholders,
    validate_print_work_packet,
)

SOURCE = "c2def7190bac0b8a7c2a1e0453bd12e4c1167925"
X1 = "0465dc27bf765e1bbd6d40c985999fef4bf732e8"
PHASE_ROOT = "docs/elowen-cairn/v663-v5"
DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]
VALIDATORS = {
    function.__name__: function
    for function in (
        validate_print_work_packet,
        validate_print_component_topology,
        validate_print_material_lots,
        validate_print_edition_dependencies,
        validate_print_si_placeholders,
        validate_print_material_cues,
        validate_print_equipment_reservations,
        validate_print_privacy_notice,
        validate_print_accessibility_companion,
        validate_print_rights_hold,
        validate_print_external_cues,
        validate_print_custody_placeholder,
        validate_print_correction_lineage,
        validate_print_handover,
    )
}
CASES = elowen_fixture_cases()


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
    return strict_json_loads(git("show", f"{X1}:{PHASE_ROOT}/x1/{name}"), name)


class TestImmutableX1(unittest.TestCase):
    def test_direct_child(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").strip(), SOURCE)

    def test_thirteen_json_files_only(self) -> None:
        paths = git("ls-tree", "-r", "--name-only", X1, "--", f"{PHASE_ROOT}/x1").splitlines()
        self.assertEqual(len(paths), 13)
        self.assertTrue(all(path.endswith(".json") for path in paths))

    def test_no_x2_path(self) -> None:
        paths = git("diff", "--name-only", SOURCE, X1).splitlines()
        self.assertTrue(paths)
        self.assertTrue(all(path.startswith(f"{PHASE_ROOT}/x1/") for path in paths))

    def test_all_strict_json(self) -> None:
        names = (
            "builder-profile.json", "novelty-audit.json", "phase-charter.json",
            "portfolio-freeze.json", "proposal-freeze.json", "source-verification.json",
            "sparse-lane-receipt.json", "startup-method-flow.json",
            "workflow-plan-request.json", "workflow-plan.json",
            "workflow-refinement-receipt.json", "x1-staged-review.json",
            "x1-validation-receipt.json",
        )
        for name in names:
            self.assertIsInstance(x1_json(name), dict)

    def test_staged_manifest(self) -> None:
        review = x1_json("x1-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["manifest_entry_count"], 12)
        self.assertEqual(len(review["entries"]), 12)
        self.assertEqual(review["expected_final_staged_path_count"], 13)

    def test_proposal_counts(self) -> None:
        packet = x1_json("proposal-freeze.json")
        self.assertEqual(packet["inherited_frozen_baseline"], 3750)
        self.assertEqual(packet["new_frozen_total"], 3770)
        self.assertEqual(len(packet["selected_inherited"]), 20)
        self.assertEqual(len(packet["new_proposals"]), 20)

    def test_outcome_counts(self) -> None:
        counts = Counter(
            row["expected_disposition"]
            for row in x1_json("proposal-freeze.json")["new_proposals"]
        )
        self.assertEqual(counts, Counter(completed=14, represented=4, open_gap=1, exact_gate=1))

    def test_proposal_fields(self) -> None:
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure",
            "approval_class", "execution_lane", "primary_source_needs",
            "concrete_artifacts", "acceptance_or_falsifier",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in x1_json("proposal-freeze.json")["new_proposals"]:
            self.assertEqual(set(row), required)
            self.assertTrue(all(row[field] for field in required))

    def test_novelty(self) -> None:
        novelty = x1_json("novelty-audit.json")
        self.assertEqual(novelty["inherited_rows_examined"], 3750)
        self.assertEqual(novelty["candidate_rows"], 20)
        self.assertEqual(novelty["exact_normalized_collisions"], 0)

    def test_portfolios(self) -> None:
        packet = x1_json("portfolio-freeze.json")
        actual = {
            "safe_now_owner": len(packet["safe_now"]["owner_execution"]),
            "safe_now_successor": len(packet["safe_now"]["successor_recommendation"]),
            "candidate_owner": len(packet["candidate"]["owner_execution"]),
            "candidate_successor": len(packet["candidate"]["successor_recommendation"]),
            "exact": len(packet["approval_gates"]["exact"]),
            "blocked": len(packet["approval_gates"]["blocked"]),
            "skills_owner": len(packet["skills"]["owner_build"]),
            "skills_successor": len(packet["skills"]["successor_recommendation"]),
            "runners_owner": len(packet["runners"]["owner_build"]),
            "runners_successor": len(packet["runners"]["successor_recommendation"]),
            "clean_fix_refine_owner": len(packet["clean_fix_refine"]["owner_execution"]),
            "clean_fix_refine_successor": len(packet["clean_fix_refine"]["successor_recommendation"]),
        }
        self.assertEqual(actual, packet["expected_counts"])
        self.assertEqual((actual["safe_now_owner"], actual["safe_now_successor"]), (30, 20))
        self.assertEqual((actual["candidate_owner"], actual["candidate_successor"]), (15, 15))
        self.assertEqual((actual["exact"], actual["blocked"]), (10, 5))
        self.assertEqual((actual["skills_owner"], actual["skills_successor"]), (10, 10))
        self.assertEqual((actual["runners_owner"], actual["runners_successor"]), (10, 10))
        self.assertEqual(
            (actual["clean_fix_refine_owner"], actual["clean_fix_refine_successor"]),
            (30, 30),
        )

    def test_profile(self) -> None:
        profile = x1_json("builder-profile.json")
        self.assertEqual(profile["activation_baseline"]["effective_negatives"], 23620)
        self.assertEqual(profile["activation_baseline"]["effective_methods"], 8214)
        self.assertEqual((profile["next_owner"], profile["next_phase"]), ("Sylven Arc", "v663-v6"))
        self.assertEqual(profile["hardening_profile"], "elowen-v663-v5")
        self.assertEqual(profile["planned_owner_delta"]["startup_operational_negatives"], 17)
        self.assertEqual(profile["planned_owner_delta"]["synthetic_rejected_mutations"], 70)

    def test_source_status(self) -> None:
        statuses = {row["status"] for row in x1_json("builder-profile.json")["source_records"]}
        self.assertEqual(statuses, {"current", "stable", "watch"})

    def test_sparse(self) -> None:
        receipt = x1_json("sparse-lane-receipt.json")
        self.assertTrue(receipt["clean_after_materialization"])
        self.assertEqual(receipt["initial_materialized_files"], 4)
        self.assertEqual(len(receipt["sparse_patterns"]), 6)

    def test_startup_failures(self) -> None:
        flow = x1_json("startup-method-flow.json")
        self.assertEqual(
            (flow["method_count"], flow["retained_failed_witness_count"],
             flow["bounded_passing_witness_count"], flow["pending_witness_count"]),
            (17, 17, 17, 0),
        )
        self.assertEqual(len({row["method_id"] for row in flow["records"]}), 17)

    def test_workflow_refinement(self) -> None:
        receipt = x1_json("workflow-refinement-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual((receipt["issues"], receipt["policy_checks"], receipt["policy_checks_passed"]), (0, 20, 20))
        self.assertFalse(receipt["confirmation_required"])

    def test_planning_only_validation(self) -> None:
        receipt = x1_json("x1-validation-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["checks"]["lifecycle"]["x2_directory_exists"])
        self.assertFalse(receipt["checks"]["lifecycle"]["x2_implementation_or_outcome_present"])
        self.assertTrue(receipt["checks"]["lifecycle"]["x1_only"])


class TestElowenFixtureContracts(unittest.TestCase):
    """One pass and five rejecting subtests per completed proposal."""


def _positive_test(case: dict) -> object:
    def test(self: TestElowenFixtureContracts) -> None:
        self.assertTrue(VALIDATORS[case["validator"]](case["positive"])["valid"])
    return test


def _negative_test(case: dict) -> object:
    def test(self: TestElowenFixtureContracts) -> None:
        self.assertEqual(len(case["mutations"]), 5)
        for mutation in case["mutations"]:
            with self.subTest(mutation=mutation["label"]):
                with self.assertRaises(DeltaError):
                    VALIDATORS[case["validator"]](mutation["record"])
    return test


for index, fixture_case in enumerate(CASES, 1):
    setattr(TestElowenFixtureContracts, f"test_{index:02d}_positive", _positive_test(fixture_case))
    setattr(TestElowenFixtureContracts, f"test_{index:02d}_five_rejections", _negative_test(fixture_case))


class TestElowenMutationTruth(unittest.TestCase):
    def test_fixture_family(self) -> None:
        self.assertEqual(len(CASES), 14)
        self.assertEqual(len({case["proposal_id"] for case in CASES}), 14)
        self.assertEqual({case["validator"] for case in CASES}, set(VALIDATORS))

    def test_matrix_counts(self) -> None:
        payload = elowen_mutation_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(
            (payload["proposal_count"], payload["mutations_per_proposal"],
             payload["negative_fixture_count"], payload["rejected_fixture_count"],
             payload["positive_fixture_count"], payload["passing_fixture_count"]),
            (14, 5, 70, 70, 14, 14),
        )
        self.assertEqual(payload["failed_witnesses_erased"], 0)

    def test_mutation_ids(self) -> None:
        records = elowen_mutation_payload()["records"]
        self.assertEqual(len({row["mutation_id"] for row in records}), 70)
        self.assertEqual(len({row["fixture_id"] for row in records}), 70)
        self.assertEqual(set(Counter(row["proposal_id"] for row in records).values()), {5})
        self.assertTrue(all(row["rejected"] and row["zero_credit"] for row in records))

    def test_strict_json(self) -> None:
        rendered = json.dumps(elowen_mutation_payload(), ensure_ascii=False, allow_nan=False, sort_keys=True)
        self.assertIsInstance(strict_json_loads(rendered, "Elowen mutation payload"), dict)

    def test_hardening_counts(self) -> None:
        payload = elowen_hardening_payload()
        self.assertTrue(payload["valid"])
        self.assertEqual(
            (payload["negative_fixture_count"], payload["rejected_fixture_count"],
             payload["positive_fixture_count"], payload["passing_fixture_count"],
             payload["full_mutation_matrix_negative_count"]),
            (70, 70, 14, 14, 70),
        )

    def test_selector(self) -> None:
        self.assertEqual(hardening_payload_for_profile("elowen-v663-v5")["profile"], "elowen-v663-v5")
        with self.assertRaises(DeltaError):
            hardening_payload_for_profile("elowen-v663-v5-unknown")

    def test_boundaries_false(self) -> None:
        payload = elowen_hardening_payload()
        fields = (
            "real_person_present", "real_workshop_present", "real_equipment_present",
            "real_material_present", "real_print_present", "real_archive_object_present",
            "real_measurement_present", "equipment_use_authorized",
            "reproduction_authorized", "rights_released", "privacy_complete",
            "accessibility_complete", "professional_authority", "legal_authority",
            "cultural_authority", "maori_authority", "exhaustive_security",
        )
        self.assertTrue(all(payload[field] is False for field in fields))


class TestGeneratedLocalTools(unittest.TestCase):
    def test_all_json_strict(self) -> None:
        paths = sorted((ROOT / PHASE_ROOT).rglob("*.json"))
        self.assertGreaterEqual(len(paths), 50)
        for path in paths:
            self.assertIsInstance(strict_json_loads(path.read_text(encoding="utf-8"), path.name), dict)

    def test_ten_skills(self) -> None:
        roots = sorted(path for path in (ROOT / PHASE_ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(roots), 10)
        for root in roots:
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            smoke = strict_json_loads((root / "smoke.json").read_text(encoding="utf-8"), root.name)
            agent_text = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname: ghc-family-elowen-cairn-"))
            self.assertIn("hardening --profile elowen-v663-v5", " ".join(text.split()))
            self.assertIn("Use $" + root.name, agent_text)
            self.assertEqual(smoke["name"], root.name)
            self.assertFalse(smoke["installed_globally"])
            self.assertTrue(smoke["valid"])

    def test_ten_runners(self) -> None:
        paths = sorted((ROOT / PHASE_ROOT / "runners").glob("*.json"))
        self.assertEqual(len(paths), 10)
        case_by_validator = {case["validator"]: case for case in CASES}
        for path in paths:
            contract = strict_json_loads(path.read_text(encoding="utf-8"), path.name)
            callback = getattr(toolkit, contract["callable"])
            if contract["callable"] == "elowen_hardening_payload":
                result = callback()
                self.assertEqual(result["negative_fixture_count"], 70)
            elif contract["callable"] == "validate_print_privacy_accessibility":
                result = callback(
                    {
                        "privacy": case_by_validator[
                            "validate_print_privacy_notice"
                        ]["positive"],
                        "accessibility": case_by_validator[
                            "validate_print_accessibility_companion"
                        ]["positive"],
                    }
                )
            else:
                result = callback(case_by_validator[contract["callable"]]["positive"])
            self.assertTrue(result["valid"])

    def test_represented_and_open_gap_refusal(self) -> None:
        trinity = {
            "gmut_observations": 0, "gmut_likelihoods": 0,
            "thos_participants": 0, "thos_operators": 0,
            "freed_id_real_keys": 0, "freed_id_real_proofs": 0,
            "cbr_real_decisions": 0, "psyche_inferences": 0,
            "empirical_claimed": False, "deployment_claimed": False,
            "stage_20_claimed": False,
        }
        self.assertTrue(toolkit.validate_print_trinity_boundaries(trinity)["valid"])
        with self.assertRaises(DeltaError):
            toolkit.validate_print_trinity_boundaries({**trinity, "gmut_observations": 1})
        zero = {
            "source_url": "https://www.loc.gov/apis/additional-apis/prints-and-photographs-api/",
            "network_calls": 0, "downloaded_rows": 0, "ingested_rows": 0,
            "credentials_requested": False, "rights_reviewed": False,
            "coverage_claimed": False, "completeness_claimed": False,
            "open_gap": True,
        }
        self.assertTrue(toolkit.validate_print_zero_row_adapter(zero)["valid"])
        with self.assertRaises(DeltaError):
            toolkit.validate_print_zero_row_adapter({**zero, "downloaded_rows": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
