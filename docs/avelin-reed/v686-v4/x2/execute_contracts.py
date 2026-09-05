"""Execute the frozen Avelin contract portfolio with retained adverse inputs."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runners'))
SOURCE = 'c5cdc995c99bca100f5a63a4f3f23e932d9433a5'
X1 = '5fbfddafacbfdae773777a7e7591b473797491a5'
DOMAIN = 'compact UTF-8 sorted-key finite JSON'
MODULES = {name: importlib.import_module('ghc_family_temporal_' + name) for name in ['intervals', 'windows', 'journals', 'guards', 'reports']}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def write(relative, value):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(value, output, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        output.write('\n')


def evaluate(proposal):
    return MODULES[proposal['runner']].run(proposal['family'], copy.deepcopy(proposal['input']))


def report_for(proposal, result):
    return {'schema': 'ghc.family.temporal-contract-report.v1', 'proposal': proposal['proposal_id'],
            'definition_sha256': proposal['definition_sha256'], 'input_sha256': digest(proposal['input']),
            'result': result, 'result_sha256': digest(result), 'disposition': proposal['expected_execution_disposition'],
            'scope': {'owner': 'Avelin Reed', 'phase': 'v686-v4', 'source': SOURCE, 'x1': X1},
            'hash_domain': DOMAIN, 'synthetic': True, 'empirical': False, 'authority': False}


def validate_report(proposal, report):
    try:
        if type(report) is not dict:
            return False
        expected = report_for(proposal, proposal['expected_result'])
        return canonical(report) == canonical(expected)
    except (ValueError, TypeError, OverflowError, UnicodeError):
        return False


def main():
    proposals = read('x1/new-proposals.json')['proposals']
    rows = []
    reports = {}
    failures = []
    for proposal in proposals:
        definition = {k: v for k, v in proposal.items() if k != 'definition_sha256'}
        if digest(definition) != proposal['definition_sha256']:
            raise ValueError('Frozen definition mismatch')
        original = copy.deepcopy(proposal['input'])
        actual = MODULES[proposal['runner']].run(proposal['family'], proposal['input'])
        matched = canonical(actual) == canonical(proposal['expected_result'])
        unchanged = canonical(original) == canonical(proposal['input'])
        envelope = report_for(proposal, actual)
        valid = validate_report(proposal, envelope)
        row = {'proposal_id': proposal['proposal_id'], 'actual': actual, 'expected': proposal['expected_result'],
               'oracle_matched': matched, 'input_unchanged': unchanged, 'report_valid': valid,
               'outcome': proposal['expected_execution_disposition'], 'report': envelope}
        rows.append(row)
        reports[proposal['proposal_id']] = envelope
        if not (matched and unchanged and valid):
            failures.append(row['proposal_id'])
    write('x2/contract-results.json', {'schema': 'ghc.family.contract-results.v686.v4', 'rows': rows, 'count': len(rows), 'failures': failures})
    if failures:
        print(json.dumps({'status': 'FAIL', 'failing_proposals': failures}))
        return 1

    by_id = {p['proposal_id']: p for p in proposals}
    negatives = []

    def retain(adverse_id, kind, proposal, invalid):
        accepted = validate_report(proposal, invalid)
        recovered = validate_report(proposal, reports[proposal['proposal_id']])
        record = {'negative_id': adverse_id, 'kind': kind, 'proposal_id': proposal['proposal_id'],
                  'invalid_report': invalid, 'invalid_accepted': accepted, 'initial_success_credit': 0,
                  'corrected_report_sha256': digest(reports[proposal['proposal_id']]), 'bounded_recovery_passed': recovered,
                  'same_owner_only': True, 'independent_reproduction': False}
        negatives.append(record)
        if accepted or not recovered:
            raise ValueError('Adverse contract did not reject or recovery failed: ' + adverse_id)
        return record

    mutations = []
    for proposal in proposals:
        for ordinal, kind in enumerate(proposal['preregistered_mutations'], 1):
            invalid = copy.deepcopy(reports[proposal['proposal_id']])
            if kind == 'wrong_definition_digest':
                invalid['definition_sha256'] = '0' * 64
            elif kind == 'wrong_input_digest':
                invalid['input_sha256'] = '0' * 64
            elif kind == 'missing_scope':
                invalid.pop('scope')
            elif kind == 'empirical_promotion':
                invalid['empirical'] = True
            elif kind == 'authority_promotion':
                invalid['authority'] = True
            mutations.append(retain(proposal['proposal_id'] + f'-M{ordinal}', kind, proposal, invalid))
    write('x2/registered-mutations.json', {'schema': 'ghc.family.mutations.v686.v4', 'count': len(mutations), 'all_rejected': True, 'rows': mutations})

    plan = read('x1/portfolio-plan.json')
    safe = []
    for task in plan['safe_tasks']:
        row = next(r for r in rows if r['proposal_id'] == task['proposal_id'])
        passed = row['oracle_matched'] if task['kind'] == 'frozen_oracle' else row['input_unchanged']
        safe.append({**task, 'outcome': 'completed', 'pass': passed, 'witness': task['kind'],
                     'result_binding': digest(row['report']), 'execution_counting': 'One scheduled assertion; shared execution is not independent evidence.'})
    candidate_rows = []
    for index, task in enumerate(plan['candidate_tasks']):
        proposal = by_id[task['proposal_id']]
        invalid = copy.deepcopy(reports[task['proposal_id']])
        if task['kind'] == 'changed_report_value':
            invalid['result'] = {'fabricated': True}
            invalid['result_sha256'] = digest(invalid['result'])
        else:
            invalid = copy.deepcopy(reports[proposals[(index + 1) % len(proposals)]['proposal_id']])
        witness = retain(task['work_id'], task['kind'], proposal, invalid)
        candidate_rows.append({**task, 'outcome': 'completed', 'pass': not witness['invalid_accepted'], 'negative_id': witness['negative_id']})
    correction_rows = []
    for task in plan['clean_fix_refine']:
        proposal = by_id[task['proposal_id']]
        invalid = copy.deepcopy(reports[task['proposal_id']])
        if task['kind'] == 'CLEAN_extra_field':
            invalid['unregistered'] = 'fixture'
        elif task['kind'] == 'FIX_changed_result':
            invalid['result'] = {'fabricated': True}
        else:
            invalid.pop('hash_domain')
        witness = retain(task['work_id'], task['kind'], proposal, invalid)
        correction_rows.append({**task, 'outcome': 'completed', 'initial_pass': False,
                                'corrected_pass': witness['bounded_recovery_passed'], 'negative_id': witness['negative_id']})
    write('x2/portfolio-results.json', {'schema': 'ghc.family.portfolio-results.v686.v4', 'safe_tasks': safe,
                                      'candidate_tasks': candidate_rows, 'clean_fix_refine': correction_rows,
                                      'exact_packets': plan['exact_packets'], 'blocked_packets': plan['blocked_packets']})
    write('x2/retained-adverse-records.json', {'schema': 'ghc.family.retained-adverse.v686.v4', 'count': len(negatives), 'rows': negatives, 'erased_negative_count': 0})
    from collections import Counter
    summary = {'schema': 'ghc.family.contract-summary.v686.v4', 'source': SOURCE, 'x1': X1,
               'oracle_matches': len(rows), 'input_nonmutation_matches': len(rows), 'mutations_rejected': len(mutations),
               'safe_tasks': len(safe), 'candidates_rejected': len(candidate_rows), 'corrections_passed': len(correction_rows),
               'exact_unexecuted': len(plan['exact_packets']), 'blocked_unexecuted': len(plan['blocked_packets']),
               'retained_adverse_records': len(negatives), 'outcomes': dict(Counter(r['outcome'] for r in rows)),
               'same_owner_only': True, 'independent_reproduction': False, 'terminal_verdict': 'NOT_READY_FOR_STAGE_20'}
    write('x2/contract-summary.json', summary)
    print(json.dumps(summary))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
