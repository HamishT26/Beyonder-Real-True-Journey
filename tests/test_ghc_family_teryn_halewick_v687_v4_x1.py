"""Planning-only invariants. Run at the planning tree; later stages replay its manifest."""
import collections
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/teryn-halewick/v687-v4/x1'

def load(name):
    return json.loads((BASE/name).read_text(encoding='utf8'))

class PlanningContract(unittest.TestCase):
    def test_no_execution_credit(self):
        truth=load('phase-truth.json')
        self.assertEqual(truth['state'],'X1_PLANNING_ONLY')
        for key in ['implemented_contracts','built_skills','built_runners','installed_direct_packages','canonical_invocations','canonical_successes']:
            self.assertEqual(truth[key],0)
    def test_independent_contract_inventory(self):
        rows=load('new-proposals.json')['proposals']
        self.assertEqual(len(rows),200)
        self.assertEqual(len({r['id'] for r in rows}),200)
        self.assertEqual(len({json.dumps([r['operation'],r['input']],sort_keys=True) for r in rows}),200)
        self.assertEqual(set(collections.Counter(r['operation'] for r in rows).values()),{20})
        for r in rows:
            self.assertTrue(r['planning_only'])
            self.assertEqual(r['inherited_execution_credit'],0)
            self.assertEqual(len(r['mutations']),5)
            self.assertEqual(set(r['expected_output']),{'decision','result','source_preserved','external_credit'})
    def test_inherited_zero_credit(self):
        r=load('inherited-review.json')
        self.assertEqual(len(r['rows']),200)
        self.assertTrue(all(x['new_owner_credit']==0 for x in r['rows']))
    def test_portfolio_ranges_and_unique_ids(self):
        r=load('portfolio-plan.json')
        for name,size in [('safe',300),('candidates',250),('clean_fix_refine',300),('exact_packets',50),('blocked_packets',30)]:
            self.assertEqual(len(r[name]),size)
            self.assertEqual(len({x['id'] for x in r[name]}),size)
        self.assertTrue(all(not x['executed'] for x in r['exact_packets']+r['blocked_packets']))
    def test_package_closure_frozen_without_installation(self):
        p=load('package-plan.json')
        self.assertEqual(sum(x['direct'] for x in p['packages']),3)
        self.assertEqual(len(p['packages']),8)
        self.assertEqual(p['installation_credit_in_x1'],0)
        for x in p['packages']:
            self.assertEqual(len(x['sha256']),64)
            self.assertTrue(x['url'].startswith('https://files.pythonhosted.org/'))
    def test_skills_and_practices_are_planned(self):
        p=load('skill-runner-plan.json')
        self.assertEqual(len(p['skills']),10)
        self.assertEqual(len(p['runners']),10)
        self.assertTrue(all(not x['built'] for x in p['skills']+p['runners']))
        self.assertEqual(len(load('identity.json')['practices']),4)
    def test_terminal_boundary(self):
        r=load('route-plan.json')
        self.assertEqual((r['next_owner'],r['next_phase']),('Caelen Ash','v687-v5'))
        self.assertEqual(r['message_count'],0)
        self.assertEqual(r['state'],'PREPARED_NOT_SENT')
        self.assertEqual(r['terminal_verdict'],'NOT_READY_FOR_STAGE_20')
    def test_overview_has_substantive_three_page_equivalent(self):
        text=(BASE/'integrated-overview.md').read_text(encoding='utf8')
        self.assertGreaterEqual(len(text.split()),1500)
    def test_startup_failure_nonerasure(self):
        ledger=load('method-flow/ledger.json')
        self.assertEqual(len(ledger['methods']),8)
        self.assertEqual(len(ledger['witnesses']),16)

if __name__=='__main__': unittest.main()
