from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v656_v1_core as core
import ghc_family_v656_v1_phase_data as data


class TamarVeyV656V1CoreTests(unittest.TestCase):
    def test_all_valid_contracts_pass(self) -> None:
        for proposal in data.PROPOSALS:
            with self.subTest(proposal=proposal["proposal_id"]):
                self.assertEqual(core.validate_contract(core.valid_contract(proposal)), [])

    def test_all_frozen_mutations_are_rejected(self) -> None:
        suite = core.execute_all()
        self.assertEqual(suite["proposal_count"], 30)
        self.assertEqual(suite["valid_fixture_count"], 30)
        self.assertEqual(suite["rejected_mutation_count"], 150)
        self.assertEqual(suite["accepted_mutation_count"], 0)

    def test_outcome_distribution_is_frozen(self) -> None:
        suite = core.execute_all()
        counts = {name: 0 for name in data.OUTCOME_CLASSES}
        for result in suite["results"]:
            counts[result["observed_outcome"]] += 1
        self.assertEqual(
            counts,
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )

    def test_external_actions_and_promotions_remain_zero(self) -> None:
        for result in core.execute_all()["results"]:
            contract = result["contract"]
            self.assertTrue(
                all(value == 0 for value in contract["external_action_counts"].values())
            )
            self.assertTrue(
                all(value is False for value in contract["promotion_claims"].values())
            )

    def test_each_group_has_three_contracts_and_fifteen_rejections(self) -> None:
        for group_index in range(1, 11):
            with self.subTest(group=group_index):
                group = core.execute_group(group_index)
                self.assertEqual(len(group["proposal_ids"]), 3)
                self.assertEqual(group["valid_fixture_count"], 3)
                self.assertEqual(group["rejected_mutation_count"], 15)
                self.assertEqual(group["accepted_mutation_count"], 0)

    def test_phase_local_runner_modules_import(self) -> None:
        modules = [
            "ghc_family_darkroom_film_custody_boundary",
            "ghc_family_darkroom_chemical_sequence_integrity",
            "ghc_family_darkroom_capacity_waste_reserve",
            "ghc_family_darkroom_optical_exposure_proxy",
            "ghc_family_darkroom_wash_archive_handover",
            "ghc_family_darkroom_accessibility_incident_boundary",
            "ghc_family_photo_privacy_authority_reserve",
            "ghc_family_gmut_photochemical_field_firewall",
            "ghc_family_thos_freed_darkroom_profile",
            "ghc_family_v656_v1_suite",
        ]
        for name in modules:
            with self.subTest(module=name):
                self.assertIsNotNone(importlib.import_module(name))

    def test_protected_gate_set_is_consistent(self) -> None:
        for result in core.execute_all()["results"]:
            self.assertEqual(
                result["contract"]["protected_gates"],
                data.PROTECTED_GATES,
            )


if __name__ == "__main__":
    unittest.main()
