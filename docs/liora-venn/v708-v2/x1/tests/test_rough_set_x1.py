from __future__ import annotations

import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("liora_rough_set", ROOT / "x1" / "code" / "rough_set.py")
rs = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(rs)
FIXTURES = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]


class RoughSetX1Tests(unittest.TestCase):
    def table(self, index=0): return FIXTURES[index]
    def test_01_validate_good(self): self.assertIs(rs.validate_table(self.table()), self.table())
    def test_02_duplicate_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][1]["object"]=t["rows"][0]["object"]
        with self.assertRaisesRegex(ValueError,"duplicate_object"):rs.validate_table(t)
    def test_03_boolean_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][0]["conditions"]["a"]=True
        with self.assertRaisesRegex(ValueError,"invalid_condition_value"):rs.validate_table(t)
    def test_04_shape_rejected(self):
        t=json.loads(json.dumps(self.table()));t["condition_attributes"].append("z")
        with self.assertRaisesRegex(ValueError,"condition_shape_mismatch"):rs.validate_table(t)
    def test_05_decision_rejected(self):
        t=json.loads(json.dumps(self.table()));t["rows"][0]["decision"]="bad"
        with self.assertRaisesRegex(ValueError,"invalid_decision"):rs.validate_table(t)
    def test_06_target_rejected(self):
        t=json.loads(json.dumps(self.table()));t["target"].append("MISSING")
        with self.assertRaisesRegex(ValueError,"invalid_target"):rs.validate_table(t)
    def test_07_partition_agreement(self):
        for t in FIXTURES:self.assertEqual(rs.partition(t),rs.partition_pairwise(t))
    def test_08_partition_cover(self):
        for t in FIXTURES:self.assertEqual(sorted(sum(rs.partition(t),[])),sorted(r["object"] for r in t["rows"]))
    def test_09_lower_subset_target(self):
        for t in FIXTURES:self.assertTrue(set(rs.approximations(t)["lower"])<=set(t["target"]))
    def test_10_target_subset_upper(self):
        for t in FIXTURES:self.assertTrue(set(t["target"])<=set(rs.approximations(t)["upper"]))
    def test_11_boundary_identity(self):
        for t in FIXTURES:
            a=rs.approximations(t);self.assertEqual(set(a["boundary"]),set(a["upper"])-set(a["lower"]))
    def test_12_negative_identity(self):
        for t in FIXTURES:
            a=rs.approximations(t);u={r["object"] for r in t["rows"]};self.assertEqual(set(a["negative"]),u-set(a["upper"]))
    def test_13_accuracy_bounds(self):
        for t in FIXTURES:
            n,d=rs.accuracy_membership(t)["accuracy"];self.assertGreaterEqual(Fraction(n,d),0);self.assertLessEqual(Fraction(n,d),1)
    def test_14_membership_bounds(self):
        for t in FIXTURES:
            for n,d in rs.accuracy_membership(t)["membership"].values():self.assertTrue(Fraction(0)<=Fraction(n,d)<=Fraction(1))
    def test_15_positive_region_bound(self):
        for t in FIXTURES:self.assertLessEqual(len(rs.positive_dependency(t)["positive_region"]),len(t["rows"]))
    def test_16_dependency_bounds(self):
        for t in FIXTURES:
            n,d=rs.positive_dependency(t)["dependency"];self.assertTrue(Fraction(0)<=Fraction(n,d)<=Fraction(1))
    def test_17_dependency_refinement(self):
        for t in FIXTURES:self.assertLessEqual(rs.dependency_fraction(t,["a"]),rs.dependency_fraction(t,["a","b","c"]))
    def test_18_discernibility_known_pairs(self):
        for t in FIXTURES:
            by={r["object"]:r for r in t["rows"]}
            for cell in rs.discernibility(t):self.assertNotEqual(by[cell["left"]]["decision"],by[cell["right"]]["decision"])
    def test_19_reduct_preservation(self):
        for t in FIXTURES:
            result=rs.reducts(t);full=Fraction(*result["full_dependency"])
            for reduct in result["reducts"]:self.assertEqual(rs.dependency_fraction(t,reduct),full)
    def test_20_reduct_minimality(self):
        for t in FIXTURES:
            result=rs.reducts(t);full=Fraction(*result["full_dependency"])
            for reduct in result["reducts"]:
                for i in range(len(reduct)):self.assertNotEqual(rs.dependency_fraction(t,reduct[:i]+reduct[i+1:]),full)
    def test_21_core_intersection(self):
        for t in FIXTURES:
            result=rs.core(t);expected=set(result["reducts"][0]) if result["reducts"] else set()
            for reduct in result["reducts"][1:]:expected&=set(reduct)
            self.assertEqual(result["core"],sorted(expected))
    def test_22_empty_target_convention(self):
        t=json.loads(json.dumps(self.table()));t["target"]=[];self.assertEqual(rs.accuracy_membership(t)["accuracy"],[1,1])
    def test_23_digest_changes(self):
        t=json.loads(json.dumps(self.table()));before=rs.digest(t);t["rows"][0]["conditions"]["a"]=2;self.assertNotEqual(before,rs.digest(t))
    def test_24_all_operations(self):
        for t in FIXTURES:
            for operation in rs.X1_OPERATIONS:self.assertIsNotNone(rs.dispatch(operation,t))
    def test_25_models_written(self):
        self.assertEqual(len(list((ROOT/"x1"/"models").glob("*.json"))),15)


if __name__ == "__main__": unittest.main()
