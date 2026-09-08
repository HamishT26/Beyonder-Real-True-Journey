"""Check prospective definitions and exact mathematical oracles without importing implementations."""
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'docs/seren-talewood/v689-v2-r2/plan'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

class PlanContract(unittest.TestCase):
    def test_confirmed_route_has_no_skips_or_duplicate_slots(self):
        route=load(ROOT/'workflow/thirty-seat-schedule.json')
        self.assertTrue(route['user_confirmed_normalization'])
        self.assertEqual(len(set(route['cycle'])),30)
        rows=route['assignments']
        self.assertEqual(len(rows),294)
        self.assertEqual((rows[0]['phase'],rows[0]['owner']),('v689-v3','Eiren Kestrel'))
        self.assertEqual((rows[29]['phase'],rows[29]['owner']),('v692-v8','Seren Talewood'))
        self.assertEqual((rows[31]['phase'],rows[31]['owner']),('v693-v2','Rowan Ash'))
        self.assertEqual((rows[-1]['phase'],rows[-1]['owner']),('v725-v8','Orren Pike'))
        self.assertEqual(len({r['phase'] for r in rows}),294)

    def test_blank_root_preserves_provenance_without_false_ancestry(self):
        p=load(PLAN/'source-provenance.json')
        self.assertFalse(p['git_ancestry_claimed'] or p['source_replayed'])
        self.assertTrue(p['prior_hold_preserved'] and p['source_four_way_equal'])
        self.assertEqual(p['source_commit'],'7034e1721b29bd46e10e2a467e79a114f31b5885')

    def test_two_hundred_distinct_contracts_are_prospective(self):
        data=load(PLAN/'new-proposals.json')
        rows=data['proposals']
        self.assertEqual(len(rows),200)
        self.assertEqual(len({r['input_sha256'] for r in rows}),200)
        self.assertEqual(len({r['proposal_id'] for r in rows}),200)
        self.assertTrue(all(r['outcomes_observed'] is False for r in rows))
        for r in rows:
            self.assertEqual(set(r['expected']),{'ok','value','error'})
            self.assertEqual(type(r['expected']['ok']),bool)
        self.assertEqual(sum(r['stage']=='x1' for r in rows),100)
        self.assertEqual(sum(r['stage']=='x2' for r in rows),100)

    def test_operation_shapes_match_the_frozen_inputs(self):
        specs=load(PLAN/'operation-contracts.json')
        self.assertEqual(len(specs),40)
        fields={r['op']:set(r['required_fields'])|{'op'} for r in specs}
        for r in load(PLAN/'new-proposals.json')['proposals']:
            self.assertEqual(set(r['input']),fields[r['input']['op']])

    def test_frozen_unit_fraction_witnesses_have_exact_residuals(self):
        for r in load(PLAN/'new-proposals.json')['proposals']:
            if r['input']['op']!='egyptian_fraction_verify' or not r['expected']['ok']:
                continue
            data=r['input'];expected=r['expected']['value']
            residual=Fraction(4,data['n'])-sum(Fraction(1,x) for x in data['denominators'])
            self.assertEqual(residual,Fraction(expected['residual']))
            self.assertEqual(residual==0,expected['valid'])

    def test_stationarity_oracles_satisfy_their_linear_equations(self):
        for r in load(PLAN/'new-proposals.json')['proposals']:
            if r['input']['op']!='stationary_distribution' or not r['expected']['ok']:
                continue
            matrix=[[Fraction(v) for v in row] for row in r['input']['matrix']]
            pi=[Fraction(v) for v in r['expected']['value']]
            self.assertEqual(sum(pi),1)
            self.assertEqual([sum(pi[i]*matrix[i][j] for i in range(len(pi))) for j in range(len(pi))],pi)

    def test_review_window_and_selected_inherited_records_are_separate(self):
        sources=load(PLAN/'prior-fifteen-sources.json')
        inherited=load(PLAN/'inherited-selections.json')
        self.assertEqual(len(sources['records']),15)
        self.assertTrue(all(r['files'] and r['overview_words'] for r in sources['records']))
        self.assertFalse(sources['source_tests_executed'])
        self.assertEqual(len(inherited['selections']),200)
        self.assertEqual(len({r['source_id'] for r in inherited['selections']}),200)
        self.assertTrue(all(r['execution_credit']==r['novelty_credit']==0 for r in inherited['selections']))

    def test_spontaneous_capacity_is_not_execution(self):
        portfolio=load(PLAN/'approval-portfolio.json')
        reserved=[r for r in portfolio['safe'] if r['kind']=='spontaneous_capacity_reservation']
        self.assertEqual(len(reserved),40)
        self.assertTrue(all(r['execution_credit']==0 and r['contract_required_before_execution'] for r in reserved))
        self.assertEqual(len(portfolio['candidates']),100)
        self.assertTrue(all(r['expected']=={'ok':False,'value':None,'error':'schema'} for r in portfolio['candidates']))

    def test_exact_packets_are_concrete_and_blocked_subjects_unexecuted(self):
        p=load(PLAN/'approval-portfolio.json')
        self.assertEqual(len(p['exact']),50)
        self.assertEqual(len({(r['action'],r['target']) for r in p['exact']}),50)
        self.assertEqual(p['exact'][-1]['target'],'Eiren Kestrel')
        self.assertEqual(p['exact'][-1]['stage'],'terminal')
        self.assertEqual(len(p['blocked']),30)
        self.assertTrue(all(r['executed'] is False and r['success_credit']==0 for r in p['blocked']))

    def test_package_closure_and_rejected_candidate_are_explicit(self):
        p=load(PLAN/'package-plan.json')
        r=load(PLAN/'package-review-before-install.json')
        self.assertEqual(len(p['packages']),16)
        self.assertEqual(sum(x['role']=='direct_new' for x in p['packages']),13)
        self.assertNotIn('z3-solver',[x['name'] for x in p['packages']])
        self.assertIn('dictdiffer',[x['name'] for x in p['packages']])
        self.assertTrue(all(x['hash_matched'] and x['licenses'] and not x['code_executed'] for x in r['packages']))
        self.assertFalse(r['installed'] or r['full_security_claim'])

    def test_limits_and_tool_targets_follow_new_authority(self):
        profile=load(ROOT/'workflow/current-workflow.json')
        limits=profile['limits'];targets=profile['phase_targets']
        for key in ['inherited_proposals','new_proposals','safe_now_x1','safe_now_x2','candidate_x2','clean_fix_refine_x1','clean_fix_refine_x2','skills_x1','skills_x2','runners_x1','runners_x2']:
            low,high=limits[key]
            self.assertLessEqual(low,targets[key]);self.assertLessEqual(targets[key],high)
        self.assertEqual((limits['own_practices'],limits['next_practices']),(4,1))
        self.assertEqual((limits['web_searches_x1_maximum'],limits['web_searches_x2_maximum']),(500,500))
        tools=load(PLAN/'tool-build-plan.json')
        self.assertEqual((len(tools['skills']),len(tools['runners'])),(20,10))

    def test_no_canonical_or_delivery_is_preclaimed(self):
        history=load(PLAN/'retained-intake-events.json')
        self.assertEqual(history['canonical_invocations'],0)
        self.assertEqual(history['successor_messages'],0)
        self.assertFalse(history['source_canonical_replayed'])
        self.assertTrue(all(r['original_success_credit']==0 for r in history['events']))
        self.assertEqual(load(PLAN/'workflow-audit-receipt.json')['receipts'][1]['exit_code'],0)

if __name__=='__main__':unittest.main()
