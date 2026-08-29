from __future__ import annotations

from typing import Any


def validate_graph(payload: dict[str, Any]) -> dict[str, Any]:
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    node_ids = [node.get("id") for node in nodes]
    errors: list[str] = []
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_lock")
    if len(node_ids) != len(set(node_ids)) or any(not item for item in node_ids):
        errors.append("node_identity")
    known = set(node_ids)
    for edge in edges:
        if edge.get("from") not in known or edge.get("to") not in known:
            errors.append("orphan_edge")
    if payload.get("real_measurements", 0) != 0:
        errors.append("real_measurement")
    if payload.get("authority_conferred", False):
        errors.append("authority_promotion")
    return {"passed": not errors, "errors": errors, "node_count": len(nodes), "edge_count": len(edges)}


def run(payload: dict[str, Any]) -> dict[str, Any]:
    return validate_graph(payload)
