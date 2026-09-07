"""Current owner finite contracts and invariants; no sibling test execution."""
import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE = ROOT / 'docs/talen-briar/v687-v6'
spec = importlib.util.spec_from_file_location('talen_core', ROOT / 'scripts/ghc_family_talen_briar_v687_v6_core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
ROWS = json.loads((PHASE / 'x1/new-proposals.json').read_text('utf-8'))['new_proposals']


class CurrentOwnerContracts(unittest.TestCase):
    def test_duplicate_key_refusal(self):
        with self.assertRaises(ValueError):
            core.strict_load(b'{"x":{"a":1,"a":2}}')

    def test_nonfinite_refusal(self):
        for value in ['NaN', 'Infinity', '-Infinity', '1e999']:
            with self.assertRaises(ValueError):
                core.strict_load(('{"x":'+value+'}').encode())

    def test_unknown_operation_refusal(self):
        self.assertEqual(core.run('unknown', {})['reason'], 'UNKNOWN_OPERATION')

    def test_undeclared_fields_refused(self):
        row = ROWS[0]
        payload = dict(row['input'], authority=True)
        self.assertEqual(core.run(row['operation'], payload)['reason'], 'INPUT_SHAPE')

    def test_complete_oracle_has_type_and_field_sensitivity(self):
        self.assertFalse(core.type_equal(True, 1))
        self.assertFalse(core.type_equal(1, 1.0))
        self.assertFalse(core.type_equal({'a': None}, {}))
        self.assertFalse(core.type_equal({'a': 1}, {'a': 1, 'authority': True}))

    def test_input_budget_refusal(self):
        with self.assertRaises(ValueError):
            core.strict_load(b' ' * 2097153)


def operation_test(operation):
    def check(self):
        selected = [r for r in ROWS if r['operation'] == operation]
        self.assertEqual(len(selected), 20)
        for row in selected:
            with self.subTest(proposal=row['proposal_id']):
                payload = copy.deepcopy(row['input'])
                actual = core.run(operation, payload)
                self.assertTrue(core.type_equal(actual, row['expected_output']), row['proposal_id'])
                self.assertTrue(core.type_equal(payload, row['input']))
                self.assertFalse(actual['external_credit'])
    return check


for operation in sorted({r['operation'] for r in ROWS}):
    setattr(CurrentOwnerContracts, 'test_contract_'+operation, operation_test(operation))

if __name__ == '__main__':
    unittest.main()
