from __future__ import annotations

import itertools
from copy import deepcopy
from typing import Any

from common import sha256_value
from x1_algorithms import adjacency, chordless_cycle_witness, independent_chordal_oracle, normalize_graph

def maximal_cliques(graph: dict[str, Any]) -> list[list[str]]:
    adj = adjacency(graph); nodes = graph["nodes"]; cliques = []
    for size in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, size):
            if all(b in adj[a] for a, b in itertools.combinations(subset, 2)):
                cliques.append(set(subset))
    maximal = [c for c in cliques if not any(c < other for other in cliques)]
    return sorted([sorted(c) for c in maximal], key=lambda c: (len(c), c))

def clique_forest(cliques: list[list[str]]) -> list[list[int]]:
    parent = list(range(len(cliques)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    candidates = []
    for i, j in itertools.combinations(range(len(cliques)), 2):
        weight = len(set(cliques[i]) & set(cliques[j]))
        if weight: candidates.append((-weight, i, j))
    edges = []
    for _, i, j in sorted(candidates):
        ri, rj = find(i), find(j)
        if ri != rj: parent[ri] = rj; edges.append([i, j])
    return edges

def running_intersection(cliques: list[list[str]], edges: list[list[int]]) -> tuple[bool, dict[str, bool]]:
    vertices = sorted({v for clique in cliques for v in clique}); edge_set = {tuple(sorted(e)) for e in edges}; results = {}
    for vertex in vertices:
        ids = [i for i, clique in enumerate(cliques) if vertex in clique]
        if len(ids) <= 1: results[vertex] = True; continue
        seen = {ids[0]}; stack = [ids[0]]
        while stack:
            current = stack.pop()
            for other in ids:
                if other not in seen and tuple(sorted((current, other))) in edge_set:
                    seen.add(other); stack.append(other)
        results[vertex] = len(seen) == len(ids)
    return all(results.values()), results

def separator_profile(cliques: list[list[str]], edges: list[list[int]]) -> list[list[str]]:
    return sorted({tuple(sorted(set(cliques[i]) & set(cliques[j]))) for i, j in edges if set(cliques[i]) & set(cliques[j])})

def triangulate(graph: dict[str, Any]) -> dict[str, Any]:
    current = deepcopy(graph); added = []
    guard = len(graph["nodes"]) ** 2 + 1
    for _ in range(guard):
        witness = chordless_cycle_witness(current)
        if witness is None: return {"graph": current, "added_edges": added, "chordal": True}
        existing = {tuple(e) for e in current["edges"]}
        choices = [pair for pair in itertools.combinations(sorted(witness), 2) if tuple(sorted(pair)) not in existing]
        if not choices: raise RuntimeError("cycle witness has no missing chord")
        edge = list(min(choices)); current["edges"] = sorted(current["edges"] + [edge]); added.append(edge)
    raise RuntimeError("triangulation guard exhausted")

def relabeled(graph: dict[str, Any]) -> dict[str, Any]:
    mapping = {old: f"r{i:02d}" for i, old in enumerate(reversed(graph["nodes"]), 1)}
    return normalize_graph({"id": graph["id"] + "-relabel", "nodes": [mapping[v] for v in graph["nodes"]], "edges": [[mapping[a], mapping[b]] for a, b in graph["edges"]]})

def invariant_profile(graph: dict[str, Any]) -> dict[str, Any]:
    cliques = maximal_cliques(graph)
    return {"vertices": len(graph["nodes"]), "edges": len(graph["edges"]), "chordal": independent_chordal_oracle(graph), "clique_sizes": sorted(len(c) for c in cliques)}

def evaluate_x2(slug: str, fixture: dict[str, Any]) -> dict[str, Any]:
    before = sha256_value(fixture); graph = normalize_graph(fixture); cliques = maximal_cliques(graph); forest = clique_forest(cliques)
    if slug == "maximal-cliques": value = {"cliques": cliques}
    elif slug == "clique-tree-candidate": value = {"cliques": cliques, "edges": forest, "applicable": independent_chordal_oracle(graph)}
    elif slug == "running-intersection-check":
        valid, by_vertex = running_intersection(cliques, forest); value = {"valid": valid, "by_vertex": by_vertex, "chordal": independent_chordal_oracle(graph)}
    elif slug == "minimal-separator-profile": value = {"separators": separator_profile(cliques, forest), "applicable": independent_chordal_oracle(graph)}
    elif slug == "fill-edge-triangulation": value = triangulate(graph)
    elif slug == "edge-deletion-comparison":
        kept = graph["edges"][:-1] if graph["edges"] else []; changed = normalize_graph({"id": graph["id"] + "-delete", "nodes": graph["nodes"], "edges": kept})
        value = {"deleted": graph["edges"][-1] if graph["edges"] else None, "before_chordal": independent_chordal_oracle(graph), "after_chordal": independent_chordal_oracle(changed)}
    elif slug == "relabel-covariance":
        renamed = relabeled(graph); value = {"original": invariant_profile(graph), "relabeled": invariant_profile(renamed), "covariant": invariant_profile(graph) == invariant_profile(renamed)}
    elif slug == "three-coordinate-model": value = {"coordinates": [len(graph["nodes"]), len(graph["edges"]), len(cliques)], "status": "represented", "physical_model": False}
    elif slug == "external-graph-corpus-gap": value = {"status": "open_gap", "real_graph_rows": 0, "benchmarks": 0, "transfer_claim": False}
    elif slug == "deployment-authority-hold": value = {"status": "exact_gate", "deployment_authority": False, "affected_party_acceptance": False, "maori_authority": False}
    else: raise ValueError(f"unsupported x2 operation: {slug}")
    if before != sha256_value(fixture): raise RuntimeError("input mutation detected")
    return {"operation": slug, "fixture_id": fixture["id"], "input_sha256": before, "output": value, "input_unchanged": True}
