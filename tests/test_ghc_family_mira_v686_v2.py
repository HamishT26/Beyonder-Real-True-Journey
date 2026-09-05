"""Selected owner tests: frozen family contracts plus security and semantic invariants."""
import copy,importlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_evidence_selectors as s
import ghc_family_evidence_patch as p
import ghc_family_correction_lineage as l
import ghc_family_receipt_binding as r
import ghc_family_obligation_projection as o
ROWS=json.loads((ROOT/'docs/mira-fenwick/v686-v2/x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']
COMPUTE={'selectors':s.evaluate,'patch':p.evaluate,'lineage':l.evaluate,'receipts':r.evaluate,'obligations':o.evaluate}

class FrozenFamilies(unittest.TestCase):pass
def family_test(family):
    def test(self):
        for row in [x for x in ROWS if x['family']==family]:
            with self.subTest(proposal=row['proposal_id']):
                original=s.canonical(row['input']);value=COMPUTE[row['runner']](row['operation'],row['input'])
                self.assertEqual(s.canonical(value),s.canonical(row['expected_result']))
                self.assertEqual(original,s.canonical(row['input']))
    return test
for family in sorted({x['family'] for x in ROWS}):setattr(FrozenFamilies,'test_'+family,family_test(family))

class IndependentInvariants(unittest.TestCase):
    def test_explicit_null_permissions_do_not_inherit_unrestricted_default(self):
        self.assertEqual(p.evaluate('patch',{'document':{},'operations':[{'op':'add','path':'/a','value':1}],'allowed':None}),{'error':'invalid_permissions'})
    def test_duplicate_json_member_rejected(self):
        with self.assertRaises(s.Refusal):s.strict_load('{"a":1,"a":2}')
    def test_nonfinite_json_rejected(self):
        for word in ('NaN','Infinity','-Infinity'):
            with self.subTest(word=word),self.assertRaises(s.Refusal):s.strict_load(word)
    def test_lone_surrogate_rejected(self):
        with self.assertRaises(s.Refusal):s.check_json(chr(0xd800))
    def test_nonstring_object_key_rejected(self):
        with self.assertRaises(s.Refusal):s.check_json({1:'x'})
    def test_deep_tree_rejected(self):
        value=0
        for _ in range(66):value=[value]
        with self.assertRaises(s.Refusal):s.check_json(value)
    def test_large_node_budget_rejected(self):
        with self.assertRaises(s.Refusal):s.check_json([0]*10001)
    def test_huge_array_index_has_bounded_refusal(self):
        self.assertEqual(s.evaluate('resolve',{'document':[0],'pointer':'/'+'9'*1000}),{'error':'missing_target'})
    def test_escaped_path_roundtrip(self):
        for parts in ([],[''],['~','/','a/b','~01'],['Māori',' ','01']):self.assertEqual(s.tokens(s.pointer_from_tokens(parts)),parts)
    def test_no_unicode_normalization(self):
        self.assertEqual(s.evaluate('resolve',{'document':{'Å':1},'pointer':'/Å'}),{'error':'missing_target'})
    def test_projection_copy_does_not_alias_document(self):
        doc={'a':[1]};out=s.project(doc,['/a']);out['/a'].append(2);self.assertEqual(doc,{'a':[1]})
    def test_atomic_failure_preserves_document_and_patch(self):
        data={'document':{'a':1},'operations':[{'op':'replace','path':'/a','value':2},{'op':'remove','path':'/missing'}]}
        original=copy.deepcopy(data);self.assertIn('error',p.evaluate('patch',data));self.assertEqual(data,original)
    def test_patch_values_do_not_alias_output(self):
        value=[];out=p.patch({},[{'op':'add','path':'/a','value':value}]);out['a'].append(1);self.assertEqual(value,[])
    def test_numeric_test_is_distinct_from_receipt_byte_equality(self):
        self.assertTrue(p.equal(1,1.0));self.assertNotEqual(s.sha(1),s.sha(1.0))
    def test_nested_boolean_number_inequality(self):
        self.assertFalse(p.equal({'a':[False]},{'a':[0]}))
    def test_permission_decodes_tokens_before_ancestry(self):
        self.assertEqual(p.evaluate('patch',{'document':{'a/b':{}},'operations':[{'op':'add','path':'/a~1b/x','value':1}],'allowed':['/a']}),{'error':'path_not_allowed'})
    def test_move_self_still_requires_existing_source(self):
        self.assertEqual(p.evaluate('patch',{'document':{},'operations':[{'op':'move','path':'/a','from':'/a'}]}),{'error':'missing_target'})
    def test_operation_limit_refuses_before_application(self):
        self.assertEqual(p.evaluate('patch',{'document':{},'operations':[{'op':'add','path':'/a','value':1}]*501}),{'error':'operation_limit'})
    def test_lineage_boolean_ordinal_rejected(self):
        data={'snapshots':[0,1],'links':[{'ordinal':True,'parent_sha256':s.sha(0),'child_sha256':s.sha(1),'reason':'r'}]}
        self.assertEqual(l.evaluate('chain',data),{'error':'ordinal_mismatch'})
    def test_changed_path_zero_and_false_are_distinct(self):
        self.assertEqual(l.evaluate('changes',{'before':{'a':0},'after':{'a':False}}),['/a'])
    def test_manifest_empty_segments_rejected(self):
        for path in ('a//b','./a','a/../b','a/','/a'):
            self.assertFalse(r.literal_path(path))
    def test_manifest_size_boolean_rejected(self):
        import hashlib
        self.assertEqual(r.evaluate('manifest',{'files':{'a':'x'},'entries':[{'path':'a','bytes':True,'sha256':hashlib.sha256(b'x').hexdigest()}]}),{'error':'size_mismatch'})
    def test_obligation_external_action_refused(self):
        d=copy.deepcopy(ROWS[-1]['input']);d['external_action']=True;self.assertEqual(o.evaluate('obligation',d),{'error':'unsupported_promotion'})
    def test_envelope_forged_result_digest_does_not_establish_answer(self):
        row=ROWS[0];record=s.envelope(row,{'fiction':True});self.assertFalse(s.verify_envelope(row,record,s.evaluate)['accepted'])
    def test_envelope_false_integer_promotion_rejected(self):
        row=ROWS[0];record=s.envelope(row,[]);record['authority']=0;self.assertFalse(s.verify_envelope(row,record,s.evaluate)['accepted'])

if __name__=='__main__':unittest.main()
