"""Independent invariants for the new finite capacity models."""
import copy,importlib.util,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_capacity_core import ContractError,evaluate,typed_equal,strict_json
from ghc_family_weighted_route_review import review
PHASE=ROOT/'docs/seren-talewood/v689-v2-r3'

class CapacityInvariants(unittest.TestCase):
    def test_closed_typed_envelope_comparison(self):
        self.assertFalse(typed_equal({'x':True},{'x':1}))
        self.assertFalse(typed_equal({'x':1},{'x':1.0}))
        self.assertFalse(typed_equal({'x':[]},{'x':[],'extra':None}))

    def test_duplicate_json_and_nonfinite_are_visible(self):
        for text in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}']:
            with self.assertRaises(ContractError):strict_json(text)

    def test_queue_conserves_service_and_wait(self):
        from fractions import Fraction as F
        for jobs in [[[0,2],[1,3],[7,1]],[[0,0],[0,0]],[[2,1],[2,1],[2,1]]]:
            out=evaluate({'op':'fcfs','jobs':jobs})['value']
            starts=list(map(F,out['starts']));ends=list(map(F,out['finishes']))
            self.assertEqual(sum((e-s for s,e in zip(starts,ends)),F(0)),sum(j[1] for j in jobs))
            self.assertEqual(F(out['total_wait']),sum((s-j[0] for s,j in zip(starts,jobs)),F(0)))
            self.assertTrue(all(ends[i]<=starts[i+1] for i in range(len(jobs)-1)))

    def test_packing_preserves_every_indivisible_item(self):
        for sizes in [[7,5,3,2,2,1],[6,6,4,4],[1]*9]:
            out=evaluate({'op':'ffd','sizes':sizes,'capacity':10})['value']
            self.assertEqual(sorted(i for b in out['bins'] for i in b),list(range(len(sizes))))
            self.assertTrue(all(sum(sizes[i] for i in b)<=10 for b in out['bins']))
            self.assertFalse(out['optimality_claimed'])

    def test_largest_remainder_retains_alabama_paradox(self):
        weights=[1500,1500,900,500,500,200]
        a=evaluate({'op':'fair_quota','weights':weights,'total':25})['value']['allocation']
        b=evaluate({'op':'fair_quota','weights':weights,'total':26})['value']['allocation']
        self.assertEqual(a,[7,7,4,3,3,1]);self.assertEqual(b,[8,8,5,2,2,1])
        self.assertLess(b[3],a[3]);self.assertLess(b[4],a[4])

    def test_prefix_cost_has_no_silent_truncation(self):
        req={'op':'context_batches','sizes':[4,2,3,1],'prefix':2,'limit':8};before=copy.deepcopy(req)
        out=evaluate(req)['value'];self.assertEqual(req,before)
        self.assertEqual([i for b in out['batches'] for i in b],list(range(4)))
        self.assertEqual(sum(out['totals']),sum(req['sizes'])+2*len(out['batches']))

    def test_coverage_conservation_uses_window_clipping(self):
        from fractions import Fraction as F
        out=evaluate({'op':'coverage','intervals':[[-1,1],[2,4],[3,5],[9,12]],'window':[0,10]})['value']
        self.assertEqual(out,{'covered_duration':'5','gaps':[['1','2'],['5','9']]})
        self.assertEqual(F(out['covered_duration'])+sum((F(y)-F(x) for x,y in out['gaps']),F(0)),10)

    def test_current_weighted_route_and_wrong_identity(self):
        route=json.loads((PHASE/'plan/route-v4.json').read_bytes());profile=json.loads((PHASE/'plan/profile-v4.json').read_bytes())
        out=review(route,profile);self.assertEqual(out['model_roles'],{'Sol':196,'Astra':98})
        self.assertEqual(route['assignments'][1]['owner'],'Elaren Kestrel')
        route['cycle'][33]='Thalen Briar'
        with self.assertRaises(ContractError):review(route,profile)

    def test_portable_record_codec_preserves_container_types(self):
        path=PHASE/'x1/ghc_family_portfolio_execute.py';spec=importlib.util.spec_from_file_location('portfolio_codec',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        source={'0':[False,0,None,{},[],{'/':'x'}]};flat=mod.flatten(source);restored=mod.rebuild(flat)
        self.assertTrue(typed_equal(source,restored));restored['0'][5]['/']='edited';self.assertEqual(source['0'][5]['/'],'x')

    def test_graph_cycle_and_diamond_are_distinct(self):
        good=evaluate({'op':'critical_path','durations':[1,2,3,4],'edges':[[0,1],[0,2],[1,3],[2,3]]})
        self.assertEqual(good['value']['makespan'],'8')
        bad=evaluate({'op':'critical_path','durations':[1,2],'edges':[[0,1],[1,0]]})
        self.assertEqual(bad['error'],'E_CYCLE')

    def test_empty_and_zero_denominators_do_not_create_savings(self):
        self.assertEqual(evaluate({'op':'mix_cost','astra_cost':0})['error'],'E_POSITIVE')
        self.assertEqual(evaluate({'op':'token_cost','input_tokens':1,'cached_tokens':2,'output_tokens':0,'rates':[1,1,1]})['error'],'E_CACHE')

    def test_boolean_nested_data_never_becomes_duration(self):
        for req in [{'op':'critical_path','durations':[True],'edges':[]},{'op':'edd','jobs':[[False,1]]},{'op':'fcfs','jobs':[[0,True]]}]:
            self.assertEqual(evaluate(req)['error'],'E_RATIONAL')

if __name__=='__main__':unittest.main()
