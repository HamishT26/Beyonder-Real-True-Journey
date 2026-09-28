from __future__ import annotations

import itertools
from copy import deepcopy
from typing import Any

from common import sha256_value

def normalize_graph(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) < {"id", "nodes", "edges"}:
        raise ValueError("graph record requires id, nodes, and edges")
    nodes = record["nodes"]
    edges = record["edges"]
    if not isinstance(nodes, list) or not all(isinstance(v, str) and v for v in nodes) or len(nodes) != len(set(nodes)):
        raise ValueError("nodes must be unique nonempty strings")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    node_set = set(nodes)
    normalized = []
    seen = set()
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2 or not all(isinstance(v, str) for v in edge):
            raise ValueError("each edge must contain two string endpoints")
        a, b = edge
        if a not in node_set or b not in node_set:
            raise ValueError("edge endpoint is outside the node set")
        if a == b:
            raise ValueError("self-loops are refused")
        pair = tuple(sorted((a, b)))
        if pair not in seen:
            seen.add(pair); normalized.append(list(pair))
    return {"id": record["id"], "nodes": sorted(nodes), "edges": sorted(normalized)}

def adjacency(graph: dict[str, Any]) -> dict[str, set[str]]:
    adj = {v: set() for v in graph["nodes"]}
    for a, b in graph["edges"]:
        adj[a].add(b); adj[b].add(a)
    return adj

def components(graph: dict[str, Any]) -> list[list[str]]:
    adj = adjacency(graph); unseen = set(graph["nodes"]); out = []
    while unseen:
        start = min(unseen); stack = [start]; comp = []; unseen.remove(start)
        while stack:
            v = stack.pop(); comp.append(v)
            for w in sorted(adj[v], reverse=True):
                if w in unseen: unseen.remove(w); stack.append(w)
        out.append(sorted(comp))
    return sorted(out)

def induced(graph: dict[str, Any], selected: list[str]) -> dict[str, Any]:
    keep = set(selected)
    return {"id": graph["id"] + "-induced", "nodes": sorted(keep), "edges": [e for e in graph["edges"] if set(e) <= keep]}

def is_clique(adj: dict[str, set[str]], vertices: set[str]) -> bool:
    return all(b in adj[a] for a, b in itertools.combinations(sorted(vertices), 2))

def simplicial_vertices(graph: dict[str, Any]) -> list[str]:
    adj = adjacency(graph)
    return [v for v in graph["nodes"] if is_clique(adj, adj[v])]

def mcs_order(graph: dict[str, Any]) -> list[str]:
    adj = adjacency(graph); weights = {v: 0 for v in graph["nodes"]}; unseen = set(graph["nodes"]); order = []
    while unseen:
        best_weight = max(weights[v] for v in unseen)
        v = min(v for v in unseen if weights[v] == best_weight)
        unseen.remove(v); order.append(v)
        for w in adj[v] & unseen: weights[w] += 1
    return order

def perfect_elimination_order(graph: dict[str, Any]) -> list[str] | None:
    current = deepcopy(graph); order = []
    while current["nodes"]:
        candidates = simplicial_vertices(current)
        if not candidates: return None
        chosen = min(candidates); order.append(chosen)
        remaining = [v for v in current["nodes"] if v != chosen]
        current = induced(current, remaining)
    return order

def chordless_cycle_witness(graph: dict[str, Any]) -> list[str] | None:
    nodes = graph["nodes"]
    for size in range(4, len(nodes) + 1):
        for subset in itertools.combinations(nodes, size):
            sub = induced(graph, list(subset)); adj = adjacency(sub)
            if all(len(adj[v]) == 2 for v in subset) and len(components(sub)) == 1:
                return list(subset)
    return None

def independent_chordal_oracle(graph: dict[str, Any]) -> bool:
    return chordless_cycle_witness(graph) is None

def evaluate(slug: str, fixture: dict[str, Any]) -> dict[str, Any]:
    original = deepcopy(fixture); before = sha256_value(original); graph = normalize_graph(fixture)
    adj = adjacency(graph)
    if slug == "record-shape":
        value = {"valid": True, "node_count": len(graph["nodes"]), "edge_count": len(graph["edges"])}
    elif slug == "graph-normalization":
        value = {"nodes": graph["nodes"], "edges": graph["edges"]}
    elif slug == "adjacency-symmetry":
        value = {"symmetric": all(v in adj[w] for v in adj for w in adj[v]), "loops": sum(v in adj[v] for v in adj)}
    elif slug == "connected-components":
        value = {"components": components(graph)}
    elif slug == "induced-subgraph":
        selected = graph["nodes"][::2] or graph["nodes"][:1]
        value = {"selected": selected, "graph": induced(graph, selected)}
    elif slug == "simplicial-vertices":
        value = {"vertices": simplicial_vertices(graph)}
    elif slug == "maximum-cardinality-search":
        value = {"order": mcs_order(graph)}
    elif slug == "perfect-elimination-order":
        value = {"order": perfect_elimination_order(graph), "exists": perfect_elimination_order(graph) is not None}
    elif slug == "chordality-decision":
        peo = perfect_elimination_order(graph)
        value = {"chordal": peo is not None, "peo": peo, "oracle": independent_chordal_oracle(graph)}
    elif slug == "chordless-cycle-witness":
        value = {"witness": chordless_cycle_witness(graph), "chordal": independent_chordal_oracle(graph)}
    else:
        raise ValueError(f"unsupported x1 operation: {slug}")
    after = sha256_value(fixture)
    if before != after: raise RuntimeError("input mutation detected")
    return {"operation": slug, "fixture_id": fixture["id"], "input_sha256": before, "output": value, "input_unchanged": True}
