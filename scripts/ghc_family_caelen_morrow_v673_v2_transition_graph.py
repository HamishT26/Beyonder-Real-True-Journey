"""Synthetic lifecycle and disassembly graphs for Caelen v673-v2."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

ALLOWED_TRANSITIONS = {
    "planned": {"quarantined", "represented"},
    "quarantined": {"represented", "closed_synthetic"},
    "represented": {"closed_synthetic"},
    "closed_synthetic": set(),
}


def transition(current: str, target: str) -> dict[str, Any]:
    """Evaluate one closed-vocabulary synthetic transition."""
    if current not in ALLOWED_TRANSITIONS:
        return {"accepted": False, "reason": "unknown_current_state", "current": current, "target": target}
    if target not in ALLOWED_TRANSITIONS[current]:
        return {"accepted": False, "reason": "transition_not_allowed", "current": current, "target": target}
    return {
        "accepted": True,
        "reason": "bounded_synthetic_transition",
        "current": current,
        "target": target,
        "real_world_effect": False,
        "authority_effect": False,
    }


def topological_order(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, Any]:
    """Return a deterministic order or fail closed on malformed/cyclic graphs."""
    if len(nodes) != len(set(nodes)) or not nodes:
        return {"valid": False, "reason": "nodes_must_be_nonempty_and_unique", "order": []}
    node_set = set(nodes)
    if any(source not in node_set or target not in node_set or source == target for source, target in edges):
        return {"valid": False, "reason": "edge_outside_node_set_or_self_loop", "order": []}
    indegree = {node: 0 for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for source, target in edges:
        outgoing[source].append(target)
        indegree[target] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target in sorted(outgoing[node]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(order) != len(nodes):
        return {"valid": False, "reason": "cycle_detected", "order": []}
    return {
        "valid": True,
        "reason": "bounded_synthetic_dependency_order",
        "order": order,
        "repair_instruction": False,
        "real_instrument_application": False,
    }


def state_machine_receipt() -> dict[str, Any]:
    """Expose the immutable closed vocabulary for evidence and tests."""
    return {
        "schema": "ghc.family.synthetic-transition-graph.v1",
        "states": sorted(ALLOWED_TRANSITIONS),
        "edges": sorted([f"{source}->{target}" for source, targets in ALLOWED_TRANSITIONS.items() for target in targets]),
        "terminal": [state for state, targets in ALLOWED_TRANSITIONS.items() if not targets],
        "boundary": "Software state only; no real disassembly, repair, custody, safety, or authority transition.",
    }
