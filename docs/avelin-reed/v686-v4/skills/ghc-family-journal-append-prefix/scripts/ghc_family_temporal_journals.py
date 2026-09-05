"""Persistent synthetic journals, correction graphs, and temporal projections."""
from pyrsistent import freeze, thaw
from ghc_family_temporal_reports import Refusal, cli, exact_keys, finite_json, label, record_list, tick

FAMILIES = {'journal_append', 'journal_prefix', 'correction_frontier', 'asof_projection'}


def run(family, data):
    try:
        finite_json(data)
        if type(family) is not str:
            raise Refusal('unknown_family')
        if family in {'journal_append', 'journal_prefix'}:
            exact_keys(data, ['journal', 'entry'] if family == 'journal_append' else ['journal', 'length'])
            if type(data['journal']) is not list or len(data['journal']) > 64:
                raise Refusal('journal_budget')
            original = freeze(data['journal'])
            if family == 'journal_append':
                updated = original.append(freeze(data['entry']))
                return {'prior': thaw(original), 'next': thaw(updated), 'prior_unchanged': thaw(original) == data['journal']}
            n = data['length']
            if type(n) is not int or not 0 <= n <= len(original):
                raise Refusal('invalid_prefix')
            return thaw(original[:n])
        if family == 'correction_frontier':
            exact_keys(data, ['records'])
            rows = record_list(data['records'], ['record', 'parent'])
            records = {row['record']: row['parent'] for row in rows}
            for parent in records.values():
                if parent is not None:
                    label(parent)
                    if parent not in records:
                        raise Refusal('missing_parent')
            for start in records:
                trail = set()
                cursor = start
                while cursor is not None:
                    if cursor in trail:
                        raise Refusal('cycle')
                    trail.add(cursor)
                    cursor = records[cursor]
            return sorted(set(records) - {p for p in records.values() if p is not None})
        if family == 'asof_projection':
            exact_keys(data, ['records', 'recorded_cut', 'valid_tick'])
            rows = record_list(data['records'], ['record', 'recorded', 'lo', 'hi', 'value'])
            cut, valid = tick(data['recorded_cut']), tick(data['valid_tick'])
            for row in rows:
                tick(row['recorded'])
            return sorted(row['record'] for row in rows if row['recorded'] <= cut and row['lo'] <= valid < row['hi'])
        raise Refusal('unknown_family')
    except Refusal as exc:
        return {'error': str(exc)}


if __name__ == '__main__':
    raise SystemExit(cli(run, FAMILIES))
