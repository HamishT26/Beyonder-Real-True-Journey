import copy
import json
import pathlib
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))
from ghc_family_nfa_core import OPS, evaluate

CONTRACTS = json.loads((ROOT.parent / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]


class NondeterministicTables(unittest.TestCase):
    def test_unknown_field_is_refused(self):
        request = copy.deepcopy(CONTRACTS[0]["input"])
        request["unexpected"] = True
        self.assertEqual(evaluate(request)["error"], "fields")

    def test_enumeration_bounds_and_boolean_counts(self):
        word_count = copy.deepcopy(next(row["input"] for row in CONTRACTS if row["input"]["op"] == "nfa_word_count"))
        for value in [True, -1, 9, 1.5]:
            request = copy.deepcopy(word_count)
            request["length"] = value
            self.assertFalse(evaluate(request)["accepted"])
        words = copy.deepcopy(next(row["input"] for row in CONTRACTS if row["input"]["op"] == "nfa_words"))
        words["max_length"] = 9
        self.assertFalse(evaluate(words)["accepted"])

    def test_requested_authority_cannot_execute(self):
        request = copy.deepcopy(next(row["input"] for row in CONTRACTS if row["input"]["op"] == "nfa_authority_reservation"))
        request["requested"] = True
        response = evaluate(request)
        self.assertFalse(response["accepted"])
        self.assertEqual(response["error"], "authority")
        self.assertEqual(response["boundary"]["external_actions"], 0)

    def test_malformed_regex_is_refused(self):
        request = copy.deepcopy(next(row["input"] for row in CONTRACTS if row["input"]["op"] == "regex_membership"))
        request["pattern"] = "(unclosed"
        self.assertEqual(evaluate(request)["error"], "invalid")


def family_test(operation):
    def test(self):
        for contract in CONTRACTS:
            if contract["input"]["op"] != operation:
                continue
            with self.subTest(proposal=contract["proposal_id"]):
                request = copy.deepcopy(contract["input"])
                self.assertEqual(evaluate(request), contract["expected"])
                self.assertEqual(request, contract["input"])

    return test


for operation in OPS:
    setattr(NondeterministicTables, "test_" + operation, family_test(operation))


if __name__ == "__main__":
    unittest.main()
