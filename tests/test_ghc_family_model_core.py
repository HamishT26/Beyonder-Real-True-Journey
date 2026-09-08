"""Independent mathematical invariants and counterexamples for bounded models."""
import copy
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_model_core as model

P=[['3/4','1/4'],['1/2','1/2']]
PI=['2/3','1/3']
RING=[[0,1,0],[0,0,1],[1,0,0]]
THIRDS=['1/3']*3

class ModelInvariants(unittest.TestCase):
    def test_markov_evolution_preserves_probability_mass(self):
        p=['1','0']
        for _ in range(12):
            p=model.markov_step({'matrix':P,'distribution':p})
            self.assertEqual(sum(Fraction(v) for v in p),1)
            self.assertTrue(all(Fraction(v)>=0 for v in p))

    def test_stationary_solution_is_exactly_invariant(self):
        pi=model.stationary_distribution({'matrix':P})
        self.assertEqual(model.markov_step({'matrix':P,'distribution':pi}),pi)

    def test_stationarity_does_not_require_aperiodicity(self):
        self.assertEqual(model.stationary_distribution({'matrix':RING}),THIRDS)

    def test_reversal_applied_twice_recovers_the_kernel(self):
        reversed_kernel=model.time_reversal({'matrix':RING,'stationary':THIRDS})
        recovered=model.time_reversal({'matrix':reversed_kernel,'stationary':THIRDS})
        self.assertEqual(recovered,[[str(Fraction(v)) for v in row] for row in RING])

    def test_currents_are_antisymmetric_and_divergence_free(self):
        j=[[Fraction(v) for v in row] for row in model.probability_current({'matrix':RING,'stationary':THIRDS})]
        for i in range(3):
            self.assertEqual(sum(j[i]),0)
            for k in range(3):self.assertEqual(j[i][k],-j[k][i])

    def test_entropy_can_decrease_under_a_non_doubly_stochastic_channel(self):
        before=float(model.entropy({'distribution':['1/2','1/2']}))
        after=model.markov_step({'matrix':[[1,0],[1,0]],'distribution':['1/2','1/2']})
        self.assertLess(float(model.entropy({'distribution':after})),before)

    def test_relative_entropy_contracts_for_a_shared_channel(self):
        p=['1/4','3/4'];q=['1/2','1/2']
        before=float(model.relative_entropy({'p':p,'q':q})['nats'])
        after=float(model.relative_entropy({'p':model.markov_step({'matrix':P,'distribution':p}),
                                           'q':model.markov_step({'matrix':P,'distribution':q})})['nats'])
        self.assertLessEqual(after,before+2e-12)

    def test_infinite_divergence_is_not_a_large_finite_number(self):
        result=model.relative_entropy({'p':[1,0],'q':[0,1]})
        self.assertIsNone(result['nats']);self.assertEqual(result['support_mismatch'],[0])

    def test_reversible_entropy_production_is_zero(self):
        self.assertEqual(model.entropy_production({'matrix':P,'stationary':PI})['nats_per_step'],'0.000000000000')

    def test_nonlumpable_projection_disagrees_for_an_arbitrary_initial_state(self):
        coarse=model.coarse_grain({'matrix':RING,'stationary':THIRDS,'groups':[[0,1],[2]]})
        full_step=model.markov_step({'matrix':RING,'distribution':[1,0,0]})
        aggregated=[str(Fraction(full_step[0])+Fraction(full_step[1])),full_step[2]]
        projected=model.markov_step({'matrix':coarse['matrix'],'distribution':[1,0]})
        self.assertFalse(coarse['lumpable']);self.assertNotEqual(aggregated,projected)

    def test_first_hit_probabilities_obey_the_transient_recurrence(self):
        p=[[1,0,0],[0,1,0],['1/4','3/4',0]]
        h=[[Fraction(v) for v in row] for row in model.absorption_probabilities({'matrix':p,'targets':[0,1]})]
        for col in range(2):self.assertEqual(h[2][col],sum(Fraction(p[2][j])*h[j][col] for j in range(3)))

    def test_targets_are_stopping_states_even_when_original_edges_leave(self):
        self.assertEqual(model.absorption_probabilities({'matrix':[[0,1],[1,0]],'targets':[0]}),[['1'],['1']])
        self.assertEqual(model.hitting_times({'matrix':[[0,1],[1,0]],'targets':[0]}),['0','1'])

    def test_escape_probability_keeps_expected_hit_time_infinite(self):
        p=[[0,'1/2','1/2'],[0,1,0],[0,0,1]]
        self.assertEqual(model.absorption_probabilities({'matrix':p,'targets':[1]})[0],['1/2'])
        self.assertIsNone(model.hitting_times({'matrix':p,'targets':[1]})[0])

    def test_total_variation_is_symmetric_and_within_unit_bounds(self):
        p=['1/3','2/3'];q=['3/4','1/4']
        a=model.distribution_distance({'p':p,'q':q});b=model.distribution_distance({'p':q,'q':p})
        self.assertEqual(a,b);self.assertTrue(0<=Fraction(a['tv'])<=1)

    def test_independent_coupling_is_not_automatically_optimal(self):
        result=model.coupling_bounds({'p':['1/2','1/2'],'q':['1/2','1/2']})
        self.assertLess(Fraction(result['minimum_disagreement']),Fraction(result['independent_disagreement']))

    def test_matching_synthetic_consent_never_grants_authority(self):
        result=model.consent_scope_check({'grant':{'actions':['read'],'resources':['a'],'purpose':'study','expires':5,'revoked':False},
              'action':'read','resource':'a','purpose':'study','now':1})
        self.assertTrue(result['matches']);self.assertFalse(result['authority_granted'])

    def test_revoked_synthetic_consent_stays_unmatched(self):
        result=model.consent_scope_check({'grant':{'actions':['read'],'resources':['a'],'purpose':'study','expires':5,'revoked':True},
              'action':'read','resource':'a','purpose':'study','now':1})
        self.assertFalse(result['matches'] or result['authority_granted'])

    def test_represented_reviews_never_fill_completed_coverage(self):
        self.assertFalse(model.review_coverage({'required':['keyboard'],'observed':[{'area':'keyboard','state':'represented'}]})['complete'])

    def test_search_witnesses_are_verified_by_exact_substitution(self):
        for n in [2,3,5,7,11,13,17,19]:
            result=model.egyptian_fraction_search({'n':n,'max_denominator':1000000,'max_pairs':100000})
            self.assertEqual(result['coverage'],'found_within_bounds')
            witness=result['witness']
            self.assertTrue(all(type(v) is int and v>0 for v in witness))
            self.assertEqual(sum(Fraction(1,v) for v in witness),Fraction(4,n))

    def test_search_budget_exhaustion_differs_from_bounded_absence(self):
        exhausted=model.egyptian_fraction_search({'n':5,'max_denominator':10,'max_pairs':1})
        absent=model.egyptian_fraction_search({'n':5,'max_denominator':1,'max_pairs':100})
        self.assertEqual(exhausted['coverage'],'pair_budget_exhausted')
        self.assertEqual(absent['coverage'],'bounded_no_witness')

    def test_boolean_and_float_probabilities_are_refused(self):
        for value in [True,1.0,False]:
            self.assertEqual(model.evaluate({'op':'entropy','distribution':[value]})['error'],'type')

    def test_model_inputs_are_unchanged(self):
        request={'op':'coarse_grain','matrix':RING,'stationary':THIRDS,'groups':[[0,1],[2]]}
        before=copy.deepcopy(request);self.assertTrue(model.evaluate(request)['ok']);self.assertEqual(request,before)

    def test_unknown_fields_and_operations_are_refused(self):
        self.assertEqual(model.evaluate({'op':'entropy','distribution':[1],'extra':True})['error'],'schema')
        self.assertEqual(model.evaluate({'op':'unknown'})['error'],'domain')

if __name__=='__main__':unittest.main()
