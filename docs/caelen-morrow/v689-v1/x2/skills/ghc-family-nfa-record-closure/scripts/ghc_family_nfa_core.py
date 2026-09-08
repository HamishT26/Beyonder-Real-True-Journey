"""Bounded synthetic NFA and regex evidence core for Caelen Morrow v689-v1."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import pathlib
import re
import sys

EPS = "epsilon"
OPS = [
    "nfa_shape", "nfa_epsilon_closure", "nfa_move", "nfa_run_states",
    "nfa_accepts", "nfa_reachable", "nfa_live", "nfa_determinize",
    "nfa_subset_trace", "nfa_epsilon_eliminate", "nfa_shortest", "nfa_words",
    "nfa_word_count", "nfa_finite", "regex_token_profile", "regex_membership",
    "regex_nfa_comparison", "nfa_transition_text", "nfa_provenance",
    "nfa_authority_reservation",
]
ENVELOPE = {
    "synthetic": True,
    "external_actions": 0,
    "empirical_credit": 0,
    "independent_reproduction": False,
    "authority_granted": False,
}
REQUIRED = {
    "nfa_shape": {"op", "machine"},
    "nfa_epsilon_closure": {"op", "machine", "seeds"},
    "nfa_move": {"op", "machine", "states", "symbol"},
    "nfa_run_states": {"op", "machine", "word"},
    "nfa_accepts": {"op", "machine", "word"},
    "nfa_reachable": {"op", "machine"},
    "nfa_live": {"op", "machine"},
    "nfa_determinize": {"op", "machine"},
    "nfa_subset_trace": {"op", "machine", "word"},
    "nfa_epsilon_eliminate": {"op", "machine"},
    "nfa_shortest": {"op", "machine"},
    "nfa_words": {"op", "machine", "max_length"},
    "nfa_word_count": {"op", "machine", "length"},
    "nfa_finite": {"op", "machine"},
    "regex_token_profile": {"op", "pattern"},
    "regex_membership": {"op", "pattern", "word"},
    "regex_nfa_comparison": {"op", "pattern", "machine", "max_length"},
    "nfa_transition_text": {"op", "machine"},
    "nfa_provenance": {"op", "machine", "source_label", "declared_digest", "review"},
    "nfa_authority_reservation": {"op", "action", "requested"},
}
AUTHORITY_ACTIONS = {
    "deploy_nfa_parser", "operate_real_controller", "issue_real_identity",
    "certify_formal_safety", "approve_legal_rights", "ratify_cultural_interpretation",
    "approve_maori_wording", "assert_privacy_complete", "assert_empirical_gmut",
    "promote_stage20",
}


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def accepted(value, disposition="completed"):
    return {"accepted": True, "error": None, "value": value, "disposition": disposition, "boundary": ENVELOPE}


def rejected(error):
    return {"accepted": False, "error": error, "value": None, "disposition": "completed", "boundary": ENVELOPE}


def validate_word(word, alphabet):
    return isinstance(word, str) and len(word) <= 128 and all(symbol in alphabet for symbol in word)


def validate_machine(machine):
    if not isinstance(machine, dict) or set(machine) != {"states", "alphabet", "initial", "finals", "transitions"}:
        return False
    states, alphabet = machine["states"], machine["alphabet"]
    if not isinstance(states, list) or not 1 <= len(states) <= 32 or len(states) != len(set(states)):
        return False
    if any(not isinstance(state, str) or not re.fullmatch(r"[A-Za-z0-9_]{1,32}", state) for state in states):
        return False
    if not isinstance(alphabet, list) or not 1 <= len(alphabet) <= 8 or len(alphabet) != len(set(alphabet)):
        return False
    if any(not isinstance(symbol, str) or not re.fullmatch(r"[a-z]", symbol) for symbol in alphabet):
        return False
    if machine["initial"] not in states or not isinstance(machine["finals"], list) or not set(machine["finals"]) <= set(states):
        return False
    if len(machine["finals"]) != len(set(machine["finals"])) or not isinstance(machine["transitions"], dict):
        return False
    if not set(machine["transitions"]) <= set(states):
        return False
    edges = 0
    for row in machine["transitions"].values():
        if not isinstance(row, dict) or not set(row) <= set(alphabet) | {EPS}:
            return False
        for targets in row.values():
            if not isinstance(targets, list) or not targets or len(targets) != len(set(targets)) or not set(targets) <= set(states):
                return False
            edges += len(targets)
    return edges <= 512


def closure(machine, seeds):
    seen = set(seeds)
    stack = list(seeds)
    while stack:
        state = stack.pop()
        for target in machine["transitions"].get(state, {}).get(EPS, []):
            if target not in seen:
                seen.add(target)
                stack.append(target)
    return sorted(seen)


def move(machine, states, symbol):
    targets = set()
    for state in closure(machine, states):
        targets.update(machine["transitions"].get(state, {}).get(symbol, []))
    return closure(machine, targets)


def run(machine, word):
    current = closure(machine, [machine["initial"]])
    trace = [current]
    for symbol in word:
        current = move(machine, current, symbol)
        trace.append(current)
    return trace


def accepts(machine, word):
    return bool(set(run(machine, word)[-1]) & set(machine["finals"]))


def all_words(alphabet, max_length):
    return ["".join(parts) for length in range(max_length + 1) for parts in itertools.product(sorted(alphabet), repeat=length)]


def reachable(machine):
    seen = {machine["initial"]}
    stack = [machine["initial"]]
    while stack:
        state = stack.pop()
        for targets in machine["transitions"].get(state, {}).values():
            for target in targets:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
    return sorted(seen)


def live(machine):
    reverse = {state: set() for state in machine["states"]}
    for source, row in machine["transitions"].items():
        for targets in row.values():
            for target in targets:
                reverse[target].add(source)
    seen = set(machine["finals"])
    stack = list(seen)
    while stack:
        state = stack.pop()
        for source in reverse[state]:
            if source not in seen:
                seen.add(source)
                stack.append(source)
    return sorted(seen)


def subset_name(states):
    return "{" + ",".join(states) + "}"


def determinize(machine):
    start = closure(machine, [machine["initial"]])
    queue = [start]
    seen = {tuple(start)}
    table = {}
    while queue:
        subset = queue.pop(0)
        name = subset_name(subset)
        table[name] = {}
        for symbol in machine["alphabet"]:
            target = move(machine, subset, symbol)
            name_target = subset_name(target)
            table[name][symbol] = name_target
            key = tuple(target)
            if key not in seen:
                if len(seen) >= 1024:
                    raise ValueError("subset_bound")
                seen.add(key)
                queue.append(target)
    states = [subset_name(list(item)) for item in sorted(seen)]
    finals = sorted(name for name in states if set(name[1:-1].split(",") if name != "{}" else []) & set(machine["finals"]))
    return {"initial": subset_name(start), "states": states, "finals": finals, "transitions": table}


def epsilon_eliminate(machine):
    transitions = {}
    for state in machine["states"]:
        row = {}
        for symbol in machine["alphabet"]:
            targets = move(machine, closure(machine, [state]), symbol)
            if targets:
                row[symbol] = targets
        if row:
            transitions[state] = row
    finals = sorted(state for state in machine["states"] if set(closure(machine, [state])) & set(machine["finals"]))
    return {"states": machine["states"], "alphabet": machine["alphabet"], "initial": machine["initial"], "finals": finals, "transitions": transitions, "epsilon_free": True}


def shortest(machine):
    start = closure(machine, [machine["initial"]])
    queue = [("", start)]
    seen = {tuple(start)}
    while queue:
        word, states = queue.pop(0)
        if set(states) & set(machine["finals"]):
            return word
        for symbol in sorted(machine["alphabet"]):
            target = move(machine, states, symbol)
            key = tuple(target)
            if key not in seen:
                seen.add(key)
                queue.append((word + symbol, target))
    return None


def finite_language(machine):
    dfa = determinize(machine)
    reverse = {state: set() for state in dfa["states"]}
    for source, row in dfa["transitions"].items():
        for target in row.values():
            reverse[target].add(source)
    coaccessible = set(dfa["finals"])
    stack = list(coaccessible)
    while stack:
        state = stack.pop()
        for source in reverse[state]:
            if source not in coaccessible:
                coaccessible.add(source)
                stack.append(source)
    visiting, done = set(), set()
    def has_cycle(state):
        if state in visiting:
            return True
        if state in done:
            return False
        visiting.add(state)
        for target in dfa["transitions"].get(state, {}).values():
            if target in coaccessible and has_cycle(target):
                return True
        visiting.remove(state)
        done.add(state)
        return False
    return not any(has_cycle(state) for state in sorted(coaccessible) if state not in done)


def token_profile(pattern):
    return {"characters": len(pattern), "alternations": pattern.count("|"), "stars": pattern.count("*"), "classes": pattern.count("["), "groups": pattern.count("("), "empty_pattern": pattern == ""}


def evaluate(request):
    original = copy.deepcopy(request)
    if not isinstance(request, dict) or not isinstance(request.get("op"), str):
        return rejected("fields")
    operation = request["op"]
    if operation not in REQUIRED:
        return rejected("operation")
    if set(request) != REQUIRED[operation]:
        return rejected("fields")
    machine = request.get("machine")
    if machine is not None and not validate_machine(machine):
        return rejected("machine")
    try:
        if operation == "nfa_shape":
            value = {"states": len(machine["states"]), "alphabet": len(machine["alphabet"]), "transition_edges": sum(len(targets) for row in machine["transitions"].values() for targets in row.values()), "epsilon_edges": sum(len(row.get(EPS, [])) for row in machine["transitions"].values())}
        elif operation == "nfa_epsilon_closure":
            if not isinstance(request["seeds"], list) or not request["seeds"] or not set(request["seeds"]) <= set(machine["states"]): return rejected("seeds")
            value = {"closure": closure(machine, request["seeds"]), "seeds_preserved": True}
        elif operation == "nfa_move":
            if not isinstance(request["states"], list) or not set(request["states"]) <= set(machine["states"]) or request["symbol"] not in machine["alphabet"]: return rejected("move")
            value = {"states": move(machine, request["states"], request["symbol"]), "symbol": request["symbol"]}
        elif operation in {"nfa_run_states", "nfa_accepts", "nfa_subset_trace"}:
            if not validate_word(request["word"], machine["alphabet"]): return rejected("word")
            trace = run(machine, request["word"])
            if operation == "nfa_run_states": value = {"trace": trace, "accepts": bool(set(trace[-1]) & set(machine["finals"]))}
            elif operation == "nfa_accepts": value = {"accepts": bool(set(trace[-1]) & set(machine["finals"])), "final_states": trace[-1]}
            else: value = {"trace": trace, "subset_labels": [subset_name(states) for states in trace]}
        elif operation == "nfa_reachable":
            reached = reachable(machine); value = {"reachable": reached, "unreachable": sorted(set(machine["states"]) - set(reached))}
        elif operation == "nfa_live":
            alive = live(machine); value = {"live": alive, "dead": sorted(set(machine["states"]) - set(alive))}
        elif operation == "nfa_determinize": value = determinize(machine)
        elif operation == "nfa_epsilon_eliminate": value = epsilon_eliminate(machine)
        elif operation == "nfa_shortest":
            witness = shortest(machine); value = {"word": witness, "empty_language": witness is None}
        elif operation == "nfa_words":
            length = request["max_length"]
            if isinstance(length, bool) or not isinstance(length, int) or not 0 <= length <= 8 or sum(len(machine["alphabet"]) ** n for n in range(length + 1)) > 4096: return rejected("bound")
            value = {"words": [word for word in all_words(machine["alphabet"], length) if accepts(machine, word)], "exhaustive_through_length": length, "unbounded_language_claim": False}
        elif operation == "nfa_word_count":
            length = request["length"]
            if isinstance(length, bool) or not isinstance(length, int) or not 0 <= length <= 8 or len(machine["alphabet"]) ** length > 4096: return rejected("bound")
            value = {"length": length, "count": sum(accepts(machine, word) for word in all_words(machine["alphabet"], length) if len(word) == length)}
        elif operation == "nfa_finite": value = {"finite": finite_language(machine), "scope": "declared finite nondeterministic table only"}
        elif operation in {"regex_token_profile", "regex_membership", "regex_nfa_comparison"}:
            pattern = request["pattern"]
            if not isinstance(pattern, str) or len(pattern) > 256: return rejected("pattern")
            compiled = re.compile(pattern)
            if operation == "regex_token_profile": value = token_profile(pattern)
            elif operation == "regex_membership":
                if not isinstance(request["word"], str) or len(request["word"]) > 128: return rejected("word")
                value = {"matches": compiled.fullmatch(request["word"]) is not None, "engine_scope": "Python fullmatch on supplied synthetic text"}
            else:
                length = request["max_length"]
                if isinstance(length, bool) or not isinstance(length, int) or not 0 <= length <= 8: return rejected("bound")
                mismatches = [word for word in all_words(machine["alphabet"], length) if (compiled.fullmatch(word) is not None) != accepts(machine, word)]
                value = {"mismatches": mismatches, "agrees": not mismatches, "exhaustive_through_length": length, "unbounded_equivalence_claim": False}
        elif operation == "nfa_transition_text":
            lines = [f"{source} --{symbol}--> {target}" for source in sorted(machine["states"]) for symbol in sorted(machine["transitions"].get(source, {})) for target in sorted(machine["transitions"][source][symbol])]
            result = accepted({"lines": lines, "initial": machine["initial"], "finals": sorted(machine["finals"]), "affected_user_review": False, "accessibility_conformance": False}, "represented")
            assert request == original
            return result
        elif operation == "nfa_provenance":
            if request["source_label"] is not None and not isinstance(request["source_label"], str): return rejected("source_label")
            if request["declared_digest"] is not None and (not isinstance(request["declared_digest"], str) or not re.fullmatch(r"[0-9a-f]{64}", request["declared_digest"])): return rejected("digest")
            if request["review"] != "same_owner": return rejected("review")
            actual = hashlib.sha256(canonical_bytes(machine)).hexdigest()
            missing = (["source_label"] if request["source_label"] is None else []) + (["declared_digest"] if request["declared_digest"] is None else [])
            result = accepted({"machine_sha256": actual, "source_label": request["source_label"], "digest_matches": request["declared_digest"] == actual, "missing": missing, "review": "same_owner", "real_identity_assurance": False}, "open_gap" if missing else "represented")
            assert request == original
            return result
        else:
            if request["action"] not in AUTHORITY_ACTIONS or not isinstance(request["requested"], bool): return rejected("action")
            if request["requested"]: return rejected("authority")
            result = accepted({"action": request["action"], "executed": False, "authority_granted": False, "required": "fresh action-specific evidence and competent authority"}, "exact_gate")
            assert request == original
            return result
    except (KeyError, TypeError, ValueError, re.error):
        return rejected("invalid")
    assert request == original
    return accepted(value)


def main(allowed_operations=None):
    if len(sys.argv) != 2:
        print(json.dumps(rejected("arguments"), sort_keys=True))
        return 2
    try:
        request = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print(json.dumps(rejected("json"), sort_keys=True))
        return 2
    if allowed_operations is not None and request.get("op") not in set(allowed_operations):
        print(json.dumps(rejected("operation"), sort_keys=True))
        return 2
    response = evaluate(request)
    print(json.dumps(response, ensure_ascii=False, sort_keys=True))
    return 0 if response["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
