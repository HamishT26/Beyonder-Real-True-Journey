"""Planning gates. No proposal evaluator is imported or run in this phase."""
import ast, hashlib, json, unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/ilyan-reed/v685-v8/x1'
def read(n):return json.loads((BASE/n).read_text(encoding='utf8'))
class PlanningGate(unittest.TestCase):
    def test_source_is_exact_and_failure_is_preserved(self):
        s=read('activation-source.json')
        self.assertEqual(s['source'],'f5464f56d095e9c691707f669668b86ff70468a6')
        self.assertEqual(s['source_canonical_success_credit'],0)
        self.assertEqual(s['initial_activation_baseline']['effective_negatives'],64410)
        self.assertEqual(s['latest_source_working_baseline']['effective_negatives'],64412)
        self.assertEqual(s['repository_seal']['effective_negatives'],64405)
    def test_x1_is_planning_only(self):
        s=read('phase-truth.json')
        self.assertEqual(s['state'],'PLANNING_ONLY')
        self.assertIs(s['x2_execution_started'],False)
        self.assertFalse((BASE.parent/'x2').exists())
    def test_inherited_rows_have_no_credit(self):
        rows=read('inherited-selection.json')['rows']
        self.assertEqual(len(rows),200)
        self.assertTrue(all(r['execution_credit']==r['novelty_credit']==0 for r in rows))
    def test_new_contracts_have_distinct_claims_and_inputs(self):
        rows=read('new-proposals.json')['proposals']
        self.assertEqual(len(rows),200)
        self.assertEqual(len({r['proposal_id'] for r in rows}),200)
        self.assertEqual(len({r['title'] for r in rows}),200)
        self.assertEqual(Counter(r['expected_execution_disposition'] for r in rows),{'completed':170,'represented':10,'open_gap':10,'exact_gate':10})
        self.assertTrue(all(len(r['preregistered_mutations'])==5 and r['input'] and 'expected_result' in r for r in rows))
    def test_profile_and_portfolio_ranges(self):
        p=read('portfolio-plan.json');limits=read('workflow-profile.json')['plan_limits']
        for k,(low,high) in limits.items():self.assertTrue(low<=len(p[k])<=high,k)
        for k in limits:self.assertTrue(all(r['execution_credit']==0 for r in p[k]))
        self.assertEqual(Counter(r['category'] for r in p['clean_fix_refine']),{'CLEAN':100,'FIX':100,'REFINE':100})
        for k in ['exact_packets','blocked_packets']:
            self.assertTrue(all(not r['operation_executed'] for r in p[k]))
            self.assertEqual(len({r['title'] for r in p[k]}),len(p[k]))
    def test_build_and_next_owner_plans_are_bounded(self):
        p=read('skill-runner-plan.json')
        self.assertEqual(len(p['skills']),20);self.assertEqual(len(p['runners']),5)
        self.assertEqual(len(p['promotion_pairs']),10)
        self.assertEqual(len(p['next_owner_skills']),10);self.assertEqual(len(p['next_owner_runners']),10)
    def test_toolchain_is_locked_and_deferred(self):
        p=read('package-plan.json')
        self.assertEqual(sum(r['category']=='direct' for r in p['packages']),3)
        self.assertTrue(p['install_after_x1_equality'])
        self.assertTrue(all(len(r['sha256'])==64 and r['wheel'].endswith('.whl') for r in p['packages']))
    def test_route_is_single_existing_next_task(self):
        p=read('route-plan.json')
        self.assertEqual((p['next_owner'],p['next_phase']),('Neris Solane','v686-v1'))
        self.assertEqual((p['send_count'],p['subagents'],p['creation_count_this_task']),(0,0,0))
        self.assertEqual(p['delivery_state'],'PREPARED_NOT_SENT')
    def test_novelty_is_bounded_not_universal(self):
        p=read('novelty-audit.json')
        self.assertEqual(p['comparisons'],40000)
        self.assertFalse(p['universal_novelty_claimed'])
        self.assertFalse(any(r['quarantine'] or r['exact_collision'] for r in p['rows']))
    def test_practice_and_authority_boundaries(self):
        p=read('identity-and-practice.json')
        self.assertEqual(len(p['practices']),4)
        self.assertEqual(p['priority_pillar'],'THOS Body')
        self.assertIn('Māori authority',p['identity_boundary'])
        self.assertTrue(len(p['protected_gates'])>=8)
    def test_builder_syntax(self):
        ast.parse((ROOT/'scripts/build_ghc_family_ilyan_reed_v685_v8_x1.py').read_text(encoding='utf8'))
if __name__=='__main__':unittest.main()
