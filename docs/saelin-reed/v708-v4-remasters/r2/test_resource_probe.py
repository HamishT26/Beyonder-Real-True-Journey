"""Independent arithmetic fixtures for the corrected measurement adapter."""
import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('owned_resource_probe', Path(__file__).with_name('resource_probe.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(cpu, at, group='test', rss=100):
    return dict(cpu=cpu, sampled_at=at, group=group, rss=rss)


class ResourceMeasurementTests(unittest.TestCase):
    def test_different_counter_intervals_have_independent_denominators(self):
        before = {(1, 1): row(1, 0), (2, 2): row(0, 8)}
        after = {(1, 1): row(6, 10), (2, 2): row(1, 12)}
        groups, logical = module.aggregate_samples(before, after, 2)
        actual = groups['test']
        self.assertEqual(logical, 2)
        # Hand calculation: (5/10 + 1/4) / 2 * 100 = 37.5 percent.
        self.assertEqual(actual['matched_process_cpu_percent_of_logical_capacity'], 37.5)
        self.assertEqual((actual['sample_interval_min_seconds'], actual['sample_interval_max_seconds']), (4, 10))

    def test_unknown_capacity_is_not_one_cpu(self):
        groups, logical = module.aggregate_samples({(1, 1): row(0, 0)}, {(1, 1): row(1, 2)}, None)
        self.assertIsNone(logical)
        self.assertIsNone(groups['test']['matched_process_cpu_percent_of_logical_capacity'])

    def test_reused_pid_is_not_matched(self):
        groups, _ = module.aggregate_samples({(1, 1): row(5, 0)}, {(1, 2): row(1, 2)}, 4)
        self.assertEqual(groups['test']['new_processes_without_baseline'], 1)
        self.assertEqual(groups['test']['matched_cpu_samples'], 0)
        self.assertIsNone(groups['test']['matched_process_cpu_percent_of_logical_capacity'])

    def test_regressing_counter_is_flagged_not_clamped(self):
        groups, _ = module.aggregate_samples({(1, 1): row(5, 0)}, {(1, 1): row(1, 2)}, 4)
        self.assertEqual(groups['test']['invalid_counter_pairs'], 1)
        self.assertIsNone(groups['test']['matched_process_cpu_percent_of_logical_capacity'])

    def test_zero_interval_is_flagged(self):
        groups, _ = module.aggregate_samples({(1, 1): row(0, 2)}, {(1, 1): row(1, 2)}, 4)
        self.assertEqual(groups['test']['invalid_counter_pairs'], 1)

    def test_exited_process_has_no_invented_end_counter(self):
        groups, _ = module.aggregate_samples({(1, 1): row(8, 0)}, {}, 4)
        self.assertEqual(groups, {})

    def test_nonfinite_values_are_not_rates(self):
        groups, _ = module.aggregate_samples({(1, 1): row(0, 0)}, {(1, 1): row(math.nan, 2)}, 4)
        self.assertEqual(groups['test']['invalid_counter_pairs'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
