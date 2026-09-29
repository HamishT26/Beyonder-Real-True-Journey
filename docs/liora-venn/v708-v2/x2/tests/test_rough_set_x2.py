from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for code_dir in (ROOT / "x1" / "code", ROOT / "x2" / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import rough_set as x1
import rough_set_x2 as x2


class RoughSetX2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adviser = x2.adviser_fixture()
        cls.fixtures = json.loads(
            (ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8")
        )["fixtures"]

    def test_01_adviser_table_is_valid(self):
        self.assertIs(x1.validate_table(self.adviser), self.adviser)

    def test_02_adviser_full_partition(self):
        self.assertEqual(
            x1.partition(self.adviser), [["u1", "u2"], ["u3"], ["u4"]]
        )

    def test_03_adviser_full_positive_region(self):
        self.assertEqual(
            x1.positive_dependency(self.adviser),
            {"positive_region": ["u3", "u4"], "dependency": [1, 2]},
        )

    def test_04_adviser_empty_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, []), {"positive_region": [], "dependency": [0, 1]})

    def test_05_adviser_a_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["a"]), {"positive_region": ["u4"], "dependency": [1, 4]})

    def test_06_adviser_b_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["b"]), {"positive_region": ["u3"], "dependency": [1, 4]})

    def test_07_adviser_c_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["c"]), {"positive_region": ["u4"], "dependency": [1, 4]})

    def test_08_adviser_ab_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["a", "b"]), {"positive_region": ["u3", "u4"], "dependency": [1, 2]})

    def test_09_adviser_ac_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["a", "c"]), {"positive_region": ["u4"], "dependency": [1, 4]})

    def test_10_adviser_bc_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["b", "c"]), {"positive_region": ["u3", "u4"], "dependency": [1, 2]})

    def test_11_adviser_abc_subset(self):
        self.assertEqual(x1.positive_dependency(self.adviser, ["a", "b", "c"]), {"positive_region": ["u3", "u4"], "dependency": [1, 2]})

    def test_12_adviser_complete_reduct_family(self):
        self.assertEqual(x1.reducts(self.adviser)["reducts"], [["a", "b"], ["b", "c"]])

    def test_13_adviser_core(self):
        self.assertEqual(x1.core(self.adviser)["core"], ["b"])

    def test_14_full_set_is_nonminimal(self):
        self.assertNotIn(["a", "b", "c"], x1.reducts(self.adviser)["reducts"])

    def test_15_positive_control_is_preserving(self):
        full = x1.positive_dependency(self.adviser)["positive_region"]
        self.assertEqual(x1.positive_dependency(self.adviser, ["a", "b"])["positive_region"], full)

    def test_16_mutant_uses_restricted_universe(self):
        claim = x2.adviser_mutant_claim()
        self.assertEqual(claim["working_universe"], ["u3", "u4"])

    def test_17_mutant_looks_numerically_plausible(self):
        claim = x2.adviser_mutant_claim()
        self.assertEqual(claim["claimed_dependency_using_original_denominator"], [2, 4])

    def test_18_mutant_is_rejected(self):
        check = x2.check_adviser_mutant(x2.adviser_mutant_claim())
        self.assertFalse(check["accepted"])
        self.assertEqual(check["correct_positive_region"], ["u4"])

    def test_19_mutant_counterexample_is_explicit(self):
        check = x2.check_adviser_mutant(x2.adviser_mutant_claim())
        self.assertEqual(check["counterexample"]["objects"], ["u2", "u3"])

    def test_20_undeclared_null_is_malformed(self):
        malformed = copy.deepcopy(self.adviser)
        malformed["rows"][1]["conditions"]["a"] = None
        with self.assertRaisesRegex(ValueError, "invalid_condition_value"):
            x1.validate_table(malformed)

    def test_21_intentional_inconsistency_is_valid(self):
        census = x2.consistency_census(self.adviser)
        self.assertEqual(census["conflicting_blocks"], 1)
        self.assertEqual(census["conflicting_objects"], ["u1", "u2"])

    def test_22_consistency_census_block_count(self):
        census = x2.consistency_census(self.adviser)
        self.assertEqual(census["consistent_blocks"], 2)

    def missing_table(self):
        return {
            "condition_attributes": ["a"],
            "rows": [
                {"object": "m1", "conditions": {"a": "?"}, "decision": 0},
                {"object": "m2", "conditions": {"a": 0}, "decision": 0},
                {"object": "m3", "conditions": {"a": 1}, "decision": 1},
            ],
            "target": ["m1", "m2"],
        }

    def test_23_pessimistic_missing_neighborhoods(self):
        self.assertEqual(
            x2.missing_neighborhoods(self.missing_table(), optimistic=False),
            {"m1": ["m1"], "m2": ["m2"], "m3": ["m3"]},
        )

    def test_24_optimistic_missing_neighborhoods(self):
        self.assertEqual(
            x2.missing_neighborhoods(self.missing_table(), optimistic=True),
            {"m1": ["m1", "m2", "m3"], "m2": ["m1", "m2"], "m3": ["m1", "m3"]},
        )

    def test_25_pessimistic_approximation(self):
        result = x2.neighborhood_approximations(self.missing_table(), optimistic=False)
        self.assertEqual((result["lower"], result["upper"]), (["m1", "m2"], ["m1", "m2"]))

    def test_26_optimistic_approximation(self):
        result = x2.neighborhood_approximations(self.missing_table(), optimistic=True)
        self.assertEqual((result["lower"], result["upper"]), (["m2"], ["m1", "m2", "m3"]))

    def dominance_table(self):
        return {
            "condition_attributes": ["a", "b"],
            "rows": [
                {"object": "d1", "conditions": {"a": 0, "b": 0}, "decision": 0},
                {"object": "d2", "conditions": {"a": 1, "b": 0}, "decision": 1},
                {"object": "d3", "conditions": {"a": 1, "b": 1}, "decision": 2},
            ],
            "target": ["d2", "d3"],
        }

    def test_27_dominance_cones(self):
        cones = x2.dominance_cones(self.dominance_table())
        self.assertEqual(cones["upward"]["d1"], ["d1", "d2", "d3"])
        self.assertEqual(cones["downward"]["d3"], ["d1", "d2", "d3"])

    def test_28_dominance_reflexivity(self):
        cones = x2.dominance_cones(self.missing_table())
        for label in ("m1", "m2", "m3"):
            self.assertIn(label, cones["upward"][label])

    def test_29_dominance_approximation(self):
        result = x2.dominance_approximations(self.dominance_table(), threshold=1)
        self.assertEqual(result["target"], ["d2", "d3"])
        self.assertEqual(result["lower"], ["d2", "d3"])
        self.assertEqual(result["upper"], ["d2", "d3"])

    def test_30_correction_preserves_original(self):
        table = copy.deepcopy(self.fixtures[0])
        before = x1.digest(table)
        result = x2.correction_lineage(table, {"object": "O1", "attribute": "a", "old": 0, "new": 9})
        self.assertTrue(result["original_preserved"])
        self.assertEqual(x1.digest(table), before)

    def test_31_correction_changes_digest(self):
        table = copy.deepcopy(self.fixtures[0])
        result = x2.correction_lineage(table, {"object": "O1", "attribute": "a", "old": 0, "new": 9})
        self.assertTrue(result["changed"])

    def test_32_stale_correction_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "stale_patch_old_value"):
            x2.correction_lineage(self.fixtures[0], {"object": "O1", "attribute": "a", "old": 7, "new": 9})

    def test_33_accessible_projection_names_coordinates(self):
        result = x2.accessible_projection(self.fixtures[0])
        self.assertEqual(result["ordered_labels"], ["lower_cardinality", "boundary_cardinality", "upper_cardinality"])
        self.assertFalse(result["manual_accessibility_evaluation"])

    def test_34_authority_boundary_is_false(self):
        result = x2.authority_boundary(self.fixtures[0])
        for key in ("classification_authority", "identity_authority", "remedy_authority", "legal_or_cultural_authority", "maori_authority"):
            self.assertFalse(result[key])

    def test_35_all_x2_operations_cover_all_fixtures(self):
        for table in self.fixtures:
            for operation in x2.X2_OPERATIONS:
                self.assertIsNotNone(x2.dispatch(operation, table))


if __name__ == "__main__":
    unittest.main()
