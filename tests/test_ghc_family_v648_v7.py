import json, subprocess, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHASE=ROOT/'docs/tamar-vey/v648-v7'
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
class V648V7EvidenceTests(unittest.TestCase):
    def test_core_distribution(self):
        d=load('x2/core-outcome-ledger.json'); self.assertEqual(d['count'],10); self.assertEqual(d['distribution'],{'completed':6,'represented':2,'open_gap':1,'exact_gate':1}); self.assertTrue(all(r['acceptance_gate_passed'] for r in d['items']))
    def test_empirical_and_authority_absence(self):
        d=load('x2/evidence-ledger.json'); self.assertEqual((d['real_rows'],d['likelihood_evaluations'],d['real_participants_or_operators'],d['real_keys_or_proofs'],d['authority_decisions']),(0,0,0,0,0)); self.assertFalse(d['independent_reproduction'])
    def test_mutations_retained(self):
        d=load('validation/x2-synthetic-mutation-results.json'); self.assertEqual((d['count'],d['executed_count'],d['rejected_count'],d['completion_credit']),(70,70,70,0)); self.assertTrue(all(r['retained_negative'] for r in d['items']))
    def test_portfolios(self):
        d=load('x2/portfolio-ledger.json'); self.assertEqual((d['safe_completed'],d['candidates_completed'],d['skills_initialized'],d['skills_validated'],d['skills_smoke_used'],d['runners_invoked'],d['clean_refine_completed']),(30,20,20,20,19,9,30)); self.assertEqual(d['inherited_completion_credit'],0)
    def test_skills_phase_local(self):
        d=load('x2/skill-use-ledger.json'); self.assertEqual((d['skill_count'],d['completed_count'],d['pending_count']),(20,19,1)); self.assertTrue(all(not r['global_install'] for r in d['items'])); self.assertTrue(all(r['forward_test']=='not_permitted_no_subagents' for r in d['items']))
    def test_negatives_and_gates(self):
        n=load('x2/retained-negative-register.json'); g=load('x2/gate-register.json'); self.assertEqual(n['effective'],4575); self.assertFalse(n['negative_erased']); self.assertEqual((g['open_gaps'],g['exact_gates']),(33,34)); self.assertEqual(g['silently_closed'],0)
    def test_manifest_privacy(self):
        p=load('validation/evidence-staged-privacy.json'); m=load('validation/evidence-staged-manifest.json'); self.assertEqual(len(p['pattern_classes']),5); self.assertEqual(p['confirmed_hit_count'],0); self.assertEqual(m['entry_count'],len(m['entries']))
    def test_x1_immutable_commit(self):
        self.assertEqual(subprocess.check_output(['git','rev-parse','5ab7e85107f92dd8f6f21af66244c6dc9791b39d^'],cwd=ROOT,text=True).strip(),'38e3fe7bc710239337f831617ced97bec51d7d7a')
if __name__=='__main__': unittest.main()
