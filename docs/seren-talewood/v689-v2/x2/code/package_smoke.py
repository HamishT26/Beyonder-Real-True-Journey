"""Bounded local parser comparisons. PEG results are not CFG ambiguity proofs."""
import argparse
import importlib.metadata
import json
import sys
from pathlib import Path


def exercise(site):
    sys.path.insert(0, str(site.resolve()))
    import lark
    import tatsu
    import parsy
    for module in [lark, tatsu, parsy]:
        assert Path(module.__file__).resolve().is_relative_to(site.resolve())
    balanced_lark = lark.Lark('start: "a" start "b" |', parser='earley')
    balanced_tatsu = tatsu.compile('@@grammar :: SyntheticBalanced\nstart = pairs $;\npairs = /a/ pairs /b/ | ();')
    @parsy.generate
    def nested():
        return (yield parsy.string('a') >> balanced_parsy << parsy.string('b'))
    balanced_parsy = nested | parsy.success('')
    vectors = [(('a' * n + 'b' * n), True) for n in range(7)] + [
        ('a', False), ('b', False), ('ba', False), ('aba', False), ('abb', False),
        ('aab', False), ('aabbx', False), ('ab ab', False), ('abab', False), ('aaabbbx', False)]
    outcomes = []
    for package, parser, exception in [
            ('lark', balanced_lark.parse, lark.exceptions.UnexpectedInput),
            ('TatSu', balanced_tatsu.parse, tatsu.exceptions.FailedParse),
            ('parsy', balanced_parsy.parse, parsy.ParseError)]:
        for word, expected in vectors:
            try:
                parser(word)
                accepted = True
            except exception:
                accepted = False
            outcomes.append({'package': package, 'case': word, 'expected_membership': expected,
                             'observed_membership': accepted, 'passed': accepted is expected})
    ambiguity = lark.Lark('start: start start | "a"', parser='earley', ambiguity='explicit').parse('aaa')
    ambiguity_seen = any(tree.data == '_ambig' for tree in ambiguity.iter_subtrees())
    assert ambiguity_seen
    # Same two textual alternatives exhibit ordered-choice behavior in a PEG.
    ordered = tatsu.compile('@@grammar :: SyntheticOrdered\nstart = (/a/ | /ab/) $;')
    try:
        ordered.parse('ab')
        peg_accepted = True
    except tatsu.exceptions.FailedParse:
        peg_accepted = False
    try:
        (parsy.string('a') | parsy.string('ab')).parse('ab')
        combinator_accepted = True
    except parsy.ParseError:
        combinator_accepted = False
    assert not peg_accepted and not combinator_accepted
    return {'schema': 'ghc.family.cfg.package-smoke.v1',
            'versions': {p: importlib.metadata.version(p) for p in ['lark', 'TatSu', 'parsy']},
            'membership_checks': outcomes, 'passed': all(row['passed'] for row in outcomes),
            'lark_explicit_ambiguity_seen': ambiguity_seen,
            'ordered_choice_counterexample': {'input': 'ab', 'alternatives': ['a', 'ab'],
                                              'tatsu_accepted': peg_accepted, 'parsy_accepted': combinator_accepted,
                                              'cfg_union_would_accept': True},
            'packages_are_independent_reproduction': False, 'general_grammar_equivalence': False,
            'untrusted_grammar_compiled': False, 'network_actions_during_smoke': 0,
            'acknowledgement': 'This product includes software developed by Juancarlo Añez (https://github.com/apalala).'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    result = exercise(args.site)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'passed': result['passed'], 'membership_checks': len(result['membership_checks']),
                      'ambiguity_seen': result['lark_explicit_ambiguity_seen'], 'versions': result['versions']}))
    raise SystemExit(0 if result['passed'] else 1)
