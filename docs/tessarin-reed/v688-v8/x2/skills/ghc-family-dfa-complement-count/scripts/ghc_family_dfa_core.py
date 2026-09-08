"""Bounded deterministic finite-table projections; no external execution."""
from collections import deque
import argparse
import hashlib
import itertools
import json
import re

BOUNDARY = {'synthetic': True, 'external_actions': 0, 'empirical_credit': 0,
            'independent_reproduction': False, 'authority_granted': False}
OPS = ['dfa_shape', 'dfa_run', 'dfa_reachable', 'dfa_live',
       'dfa_complement_membership', 'dfa_word_count', 'dfa_words', 'dfa_shortest',
       'dfa_finite', 'dfa_equivalent', 'dfa_subset', 'dfa_disjoint',
       'dfa_union_membership', 'dfa_intersection_membership',
       'dfa_difference_membership', 'dfa_xor_membership', 'dfa_residual',
       'dfa_transition_text', 'dfa_provenance', 'dfa_authority_reservation']
ACTIONS = ['deploy_parser', 'operate_real_controller', 'issue_real_identity',
           'certify_formal_safety', 'approve_legal_rights',
           'ratify_cultural_interpretation', 'approve_maori_wording',
           'assert_privacy_complete', 'assert_empirical_gmut', 'promote_stage20']

class ProfileError(ValueError):
    pass

def require(condition, code):
    if not condition:
        raise ProfileError(code)

def exact(obj, fields):
    require(type(obj) is dict and set(obj) == set(fields), 'fields')

def machine(m):
    exact(m, ['states', 'alphabet', 'initial', 'finals', 'transitions'])
    states, alphabet, finals = m['states'], m['alphabet'], m['finals']
    require(type(states) is list and 1 <= len(states) <= 32, 'states')
    require(all(type(s) is str and re.fullmatch(r'[A-Za-z0-9_]{1,32}', s) for s in states), 'state_label')
    require(len(set(states)) == len(states), 'duplicate_state')
    require(type(alphabet) is list and 1 <= len(alphabet) <= 8, 'alphabet')
    require(all(type(a) is str and re.fullmatch('[a-z]', a) for a in alphabet), 'symbol')
    require(len(set(alphabet)) == len(alphabet), 'duplicate_symbol')
    require(type(m['initial']) is str and m['initial'] in states, 'initial')
    require(type(finals) is list and all(type(s) is str and s in states for s in finals), 'finals')
    require(len(set(finals)) == len(finals), 'duplicate_final')
    exact(m['transitions'], states)
    for row in m['transitions'].values():
        exact(row, alphabet)
        require(all(type(s) is str and s in states for s in row.values()), 'destination')
    return m

def word(w, alphabet):
    require(type(w) is str and len(w) <= 128 and all(a in alphabet for a in w), 'word')
    return w

def trace(m, w, start=None):
    result = [m['initial'] if start is None else start]
    for a in w:
        result.append(m['transitions'][result[-1]][a])
    return result

def accepts(m, w):
    return trace(m, w)[-1] in m['finals']

def reachable(m):
    seen = {m['initial']}
    queue = deque(seen)
    while queue:
        s = queue.popleft()
        for t in m['transitions'][s].values():
            if t not in seen:
                seen.add(t)
                queue.append(t)
    return seen

def live_states(m):
    live = set(m['finals'])
    while True:
        more = {s for s, row in m['transitions'].items() if set(row.values()) & live}
        if more <= live:
            return live
        live |= more

def shortest_word(m):
    queue = deque([(m['initial'], '')])
    seen = {m['initial']}
    while queue:
        s, w = queue.popleft()
        if s in m['finals']:
            return w
        for a in sorted(m['alphabet']):
            t = m['transitions'][s][a]
            if t not in seen:
                seen.add(t)
                queue.append((t, w + a))
    return None

def is_finite(m):
    productive = reachable(m) & live_states(m)
    colors = {}
    def cyclic(s):
        if colors.get(s) == 1:
            return True
        if colors.get(s) == 2:
            return False
        colors[s] = 1
        for t in m['transitions'][s].values():
            if t in productive and cyclic(t):
                return True
        colors[s] = 2
        return False
    return not any(cyclic(s) for s in sorted(productive) if s not in colors)

def relation(left, right, op):
    first = (left['initial'], right['initial'])
    queue = deque([(first, '')])
    seen = {first}
    while queue:
        (s, t), w = queue.popleft()
        a, b = s in left['finals'], t in right['finals']
        bad = a != b if op == 'dfa_equivalent' else a and not b if op == 'dfa_subset' else a and b
        if bad:
            return {'holds': False, 'counterexample': w, 'scope': 'complete product of declared tables'}
        for symbol in sorted(left['alphabet']):
            pair = (left['transitions'][s][symbol], right['transitions'][t][symbol])
            if pair not in seen:
                seen.add(pair)
                require(len(seen) <= 1024, 'product_budget')
                queue.append((pair, w + symbol))
    return {'holds': True, 'counterexample': None, 'scope': 'complete product of declared tables'}

def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()

def result(value=None, disposition='completed', error=None):
    return {'accepted': error is None, 'error': error, 'value': value,
            'disposition': disposition, 'boundary': dict(BOUNDARY)}

def evaluate(request, allowed=None):
    try:
        require(type(request) is dict, 'request')
        op = request.get('op')
        require(type(op) is str and op in OPS and (allowed is None or op in allowed), 'operation')
        if op == 'dfa_authority_reservation':
            exact(request, ['op', 'action', 'requested'])
            require(request['action'] in ACTIONS and request['requested'] is False, 'authority_not_granted')
            return result({'action': request['action'], 'executed': False, 'authority_granted': False,
                           'required': 'fresh action-specific evidence and competent authority'}, 'exact_gate')
        pair = op in OPS[9:16]
        extras = ['word'] if op in ['dfa_run', 'dfa_complement_membership'] or op in OPS[12:16] else ['length'] if op == 'dfa_word_count' else ['max_length'] if op == 'dfa_words' else ['prefix', 'suffix'] if op == 'dfa_residual' else ['source_label', 'declared_digest', 'review'] if op == 'dfa_provenance' else []
        exact(request, ['op'] + (['left', 'right'] if pair else ['machine']) + extras)
        m = machine(request['left'] if pair else request['machine'])
        if pair:
            other = machine(request['right'])
            require(set(m['alphabet']) == set(other['alphabet']), 'alphabet_mismatch')
        if 'word' in extras:
            w = word(request['word'], m['alphabet'])
        if op == 'dfa_shape':
            value = {'states': len(m['states']), 'alphabet': len(m['alphabet']), 'transitions': len(m['states']) * len(m['alphabet']), 'complete': True}
        elif op == 'dfa_run':
            t = trace(m, w)
            value = {'trace': t, 'final': t[-1], 'accepts': t[-1] in m['finals']}
        elif op == 'dfa_reachable':
            r = reachable(m)
            value = {'reachable': sorted(r), 'unreachable': sorted(set(m['states']) - r)}
        elif op == 'dfa_live':
            r = live_states(m)
            value = {'live': sorted(r), 'dead': sorted(set(m['states']) - r)}
        elif op == 'dfa_complement_membership':
            value = {'accepts': not accepts(m, w), 'alphabet_relative': True}
        elif op == 'dfa_word_count':
            n = request['length']
            require(type(n) is int and 0 <= n <= 128, 'length')
            counts = {s: int(s == m['initial']) for s in m['states']}
            for _ in range(n):
                new = dict.fromkeys(m['states'], 0)
                for s, count in counts.items():
                    for t in m['transitions'][s].values():
                        new[t] += count
                counts = new
            value = {'length': n, 'count': sum(counts[s] for s in m['finals'])}
        elif op == 'dfa_words':
            n = request['max_length']
            require(type(n) is int and 0 <= n <= 8, 'enumeration_length')
            require(sum(len(m['alphabet']) ** k for k in range(n + 1)) <= 4096, 'enumeration_budget')
            ws = [''.join(t) for k in range(n + 1) for t in itertools.product(sorted(m['alphabet']), repeat=k)]
            value = {'words': [w for w in ws if accepts(m, w)], 'exhaustive_through_length': n, 'unbounded_language_claim': False}
        elif op == 'dfa_shortest':
            w = shortest_word(m)
            value = {'word': w, 'empty_language': w is None}
        elif op == 'dfa_finite':
            value = {'finite': is_finite(m), 'scope': 'declared finite transition table only'}
        elif op in OPS[9:12]:
            value = relation(m, other, op)
        elif op in OPS[12:16]:
            a, b = accepts(m, w), accepts(other, w)
            v = a or b if op == 'dfa_union_membership' else a and b if op == 'dfa_intersection_membership' else a and not b if op == 'dfa_difference_membership' else a != b
            value = {'left_accepts': a, 'right_accepts': b, 'accepts': v, 'constructed_machine': False}
        elif op == 'dfa_residual':
            prefix = word(request['prefix'], m['alphabet'])
            suffix = word(request['suffix'], m['alphabet'])
            require(len(prefix) + len(suffix) <= 128, 'word')
            start = trace(m, prefix)[-1]
            t = trace(m, suffix, start)
            value = {'residual_initial': start, 'suffix_trace': t, 'accepts': t[-1] in m['finals']}
        elif op == 'dfa_transition_text':
            return result({'lines': [s + ' --' + a + '--> ' + m['transitions'][s][a] for s in sorted(m['states']) for a in sorted(m['alphabet'])], 'initial': m['initial'], 'finals': sorted(m['finals']), 'affected_user_review': False, 'accessibility_conformance': False}, 'represented')
        else:
            label, declared = request['source_label'], request['declared_digest']
            require(label is None or (type(label) is str and re.fullmatch('[A-Za-z][A-Za-z0-9_-]{0,63}', label)), 'source_label')
            require(declared is None or (type(declared) is str and re.fullmatch('[a-f0-9]{64}', declared)), 'digest')
            require(request['review'] == 'same_owner', 'review')
            actual = hashlib.sha256(encode(m)).hexdigest()
            missing = (['source_label'] if label is None else []) + (['declared_digest'] if declared is None else [])
            if declared is not None and declared != actual:
                missing.append('digest_mismatch')
            return result({'machine_sha256': actual, 'source_label': label, 'digest_matches': declared == actual, 'missing': missing, 'review': 'same_owner', 'real_identity_assurance': False}, 'open_gap' if missing else 'represented')
        return result(value)
    except ProfileError as exc:
        return result(error=str(exc))

def strict_load(text):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, 'duplicate_key')
            obj[key] = value
        return obj
    return json.loads(text, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ProfileError('nonfinite_json')))

def main(allowed=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request', help='UTF-8 synthetic JSON request file')
    args = parser.parse_args()
    with open(args.request, encoding='utf-8') as handle:
        content = handle.read(262145)
    try:
        require(len(content) <= 262144, 'request_budget')
        response = evaluate(strict_load(content), allowed)
    except (ProfileError, json.JSONDecodeError) as exc:
        response = result(error=str(exc) if isinstance(exc, ProfileError) else 'json_syntax')
    print(json.dumps(response, sort_keys=True))
    return 0 if response['accepted'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
