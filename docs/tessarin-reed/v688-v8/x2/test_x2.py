import copy
import json
import pathlib
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'code'))
from ghc_family_dfa_core import OPS, evaluate, strict_load, ProfileError

CONTRACTS = json.loads((ROOT.parent / 'x1/new-proposals.json').read_text())['proposals']

class FiniteTables(unittest.TestCase):
    def test_partial_complement_is_refused(self):
        request = copy.deepcopy(CONTRACTS[40]['input'])
        del request['machine']['transitions']['q0']['a']
        self.assertFalse(evaluate(request)['accepted'])

    def test_duplicate_json_is_refused(self):
        with self.assertRaises(ProfileError):
            strict_load('{"op":"dfa_run","op":"dfa_shape"}')

    def test_budgets_and_boolean_counts(self):
        request = copy.deepcopy(CONTRACTS[50]['input'])
        for length in [True, -1, 129, 1.5]:
            request['length'] = length
            self.assertFalse(evaluate(request)['accepted'])
        request = copy.deepcopy(CONTRACTS[60]['input'])
        request['max_length'] = 9
        self.assertFalse(evaluate(request)['accepted'])

    def test_authority_request_cannot_execute(self):
        request = copy.deepcopy(CONTRACTS[190]['input'])
        request['requested'] = True
        response = evaluate(request)
        self.assertFalse(response['accepted'])
        self.assertEqual(response['boundary']['external_actions'], 0)

def family_test(op):
    def test(self):
        for contract in CONTRACTS:
            if contract['input']['op'] != op:
                continue
            with self.subTest(proposal=contract['proposal_id']):
                request = copy.deepcopy(contract['input'])
                self.assertEqual(evaluate(request), contract['expected'])
                self.assertEqual(request, contract['input'])
    return test

for operation in OPS:
    setattr(FiniteTables, 'test_' + operation, family_test(operation))

if __name__ == '__main__':
    unittest.main()
