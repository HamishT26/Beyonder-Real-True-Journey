"""Evidence builder for the immutable x1 contracts; runtime imports no oracle."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from ghc_family_cfg_core import evaluate, strict_loads

ROOT = Path(__file__).resolve().parents[2]


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(',', ':')).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n', encoding='utf-8', newline='\n')


def run():
    rows = strict_loads((ROOT / 'x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']
    directory = ROOT / 'x2/contracts'
    directory.mkdir(exist_ok=False)
    results = []
    for index, proposal in enumerate(rows, 1):
        request = copy.deepcopy(proposal['input'])
        before = canonical(request)
        observed = evaluate(request)
        matches = canonical(observed) == canonical(proposal['expected'])
        unchanged = canonical(request) == before
        result = {'schema': 'ghc.family.cfg.contract-result.v1', 'proposal_id': proposal['proposal_id'],
                  'input': proposal['input'], 'expected': proposal['expected'], 'observed': observed,
                  'input_sha256': digest(proposal['input']), 'expected_sha256': digest(proposal['expected']),
                  'observed_sha256': digest(observed), 'hash_domain': 'ASCII-escaped sorted compact JSON UTF-8',
                  'whole_envelope_equal': matches, 'input_unchanged': unchanged,
                  'outcome': observed['disposition'] if matches and unchanged else 'open_gap',
                  'same_owner_only': True, 'independent_reproduction': False, 'source': 'ac9f049a165005776a2aec4c451e654c3d08013b',
                  'x1': '5ed797b5674205dc6f9928a804f77d44decc149d'}
        save(directory / f'{index:03}.json', result)
        results.append(result)
    save(ROOT / 'x2/execution-summary.json', {'schema': 'ghc.family.cfg.execution.v1', 'contracts': len(results),
          'passed': sum(r['whole_envelope_equal'] and r['input_unchanged'] for r in results),
          'outcomes': dict(Counter(r['outcome'] for r in results)), 'inherited_execution_credit': 0,
          'source_canonical_replayed': False, 'empirical_credit': 0, 'independent_reproduction': False})
    assert all(r['whole_envelope_equal'] and r['input_unchanged'] for r in results), 'Retain failed outputs; do not change x1.'
    by_id = {p['proposal_id']: p for p in rows}
    portfolio = strict_loads((ROOT / 'x1/approval-portfolio.json').read_text(encoding='utf-8'))
    output = {}
    for group in ['safe_now', 'candidates', 'clean_fix_refine']:
        outcomes = []
        for task in portfolio[group]:
            proposal = by_id[task['proposal_id']]
            request = copy.deepcopy(proposal['input'])
            before = canonical(request)
            procedure = task['procedure']
            observed_envelope = None
            if procedure == 'whole_envelope':
                observed_envelope = evaluate(request)
                predicate = canonical(observed_envelope) == canonical(proposal['expected'])
            elif procedure == 'input_nonmutation':
                observed_envelope = evaluate(request)
                predicate = before == canonical(request)
            elif procedure == 'unknown_top_field_refusal':
                request['undeclared_field'] = 'synthetic scope challenge'
                observed_envelope = evaluate(request)
                predicate = observed_envelope['accepted']
            elif procedure == 'duplicate_nonterminal_refusal':
                request['grammar']['nonterminals'].append(request['grammar']['nonterminals'][0])
                observed_envelope = evaluate(request)
                predicate = observed_envelope['accepted']
            elif procedure == 'canonical_json_roundtrip':
                observed_envelope = evaluate(strict_loads(before.decode('utf-8')))
                predicate = canonical(observed_envelope) == canonical(proposal['expected'])
            elif procedure == 'authority_poisoned_envelope_refusal':
                observed_envelope = evaluate(request)
                observed_envelope['boundary']['authority_granted'] = True
                predicate = canonical(observed_envelope) == canonical(proposal['expected'])
            elif procedure == 'missing_production_rhs_refusal':
                if request['grammar']['productions']:
                    del request['grammar']['productions'][0]['rhs']
                else:
                    request['grammar']['productions'].append({'lhs': request['grammar']['start']})
                observed_envelope = evaluate(request)
                predicate = observed_envelope['accepted']
            else:
                raise AssertionError(procedure)
            record = {'task_id': task['task_id'], 'proposal_id': task['proposal_id'], 'procedure': procedure,
                      'request': request, 'observed_envelope': observed_envelope, 'observed_predicate': predicate,
                      'expected_predicate': task['expected_result'], 'validation_passed': predicate is task['expected_result'],
                      'witness_result': 'pass' if predicate else 'fail', 'failed_witness_credit': 0,
                      'novelty_credit': 0, 'same_owner_only': True}
            if 'category' in task:
                record['category'] = task['category']
            outcomes.append(record)
        output[group] = outcomes
    for group in ['exact_packets', 'blocked_packets']:
        output[group] = [{'packet_id': packet['packet_id'], 'action': packet['action'], 'executed': False,
                          'outcome': 'exact_gate', 'novelty_credit': 0} for packet in portfolio[group]]
    output['schema'] = 'ghc.family.cfg.portfolio-results.v1'
    output['counts'] = {group: len(output[group]) for group in ['safe_now', 'candidates', 'clean_fix_refine', 'exact_packets', 'blocked_packets']}
    output['validation_passed'] = all(row['validation_passed'] for group in ['safe_now', 'candidates', 'clean_fix_refine'] for row in output[group])
    output['execution_vs_refusal'] = 'A passing refusal predicate retains a failed subject witness with zero proposal or authority credit.'
    save(ROOT / 'x2/portfolio-results.json', output)
    assert output['validation_passed']
    ambiguous_alphabet = {'nonterminals': ['S'], 'terminals': ['a', 'b', 'ab'], 'start': 'S',
                          'productions': [{'lhs': 'S', 'rhs': ['a', 'b']}, {'lhs': 'S', 'rhs': ['ab']}]}
    scope_request = {'op': 'cfg_bounded_language', 'grammar': ambiguous_alphabet, 'max_steps': 1, 'max_length': 2}
    refusal = evaluate(scope_request)
    structural = evaluate({'op': 'cfg_shape', 'grammar': ambiguous_alphabet})
    assert not refusal['accepted'] and structural['accepted']
    save(ROOT / 'x2/scope-clarification.json', {
        'schema': 'ghc.family.cfg.scope-clarification.v1', 'x1_modified': False, 'frozen_cases_affected': 0,
        'issue': 'The frozen string result schema cannot distinguish concatenated multi-character terminal tokens.',
        'distinct_token_sequences': [['a', 'b'], ['ab']], 'naive_joined_strings': ['ab', 'ab'],
        'limited_operations': ['cfg_derivation_validate', 'cfg_bounded_language', 'cfg_bounded_derivation_counts', 'cfg_ambiguity_witness'],
        'resolution': 'Require one-character terminal alphabets for these four operations; structural and spaced-text operations retain token boundaries.',
        'request': scope_request, 'refusal': refusal, 'structural_control': structural,
        'failed_witness_credit': 0, 'canonical_profile_conformance_outside_frozen_cases': False,
        'new_proposal_credit': 0, 'future_revision_requires_new_contract': True})
    print(json.dumps({'contracts': 200, 'outcomes': dict(Counter(r['outcome'] for r in results)),
                      'portfolio_counts': output['counts'], 'portfolio_validation_passed': output['validation_passed']}))


if __name__ == '__main__':
    run()
