"""Explicit local merge strategies and literal field projections."""
import copy
from boltons.iterutils import remap
import jsonmerge
from mergedeep import merge, Strategy
import pydash
from ghc_family_record_selection import (
    ContractError, bounded_json, cli, fields, no, ok, require, text_list,
)

OPERATIONS = ('typed_merge', 'schema_merge', 'recursive_prune', 'field_projection')
STRATEGIES = {'replace':Strategy.REPLACE, 'additive':Strategy.ADDITIVE,
              'typesafe_replace':Strategy.TYPESAFE_REPLACE,
              'typesafe_additive':Strategy.TYPESAFE_ADDITIVE}


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == 'typed_merge':
            fields(payload, ('left', 'right', 'strategy'))
            strategy = payload['strategy']
            require(type(strategy) is str and strategy in STRATEGIES, 'UNKNOWN_STRATEGY')
            require(type(payload['left']) is dict and type(payload['right']) is dict, 'MAPPING_REQUIRED')
            try:
                value = merge({}, copy.deepcopy(payload['left']), copy.deepcopy(payload['right']),
                              strategy=STRATEGIES[strategy])
            except TypeError as exc:
                raise ContractError('MERGE_TYPE_CONFLICT') from exc
            return ok(value)
        if operation == 'schema_merge':
            fields(payload, ('base', 'head', 'strategy'))
            strategy = payload['strategy']
            require(type(strategy) is str and strategy in ('overwrite','objectMerge','append','discard'), 'UNKNOWN_STRATEGY')
            base, head = payload['base'], payload['head']
            if strategy == 'append':
                require(type(base) is list and type(head) is list, 'MERGE_TYPE_CONFLICT')
            if strategy == 'objectMerge':
                require(type(base) is dict and type(head) is dict, 'MERGE_TYPE_CONFLICT')
            # Only a local fixed strategy is accepted; arbitrary schemas and references are excluded.
            merger = jsonmerge.Merger({'mergeStrategy':strategy})
            return ok(merger.merge(copy.deepcopy(base), copy.deepcopy(head)))
        if operation == 'recursive_prune':
            fields(payload, ('document', 'drop_keys'))
            document, drops = payload['document'], payload['drop_keys']
            require(type(document) in (dict,list), 'CONTAINER_REQUIRED')
            require(text_list(drops), 'INVALID_DROP_KEYS')
            omitted = set(drops)
            return ok(remap(document, visit=lambda path,key,value: not(type(key) is str and key in omitted)))
        if operation == 'field_projection':
            fields(payload, ('document','keys','mode'))
            document, keys, mode = payload['document'], payload['keys'], payload['mode']
            require(type(document) is dict and text_list(keys), 'INVALID_PROJECTION')
            require(mode in ('pick','omit'), 'UNKNOWN_MODE')
            chosen = set(keys)
            # Filtering original pairs avoids pydash's deep-path interpretation of dotted keys.
            selected = pydash.filter_(list(document.items()),
                                      lambda pair: (pair[0] in chosen) == (mode == 'pick'))
            return ok(dict(selected))
        raise ContractError('UNKNOWN_OPERATION')
    except ContractError as exc:
        return no(str(exc))


if __name__ == '__main__':
    raise SystemExit(cli(evaluate))
