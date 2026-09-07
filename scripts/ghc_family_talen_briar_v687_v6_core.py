"""Finite synthetic archive contracts. No external writes or authority grants."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import math
import pathlib
import re


class Refusal(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def rational(value):
    require(type(value) is str, 'RATIONAL_STRING_REQUIRED')
    require(len(value) <= 128 and re.fullmatch(r'[+-]?[0-9]+(?:/[0-9]+)?', value), 'INVALID_RATIONAL')
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Refusal('INVALID_RATIONAL') from error


def cif_category_cardinality(p):
    tags = p['tags']
    require(type(tags) is list and tags, 'EMPTY_HEADER')
    valid = lambda t: type(t) is str and re.fullmatch(r'_[!-~]+', t)
    require(all(valid(t) for t in tags), 'INVALID_TAG')
    lower = [t.lower() for t in tags]
    require(len(lower) == len(set(lower)), 'DUPLICATE_TAG')
    required = p['required']
    require(type(required) is list and all(valid(t) for t in required), 'INVALID_REQUIRED_TAG')
    names = [t.lower() for t in required]
    require(len(names) == len(set(names)), 'DUPLICATE_REQUIRED_TAG')
    require(set(names) <= set(lower), 'MISSING_REQUIRED_TAG')
    limit = p['max_rows']
    require(type(limit) is int and 0 <= limit <= 10000, 'INVALID_LIMIT')
    values = p['values']
    require(type(values) is list, 'INVALID_VALUES')
    require(all(type(v) is str for v in values), 'NONLEXICAL_CELL')
    require(values, 'EMPTY_LOOP')
    require(len(values) % len(tags) == 0, 'NONRECTANGULAR')
    require(len(values) // len(tags) <= limit, 'ROW_LIMIT')
    return dict(tags=tags, rows=[values[i:i+len(tags)] for i in range(0, len(values), len(tags))])


def symmetry_code_literal_boundary(p):
    require(p['profile'] == 'declared-code-literal-v1', 'UNSUPPORTED_PROFILE')
    require(p['request'] == 'inspect', 'APPLICATION_AUTHORITY_REQUIRED')
    code = p['code']
    require(code != '.', 'INAPPLICABLE')
    require(code != '?', 'UNKNOWN')
    require(type(code) is str and len(code) <= 100, 'INVALID_CODE')
    match = re.fullmatch(r'([1-9][0-9]*)_([0-9]{3})', code)
    require(match, 'INVALID_CODE')
    table = p['dictionary']
    require(type(table) is list, 'INVALID_DICTIONARY')
    by_id = {}
    for r in table:
        require(type(r) is dict and set(r) == {'code_id', 'expression'}, 'INVALID_DICTIONARY')
        require(type(r['code_id']) is str and re.fullmatch(r'[1-9][0-9]*', r['code_id']), 'INVALID_DICTIONARY')
        require(type(r['expression']) is str and 0 < len(r['expression']) <= 4096, 'INVALID_DICTIONARY')
        require(r['code_id'] not in by_id, 'DUPLICATE_CODE_ID')
        by_id[r['code_id']] = r['expression']
    require(match[1] in by_id, 'UNKNOWN_CODE_ID')
    return dict(code_id=match[1], shift_digits=match[2], expression_literal=by_id[match[1]], operation_evaluated=False)


def reflection_merge_provenance(p):
    require(p['model_family'] == 'scalar_tensor_eft', 'MODEL_FAMILY_OUTSIDE_PROFILE')
    require(p['claim'] == 'synthetic_arithmetic', 'EXTERNAL_CLAIM_HELD')
    require(type(p['rows']) is list and len(p['rows']) <= 1000, 'INVALID_ROWS')
    labels = set()
    groups = {}
    for r in p['rows']:
        require(type(r) is dict and set(r) == {'label', 'hkl', 'intensity', 'weight'}, 'ROW_SHAPE')
        label = r['label']
        require(type(label) is str and 0 < len(label) <= 128, 'INVALID_LABEL')
        require(label not in labels, 'DUPLICATE_LABEL')
        labels.add(label)
        hkl = r['hkl']
        require(type(hkl) is list and len(hkl) == 3 and all(type(x) is int for x in hkl), 'INVALID_HKL')
        intensity = rational(r['intensity'])
        weight = rational(r['weight'])
        require(weight > 0, 'NONPOSITIVE_WEIGHT')
        groups.setdefault(tuple(hkl), []).append((label, intensity, weight))
    result = []
    for hkl, records in sorted(groups.items()):
        total = sum(r[2] for r in records)
        mean = sum(r[1]*r[2] for r in records) / total
        result.append(dict(hkl=list(hkl), weighted_mean=str(mean), total_weight=str(total), members=sorted(r[0] for r in records)))
    return result


def detector_distance_uncertainty(p):
    require(p['source_kind'] == 'synthetic', 'REAL_MEASUREMENT_RESERVED')
    require(p['request'] == 'represent', 'CALIBRATION_AUTHORITY_RESERVED')
    require(p['uncertainty_kind'] == 'absolute_bound', 'UNSUPPORTED_UNCERTAINTY_KIND')
    units = dict(mm=Fraction(1), cm=Fraction(10), m=Fraction(1000))
    require(p['unit'] in units and p['target_unit'] in units, 'UNKNOWN_UNIT')
    distance = rational(p['distance'])
    require(distance > 0, 'NONPOSITIVE_DISTANCE')
    require(p['uncertainty'] is not None, 'UNCERTAINTY_ABSENT')
    bound = rational(p['uncertainty'])
    require(bound >= 0, 'NEGATIVE_UNCERTAINTY')
    require(distance-bound > 0, 'NONPOSITIVE_INTERVAL')
    scale = units[p['unit']] / units[p['target_unit']]
    return dict(interval=[str((distance-bound)*scale), str((distance+bound)*scale)], unit=p['target_unit'])


def matrix3(value, strings=False):
    require(type(value) is list and len(value) == 3 and all(type(r) is list and len(r) == 3 for r in value), 'MATRIX_SHAPE')
    if strings:
        entries = [[rational(x) for x in row] for row in value]
    else:
        require(all(type(x) is int and abs(x) <= 1000000 for row in value for x in row), 'INTEGER_MATRIX_REQUIRED')
        entries = value
    from sympy import Matrix, Rational
    return Matrix([[Rational(x.numerator, x.denominator) if isinstance(x, Fraction) else x for x in row] for row in entries])


def cell_setting_nonidentity(p):
    require(p['claim'] == 'coordinate_contract', 'STRUCTURE_IDENTITY_RESERVED')
    forward = matrix3(p['forward'])
    reverse = matrix3(p['reverse'])
    a, b = forward.det(), reverse.det()
    require(a != 0, 'SINGULAR_FORWARD')
    require(b != 0, 'SINGULAR_REVERSE')
    require(abs(a) == abs(b) == 1, 'NONUNIMODULAR')
    from sympy import eye
    require(forward*reverse == reverse*forward == eye(3), 'INVERSE_MISMATCH')
    return dict(inverse_pair=True, structure_identity_established=False)


def diffraction_image_fixity(p):
    require(p['source_kind'] == 'synthetic_bytes', 'REAL_IMAGE_RESERVED')
    require(p['request'] == 'inspect', 'PUBLICATION_RESERVED')
    require(type(p['expected_bytes']) is int and p['expected_bytes'] >= 0, 'INVALID_BYTE_COUNT')
    require(type(p['max_bytes']) is int and 0 <= p['max_bytes'] <= 1048576, 'INVALID_BYTE_LIMIT')
    require(type(p['expected_sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', p['expected_sha256']), 'INVALID_DIGEST')
    chunks = p['chunks']
    require(type(chunks) is list and len(chunks) <= 10000, 'INVALID_CHUNKS')
    require(all(type(c) is dict and set(c) == {'ordinal', 'hex'} and type(c['ordinal']) is int for c in chunks), 'INVALID_CHUNKS')
    ordinals = [c['ordinal'] for c in chunks]
    require(len(set(ordinals)) == len(ordinals), 'DUPLICATE_ORDINAL')
    require(sorted(ordinals) == list(range(len(chunks))), 'CHUNK_GAP')
    require(ordinals == list(range(len(chunks))), 'CHUNK_ORDER')
    total = 0
    digest = hashlib.sha256()
    for c in chunks:
        h = c['hex']
        require(type(h) is str and re.fullmatch(r'(?:[0-9a-fA-F]{2})*', h), 'INVALID_HEX')
        total += len(h)//2
        require(total <= p['max_bytes'], 'BYTE_LIMIT')
        digest.update(bytes.fromhex(h))
    require(total == p['expected_bytes'], 'LENGTH_MISMATCH')
    require(digest.hexdigest() == p['expected_sha256'], 'DIGEST_MISMATCH')
    return dict(bytes=total, sha256=digest.hexdigest(), chunks=len(chunks), image_authenticity_established=False)


def reciprocal_basis_orientation(p):
    require(p['model_family'] == 'scalar_tensor_eft', 'MODEL_FAMILY_OUTSIDE_PROFILE')
    require(p['claim'] == 'representation', 'EXTERNAL_CLAIM_HELD')
    require(p['ordering'] == 'columns', 'ORDERING_OUTSIDE_PROFILE')
    basis = matrix3(p['basis'], strings=True)
    determinant = basis.det()
    require(determinant != 0, 'SINGULAR_BASIS')
    dual = basis.inv().T
    return dict(determinant=str(determinant), handedness='right' if determinant > 0 else 'left', dual_basis=[[str(dual[i,j]) for j in range(3)] for i in range(3)], empirical=False)


def cif_loop_order_separation(p):
    require(p['relation'] in ['keyed', 'ordered'], 'UNSUPPORTED_RELATION')
    indexed = []
    sequences = []
    for side in ['left', 'right']:
        rows = p[side]
        require(type(rows) is list and len(rows) <= 10000, 'INVALID_ROWS')
        values = {}
        order = []
        for row in rows:
            require(type(row) is dict and set(row) == {'key', 'value'}, 'ROW_SHAPE')
            key = row['key']
            require(type(key) is str and key, 'INVALID_KEY')
            require(type(row['value']) is str, 'NONLEXICAL_CELL')
            require(key not in values, 'DUPLICATE_'+side.upper()+'_KEY')
            values[key] = row['value']
            order.append(key)
        indexed.append(values)
        sequences.append(order)
    left, right = indexed
    left_only, right_only = sorted(left.keys()-right.keys()), sorted(right.keys()-left.keys())
    changed = sorted(k for k in left.keys() & right.keys() if left[k] != right[k])
    order_changed = sequences[0] != sequences[1]
    equal = not (left_only or right_only or changed or (p['relation'] == 'ordered' and order_changed))
    return dict(equal=equal, left_only=left_only, right_only=right_only, changed=changed, order_changed=order_changed)


def structure_factor_missingness(p):
    require(p['quantity'] in ['intensity', 'amplitude', 'phase'], 'UNSUPPORTED_QUANTITY')
    require(type(p['quoted']) is bool, 'QUOTING_STATE_REQUIRED')
    token = p['token']
    def result(state, value=None, uncertainty=None, literal=None):
        return dict(state=state, value=value, standard_uncertainty=uncertainty, literal=literal, measurement_established=False)
    if token is None:
        return result('absent')
    require(type(token) is str and len(token) <= 128, 'LEXICAL_TOKEN_REQUIRED')
    if p['quoted']:
        return result('literal', literal=token)
    if token in ['?', '.']:
        return result('unknown' if token == '?' else 'inapplicable')
    match = re.fullmatch(r'(?P<number>[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE](?P<exponent>[+-]?[0-9]+))?)(?:\((?P<su>[0-9]+)\))?', token)
    require(match, 'INVALID_NUMERIC_TOKEN')
    exponent = int(match['exponent'] or 0)
    require(abs(exponent) <= 100, 'EXPONENT_LIMIT')
    value = Fraction(match['number'])
    require(p['quantity'] != 'amplitude' or value >= 0, 'NEGATIVE_AMPLITUDE')
    uncertainty = None
    if match['su'] is not None:
        mantissa = re.split('[eE]', match['number'])[0]
        decimals = len(mantissa.split('.')[1]) if '.' in mantissa else 0
        uncertainty = str(int(match['su']) * Fraction(10)**(exponent-decimals))
    return result('numeric', str(value), uncertainty)


def deposition_rollback_readback(p):
    require(p['source_kind'] == 'synthetic', 'REAL_DEPOSITION_RESERVED')
    require(p['rights'] == 'unchanged', 'RIGHTS_AUTHORITY_RESERVED')
    require(p['action'] != 'delete_history', 'DESTRUCTIVE_ACTION_RESERVED')
    require(p['action'] != 'publish', 'EXTERNAL_WRITE_RESERVED')
    require(p['action'] == 'preview', 'UNKNOWN_ACTION')
    rows = p['revisions']
    require(type(rows) is list and len(rows) <= 1000, 'INVALID_REVISIONS')
    by_label = {}
    for row in rows:
        require(type(row) is dict and set(row) == {'label', 'parent', 'digest'}, 'INVALID_REVISION')
        require(type(row['label']) is str and row['label'] and (row['parent'] is None or type(row['parent']) is str), 'INVALID_REVISION')
        require(type(row['digest']) is str and re.fullmatch(r'[0-9a-f]{64}', row['digest']), 'INVALID_REVISION')
        require(row['label'] not in by_label, 'DUPLICATE_REVISION')
        by_label[row['label']] = row
    require(all(r['parent'] is None or r['parent'] in by_label for r in rows), 'MISSING_PARENT')
    for row in rows:
        visited = set()
        label = row['label']
        while label is not None:
            require(label not in visited, 'REVISION_CYCLE')
            visited.add(label)
            label = by_label[label]['parent']
    current, target = p['current'], p['target']
    require(current in by_label, 'CURRENT_ABSENT')
    require(target in by_label, 'TARGET_ABSENT')
    require(p['readback_digest'] == by_label[current]['digest'], 'STALE_READBACK')
    require(type(p['retained']) is list and all(type(x) is str for x in p['retained']), 'INVALID_RETENTION')
    require(target in p['retained'], 'TARGET_NOT_RETAINED')
    require(current in p['retained'], 'CURRENT_NOT_RETAINED')
    ancestors = set()
    label = current
    while label is not None:
        ancestors.add(label)
        label = by_label[label]['parent']
    require(target in ancestors, 'TARGET_NOT_ANCESTOR')
    return dict(event_kind='no_change' if current == target else 'additive_rollback_preview', prior_current=current, restores_from=target, restored_digest=by_label[target]['digest'], history_erased=False, external_write=False)


OPERATIONS = {f.__name__: f for f in [cif_category_cardinality, symmetry_code_literal_boundary,
    reflection_merge_provenance, detector_distance_uncertainty, cell_setting_nonidentity,
    diffraction_image_fixity, reciprocal_basis_orientation, cif_loop_order_separation,
    structure_factor_missingness, deposition_rollback_readback]}
FIELDS = dict(cif_category_cardinality='tags values required max_rows',
    symmetry_code_literal_boundary='code dictionary profile request',
    reflection_merge_provenance='rows model_family claim',
    detector_distance_uncertainty='distance uncertainty unit target_unit uncertainty_kind source_kind request',
    cell_setting_nonidentity='forward reverse claim',
    diffraction_image_fixity='chunks expected_bytes expected_sha256 max_bytes source_kind request',
    reciprocal_basis_orientation='basis ordering model_family claim',
    cif_loop_order_separation='left right relation',
    structure_factor_missingness='token quoted quantity',
    deposition_rollback_readback='revisions current target readback_digest retained source_kind action rights')


def run(operation, payload):
    """Return a detached view. This function has no network or filesystem effects."""
    original = copy.deepcopy(payload)
    try:
        require(operation in OPERATIONS, 'UNKNOWN_OPERATION')
        require(type(payload) is dict and set(payload) == set(FIELDS[operation].split()), 'INPUT_SHAPE')
        details = OPERATIONS[operation](copy.deepcopy(payload))
        reason = None
    except Refusal as error:
        details, reason = None, str(error)
    require(type_equal(original, payload), 'INPUT_MUTATION')
    return dict(decision='HOLD' if reason else 'BOUNDED_VIEW', details=details, reason=reason,
                source_preserved=True, external_credit=False)


def type_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(type_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(type_equal(a,b) for a,b in zip(left,right))
    return left == right


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('Nonfinite JSON constant')


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('Nonfinite JSON number')
    return number


def strict_load(data):
    require(len(data) <= 2097152, 'INPUT_BYTE_LIMIT')
    return json.loads(data, object_pairs_hook=unique_pairs, parse_constant=nonfinite, parse_float=finite_float)


def cli(operation=None):
    parser = argparse.ArgumentParser(description='Bounded synthetic archive inspection only.')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    if operation is None:
        parser.add_argument('--operation', choices=sorted(OPERATIONS), required=True)
    args = parser.parse_args()
    data = strict_load(pathlib.Path(args.input).read_bytes())
    result = run(operation or args.operation, data)
    with pathlib.Path(args.output).open('x', encoding='utf-8', newline='\n') as output:
        output.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n')


if __name__ == '__main__':
    cli()
