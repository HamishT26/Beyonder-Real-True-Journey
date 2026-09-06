"""Tests bind complete outputs to x1-frozen expectations, including refusal reasons."""
from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_iveren_brook_v687_v2_core import dispatch

CASES = json.loads(
    (ROOT / "docs/iveren-brook/v687-v2/x1/new-proposals.json").read_bytes()
)["proposals"]


def typed_json(value):
    # JSON spelling distinguishes booleans, integers, floats and field presence.
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)


class FrozenContracts(unittest.TestCase):
    pass


def make_test(case):
    def check(self):
        request = copy.deepcopy(case["input"])
        before = typed_json(request)
        actual = dispatch(case["operation"], request)
        self.assertEqual(typed_json(actual), typed_json(case["expected_value"]), case["id"])
        self.assertEqual(typed_json(request), before, "input mutated")
    return check


for case in CASES:
    setattr(FrozenContracts, "test_" + case["id"].replace("-", "_"), make_test(case))


if __name__ == "__main__":
    unittest.main()
