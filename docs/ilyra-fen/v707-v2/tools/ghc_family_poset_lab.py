#!/usr/bin/env python3
"""Finite synthetic poset evidence utilities for Ilyra Fen v707-v2.

The module uses bounded exact enumeration only.  It does not model people,
institutions, rights, physical systems, or operational authority.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb
from typing import Any, Iterable


MAX_NODES = 7


class PosetRecordError(ValueError):
    """Raised when a synthetic finite-poset record is outside the contract."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def _subsets(nodes: tuple[str, ...]) -> Iterable[tuple[str, ...]]:
    for size in range(len(nodes) + 1):
        yield from combinations(nodes, size)


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != {"id", "nodes", "covers"}:
        raise PosetRecordError("record must contain exactly id, nodes, and covers")
    if not isinstance(record["id"], str) or not record["id"]:
        raise PosetRecordError("id must be a nonempty string")
    nodes = record["nodes"]
    if not isinstance(nodes, list) or not 2 <= len(nodes) <= MAX_NODES:
        raise PosetRecordError(f"nodes must be a list of length 2..{MAX_NODES}")
    if any(not isinstance(node, str) or not node for node in nodes):
        raise PosetRecordError("every node must be a nonempty string")
    if len(nodes) != len(set(nodes)):
        raise PosetRecordError("nodes must be unique")
    if nodes != sorted(nodes):
        raise PosetRecordError("nodes must be sorted")
    covers = record["covers"]
    if not isinstance(covers, list):
        raise PosetRecordError("covers must be a list")
    normalized: list[tuple[str, str]] = []
    for edge in covers:
        if not isinstance(edge, list) or len(edge) != 2 or any(not isinstance(v, str) for v in edge):
            raise PosetRecordError("every cover must be a two-string list")
        lower, upper = edge
        if lower not in nodes or upper not in nodes:
            raise PosetRecordError("cover endpoint is not declared")
        if lower == upper:
            raise PosetRecordError("self covers are forbidden")
        normalized.append((lower, upper))
    if len(normalized) != len(set(normalized)):
        raise PosetRecordError("duplicate covers are forbidden")
    if normalized != sorted(normalized):
        raise PosetRecordError("covers must be sorted")

    closure = _closure(tuple(nodes), tuple(normalized))
    for left in nodes:
        for right in nodes:
            if left != right and (left, right) in closure and (right, left) in closure:
                raise PosetRecordError("covers contain a directed cycle")
    for lower, upper in normalized:
        for middle in nodes:
            if middle not in {lower, upper} and (lower, middle) in closure and (middle, upper) in closure:
                raise PosetRecordError("declared cover is transitively redundant")
    return {"id": record["id"], "nodes": list(nodes), "covers": [list(edge) for edge in normalized]}


def _closure(nodes: tuple[str, ...], covers: tuple[tuple[str, str], ...]) -> set[tuple[str, str]]:
    relation = {(node, node) for node in nodes} | set(covers)
    changed = True
    while changed:
        changed = False
        additions = {
            (left, right)
            for left, middle in relation
            for middle2, right in relation
            if middle == middle2 and (left, right) not in relation
        }
        if additions:
            relation |= additions
            changed = True
    return relation


def closure(record: dict[str, Any]) -> set[tuple[str, str]]:
    checked = validate_record(record)
    return _closure(tuple(checked["nodes"]), tuple(tuple(edge) for edge in checked["covers"]))


def is_ideal(candidate: Iterable[str], nodes: tuple[str, ...], relation: set[tuple[str, str]]) -> bool:
    chosen = set(candidate)
    return all(lower in chosen for lower, upper in relation if upper in chosen)


def is_antichain(candidate: Iterable[str], relation: set[tuple[str, str]]) -> bool:
    values = tuple(candidate)
    return all(
        (left, right) not in relation and (right, left) not in relation
        for left, right in combinations(values, 2)
    )


def is_chain(candidate: Iterable[str], relation: set[tuple[str, str]]) -> bool:
    values = tuple(candidate)
    return all((left, right) in relation or (right, left) in relation for left, right in combinations(values, 2))


def ideals(record: dict[str, Any]) -> list[list[str]]:
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    relation = closure(checked)
    return [list(part) for part in _subsets(nodes) if is_ideal(part, nodes, relation)]


def antichains(record: dict[str, Any]) -> list[list[str]]:
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    relation = closure(checked)
    return [list(part) for part in _subsets(nodes) if is_antichain(part, relation)]


def maximal_elements(ideal: Iterable[str], relation: set[tuple[str, str]]) -> list[str]:
    chosen = set(ideal)
    return sorted(node for node in chosen if not any(node != other and (node, other) in relation for other in chosen))


def downset(antichain: Iterable[str], nodes: tuple[str, ...], relation: set[tuple[str, str]]) -> list[str]:
    top = set(antichain)
    return sorted(node for node in nodes if any((node, upper) in relation for upper in top))


def linear_extensions(record: dict[str, Any]) -> list[list[str]]:
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    relation = closure(checked)
    strict = {(left, right) for left, right in relation if left != right}
    return [
        list(order)
        for order in permutations(nodes)
        if all(order.index(lower) < order.index(upper) for lower, upper in strict)
    ]


def mobius_table(record: dict[str, Any]) -> dict[str, int]:
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    relation = closure(checked)

    @lru_cache(maxsize=None)
    def mu(lower: str, upper: str) -> int:
        if (lower, upper) not in relation:
            return 0
        if lower == upper:
            return 1
        return -sum(mu(lower, middle) for middle in nodes if middle != upper and (lower, middle) in relation and (middle, upper) in relation)

    return {f"{lower}|{upper}": mu(lower, upper) for lower in nodes for upper in nodes if (lower, upper) in relation}


def analyze(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    relation = closure(checked)
    ideal_rows = ideals(checked)
    antichain_rows = antichains(checked)
    extension_rows = linear_extensions(checked)
    chains = [part for part in _subsets(nodes) if is_chain(part, relation)]
    ideal_to_antichain = [{"ideal": row, "maximal": maximal_elements(row, relation)} for row in ideal_rows]
    roundtrips = [downset(item["maximal"], nodes, relation) == item["ideal"] for item in ideal_to_antichain]
    rank_distribution = {str(size): sum(1 for row in ideal_rows if len(row) == size) for size in range(len(nodes) + 1)}
    result = {
        "fixture_id": checked["id"],
        "source_sha256": digest(checked),
        "node_count": len(nodes),
        "cover_count": len(checked["covers"]),
        "order_pair_count": len(relation),
        "ideal_count": len(ideal_rows),
        "antichain_count": len(antichain_rows),
        "width": max(map(len, antichain_rows)),
        "height": max(map(len, chains)),
        "linear_extension_count": len(extension_rows),
        "ideals": ideal_rows,
        "antichains": antichain_rows,
        "ideal_to_antichain": ideal_to_antichain,
        "bijection_roundtrip": all(roundtrips) and len(ideal_rows) == len(antichain_rows),
        "rank_distribution": rank_distribution,
        "mobius": mobius_table(checked),
    }
    result["result_sha256"] = digest(result)
    return result


def oracle_counts(record: dict[str, Any]) -> dict[str, int]:
    """Independently structured same-author exhaustive oracle for tiny records."""
    checked = validate_record(record)
    nodes = tuple(checked["nodes"])
    outgoing = {node: [] for node in nodes}
    incoming = {node: [] for node in nodes}
    for lower, upper in checked["covers"]:
        outgoing[lower].append(upper)
        incoming[upper].append(lower)

    def predecessors(node: str) -> set[str]:
        seen: set[str] = set()
        stack = list(incoming[node])
        while stack:
            current = stack.pop()
            if current not in seen:
                seen.add(current)
                stack.extend(incoming[current])
        return seen

    predecessor_map = {node: predecessors(node) for node in nodes}
    ideal_count = 0
    antichain_count = 0
    width = 0
    height = 0
    for part in _subsets(nodes):
        chosen = set(part)
        if all(predecessor_map[node] <= chosen for node in chosen):
            ideal_count += 1
        comparable = False
        for left, right in combinations(part, 2):
            if left in predecessor_map[right] or right in predecessor_map[left]:
                comparable = True
                break
        if not comparable:
            antichain_count += 1
            width = max(width, len(part))
        if all(left in predecessor_map[right] or right in predecessor_map[left] for left, right in combinations(part, 2)):
            height = max(height, len(part))

    extension_count = 0
    for order in permutations(nodes):
        position = {node: index for index, node in enumerate(order)}
        if all(position[lower] < position[upper] for lower, upper in checked["covers"]):
            extension_count += 1
    return {
        "ideal_count": ideal_count,
        "antichain_count": antichain_count,
        "width": width,
        "height": height,
        "linear_extension_count": extension_count,
    }


def relabel(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    reversed_nodes = list(reversed(checked["nodes"]))
    mapping = {old: f"r{index:02d}" for index, old in enumerate(reversed_nodes, start=1)}
    nodes = sorted(mapping.values())
    covers = sorted([[mapping[lower], mapping[upper]] for lower, upper in checked["covers"]])
    return {"id": checked["id"] + "-RELABEL", "nodes": nodes, "covers": covers}


def dual(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    return {"id": checked["id"] + "-DUAL", "nodes": checked["nodes"], "covers": sorted([[upper, lower] for lower, upper in checked["covers"]])}


def disjoint_singleton(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    extra = "z"
    while extra in checked["nodes"]:
        extra += "z"
    return {"id": checked["id"] + "-PLUS1", "nodes": sorted(checked["nodes"] + [extra]), "covers": checked["covers"]}


def ordinal_singleton(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    extra = "z"
    while extra in checked["nodes"]:
        extra += "z"
    maximal = []
    relation = closure(checked)
    for node in checked["nodes"]:
        if not any(node != other and (node, other) in relation for other in checked["nodes"]):
            maximal.append(node)
    covers = sorted(checked["covers"] + [[node, extra] for node in maximal])
    return {"id": checked["id"] + "-ORD1", "nodes": sorted(checked["nodes"] + [extra]), "covers": covers}


def fixtures() -> list[dict[str, Any]]:
    specs = [
        ("PS01", ["a", "b"], [["a", "b"]]),
        ("PS02", ["a", "b"], []),
        ("PS03", ["a", "b", "c"], [["a", "c"], ["b", "c"]]),
        ("PS04", ["a", "b", "c"], [["a", "b"], ["a", "c"]]),
        ("PS05", ["a", "b", "c"], [["a", "b"], ["b", "c"]]),
        ("PS06", ["a", "b", "c"], []),
        ("PS07", ["a", "b", "c", "d"], [["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"]]),
        ("PS08", ["a", "b", "c", "d"], [["a", "b"], ["c", "b"], ["c", "d"]]),
        ("PS09", ["a", "b", "c", "d"], [["a", "b"], ["b", "c"], ["c", "d"]]),
        ("PS10", ["a", "b", "c", "d"], [["a", "b"], ["c", "b"], ["c", "d"]]),
        ("PS11", ["a", "b", "c", "d"], []),
        ("PS12", ["a", "b", "c", "d", "e"], [["a", "b"], ["b", "e"], ["a", "c"], ["c", "d"], ["d", "e"]]),
        ("PS13", ["a", "b", "c", "d", "e"], [["a", "b"], ["c", "b"], ["c", "d"], ["e", "d"]]),
        ("PS14", ["a", "b", "c", "d", "e"], [["a", "c"], ["b", "c"], ["c", "d"], ["c", "e"]]),
        ("PS15", ["a", "b", "c", "d", "e", "f"], [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"], ["e", "f"]]),
    ]
    return [validate_record({"id": ident, "nodes": nodes, "covers": sorted(covers)}) for ident, nodes, covers in specs]


def run_x1_tests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in fixtures():
        result = analyze(record)
        oracle = oracle_counts(record)
        observed = {key: result[key] for key in oracle}
        rows.append({"id": f"IF7072-X1-ORACLE-{record['id']}", "passed": observed == oracle, "observed": observed, "oracle": oracle})

    malformed = []
    base = fixtures()[0]
    malformed.append(("duplicate-node", {**base, "nodes": ["a", "a"]}))
    malformed.append(("directed-cycle", {"id": "BAD-CYCLE", "nodes": ["a", "b"], "covers": [["a", "b"], ["b", "a"]]}))
    malformed.append(("unknown-endpoint", {"id": "BAD-END", "nodes": ["a", "b"], "covers": [["a", "c"]]}))
    malformed.append(("self-cover", {"id": "BAD-SELF", "nodes": ["a", "b"], "covers": [["a", "a"]]}))
    malformed.append(("redundant-cover", {"id": "BAD-REDUNDANT", "nodes": ["a", "b", "c"], "covers": [["a", "b"], ["a", "c"], ["b", "c"]]}))
    for name, subject in malformed:
        rejected = False
        reason = ""
        try:
            validate_record(subject)
        except PosetRecordError as exc:
            rejected = True
            reason = str(exc)
        rows.append({
            "id": f"IF7072-X1-INVALID-{name}",
            "passed": rejected,
            "invalid_subject_state": "fail",
            "invalid_subject_success_credit": 0,
            "refusal_guard_state": "pass" if rejected else "fail",
            "reason": reason,
        })
    return rows


def run_x2_tests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    keys = ("ideal_count", "antichain_count", "width", "height", "linear_extension_count")
    for record in fixtures():
        baseline = analyze(record)
        changed = analyze(relabel(record))
        rows.append({
            "id": f"IF7072-X2-RELABEL-{record['id']}",
            "passed": all(baseline[key] == changed[key] for key in keys),
            "baseline": {key: baseline[key] for key in keys},
            "changed": {key: changed[key] for key in keys},
        })
    for record in fixtures():
        baseline = analyze(record)
        changed = analyze(dual(record))
        rows.append({
            "id": f"IF7072-X2-DUAL-{record['id']}",
            "passed": all(baseline[key] == changed[key] for key in keys),
            "baseline": {key: baseline[key] for key in keys},
            "changed": {key: changed[key] for key in keys},
        })
    return rows


def transformation_checks(record: dict[str, Any]) -> dict[str, Any]:
    baseline = analyze(record)
    relabeled = analyze(relabel(record))
    mirrored = analyze(dual(record))
    disjoint = analyze(disjoint_singleton(record))
    ordinal = analyze(ordinal_singleton(record))
    n = baseline["node_count"]
    return {
        "fixture_id": record["id"],
        "relabel_covariant": all(baseline[key] == relabeled[key] for key in ("ideal_count", "antichain_count", "width", "height", "linear_extension_count")),
        "dual_invariant": all(baseline[key] == mirrored[key] for key in ("ideal_count", "antichain_count", "width", "height", "linear_extension_count")),
        "disjoint_singleton_law": {
            "observed_ideal_count": disjoint["ideal_count"],
            "expected_ideal_count": 2 * baseline["ideal_count"],
            "observed_linear_extensions": disjoint["linear_extension_count"],
            "expected_linear_extensions": comb(n + 1, 1) * baseline["linear_extension_count"],
            "passed": disjoint["ideal_count"] == 2 * baseline["ideal_count"] and disjoint["linear_extension_count"] == (n + 1) * baseline["linear_extension_count"],
        },
        "ordinal_singleton_law": {
            "observed_ideal_count": ordinal["ideal_count"],
            "expected_ideal_count": baseline["ideal_count"] + 1,
            "observed_height": ordinal["height"],
            "expected_height": baseline["height"] + 1,
            "passed": ordinal["ideal_count"] == baseline["ideal_count"] + 1 and ordinal["height"] == baseline["height"] + 1,
        },
    }


if __name__ == "__main__":
    payload = {"fixtures": fixtures(), "analyses": [analyze(record) for record in fixtures()]}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
