"""Bounded batching, catalog sorting, JSON streams, and resource accounting."""
import io
import ijson
from more_itertools import chunked
from natsort import natsorted, ns
from ghc_family_record_selection import (
    ContractError, bounded_json, canonical, cli, fields, no, ok, require,
    strict_loads, text_list,
)

OPERATIONS = ('batch_records','natural_labels','stream_items','resource_budget')


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == 'batch_records':
            fields(payload, ('items','width','strict'))
            items,width,strict=payload['items'],payload['width'],payload['strict']
            require(type(items) is list and type(strict) is bool, 'INVALID_BATCH_INPUT')
            require(type(width) is int and 1 <= width <= 1000, 'INVALID_WIDTH')
            try:
                return ok(list(chunked(items,width,strict=strict)))
            except ValueError as exc:
                raise ContractError('INCOMPLETE_BATCH') from exc
        if operation == 'natural_labels':
            fields(payload, ('labels','reverse'))
            require(text_list(payload['labels']), 'NON_TEXT_LABEL')
            require(type(payload['reverse']) is bool, 'INVALID_REVERSE')
            return ok(natsorted(payload['labels'], alg=ns.INT, reverse=payload['reverse']))
        if operation == 'stream_items':
            fields(payload, ('text','prefix'))
            text,prefix=payload['text'],payload['prefix']
            require(type(text) is str and len(text.encode('utf-8')) <= 4096, 'INPUT_BUDGET')
            require(prefix in ('item','rows.item'), 'INVALID_PREFIX')
            parsed = strict_loads(text)
            bounded_json(parsed)
            try:
                return ok(list(ijson.items(io.BytesIO(text.encode('utf-8')),prefix,use_float=True)))
            except ijson.JSONError as exc:
                raise ContractError('INVALID_JSON') from exc
        if operation == 'resource_budget':
            fields(payload, ('payload','max_depth','max_nodes','max_bytes'))
            for key,ceiling in [('max_depth',16),('max_nodes',1000),('max_bytes',65536)]:
                require(type(payload[key]) is int and 1 <= payload[key] <= ceiling, 'INVALID_BUDGET')
            stack=[(payload['payload'],1)];depth=nodes=0
            while stack:
                value,level=stack.pop();nodes+=1;depth=max(depth,level)
                if type(value) is dict: stack.extend((v,level+1) for v in value.values())
                elif type(value) is list: stack.extend((v,level+1) for v in value)
            size=len(canonical(payload['payload']))
            violations=[label for label,value,key in [('depth',depth,'max_depth'),('nodes',nodes,'max_nodes'),('bytes',size,'max_bytes')] if value>payload[key]]
            return ok({'within':not violations,'violations':violations,'depth':depth,'nodes':nodes,'utf8_bytes':size})
        raise ContractError('UNKNOWN_OPERATION')
    except ContractError as exc:
        return no(str(exc))


if __name__ == '__main__':
    raise SystemExit(cli(evaluate))
