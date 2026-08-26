"""Append-only synthetic lot, transfer, and correction trace checks."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

try:
    from scripts.ghc_family_grain_milling_contracts import ContractError
except ModuleNotFoundError:  # Direct script execution resolves from scripts/.
    from ghc_family_grain_milling_contracts import ContractError


def validate_event_chain(events: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(events)
    if not rows:
        raise ContractError("empty_event_chain")
    seen: set[str] = set()
    previous_sequence = 0
    for event in rows:
        event_id = str(event.get("event_id", ""))
        sequence = event.get("source_sequence")
        if not event_id or event_id in seen:
            raise ContractError("duplicate_or_missing_event_id")
        if not isinstance(sequence, int) or sequence != previous_sequence + 1:
            raise ContractError("noncontiguous_source_sequence")
        if event.get("real_world_action", False):
            raise ContractError("external_action_prohibited")
        parent = event.get("parent_event_id")
        if previous_sequence == 0 and parent is not None:
            raise ContractError("root_parent_prohibited")
        if previous_sequence > 0 and parent not in seen:
            raise ContractError("missing_parent")
        seen.add(event_id)
        previous_sequence = sequence
    return {
        "accepted": True,
        "events": len(rows),
        "last_sequence": previous_sequence,
        "append_only": True,
        "real_world_actions": 0,
    }


def validate_transfer_graph(edges: Iterable[tuple[str, str]]) -> dict[str, Any]:
    graph: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for source, target in edges:
        if not source or not target or source == target:
            raise ContractError("invalid_transfer_edge")
        graph[source].append(target)
        nodes.update((source, target))
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ContractError("cyclic_transfer_graph")
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in sorted(nodes):
        visit(node)
    return {"accepted": True, "nodes": len(nodes), "edges": sum(map(len, graph.values())), "acyclic": True}


def positive_fixture() -> list[dict[str, Any]]:
    return [
        {"event_id": "fixture-intake", "source_sequence": 1, "parent_event_id": None, "real_world_action": False},
        {"event_id": "fixture-transfer", "source_sequence": 2, "parent_event_id": "fixture-intake", "real_world_action": False},
        {"event_id": "fixture-correction", "source_sequence": 3, "parent_event_id": "fixture-transfer", "real_world_action": False},
    ]
