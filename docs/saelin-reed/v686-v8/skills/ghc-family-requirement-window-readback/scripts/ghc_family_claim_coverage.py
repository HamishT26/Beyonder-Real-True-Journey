"""Read dependency, binding, obligation, and interval contracts without world claims."""
import datetime
import re
from ghc_family_contract_oracle import ContractError, main, require, same
from ghc_family_witness_pairing import labels


def dependency_partition(value):
    require(type(value) is dict and set(value) == {'required', 'available'}, 'INVALID_DEPENDENCIES')
    required = set(labels(value['required'], 'INVALID_DEPENDENCIES'))
    available = set(labels(value['available'], 'INVALID_DEPENDENCIES'))
    return {'missing': sorted(required - available), 'unused': sorted(available - required)}


def evidence_binding(value):
    if type(value) is not dict or set(value) != {'expected', 'report'}:
        return False
    for row in (value['expected'], value['report']):
        if type(row) is not dict or set(row) != {'source', 'x1', 'definition'}:
            return False
        for key, size in (('source', 40), ('x1', 40), ('definition', 64)):
            if type(row[key]) is not str or not re.fullmatch('[0-9a-f]{' + str(size) + '}', row[key]):
                return False
    return same(value['expected'], value['report'])


def requirement_readback(value):
    require(type(value) is dict and set(value) == {'requirements'}
            and type(value['requirements']) is dict, 'INVALID_REQUIREMENTS')
    unresolved = []
    for key, status in value['requirements'].items():
        require(type(key) is str and key and status in ('present', 'missing', 'contested'), 'INVALID_REQUIREMENT')
        if status != 'present':
            unresolved.append(key)
    return {'missing_or_contested': sorted(unresolved), 'world_verified': False}


def iso_date(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'INVALID_DATE')
    try:
        return datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError('INVALID_DATE') from exc


def window_contract(value):
    require(type(value) is dict, 'MAPPING_REQUIRED')
    require(set(value) == {'windows'} and type(value['windows']) is list, 'WINDOWS_REQUIRED')
    starts, ends = [], []
    for window in value['windows']:
        require(type(window) is dict and set(window) == {'start', 'end'}, 'INVALID_WINDOW')
        start, end = iso_date(window['start']), iso_date(window['end'])
        require(start <= end, 'REVERSED_WINDOW')
        starts.append(start)
        ends.append(end)
    if not starts or max(starts) > min(ends):
        return {'intersection': None}
    return {'intersection': [max(starts).isoformat(), min(ends).isoformat()]}


OPERATIONS = {fn.__name__: fn for fn in
              (dependency_partition, evidence_binding, requirement_readback, window_contract)}

if __name__ == '__main__':
    main(OPERATIONS)
