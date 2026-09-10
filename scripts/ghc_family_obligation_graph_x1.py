"""Finite directed-obligation graph operations for Ilyra v690-v2 x1."""

from __future__ import annotations

import copy
from collections import deque
from typing import Any

OPERATIONS = {
    "canonical_graph_record",
    "out_adjacency",
    "in_adjacency",
    "reachable_nodes",
    "shortest_hop_path",
    "dag_status",
    "topological_order",
    "weak_components",
    "transitive_closure",
    "boundary_edges",
}

FIELDS = {
    "canonical_graph_record": {"case_id", "nodes", "edges"},
    "out_adjacency": {"case_id", "nodes", "edges"},
    "in_adjacency": {"case_id", "nodes", "edges"},
    "reachable_nodes": {"case_id", "nodes", "edges", "source"},
    "shortest_hop_path": {"case_id", "nodes", "edges", "source", "target"},
    "dag_status": {"case_id", "nodes", "edges"},
    "topological_order": {"case_id", "nodes", "edges"},
    "weak_components": {"case_id", "nodes", "edges"},
    "transitive_closure": {"case_id", "nodes", "edges"},
    "boundary_edges": {"case_id", "nodes", "edges", "inside"},
}


def error(name: str) -> dict[str, Any]:
    return {"ok": False, "error": name, "original_success_credit": 0}


def string_list(value: Any, name: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or len(value) > 12
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise ValueError(f"invalid_{name}")
    return sorted(value)


def graph(payload: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    case_id = payload["case_id"]
    if isinstance(case_id, bool) or not isinstance(case_id, int) or not 1 <= case_id <= 10:
        raise ValueError("invalid_case_id")
    nodes = string_list(payload["nodes"], "nodes")
    raw_edges = payload["edges"]
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
    nodes: list[str], edges: list[tuple[str, str]], source: str, *, include_source: bool
) -> list[str]:
    if source not in nodes:
        raise ValueError("unknown_source")
    outgoing = adjacency(nodes, edges)
    queue = deque([source])
    seen = {source}
    while queue:
        node = queue.popleft()
        for nxt in outgoing[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    if not include_source:
        seen.remove(source)
    return sorted(seen)


def shortest(
    nodes: list[str], edges: list[tuple[str, str]], source: str, target: str
) -> list[str] | None:
    if source not in nodes or target not in nodes:
        raise ValueError("unknown_endpoint")
    outgoing = adjacency(nodes, edges)
    queue = deque([[source]])
    seen = {source}
    while queue:
        path = queue.popleft()
        if path[-1] == target:
            return path
        for nxt in outgoing[path[-1]]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])
    return None


def topological(
    nodes: list[str], edges: list[tuple[str, str]]
) -> tuple[list[str] | None, list[str]]:
    incoming_count = {node: 0 for node in nodes}
    outgoing = adjacency(nodes, edges)
    for _, right in edges:
        incoming_count[right] += 1
    available = sorted(node for node in nodes if incoming_count[node] == 0)
    order: list[str] = []
    while available:
        node = available.pop(0)
        order.append(node)
        for nxt in outgoing[node]:
            incoming_count[nxt] -= 1
            if incoming_count[nxt] == 0:
                available.append(nxt)
                available.sort()
    blocked = sorted(set(nodes) - set(order))
    return (order if not blocked else None), blocked


def components(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[str]]:
    neighbors = {node: set() for node in nodes}
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    pending = set(nodes)
    found: list[list[str]] = []
    while pending:
        start = min(pending)
        queue = [start]
        component: set[str] = set()
        while queue:
            node = queue.pop()
            if node in component:
                continue
            component.add(node)
            queue.extend(sorted(neighbors[node] - component, reverse=True))
        pending -= component
        found.append(sorted(component))
    return sorted(found)


def evaluate(operation: str, payload: dict[str, Any]) -> dict[str, Any]:
    nodes, edges = graph(payload)
    if operation == "canonical_graph_record":
        return {"directed": True, "edges": [list(edge) for edge in edges], "nodes": nodes}
    if operation == "out_adjacency":
        return {"adjacency": adjacency(nodes, edges), "direction": "outgoing"}
    if operation == "in_adjacency":
        reverse = sorted((right, left) for left, right in edges)
        return {"adjacency": adjacency(nodes, reverse), "direction": "incoming"}
    if operation == "reachable_nodes":
        return {
            "reachable": reachable(nodes, edges, payload["source"], include_source=True),
            "source": payload["source"],
        }
    if operation == "shortest_hop_path":
        path = shortest(nodes, edges, payload["source"], payload["target"])
        return {
            "hops": None if path is None else len(path) - 1,
            "path": path,
            "source": payload["source"],
            "target": payload["target"],
        }
    if operation == "dag_status":
        order, blocked = topological(nodes, edges)
        return {"blocked_nodes": blocked, "is_dag": order is not None, "order": order}
    if operation == "topological_order":
        order, blocked = topological(nodes, edges)
        if order is None or blocked:
            raise ValueError("cycle_not_supported")
        return {"lexicographic": True, "order": order}
    if operation == "weak_components":
        return {"components": components(nodes, edges), "directed_edges_retained": True}
    if operation == "transitive_closure":
        pairs = [
            [source, target]
            for source in nodes
            for target in reachable(nodes, edges, source, include_source=False)
        ]
        return {"pairs": pairs, "self_pairs": False}
    if operation == "boundary_edges":
        inside = string_list(payload["inside"], "inside")
        if any(node not in nodes for node in inside):
            raise ValueError("unknown_inside_node")
        inside_set = set(inside)
        return {
            "entering": [
                list(edge) for edge in edges if edge[0] not in inside_set and edge[1] in inside_set
            ],
            "leaving": [
                list(edge) for edge in edges if edge[0] in inside_set and edge[1] not in inside_set
            ],
            "partition": inside,
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
    return {"ok": True, "operation": operation, "outcome": "completed", "value": value}
