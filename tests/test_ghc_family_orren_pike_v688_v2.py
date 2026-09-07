"""Owner-only tests of frozen SVG behavior and evidence integrity."""
import collections,copy,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/orren-pike/v688-v2'
sys.path.insert(0,str(ROOT/'scripts/orren_pike_v688_v2'))
from ghc_family_svg_evidence_core import evaluate,strict_loads,Refusal
PROPOSALS=json.loads((BASE/'x1/new-proposals.json').read_text())['proposals']
def typed(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)

class SVGContractTests(unittest.TestCase):
 def test_extra_fields_refused(self):
  for p in PROPOSALS:
   with self.subTest(p=p['proposal_id']):self.assertEqual(evaluate({**p['input'],'external_permission':True})['error'],'FIELD_SET')
 def test_nested_duplicate_keys_refused(self):
  with self.assertRaises(Refusal):strict_loads('{"outer":{"x":1,"x":2}}')
 def test_nonfinite_constants_refused(self):
  for token in ['NaN','Infinity','-Infinity']:
   with self.subTest(token=token),self.assertRaises(Refusal):strict_loads('{"x":'+token+'}')
 def test_inputs_preserved(self):
  for p in PROPOSALS:
   before=typed(p['input']);evaluate(p['input']);self.assertEqual(typed(p['input']),before)
 def test_relative_lineto_composes(self):
  first=evaluate({'operation':'lineto','command':'l','current':['1','2'],'parameters':['3','4']})['value']
  second=evaluate({'operation':'lineto','command':'l','current':first['current_point'],'parameters':['-1','-2']})['value']
  joined=evaluate({'operation':'lineto','command':'l','current':['1','2'],'parameters':['3','4','-1','-2']})['value']
  self.assertEqual(joined['endpoints'],first['endpoints']+second['endpoints'])
 def test_odd_dash_representation_agrees_with_explicit_duplication(self):
  a=evaluate({'operation':'dash_array','values':['1','2','3']})
  b=evaluate({'operation':'dash_array','values':['1','2','3','1','2','3']})
  self.assertEqual(a,b)
 def test_deck_graph_has_one_immediate_parent(self):
  index=json.loads((BASE/'x2/deck/deck-index.json').read_text());cards={cid:json.loads((BASE/'x2/deck/cards'/f'{cid}.json').read_text()) for cid in index['cards']}
  self.assertEqual(len(cards),len(index['cards']));self.assertEqual(sum(c['tier']==1 for c in cards.values()),1)
  for c in cards.values():
   if c['tier']>1:self.assertEqual(len(c['parent_ids']),1);self.assertEqual(cards[c['parent_ids'][0]]['tier'],c['tier']-1)
 def test_method_flow_links_and_counts(self):
  x=json.loads((BASE/'x2/method-flow/ledger.json').read_text());ms={m['method_id']:m for m in x['methods']};ws={w['witness_id']:w for w in x['witnesses']}
  self.assertEqual(len(ms),x['counts']['methods']);self.assertEqual(len(ws),x['counts']['witnesses']);self.assertEqual(dict(collections.Counter(w['result'] for w in ws.values())),x['counts']['witness_results'])
  for w in ws.values():self.assertIn(w['method_id'],ms);self.assertTrue(w['same_owner_only']);self.assertFalse(w['independent_reproduction'])
  for m in ms.values():self.assertTrue(set(m['validation_witness_ids'])<=set(ws))

def operation_test(operation):
 def check(self):
  selected=[p for p in PROPOSALS if p['operation']==operation];self.assertEqual(len(selected),10)
  for p in selected:
   with self.subTest(contract=p['proposal_id']):self.assertEqual(typed(evaluate(copy.deepcopy(p['input']))),typed(p['expected_output']))
 return check
for op in dict.fromkeys(p['operation'] for p in PROPOSALS):setattr(SVGContractTests,'test_contract_'+op,operation_test(op))
if __name__=='__main__':unittest.main()
