"""Compare owner behaviour with immutable prospective contracts and boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_reaction_core as core

ORIGINAL=json.loads((ROOT/'x1/new-proposals.json').read_text())['proposals']
CORRECTION=json.loads((ROOT/'x1/addendum/ordered-species-correction.json').read_text())
CASES=[CORRECTION['corrected_definition'] if r['proposal_id']=='MV6884-N195' else r for r in ORIGINAL]

class ReactionContracts(unittest.TestCase):
    def test_original_ordering_failure_remains_addressable(self):
        original=next(r for r in ORIGINAL if r['proposal_id']=='MV6884-N195')
        self.assertNotIn('reactant_order',original['input'])
        self.assertEqual(list(original['input']['reactants']),['A','Z'])
        self.assertEqual(CORRECTION['corrected_definition']['input']['reactant_order'],['Z','A'])
        self.assertEqual(CORRECTION['novelty_credit'],0)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(core.Refusal,'DUPLICATE_JSON_KEY'):
            core.strict_loads('{"operation":"flat_formula","operation":"grouped_formula"}')

    def test_nonfinite_json_constants_are_rejected(self):
        for token in ['NaN','Infinity','-Infinity']:
            with self.subTest(token=token),self.assertRaisesRegex(core.Refusal,'NONFINITE_JSON'):
                core.strict_loads('{"value":'+token+'}')

    def test_comparator_preserves_types_and_array_positions(self):
        for left,right in [(True,1),(1,1.0),({'x':False},{'x':0}),([1,2],[2,1]),({'x':1},{'x':1,'y':0}),('01','1')]:
            self.assertFalse(core.typed_equal(left,right))
        self.assertTrue(core.typed_equal({'x':1,'y':[False,None]},{'y':[False,None],'x':1}))

    def test_all_inputs_remain_unchanged(self):
        for row in CASES:
            value=copy.deepcopy(row['input']);before=copy.deepcopy(value)
            core.evaluate(value)
            self.assertTrue(core.typed_equal(value,before),row['proposal_id'])

    def test_extra_fields_cannot_bypass_any_operation(self):
        seen=set()
        for row in CASES:
            if row['operation'] in seen:continue
            seen.add(row['operation']);value=copy.deepcopy(row['input']);value['execute_external_action']=True
            self.assertEqual(core.evaluate(value)['error'],'FIELD_SET')
        self.assertEqual(len(seen),20)

    def test_frozen_order_adversaries(self):
        for row in CORRECTION['adverse_order_cases']:
            self.assertTrue(core.typed_equal(core.evaluate(row['input']),row['expected_output']),row['case'])

    def test_resource_bounds_and_unknown_operation(self):
        self.assertEqual(core.evaluate({'operation':'unlisted'})['error'],'OPERATION')
        self.assertEqual(core.evaluate({'operation':'grouped_formula','formula':'('*25+'H'+')'*25})['error'],'GROUP_DEPTH')
        self.assertEqual(core.evaluate({'operation':'complex_incidence','node_count':1001,'edges':[]})['error'],'NODE_COUNT')
        self.assertEqual(core.evaluate({'operation':'mass_action_monomial','law':'declared_mass_action','coefficient':'1','concentrations':['2'],'orders':[13]})['error'],'ORDER_RANGE')

def make_test(operation):
    def test(self):
        rows=[r for r in CASES if r['operation']==operation]
        self.assertEqual(len(rows),10)
        for row in rows:
            with self.subTest(proposal=row['proposal_id']):
                actual=core.evaluate(copy.deepcopy(row['input']))
                self.assertTrue(core.typed_equal(actual,row['expected_output']),(actual,row['expected_output']))
    return test

for operation in dict.fromkeys(r['operation'] for r in CASES):
    setattr(ReactionContracts,'test_frozen_'+operation,make_test(operation))

if __name__=='__main__':unittest.main()
