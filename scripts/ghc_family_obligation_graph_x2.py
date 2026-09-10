"""Finite provenance and authority graph operations for Ilyra v690-v2 x2."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import deque
from itertools import pairwise
from typing import Any

OPERATIONS = {
    "transitive_reduction",
    "graph_diff",
    "provenance_path_digest",
    "correction_chain",
    "dependency_blockers",
    "release_gate",
    "critical_path",
    "dot_projection",
    "accessible_graph_summary",
    "obligation_reservation",
}

FIELDS = {
    "transitive_reduction": {"case_id", "nodes", "edges"},
    "graph_diff": {"case_id", "before", "after"},
    "provenance_path_digest": {"case_id", "nodes", "edges", "path", "source_sha256"},
    "correction_chain": {"case_id", "events"},
    "dependency_blockers": {"case_id", "obligations"},
    "release_gate": {"case_id", "authority", "consent", "evidence"},
    "critical_path": {"case_id", "nodes", "weighted_edges"},
    "dot_projection": {"case_id", "nodes", "edges", "graph_id"},
    "accessible_graph_summary": {
        "case_id",
        "blocked",
        "completed",
        "exact_gates",
        "open_gaps",
        "represented",
    },
    "obligation_reservation": {"case_id", "authority", "evidence", "kind", "obligation"},
}


def error(name: str) -> dict[str, Any]:
    return {"ok": False, "error": name, "original_success_credit": 0}


def case_id(payload: dict[str, Any]) -> None:
    value = payload["case_id"]
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 10:
        raise ValueError("invalid_case_id")


def strings(value: Any, name: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or len(value) > 12
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise ValueError(f"invalid_{name}")
    return sorted(value)


def graph(value: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    nodes = strings(value["nodes"], "nodes")
    raw_edges = value["edges"]
    if not isinstance(raw_edges, list) or len(raw_edges) > 40:
        raise ValueError("invalid_edges")
    edges: list[tuple[str, str]] = []
    for row in raw_edges:
        if (
            not isinstance(row, list)
            or len(row) != 2
            or not all(isinstance(item, str) for item in row)
            or row[0] not in nodes
            or row[1] not in nodes
            or row[0] == row[1]
        ):
            raise ValueError("invalid_edge")
        edges.append((row[0], row[1]))
    if len(set(edges)) != len(edges):
        raise ValueError("duplicate_edge")
    return nodes, sorted(edges)


def adjacency(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {node: [] for node in nodes}
    for left, right in edges:
        result[left].append(right)
    for node in nodes:
        result[node].sort()
    return result


def reachable(
    nodes: list[str], edges: list[tuple[str, str]], source: str
) -> list[str]:
    outgoing = adjacency(nodes, edges)
    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for nxt in outgoing[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    seen.remove(source)
    return sorted(seen)


def topological(
    nodes: list[str], edges: list[tuple[str, str]]
) -> tuple[list[str] | None, list[str]]:
    indegree = {node: 0 for node in nodes}
    outgoing = adjacency(nodes, edges)
    for _, right in edges:
        indegree[right] += 1
    ready = sorted(node for node in nodes if indegree[node] == 0)
    order: list[str] = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for nxt in outgoing[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
                ready.sort()
    blocked = sorted(set(nodes) - set(order))
    return (order if not blocked else None), blocked


def closure(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[str]]:
    return [[source, target] for source in nodes for target in reachable(nodes, edges, source)]


def reduction(
    nodes: list[str], edges: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    order, blocked = topological(nodes, edges)
    if order is None or blocked:
        raise ValueError("cycle_not_supported")
    kept = []
    for edge in edges:
        without = [candidate for candidate in edges if candidate != edge]
        if edge[1] not in reachable(nodes, without, edge[0]):
            kept.append(edge)
    return kept


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def evaluate(operation: str, payload: dict[str, Any]) -> dict[str, Any]:
    case_id(payload)
    if operation == "transitive_reduction":
        nodes, edges = graph(payload)
        reduced = reduction(nodes, edges)
        return {
            "edges": [list(edge) for edge in reduced],
            "reachability_preserved": closure(nodes, edges) == closure(nodes, reduced),
        }
    if operation == "graph_diff":
        before_nodes, before_edges = graph(payload["before"])
        after_nodes, after_edges = graph(payload["after"])
        return {
            "added_edges": [list(edge) for edge in sorted(set(after_edges) - set(before_edges))],
            "added_nodes": sorted(set(after_nodes) - set(before_nodes)),
            "removed_edges": [list(edge) for edge in sorted(set(before_edges) - set(after_edges))],
            "removed_nodes": sorted(set(before_nodes) - set(after_nodes)),
            "source_retained": True,
        }
    if operation == "provenance_path_digest":
        nodes, edges = graph(payload)
        path = payload["path"]
        source = payload["source_sha256"]
        if (
            not isinstance(path, list)
            or not path
            or any(node not in nodes for node in path)
            or any((left, right) not in edges for left, right in pairwise(path))
            or not isinstance(source, str)
            or re.fullmatch(r"[0-9a-f]{64}", source) is None
        ):
            raise ValueError("invalid_provenance_path")
        record = {
            "edges": [list(edge) for edge in edges],
            "nodes": nodes,
            "path": path,
            "source_sha256": source,
        }
        return {
            "binding_sha256": hashlib.sha256(canonical_bytes(record)).hexdigest(),
            "identity_established": False,
            "path_valid": True,
            "source_sha256": source,
        }
    if operation == "correction_chain":
        events = payload["events"]
        if not isinstance(events, list) or not events:
            raise ValueError("invalid_events")
        seen: set[str] = set()
        parent = None
        digests = []
        for event in events:
            if not isinstance(event, dict) or set(event) != {"digest", "event_id", "parent_id"}:
                raise ValueError("invalid_event_shape")
            if (
                not isinstance(event["event_id"], str)
                or event["event_id"] in seen
                or event["parent_id"] != parent
                or not isinstance(event["digest"], str)
                or re.fullmatch(r"[0-9a-f]{64}", event["digest"]) is None
            ):
                raise ValueError("invalid_correction_chain")
            seen.add(event["event_id"])
            parent = event["event_id"]
            digests.append(event["digest"])
        return {
            "count": len(events),
            "digests_retained": digests,
            "source_retained": True,
            "tip": parent,
            "valid": True,
        }
    if operation == "dependency_blockers":
        rows = payload["obligations"]
        if not isinstance(rows, list) or not rows:
            raise ValueError("invalid_obligations")
        ids = [row.get("id") for row in rows if isinstance(row, dict)]
        if len(ids) != len(rows) or any(not isinstance(item, str) for item in ids):
            raise ValueError("invalid_obligation")
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate_obligation")
        by_id = {row["id"]: row for row in rows}
        allowed = {"completed", "pending", "open_gap", "exact_gate"}
        for row in rows:
            if set(row) != {"id", "requires", "state"} or row["state"] not in allowed:
                raise ValueError("invalid_obligation_shape")
            if (
                not isinstance(row["requires"], list)
                or any(dep not in by_id for dep in row["requires"])
                or row["id"] in row["requires"]
            ):
                raise ValueError("invalid_dependency")
        completed = sorted(row["id"] for row in rows if row["state"] == "completed")
        ready = sorted(
            row["id"]
            for row in rows
            if row["state"] == "pending"
            and all(by_id[dep]["state"] == "completed" for dep in row["requires"])
        )
        blocked = sorted(
            row["id"]
            for row in rows
            if row["state"] == "pending" and row["id"] not in ready
        )
        unresolved = sorted(
            row["id"] for row in rows if row["state"] in {"open_gap", "exact_gate"}
        )
        return {
            "blocked": blocked,
            "completed": completed,
            "ready": ready,
            "source_retained": True,
            "unresolved": unresolved,
        }
    if operation == "release_gate":
        allowed = {"verified", "absent"}
        if any(payload[key] not in allowed for key in ("authority", "consent", "evidence")):
            raise ValueError("invalid_release_state")
        eligible = all(
            payload[key] == "verified" for key in ("authority", "consent", "evidence")
        )
        return {
            "eligible_in_synthetic_model": eligible,
            "real_authority_established": False,
            "requires_external_review": True,
        }
    if operation == "critical_path":
        nodes = strings(payload["nodes"], "nodes")
        raw_edges = payload["weighted_edges"]
        if not isinstance(raw_edges, list) or not raw_edges:
            raise ValueError("invalid_weighted_edges")
        edges: list[tuple[str, str]] = []
        weights: dict[tuple[str, str], int] = {}
        for row in raw_edges:
            if (
                not isinstance(row, list)
                or len(row) != 3
                or row[0] not in nodes
                or row[1] not in nodes
                or row[0] == row[1]
                or isinstance(row[2], bool)
                or not isinstance(row[2], int)
                or row[2] <= 0
            ):
                raise ValueError("invalid_weighted_edge")
            edge = (row[0], row[1])
            if edge in weights:
                raise ValueError("duplicate_weighted_edge")
            edges.append(edge)
            weights[edge] = row[2]
        order, blocked = topological(nodes, sorted(edges))
        if order is None or blocked:
            raise ValueError("cycle_not_supported")
        incoming = {node: [] for node in nodes}
        for left, right in edges:
            incoming[right].append(left)
        best = {node: (0, [node]) for node in nodes}
        for node in order:
            candidates = [
                (best[left][0] + weights[(left, node)], best[left][1] + [node])
                for left in sorted(incoming[node])
            ]
            if candidates:
                best[node] = min(candidates, key=lambda item: (-item[0], item[1]))
        length, path = min(best.values(), key=lambda item: (-item[0], item[1]))
        return {
            "length": length,
            "path": path,
            "positive_integer_weights_assumed": True,
        }
    if operation == "dot_projection":
        nodes, edges = graph(payload)
        graph_id = payload["graph_id"]
        if (
            not isinstance(graph_id, str)
            or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", graph_id) is None
        ):
            raise ValueError("invalid_graph_id")
        lines = [f"digraph {graph_id} {{"]
        lines.extend(f"  {json.dumps(node)};" for node in nodes)
        lines.extend(
            f"  {json.dumps(left)} -> {json.dumps(right)};" for left, right in edges
        )
        lines.append("}")
        return {"dot": "\n".join(lines), "rendered": False, "source_retained": True}
    if operation == "accessible_graph_summary":
        for key in ("blocked", "completed", "exact_gates", "open_gaps", "represented"):
            value = payload[key]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError("invalid_count")
        return {
            "manual_evaluation": "reserved",
            "real_people_described": False,
            "text": (
                f"Synthetic graph states: completed {payload['completed']}; represented "
                f"{payload['represented']}; blocked {payload['blocked']}; open gaps "
                f"{payload['open_gaps']}; exact gates {payload['exact_gates']}."
            ),
        }
    if operation == "obligation_reservation":
        if payload["kind"] not in {"scientific_evidence", "competent_authority"}:
            raise ValueError("invalid_obligation_kind")
        if (
            not isinstance(payload["obligation"], str)
            or not payload["obligation"]
            or payload["authority"] is not None
            or payload["evidence"] is not None
        ):
            raise ValueError("unsupported_evidence_or_authority_promotion")
        return {
            "authority": None,
            "evidence": None,
            "obligation": payload["obligation"],
            "state": "open_gap"
            if payload["kind"] == "scientific_evidence"
            else "exact_gate",
        }
    raise ValueError("unknown_operation")


def run(request: Any) -> dict[str, Any]:
    original = copy.deepcopy(request)
    if not isinstance(request, dict) or set(request) != {"operation", "payload"}:
        return error("invalid_request_shape")
    operation = request["operation"]
    payload = request["payload"]
    if operation not in OPERATIONS:
        return error("unknown_operation")
    if not isinstance(payload, dict):
        return error("invalid_payload")
    if set(payload) != FIELDS[operation]:
        return error("unknown_payload_field")
    try:
        value = evaluate(operation, copy.deepcopy(payload))
    except (KeyError, TypeError, ValueError) as exc:
        return error(str(exc) or "invalid_payload")
    if request != original:
        return error("input_mutated")
    outcome = (
        "represented"
        if operation == "accessible_graph_summary"
        else value["state"]
        if operation == "obligation_reservation"
        else "completed"
    )
    return {"ok": True, "operation": operation, "outcome": outcome, "value": value}
