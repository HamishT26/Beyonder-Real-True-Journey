"""Validate the immutable planning contract, without executing x2 behavior."""
import collections
import hashlib
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = 'ac9f049a165005776a2aec4c451e654c3d08013b'

def load(name): return json.loads((ROOT / name).read_text(encoding='utf-8'))
def digest(value): return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()

class PlanningContract(unittest.TestCase):
    def setUp(self):
        self.freeze = load('new-proposals.json')
        self.rows = self.freeze['proposals']
        self.portfolio = load('approval-portfolio.json')

    def test_source_and_planning_boundary(self):
        self.assertEqual(self.freeze['source'], SOURCE)
        self.assertIs(self.freeze['planning_only'], True)
        self.assertIs(self.freeze['outcomes_observed'], False)
        self.assertEqual(load('phase-truth.json')['canonical_invocations'], 0)
        self.assertEqual(load('package-capability-plan.json')['exact_packages_selected'], [])
        self.assertFalse((ROOT.parent / 'x2').exists())

    def test_two_hundred_unique_new_contracts(self):
        self.assertEqual(len(self.rows), 200)
        for field in ['proposal_id', 'title']:
            self.assertEqual(len({row[field] for row in self.rows}), 200)
        self.assertEqual(len({digest(row['input']) for row in self.rows}), 200)

    def test_complete_contract_fields(self):
        required = {'proposal_id', 'title', 'input', 'expected', 'expected_execution_disposition',
                    'pillar', 'practice', 'approval_class', 'execution_lane', 'hypothesis',
                    'null_or_failure_condition', 'falsifier', 'acceptance', 'source_need',
                    'artifact', 'rollback_recovery', 'protected_gates', 'novelty_scope'}
        for row in self.rows:
            self.assertEqual(set(row), required)
            self.assertEqual(row['execution_lane'], 'x2_build_task')
            self.assertEqual(set(row['expected']), {'accepted', 'error', 'value', 'disposition', 'boundary'})
            self.assertEqual(row['expected_execution_disposition'], row['expected']['disposition'])
            self.assertIs(row['expected']['boundary']['authority_granted'], False)

    def test_inherited_selections_have_zero_credit(self):
        data = load('inherited-proposals.json')
        self.assertEqual(data['source'], SOURCE)
        self.assertEqual(len(data['selections']), 200)
        self.assertEqual(len({r['source_id'] for r in data['selections']}), 200)
        for row in data['selections']:
            self.assertEqual(row['novelty_credit'], 0)
            self.assertEqual(row['execution_credit'], 0)
            self.assertTrue(row['source_id'].startswith('CM6891-N'))

    def test_release_portfolio_ranges_and_ids(self):
        profile = load('workflow-profile.json')
        identifiers = []
        for key, (low, high) in profile['plan_limits'].items():
            rows = self.portfolio[key]
            self.assertLessEqual(low, len(rows))
            self.assertLessEqual(len(rows), high)
            identifiers += [r.get('task_id', r.get('packet_id')) for r in rows]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertFalse(self.portfolio['destructive_cleanup_planned'])
        self.assertEqual(collections.Counter(r['category'] for r in self.portfolio['clean_fix_refine']),
                         {'CLEAN': 100, 'FIX': 100, 'REFINE': 100})

    def test_portfolio_proposal_bindings_and_reservations(self):
        identifiers = {r['proposal_id'] for r in self.rows}
        for group in ['safe_now', 'candidates', 'clean_fix_refine']:
            for row in self.portfolio[group]:
                self.assertIn(row['proposal_id'], identifiers)
                self.assertEqual(row['execution_credit_at_x1'], 0)
        for group in ['exact_packets', 'blocked_packets']:
            for row in self.portfolio[group]:
                self.assertIs(row['executed'], False)
                self.assertEqual(row['expected_execution_disposition'], 'exact_gate')

    def test_request_profile_and_grammar_fixtures(self):
        profile = load('formal-profile.json')
        self.assertEqual(len(profile['operation_fields']), 20)
        self.assertEqual(len(load('grammar-fixtures.json')['grammars']), 10)
        for row in self.rows:
            self.assertEqual(sorted(row['input']), profile['operation_fields'][row['input']['op']])
        self.assertEqual(profile['end_marker'], '$')
        self.assertTrue(profile['first_excludes_epsilon'])
        self.assertEqual(profile['limits']['explored_derivation_nodes'], 10000)

    def test_explicit_expected_edge_distinctions(self):
        by_id = {r['proposal_id']: r for r in self.rows}
        self.assertEqual(by_id['ST6892-N011']['expected']['value'], {'nullable': []})
        self.assertEqual(by_id['ST6892-N012']['expected']['value'], {'nullable': ['S']})
        self.assertEqual(by_id['ST6892-N100']['expected']['value'], {'left_recursive': ['S', 'U']})
        self.assertFalse(by_id['ST6892-N141']['expected']['value']['complete'])
        self.assertEqual(by_id['ST6892-N170']['expected']['value']['counts']['aaa'], 2)
        self.assertEqual(collections.Counter(r['expected_execution_disposition'] for r in self.rows),
                         {'completed': 190, 'represented': 10})

    def test_four_practices_and_additive_tools(self):
        identity = load('identity-and-practices.json')
        self.assertEqual(identity['owner'], 'Seren Talewood')
        self.assertEqual(len(identity['practices']), 4)
        self.assertEqual(len({p['pillar'] for p in identity['practices']}), 3)
        tools = load('tool-plan.json')
        self.assertEqual(len(tools['skills']), 10)
        self.assertEqual(len(tools['runners']), 5)
        self.assertEqual(len(load('next-owner-ideas.json')['skills']), 10)
        self.assertEqual(len(load('next-owner-ideas.json')['runners']), 10)
        for skill in tools['skills']: self.assertTrue(skill['name'].startswith('ghc-family-'))
        for runner in tools['runners']: self.assertTrue(runner['name'].startswith('ghc_family_'))

    def test_route_and_lifecycle_are_prospective(self):
        route = load('route-freeze.json')
        self.assertEqual((route['owner'], route['phase']), ('Seren Talewood', 'v689-v2'))
        self.assertEqual((route['next_owner'], route['next_phase']), ('Eiren Kestrel', 'v689-v3'))
        self.assertEqual(route['successor_contacts'], 0)
        self.assertFalse(route['resend_or_substitution_authorized'])
        self.assertFalse(route['successor_activation_authorized'])
        self.assertTrue(route['wait_for_hamish_after_closeout'])
        self.assertEqual(len(route['user_supplied_roster']), 30)
        self.assertEqual(load('lifecycle-plan.json')['planned_commits'], 3)
        self.assertEqual(load('lifecycle-plan.json')['commit_ceiling'], 8)
        self.assertFalse(load('lifecycle-plan.json')['full_repository_suite'])

    def test_source_audit_coverage_and_corpus(self):
        audit = load('source-audit.json')
        self.assertTrue(audit['ready_for_bounded_planning'])
        self.assertFalse(audit['canonical_chain_mapping_complete'])
        self.assertEqual(audit['declared_chain'], 17230)
        self.assertEqual(audit['root']['declared_pre_root_baseline'], 4550)
        self.assertEqual(load('novelty-review.json')['exact_collisions'], [])
        index = load('source-corpus-index.json')
        count = 0
        for path in index['shards']:
            relative = path.split('/x1/', 1)[1]
            count += len(load(relative)['records'])
        self.assertEqual(count, index['records'])

    def test_source_seal_overlay_and_retained_failures(self):
        baseline = load('activation-baseline.json')
        self.assertEqual(baseline['repository_sealed']['negatives'], 86292)
        self.assertEqual(baseline['activation_baseline']['negatives'], 86293)
        self.assertFalse(baseline['source_canonical_replayed'])
        methods = load('method-flow-startup.json')
        self.assertTrue(methods['methods'])
        negative_ids = {n for m in methods['methods'] for n in m['retained_negative_ids']}
        failed = [w for w in methods['witnesses'] if w['result'] == 'fail']
        self.assertEqual({n for w in failed for n in w['retained_negative_ids']}, negative_ids)
        self.assertFalse(any(w['independent_reproduction'] for w in methods['witnesses']))
        self.assertEqual(load('reading-receipt.json')['baton']['words'], 55488)
        self.assertTrue(load('reading-receipt.json')['baton']['read_through_eof'])

if __name__ == '__main__': unittest.main()
