#!/usr/bin/env python3
"""Finite abstract-reduction-system primitives for Auren v707-v4 x2."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from reduction_lab import (
    analyze_x1,
    locally_confluent,
    normal_forms,
    oracle_closure,
    reflexive_transitive_closure,
    strongly_connected_components,
    termination_status,
    validate_record,
)


def globally_confluent(record: Any) -> bool:
    checked = validate_record(record)
    closure = {key: set(values) for key, values in reflexive_transitive_closure(record).items()}
    for ancestor in checked["terms"]:
        descendants = sorted(closure[ancestor])
        for left in descendants:
            for right in descendants:
                if not closure[left] & closure[right]:
                    return False
    return True


def unique_normal_form(record: Any) -> bool:
    normals = set(normal_forms(record))
    closure = reflexive_transitive_closure(record)
    return all(len(normals.intersection(targets)) <= 1 for targets in closure.values())


def newman_implication(record: Any) -> dict[str, Any]:
    terminating = termination_status(record)
    local = locally_confluent(record)
    global_result = globally_confluent(record)
    premise = terminating and local
    return {"terminating": terminating, "locally_confluent": local, "globally_confluent": global_result, "premise_holds": premise, "implication_holds": (not premise) or global_result}


def deterministic_rule_deletion(record: Any) -> dict[str, Any]:
    checked = validate_record(record)
    deleted = checked["rules"][-1] if checked["rules"] else None
    reduced = deepcopy(record)
    if deleted is not None:
        removed = False
        rules = []
        for rule in record["rules"]:
            pair = (rule["source"], rule["target"])
            if not removed and pair == deleted:
                removed = True
                continue
            rules.append(rule)
        reduced["rules"] = rules
    summary = analyze_x1(reduced)
    return {
        "deleted_rule": None if deleted is None else {"source": deleted[0], "target": deleted[1]},
        "remaining_rule_count": summary["relation-normalization"]["rule_count"],
        "terminating": summary["termination-status"]["terminating"],
        "normal_forms": summary["normal-forms"],
        "locally_confluent": summary["local-confluence"]["locally_confluent"],
        "globally_confluent": globally_confluent(reduced),
    }


def relabel_record(record: Any) -> tuple[dict[str, Any], dict[str, str]]:
    checked = validate_record(record)
    mapping = {term: f"u{index:02d}" for index, term in enumerate(reversed(checked["terms"]), 1)}
    relabeled = deepcopy(record)
    relabeled["terms"] = [mapping[term] for term in record["terms"]]
    relabeled["rules"] = [{"source": mapping[rule["source"]], "target": mapping[rule["target"]]} for rule in record["rules"]]
    relabeled["fixture_id"] = f"{record.get('fixture_id', 'fixture')}-RELABEL"
    return relabeled, mapping


def relabel_covariance(record: Any) -> dict[str, Any]:
    relabeled, mapping = relabel_record(record)
    original = analyze_x1(record)
    changed = analyze_x1(relabeled)
    original_component_sizes = sorted(len(row) for row in original["strong-components"])
    changed_component_sizes = sorted(len(row) for row in changed["strong-components"])
    invariants = {
        "term_count": original["record-shape"]["term_count"] == changed["record-shape"]["term_count"],
        "rule_count": original["relation-normalization"]["rule_count"] == changed["relation-normalization"]["rule_count"],
        "termination": original["termination-status"] == changed["termination-status"],
        "normal_form_count": len(original["normal-forms"]) == len(changed["normal-forms"]),
        "component_sizes": original_component_sizes == changed_component_sizes,
        "local_peak_count": len(original["local-peaks"]) == len(changed["local-peaks"]),
        "local_confluence": original["local-confluence"] == changed["local-confluence"],
        "global_confluence": globally_confluent(record) == globally_confluent(relabeled),
    }
    return {"mapping": mapping, "invariants": invariants, "covariant": all(invariants.values())}


def strategy_traces(record: Any) -> dict[str, dict[str, Any]]:
    checked = validate_record(record)
    graph = {term: [] for term in checked["terms"]}
    for source, target in checked["rules"]:
        graph[source].append(target)
    traces: dict[str, dict[str, Any]] = {}
    for start in checked["terms"]:
        trace = [start]
        seen = {start}
        current = start
        cycle = False
        while graph[current]:
            target = min(graph[current])
            trace.append(target)
            if target in seen:
                cycle = True
                break
            seen.add(target)
            current = target
        traces[start] = {"trace": trace, "cycle_detected": cycle, "normal_form": None if cycle or graph[trace[-1]] else trace[-1]}
    return traces


def accessible_summary(record: Any) -> str:
    checked = validate_record(record)
    terminating = termination_status(record)
    local = locally_confluent(record)
    global_result = globally_confluent(record)
    normals = normal_forms(record)
    return (
        f"{record.get('fixture_id', 'fixture')}: {len(checked['terms'])} terms, {len(checked['rules'])} normalized rules, "
        f"termination={str(terminating).lower()}, local_confluence={str(local).lower()}, "
        f"global_confluence={str(global_result).lower()}, normal_forms={','.join(normals) if normals else 'none'}."
    )


def three_coordinate_model(record: Any) -> dict[str, int]:
    checked = validate_record(record)
    peaks = analyze_x1(record)["local-peaks"]
    return {"term_count": len(checked["terms"]), "rule_count": len(checked["rules"]), "local_peak_count": len(peaks)}


def oracle_global_confluence(record: Any) -> bool:
    checked = validate_record(record)
    closure = {key: set(values) for key, values in oracle_closure(record).items()}
    for ancestor in checked["terms"]:
        descendants = closure[ancestor]
        for left in descendants:
            for right in descendants:
                if not closure[left] & closure[right]:
                    return False
    return True


def analyze_x2(record: Any) -> dict[str, Any]:
    return {
        "global-confluence": {"globally_confluent": globally_confluent(record)},
        "unique-normal-form": {"unique_normal_form": unique_normal_form(record)},
        "newman-implication": newman_implication(record),
        "rule-deletion": deterministic_rule_deletion(record),
        "relabel-covariance": relabel_covariance(record),
        "strategy-trace": strategy_traces(record),
        "accessible-summary": accessible_summary(record),
        "three-coordinate-model": three_coordinate_model(record),
        "empirical-calibration-gap": {"state": "open_gap", "empirical_records": 0, "completion_credit": 0},
        "deployment-authority-hold": {"state": "exact_gate", "executed": False, "competent_authority_evidence": 0, "affected_party_acceptance": 0, "completion_credit": 0},
    }
