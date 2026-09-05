"""Behavioral checks beyond the frozen example reports."""
import copy,importlib,json,random,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_protocol_trace as trace
import ghc_family_protocol_budget as budget
import ghc_family_protocol_analysis as analysis
import ghc_family_protocol_provenance as prov
import ghc_family_protocol_export as export
import build_ghc_family_ilyan_reed_v685_v8_x2 as lab
class ProtocolBehavior(unittest.TestCase):
    def test_every_frozen_oracle(self):
        for p in lab.read('x1/new-proposals.json')['proposals']:
            with self.subTest(p=p['proposal_id']):self.assertTrue(lab.evaluate(p,lab.fixture(p))['accepted'])
    def test_all_preregistered_mutations_rejected(self):
        rows=lab.read('x2/invalid-mutations.json')['records'];self.assertEqual(len(rows),1000);self.assertTrue(all(not r['result']['accepted'] for r in rows))
    def test_schedule_preserves_equal_time_fifo(self):
        events=[[str(i),3,0] for i in range(80)];self.assertEqual(trace.schedule({'events':events}),[str(i) for i in range(80)])
    def test_queue_translation_preserves_waiting(self):
        jobs=[['a',0,3],['b',1,4],['c',2,1]];base=trace.queue({'jobs':jobs});shift=trace.queue({'jobs':[[n,a+10,s] for n,a,s in jobs]});self.assertEqual(shift,[[n,a+10,b+10] for n,a,b in base])
    def test_replay_is_idempotent_for_separated_duplicates(self):
        e=[[str(i),i] for i in range(100)];self.assertEqual(trace.replay({'events':e+e[::-1]}),4950)
    def test_terminal_state_rejects_later_actions(self):
        for e in ['start','pause','resume','finish']:self.assertIn('error',trace.transition({'events':['cancel',e]}))
    def test_budget_granularity_is_invariant(self):
        self.assertTrue(budget.budget({'arms':[[1]*97,[97]],'cap':97})['matched'])
    def test_masking_overlap_is_symmetric(self):
        a=['a','b','c'];b=['b','d'];self.assertEqual(budget.separation({'evaluators':a,'key_holders':b}),budget.separation({'evaluators':b,'key_holders':a}))
    def test_denominator_never_drops_missing(self):
        x=budget.denominator({'rows':['observed']*7+['missing']*13+['excluded']*3});self.assertEqual(x['total'],23)
    def test_mean_translation_and_scale(self):
        rng=random.Random(6858)
        for _ in range(30):
            x=[rng.randrange(-100,100) for _ in range(9)];from fractions import Fraction
            m=Fraction(analysis.summary({'values':x,'stat':'mean'}));self.assertEqual(Fraction(analysis.summary({'values':[3*v+7 for v in x],'stat':'mean'})),3*m+7)
    def test_pair_swapping_negates_differences(self):
        a=[['a',7],['b',3]];b=[['a',2],['b',8]];self.assertEqual(analysis.paired({'a':b,'b':a}),[['a','-5'],['b','5']])
    def test_histogram_conserves_fixture_count(self):
        self.assertEqual(sum(analysis.histogram({'values':list(range(101)),'edges':[0,25,50,75,100]})),101)
    def test_cycle_detection_survives_disconnected_component(self):
        self.assertEqual(prov.lineage({'nodes':['a','b','c'],'edges':[['a','b'],['b','a']]}),{'error':'cycle'})
    def test_merge_is_nondestructive(self):
        d={'left':{'a':{'v':2}},'right':{'b':3}};before=copy.deepcopy(d);out=prov.merge(d);self.assertEqual(d,before);self.assertEqual(out,{'a':{'v':2},'b':3})
    def test_typed_json_equality_rejects_boolean_integer_substitution(self):
        self.assertEqual(prov.merge({'left':{'a':False},'right':{'a':0}}),{'error':'conflict'})
    def test_projection_retains_source(self):
        d={'record':{'title':'x','note':'draft'},'allow':['title'],'required':['title']};before=copy.deepcopy(d);self.assertEqual(export.export(d),{'title':'x'});self.assertEqual(d,before)
    def test_reservation_cannot_be_promoted_by_a_field(self):
        self.assertEqual(export.reservation({'obligation':'review','evidence':'synthetic pass','authority':None,'disposition':'completed'}),{'error':'unsupported_promotion'})
    def test_portfolio_gates_are_unexecuted(self):
        d=lab.read('x2/portfolio-results.json')
        for k in ['exact_packets','blocked_packets']:self.assertTrue(all(not r['operation_executed'] for r in d[k]))
        for k in ['safe_now','candidates','clean_fix_refine']:self.assertTrue(all(r['passed'] for r in d[k]))
if __name__=='__main__':unittest.main()
