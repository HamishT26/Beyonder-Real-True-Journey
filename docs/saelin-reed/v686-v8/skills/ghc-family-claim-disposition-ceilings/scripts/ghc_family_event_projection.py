"""Nonmutating event-log and terminal-precondition projections."""
import datetime
import re
from ghc_family_contract_oracle import ContractError, main, require, same


def append_prefix(value):
    require(type(value) is dict and set(value) == {'before', 'after'}
            and type(value['before']) is list and type(value['after']) is list, 'ARRAYS_REQUIRED')
    before, after = value['before'], value['after']
    return len(after) >= len(before) and same(before, after[:len(before)])


def correction_projection(value):
    require(type(value) is list, 'CORRECTION_ARRAY_REQUIRED')
    if not value:
        return {'history': [], 'current': None}
    nodes, children = {}, {}
    for row in value:
        require(type(row) is dict and set(row) == {'id', 'replaces', 'value'}
                and type(row['id']) is str and row['id']
                and (row['replaces'] is None or type(row['replaces']) is str), 'INVALID_CORRECTION')
        require(row['id'] not in nodes, 'DUPLICATE_CORRECTION')
        nodes[row['id']] = row
    roots = []
    for name, row in nodes.items():
        parent = row['replaces']
        if parent is None:
            roots.append(name)
        else:
            require(parent in nodes, 'MISSING_PREDECESSOR')
            require(parent not in children, 'NONLINEAR_CORRECTION')
            children[parent] = name
    require(len(roots) == 1, 'NONLINEAR_CORRECTION')
    history, current = [], roots[0]
    while current is not None:
        require(current not in history, 'NONLINEAR_CORRECTION')
        history.append(current)
        current = children.get(current)
    require(len(history) == len(nodes), 'NONLINEAR_CORRECTION')
    last = nodes[history[-1]]
    return {'history': history, 'current': {'id': last['id'], 'value': last['value']}}


def temporal_order(value):
    require(type(value) is list, 'EVENT_ARRAY_REQUIRED')
    events, seen = [], set()
    for ordinal, row in enumerate(value):
        require(type(row) is dict and set(row) == {'id', 'at'}
                and type(row['id']) is str and row['id'], 'INVALID_EVENT')
        require(row['id'] not in seen, 'DUPLICATE_EVENT')
        seen.add(row['id'])
        text = row['at']
        require(type(text) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?', text), 'INVALID_INSTANT')
        try:
            instant = datetime.datetime.fromisoformat(text.replace('Z', '+00:00'))
        except ValueError as exc:
            raise ContractError('INVALID_INSTANT') from exc
        require(instant.tzinfo is not None, 'OFFSET_REQUIRED')
        events.append((instant.astimezone(datetime.timezone.utc), ordinal, row['id']))
    return [row[2] for row in sorted(events)]


TERMINAL_FLAGS = ('sealed', 'pushed', 'clean', 'fresh_equal', 'validated',
                  'unique_recipient', 'current_authority', 'usage_available',
                  'recipient_reread', 'not_previously_sent')


def terminal_preconditions(value):
    require(type(value) is dict, 'GUARD_MAPPING_REQUIRED')
    missing = [key for key in TERMINAL_FLAGS if value.get(key) is not True]
    return {'decision': 'held' if missing else 'eligible_for_one_send',
            'missing': missing, 'send_performed': False}


OPERATIONS = {fn.__name__: fn for fn in
              (append_prefix, correction_projection, temporal_order, terminal_preconditions)}

if __name__ == '__main__':
    main(OPERATIONS)
