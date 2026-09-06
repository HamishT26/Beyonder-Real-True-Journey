"""Strict result envelopes and explicit test-oracle decisions for local JSON data."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import rfc8785
from jsonschema import Draft202012Validator


class ContractError(ValueError):
    """A public contract refusal code, never an implicit successful operation."""


def require(condition, code):
    if not condition:
        raise ContractError(code)


def finite_json(value, depth=0):
    require(depth <= 64, 'JSON_DEPTH_LIMIT')
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float:
        require(math.isfinite(value), 'NONFINITE_JSON')
        return
    if type(value) is list:
        for item in value:
            finite_json(item, depth + 1)
        return
    if type(value) is dict:
        require(all(type(key) is str for key in value), 'JSON_STRING_KEYS_REQUIRED')
        for item in value.values():
            finite_json(item, depth + 1)
        return
    raise ContractError('INVALID_JSON_TYPE')


def strict_loads(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def nonfinite(_):
        raise ContractError('NONFINITE_JSON')
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite)
    finite_json(value)
    return value


def json_bytes(value):
    """Type-preserving report encoding; deliberately not RFC 8785 or a Git blob."""
    finite_json(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha(value):
    return hashlib.sha256(json_bytes(value)).hexdigest()


ENVELOPE = Draft202012Validator({'oneOf': [
    {'type': 'object', 'required': ['ok', 'value'],
     'properties': {'ok': {'const': True, 'type': 'boolean'}, 'value': {}},
     'additionalProperties': False},
    {'type': 'object', 'required': ['ok', 'reason'],
     'properties': {'ok': {'const': False, 'type': 'boolean'},
                    'reason': {'type': 'string', 'minLength': 1}},
     'additionalProperties': False}
]})


def result_envelope(value):
    finite_json(value)
    return ENVELOPE.is_valid(value)


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def typed_equal(value):
    require(type(value) is list and len(value) == 2, 'PAIR_REQUIRED')
    finite_json(value)
    return same(*value)


def oracle_verdict(value):
    require(type(value) is dict and set(value) == {'expected', 'observed'}, 'ORACLE_FIELDS_REQUIRED')
    expected, observed = value['expected'], value['observed']
    if not result_envelope(expected):
        return 'invalid_expectation'
    if not result_envelope(observed):
        return 'invalid_observation'
    if expected['ok'] and not observed['ok']:
        return 'unexpected_refusal'
    if observed['ok'] and not expected['ok']:
        return 'unexpected_acceptance'
    if same(expected, observed):
        return 'expectation_met'
    return 'value_mismatch' if expected['ok'] else 'reason_mismatch'


def jcs_payload(value):
    finite_json(value)
    try:
        return {'text': rfc8785.dumps(value).decode('utf-8')}
    except rfc8785.CanonicalizationError as exc:
        raise ContractError('JCS_DOMAIN') from exc


OPERATIONS = {fn.__name__: fn for fn in
              (result_envelope, typed_equal, oracle_verdict, jcs_payload)}


def evaluate(operations, operation, value):
    require(operation in operations, 'UNKNOWN_OPERATION')
    finite_json(value)
    try:
        return operations[operation](value)
    except ContractError as exc:
        return {'error': str(exc)}


def make_report(definition, observed, source, x1):
    matched = same(definition['expected_value'], observed)
    return {'case_id': definition['id'], 'source': source, 'x1': x1,
            'definition_sha256': sha(definition), 'input_sha256': sha(definition['input']),
            'expected_sha256': sha(definition['expected_value']), 'observed_sha256': sha(observed),
            'expected': definition['expected_value'], 'observed': observed,
            'expectation_met': matched, 'claim_scope': definition['claim_scope'],
            'disposition': 'completed' if matched else 'open_gap'}


def verify_report(definition, report, source, x1):
    """Integrity and honest disposition only; no independent execution attestation."""
    if type(report) is not dict or 'observed' not in report:
        return False
    try:
        return same(report, make_report(definition, report['observed'], source, x1))
    except (ContractError, KeyError, TypeError, ValueError):
        return False


def main(operations=OPERATIONS):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation', choices=sorted(operations), required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    require(len(raw) <= 2_000_000, 'INPUT_BYTE_LIMIT')
    result = evaluate(operations, args.operation, strict_loads(raw))
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
