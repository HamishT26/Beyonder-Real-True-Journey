"""Frozen x1 expectations plus cross-contract behavior; same-owner validation."""
import copy
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ghc_family_contract_oracle as core

SOURCE = 'e85af4eea2aed7f98d2dfec936f26a8e175fba44'
X1 = '9012ca9b7d7ed583d09267ebfa0ef271b1087706'
PLAN_PATH = 'docs/saelin-reed/v686-v8/x1/new-proposals.json'
DEFINITIONS = core.strict_loads(subprocess.check_output(['git', '-C', str(ROOT), 'show', X1 + ':' + PLAN_PATH]))['proposals']
MODULES = [importlib.import_module('ghc_family_' + suffix) for suffix in
           ('contract_oracle', 'disposition_audit', 'witness_pairing', 'claim_coverage', 'event_projection')]
OPERATIONS = {name: fn for module in MODULES for name, fn in module.OPERATIONS.items()}


class FrozenCase(unittest.TestCase):
    def __init__(self, definition):
        super().__init__('runTest')
        self.definition = definition

    def id(self):
        return 'frozen.' + self.definition['id']

    def shortDescription(self):
        return self.definition['title']

    def runTest(self):
        payload = copy.deepcopy(self.definition['input'])
        before = core.json_bytes(payload)
        observed = core.evaluate(OPERATIONS, self.definition['operation'], payload)
        self.assertTrue(core.same(observed, self.definition['expected_value']),
                        self.definition['id'] + ': expected ' + repr(self.definition['expected_value']) + ' observed ' + repr(observed))
        self.assertEqual(core.json_bytes(payload), before, 'Input was mutated')


class CrossContractTests(unittest.TestCase):
    def test_duplicate_json_keys_refused(self):
        with self.assertRaisesRegex(core.ContractError, 'DUPLICATE_JSON_KEY'):
            core.strict_loads('{"x":1,"x":2}')

    def test_all_nonfinite_json_forms_refused(self):
        for text in ('NaN', 'Infinity', '-Infinity', '1e999'):
            with self.subTest(text=text), self.assertRaisesRegex(core.ContractError, 'NONFINITE_JSON'):
                core.strict_loads(text)

    def test_frozen_plan_is_unchanged(self):
        self.assertEqual((ROOT / PLAN_PATH).read_bytes(), subprocess.check_output(['git', '-C', str(ROOT), 'show', X1 + ':' + PLAN_PATH]))

    def test_every_report_binding_rejects_substitution(self):
        definition = DEFINITIONS[0]
        report = core.make_report(definition, definition['expected_value'], SOURCE, X1)
        for field in report:
            wrong = copy.deepcopy(report)
            wrong[field] = {'substituted': True}
            self.assertFalse(core.verify_report(definition, wrong, SOURCE, X1), field)

    def test_honest_failure_report_is_not_completion(self):
        definition = DEFINITIONS[0]
        report = core.make_report(definition, False, SOURCE, X1)
        self.assertTrue(core.verify_report(definition, report, SOURCE, X1))
        self.assertFalse(report['expectation_met'])
        self.assertEqual(report['disposition'], 'open_gap')

    def test_jcs_bytes_do_not_replace_typed_equality(self):
        self.assertFalse(core.typed_equal([1, 1.0]))
        self.assertEqual(core.jcs_payload(1), core.jcs_payload(1.0))

    def test_depth_limit_is_explicit(self):
        value = 0
        for _ in range(65):
            value = [value]
        with self.assertRaisesRegex(core.ContractError, 'JSON_DEPTH_LIMIT'):
            core.finite_json(value)

    def test_unknown_graph_nodes_are_not_created(self):
        value = {'nodes': ['a'], 'edges': [['a', 'missing']]}
        original = copy.deepcopy(value)
        self.assertEqual(core.evaluate(OPERATIONS, 'acyclic_order', value), {'error': 'UNKNOWN_NODE'})
        self.assertEqual(value, original)

    def test_numeric_terminal_flags_never_authorize(self):
        module = MODULES[-1]
        value = {key: 1 for key in module.TERMINAL_FLAGS}
        result = module.terminal_preconditions(value)
        self.assertEqual(result['decision'], 'held')
        self.assertFalse(result['send_performed'])
        self.assertEqual(len(result['missing']), 10)

    def test_cli_refuses_output_overwrite(self):
        scratch = Path(os.environ['SAELIN_TEST_ARTIFACTS'])
        scratch.mkdir(parents=True, exist_ok=True)
        incoming, outgoing = scratch / 'cli-input.json', scratch / 'cli-existing.json'
        incoming.write_text('{"ok":true,"value":1}', encoding='utf-8')
        if not outgoing.exists():
            outgoing.write_bytes(b'RETAINED')
        before = outgoing.read_bytes()
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/ghc_family_contract_oracle.py'),
                               '--operation', 'result_envelope', '--input', str(incoming), '--output', str(outgoing)], capture_output=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(outgoing.read_bytes(), before)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite(FrozenCase(row) for row in DEFINITIONS)
    suite.addTests(loader.loadTestsFromTestCase(CrossContractTests))
    return suite


if __name__ == '__main__':
    unittest.main()
