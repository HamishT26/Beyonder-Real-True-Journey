#!/usr/bin/env python3
"""Finite abstract-reduction-system primitives for Auren v707-v4 x1."""

from __future__ import annotations

from itertools import combinations
from typing import Any


class ReductionRecordError(ValueError):
    """Raised when a bounded synthetic reduction record is malformed."""


def validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ReductionRecordError("record_not_object")
    terms = record.get("terms")
    rules = record.get("rules")
    if not isinstance(terms, list) or not terms or not all(isinstance(term, str) and term for term in terms):
        raise ReductionRecordError("invalid_terms")
    if len(set(terms)) != len(terms):
        raise ReductionRecordError("duplicate_terms")
    if not isinstance(rules, list):
        raise ReductionRecordError("rules_not_list")
    normalized_rules: list[tuple[str, str]] = []
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != {"source", "target"}:
            raise ReductionRecordError("invalid_rule_shape")
        source = rule["source"]
        target = rule["target"]
        if source not in terms or target not in terms:
            raise ReductionRecordError("unknown_rule_endpoint")
        normalized_rules.append((source, target))
    return {"fixture_id": record.get("fixture_id"), "terms": sorted(terms), "rules": sorted(set(normalized_rules))}


def adjacency(record: Any) -> tuple[list[str], dict[str, set[str]]]:
    checked = validate_record(record)
    graph = {term: set() for term in checked["terms"]}
    for source, target in checked["rules"]:
        graph[source].add(target)
    return checked["terms"], graph


def reflexive_transitive_closure(record: Any) -> dict[str, list[str]]:
    terms, graph = adjacency(record)
    closure: dict[str, list[str]] = {}
    for start in terms:
        seen = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for target in sorted(graph[current]):
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        closure[start] = sorted(seen)
    return closure


def strongly_connected_components(record: Any) -> list[list[str]]:
    terms, _ = adjacency(record)
    closure = reflexive_transitive_closure(record)
    remaining = set(terms)
    components: list[list[str]] = []
    while remaining:
        pivot = min(remaining)
        component = sorted(term for term in remaining if term in closure[pivot] and pivot in closure[term])
        components.append(component)
        remaining.difference_update(component)
    return sorted(components, key=lambda row: (row[0], len(row)))


def termination_status(record: Any) -> bool:
    checked = validate_record(record)
    if any(source == target for source, target in checked["rules"]):
        return False
    return all(len(component) == 1 for component in strongly_connected_components(record))


def normal_forms(record: Any) -> list[str]:
    terms, graph = adjacency(record)
    return [term for term in terms if not graph[term]]


def descendant_sets(record: Any) -> dict[str, list[str]]:
    return reflexive_transitive_closure(record)


def local_peaks(record: Any) -> list[dict[str, str]]:
    terms, graph = adjacency(record)
    peaks = []
    for source in terms:
        for left, right in combinations(sorted(graph[source]), 2):
            peaks.append({"source": source, "left": left, "right": right})
    return peaks


def joinability_matrix(record: Any) -> dict[str, bool]:
    terms, _ = adjacency(record)
    closure = {key: set(values) for key, values in reflexive_transitive_closure(record).items()}
    return {f"{left}|{right}": bool(closure[left] & closure[right]) for left in terms for right in terms}


def locally_confluent(record: Any) -> bool:
    closure = {key: set(values) for key, values in reflexive_transitive_closure(record).items()}
    return all(bool(closure[peak["left"]] & closure[peak["right"]]) for peak in local_peaks(record))


def analyze_x1(record: Any) -> dict[str, Any]:
    checked = validate_record(record)
    return {
        "record-shape": {"valid": True, "term_count": len(checked["terms"]), "declared_rule_count": len(record["rules"])},
        "relation-normalization": {"rules": [{"source": a, "target": b} for a, b in checked["rules"]], "rule_count": len(checked["rules"])},
        "reflexive-transitive-closure": reflexive_transitive_closure(record),
        "strong-components": strongly_connected_components(record),
        "termination-status": {"terminating": termination_status(record)},
        "normal-forms": normal_forms(record),
        "descendant-sets": descendant_sets(record),
        "local-peaks": local_peaks(record),
        "joinability": joinability_matrix(record),
        "local-confluence": {"locally_confluent": locally_confluent(record)},
    }


def oracle_closure(record: Any) -> dict[str, list[str]]:
    checked = validate_record(record)
    terms = checked["terms"]
    relation = {(term, term) for term in terms} | set(checked["rules"])
    changed = True
    while changed:
        changed = False
        additions = {(left, right2) for left, middle in relation for middle2, right2 in relation if middle == middle2}
        before = len(relation)
        relation |= additions
        changed = len(relation) != before
    return {term: sorted(target for left, target in relation if left == term) for term in terms}


def oracle_local_confluence(record: Any) -> bool:
    closure = {key: set(values) for key, values in oracle_closure(record).items()}
    checked = validate_record(record)
    graph = {term: set() for term in checked["terms"]}
    for source, target in checked["rules"]:
        graph[source].add(target)
    for source in checked["terms"]:
        for left, right in combinations(sorted(graph[source]), 2):
            if not closure[left] & closure[right]:
                return False
    return True
