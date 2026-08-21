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

import ghc_family_seed_bank_evidence as seed_bank


DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_seed_bank_evidence.py",
]


class SeedBankRegistryTests(unittest.TestCase):
    def test_registry_has_exactly_twenty_unique_surfaces(self) -> None:
        self.assertEqual(len(seed_bank.SURFACE_SPECS), 20)
        self.assertEqual(len(seed_bank.SPEC_BY_SLUG), 20)
        self.assertEqual(len(seed_bank.SPEC_BY_ID), 20)
        self.assertEqual(
            [row["proposal_id"] for row in seed_bank.SURFACE_SPECS],
            [f"VE6643-N{index:03d}" for index in range(1, 21)],
        )

    def test_only_four_core_outcomes_are_present(self) -> None:
        observed = {row["expected_outcome"] for row in seed_bank.SURFACE_SPECS}
        self.assertEqual(observed, seed_bank.ALLOWED_OUTCOMES)

    def test_frozen_outcome_distribution(self) -> None:
        payload = seed_bank.ghc_family_execute_v664_v3()
        self.assertEqual(
            payload["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )

    def test_all_eighty_mutations_are_rejected(self) -> None:
        rejected = 0
        for spec in seed_bank.SURFACE_SPECS:
            execution = seed_bank.ghc_family_execute_seed_bank_surface(spec["surface"])
            self.assertEqual(execution["mutation_count"], 4)
            self.assertTrue(execution["valid"])
            rejected += execution["rejected_mutation_count"]
        self.assertEqual(rejected, 80)

    def test_every_fixture_retains_all_protected_refusals(self) -> None:
        for spec in seed_bank.SURFACE_SPECS:
            fixture = seed_bank.ghc_family_build_seed_bank_fixture(spec["surface"])
            self.assertEqual(fixture["protected_gates"], list(seed_bank.PROTECTED_GATES))
            for field in seed_bank.REFUSAL_FIELDS:
                self.assertIs(fixture[field], False, (spec["surface"], field))

    def test_every_fixture_has_zero_real_world_rows_and_no_authority(self) -> None:
        for spec in seed_bank.SURFACE_SPECS:
            fixture = seed_bank.ghc_family_build_seed_bank_fixture(spec["surface"])
            self.assertTrue(fixture["synthetic"])
            self.assertEqual(fixture["real_world_rows"], 0)
            self.assertEqual(fixture["authority"], "none")

    def test_open_gap_is_the_zero_row_adapter_only(self) -> None:
        rows = [row for row in seed_bank.SURFACE_SPECS if row["expected_outcome"] == "open_gap"]
        self.assertEqual([row["surface"] for row in rows], ["zero-row-seed-adapter"])
        fixture = seed_bank.ghc_family_build_seed_bank_fixture(rows[0]["surface"])
        self.assertEqual(fixture["live_calls"], 0)
        self.assertEqual(fixture["downloads"], 0)
        self.assertTrue(fixture["gap_open"])

    def test_exact_gate_is_the_rights_matrix_only(self) -> None:
        rows = [row for row in seed_bank.SURFACE_SPECS if row["expected_outcome"] == "exact_gate"]
        self.assertEqual([row["surface"] for row in rows], ["seed-stewardship-authority-matrix"])
        fixture = seed_bank.ghc_family_build_seed_bank_fixture(rows[0]["surface"])
        self.assertEqual(fixture["occupied_chairs"], 0)
        self.assertFalse(fixture["authority_decision_made"])
        self.assertTrue(fixture["gate_open"])

    def test_stage_20_surface_is_a_completed_refusal_not_readiness(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("stage-20-refusal-proof")
        self.assertEqual(fixture["expected_outcome"], "completed")
        self.assertEqual(fixture["admitted_evidence_rows"], 0)
        self.assertFalse(fixture["stage_20_ready"])

    def test_unknown_surface_is_rejected(self) -> None:
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_build_seed_bank_fixture("unknown-surface")

    def test_missing_key_is_rejected(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("seed-accession-capsule")
        fixture.pop("custody_state")
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_validate_seed_bank_surface(fixture)

    def test_extra_key_is_rejected(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("seed-accession-capsule")
        fixture["unfrozen_field"] = True
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_validate_seed_bank_surface(fixture)

    def test_protected_gate_promotion_is_rejected(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("seed-accession-capsule")
        fixture["professional_authority"] = True
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_validate_seed_bank_surface(fixture)

    def test_source_map_drift_is_rejected(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("seed-accession-capsule")
        fixture["source_ids"] = ["unfrozen-source"]
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_validate_seed_bank_surface(fixture)

    def test_phase_execution_is_network_and_download_free(self) -> None:
        payload = seed_bank.ghc_family_execute_v664_v3()
        self.assertEqual(payload["network_calls"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["real_world_rows"], 0)
        self.assertEqual(payload["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(payload.get("post_success_replay", False))

    def test_phase_aliases_are_additive_and_callable(self) -> None:
        self.assertIs(seed_bank.build_ghc_family_v664_v3_evidence, seed_bank.ghc_family_execute_v664_v3)
        self.assertIs(seed_bank.ghc_family_validate_v664_v3_surface, seed_bank.ghc_family_validate_seed_bank_surface)
        self.assertIs(seed_bank.ghc_family_run_v664_v3_profile, seed_bank.ghc_family_run_seed_bank_profile)

    def test_fixture_serialization_is_deterministic(self) -> None:
        first = seed_bank.ghc_family_build_seed_bank_fixture("seed-label-register")
        second = seed_bank.ghc_family_build_seed_bank_fixture("seed-label-register")
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )

    def test_validator_does_not_mutate_fixture(self) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture("seed-metadata-amendment-trail")
        before = deepcopy(fixture)
        seed_bank.ghc_family_validate_seed_bank_surface(fixture)
        self.assertEqual(fixture, before)

    def test_cli_all_profile_is_valid(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "ghc_family_seed_bank_evidence.py"), "--profile", "all"],
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


class SeedBankRunnerTests(unittest.TestCase):
    def test_runner_registry_has_ten_profiles(self) -> None:
        self.assertEqual(len(seed_bank.RUNNER_PROFILES), 10)
        covered = [surface for rows in seed_bank.RUNNER_PROFILES.values() for surface in rows]
        self.assertEqual(sorted(covered), sorted(seed_bank.SPEC_BY_SLUG))
        self.assertEqual(len(covered), len(set(covered)))

    def test_unknown_runner_profile_is_rejected(self) -> None:
        with self.assertRaises(seed_bank.EvidenceError):
            seed_bank.ghc_family_run_seed_bank_profile("unknown-profile")


def _surface_test(surface: str):
    def test(self: unittest.TestCase) -> None:
        fixture = seed_bank.ghc_family_build_seed_bank_fixture(surface)
        result = seed_bank.ghc_family_validate_seed_bank_surface(fixture)
        self.assertTrue(result["valid"])
        self.assertEqual(result["surface"], surface)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertEqual(result["authority"], "none")

    return test


def _runner_test(profile: str):
    def test(self: unittest.TestCase) -> None:
        result = seed_bank.ghc_family_run_seed_bank_profile(profile)
        self.assertTrue(result["valid"])
        self.assertEqual(result["profile"], profile)
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertTrue(result["family_current_runner"].startswith("ghc_family_seed_bank_"))

    return test


for _surface in seed_bank.SPEC_BY_SLUG:
    setattr(
        SeedBankRegistryTests,
        f"test_surface_{_surface.replace('-', '_')}",
        _surface_test(_surface),
    )

for _profile in seed_bank.RUNNER_PROFILES:
    setattr(
        SeedBankRunnerTests,
        f"test_profile_{_profile.replace('-', '_')}",
        _runner_test(_profile),
    )


if __name__ == "__main__":
    unittest.main()
