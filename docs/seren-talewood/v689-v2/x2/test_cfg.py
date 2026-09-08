"""Owner-only semantic tests, including cases outside the frozen proposal corpus."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'x2/code'))
import ghc_family_cfg_core as cfg


def grammar(rules, nonterminals=('S',), terminals=('a', 'b')):
    return {'nonterminals': list(nonterminals), 'terminals': list(terminals), 'start': 'S',
            'productions': [{'lhs': lhs, 'rhs': list(rhs)} for lhs, rhs in rules]}


def request(op, value, **extras):
    return {'op': op, 'grammar': value, **extras}


class GrammarSemantics(unittest.TestCase):
    def test_all_frozen_contract_envelopes_and_input_fixity(self):
        rows = json.loads((ROOT / 'x1/new-proposals.json').read_text())['proposals']
        for row in rows:
            with self.subTest(proposal=row['proposal_id']):
                supplied = copy.deepcopy(row['input'])
                observed = cfg.evaluate(supplied)
                self.assertEqual(json.dumps(observed, sort_keys=True), json.dumps(row['expected'], sort_keys=True))
                self.assertEqual(supplied, row['input'])

    def test_nullable_conjunction_and_terminal_barrier(self):
        value = grammar([('S', 'AB'), ('A', ''), ('B', 'b')], ('S', 'A', 'B'))
        self.assertEqual(cfg.evaluate(request('cfg_nullable', value))['value']['nullable'], ['A'])

    def test_productivity_requires_all_rhs_nonterminals(self):
        value = grammar([('S', 'AB'), ('A', 'a'), ('B', 'B')], ('S', 'A', 'B'))
        self.assertEqual(cfg.evaluate(request('cfg_productive', value))['value'],
                         {'productive': ['A'], 'unproductive': ['B', 'S']})

    def test_reachability_is_separate_from_productivity(self):
        value = grammar([('S', 'S'), ('A', 'a')], ('S', 'A'))
        self.assertEqual(cfg.evaluate(request('cfg_reachable', value))['value']['reachable'], ['S'])
        self.assertEqual(cfg.evaluate(request('cfg_productive', value))['value']['productive'], ['A'])

    def test_first_propagates_through_two_nullable_symbols(self):
        value = grammar([('S', 'ABC'), ('A', ''), ('B', ''), ('C', 'b')], ('S', 'A', 'B', 'C'))
        self.assertEqual(cfg.evaluate(request('cfg_first', value))['value']['first']['S'], ['b'])

    def test_follow_nullable_suffix_propagation(self):
        value = grammar([('S', 'ABC'), ('A', 'a'), ('B', 'b'), ('B', ''), ('C', 'c'), ('C', '')],
                        ('S', 'A', 'B', 'C'), ('a', 'b', 'c'))
        result = cfg.evaluate(request('cfg_follow', value))['value']['follow']
        self.assertEqual(result, {'A': ['$', 'b', 'c'], 'B': ['$', 'c'], 'C': ['$'], 'S': ['$']})

    def test_predict_reports_epsilon_follow_conflict(self):
        value = grammar([('S', 'Ab'), ('A', 'b'), ('A', '')], ('S', 'A'))
        self.assertEqual(cfg.evaluate(request('cfg_ll1_conflicts', value))['value']['conflicts'],
                         [{'nonterminal': 'A', 'lookahead': 'b', 'productions': [1, 2]}])

    def test_conflicts_retain_three_competing_indices(self):
        value = grammar([('S', 'a'), ('S', 'aS'), ('S', 'aa')])
        self.assertEqual(cfg.evaluate(request('cfg_ll1_conflicts', value))['value']['conflicts'][0]['productions'], [0, 1, 2])

    def test_left_recursion_through_nullable_prefix(self):
        value = grammar([('S', 'AB'), ('A', ''), ('B', 'S')], ('S', 'A', 'B'))
        self.assertEqual(cfg.evaluate(request('cfg_left_recursive', value))['value']['left_recursive'], ['B', 'S'])

    def test_right_recursion_is_not_left_recursion(self):
        value = grammar([('S', 'aS'), ('S', '')])
        self.assertEqual(cfg.evaluate(request('cfg_left_recursive', value))['value']['left_recursive'], [])

    def test_unit_cycle_eliminates_without_losing_terminal_rules(self):
        value = grammar([('S', 'A'), ('A', 'S'), ('A', 'a')], ('S', 'A'))
        before = copy.deepcopy(value)
        result = cfg.evaluate(request('cfg_unit_eliminate', value))['value']
        self.assertEqual(result['productions'], [{'lhs': 'A', 'rhs': ['a']}, {'lhs': 'S', 'rhs': ['a']}])
        self.assertEqual(value, before)

    def test_epsilon_variants_distinguish_occurrences_and_deduplicate(self):
        value = grammar([('S', '')])
        self.assertEqual(cfg.evaluate(request('cfg_epsilon_variants', value, rhs=['S', 'S']))['value']['rhs_variants'],
                         [[], ['S'], ['S', 'S']])

    def test_derive_step_refuses_nonleftmost_rewrite(self):
        value = grammar([('S', 'a')])
        self.assertFalse(cfg.evaluate(request('cfg_derive_step', value, sentential=['S', 'S'], production=0, position=1))['accepted'])

    def test_boolean_and_negative_indices_refused(self):
        value = grammar([('S', 'a')])
        for index in [True, -1, 0.0, '0']:
            self.assertFalse(cfg.evaluate(request('cfg_derivation_validate', value, trace=[index]))['accepted'])

    def test_trace_refuses_steps_after_completion(self):
        value = grammar([('S', 'a')])
        self.assertFalse(cfg.evaluate(request('cfg_derivation_validate', value, trace=[0, 0]))['accepted'])

    def test_production_reordering_changes_index_meaning(self):
        first = grammar([('S', 'a'), ('S', 'b')])
        second = grammar([('S', 'b'), ('S', 'a')])
        self.assertEqual(cfg.evaluate(request('cfg_derivation_validate', first, trace=[0]))['value']['word'], 'a')
        self.assertEqual(cfg.evaluate(request('cfg_derivation_validate', second, trace=[0]))['value']['word'], 'b')

    def test_empty_language_and_epsilon_are_distinct(self):
        for value, words in [(grammar([]), []), (grammar([('S', '')], terminals=()), [''])]:
            self.assertEqual(cfg.evaluate(request('cfg_bounded_language', value, max_steps=1, max_length=0))['value']['words'], words)

    def test_terminal_budget_does_not_prune_nullable_sentential_forms(self):
        value = grammar([('S', 'AA'), ('A', '')], ('S', 'A'))
        self.assertEqual(cfg.evaluate(request('cfg_bounded_language', value, max_steps=3, max_length=0))['value']['words'], [''])

    def test_counts_keep_catalan_paths(self):
        value = grammar([('S', 'SS'), ('S', 'a')])
        self.assertEqual(cfg.evaluate(request('cfg_bounded_derivation_counts', value, max_steps=7, max_length=4))['value']['counts'],
                         {'a': 1, 'aa': 1, 'aaa': 2, 'aaaa': 5})

    def test_ambiguity_requires_distinct_complete_equal_yields(self):
        value = grammar([('S', 'SS'), ('S', 'a')])
        for traces, word in [([[1], [1]], 'a'), ([[0, 1], [1]], 'a'), ([[1], [0, 1, 1]], 'aa')]:
            self.assertFalse(cfg.evaluate(request('cfg_ambiguity_witness', value, traces=traces, word=word))['accepted'])

    def test_nullable_certificate_rejects_forward_and_false_dependencies(self):
        value = grammar([('S', 'A'), ('A', '')], ('S', 'A'))
        bad = [{'symbol': 'S', 'production': 0, 'dependencies': ['A']}, {'symbol': 'A', 'production': 1, 'dependencies': []}]
        self.assertFalse(cfg.evaluate(request('cfg_nullable_proof', value, proof=bad))['accepted'])
        bad[0]['dependencies'] = []
        self.assertFalse(cfg.evaluate(request('cfg_nullable_proof', value, proof=bad))['accepted'])

    def test_partial_certificate_does_not_invent_proof(self):
        value = grammar([('S', '')])
        result = cfg.evaluate(request('cfg_nullable_proof', value, proof=[]))['value']
        self.assertEqual(result['verified_nullable'], [])
        self.assertEqual(result['unproven_nullable'], ['S'])

    def test_spaced_text_retains_multichar_tokens(self):
        value = grammar([('S', ['ab', 'c'])], terminals=('ab', 'c'))
        self.assertEqual(cfg.evaluate(request('cfg_derivation_text', value, trace=[0]))['value']['lines'], ['0: S', '1: ab c'])
        self.assertFalse(cfg.evaluate(request('cfg_derivation_validate', value, trace=[0]))['accepted'])

    def test_request_structure_and_duplicate_productions_refused(self):
        valid = request('cfg_shape', grammar([('S', 'a')]))
        alterations = [[], None, {'op': 'cfg_unknown', 'grammar': valid['grammar']}, {**valid, 'authority': True}]
        duplicate = copy.deepcopy(valid)
        duplicate['grammar']['productions'] *= 2
        alterations.append(duplicate)
        for value in alterations:
            self.assertEqual(cfg.evaluate(value), cfg.envelope(accepted=False))

    def test_duplicate_json_keys_and_constants_refused(self):
        for text in ['{"op":1,"op":2}', '{"grammar":{"x":1,"x":2}}', '{"x":NaN}']:
            with self.assertRaises(ValueError):
                cfg.strict_loads(text)

    def test_resource_limits_refuse_without_partial_results(self):
        explosive = grammar([('S', 'SS'), ('S', 'SSS'), ('S', 'SSSS'), ('S', 'a')])
        self.assertEqual(cfg.evaluate(request('cfg_bounded_language', explosive, max_steps=8, max_length=8)), cfg.envelope(accepted=False))
        growth = grammar([('S', 'SSSSSSSS')])
        self.assertFalse(cfg.evaluate(request('cfg_derivation_validate', growth, trace=[0] * 20))['accepted'])
        for limit in [True, 9, -1, 3.0]:
            self.assertFalse(cfg.evaluate(request('cfg_bounded_language', growth, max_steps=limit, max_length=1))['accepted'])

    def test_scope_wrapper_and_boundary_do_not_grant_authority(self):
        value = request('cfg_shape', grammar([]))
        self.assertEqual(cfg.evaluate(value, ['cfg_nullable']), cfg.envelope(accepted=False))
        result = cfg.evaluate(value)
        self.assertEqual(result['boundary'], cfg.boundary())
        result['boundary']['authority_granted'] = True
        self.assertFalse(cfg.evaluate(value)['boundary']['authority_granted'])


if __name__ == '__main__':
    unittest.main()
