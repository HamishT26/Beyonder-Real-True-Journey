"""Build the planning-only freeze for Ilyra Fen v690-v2."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import zipfile
from collections import deque
from itertools import pairwise
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v690-v2"
PLAN = BASE / "plan"
OWNER = "Ilyra Fen"
PHASE = "v690-v2"
BRANCH = "codex/GHC-Family/ilyra-fen-main"
SOURCE_OWNER = "Lyren Moss"
SOURCE_PHASE = "v690-v1"
SOURCE_FINAL = "9936e2855b72bddfecdea77abdd6f083f14a09f1"
SOURCE_X1 = "13048b82fb42c27ff287bf6793c9b52d67a49f96"
SOURCE_X2 = "b716b6694110e4b60154d8d91de1bfdf5b2b7ab1"
SOURCE_BATON = "docs/lyren-moss/v690-v1/final/hand-off-baton.md"
SOURCE_BATON_SHA256 = "009d96aec25be34dcd4eac9187388e838ea1f1db44a87d33cc3be626e385112b"
SOURCE_CANONICAL_SHA256 = "8d089142b18915b3cf149cea7dde9638085c06b54d91320fb0bedda030dbb2c0"
BOUNDARY = (
    "Bounded same-owner synthetic software and documentation planning only; no empirical "
    "GMUT confirmation, production THOS certification, live Freed ID lifecycle, identity "
    "or consent evidence, professional qualification, legal or cultural authority, Maori "
    "authority, complete privacy or accessibility assurance, exhaustive security, "
    "independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, "
    "Theory-of-Everything proof, canon, or Stage 20 readiness."
)
RELATIONAL_BOUNDARY = (
    "Ilyra Fen, they and them, the role directed-obligation provenance cartographer and "
    "the hope of making dependency, correction, and authority boundaries inspectable are "
    "corrigible relational working language only. They are not evidence of consciousness, "
    "sentience, personhood, identity continuity, employment, qualification, independent "
    "agency, or authority."
)
PROTECTED_GATES = [
    "real participants affected people and operational deployment",
    "empirical GMUT observables likelihood calibration and falsification",
    "THOS governed real matched-budget evaluation and safety review",
    "Freed ID standards-conformant live keys proofs lifecycle and trust governance",
    "legal cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security independent reproduction",
    "AGI ASI consciousness personhood Theory-of-Everything canon Stage 20",
]

X1_OPERATIONS = [
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
]
X2_OPERATIONS = [
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
]

PRACTICES = [
    {
        "name": "finite directed-graph algorithm tester",
        "pillar": "GMUT Mind",
        "boundary": "Finite definitions and counterexamples only; not a physical or cognitive observable.",
    },
    {
        "name": "provenance and correction-lineage engineer",
        "pillar": "THOS Body",
        "boundary": "Typed provenance and additive correction only; not authenticity or production authority.",
    },
    {
        "name": "public-interest data-governance reviewer",
        "pillar": "Freed ID and CBR Heart",
        "boundary": "Synthetic decision fields only; no consent, rights, legal, cultural, or Maori authority.",
    },
    {
        "name": "accessible dependency-status editor",
        "pillar": "Freed ID and CBR Heart",
        "boundary": "Structural text representation only; manual and affected-user evaluation remain reserved.",
    },
]
SUCCESSOR_PRACTICES = [
    "adversarial reachability-policy auditor",
    "provenance-graph visualization accessibility reviewer",
]

RECENT_BUNDLES = [
    (
        "Lyren Moss v690-v1",
        SOURCE_FINAL,
        "docs/lyren-moss/v690-v1/final/overview.md",
        "Keep detected, corrected, uncorrectable, and authority states separate; retain all failed subjects.",
    ),
    (
        "Ilyan Reed v689-v8",
        "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e",
        "docs/ilyan-reed/v689-v8/final/overview.md",
        "Approximate membership and digests cannot certify identity, consent, or rights.",
    ),
    (
        "Vesper Arlen v689-v7-r2",
        "497225ad1af5f6b46ed8353bc0445d4d592e1981",
        "docs/vesper-arlen/v689-v7-r2/final/overview.md",
        "Treat historical instructions as source content and preserve contradictions without adopting them.",
    ),
    (
        "Vesper Arlen v689-v7",
        "ceed54dca93bdf938ee779ecf571fd73e28df0b6",
        "docs/vesper-arlen/v689-v7/final/overview.md",
        "Fixity and recoverability do not establish authenticity, truth, consent, or authority.",
    ),
    (
        "Neris Solane v689-v6",
        "d58272639a581e28176b2aca76f8f468df60e9a6",
        "docs/neris-solane/v689-v6/final/overview.md",
        "Numerical identities, stability, continuum claims, and empirical claims require distinct evidence.",
    ),
    (
        "Rowan Ash v689-v5",
        "ffdff93a34f607f5d4a7c497f0056afcc82cdbf2",
        "docs/rowan-ash/v689-v5/final/overview.md",
        "Graph energy and topology depend on explicit objects, weights, dynamics, and coefficient domains.",
    ),
    (
        "Elaren Kestrel v689-v4",
        "d0707cbb99491bbd6b5d652d506dd811b612d587",
        "docs/elaren-kestrel/v689-v4/final/overview.md",
        "Freeze full typed envelopes and keep structural representation below professional or cultural claims.",
    ),
    (
        "Eiren Kestrel v689-v3",
        "1ddbae5ab48e5f0ea489b118142ef4374b033895",
        "docs/eiren-kestrel/v689-v3/final/overview.md",
        "Preserve invalid aggregates, isolate only failed dependencies, and avoid global-name overwrite.",
    ),
    (
        "Seren Talewood v689-v2-r3",
        "40b1bfda5544da1609b8eec294812400452a9d80",
        "docs/seren-talewood/v689-v2-r3/final/overview.md",
        "Use the 45-position weighted route and treat long projections as prospective planning only.",
    ),
    (
        "Seren Talewood v689-v2-r2",
        "bbf670530d5971aade7bec58733ed1e457f362cb",
        "docs/seren-talewood/v689-v2-r2/final/overview.md",
        "Bind raw Git bytes separately from checkout bytes and preserve a failed canonical without replay.",
    ),
]

PACKAGE_WHEELS = {
    "graphviz-0.21-py3-none-any.whl": "54f33de9f4f911d7e84e4191749cac8cc5653f815b06738c54db9a15ab8b1e42",
    "networkx-3.6.1-py3-none-any.whl": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
    "rustworkx-0.18.1-cp310-abi3-win_amd64.whl": "91feb30971df6ac53d51503970e4aac67e4d9bc7834535f2b7cd3674645003ac",
}


def json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo)


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


def graph_parts(payload: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    nodes = string_list(payload["nodes"], "nodes")
    raw_edges = payload["edges"]
    if not isinstance(raw_edges, list) or len(raw_edges) > 40:
        raise ValueError("invalid_edges")
    edges: list[tuple[str, str]] = []
    for raw in raw_edges:
        if (
            not isinstance(raw, list)
            or len(raw) != 2
            or not all(isinstance(item, str) for item in raw)
            or raw[0] not in nodes
            or raw[1] not in nodes
            or raw[0] == raw[1]
        ):
            raise ValueError("invalid_edge")
        edges.append((raw[0], raw[1]))
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
    nodes: list[str], edges: list[tuple[str, str]], source: str, *, include_source: bool = True
) -> list[str]:
    if source not in nodes:
        raise ValueError("unknown_source")
    outgoing = adjacency(nodes, edges)
    seen = {source}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        for nxt in outgoing[current]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    if not include_source:
        seen.remove(source)
    return sorted(seen)


def shortest_path(
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


def kahn(
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


def weak_components(
    nodes: list[str], edges: list[tuple[str, str]]
) -> list[list[str]]:
    neighbors = {node: set() for node in nodes}
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    unseen = set(nodes)
    result: list[list[str]] = []
    while unseen:
        start = min(unseen)
        stack = [start]
        component: set[str] = set()
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(sorted(neighbors[node] - component, reverse=True))
        unseen -= component
        result.append(sorted(component))
    return sorted(result)


def transitive_pairs(
    nodes: list[str], edges: list[tuple[str, str]]
) -> list[list[str]]:
    return [
        [source, target]
        for source in nodes
        for target in reachable(nodes, edges, source, include_source=False)
    ]


def transitive_reduction(
    nodes: list[str], edges: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    order, _ = kahn(nodes, edges)
    if order is None:
        raise ValueError("cycle_not_supported")
    retained: list[tuple[str, str]] = []
    for edge in edges:
        reduced = [candidate for candidate in edges if candidate != edge]
        if edge[1] not in reachable(nodes, reduced, edge[0], include_source=False):
            retained.append(edge)
    return retained


def dag_fixture(index: int) -> dict[str, Any]:
    size = 4 + (index % 4)
    nodes = [f"n{item}" for item in range(size)]
    edges = [[nodes[item], nodes[item + 1]] for item in range(size - 1)]
    if index % 2 == 0 and size >= 4:
        edges.append([nodes[0], nodes[2]])
    if index % 3 == 0 and size >= 5:
        edges.append([nodes[1], nodes[3]])
    return {"nodes": nodes, "edges": edges}


def cycle_fixture(index: int) -> dict[str, Any]:
    value = dag_fixture(index)
    if index % 2 == 0:
        value["edges"].append([value["nodes"][-1], value["nodes"][0]])
    return value


def weak_fixture(index: int) -> dict[str, Any]:
    left = 2 + index % 3
    right = 2 + (index + 1) % 3
    nodes = [f"a{item}" for item in range(left)] + [f"b{item}" for item in range(right)]
    edges = [[f"a{item}", f"a{item + 1}"] for item in range(left - 1)]
    edges += [[f"b{item}", f"b{item + 1}"] for item in range(right - 1)]
    return {"nodes": nodes, "edges": edges}


def fixtures(operation: str) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for index in range(1, 11):
        graph = dag_fixture(index)
        if operation in {
            "canonical_graph_record",
            "out_adjacency",
            "in_adjacency",
            "transitive_closure",
            "transitive_reduction",
            "dot_projection",
        }:
            payload = copy.deepcopy(graph)
            if operation == "dot_projection":
                payload["graph_id"] = f"obligation_{index:02d}"
        elif operation == "reachable_nodes":
            payload = {**copy.deepcopy(graph), "source": graph["nodes"][0]}
        elif operation == "shortest_hop_path":
            payload = {
                **copy.deepcopy(graph),
                "source": graph["nodes"][0],
                "target": graph["nodes"][-1],
            }
        elif operation == "dag_status":
            payload = cycle_fixture(index)
        elif operation == "topological_order":
            payload = copy.deepcopy(graph)
        elif operation == "weak_components":
            payload = weak_fixture(index)
        elif operation == "boundary_edges":
            cut = max(1, len(graph["nodes"]) // 2)
            payload = {**copy.deepcopy(graph), "inside": graph["nodes"][:cut]}
        elif operation == "graph_diff":
            after = copy.deepcopy(graph)
            new_node = f"z{index}"
            after["nodes"].append(new_node)
            after["edges"].append([after["nodes"][-2], new_node])
            payload = {"before": graph, "after": after}
        elif operation == "provenance_path_digest":
            payload = {
                **copy.deepcopy(graph),
                "path": list(graph["nodes"]),
                "source_sha256": sha256_bytes(f"source-{index}".encode()),
            }
        elif operation == "correction_chain":
            events = []
            parent = None
            for step in range(3 + index % 3):
                digest = sha256_bytes(f"state-{index}-{step}".encode())
                event_id = f"event-{index}-{step}"
                events.append({"digest": digest, "event_id": event_id, "parent_id": parent})
                parent = event_id
            payload = {"events": events}
        elif operation == "dependency_blockers":
            obligations = [
                {"id": "source", "requires": [], "state": "completed"},
                {"id": "review", "requires": ["source"], "state": "pending"},
                {"id": "release", "requires": ["review"], "state": "pending"},
                {
                    "id": "authority",
                    "requires": [],
                    "state": "open_gap" if index % 2 else "exact_gate",
                },
            ]
            payload = {"obligations": obligations}
        elif operation == "release_gate":
            payload = {
                "authority": "verified" if index % 2 == 0 else "absent",
                "consent": "verified" if index % 3 == 0 else "absent",
                "evidence": "verified" if index % 5 == 0 else "absent",
            }
        elif operation == "critical_path":
            nodes = graph["nodes"]
            weighted = [
                [nodes[item], nodes[item + 1], 1 + (item + index) % 4]
                for item in range(len(nodes) - 1)
            ]
            if len(nodes) >= 4:
                weighted.append([nodes[0], nodes[2], 1])
            payload = {"nodes": nodes, "weighted_edges": weighted}
        elif operation == "accessible_graph_summary":
            payload = {
                "blocked": index % 4,
                "completed": 2 + index,
                "exact_gates": index % 3,
                "open_gaps": (index + 1) % 3,
                "represented": index % 2,
            }
        elif operation == "obligation_reservation":
            payload = {
                "authority": None,
                "evidence": None,
                "kind": "scientific_evidence" if index <= 5 else "competent_authority",
                "obligation": (
                    [
                        "defined observable map",
                        "calibrated empirical comparison",
                        "independent reproduction",
                        "affected-user accessibility evaluation",
                        "complete privacy and security evaluation",
                        "production release authority",
                        "verified consent and remedy authority",
                        "legal and cultural adjudication",
                        "Maori data-governance authority",
                        "Stage 20 promotion",
                    ][index - 1]
                ),
            }
        else:
            raise ValueError(f"unknown operation {operation}")
        payload["case_id"] = index
        values.append(payload)
    return values


def reference(operation: str, payload: dict[str, Any]) -> Any:
    case_id = payload.pop("case_id", None)
    if isinstance(case_id, bool) or not isinstance(case_id, int) or not 1 <= case_id <= 10:
        raise ValueError("invalid_case_id")
    if operation == "graph_diff":
        before_nodes, before_edges = graph_parts(payload["before"])
        after_nodes, after_edges = graph_parts(payload["after"])
        return {
            "added_edges": [list(edge) for edge in sorted(set(after_edges) - set(before_edges))],
            "added_nodes": sorted(set(after_nodes) - set(before_nodes)),
            "removed_edges": [list(edge) for edge in sorted(set(before_edges) - set(after_edges))],
            "removed_nodes": sorted(set(before_nodes) - set(after_nodes)),
            "source_retained": True,
        }
    if operation == "correction_chain":
        events = payload["events"]
        if not isinstance(events, list) or not events:
            raise ValueError("invalid_events")
        seen: set[str] = set()
        parent = None
        digests: list[str] = []
        for event in events:
            if set(event) != {"digest", "event_id", "parent_id"}:
                raise ValueError("invalid_event_shape")
            if (
                not isinstance(event["event_id"], str)
                or event["event_id"] in seen
                or event["parent_id"] != parent
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
        if set(payload) != {"authority", "consent", "evidence"}:
            raise ValueError("invalid_release_gate")
        allowed = {"verified", "absent"}
        if any(payload[key] not in allowed for key in payload):
            raise ValueError("invalid_release_state")
        eligible = all(payload[key] == "verified" for key in payload)
        return {
            "eligible_in_synthetic_model": eligible,
            "real_authority_established": False,
            "requires_external_review": True,
        }
    if operation == "critical_path":
        nodes = string_list(payload["nodes"], "nodes")
        raw = payload["weighted_edges"]
        if not isinstance(raw, list) or not raw:
            raise ValueError("invalid_weighted_edges")
        edges: list[tuple[str, str]] = []
        weights: dict[tuple[str, str], int] = {}
        for row in raw:
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
        order, blocked = kahn(nodes, sorted(edges))
        if blocked or order is None:
            raise ValueError("cycle_not_supported")
        best = {node: (0, [node]) for node in nodes}
        incoming = {node: [] for node in nodes}
        for left, right in edges:
            incoming[right].append(left)
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
    if operation == "accessible_graph_summary":
        if set(payload) != {
            "blocked",
            "completed",
            "exact_gates",
            "open_gaps",
            "represented",
        }:
            raise ValueError("invalid_summary")
        for value in payload.values():
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
        if set(payload) != {"authority", "evidence", "kind", "obligation"}:
            raise ValueError("invalid_reservation")
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

    nodes, edges = graph_parts(payload)
    if operation == "canonical_graph_record":
        return {"directed": True, "edges": [list(edge) for edge in edges], "nodes": nodes}
    if operation == "out_adjacency":
        return {"adjacency": adjacency(nodes, edges), "direction": "outgoing"}
    if operation == "in_adjacency":
        reverse = sorted((right, left) for left, right in edges)
        return {"adjacency": adjacency(nodes, reverse), "direction": "incoming"}
    if operation == "reachable_nodes":
        return {
            "reachable": reachable(nodes, edges, payload["source"]),
            "source": payload["source"],
        }
    if operation == "shortest_hop_path":
        path = shortest_path(nodes, edges, payload["source"], payload["target"])
        return {
            "hops": None if path is None else len(path) - 1,
            "path": path,
            "source": payload["source"],
            "target": payload["target"],
        }
    if operation == "dag_status":
        order, blocked = kahn(nodes, edges)
        return {"blocked_nodes": blocked, "is_dag": order is not None, "order": order}
    if operation == "topological_order":
        order, blocked = kahn(nodes, edges)
        if blocked or order is None:
            raise ValueError("cycle_not_supported")
        return {"lexicographic": True, "order": order}
    if operation == "weak_components":
        return {"components": weak_components(nodes, edges), "directed_edges_retained": True}
    if operation == "transitive_closure":
        return {"pairs": transitive_pairs(nodes, edges), "self_pairs": False}
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
    if operation == "transitive_reduction":
        reduced = transitive_reduction(nodes, edges)
        return {
            "edges": [list(edge) for edge in reduced],
            "reachability_preserved": transitive_pairs(nodes, edges)
            == transitive_pairs(nodes, reduced),
        }
    if operation == "provenance_path_digest":
        path = payload["path"]
        if (
            not isinstance(path, list)
            or not path
            or any(node not in nodes for node in path)
            or any((left, right) not in edges for left, right in pairwise(path))
            or re.fullmatch(r"[0-9a-f]{64}", payload["source_sha256"]) is None
        ):
            raise ValueError("invalid_provenance_path")
        record = {
            "edges": [list(edge) for edge in edges],
            "nodes": nodes,
            "path": path,
            "source_sha256": payload["source_sha256"],
        }
        return {
            "binding_sha256": sha256_bytes(json_bytes(record)),
            "identity_established": False,
            "path_valid": True,
            "source_sha256": payload["source_sha256"],
        }
    if operation == "dot_projection":
        graph_id = payload["graph_id"]
        if not isinstance(graph_id, str) or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", graph_id) is None:
            raise ValueError("invalid_graph_id")
        lines = [f"digraph {graph_id} {{"]
        lines.extend(f"  {json.dumps(node)};" for node in nodes)
        lines.extend(
            f"  {json.dumps(left)} -> {json.dumps(right)};" for left, right in edges
        )
        lines.append("}")
        return {"dot": "\n".join(lines), "rendered": False, "source_retained": True}
    raise ValueError(f"unknown operation {operation}")


def envelope(operation: str, payload: dict[str, Any]) -> dict[str, Any]:
    value = reference(operation, copy.deepcopy(payload))
    outcome = (
        "represented"
        if operation == "accessible_graph_summary"
        else value["state"]
        if operation == "obligation_reservation"
        else "completed"
    )
    return {"ok": True, "operation": operation, "outcome": outcome, "value": value}


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    operations = X1_OPERATIONS + X2_OPERATIONS
    for operation_index, operation in enumerate(operations):
        lane = "x1" if operation_index < 10 else "x2"
        practice = (
            PRACTICES[0]["name"]
            if operation_index < 10
            else PRACTICES[1]["name"]
            if operation_index < 16
            else PRACTICES[2]["name"]
            if operation_index < 18
            else PRACTICES[3]["name"]
        )
        pillar = next(item["pillar"] for item in PRACTICES if item["name"] == practice)
        for case_index, payload in enumerate(fixtures(operation), start=1):
            sequence = operation_index * 10 + case_index
            expected = envelope(operation, payload)
            candidate = copy.deepcopy({"operation": operation, "payload": payload})
            candidate["payload"]["unreviewed_authority_grant"] = True
            outcome = expected["outcome"]
            approval = (
                "exact"
                if outcome == "exact_gate"
                else "blocked"
                if outcome == "open_gap"
                else "candidate"
                if outcome == "represented"
                else "safe_now"
            )
            rows.append(
                {
                    "approval_class": approval,
                    "artifact": f"{lane}/results.json",
                    "candidate_expected": {
                        "error": "unknown_payload_field",
                        "ok": False,
                        "original_success_credit": 0,
                    },
                    "candidate_subject": candidate,
                    "expected": expected,
                    "expected_execution_disposition": outcome,
                    "falsifier": (
                        "Compare the complete typed result, require unchanged input, and require "
                        "the paired unknown authority-field subject to fail."
                    ),
                    "hypothesis": (
                        "This exact finite request agrees with its frozen reference envelope while "
                        "preserving provenance and authority boundaries."
                    ),
                    "lane": lane,
                    "mission": {
                        "x1": "Expose finite directed-graph structure and assumptions exactly.",
                        "x2": "Bind graph-derived evidence without promoting it into consent or authority.",
                    }[lane],
                    "null_or_failure": (
                        "Any complete typed mismatch, accepted unknown field, input mutation, erased "
                        "failed subject, unsupported correction, or authority promotion refutes the claim."
                    ),
                    "operation": operation,
                    "oracle_basis": (
                        "Independent planning reference over finite declared nodes, edges, states, "
                        "or canonical UTF-8 JSON."
                    ),
                    "pillar": pillar,
                    "practice": practice,
                    "proposal_id": f"IF6902-{sequence:03d}",
                    "protected_gates": PROTECTED_GATES,
                    "request": {"operation": operation, "payload": payload},
                    "rollback": (
                        "Retain the frozen request and failed subject, isolate the responsible "
                        "operation, and add a separately attributable correction without erasure."
                    ),
                    "title": (
                        f"Obligation graph {operation.replace('_', ' ')} - fixture {case_index:02d}"
                    ),
                }
            )
    return rows


def inspect_wheels(wheel_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for filename, expected_hash in sorted(PACKAGE_WHEELS.items()):
        path = wheel_dir / filename
        data = path.read_bytes()
        observed_hash = sha256_bytes(data)
        if observed_hash != expected_hash:
            raise RuntimeError(f"wheel hash mismatch: {filename}")
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            unsafe = [
                name
                for name in names
                if PurePosixPath(name).is_absolute()
                or ".." in PurePosixPath(name).parts
                or re.match(r"^[A-Za-z]:", name)
            ]
            if unsafe:
                raise RuntimeError(f"unsafe wheel members: {filename}: {unsafe}")
            metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
            metadata = archive.read(metadata_name).decode("utf-8", errors="replace")
            fields = {}
            for key in ("Name", "Version", "License-Expression", "Requires-Python"):
                match = re.search(rf"^{re.escape(key)}:\s*(.+)$", metadata, flags=re.MULTILINE)
                fields[key.lower().replace("-", "_")] = match.group(1).strip() if match else None
            license_paths = [
                name
                for name in names
                if any(token in PurePosixPath(name).name.lower() for token in ("license", "copying", "notice"))
            ]
        rows.append(
            {
                "bytes": len(data),
                "filename": filename,
                "license_paths": sorted(license_paths),
                "member_count": len(names),
                "metadata": fields,
                "sha256": observed_hash,
                "unsafe_members": unsafe,
            }
        )
    return rows


def inherited_rows(source_root: Path) -> list[dict[str, Any]]:
    source_path = source_root / "docs" / "lyren-moss" / "v690-v1" / "plan" / "new-proposals.json"
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    proposals = payload["proposals"]
    if len(proposals) != 200:
        raise RuntimeError("expected exactly 200 Lyren proposals")
    rows = []
    for index, record in enumerate(proposals, start=1):
        encoded = json_bytes(record)
        rows.append(
            {
                "execution_credit": 0,
                "novelty_credit": 0,
                "record": record,
                "selection_id": f"IF6902-INHERITED-{index:03d}",
                "source_commit": SOURCE_FINAL,
                "source_owner": SOURCE_OWNER,
                "source_phase": SOURCE_PHASE,
                "source_proposal_id": record["proposal_id"],
                "source_record_sha256": sha256_bytes(encoded),
            }
        )
    return rows


def recent_reviews(git_root: Path) -> list[dict[str, Any]]:
    rows = []
    for label, commit, path, lesson in RECENT_BUNDLES:
        data = git_blob(git_root, commit, path)
        text = data.decode("utf-8")
        rows.append(
            {
                "bytes": len(data),
                "commit": commit,
                "label": label,
                "lesson": lesson,
                "lines": len(text.splitlines()),
                "path": path,
                "sha256": sha256_bytes(data),
                "source_execution_credit": 0,
                "source_novelty_credit": 0,
            }
        )
    return rows


def skill_runner_plan() -> dict[str, Any]:
    x1_skills = [f"ghc-family-obligation-graph-{name.replace('_', '-')}" for name in X1_OPERATIONS]
    x2_skills = [f"ghc-family-obligation-graph-{name.replace('_', '-')}" for name in X2_OPERATIONS]
    return {
        "global_candidates": [
            "ghc-family-obligation-graph-structure",
            "ghc-family-obligation-graph-reachability",
            "ghc-family-obligation-graph-dag-contracts",
            "ghc-family-obligation-graph-provenance-correction",
            "ghc-family-obligation-graph-rights-authority",
        ],
        "global_promotion_state": "planned_only_collision_and_compatibility_preflight_required",
        "local_skills_x1": x1_skills,
        "local_skills_x2": x2_skills,
        "runners_x1": [f"ghc_family_obligation_graph_pair_{index:02d}.py" for index in range(1, 6)],
        "runners_x2": [f"ghc_family_obligation_graph_pair_{index:02d}.py" for index in range(6, 11)],
        "successor_runner_ideas": [
            "bounded policy-reachability comparison",
            "strong-component authority quarantine",
            "graph correction lineage replay",
            "multi-root provenance frontier",
            "accessible unresolved-dependency reporter",
            "path ambiguity witness",
            "consent-expiry dependency simulator",
            "transitive-reduction equivalence grid",
            "DOT source fixity reviewer",
            "exact successor source confirmation wrapper",
        ],
        "successor_skill_ideas": [
            "policy reachability assumption ledger",
            "cycle authority quarantine",
            "provenance root conflict map",
            "correction branch nonerasure",
            "dependency expiry guard",
            "consent and authority separation",
            "accessible blocked-path explanation",
            "graph serialization byte-domain receipt",
            "finite-field and graph evidence separator",
            "successor route edge confirmation",
        ],
    }


def exact_packets() -> list[dict[str, Any]]:
    actions = [
        "freeze source provenance",
        "verify source baton through EOF",
        "verify source canonical and route receipts",
        "verify source clean four-way equality",
        "create blank parentless owner branch",
        "freeze recent ten-bundle review",
        "freeze 200 inherited zero-credit selections",
        "freeze 200 new proposal envelopes",
        "freeze x1 safe portfolio",
        "freeze x1 candidate portfolio",
        "freeze x1 cleanup portfolio",
        "freeze x2 safe portfolio",
        "freeze x2 candidate portfolio",
        "freeze x2 cleanup portfolio",
        "freeze package wheel hashes",
        "freeze package rollback",
        "freeze x1 skill interfaces",
        "freeze x1 runner interfaces",
        "freeze x2 skill interfaces",
        "freeze x2 runner interfaces",
        "freeze five global candidates",
        "freeze four practices",
        "freeze two successor practices",
        "freeze source research references",
        "freeze protected evidence gates",
        "commit parentless planning root",
        "push planning root",
        "verify planning root four-way equality",
        "install D-isolated package closure",
        "execute x1 safe cases",
        "execute x1 invalid candidate subjects",
        "execute x1 lossless inherited refinements",
        "validate x1 skills and runners",
        "seal x1 manifest and accounting",
        "commit frozen x1",
        "push and verify frozen x1",
        "execute x2 safe cases",
        "execute x2 invalid candidate subjects",
        "execute x2 lossless inherited refinements",
        "validate x2 skills and runners",
        "promote only collision-free global candidates",
        "build four-tier deck",
        "seal x2 manifest and accounting",
        "commit immutable x2",
        "push and verify immutable x2",
        "build three-page-or-longer report and baton",
        "commit and push exact final",
        "invoke canonical once with no success replay",
        "reread route and exact successor guards",
        "send at most one compact Mira Fenwick activation",
    ]
    return [
        {
            "action": action,
            "executed_during_planning": False,
            "packet_id": f"IF6902-EXACT-{index:03d}",
            "protected": True,
            "state": "planned_exact_prerequisite",
        }
        for index, action in enumerate(actions, start=1)
    ]


def blocked_packets() -> list[dict[str, Any]]:
    subjects = [
        "real participant recruitment",
        "real identity credential issuance",
        "real consent determination",
        "real legal adjudication",
        "real cultural adjudication",
        "Maori authority determination",
        "production deployment",
        "production data migration",
        "host security weakening",
        "credential or secret collection",
        "unbounded repository scan",
        "sibling lane mutation",
        "source history rewrite",
        "force push",
        "canonical success replay",
        "precontacting Mira Fenwick",
        "creating a replacement successor task",
        "substituting a standby or subagent endpoint",
        "independent-reproduction claim",
        "complete privacy claim",
        "complete accessibility claim",
        "exhaustive security claim",
        "professional qualification claim",
        "empirical GMUT confirmation",
        "Theory-of-Everything proof claim",
        "AGI or ASI claim",
        "consciousness or personhood claim",
        "identity continuity claim",
        "Stage 20 promotion",
        "unspecified destructive cleanup",
    ]
    return [
        {
            "executed": False,
            "packet_id": f"IF6902-BLOCKED-{index:03d}",
            "reason": "Missing exact evidence, competent authority, affected-party authority, or safe bounded scope.",
            "state": "blocked",
            "subject": subject,
        }
        for index, subject in enumerate(subjects, start=1)
    ]


def build(source_root: Path, git_root: Path, wheel_dir: Path) -> None:
    PLAN.mkdir(parents=True, exist_ok=True)
    proposals = proposal_rows()
    inherited = inherited_rows(source_root)
    reviews = recent_reviews(git_root)
    wheel_reviews = inspect_wheels(wheel_dir)
    outcomes: dict[str, int] = {"completed": 0, "represented": 0, "open_gap": 0, "exact_gate": 0}
    for row in proposals:
        outcomes[row["expected_execution_disposition"]] += 1
    if outcomes != {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}:
        raise RuntimeError(f"unexpected outcome plan: {outcomes}")

    write_text(
        PLAN / "authorization.md",
        f"""# Ilyra Fen v690-v2 authorization and boundary

Hamish's current 45-position, 30-identity workflow and Lyren Moss's acknowledged one-send activation authorize this owner phase. The route position is Ilyra Fen v690-v2, with Mira Fenwick v690-v3 prospective only after Ilyra's exact terminal gate. No replacement task, fork, collaboration subagent, model override, sibling mutation, early successor contact, destructive cleanup, or canonical replay is authorized.

The branch is {BRANCH}. It is a parentless owner root. Lyren exact final {SOURCE_FINAL} is explicit provenance and is not Git ancestry.

{RELATIONAL_BOUNDARY}

{BOUNDARY}

Terminal planning verdict: NOT_READY_FOR_STAGE_20.
""",
    )
    write_json(
        PLAN / "profile.json",
        {
            "boundary": BOUNDARY,
            "branch": BRANCH,
            "commit_budget": {"planning": 1, "x1": 2, "x2": 3, "final": 2, "total": 8},
            "file_ceiling": 2000,
            "hope": "make dependency, correction, and authority boundaries inspectable without turning reachability into permission",
            "outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "owner": OWNER,
            "phase": PHASE,
            "pillar_primary": "Freed ID and CBR Heart",
            "practices": PRACTICES,
            "pronouns": ["they", "them"],
            "relational_boundary": RELATIONAL_BOUNDARY,
            "role": "directed-obligation provenance cartographer",
            "schema": "ghc.family.owner-profile.v1",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PLAN / "source-provenance.json",
        {
            "baton": SOURCE_BATON,
            "baton_sha256": SOURCE_BATON_SHA256,
            "canonical_receipt_sha256": SOURCE_CANONICAL_SHA256,
            "final": SOURCE_FINAL,
            "owner": SOURCE_OWNER,
            "phase": SOURCE_PHASE,
            "route_delivery_state": "SENT_ONCE_ACKNOWLEDGED",
            "source_is_ancestor": False,
            "source_validation_credit": 0,
            "x1": SOURCE_X1,
            "x2": SOURCE_X2,
        },
    )
    write_json(
        PLAN / "route.json",
        {
            "current": {"owner": OWNER, "phase": PHASE, "position": 8},
            "endpoint_kind": "main_task",
            "next": {"owner": "Mira Fenwick", "phase": "v690-v3", "position": 9},
            "next_state": "prospective_terminal_only",
            "precontacted": False,
            "replacement_creation_authorized": False,
            "route_terminal": "Teryn Halewick v725-v8",
            "send_limit": 1,
            "standby_substitution_authorized": False,
        },
    )
    write_json(
        PLAN / "recent-bundle-review.json",
        {
            "count": len(reviews),
            "records": reviews,
            "review_credit": "context_only_zero_source_execution_or_novelty_credit",
            "schema": "ghc.family.recent-bundle-review.v1",
        },
    )
    write_json(
        PLAN / "inherited-selections.json",
        {
            "count": len(inherited),
            "records": inherited,
            "source_commit": SOURCE_FINAL,
            "source_execution_credit": 0,
            "source_novelty_credit": 0,
        },
    )
    write_json(
        PLAN / "new-proposals.json",
        {
            "planning_only": True,
            "production_evaluator_executed": False,
            "proposals": proposals,
            "reference_oracle_credit": "planning_definition_only",
        },
    )
    for lane, subset in (("x1", proposals[:100]), ("x2", proposals[100:])):
        inherited_subset = inherited[:100] if lane == "x1" else inherited[100:]
        write_json(
            PLAN / f"portfolio-{lane}.json",
            {
                "candidate_tasks": [
                    {
                        "candidate_expected": row["candidate_expected"],
                        "candidate_subject": row["candidate_subject"],
                        "original_success_credit": 0,
                        "proposal_id": row["proposal_id"],
                        "task_id": f"IF6902-{lane.upper()}-CANDIDATE-{index:03d}",
                    }
                    for index, row in enumerate(subset, start=1)
                ],
                "clean_fix_refine_tasks": [
                    {
                        "action": "canonicalize, parse, re-encode, and compare the exact inherited record",
                        "expected": "lossless_equal_without_source_execution_or_novelty_credit",
                        "selection_id": row["selection_id"],
                        "task_id": f"IF6902-{lane.upper()}-CLEAN-{index:03d}",
                    }
                    for index, row in enumerate(inherited_subset, start=1)
                ],
                "execution_state": "frozen_not_executed",
                "lane": lane,
                "safe_tasks": [
                    {
                        "expected": row["expected"],
                        "proposal_id": row["proposal_id"],
                        "request": row["request"],
                        "task_id": f"IF6902-{lane.upper()}-SAFE-{index:03d}",
                    }
                    for index, row in enumerate(subset, start=1)
                ],
            },
        )
    write_json(PLAN / "exact-packets.json", {"count": 50, "packets": exact_packets()})
    write_json(PLAN / "blocked-packets.json", {"count": 30, "packets": blocked_packets()})
    write_json(PLAN / "identity-practices.json", {"owner_practices": PRACTICES, "successor_practices": SUCCESSOR_PRACTICES})
    write_json(PLAN / "skills-runners.json", skill_runner_plan())
    write_json(
        PLAN / "package-plan.json",
        {
            "direct_count": 3,
            "environment": "D-isolated owner environment only",
            "installation_state": "downloaded_not_installed_at_planning",
            "no_index_hash_required_install_planned": True,
            "packages": wheel_reviews,
            "registry": "PyPI official distribution files",
            "rollback": "Stop selecting the exact D environment; preserve wheels and receipts.",
            "shared_prefix_mutation": False,
            "supply_chain_boundary": "Point-in-time wheel metadata and bytes only; not exhaustive security, license advice, or endorsement.",
        },
    )
    write_text(
        PLAN / "research-sources.md",
        """# Ilyra v690-v2 research sources and limits

- A. B. Kahn, Topological sorting of large networks, DOI 10.1145/368996.369025.
- A. V. Aho, M. R. Garey, and J. D. Ullman, The Transitive Reduction of a Directed Graph, DOI 10.1137/0201008.
- RFC 8785, JSON Canonicalization Scheme, https://www.rfc-editor.org/rfc/rfc8785.html.
- W3C PROV-O Recommendation, https://www.w3.org/TR/prov-o/.
- W3C Verifiable Credentials Data Model 2.0 Recommendation, https://www.w3.org/TR/vc-data-model-2.0/.
- Graphviz DOT language, https://graphviz.org/doc/info/lang.html.
- NetworkX 3.6.1, rustworkx 0.18.1, and graphviz 0.21 official PyPI records.

These sources define vocabulary, established algorithms, standards context, and package provenance. They do not validate this implementation, transfer authorship or authority, establish consent or identity, or support empirical GMUT, production THOS, live Freed ID, independent reproduction, a Theory of Everything, or Stage 20.
""",
    )
    write_json(
        PLAN / "additional-work.json",
        {
            "new_proposals": 200,
            "inherited_proposals": 200,
            "safe_each_session": 100,
            "candidate_each_session": 100,
            "clean_fix_refine_each_session": 100,
            "skills_each_session": 10,
            "runners_each_session": 5,
            "successor_practices": SUCCESSOR_PRACTICES,
            "successor_skill_ideas": skill_runner_plan()["successor_skill_ideas"],
            "successor_runner_ideas": skill_runner_plan()["successor_runner_ideas"],
        },
    )
    write_json(
        PLAN / "startup-failures.json",
        {
            "metric_domain_note": {
                "canonical_unicode_regex_words": 36762,
                "whitespace_words": 35550,
                "state": "different_declared_counting_domains_not_a_source_seal_mismatch",
            },
            "records": [
                {
                    "failure": "The first 250-line baton window exceeded the display budget and was truncated.",
                    "id": "IF6902-STARTUP-F001",
                    "original_success_credit": 0,
                    "recovery": "Reread the affected range as two exact 125-line windows and continue through literal EOF.",
                },
                {
                    "failure": "A PowerShell foreach projection piped directly after the block and hit an empty-pipeline parser error.",
                    "id": "IF6902-STARTUP-F002",
                    "original_success_credit": 0,
                    "recovery": "Materialize the projection array before Format-Table.",
                },
                {
                    "failure": "The first combined orphan-switch readback rendered no attributable summary although the operation completed.",
                    "id": "IF6902-STARTUP-F003",
                    "original_success_credit": 0,
                    "recovery": "Use symbolic-ref, unborn-HEAD, tracked-file, physical-file, and porcelain scalar probes.",
                },
                {
                    "failure": "The first broad source-thread reread exceeded its output budget.",
                    "id": "IF6902-STARTUP-F004",
                    "original_success_credit": 0,
                    "recovery": "Use only the bounded terminal artifact paths exposed in the truncated result, then read those files directly.",
                },
                {
                    "failure": "A combined Elaren and Eiren overview display truncated the Eiren record.",
                    "id": "IF6902-STARTUP-F005",
                    "original_success_credit": 0,
                    "recovery": "Reread Eiren alone in two bounded 75-line windows.",
                },
                {
                    "failure": "The first planning test aggregate found only 145 distinct complete request bodies across 200 proposal rows.",
                    "id": "IF6902-STARTUP-F006",
                    "original_success_credit": 0,
                    "recovery": "Add a required bounded case_id to every frozen payload, regenerate planning, and rerun only the planning suite.",
                },
                {
                    "failure": "The bare ruff command was not exposed on the current PowerShell PATH.",
                    "id": "IF6902-STARTUP-F007",
                    "original_success_credit": 0,
                    "recovery": "Use the attributable python -m ruff entrypoint from the current interpreter.",
                },
                {
                    "failure": "The first Ruff module pass found two import-order findings, two sorted-min findings, and one successive-pair finding.",
                    "id": "IF6902-STARTUP-F008",
                    "original_success_credit": 0,
                    "recovery": "Apply import formatting, use min with the declared tie key, and use itertools.pairwise; rerun only the two planning Python files.",
                },
                {
                    "failure": "A post-Ruff planning test found that the manifest had inventoried a mutable .ruff_cache entry that Ruff then changed.",
                    "id": "IF6902-STARTUP-F009",
                    "original_success_credit": 0,
                    "recovery": "Exclude ephemeral caches from owner manifests, remove only the verified owner-local cache, and run Ruff with --no-cache.",
                },
                {
                    "failure": "The first verified literal recursive cache-removal command was rejected by the command policy before execution.",
                    "id": "IF6902-STARTUP-F010",
                    "original_success_credit": 0,
                    "recovery": "Use the supported python -m ruff clean operation in the exact Ilyra worktree; it removed only .ruff_cache.",
                },
                {
                    "failure": "The first exact staged allowlist found that the planning manifest had included the administrative .git pointer file.",
                    "id": "IF6902-STARTUP-F011",
                    "original_success_credit": 0,
                    "recovery": "Exclude the literal .git administrative file from owner manifests, regenerate, and rerun the exact staged allowlist.",
                },
                {
                    "failure": "The first combined planning stage wrapper returned no attributable display although staging completed.",
                    "id": "IF6902-STARTUP-F012",
                    "original_success_credit": 0,
                    "recovery": "Use a separate scalar staged-name and porcelain readback before evaluating the allowlist.",
                },
            ],
        },
    )
    write_json(
        PLAN / "phase-truth.json",
        {
            "canonical_invoked": False,
            "core_outcomes_planned": outcomes,
            "execution_complete": False,
            "owner": OWNER,
            "phase": PHASE,
            "planning_only": True,
            "route_state": "NOT_ELIGIBLE_BEFORE_TERMINAL",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PLAN / "allowlist.json",
        {
            "allowed_prefixes": [
                ".gitattributes",
                ".gitignore",
                "docs/ilyra-fen/v690-v2/plan/",
                "scripts/build_ghc_family_ilyra_v690_v2_plan.py",
                "tests/test_ghc_family_ilyra_v690_v2_plan.py",
            ],
            "planning_only": True,
        },
    )
    manifest_entries = []
    for path in sorted(candidate for candidate in ROOT.rglob("*") if candidate.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative == "docs/ilyra-fen/v690-v2/plan/manifest.json":
            continue
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if {".ruff_cache", ".pytest_cache", "__pycache__"} & set(path.relative_to(ROOT).parts):
            continue
        data = path.read_bytes()
        manifest_entries.append(
            {
                "bytes": len(data),
                "hash_domain": "raw_worktree_bytes_before_planning_commit",
                "path": relative,
                "sha256": sha256_bytes(data),
            }
        )
    write_json(
        PLAN / "manifest.json",
        {
            "entries": manifest_entries,
            "entry_count": len(manifest_entries),
            "schema": "ghc.family.owner-manifest.v1",
            "self_excluded": "manifest.json",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--git-source-root", required=True)
    parser.add_argument("--wheel-dir", required=True)
    args = parser.parse_args()
    build(Path(args.source_root).resolve(), Path(args.git_source_root).resolve(), Path(args.wheel_dir).resolve())
    print(
        json.dumps(
            {
                "inherited": 200,
                "new": 200,
                "outcomes": {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5},
                "packages": 3,
                "state": "PLANNING_ONLY_FROZEN",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
