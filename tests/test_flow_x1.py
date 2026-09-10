"""Frozen x1 cases and separate bounded algorithm invariants."""
import copy,json,itertools,unittest
from pathlib import Path
from scripts.ghc_family_flow_common import canonical,Refusal,load_json,feasible
from scripts.ghc_family_flow_x1 import evaluate,maximum_flow,cut_capacity,augment_once
ROOT=Path(__file__).resolve().parents[1]
ROWS=[r for r in json.loads((ROOT/'docs/mira-fenwick/v690-v3/plan/new-proposals.json').read_text(encoding='utf-8'))['proposals'] if r['session']=='x1']

class FrozenX1(unittest.TestCase):pass
def case_test(operation):
    def test(self):
        for row in [r for r in ROWS if r['operation']==operation]:
            with self.subTest(proposal=row['proposal_id']):
                before=canonical(row['request']);self.assertEqual(canonical(evaluate(row['request'])),canonical(row['expected_envelope']));self.assertEqual(canonical(row['request']),before)
    return test
for operation in sorted({r['operation'] for r in ROWS}):setattr(FrozenX1,'test_'+operation,case_test(operation))

class FlowX1Invariants(unittest.TestCase):
    def test_duplicate_json_fields_refused(self):
        with self.assertRaises(Refusal):load_json('{"op":"x","op":"y"}')
    def test_nonfinite_json_refused(self):
        for word in ('NaN','Infinity','-Infinity'):
            with self.subTest(word=word),self.assertRaises(Refusal):load_json(word)
    def test_unknown_field_precedes_graph_computation(self):
        self.assertEqual(evaluate({'op':'max_value','graph':None,'extra':True})['error'],'unknown_field')
    def test_maximum_flows_are_feasible(self):
        graphs=[r['request']['graph'] for r in ROWS if r['operation']=='max_value' and r['expected_envelope']['accepted']]
        for graph in graphs:self.assertTrue(feasible(graph,maximum_flow(graph)['flow']))
    def test_maximum_value_is_bounded_by_every_cut(self):
        graphs=[r['request']['graph'] for r in ROWS if r['operation']=='max_value' and r['expected_envelope']['accepted']]
        for graph in graphs:
            value=maximum_flow(graph)['value'];inner=[v for v in graph['nodes'] if v not in ('s','t')]
            for n in range(len(inner)+1):
                for part in itertools.combinations(inner,n):self.assertLessEqual(value,cut_capacity(graph,['s',*part]))
    def test_reverse_residual_step_recovers_a_second_unit(self):
        graph={'nodes':['s','a','b','t'],'arcs':[['s','a',1],['a','b',1],['b','t',1],['s','b',1],['a','t',1]]}
        before=[1,1,1,0,0];out=augment_once(graph,before)
        self.assertEqual(out,{'flow':[1,0,1,1,1],'delta':1,'value':2});self.assertEqual(before,[1,1,1,0,0])
    def test_output_container_does_not_alias_input(self):
        request={'op':'normalize','graph':{'nodes':['s','t'],'arcs':[['s','t',1]]}}
        out=evaluate(request);out['result']['arcs'][0][2]=8;self.assertEqual(request['graph']['arcs'][0][2],1)
    def test_boolean_capacity_and_oversized_graph_are_refused(self):
        self.assertEqual(evaluate({'op':'max_value','graph':{'nodes':['s','t'],'arcs':[['s','t',True]]}})['error'],'invalid_capacity')
        self.assertEqual(evaluate({'op':'max_value','graph':{'nodes':['s','t','a','b','c','d','e','f','g'],'arcs':[]}})['error'],'vertex_count')

if __name__=='__main__':unittest.main()
