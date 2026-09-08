import json,pathlib,unittest
R=pathlib.Path(__file__).resolve().parent
def load(n): return json.loads((R/n).read_text(encoding='utf-8'))
class Plan(unittest.TestCase):
 def test_counts(self): self.assertEqual(len(load('new-proposals.json')['proposals']),200)
 def test_unique(self): self.assertEqual(len({r['proposal_id'] for r in load('new-proposals.json')['proposals']}),200)
 def test_prior_zero(self): self.assertEqual(load('inherited-proposals.json')['execution_credit'],0)
 def test_no_execution(self): self.assertFalse(load('phase-truth.json')['implementation_executed'])
 def test_novelty(self): self.assertEqual(load('novelty-review.json')['exact_collisions'],[])
 def test_tools(self): self.assertEqual(len(load('tool-plan.json')['skills']),10); self.assertEqual(len(load('tool-plan.json')['runners']),5)
 def test_portfolio(self): self.assertEqual([len(load('approval-portfolio.json')[k]) for k in ['safe_now','candidates','clean_fix_refine','exact_packets','blocked_packets']],[300,250,300,50,30])
 def test_outcomes(self): self.assertEqual(set(r['expected']['disposition'] for r in load('new-proposals.json')['proposals']),{'completed','represented','open_gap','exact_gate'})
 def test_route(self): self.assertEqual(load('route-freeze.json')['send_count'],0); self.assertEqual(load('route-freeze.json')['next_phase'],'v689-v1')
 def test_packages(self): self.assertFalse(load('tool-plan.json')['installation_executed']); self.assertTrue(load('tool-plan.json')['packages']['closure_verified'])
 def test_eof(self): self.assertTrue(all(r['read_through_eof'] and r['eof'].startswith('EOF ') for r in load('reading-receipt.json')['batons_in_read_order']))
 def test_retained(self): self.assertTrue({f'TER6888-START-M{i:03}-FAIL' for i in range(1,11)} <= {w['witness_id'] for w in load('method-flow-startup.json')['witnesses']})
if __name__=='__main__': unittest.main()
