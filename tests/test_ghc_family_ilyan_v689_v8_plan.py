"""Verify frozen planning fields, not production evaluator outcomes."""
import hashlib,json,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v689-v8/plan'
def read(n):return json.loads((BASE/n).read_text(encoding='utf8'))
class Planning(unittest.TestCase):
    def test_proposal_inventory(self):
        p=read('new-proposals.json');r=p['proposals'];self.assertTrue(p['planning_only']);self.assertFalse(p['production_evaluator_executed']);self.assertEqual(len(r),200);self.assertEqual(len({x['proposal_id'] for x in r}),200);self.assertEqual(Counter(x['lane'] for x in r),{'x1':100,'x2':100})
    def test_expected_dispositions(self):self.assertEqual(Counter(x['expected_execution_disposition'] for x in read('new-proposals.json')['proposals']),{'completed':180,'represented':10,'open_gap':5,'exact_gate':5})
    def test_candidate_subjects_preserved(self):
        for r in read('new-proposals.json')['proposals']:
            self.assertIn('unreviewed_authority_grant',r['candidate_subject']['payload']);self.assertEqual(r['candidate_expected']['original_success_credit'],0)
    def test_saturation_starts_within_capacity(self):
        for r in read('new-proposals.json')['proposals']:
            if r['operation']=='saturation_hold':self.assertTrue(all(0<=x<=r['request']['payload']['cap'] for x in r['request']['payload']['counts']))
    def test_portfolio_is_defined_for_each_session(self):
        for lane in ['x1','x2']:
            p=read('portfolio-'+lane+'.json')
            for k in ['safe','candidate','clean_fix_refine']:self.assertEqual(len(p[k]),100)
            self.assertTrue(all(not r['host_cleanup'] for r in p['clean_fix_refine']))
        self.assertEqual(len(read('additional-work.json')['x2_safe_defined_before_execution']),5)
    def test_inherited_credit_is_zero(self):self.assertTrue(all(x['novelty_credit']==x['execution_credit']==0 for x in read('inherited-selections.json')['rows']))
    def test_source_layers_and_blank_root_are_explicit(self):
        s=read('source-provenance.json');self.assertFalse(s['source_is_ancestor']);self.assertEqual((s['source_repository_negatives'],s['initial_external_negatives'],s['latest_external_negatives']),(511,518,524));self.assertEqual(s['complete_read']['words'],31304)
    def test_route_is_current_and_unsubmitted(self):
        r=read('route.json');self.assertEqual((r['next_owner'],r['next_phase']),('Lyren Moss','v690-v1'));self.assertFalse(r['task_creation']);self.assertFalse(r['subagents']);self.assertEqual(r['send_limit'],1);self.assertTrue(r['opaque_acceptance_ends_retries'])
    def test_skill_runner_bounds(self):
        r=read('skills-runners.json');self.assertEqual(len(r['skills']),20);self.assertEqual(len(r['runners']),10);self.assertEqual(len(r['global_groups']),5)
    def test_locked_three_direct_packages(self):
        p=read('package-plan.json');self.assertEqual(sum(x['category']=='direct' for x in p['packages']),3);self.assertTrue(all(len(x['sha256'])==64 for x in p['packages']));self.assertEqual(p['direct_additions'],3)
    def test_reviewed_overviews_and_practices(self):
        self.assertEqual(len(read('recent-overview-review.json')['records']),10);p=read('identity-practices.json');self.assertEqual(len(p['practices']),4);self.assertEqual(len(p['next_practices']),2)
    def test_novelty_scope(self):
        p=read('novelty-review.json');self.assertFalse(p['universal_novelty']);self.assertFalse(any(r['quarantine'] or r['exact_collision'] for r in p['rows']))
if __name__=='__main__':unittest.main()
