"""Planning-contract checks; run against the immutable x1 blob snapshot later."""
import json
import math
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE = ROOT / 'docs/talen-briar/v687-v6'
LABELS = {'completed', 'represented', 'open_gap', 'exact_gate'}

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result

def forbidden(value):
    raise ValueError('Nonfinite JSON constant')

def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('Nonfinite JSON number')
    return number

def read(name):
    return json.loads((PHASE / 'x1' / name).read_text('utf-8'),
                      object_pairs_hook=unique, parse_constant=forbidden, parse_float=finite_float)

class PlanningContract(unittest.TestCase):
    def test_source_baseline(self):
        s = read('source-verification.json')
        self.assertEqual(s['source'], 'f815c68a704065970717f8d88305489a0966cd9c')
        self.assertEqual(s['source_manifest_bindings'], 821)
        self.assertEqual(s['source_manifest_mismatches'], 0)
        self.assertFalse(s['canonical_rerun_by_talen'])
        self.assertEqual(s['activation_baseline_counts']['proposals'], 14830)

    def test_inherited_credit(self):
        rows = read('inherited-review.json')['rows']
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({r['inherited_id'] for r in rows}), 200)
        self.assertTrue(all(r['new_owner_credit'] == r['execution_credit'] == 0 for r in rows))

    def test_finite_contracts(self):
        rows = read('new-proposals.json')['new_proposals']
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({r['proposal_id'] for r in rows}), 200)
        self.assertEqual(len({(r['operation'], json.dumps(r['input'], sort_keys=True)) for r in rows}), 200)
        required = {'hypothesis', 'null_or_failure_condition', 'approval_class', 'execution_lane',
                    'source_needs', 'artifacts', 'acceptance_gate', 'rollback', 'protected_gates'}
        for r in rows:
            self.assertTrue(required <= set(r))
            self.assertIn(r['expected_execution_disposition'], LABELS)
            self.assertFalse(r['implementation_in_x1'])
            self.assertFalse(r['expected_output']['external_credit'])
            self.assertTrue(r['expected_output']['source_preserved'])

    def test_prospective_state(self):
        p = read('phase-truth.json')
        self.assertEqual(p['state'], 'PLANNING_ONLY_X1')
        self.assertFalse(p['x2_implementation'])
        self.assertEqual(p['installed_packages'], 0)
        self.assertEqual(p['canonical_invocations'], 0)
        self.assertEqual(p['successor_messages'], 0)

    def test_portfolio(self):
        p = read('portfolio-plan.json')
        expected = dict(safe_now=300, candidates=250, clean_fix_refine=300, exact_packets=50, blocked_packets=30)
        self.assertEqual(p['counts'], expected)
        for name, count in expected.items():
            rows = p['portfolios'][name]
            self.assertEqual(len(rows), count)
            self.assertEqual(len({r['packet_id'] for r in rows}), count)
            self.assertTrue(all(not r['executed'] for r in rows))

    def test_skill_runner_practices(self):
        p = read('skill-runner-plan.json')
        self.assertEqual(len(p['skills']), 10)
        self.assertEqual(len(p['runners']), 10)
        self.assertEqual(len(set(r['name'] for r in p['skills'])), 10)
        self.assertEqual(p['global_promotions']['shared_runners'], 5)
        self.assertEqual(len(read('identity.json')['practices']), 4)
        self.assertEqual(len(read('successor-ideas.json')['skill_ideas']), 10)
        self.assertEqual(len(read('successor-ideas.json')['runner_ideas']), 10)

    def test_packages_not_installed(self):
        p = read('package-plan.json')
        self.assertTrue(p['planning_only'])
        self.assertEqual(p['installation_credit'], 0)
        self.assertEqual(sum(x['phase_addition'] for x in p['packages']), 3)
        self.assertTrue(all(len(x['sha256']) == 64 and x['wheel'].endswith('.whl') for x in p['packages']))
        self.assertEqual(next(x['version'] for x in p['packages'] if x['name'] == 'mpmath'), '1.3.0')

    def test_routes(self):
        p = read('route-plan.json')
        self.assertEqual((p['next_owner'], p['next_phase']), ('Orin Thale', 'v687-v7'))
        self.assertEqual(p['message_count'], 0)
        self.assertEqual(p['created_tasks'], 0)
        self.assertEqual(p['subagents'], 0)
        self.assertEqual(p['terminal_verdict'], 'NOT_READY_FOR_STAGE_20')

    def test_json_and_document_limits(self):
        for p in (PHASE / 'x1').rglob('*'):
            if p.is_file():
                text = p.read_text('utf-8')
                self.assertLessEqual(len(text.split()), 100000, str(p.name))
                if p.suffix == '.json':
                    json.loads(text, object_pairs_hook=unique, parse_constant=forbidden, parse_float=finite_float)

    def test_json_refuses_ambiguous_values(self):
        for text in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}', '{"a":1e999}']:
            with self.assertRaises(ValueError):
                json.loads(text, object_pairs_hook=unique, parse_constant=forbidden, parse_float=finite_float)

    def test_retained_failures(self):
        p = read('method-flow/ledger.json')
        self.assertTrue(all(m['retained_negative_ids'] for m in p['methods']))
        for m in p['methods']:
            results = {w['result'] for w in p['witnesses'] if w['method_id'] == m['method_id']}
            self.assertEqual(results, {'pass', 'fail'})

if __name__ == '__main__':
    unittest.main()
