from __future__ import annotations

from typing import Any


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        reasons.append("nodes_or_edges_missing")
        nodes, edges = [], []
    node_ids = [row.get("id") for row in nodes if isinstance(row, dict)]
    if len(node_ids) != len(set(node_ids)):
        reasons.append("duplicate_node")
    known = set(node_ids)
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("source") not in known or edge.get("target") not in known:
            reasons.append("orphan_edge")
    if payload.get("real_measurements", 0) != 0:
        reasons.append("real_measurement_nonzero")
    if payload.get("condition_assessment") not in (None, "unknown_not_assessed"):
        reasons.append("condition_assessment_promoted")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "topology_nodes": len(nodes),
        "topology_edges": len(edges),
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
