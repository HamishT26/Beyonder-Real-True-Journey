"""Pure bounded record selection and shared JSON/CLI contracts."""
import copy
import hashlib
import json
import math
import sys

import glom
import jmespath
import toolz
from jsonpath_ng import parse as parse_jsonpath
from jsonpath_ng.exceptions import JsonPathLexerError, JsonPathParserError

OPERATIONS = ('literal_path', 'jmes_select', 'record_group', 'jsonpath_select')


class ContractError(ValueError):
    """A deliberate, bounded input refusal."""


def require(condition, reason):
    if not condition:
        raise ContractError(reason)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def bounded_json(value, max_depth=16, max_nodes=1000, max_bytes=65536):
    stack = [(value, 1)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        require(depth <= max_depth and count <= max_nodes, 'INPUT_BUDGET')
        if type(item) is dict:
            require(all(type(k) is str for k in item), 'NON_TEXT_KEY')
            stack.extend((v, depth + 1) for v in item.values())
        elif type(item) is list:
            stack.extend((v, depth + 1) for v in item)
        else:
            require(item is None or type(item) in (str, bool, int, float), 'NON_JSON_VALUE')
            require(type(item) is not float or math.isfinite(item), 'NONFINITE_VALUE')
    require(len(canonical(value)) <= max_bytes, 'INPUT_BUDGET')


def fields(payload, names):
    require(type(payload) is dict and set(payload) == set(names), 'INVALID_FIELDS')


def text_list(value):
    return type(value) is list and all(type(v) is str for v in value)


def ok(value):
    bounded_json(value)
    return {'ok': True, 'value': copy.deepcopy(value)}


def no(reason):
    return {'ok': False, 'reason': reason}


def strict_loads(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'DUPLICATE_KEY')
            result[key] = value
        return result

    def constant(_):
        raise ContractError('INVALID_JSON')

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ContractError('INVALID_JSON') from exc


HASH_DOMAIN = 'compact UTF-8 sorted-key finite JSON'


def make_report(proposal, result, context):
    """Bind one observed result to a frozen definition and explicit owner context."""
    fields(context, ('owner','phase','source','x1'))
    definition = dict(proposal)
    claimed = definition.pop('definition_sha256')
    require(digest(definition) == claimed, 'INVALID_DEFINITION_BINDING')
    bounded_json(result)
    report = {
        'schema':'ghc.family.record-report.v1', **context,
        'proposal_id':proposal['proposal_id'], 'operation':proposal['operation'],
        'runner':proposal['runner'], 'definition_sha256':claimed,
        'input_sha256':digest(proposal['input']), 'result':copy.deepcopy(result),
        'result_sha256':digest(result),
        'disposition':proposal['expected_execution_disposition'],
        'hash_domain':HASH_DOMAIN, 'synthetic':True, 'empirical':False,
        'authority':False, 'same_owner_only':True, 'independent_reproduction':False,
    }
    report['report_sha256'] = digest(report)
    return report


def verify_report(proposal, report, context):
    """Check every field and type; this does not verify an external-world claim."""
    try:
        bounded_json(report)
        expected = make_report(proposal, proposal['expected_result'], context)
        return canonical(report) == canonical(expected)
    except (ContractError, KeyError, TypeError, ValueError, UnicodeError):
        return False


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == 'literal_path':
            fields(payload, ('document', 'path'))
            path = payload['path']
            require(type(path) is list and len(path) <= 12, 'INVALID_PATH')
            current = payload['document']
            for part in path:
                if type(current) is dict:
                    require(type(part) is str and part in current, 'MISSING_PATH')
                elif type(current) is list:
                    require(type(part) is int and 0 <= part < len(current), 'MISSING_PATH')
                else:
                    raise ContractError('MISSING_PATH')
                current = current[part]
            value = glom.glom(payload['document'], glom.Path(*path)) if path else payload['document']
            return ok(value)
        if operation in ('jmes_select', 'jsonpath_select'):
            fields(payload, ('document', 'expression'))
            expression = payload['expression']
            require(type(expression) is str and 0 < len(expression) <= 128, 'INVALID_EXPRESSION')
            try:
                if operation == 'jmes_select':
                    return ok(jmespath.search(expression, payload['document']))
                return ok([m.value for m in parse_jsonpath(expression).find(payload['document'])])
            except (jmespath.exceptions.JMESPathError, JsonPathLexerError, JsonPathParserError) as exc:
                raise ContractError('INVALID_EXPRESSION') from exc
        if operation == 'record_group':
            fields(payload, ('records', 'field'))
            rows, field = payload['records'], payload['field']
            require(type(rows) is list and type(field) is str, 'INVALID_GROUP_INPUT')
            require(all(type(r) is dict and field in r for r in rows), 'MISSING_GROUP_FIELD')
            require(all(type(r[field]) is str for r in rows), 'NON_TEXT_GROUP')
            groups = toolz.groupby(field, rows)
            return ok([{'key':k, 'records':groups[k]} for k in sorted(groups)])
        raise ContractError('UNKNOWN_OPERATION')
    except ContractError as exc:
        return no(str(exc))


def cli(evaluator):
    """Read one bounded request or a request batch from stdin; write JSON only."""
    try:
        raw = sys.stdin.buffer.read(262145)
        require(len(raw) <= 262144, 'INPUT_BUDGET')
        request = strict_loads(raw)
        if type(request) is dict and set(request) == {'requests'}:
            rows = request['requests']
            require(type(rows) is list and len(rows) <= 200, 'INVALID_BATCH')
        else:
            rows = [request]
        results = []
        for row in rows:
            fields(row, ('operation', 'input'))
            before = canonical(row['input'])
            result = evaluator(row['operation'], row['input'])
            require(before == canonical(row['input']), 'INPUT_MUTATED')
            results.append({'operation':row['operation'], 'result':result, 'input_unchanged':True})
        output = {'results':results}
        code = 0
    except ContractError as exc:
        output, code = no(str(exc)), 2
    sys.stdout.buffer.write(canonical(output) + b'\n')
    return code


if __name__ == '__main__':
    raise SystemExit(cli(evaluate))
