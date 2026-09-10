"""Finite invariants that do not import the planning oracle."""
import copy,itertools,sys,unittest
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ghc_family_membership_x1 import evaluate
def run(op,**payload):return evaluate({'operation':op,'payload':payload})
class BitsetInvariants(unittest.TestCase):
    def test_shape_over_complete_five_bit_domain(self):
        for row in itertools.product('01',repeat=5):
            bits=''.join(row);r=run('bit_shape',bits=bits)['value'];self.assertEqual(r,{'length':5,'ones':sum(map(int,row)),'zeros':5-sum(map(int,row))})
    def test_insert_is_idempotent(self):
        a=run('bit_insert',bits='000000',positions=[0,2,2,5])['value'];self.assertEqual(run('bit_insert',bits=a,positions=[0,2,5])['value'],a)
    def test_insert_order_is_irrelevant(self):self.assertEqual(run('bit_insert',bits='01000',positions=[0,4]),run('bit_insert',bits='01000',positions=[4,0]))
    def test_queries_have_no_false_negatives_after_insertion(self):
        for positions in itertools.product(range(4),repeat=2):
            pos=list(positions);b=run('bit_insert',bits='0000',positions=pos)['value'];self.assertTrue(run('membership_query',bits=b,positions=pos)['value']['possible'])
    def test_positive_membership_is_not_certification(self):
        r=run('membership_query',bits='1',positions=[0])['value'];self.assertTrue(r['possible']);self.assertFalse(r['actual_membership_established'])
    def test_occupancy_is_exact(self):self.assertEqual(run('occupancy_fraction',bits='1010000')['value'],'2/7')
    def test_union_commutes(self):
        a=run('compatible_union',left='1010',right='0110',profile_left='p',profile_right='p');b=run('compatible_union',left='0110',right='1010',profile_left='p',profile_right='p');self.assertEqual(a,b)
    def test_union_rejects_profile_mismatch(self):self.assertEqual(run('compatible_union',left='1',right='1',profile_left='p',profile_right='q')['value'],{'refused':'profile_mismatch'})
    def test_intersection_is_pointwise_subset(self):
        r=run('intersection_bound',left='10101',right='11100')['value'];self.assertEqual(r['bits'],'10100');self.assertFalse(r['underlying_set_intersection_certified'])
    def test_complement_is_involution_not_membership_proof(self):
        a=run('complement_nonmembership',bits='00101')['value'];b=run('complement_nonmembership',bits=a['bits'])['value'];self.assertEqual(b['bits'],'00101');self.assertFalse(b['complement_set_filter_certified'])
    def test_empty_confusion_denominator_is_absent(self):self.assertIsNone(run('finite_confusion',bits='000',queries=[])['value']['false_positive_fraction'])
    def test_conditional_model_matches_tuple_enumeration(self):
        for m in range(1,6):
            for s in range(m+1):
                for k in range(1,4):
                    tuples=list(itertools.product(range(m),repeat=k));yes=sum(all(p<s for p in t) for t in tuples);r=run('conditional_query_probability',width=m,occupied=s,probes=k)['value'];self.assertEqual(Fraction(r['fraction']),Fraction(yes,len(tuples)))
    def test_affine_schedule_is_declared_noncrypto(self):
        r=run('affine_probe_schedule',width=7,a=3,b=1,keys=[0,1,2])['value'];self.assertEqual(r['positions'],[1,4,0]);self.assertFalse(r['cryptographic'])
    def test_boolean_is_not_an_integer_parameter(self):self.assertFalse(run('conditional_query_probability',width=True,occupied=1,probes=1)['ok'])
    def test_float_position_is_rejected(self):self.assertFalse(run('bit_insert',bits='00',positions=[1.0])['ok'])
    def test_duplicate_query_labels_are_rejected(self):
        q={'label':'a','positions':[0],'present':False};self.assertEqual(run('finite_confusion',bits='1',queries=[q,q])['error'],'duplicate_query')
    def test_inputs_are_unchanged(self):
        p={'operation':'bit_insert','payload':{'bits':'000','positions':[1,1]}};before=copy.deepcopy(p);evaluate(p);self.assertEqual(p,before)
    def test_unknown_authority_field_is_refused(self):self.assertEqual(run('bit_shape',bits='1',authority=True),{'ok':False,'error':'unknown_payload_field','original_success_credit':0})
if __name__=='__main__':unittest.main()
