from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for code_dir in (ROOT / "x1" / "code", ROOT / "x2" / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import teren_tasks as tasks


class TerenFiveTaskTests(unittest.TestCase):
    def test_01_two_completions_present(self):
        self.assertEqual(len(tasks.task1_missing_completions()["positive"]["completions"]), 2)

    def test_02_missing_guaranteed_lower(self):
        self.assertEqual(tasks.task1_missing_completions()["positive"]["guaranteed_lower"], ["m1"])

    def test_03_missing_possible_upper(self):
        self.assertEqual(tasks.task1_missing_completions()["positive"]["possible_upper"], ["m1", "m2", "m3"])

    def test_04_missing_dependency_set(self):
        self.assertEqual(tasks.task1_missing_completions()["positive"]["dependency_values"], [[1, 3], [1, 1]])

    def test_05_missing_imputation_mutant_rejected(self):
        self.assertFalse(tasks.task1_missing_completions()["mutant_accepted"])

    def test_06_snapshot_v0(self):
        self.assertEqual(tasks.task2_versioned_corrections()["positive"]["snapshots"]["V0"]["dependency"], [1, 1])

    def test_07_snapshot_v1(self):
        result = tasks.task2_versioned_corrections()["positive"]["snapshots"]["V1"]
        self.assertEqual((result["lower"], result["upper"], result["dependency"]), ([], ["s1", "s3"], [1, 3]))

    def test_08_snapshot_v2(self):
        result = tasks.task2_versioned_corrections()["positive"]["snapshots"]["V2"]
        self.assertEqual((result["lower"], result["upper"], result["dependency"]), (["s1", "s3"], ["s1", "s3"], [1, 1]))

    def test_09_snapshot_digests_distinct(self):
        snapshots = tasks.task2_versioned_corrections()["positive"]["snapshots"]
        self.assertEqual(len({record["input_digest"] for record in snapshots.values()}), 3)

    def test_10_latest_only_mutant_rejected(self):
        self.assertFalse(tasks.task2_versioned_corrections()["mutant_accepted"])

    def test_11_reduct_family_complete(self):
        self.assertEqual(tasks.task3_reduct_family()["positive"]["reducts"], [["a"], ["b"]])

    def test_12_reduct_core_empty(self):
        self.assertEqual(tasks.task3_reduct_family()["positive"]["core"], [])

    def test_13_empty_and_c_nonpreserving(self):
        records = tasks.task3_reduct_family()["positive"]["records"]
        observed = [record["attributes"] for record in records if record["dependency"] == [0, 1]]
        self.assertEqual(observed, [[], ["c"]])

    def test_14_full_set_nonminimal(self):
        self.assertNotIn(["a", "b", "c"], tasks.task3_reduct_family()["positive"]["reducts"])

    def test_15_alias_mutant_rejected(self):
        self.assertFalse(tasks.task3_reduct_family()["mutant_accepted"])

    def test_16_all_mathematics_match(self):
        self.assertEqual(tasks.task4_permission_boundary()["positive"]["mathematical_match"], [True] * 5)

    def test_17_permission_effect_vector(self):
        self.assertEqual(tasks.task4_permission_boundary()["positive"]["effect_vector"], [1, 0, 0, 0, 0])

    def test_18_dependency_permission_mutant(self):
        self.assertEqual(tasks.task4_permission_boundary()["mutant_effect_vector"], [1, 1, 1, 1, 1])

    def test_19_permission_mutant_rejected(self):
        self.assertFalse(tasks.task4_permission_boundary()["mutant_accepted"])

    def test_20_permission_classification(self):
        self.assertEqual(tasks.task4_permission_boundary()["classification"], "INCOMPLETE_POLICY_EVIDENCE")

    def test_21_checker_verdict_vector(self):
        self.assertEqual(tasks.task5_checker_integrity()["positive"]["verdicts"], ["ACCEPT", "REJECT_MATHEMATICAL_MISMATCH", "VALID_INPUT_REFUSED_NOT_PASS"])

    def test_22_bad_submission_has_own_digest(self):
        digests = tasks.task5_checker_integrity()["positive"]["submission_digests"]
        self.assertNotEqual(digests["G"], digests["B"])

    def test_23_repair_first_mutant_accepts_bad(self):
        self.assertEqual(tasks.task5_checker_integrity()["mutant_repair_first_verdicts"][1], "ACCEPT")

    def test_24_checker_mutant_rejected(self):
        self.assertFalse(tasks.task5_checker_integrity()["mutant_accepted"])

    def test_25_all_five_tasks_present(self):
        self.assertEqual(len(tasks.run_all()), 5)


if __name__ == "__main__":
    unittest.main()
