"""Keep local validation, reserved claims, and witness credit distinct."""
from ghc_family_contract_oracle import ContractError, main, require


def claim_disposition(value):
    require(type(value) is dict and set(value) == {'kind', 'passed', 'evidence'}, 'INVALID_CLAIM')
    require(value['kind'] in ('local', 'design', 'empirical', 'authority')
            and type(value['passed']) is bool
            and value['evidence'] in ('observed', 'absent', 'synthetic'), 'INVALID_CLAIM')
    if value['kind'] == 'authority':
        return 'exact_gate'
    if value['kind'] == 'design':
        return 'represented'
    if value['kind'] == 'local' and value['passed'] and value['evidence'] == 'observed':
        return 'completed'
    return 'open_gap'


def claim_ceiling(value):
    require(type(value) is dict and set(value) == {'claims'}
            and type(value['claims']) is list
            and all(type(c) is str and c for c in value['claims']), 'INVALID_CLAIMS')
    claims = sorted(set(value['claims']))
    supported = {'local_validation', 'representation'}
    return {'allowed': [c for c in claims if c in supported],
            'reserved': [c for c in claims if c not in supported]}


def counter_partition(value):
    require(type(value) is list, 'INVALID_WITNESS')
    counts = {'passes': 0, 'expected_rejections': 0, 'failures': 0, 'success_credit': 0}
    keys = {'pass': 'passes', 'rejection': 'expected_rejections', 'failure': 'failures'}
    seen = set()
    for row in value:
        require(type(row) is dict and set(row) == {'id', 'kind', 'credit'}
                and type(row['id']) is str and row['id']
                and type(row['kind']) is str and row['kind'] in keys, 'INVALID_WITNESS')
        require(row['id'] not in seen, 'DUPLICATE_WITNESS')
        seen.add(row['id'])
        credit = 1 if row['kind'] == 'pass' else 0
        require(type(row['credit']) is int and row['credit'] == credit, 'INVALID_CREDIT')
        counts[keys[row['kind']]] += 1
        counts['success_credit'] += credit
    return counts


def credit_partition(value):
    require(type(value) is dict and value.get('origin') in ('inherited', 'new'), 'INVALID_ORIGIN')
    require(set(value) == {'origin', 'validated', 'distinct_in_scope'}
            and type(value.get('validated')) is bool
            and type(value.get('distinct_in_scope')) is bool, 'INVALID_CREDIT_FLAGS')
    if value['origin'] == 'inherited':
        return {'novelty': 0, 'execution': 0}
    return {'novelty': int(value['distinct_in_scope']), 'execution': int(value['validated'])}


OPERATIONS = {fn.__name__: fn for fn in
              (claim_disposition, claim_ceiling, counter_partition, credit_partition)}

if __name__ == '__main__':
    main(OPERATIONS)
