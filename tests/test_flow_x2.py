"""Frozen x2 envelopes plus finite optimality and nonpromotion invariants."""
import copy,itertools,json,unittest
from pathlib import Path
from scripts.ghc_family_flow_common import canonical
from scripts.ghc_family_flow_x1 import maximum_flow
from scripts.ghc_family_flow_x2 import evaluate,minimum_cut,minimum_cost,assignment
ROOT=Path(__file__).resolve().parents[1]
ROWS=[r for r in json.loads((ROOT/'docs/mira-fenwick/v690-v3/plan/new-proposals.json').read_text(encoding='utf-8'))['proposals'] if r['session']=='x2']
class FrozenX2(unittest.TestCase):pass
def case_test(operation):
    def test(self):
        for row in [r for r in ROWS if r['operation']==operation]:
            with self.subTest(proposal=row['proposal_id']):
                before=canonical(row['request']);self.assertEqual(canonical(evaluate(row['request'])),canonical(row['expected_envelope']));self.assertEqual(canonical(row['request']),before)
    return test
for operation in sorted({r['operation'] for r in ROWS}):setattr(FrozenX2,'test_'+operation,case_test(operation))

class FlowX2Invariants(unittest.TestCase):
    def test_all_27_three_vertex_forward_networks(self):
        for a,b,c in itertools.product(range(3),repeat=3):
            graph={'nodes':['s','a','t'],'arcs':[['s','a',a],['a','t',b],['s','t',c]]}
            self.assertEqual(maximum_flow(graph)['value'],minimum_cut(graph)['capacity'])
    def test_vertex_order_changes_no_optimum_value(self):
        graph={'nodes':['s','a','b','t'],'arcs':[['s','a',2],['a','t',1],['s','b',1],['b','t',2],['a','b',1]]}
        other=copy.deepcopy(graph);other['nodes'].reverse()
        self.assertEqual(maximum_flow(graph)['value'],maximum_flow(other)['value']);self.assertEqual(minimum_cut(graph)['capacity'],minimum_cut(other)['capacity'])
    def test_upstream_capacity_increase_can_have_zero_gain(self):
        request={'op':'increase_capacity','graph':{'nodes':['s','a','t'],'arcs':[['s','a',3],['a','t',2]]},'arc_index':0,'delta':1}
        self.assertEqual(evaluate(request)['result'],{'before':2,'after':2,'gain':0})
    def test_capacity_increase_cannot_escape_declared_profile(self):
        self.assertEqual(evaluate({'op':'increase_capacity','graph':{'nodes':['s','t'],'arcs':[['s','t',8]]},'arc_index':0,'delta':1})['error'],'invalid_capacity')
    def test_negative_bounded_cycle_can_lower_zero_flow_cost(self):
        graph={'nodes':['s','a','b','t'],'arcs':[['s','a',2],['a','b',2],['b','a',1],['b','t',1]]}
        self.assertEqual(minimum_cost(graph,[0,-2,1,0],0),{'feasible':True,'cost':-1})
    def test_cost_enumeration_work_budget_is_enforced(self):
        graph={'nodes':['s','a','b','t'],'arcs':[['s','a',8],['s','b',8],['a','b',8],['b','a',8],['a','t',8],['b','t',8],['t','s',8],['t','a',8]]}
        self.assertEqual(evaluate({'op':'min_cost','graph':graph,'costs':[1]*8,'required':1})['error'],'work_limit')
    def test_greedy_assignment_counterexample(self):
        self.assertEqual(assignment([[1,2],[2,99]]),{'columns':[1,0],'cost':4});self.assertGreater(1+99,4)
    def test_assignment_uses_distinct_columns(self):
        out=assignment([[4,1,3],[1,2,3]]);self.assertEqual(out,{'columns':[1,0],'cost':2});self.assertEqual(len(set(out['columns'])),2)
    def test_all_claimed_flags_leave_real_verification_missing(self):
        out=evaluate({'op':'policy_gate','graph':{'nodes':['s','t'],'arcs':[['s','t',3]]},'required':1,'consent':True,'evidence':True,'authority':True})
        self.assertEqual(out['result']['missing'],['real_world_verification']);self.assertFalse(out['result']['external_action'])
    def test_boolean_policy_flags_are_not_integer_flags(self):
        self.assertEqual(evaluate({'op':'policy_gate','graph':{'nodes':['s','t'],'arcs':[]},'required':0,'consent':1,'evidence':False,'authority':False})['error'],'invalid_flag')

if __name__=='__main__':unittest.main()
