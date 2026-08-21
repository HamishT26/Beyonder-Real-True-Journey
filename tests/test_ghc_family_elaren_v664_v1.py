from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_cylinder_evidence as cylinder


DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_cylinder_evidence.py",
]


class CylinderRegistryTests(unittest.TestCase):
    def test_registry_has_exactly_twenty_unique_surfaces(self) -> None:
        self.assertEqual(len(cylinder.SURFACE_SPECS), 20)
        self.assertEqual(len(cylinder.SPEC_BY_SLUG), 20)
        self.assertEqual(len(cylinder.SPEC_BY_ID), 20)
        self.assertEqual(
            [row["proposal_id"] for row in cylinder.SURFACE_SPECS],
            [f"EL6641-N{index:03d}" for index in range(1, 21)],
        )

    def test_only_four_core_outcomes_are_present(self) -> None:
        observed = {row["expected_outcome"] for row in cylinder.SURFACE_SPECS}
        self.assertEqual(observed, cylinder.ALLOWED_OUTCOMES)

    def test_frozen_outcome_distribution(self) -> None:
        payload = cylinder.ghc_family_execute_v664_v1()
        self.assertEqual(
            payload["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )

    def test_all_eighty_mutations_are_rejected(self) -> None:
        rejected = 0
        for spec in cylinder.SURFACE_SPECS:
            execution = cylinder.ghc_family_execute_cylinder_surface(spec["surface"])
            self.assertEqual(execution["mutation_count"], 4)
            self.assertTrue(execution["valid"])
            rejected += execution["rejected_mutation_count"]
        self.assertEqual(rejected, 80)

    def test_every_fixture_retains_all_protected_refusals(self) -> None:
        for spec in cylinder.SURFACE_SPECS:
            fixture = cylinder.ghc_family_build_cylinder_fixture(spec["surface"])
            self.assertEqual(fixture["protected_gates"], list(cylinder.PROTECTED_GATES))
            for field in cylinder.REFUSAL_FIELDS:
                self.assertIs(fixture[field], False, (spec["surface"], field))

    def test_every_fixture_has_zero_real_world_rows_and_no_authority(self) -> None:
        for spec in cylinder.SURFACE_SPECS:
            fixture = cylinder.ghc_family_build_cylinder_fixture(spec["surface"])
            self.assertTrue(fixture["synthetic"])
            self.assertEqual(fixture["real_world_rows"], 0)
            self.assertEqual(fixture["authority"], "none")

    def test_open_gap_is_the_zero_row_adapter_only(self) -> None:
        rows = [row for row in cylinder.SURFACE_SPECS if row["expected_outcome"] == "open_gap"]
        self.assertEqual([row["surface"] for row in rows], ["zero-row-vocabulary-adapter"])
        fixture = cylinder.ghc_family_build_cylinder_fixture(rows[0]["surface"])
        self.assertEqual(fixture["live_calls"], 0)
        self.assertEqual(fixture["downloads"], 0)
        self.assertTrue(fixture["gap_open"])

    def test_exact_gate_is_the_rights_matrix_only(self) -> None:
        rows = [row for row in cylinder.SURFACE_SPECS if row["expected_outcome"] == "exact_gate"]
        self.assertEqual([row["surface"] for row in rows], ["rights-authority-matrix"])
        fixture = cylinder.ghc_family_build_cylinder_fixture(rows[0]["surface"])
        self.assertEqual(fixture["occupied_chairs"], 0)
        self.assertFalse(fixture["authority_decision_made"])
        self.assertTrue(fixture["gate_open"])

    def test_stage_20_surface_is_a_completed_refusal_not_readiness(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("stage-20-admission-docket")
        self.assertEqual(fixture["expected_outcome"], "completed")
        self.assertEqual(fixture["admitted_evidence_rows"], 0)
        self.assertFalse(fixture["stage_20_ready"])

    def test_unknown_surface_is_rejected(self) -> None:
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_build_cylinder_fixture("unknown-surface")

    def test_missing_key_is_rejected(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("cylinder-capsule")
        fixture.pop("custody_state")
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_validate_cylinder_surface(fixture)

    def test_extra_key_is_rejected(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("cylinder-capsule")
        fixture["unfrozen_field"] = True
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_validate_cylinder_surface(fixture)

    def test_protected_gate_promotion_is_rejected(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("cylinder-capsule")
        fixture["professional_authority"] = True
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_validate_cylinder_surface(fixture)

    def test_source_map_drift_is_rejected(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("cylinder-capsule")
        fixture["source_ids"] = ["unfrozen-source"]
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_validate_cylinder_surface(fixture)

    def test_phase_execution_is_network_and_download_free(self) -> None:
        payload = cylinder.ghc_family_execute_v664_v1()
        self.assertEqual(payload["network_calls"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["real_world_rows"], 0)
        self.assertEqual(payload["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(payload.get("post_success_replay", False))

    def test_phase_aliases_are_additive_and_callable(self) -> None:
        self.assertIs(cylinder.build_ghc_family_v664_v1_evidence, cylinder.ghc_family_execute_v664_v1)
        self.assertIs(cylinder.ghc_family_validate_v664_v1_surface, cylinder.ghc_family_validate_cylinder_surface)
        self.assertIs(cylinder.ghc_family_run_v664_v1_profile, cylinder.ghc_family_run_cylinder_profile)

    def test_fixture_serialization_is_deterministic(self) -> None:
        first = cylinder.ghc_family_build_cylinder_fixture("transfer-provenance")
        second = cylinder.ghc_family_build_cylinder_fixture("transfer-provenance")
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )

    def test_validator_does_not_mutate_fixture(self) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture("freed-id-correction-chain")
        before = deepcopy(fixture)
        cylinder.ghc_family_validate_cylinder_surface(fixture)
        self.assertEqual(fixture, before)

    def test_cli_all_profile_is_valid(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "ghc_family_cylinder_evidence.py"), "--profile", "all"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["surface_count"], 20)


class CylinderRunnerTests(unittest.TestCase):
    def test_runner_registry_has_ten_profiles(self) -> None:
        self.assertEqual(len(cylinder.RUNNER_PROFILES), 10)
        covered = [surface for rows in cylinder.RUNNER_PROFILES.values() for surface in rows]
        self.assertEqual(sorted(covered), sorted(cylinder.SPEC_BY_SLUG))
        self.assertEqual(len(covered), len(set(covered)))

    def test_unknown_runner_profile_is_rejected(self) -> None:
        with self.assertRaises(cylinder.EvidenceError):
            cylinder.ghc_family_run_cylinder_profile("unknown-profile")


def _surface_test(surface: str):
    def test(self: unittest.TestCase) -> None:
        fixture = cylinder.ghc_family_build_cylinder_fixture(surface)
        result = cylinder.ghc_family_validate_cylinder_surface(fixture)
        self.assertTrue(result["valid"])
        self.assertEqual(result["surface"], surface)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertEqual(result["authority"], "none")

    return test


def _runner_test(profile: str):
    def test(self: unittest.TestCase) -> None:
        result = cylinder.ghc_family_run_cylinder_profile(profile)
        self.assertTrue(result["valid"])
        self.assertEqual(result["profile"], profile)
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertTrue(result["family_current_runner"].startswith("ghc_family_cylinder_"))

    return test


for _surface in cylinder.SPEC_BY_SLUG:
    setattr(
        CylinderRegistryTests,
        f"test_surface_{_surface.replace('-', '_')}",
        _surface_test(_surface),
    )

for _profile in cylinder.RUNNER_PROFILES:
    setattr(
        CylinderRunnerTests,
        f"test_profile_{_profile.replace('-', '_')}",
        _runner_test(_profile),
    )


if __name__ == "__main__":
    unittest.main()
