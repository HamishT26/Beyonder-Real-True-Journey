"""Synthetic expiry, permission-window, coverage, and evidence-class guards."""
from ghc_family_temporal_reports import Refusal, cli, exact_keys, finite_json, half_open, record_list, tick

FAMILIES = {'expiry_state', 'permit_window', 'coverage_budget', 'evidence_gate'}


def run(family, data):
    try:
        finite_json(data)
        if type(family) is not str:
            raise Refusal('unknown_family')
        if family == 'expiry_state':
            exact_keys(data, ['now', 'lo', 'hi'])
            now = tick(data['now'])
            half_open(data['lo'], data['hi'])
            return 'not_yet_valid' if now < data['lo'] else 'expired' if now >= data['hi'] else 'within_window'
        if family == 'permit_window':
            exact_keys(data, ['records', 'now', 'synthetic'])
            if data['synthetic'] is not True:
                raise Refusal('real_authority_refused')
            now = tick(data['now'])
            rows = record_list(data['records'], ['record', 'lo', 'hi', 'effect'])
            if any(type(row['effect']) is not str or row['effect'] not in {'allow', 'deny'} for row in rows):
                raise Refusal('unknown_effect')
            effects = {row['effect'] for row in rows if row['lo'] <= now < row['hi']}
            decision = 'synthetic_deny' if 'deny' in effects else 'synthetic_allow' if 'allow' in effects else 'no_matching_record'
            return {'decision': decision, 'real_authority': False}
        if family == 'coverage_budget':
            exact_keys(data, ['windows', 'budget'])
            budget = tick(data['budget'])
            if budget < 0 or type(data['windows']) is not list or len(data['windows']) > 64:
                raise Refusal('invalid_budget')
            windows = []
            for value in data['windows']:
                if type(value) is not list or len(value) != 2:
                    raise Refusal('invalid_window')
                half_open(*value)
                windows.append(tuple(value))
            merged = []
            for lo, hi in sorted(windows):
                if merged and lo <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(hi, merged[-1][1]))
                else:
                    merged.append((lo, hi))
            covered = sum(hi - lo for lo, hi in merged)
            return {'covered_ticks': covered, 'within_budget': covered <= budget}
        if family == 'evidence_gate':
            exact_keys(data, ['claim', 'evidence_class', 'external_action'])
            if data['external_action'] is not False:
                raise Refusal('external_action_refused')
            if type(data['evidence_class']) is not str or data['evidence_class'] not in {'synthetic', 'bounded_software'}:
                raise Refusal('unknown_evidence_class')
            claim = data['claim']
            if type(claim) is not str:
                raise Refusal('unknown_claim')
            if claim == 'local_software':
                return 'local_workflow_only'
            if claim in {'empirical', 'independent_reproduction'}:
                return 'open_gap'
            if claim in {'production_identity', 'professional', 'cultural', 'consciousness'}:
                return 'exact_gate'
            raise Refusal('unknown_claim')
        raise Refusal('unknown_family')
    except Refusal as exc:
        return {'error': str(exc)}


if __name__ == '__main__':
    raise SystemExit(cli(run, FAMILIES))
