"""Strict finite JSON and synthetic temporal reports; no external decisions."""
import argparse
import json
import math
from pathlib import Path
import sys

FAMILIES = {'accessible_timeline', 'thos_window_readback', 'gmut_temporal_evidence_gap', 'cbr_temporal_authority_gate'}
OUTCOMES = {'completed', 'represented', 'open_gap', 'exact_gate'}


class Refusal(ValueError):
    """A stable bounded-input refusal with no raw input in its message."""


def finite_json(value):
    """Refuse ambiguous JSON types, unbounded trees, and invalid Unicode."""
    pending = [(value, 0)]
    count = 0
    while pending:
        item, depth = pending.pop()
        count += 1
        if count > 4096 or depth > 24:
            raise Refusal('json_budget')
        if item is None or type(item) is bool:
            continue
        if type(item) in (int, float):
            if abs(item) > 1000000 or not math.isfinite(item):
                raise Refusal('nonfinite_or_large_number')
        elif type(item) is str:
            if len(item) > 4096:
                raise Refusal('string_budget')
            try:
                item.encode('utf-8')
            except UnicodeError as exc:
                raise Refusal('invalid_unicode') from exc
        elif type(item) is list:
            pending.extend((part, depth + 1) for part in item)
        elif type(item) is dict:
            if any(type(key) is not str for key in item):
                raise Refusal('nonstring_key')
            pending.extend((part, depth + 1) for part in item.values())
            pending.extend((key, depth + 1) for key in item)
        else:
            raise Refusal('non_json_type')
    if len(json.dumps(value, ensure_ascii=False).encode('utf-8')) > 65536:
        raise Refusal('byte_budget')
    return value


def exact_keys(value, names):
    if type(value) is not dict or set(value) != set(names):
        raise Refusal('unexpected_fields')


def tick(value):
    if type(value) is not int or abs(value) > 1000000:
        raise Refusal('invalid_tick')
    return value


def half_open(lo, hi):
    tick(lo)
    tick(hi)
    if lo >= hi:
        raise Refusal('invalid_window')


def label(value):
    if type(value) is not str or not value or len(value) > 80:
        raise Refusal('invalid_label')
    if any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_- ' for c in value):
        raise Refusal('invalid_label')
    return value


def record_list(value, keys):
    if type(value) is not list or len(value) > 64:
        raise Refusal('record_budget')
    seen = set()
    for row in value:
        exact_keys(row, keys)
        ident = label(row['record'])
        if ident in seen:
            raise Refusal('duplicate_record')
        seen.add(ident)
        if 'lo' in keys:
            half_open(row['lo'], row['hi'])
    return value


def pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Refusal('duplicate_member')
        result[key] = value
    return result


def load_json_bytes(data):
    if len(data) > 65536:
        raise Refusal('byte_budget')
    try:
        value = json.loads(data.decode('utf-8'), object_pairs_hook=pairs_no_duplicates,
                           parse_constant=lambda _: (_ for _ in ()).throw(Refusal('nonfinite_json')))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Refusal('invalid_json') from exc
    return finite_json(value)


def run(family, data):
    try:
        finite_json(data)
        if type(family) is not str:
            raise Refusal('unknown_family')
        if family == 'accessible_timeline':
            exact_keys(data, ['records'])
            rows = record_list(data['records'], ['record', 'lo', 'hi', 'outcome'])
            if any(type(row['outcome']) is not str or row['outcome'] not in OUTCOMES for row in rows):
                raise Refusal('unknown_outcome')
            ordered = sorted(rows, key=lambda row: (row['lo'], row['hi'], row['record']))
            lines = [f"{r['record']} | [{r['lo']}, {r['hi']}) ticks | {r['outcome']}" for r in ordered]
            return {'rows': lines, 'manual_review_reserved': True, 'real_authority': False}
        dispositions = {'thos_window_readback': 'represented', 'gmut_temporal_evidence_gap': 'open_gap', 'cbr_temporal_authority_gate': 'exact_gate'}
        if family not in dispositions:
            raise Refusal('unknown_family')
        exact_keys(data, ['obligation', 'evidence', 'authority', 'external_action'])
        if type(data['obligation']) is not str or not data['obligation'].strip():
            raise Refusal('missing_obligation')
        if data['external_action'] is not False:
            raise Refusal('external_action_refused')
        if data['evidence'] is not None or data['authority'] is not None:
            raise Refusal('unverified_external_record')
        return dispositions[family]
    except Refusal as exc:
        return {'error': str(exc)}


def cli(executor, families):
    parser = argparse.ArgumentParser(description='Evaluate one bounded synthetic temporal JSON request; never authorize external action.')
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        request = load_json_bytes(args.input.read_bytes())
        exact_keys(request, ['family', 'input'])
        if type(request['family']) is not str or request['family'] not in families:
            raise Refusal('unknown_family')
        result = executor(request['family'], request['input'])
        finite_json(result)
    except (OSError, Refusal) as exc:
        result = {'error': str(exc) if isinstance(exc, Refusal) else 'input_unavailable'}
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, allow_nan=False, indent=2) + '\n'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as output:
        output.write(payload)
    print(json.dumps({'written': True, 'same_owner_software_only': True, 'external_action': False}))
    return 0


if __name__ == '__main__':
    sys.exit(cli(run, FAMILIES))
