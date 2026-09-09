"""Independent finite-model implications and explicit inference limitations."""
import copy,importlib.util,itertools,json,pathlib,sys,unittest
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_inference_core import evaluate
from ghc_family_capacity_core import typed_equal
from hypothesis import given,settings,strategies as st

class EvidenceInvariants(unittest.TestCase):
    def test_beta_exchangeability_and_nonzero_uncertainty(self):
        a=evaluate({'op':'beta_update','alpha':1,'beta':1,'outcomes':[1,0,1]})['value']
        b=evaluate({'op':'beta_update','alpha':1,'beta':1,'outcomes':[1,1,0]})['value']
        self.assertEqual(a,b);self.assertGreater(F(a['variance']),0);self.assertFalse(a['empirical'])

    def test_likelihood_expectation_under_declared_null(self):
        for n in range(1,7):
            ratios=[F(evaluate({'op':'lr_path','null':'1/2','alternative':'3/4','outcomes':list(x)})['value']['path'][-1]) for x in itertools.product([0,1],repeat=n)]
            self.assertEqual(sum(ratios)/2**n,1)

    def test_correlated_marginals_do_not_supply_conditional_null(self):
        paths=[evaluate({'op':'lr_path','null':'1/2','alternative':'3/4','outcomes':[b]*4})['value']['path'] for b in [0,1]]
        crossing=F(sum(max(map(F,p))>=4 for p in paths),2)
        self.assertEqual(crossing,F(1,2));self.assertGreater(crossing,F(1,4))

    def test_erasure_increases_binary_decision_risk(self):
        good=evaluate({'op':'bayes_risk','joint':[['1/2',0],[0,'1/2']],'loss':[[0,1],[1,0]]})['value']
        erased=evaluate({'op':'bayes_risk','joint':[['1/2'],['1/2']],'loss':[[0,1],[1,0]]})['value']
        self.assertEqual(good['risk'],'0');self.assertEqual(erased['risk'],'1/2');self.assertFalse(erased['public_decision'])

    def test_channel_joint_preserves_probability_and_prior(self):
        out=evaluate({'op':'channel_joint','prior':['1/3','2/3'],'channel':[['1/4','3/4'],['1/2','1/2']]})['value']
        self.assertEqual([sum(map(F,r)) for r in out['joint']],[F(1,3),F(2,3)])
        self.assertEqual(sum(map(F,out['observation'])),1)

    def test_acceptance_and_opaque_attempts_block_resend_state(self):
        for state in ['accepted','unknown']:
            out=evaluate({'op':'checkpoint','events':[['p','h',state],['p','h','prepared']]})
            self.assertEqual(out['error'],'E_TERMINAL')
        out=evaluate({'op':'checkpoint','events':[['p','h','accepted']]})['value']
        self.assertEqual(out['messages_sent'],0)

    def test_purpose_and_expiry_cannot_borrow_consent(self):
        request={'op':'consent_scope','subject':'synthetic','purpose':'archive','now':10,'grant':{'subject':'synthetic','purposes':['archive'],'expires':10,'revoked':False}}
        self.assertFalse(evaluate(request)['value']['model_eligible'])
        request['now']=9;self.assertTrue(evaluate(request)['value']['model_eligible']);self.assertFalse(evaluate(request)['value']['real_consent_verified'])

    def test_conflict_removes_only_the_affected_reviewer(self):
        out=evaluate({'op':'appeal_cover','decisions':['a','b'],'reviewers':{'a':['r','s'],'b':['r']},'conflicts':[['a','r'],['b','r']]})['value']
        self.assertEqual(out['uncovered'],['b']);self.assertFalse(out['legitimacy_verified'])

    def test_retry_expectation_agrees_with_closed_form(self):
        for n in range(1,7):
            out=evaluate({'op':'retry_budget','failure_probability':'2/3','max_attempts':n,'base_delay':1})['value']
            self.assertEqual(F(out['expected_attempts']),(1-F(2,3)**n)/(1-F(2,3)));self.assertEqual(out['submissions'],0)

    def test_projection_returns_detached_containers(self):
        original={'nested':[{'x':1}]};out=evaluate({'op':'record_projection','record':original,'path':['nested']})['value']['value'];out[0]['x']=9
        self.assertEqual(original,{'nested':[{'x':1}]})

    def test_changed_workload_cannot_make_cost_comparison_valid(self):
        out=evaluate({'op':'paired_gain','before':[10,20],'after':[1,2],'same_workload_and_results':False})['value']
        self.assertFalse(out['comparable']);self.assertIsNone(out['cost_ratio']);self.assertIsNone(out['saving'])

    @settings(max_examples=40,derandomize=True,database=None,deadline=None)
    @given(st.recursive(st.one_of(st.none(),st.booleans(),st.integers(-100,100),st.text(alphabet='abc/01',max_size=6)),lambda children:st.one_of(st.lists(children,max_size=4),st.dictionaries(st.text(alphabet='ab/01',max_size=4),children,max_size=4)),max_leaves=15))
    def test_typed_record_refinement_roundtrip_property(self,value):
        p=ROOT/'docs/seren-talewood/v689-v2-r3/x1/ghc_family_portfolio_execute.py';spec=importlib.util.spec_from_file_location('r3_codec_property',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        original=copy.deepcopy(value);rebuilt=mod.rebuild(mod.flatten(value));self.assertTrue(typed_equal(rebuilt,original));self.assertTrue(typed_equal(value,original))

if __name__=='__main__':unittest.main()
