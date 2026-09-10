"""Counterexamples, atomicity and bounded counting invariants."""
import copy,itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ghc_family_membership_x2 import evaluate
def run(op,**payload):return evaluate({'operation':op,'payload':payload})
class CountingInvariants(unittest.TestCase):
    def test_increment_conserves_probe_multiplicity(self):self.assertEqual(run('counting_insert',counts=[0,0,0],positions=[1,1,2])['value'],[0,2,1])
    def test_insert_then_exact_decrement_restores_counts(self):
        for pos in itertools.product(range(3),repeat=3):
            pos=list(pos);before=[1,2,3];after=run('counting_insert',counts=before,positions=pos)['value'];self.assertEqual(run('guarded_decrement',counts=after,positions=pos,known_member=True)['value']['counts'],before)
    def test_unknown_member_refused_even_with_positive_counters(self):self.assertEqual(run('guarded_decrement',counts=[3],positions=[0],known_member=False)['value'],{'refused':'unknown_member'})
    def test_underflow_is_atomic(self):
        p={'counts':[2,0],'positions':[0,1],'known_member':True};before=copy.deepcopy(p);self.assertEqual(run('guarded_decrement',**p)['value'],{'refused':'underflow'});self.assertEqual(p,before)
    def test_repeated_probe_upper_bound(self):self.assertEqual(run('multiplicity_upper_bound',counts=[5],positions=[0,0])['value']['upper_bound'],2)
    def test_upper_bound_is_not_count_certification(self):self.assertFalse(run('multiplicity_upper_bound',counts=[5],positions=[0])['value']['exact_count_established'])
    def test_saturation_preserves_overflow_coordinates(self):
        r=run('saturation_hold',counts=[1,0],positions=[0,0,1],cap=1)['value'];self.assertEqual(r['overflow_positions'],[0]);self.assertFalse(r['decrement_information_preserved'])
    def test_preexisting_overcap_counter_is_refused(self):self.assertFalse(run('saturation_hold',counts=[2],positions=[0],cap=1)['ok'])
    def test_rebuild_keeps_colliding_remaining_member(self):
        r=run('retained_member_rebuild',width=1,records=[{'label':'a','positions':[0]},{'label':'b','positions':[0]}],remove='a')['value'];self.assertEqual(r['bits'],'1');self.assertEqual(r['remaining_labels'],['b'])
    def test_unknown_record_removal_refused(self):self.assertEqual(run('retained_member_rebuild',width=1,records=[],remove='x')['value'],{'refused':'unknown_record'})
    def test_conflicts_do_not_select_a_winner(self):
        r=run('record_union_conflicts',left=[{'label':'a','positions':[0]}],right=[{'label':'a','positions':[1]}])['value'];self.assertEqual(r['groups']['a'],[[0],[1]]);self.assertEqual(r['conflicts'],['a'])
    def test_returned_record_lists_are_detached(self):
        p={'left':[{'label':'a','positions':[0]}],'right':[]};r=run('record_union_conflicts',**p)['value'];r['groups']['a'][0].append(2);self.assertEqual(p['left'][0]['positions'],[0])
    def test_corruption_witness_is_explicit(self):
        r=run('corruption_witness',bits='01',members=[{'label':'a','positions':[0]},{'label':'b','positions':[1]}])['value'];self.assertEqual(r['false_negative_labels'],['a'])
    def test_shard_roundtrip_all_small_vectors(self):
        for n in range(1,6):
            for values in itertools.product('01',repeat=n):
                s=''.join(values)
                for block in range(1,4):self.assertEqual(run('shard_roundtrip',bits=s,block=block)['value']['reconstructed'],s)
    def test_undefined_fraction_is_visible(self):self.assertIn('undefined',run('accessible_filter_summary',tp=2,fp=0,tn=0,fn=0)['value']['text'])
    def test_summary_is_only_represented(self):self.assertEqual(run('accessible_filter_summary',tp=0,fp=0,tn=0,fn=0)['outcome'],'represented')
    def test_source_presence_cannot_close_authority(self):self.assertFalse(run('evidence_reservation',obligation='rights',kind='competent_authority',evidence='synthetic record',authority=None)['ok'])
    def test_integer_boolean_boundary(self):self.assertFalse(run('counting_insert',counts=[True],positions=[0])['ok'])
if __name__=='__main__':unittest.main()
