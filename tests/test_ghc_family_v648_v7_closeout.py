import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHASE=ROOT/'docs/tamar-vey/v648-v7'
def load(p): return json.loads((PHASE/p).read_text(encoding='utf-8'))
class V648V7CloseoutTests(unittest.TestCase):
    def test_overview_and_report(self):
        t=(PHASE/'integrated-overview.md').read_text(encoding='utf-8'); self.assertGreaterEqual(len(re.findall(r'\b\w+\b',t)),1200); self.assertLessEqual(len(re.findall(r'\b\w+\b',t)),6000); h=(PHASE/'accessible-report.html').read_text(encoding='utf-8'); self.assertIn('Skip to main content',h); self.assertIn('<caption>',h)
    def test_final_skills_and_runners(self):
        s=load('x2/skill-use-ledger-final.json'); r=load('x2/runner-use-ledger-final.json'); self.assertEqual((s['skill_count'],s['completed_count'],s['pending_count']),(20,20,0)); self.assertEqual((r['runner_count'],r['completed_count'],r['pending_count']),(10,10,0)); self.assertTrue(all(x['smoke_used'] for x in s['items']))
    def test_terminal_truth(self):
        p=load('phase-truth-final-candidate.json'); b=load('stage20-terminal-board.json'); self.assertEqual(p['outcomes'],{'completed':6,'represented':2,'open_gap':1,'exact_gate':1}); self.assertEqual(p['terminal_route'],'PREPARED_NOT_SENT'); self.assertFalse(b['ready'])
    def test_gates_and_negatives(self):
        n=load('retained-negative-register-final.json'); g=load('exact-open-gate-register-final.json'); self.assertEqual(n['effective'],4580); self.assertEqual((g['open_gaps'],g['exact_gates']),(33,34)); self.assertFalse(n['negative_erased'])
    def test_checklist_keeps_external_work_open(self):
        d=load('complete-incomplete-checklist.json'); self.assertIn('independent_reproduction',d['incomplete']); self.assertIn('stage20',d['incomplete'])
    def test_validation_budget(self):
        d=load('validation/final-validation-plan.json'); self.assertEqual(d['canonical_successful_pass_budget'],1); self.assertEqual(d['successful_passes_used'],0); self.assertEqual(d['failed_canonical_attempts'],2); self.assertEqual(d['selected_test_count'],67); self.assertEqual(len(d['excluded_source_local_tests']),2); self.assertEqual(d['replay_budget'],0); self.assertFalse(d['full_repository_suite'])
    def test_solo_and_route(self):
        d=load('orchestration/final-phase-state.json'); self.assertEqual(d['subagents'],0); self.assertEqual(d['tasks_created'],0); self.assertEqual(d['cross_platform_messages'],0); self.assertEqual(d['terminal_route'],'PREPARED_NOT_SENT')
if __name__=='__main__': unittest.main()
