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

import ghc_family_marigram_evidence as marigram


DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_marigram_evidence.py",
]


class MarigramRegistryTests(unittest.TestCase):
    def test_registry_has_exactly_twenty_unique_surfaces(self) -> None:
        self.assertEqual(len(marigram.SURFACE_SPECS), 20)
        self.assertEqual(len(marigram.SPEC_BY_SLUG), 20)
        self.assertEqual(len(marigram.SPEC_BY_ID), 20)
        self.assertEqual(
            [row["proposal_id"] for row in marigram.SURFACE_SPECS],
            [f"NE6642-N{index:03d}" for index in range(1, 21)],
        )

    def test_only_four_core_outcomes_are_present(self) -> None:
        observed = {row["expected_outcome"] for row in marigram.SURFACE_SPECS}
        self.assertEqual(observed, marigram.ALLOWED_OUTCOMES)

    def test_frozen_outcome_distribution(self) -> None:
        payload = marigram.ghc_family_execute_v664_v2()
        self.assertEqual(
            payload["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )

    def test_all_eighty_mutations_are_rejected(self) -> None:
        rejected = 0
        for spec in marigram.SURFACE_SPECS:
            execution = marigram.ghc_family_execute_marigram_surface(spec["surface"])
            self.assertEqual(execution["mutation_count"], 4)
            self.assertTrue(execution["valid"])
            rejected += execution["rejected_mutation_count"]
        self.assertEqual(rejected, 80)

    def test_every_fixture_retains_all_protected_refusals(self) -> None:
        for spec in marigram.SURFACE_SPECS:
            fixture = marigram.ghc_family_build_marigram_fixture(spec["surface"])
            self.assertEqual(fixture["protected_gates"], list(marigram.PROTECTED_GATES))
            for field in marigram.REFUSAL_FIELDS:
                self.assertIs(fixture[field], False, (spec["surface"], field))

    def test_every_fixture_has_zero_real_world_rows_and_no_authority(self) -> None:
        for spec in marigram.SURFACE_SPECS:
            fixture = marigram.ghc_family_build_marigram_fixture(spec["surface"])
            self.assertTrue(fixture["synthetic"])
            self.assertEqual(fixture["real_world_rows"], 0)
            self.assertEqual(fixture["authority"], "none")

    def test_open_gap_is_the_zero_row_adapter_only(self) -> None:
        rows = [row for row in marigram.SURFACE_SPECS if row["expected_outcome"] == "open_gap"]
        self.assertEqual([row["surface"] for row in rows], ["zero-row-tide-adapter"])
        fixture = marigram.ghc_family_build_marigram_fixture(rows[0]["surface"])
        self.assertEqual(fixture["live_calls"], 0)
        self.assertEqual(fixture["downloads"], 0)
        self.assertTrue(fixture["gap_open"])

    def test_exact_gate_is_the_rights_matrix_only(self) -> None:
        rows = [row for row in marigram.SURFACE_SPECS if row["expected_outcome"] == "exact_gate"]
        self.assertEqual([row["surface"] for row in rows], ["rights-authority-matrix"])
        fixture = marigram.ghc_family_build_marigram_fixture(rows[0]["surface"])
        self.assertEqual(fixture["occupied_chairs"], 0)
        self.assertFalse(fixture["authority_decision_made"])
        self.assertTrue(fixture["gate_open"])

    def test_stage_20_surface_is_a_completed_refusal_not_readiness(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("stage-20-refusal-proof")
        self.assertEqual(fixture["expected_outcome"], "completed")
        self.assertEqual(fixture["admitted_evidence_rows"], 0)
        self.assertFalse(fixture["stage_20_ready"])

    def test_unknown_surface_is_rejected(self) -> None:
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_build_marigram_fixture("unknown-surface")

    def test_missing_key_is_rejected(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("marigram-archive-capsule")
        fixture.pop("custody_state")
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_validate_marigram_surface(fixture)

    def test_extra_key_is_rejected(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("marigram-archive-capsule")
        fixture["unfrozen_field"] = True
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_validate_marigram_surface(fixture)

    def test_protected_gate_promotion_is_rejected(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("marigram-archive-capsule")
        fixture["professional_authority"] = True
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_validate_marigram_surface(fixture)

    def test_source_map_drift_is_rejected(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("marigram-archive-capsule")
        fixture["source_ids"] = ["unfrozen-source"]
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_validate_marigram_surface(fixture)

    def test_phase_execution_is_network_and_download_free(self) -> None:
        payload = marigram.ghc_family_execute_v664_v2()
        self.assertEqual(payload["network_calls"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["real_world_rows"], 0)
        self.assertEqual(payload["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(payload.get("post_success_replay", False))

    def test_phase_aliases_are_additive_and_callable(self) -> None:
        self.assertIs(marigram.build_ghc_family_v664_v2_evidence, marigram.ghc_family_execute_v664_v2)
        self.assertIs(marigram.ghc_family_validate_v664_v2_surface, marigram.ghc_family_validate_marigram_surface)
        self.assertIs(marigram.ghc_family_run_v664_v2_profile, marigram.ghc_family_run_marigram_profile)

    def test_fixture_serialization_is_deterministic(self) -> None:
        first = marigram.ghc_family_build_marigram_fixture("digitization-provenance")
        second = marigram.ghc_family_build_marigram_fixture("digitization-provenance")
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )

    def test_validator_does_not_mutate_fixture(self) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture("metadata-amendment-trail")
        before = deepcopy(fixture)
        marigram.ghc_family_validate_marigram_surface(fixture)
        self.assertEqual(fixture, before)

    def test_cli_all_profile_is_valid(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "ghc_family_marigram_evidence.py"), "--profile", "all"],
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


class MarigramRunnerTests(unittest.TestCase):
    def test_runner_registry_has_ten_profiles(self) -> None:
        self.assertEqual(len(marigram.RUNNER_PROFILES), 10)
        covered = [surface for rows in marigram.RUNNER_PROFILES.values() for surface in rows]
        self.assertEqual(sorted(covered), sorted(marigram.SPEC_BY_SLUG))
        self.assertEqual(len(covered), len(set(covered)))

    def test_unknown_runner_profile_is_rejected(self) -> None:
        with self.assertRaises(marigram.EvidenceError):
            marigram.ghc_family_run_marigram_profile("unknown-profile")


def _surface_test(surface: str):
    def test(self: unittest.TestCase) -> None:
        fixture = marigram.ghc_family_build_marigram_fixture(surface)
        result = marigram.ghc_family_validate_marigram_surface(fixture)
        self.assertTrue(result["valid"])
        self.assertEqual(result["surface"], surface)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertEqual(result["authority"], "none")

    return test


def _runner_test(profile: str):
    def test(self: unittest.TestCase) -> None:
        result = marigram.ghc_family_run_marigram_profile(profile)
        self.assertTrue(result["valid"])
        self.assertEqual(result["profile"], profile)
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["real_world_rows"], 0)
        self.assertTrue(result["family_current_runner"].startswith("ghc_family_marigram_"))

    return test


for _surface in marigram.SPEC_BY_SLUG:
    setattr(
        MarigramRegistryTests,
        f"test_surface_{_surface.replace('-', '_')}",
        _surface_test(_surface),
    )

for _profile in marigram.RUNNER_PROFILES:
    setattr(
        MarigramRunnerTests,
        f"test_profile_{_profile.replace('-', '_')}",
        _runner_test(_profile),
    )


if __name__ == "__main__":
    unittest.main()
