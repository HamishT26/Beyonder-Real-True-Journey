"""Bounded synthetic half-open record queries using intervaltree."""
from intervaltree import IntervalTree
from ghc_family_temporal_reports import Refusal, cli, exact_keys, finite_json, half_open, label, record_list, tick

FAMILIES = {'point_lookup', 'range_overlap', 'range_envelopment', 'conflict_pairs'}


def run(family, data):
    try:
        finite_json(data)
        if type(family) is not str or family not in FAMILIES:
            raise Refusal('unknown_family')
        keys = ['records'] if family == 'conflict_pairs' else ['records', 'point'] if family == 'point_lookup' else ['records', 'lo', 'hi']
        exact_keys(data, keys)
        fields = ['record', 'lo', 'hi'] + (['resource'] if family == 'conflict_pairs' else [])
        rows = record_list(data['records'], fields)
        tree = IntervalTree.from_tuples((row['lo'], row['hi'], row['record']) for row in rows)
        if family == 'point_lookup':
            return sorted(item.data for item in tree.at(tick(data['point'])))
        if family == 'conflict_pairs':
            by_id = {row['record']: row for row in rows}
            for row in rows:
                label(row['resource'])
            pairs = set()
            for row in rows:
                for match in tree.overlap(row['lo'], row['hi']):
                    if row['record'] != match.data and row['resource'] == by_id[match.data]['resource']:
                        pairs.add(tuple(sorted([row['record'], match.data])))
            return [list(pair) for pair in sorted(pairs)]
        half_open(data['lo'], data['hi'])
        matches = tree.overlap(data['lo'], data['hi']) if family == 'range_overlap' else tree.envelop(data['lo'], data['hi'])
        return sorted(item.data for item in matches)
    except Refusal as exc:
        return {'error': str(exc)}


if __name__ == '__main__':
    raise SystemExit(cli(run, FAMILIES))
