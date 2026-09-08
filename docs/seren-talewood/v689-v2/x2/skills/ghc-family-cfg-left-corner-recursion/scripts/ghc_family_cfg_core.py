"""Bounded synthetic CFG analysis. No packages, files, network, or authority actions.

Production indices refer to the supplied order. Enumeration counts leftmost
production traces, including paths that arrive at the same sentential form.
String-valued word operations accept one-character terminal alphabets only.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, deque

OPS = (
    'cfg_shape', 'cfg_nullable', 'cfg_productive', 'cfg_reachable',
    'cfg_first', 'cfg_follow', 'cfg_predict', 'cfg_ll1_conflicts',
    'cfg_left_corner', 'cfg_left_recursive', 'cfg_unit_closure', 'cfg_unit_eliminate',
    'cfg_epsilon_variants', 'cfg_derive_step', 'cfg_derivation_validate',
    'cfg_bounded_language', 'cfg_bounded_derivation_counts', 'cfg_ambiguity_witness',
    'cfg_nullable_proof', 'cfg_derivation_text',
)
EXTRAS = {
    'cfg_epsilon_variants': {'rhs'},
    'cfg_derive_step': {'sentential', 'production', 'position'},
    'cfg_derivation_validate': {'trace'},
    'cfg_derivation_text': {'trace'},
    'cfg_bounded_language': {'max_steps', 'max_length'},
    'cfg_bounded_derivation_counts': {'max_steps', 'max_length'},
    'cfg_ambiguity_witness': {'word', 'traces'},
    'cfg_nullable_proof': {'proof'},
}
WORD_OPS = {'cfg_derivation_validate', 'cfg_bounded_language',
            'cfg_bounded_derivation_counts', 'cfg_ambiguity_witness'}
MAX_NODES = 10000


class InvalidRequest(ValueError):
    """A refused request, including an exhausted explicit resource budget."""


def require(condition):
    if not condition:
        raise InvalidRequest('invalid_request')


def boundary():
    return {'synthetic': True, 'external_actions': 0, 'empirical_credit': 0,
            'independent_reproduction': False, 'authority_granted': False}


def envelope(value=None, accepted=True, disposition='completed'):
    return {'accepted': accepted, 'error': None if accepted else 'invalid_request',
            'value': value if accepted else None,
            'disposition': disposition if accepted else 'open_gap', 'boundary': boundary()}


def fields(value, names):
    require(type(value) is dict and set(value) == set(names))


def integer(value, lower, upper):
    require(type(value) is int and lower <= value <= upper)
    return value


def symbols(value, alphabet, maximum):
    require(type(value) is list and len(value) <= maximum)
    require(all(type(symbol) is str and symbol in alphabet for symbol in value))
    return tuple(value)


def grammar(value):
    fields(value, {'nonterminals', 'terminals', 'start', 'productions'})
    for key, pattern, minimum in [('nonterminals', r'[A-Z][A-Z0-9_]{0,15}', 1),
                                   ('terminals', r'[a-z0-9][a-z0-9_]{0,15}', 0)]:
        values = value[key]
        require(type(values) is list and minimum <= len(values) <= 16)
        require(all(type(v) is str and re.fullmatch(pattern, v) for v in values))
        require(len(set(values)) == len(values))
    nonterminals, terminals = set(value['nonterminals']), set(value['terminals'])
    require(nonterminals.isdisjoint(terminals))
    require(type(value['start']) is str and value['start'] in nonterminals)
    require(type(value['productions']) is list and len(value['productions']) <= 64)
    productions = []
    for production in value['productions']:
        fields(production, {'lhs', 'rhs'})
        require(type(production['lhs']) is str and production['lhs'] in nonterminals)
        productions.append((production['lhs'], symbols(production['rhs'], nonterminals | terminals, 8)))
    require(len(set(productions)) == len(productions))
    return nonterminals, terminals, value['start'], productions


def nullable_set(productions):
    found = set()
    while True:
        before = len(found)
        for lhs, rhs in productions:
            if all(symbol in found for symbol in rhs):
                found.add(lhs)
        if len(found) == before:
            return found


def productive_set(productions, terminals):
    found = set()
    while True:
        before = len(found)
        for lhs, rhs in productions:
            if all(symbol in found or symbol in terminals for symbol in rhs):
                found.add(lhs)
        if len(found) == before:
            return found


def reachable_from(origin, edges, reflexive=True):
    found = {origin} if reflexive else set()
    pending = list(edges[origin])
    while pending:
        symbol = pending.pop()
        if symbol not in found:
            found.add(symbol)
            pending.extend(edges[symbol] - found)
    return found


def first_sequence(rhs, first, nullable, terminals):
    found = set()
    for symbol in rhs:
        if symbol in terminals:
            found.add(symbol)
            return found, False
        found.update(first[symbol])
        if symbol not in nullable:
            return found, False
    return found, True


def first_sets(nonterminals, terminals, productions, nullable):
    first = {symbol: set() for symbol in nonterminals}
    while True:
        before = sum(map(len, first.values()))
        for lhs, rhs in productions:
            found, _ = first_sequence(rhs, first, nullable, terminals)
            first[lhs].update(found)
        if sum(map(len, first.values())) == before:
            return first


def follow_sets(nonterminals, terminals, start, productions, nullable, first):
    follow = {symbol: set() for symbol in nonterminals}
    follow[start].add('$')
    while True:
        before = sum(map(len, follow.values()))
        for lhs, rhs in productions:
            for index, symbol in enumerate(rhs):
                if symbol in nonterminals:
                    tail, tail_nullable = first_sequence(rhs[index + 1:], first, nullable, terminals)
                    follow[symbol].update(tail)
                    if tail_nullable:
                        follow[symbol].update(follow[lhs])
        if sum(map(len, follow.values())) == before:
            return follow


def sorted_mapping(mapping):
    return {symbol: sorted(mapping[symbol]) for symbol in sorted(mapping)}


def leftmost(form, nonterminals):
    return next((i for i, symbol in enumerate(form) if symbol in nonterminals), None)


def step(form, production, position, nonterminals, productions):
    integer(production, 0, len(productions) - 1)
    integer(position, 0, len(form) - 1)
    require(leftmost(form, nonterminals) == position)
    lhs, rhs = productions[production]
    require(form[position] == lhs)
    result = form[:position] + rhs + form[position + 1:]
    require(len(result) <= 128)
    return result


def trace_forms(trace, start, nonterminals, productions):
    require(type(trace) is list and len(trace) <= 64)
    forms = [(start,)]
    for production in trace:
        position = leftmost(forms[-1], nonterminals)
        require(position is not None)
        forms.append(step(forms[-1], production, position, nonterminals, productions))
    return forms, leftmost(forms[-1], nonterminals) is None


def enumerate_counts(start, nonterminals, terminals, productions, max_steps, max_length):
    """Bounded leftmost path search; never merge paths or claim unbounded absence."""
    integer(max_steps, 0, 8)
    integer(max_length, 0, 8)
    by_lhs = {symbol: [] for symbol in nonterminals}
    for lhs, rhs in productions:
        by_lhs[lhs].append(rhs)
    pending = deque([((start,), 0)])
    explored = 0
    counts = Counter()
    while pending:
        form, depth = pending.popleft()
        explored += 1
        require(explored <= MAX_NODES)
        if sum(symbol in terminals for symbol in form) > max_length:
            continue
        position = leftmost(form, nonterminals)
        if position is None:
            counts[''.join(form)] += 1
        elif depth < max_steps:
            for rhs in by_lhs[form[position]]:
                child = form[:position] + rhs + form[position + 1:]
                require(len(child) <= 128)
                require(explored + len(pending) + 1 <= MAX_NODES)
                pending.append((child, depth + 1))
    return dict(sorted(counts.items(), key=lambda pair: (len(pair[0]), pair[0])))


def compute(request):
    require(type(request) is dict and type(request.get('op')) is str and request['op'] in OPS)
    op = request['op']
    fields(request, {'op', 'grammar'} | EXTRAS.get(op, set()))
    nonterminals, terminals, start, productions = grammar(request['grammar'])
    if op in WORD_OPS:
        # The frozen string result schema cannot distinguish token concatenations.
        require(all(len(terminal) == 1 for terminal in terminals))
    nullable = nullable_set(productions)
    if op == 'cfg_shape':
        return {'nonterminals': len(nonterminals), 'terminals': len(terminals),
                'productions': len(productions), 'epsilon_rules': sum(not rhs for _, rhs in productions),
                'unit_rules': sum(len(rhs) == 1 and rhs[0] in nonterminals for _, rhs in productions)}
    if op == 'cfg_nullable':
        return {'nullable': sorted(nullable)}
    if op == 'cfg_productive':
        productive = productive_set(productions, terminals)
        return {'productive': sorted(productive), 'unproductive': sorted(nonterminals - productive)}
    if op == 'cfg_reachable':
        edges = {symbol: set() for symbol in nonterminals}
        for lhs, rhs in productions:
            edges[lhs].update(symbol for symbol in rhs if symbol in nonterminals)
        reachable = reachable_from(start, edges)
        return {'reachable': sorted(reachable), 'unreachable': sorted(nonterminals - reachable)}
    if op in {'cfg_first', 'cfg_follow', 'cfg_predict', 'cfg_ll1_conflicts'}:
        first = first_sets(nonterminals, terminals, productions, nullable)
        if op == 'cfg_first':
            return {'first': sorted_mapping(first)}
        follow = follow_sets(nonterminals, terminals, start, productions, nullable, first)
        if op == 'cfg_follow':
            return {'follow': sorted_mapping(follow)}
        predict = []
        cells = {}
        for index, (lhs, rhs) in enumerate(productions):
            lookahead, empty = first_sequence(rhs, first, nullable, terminals)
            if empty:
                lookahead.update(follow[lhs])
            predict.append({'production': index, 'lookahead': sorted(lookahead)})
            for token in lookahead:
                cells.setdefault((lhs, token), []).append(index)
        if op == 'cfg_predict':
            return {'predict': predict}
        conflicts = [{'nonterminal': lhs, 'lookahead': token, 'productions': indices}
                     for (lhs, token), indices in sorted(cells.items()) if len(indices) > 1]
        return {'conflicts': conflicts, 'conflict_free': not conflicts}
    if op in {'cfg_left_corner', 'cfg_left_recursive'}:
        edges = {symbol: set() for symbol in nonterminals}
        for lhs, rhs in productions:
            for symbol in rhs:
                if symbol in terminals:
                    break
                edges[lhs].add(symbol)
                if symbol not in nullable:
                    break
        if op == 'cfg_left_corner':
            return {'left_corner': sorted_mapping(edges)}
        return {'left_recursive': sorted(symbol for symbol in nonterminals if symbol in reachable_from(symbol, edges, False))}
    if op in {'cfg_unit_closure', 'cfg_unit_eliminate'}:
        edges = {symbol: set() for symbol in nonterminals}
        for lhs, rhs in productions:
            if len(rhs) == 1 and rhs[0] in nonterminals:
                edges[lhs].add(rhs[0])
        closure = {symbol: reachable_from(symbol, edges) for symbol in nonterminals}
        if op == 'cfg_unit_closure':
            return {'unit_closure': sorted_mapping(closure)}
        output = {(symbol, rhs) for symbol in nonterminals for lhs, rhs in productions
                  if lhs in closure[symbol] and not (len(rhs) == 1 and rhs[0] in nonterminals)}
        return {'productions': [{'lhs': lhs, 'rhs': list(rhs)} for lhs, rhs in sorted(output)], 'source_mutated': False}
    if op == 'cfg_epsilon_variants':
        rhs = symbols(request['rhs'], nonterminals | terminals, 8)
        variants = {()}
        for symbol in rhs:
            variants = {prefix + (symbol,) for prefix in variants} | (variants if symbol in nullable else set())
        return {'rhs_variants': [list(v) for v in sorted(variants, key=lambda v: (len(v), v))],
                'whole_grammar_equivalence_claim': False}
    if op == 'cfg_derive_step':
        form = symbols(request['sentential'], nonterminals | terminals, 128)
        after = step(form, request['production'], request['position'], nonterminals, productions)
        return {'sentential': list(after), 'changed_position': request['position'],
                'production': request['production'], 'leftmost': True}
    if op in {'cfg_derivation_validate', 'cfg_derivation_text'}:
        forms, complete = trace_forms(request['trace'], start, nonterminals, productions)
        if op == 'cfg_derivation_validate':
            return {'forms': [list(form) for form in forms], 'complete': complete,
                    'word': ''.join(forms[-1]) if complete else None}
        return {'lines': [str(i) + ': ' + (' '.join(form) if form else '[empty]') for i, form in enumerate(forms)],
                'complete': complete, 'accessibility_conformance': False, 'affected_user_review': False}
    if op in {'cfg_bounded_language', 'cfg_bounded_derivation_counts'}:
        counts = enumerate_counts(start, nonterminals, terminals, productions, request['max_steps'], request['max_length'])
        return {('words' if op == 'cfg_bounded_language' else 'counts'): list(counts) if op == 'cfg_bounded_language' else counts,
                'max_steps': request['max_steps'], 'max_length': request['max_length'], 'unbounded_complete': False}
    if op == 'cfg_ambiguity_witness':
        word, traces = request['word'], request['traces']
        require(type(word) is str and len(word) <= 128 and all(symbol in terminals for symbol in word))
        require(type(traces) is list and len(traces) == 2)
        require(traces[0] != traces[1])
        for trace in traces:
            forms, complete = trace_forms(trace, start, nonterminals, productions)
            require(complete and ''.join(forms[-1]) == word)
        return {'word': word, 'distinct_leftmost_derivations': True, 'same_terminal_yield': True,
                'ambiguity_witness': True, 'universal_unambiguity_claim': False}
    if op == 'cfg_nullable_proof':
        proof = request['proof']
        require(type(proof) is list and len(proof) <= len(nonterminals))
        proven = set()
        for row in proof:
            fields(row, {'symbol', 'production', 'dependencies'})
            require(type(row['symbol']) is str and row['symbol'] in nonterminals and row['symbol'] not in proven)
            index = integer(row['production'], 0, len(productions) - 1)
            lhs, rhs = productions[index]
            require(lhs == row['symbol'])
            require(symbols(row['dependencies'], nonterminals, 8) == rhs)
            require(all(symbol in proven for symbol in rhs))
            proven.add(lhs)
        return {'verified_nullable': sorted(proven), 'unproven_nullable': sorted(nullable - proven),
                'certificate_valid': True, 'source_authorship_assured': False}
    raise AssertionError('unhandled operation')


def evaluate(request, allowed=None):
    try:
        if allowed is not None:
            require(type(request) is dict and type(request.get('op')) is str and request['op'] in allowed)
        value = compute(request)
        return envelope(value, disposition='represented' if request['op'] == 'cfg_derivation_text' else 'completed')
    except InvalidRequest:
        return envelope(accepted=False)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result)
        result[key] = value
    return result


def strict_loads(text):
    def reject_constant(_):
        raise InvalidRequest('invalid_request')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def cli(allowed):
    """One bounded JSON document on stdin. Output never grants external action."""
    try:
        require(len(sys.argv) == 1)
        raw = sys.stdin.buffer.read(2_000_001)
        require(len(raw) <= 2_000_000)
        request = strict_loads(raw.decode('utf-8'))
        result = evaluate(request, allowed)
    except (InvalidRequest, ValueError, UnicodeError, RecursionError):
        result = envelope(accepted=False)
    sys.stdout.write(json.dumps(result, ensure_ascii=True, allow_nan=False, sort_keys=True) + '\n')
    return 0 if result['accepted'] else 2


if __name__ == '__main__':
    raise SystemExit(cli(OPS))
