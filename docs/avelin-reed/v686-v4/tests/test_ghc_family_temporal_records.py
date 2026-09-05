"""Owner-scoped contract and invariant tests; not independent reproduction."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runners'))
sys.path.insert(0, str(ROOT / 'x2'))
import execute_contracts as lab
import ghc_family_temporal_reports as common
import ghc_family_temporal_intervals as intervals
import ghc_family_temporal_windows as windows
import ghc_family_temporal_journals as journals
import ghc_family_temporal_guards as guards

PROPOSALS = json.loads((ROOT / 'x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']


class FrozenFamilies(unittest.TestCase):
    """Each named method executes every preregistered fixture in one family."""


def family_test(family):
    def check(self):
        for proposal in PROPOSALS:
            if proposal['family'] != family:
                continue
            with self.subTest(proposal=proposal['proposal_id']):
                before = lab.digest(proposal['input'])
                actual = lab.evaluate(proposal)
                self.assertEqual(lab.canonical(actual), lab.canonical(proposal['expected_result']))
                self.assertEqual(before, lab.digest(proposal['input']))
                definition = {key: value for key, value in proposal.items() if key != 'definition_sha256'}
                self.assertEqual(lab.digest(definition), proposal['definition_sha256'])
    return check


for _family in sorted({p['family'] for p in PROPOSALS}):
    setattr(FrozenFamilies, 'test_' + _family, family_test(_family))


class IndependentInvariants(unittest.TestCase):
    """Different assertions within the same owner; the name denotes logic only."""

    def test_boolean_is_not_a_tick(self):
        self.assertEqual(intervals.run('interval_membership', {'interval': [True, 0, 2, True], 'point': True}), {'error': 'invalid_tick'})

    def test_endpoint_closure_requires_booleans(self):
        self.assertEqual(intervals.run('interval_membership', {'interval': [1, 0, 2, True], 'point': 1}), {'error': 'invalid_endpoint_closure'})

    def test_interval_set_budget(self):
        self.assertEqual(intervals.run('interval_union', {'a': [[True, 0, 1, True]] * 65, 'b': []}), {'error': 'interval_budget'})

    def test_open_contact_does_not_fill_missing_point(self):
        result = intervals.run('interval_union', {'a': [[False, 0, 2, False]], 'b': [[False, 2, 4, False]]})
        self.assertEqual(len(result), 2)
        self.assertFalse(any((lo < 2 < hi) or (lc and lo == 2) or (rc and hi == 2) for lc, lo, hi, rc in result))

    def test_interval_algebra_matches_pointwise_boolean_logic(self):
        a = [[True, -3, 2, False], [False, 4, 7, True]]
        b = [[False, -1, 5, True]]
        def member(atoms, point):
            return any((lo < point < hi) or (lc and lo == point) or (rc and hi == point) for lc, lo, hi, rc in atoms)
        for family in ['interval_union', 'interval_intersection', 'interval_difference']:
            result = intervals.run(family, {'a': a, 'b': b})
            for doubled in range(-8, 17):
                point = doubled / 2
                aa, bb = member(a, point), member(b, point)
                expected = aa or bb if family == 'interval_union' else aa and bb if family == 'interval_intersection' else aa and not bb
                self.assertEqual(member(result, point), expected)

    def test_index_matches_linear_half_open_predicate(self):
        rows = [{'record': 'a', 'lo': -2, 'hi': 3}, {'record': 'b', 'lo': 1, 'hi': 6}]
        for point in range(-3, 8):
            self.assertEqual(windows.run('point_lookup', {'records': rows, 'point': point}), sorted(r['record'] for r in rows if r['lo'] <= point < r['hi']))

    def test_index_rejects_empty_and_duplicate_records(self):
        for rows, error in [([{'record': 'a', 'lo': 2, 'hi': 2}], 'invalid_window'), ([{'record': 'a', 'lo': 0, 'hi': 2}] * 2, 'duplicate_record')]:
            self.assertEqual(windows.run('point_lookup', {'records': rows, 'point': 1}), {'error': error})

    def test_conflict_pairs_are_resource_scoped_and_order_invariant(self):
        rows = [{'record': 'a', 'lo': 0, 'hi': 3, 'resource': 'x'}, {'record': 'b', 'lo': 1, 'hi': 4, 'resource': 'y'}, {'record': 'c', 'lo': 2, 'hi': 5, 'resource': 'x'}]
        self.assertEqual(windows.run('conflict_pairs', {'records': rows}), [['a', 'c']])
        self.assertEqual(windows.run('conflict_pairs', {'records': rows[::-1]}), [['a', 'c']])

    def test_journal_append_does_not_alias_nested_input(self):
        data = {'journal': [{'a': [1]}], 'entry': {'b': [2]}}
        result = journals.run('journal_append', data)
        data['journal'][0]['a'].append(9)
        data['entry']['b'].append(8)
        self.assertEqual(result['prior'], [{'a': [1]}])
        self.assertEqual(result['next'], [{'a': [1]}, {'b': [2]}])

    def test_prefix_restoration_does_not_truncate_source(self):
        source = [{'a': 1}, {'b': 2}]
        result = journals.run('journal_prefix', {'journal': source, 'length': 1})
        result[0]['a'] = 9
        self.assertEqual(source, [{'a': 1}, {'b': 2}])

    def test_correction_branch_remains_unadjudicated(self):
        data = {'records': [{'record': 'a', 'parent': None}, {'record': 'b', 'parent': 'a'}, {'record': 'c', 'parent': 'a'}]}
        self.assertEqual(journals.run('correction_frontier', data), ['b', 'c'])

    def test_correction_cycle_cannot_invent_a_tip(self):
        self.assertEqual(journals.run('correction_frontier', {'records': [{'record': 'a', 'parent': 'b'}, {'record': 'b', 'parent': 'a'}]}), {'error': 'cycle'})

    def test_asof_projection_preserves_conflicting_records(self):
        rows = [{'record': 'a', 'lo': 0, 'hi': 5, 'recorded': 1, 'value': False}, {'record': 'b', 'lo': 0, 'hi': 5, 'recorded': 2, 'value': True}]
        self.assertEqual(journals.run('asof_projection', {'records': rows, 'recorded_cut': 2, 'valid_tick': 3}), ['a', 'b'])

    def test_expiry_endpoint_is_exclusive(self):
        self.assertEqual(guards.run('expiry_state', {'now': 6, 'lo': 2, 'hi': 6}), 'expired')

    def test_simulated_permission_refuses_numeric_synthetic_flag(self):
        self.assertEqual(guards.run('permit_window', {'records': [], 'now': 0, 'synthetic': 1}), {'error': 'real_authority_refused'})

    def test_deny_precedence_never_sets_real_authority(self):
        result = guards.run('permit_window', {'records': [{'record': 'a', 'lo': 0, 'hi': 3, 'effect': 'deny'}, {'record': 'b', 'lo': 0, 'hi': 3, 'effect': 'allow'}], 'now': 1, 'synthetic': True})
        self.assertEqual(result, {'decision': 'synthetic_deny', 'real_authority': False})

    def test_duplicate_coverage_never_doubles_duration(self):
        self.assertEqual(guards.run('coverage_budget', {'windows': [[0, 3], [0, 3], [1, 2]], 'budget': 3}), {'covered_ticks': 3, 'within_budget': True})

    def test_unknown_claim_is_refused(self):
        self.assertEqual(guards.run('evidence_gate', {'claim': [], 'evidence_class': 'synthetic', 'external_action': False}), {'error': 'unknown_claim'})

    def test_report_preserves_manual_review_boundary(self):
        result = common.run('accessible_timeline', {'records': [{'record': 'a', 'lo': 0, 'hi': 1, 'outcome': 'open_gap'}]})
        self.assertTrue(result['manual_review_reserved'])
        self.assertFalse(result['real_authority'])

    def test_actual_authority_record_is_not_accepted_as_verified(self):
        self.assertEqual(common.run('cbr_temporal_authority_gate', {'obligation': 'review', 'evidence': None, 'authority': {'approved': True}, 'external_action': False}), {'error': 'unverified_external_record'})

    def test_duplicate_json_members_are_rejected(self):
        with self.assertRaisesRegex(common.Refusal, 'duplicate_member'):
            common.load_json_bytes(b'{"a":1,"a":2}')

    def test_nonfinite_json_is_rejected(self):
        with self.assertRaises(common.Refusal):
            common.load_json_bytes(b'{"a":NaN}')

    def test_lone_surrogate_is_rejected(self):
        with self.assertRaisesRegex(common.Refusal, 'invalid_unicode'):
            common.finite_json({'a': '\ud800'})

    def test_large_integer_is_rejected_without_overflow(self):
        with self.assertRaises(common.Refusal):
            common.finite_json(10 ** 500)

    def test_deep_tree_is_refused(self):
        value = None
        for _ in range(26):
            value = [value]
        with self.assertRaisesRegex(common.Refusal, 'json_budget'):
            common.finite_json(value)

    def test_node_budget_is_refused(self):
        with self.assertRaises(common.Refusal):
            common.finite_json([0] * 4097)

    def test_nonstring_keys_are_refused(self):
        with self.assertRaisesRegex(common.Refusal, 'nonstring_key'):
            common.finite_json({1: 'a'})

    def test_wrong_family_type_is_refused_by_every_runner(self):
        for module in [common, intervals, windows, journals, guards]:
            self.assertEqual(module.run([], {}), {'error': 'unknown_family'})

    def test_forged_result_with_matching_digest_still_fails(self):
        proposal = PROPOSALS[0]
        report = lab.report_for(proposal, False)
        self.assertFalse(lab.validate_report(proposal, report))

    def test_numeric_authority_flag_is_not_false(self):
        proposal = PROPOSALS[0]
        report = lab.report_for(proposal, proposal['expected_result'])
        report['authority'] = 0
        self.assertFalse(lab.validate_report(proposal, report))

    def test_cross_contract_report_cannot_borrow_credit(self):
        report = lab.report_for(PROPOSALS[1], PROPOSALS[1]['expected_result'])
        self.assertFalse(lab.validate_report(PROPOSALS[0], report))


if __name__ == '__main__':
    unittest.main()
