#!/usr/bin/env python3
"""Bounded finite abstract-simplicial-complex evidence for Mira Fenwick v707-v3.

The module uses exact finite enumeration and GF(2) linear algebra over synthetic
records only. It does not model people, institutions, rights, physical systems,
or operational authority.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from typing import Any, Iterable


MAX_VERTICES = 7


class SimplicialRecordError(ValueError):
    """Raised when a finite simplicial-complex record violates the contract."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != {"id", "vertices", "facets"}:
        raise SimplicialRecordError("record must contain exactly id, vertices, and facets")
    if not isinstance(record["id"], str) or not record["id"]:
        raise SimplicialRecordError("id must be a nonempty string")
    vertices = record["vertices"]
    if not isinstance(vertices, list) or not 1 <= len(vertices) <= MAX_VERTICES:
        raise SimplicialRecordError(f"vertices must be a list of length 1..{MAX_VERTICES}")
    if any(not isinstance(vertex, str) or not vertex for vertex in vertices):
        raise SimplicialRecordError("every vertex must be a nonempty string")
    if len(vertices) != len(set(vertices)):
        raise SimplicialRecordError("vertices must be unique")
    if vertices != sorted(vertices):
        raise SimplicialRecordError("vertices must be sorted")

    facets = record["facets"]
    if not isinstance(facets, list) or not facets:
        raise SimplicialRecordError("facets must be a nonempty list")
    normalized: list[tuple[str, ...]] = []
    for facet in facets:
        if not isinstance(facet, list) or not facet:
            raise SimplicialRecordError("every facet must be a nonempty list")
        if any(not isinstance(vertex, str) or vertex not in vertices for vertex in facet):
            raise SimplicialRecordError("facet contains an undeclared vertex")
        if len(facet) != len(set(facet)):
            raise SimplicialRecordError("facet vertices must be unique")
        if facet != sorted(facet):
            raise SimplicialRecordError("facet vertices must be sorted")
        normalized.append(tuple(facet))
    if len(normalized) != len(set(normalized)):
        raise SimplicialRecordError("duplicate facets are forbidden")
    if normalized != sorted(normalized):
        raise SimplicialRecordError("facets must be sorted")
    facet_sets = [set(facet) for facet in normalized]
    for index, left in enumerate(facet_sets):
        if any(index != other and left < right for other, right in enumerate(facet_sets)):
            raise SimplicialRecordError("facets must be inclusion-maximal")
    covered = set().union(*facet_sets)
    if covered != set(vertices):
        raise SimplicialRecordError("every declared vertex must occur in a facet")
    return {"id": record["id"], "vertices": list(vertices), "facets": [list(facet) for facet in normalized]}


def _subsets(values: tuple[str, ...], include_empty: bool = True) -> Iterable[tuple[str, ...]]:
    start = 0 if include_empty else 1
    for size in range(start, len(values) + 1):
        yield from combinations(values, size)


def faces(record: dict[str, Any], include_empty: bool = True) -> list[tuple[str, ...]]:
    checked = validate_record(record)
    result: set[tuple[str, ...]] = {()}
    for facet in checked["facets"]:
        result.update(_subsets(tuple(facet), include_empty=True))
    if not include_empty:
        result.discard(())
    return sorted(result, key=lambda face: (len(face), face))


def faces_by_dimension(record: dict[str, Any]) -> dict[int, list[tuple[str, ...]]]:
    grouped: dict[int, list[tuple[str, ...]]] = {}
    for face in faces(record, include_empty=False):
        grouped.setdefault(len(face) - 1, []).append(face)
    return grouped


def boundary_matrix(record: dict[str, Any], dimension: int) -> dict[str, Any]:
    grouped = faces_by_dimension(record)
    columns = grouped.get(dimension, [])
    if dimension <= 0:
        return {"dimension": dimension, "rows": [], "columns": [list(face) for face in columns], "matrix": []}
    rows = grouped.get(dimension - 1, [])
    row_index = {face: index for index, face in enumerate(rows)}
    matrix = [[0 for _ in columns] for _ in rows]
    for column_index, simplex in enumerate(columns):
        for removed in range(len(simplex)):
            face = simplex[:removed] + simplex[removed + 1 :]
            matrix[row_index[face]][column_index] ^= 1
    return {
        "dimension": dimension,
        "rows": [list(face) for face in rows],
        "columns": [list(face) for face in columns],
        "matrix": matrix,
    }


def gf2_rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    work = [sum((value & 1) << column for column, value in enumerate(row)) for row in matrix]
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work)) if (work[row] >> column) & 1), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for row in range(len(work)):
            if row != rank and ((work[row] >> column) & 1):
                work[row] ^= work[rank]
        rank += 1
        if rank == len(work):
            break
    return rank


def _matmul_mod2(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    if not left:
        return []
    inner = len(left[0])
    if inner != len(right):
        raise ValueError("matrix dimensions do not compose")
    width = len(right[0]) if right else 0
    return [
        [sum(left[row][middle] * right[middle][column] for middle in range(inner)) % 2 for column in range(width)]
        for row in range(len(left))
    ]


def boundary_square_zero(record: dict[str, Any]) -> bool:
    grouped = faces_by_dimension(record)
    maximum = max(grouped, default=0)
    for dimension in range(2, maximum + 1):
        lower = boundary_matrix(record, dimension - 1)["matrix"]
        upper = boundary_matrix(record, dimension)["matrix"]
        if any(value for row in _matmul_mod2(lower, upper) for value in row):
            return False
    return True


def connected_components(record: dict[str, Any]) -> list[list[str]]:
    checked = validate_record(record)
    vertices = checked["vertices"]
    adjacency = {vertex: set() for vertex in vertices}
    for edge in faces_by_dimension(checked).get(1, []):
        left, right = edge
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(vertices)
    components: list[list[str]] = []
    while unseen:
        root = min(unseen)
        queue = deque([root])
        unseen.remove(root)
        component: list[str] = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbour in sorted(adjacency[vertex] & unseen):
                unseen.remove(neighbour)
                queue.append(neighbour)
        components.append(sorted(component))
    return components


def analyze(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    grouped = faces_by_dimension(checked)
    maximum = max(grouped)
    f_vector = [len(grouped.get(dimension, [])) for dimension in range(maximum + 1)]
    ranks = [0] + [gf2_rank(boundary_matrix(checked, dimension)["matrix"]) for dimension in range(1, maximum + 1)]
    ranks_after = ranks[1:] + [0]
    betti = [f_vector[index] - ranks[index] - ranks_after[index] for index in range(maximum + 1)]
    reduced = [betti[0] - 1, *betti[1:]]
    euler = sum((1 if dimension % 2 == 0 else -1) * count for dimension, count in enumerate(f_vector))
    result: dict[str, Any] = {
        "id": checked["id"],
        "vertex_count": len(checked["vertices"]),
        "dimension": maximum,
        "facet_count": len(checked["facets"]),
        "nonempty_face_count": sum(f_vector),
        "f_vector": f_vector,
        "one_skeleton_edges": [list(edge) for edge in grouped.get(1, [])],
        "component_count": len(connected_components(checked)),
        "components": connected_components(checked),
        "boundary_ranks": ranks,
        "boundary_square_zero": boundary_square_zero(checked),
        "betti_numbers": betti,
        "reduced_betti_numbers": reduced,
        "euler_characteristic": euler,
        "euler_poincare_value": sum((1 if dimension % 2 == 0 else -1) * value for dimension, value in enumerate(betti)),
        "source_sha256": digest(checked),
    }
    result["euler_poincare_passed"] = result["euler_characteristic"] == result["euler_poincare_value"]
    result["result_sha256"] = digest(result)
    return result


def _oracle_column_rank(columns: list[set[int]]) -> int:
    basis: dict[int, set[int]] = {}
    for original in columns:
        column = set(original)
        while column:
            pivot = max(column)
            if pivot in basis:
                column ^= basis[pivot]
            else:
                basis[pivot] = column
                break
    return len(basis)


def oracle_counts(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    vertices = tuple(checked["vertices"])
    facets = [set(facet) for facet in checked["facets"]]
    brute_faces = [subset for subset in _subsets(vertices, include_empty=False) if any(set(subset) <= facet for facet in facets)]
    maximum = max(len(face) - 1 for face in brute_faces)
    grouped = {dimension: [face for face in brute_faces if len(face) == dimension + 1] for dimension in range(maximum + 1)}
    f_vector = [len(grouped[dimension]) for dimension in range(maximum + 1)]
    ranks = [0]
    for dimension in range(1, maximum + 1):
        lower = {face: index for index, face in enumerate(grouped[dimension - 1])}
        columns = []
        for simplex in grouped[dimension]:
            columns.append({lower[simplex[:removed] + simplex[removed + 1 :]] for removed in range(len(simplex))})
        ranks.append(_oracle_column_rank(columns))
    betti = [f_vector[index] - ranks[index] - (ranks[index + 1] if index + 1 < len(ranks) else 0) for index in range(len(f_vector))]
    edges = [set(face) for face in grouped.get(1, [])]
    remaining = set(vertices)
    component_count = 0
    while remaining:
        component_count += 1
        frontier = {min(remaining)}
        remaining -= frontier
        while frontier:
            reached = {vertex for edge in edges if edge & frontier for vertex in edge if vertex in remaining}
            remaining -= reached
            frontier = reached
    euler = sum((1 if dimension % 2 == 0 else -1) * count for dimension, count in enumerate(f_vector))
    return {
        "dimension": maximum,
        "nonempty_face_count": len(brute_faces),
        "f_vector": f_vector,
        "component_count": component_count,
        "boundary_ranks": ranks,
        "betti_numbers": betti,
        "euler_characteristic": euler,
    }


def relabel(record: dict[str, Any]) -> dict[str, Any]:
    checked = validate_record(record)
    mapping = {vertex: f"r{index:02d}" for index, vertex in enumerate(reversed(checked["vertices"]))}
    vertices = sorted(mapping.values())
    facets = sorted([sorted(mapping[vertex] for vertex in facet) for facet in checked["facets"]])
    return validate_record({"id": checked["id"] + "-RELABEL", "vertices": vertices, "facets": facets})


def induced_vertex_deletion(record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    checked = validate_record(record)
    removed = checked["vertices"][-1]
    remaining = [vertex for vertex in checked["vertices"] if vertex != removed]
    candidates = {tuple(vertex for vertex in facet if vertex != removed) for facet in checked["facets"]}
    candidates.discard(())
    maximal = sorted(candidate for candidate in candidates if not any(set(candidate) < set(other) for other in candidates))
    if not maximal:
        maximal = [(remaining[0],)]
    return removed, validate_record({"id": checked["id"] + "-DELETE", "vertices": remaining, "facets": [list(facet) for facet in maximal]})


def barycentric_subdivision_f_vector(record: dict[str, Any]) -> list[int]:
    nonempty = faces(record, include_empty=False)
    chain_counts: dict[tuple[str, ...], list[int]] = {}
    totals = [0] * (max(len(face) for face in nonempty) + 1)
    for face in nonempty:
        counts = [0] * (len(face) + 1)
        counts[1] = 1
        face_set = set(face)
        for smaller, smaller_counts in chain_counts.items():
            if set(smaller) < face_set:
                for length in range(1, len(smaller_counts)):
                    counts[length + 1] += smaller_counts[length]
        chain_counts[face] = counts
        for length, count in enumerate(counts):
            if length:
                totals[length] += count
    while totals and totals[-1] == 0:
        totals.pop()
    return totals[1:]


def transformation_checks(record: dict[str, Any]) -> dict[str, Any]:
    baseline = analyze(record)
    relabeled = analyze(relabel(record))
    removed, deletion = induced_vertex_deletion(record)
    deleted = analyze(deletion)
    subdivision = barycentric_subdivision_f_vector(record)
    subdivision_euler = sum((1 if dimension % 2 == 0 else -1) * count for dimension, count in enumerate(subdivision))
    invariant_keys = ("dimension", "nonempty_face_count", "f_vector", "component_count", "boundary_ranks", "betti_numbers", "euler_characteristic")
    return {
        "fixture_id": record["id"],
        "relabel_covariant": all(baseline[key] == relabeled[key] for key in invariant_keys),
        "vertex_deletion": {
            "removed": removed,
            "result_id": deletion["id"],
            "vertex_count": deleted["vertex_count"],
            "f_vector": deleted["f_vector"],
            "betti_numbers": deleted["betti_numbers"],
            "valid": True,
        },
        "barycentric_subdivision_census": {
            "f_vector": subdivision,
            "euler_characteristic": subdivision_euler,
            "expected_euler_characteristic": baseline["euler_characteristic"],
            "passed": subdivision_euler == baseline["euler_characteristic"],
        },
        "euler_poincare": {
            "euler_characteristic": baseline["euler_characteristic"],
            "betti_alternating_sum": baseline["euler_poincare_value"],
            "passed": baseline["euler_poincare_passed"],
        },
    }


def fixtures() -> list[dict[str, Any]]:
    specifications = [
        ("SC01-EDGE", ["a", "b"], [["a", "b"]]),
        ("SC02-TWO-POINTS", ["a", "b"], [["a"], ["b"]]),
        ("SC03-PATH3", ["a", "b", "c"], [["a", "b"], ["b", "c"]]),
        ("SC04-FILLED-TRIANGLE", ["a", "b", "c"], [["a", "b", "c"]]),
        ("SC05-TRIANGLE-CYCLE", ["a", "b", "c"], [["a", "b"], ["a", "c"], ["b", "c"]]),
        ("SC06-DISJOINT-EDGES", ["a", "b", "c", "d"], [["a", "b"], ["c", "d"]]),
        ("SC07-SQUARE-CYCLE", ["a", "b", "c", "d"], [["a", "b"], ["a", "d"], ["b", "c"], ["c", "d"]]),
        ("SC08-TRIANGULATED-SQUARE", ["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d"]]),
        ("SC09-FILLED-TETRAHEDRON", ["a", "b", "c", "d"], [["a", "b", "c", "d"]]),
        ("SC10-TETRAHEDRON-BOUNDARY", ["a", "b", "c", "d"], [["a", "b", "c"], ["a", "b", "d"], ["a", "c", "d"], ["b", "c", "d"]]),
        ("SC11-BOWTIE", ["a", "b", "c", "d", "e"], [["a", "b", "c"], ["c", "d", "e"]]),
        ("SC12-CYCLE5", ["a", "b", "c", "d", "e"], [["a", "b"], ["a", "e"], ["b", "c"], ["c", "d"], ["d", "e"]]),
        ("SC13-DISJOINT-TRIANGLES", ["a", "b", "c", "d", "e", "f"], [["a", "b", "c"], ["d", "e", "f"]]),
        ("SC14-CONE-ON-SQUARE", ["a", "b", "c", "d", "e"], [["a", "b", "e"], ["a", "d", "e"], ["b", "c", "e"], ["c", "d", "e"]]),
        ("SC15-OCTAHEDRON-BOUNDARY", ["a", "b", "c", "d", "e", "f"], [["a", "c", "e"], ["a", "c", "f"], ["a", "d", "e"], ["a", "d", "f"], ["b", "c", "e"], ["b", "c", "f"], ["b", "d", "e"], ["b", "d", "f"]]),
    ]
    return [validate_record({"id": ident, "vertices": vertices, "facets": sorted(facets)}) for ident, vertices, facets in specifications]


def run_x1_tests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in fixtures():
        result = analyze(record)
        oracle = oracle_counts(record)
        observed = {key: result[key] for key in oracle}
        rows.append({
            "id": f"MF7073-X1-ORACLE-{record['id']}",
            "passed": observed == oracle and result["boundary_square_zero"] and result["euler_poincare_passed"],
            "observed": observed,
            "oracle": oracle,
        })
    malformed = [
        ("duplicate-vertex", {"id": "BAD-DUP", "vertices": ["a", "a"], "facets": [["a"]]}),
        ("unknown-vertex", {"id": "BAD-END", "vertices": ["a", "b"], "facets": [["a", "c"]]}),
        ("unsorted-facet", {"id": "BAD-SORT", "vertices": ["a", "b"], "facets": [["b", "a"]]}),
        ("nonmaximal-facet", {"id": "BAD-MAX", "vertices": ["a", "b", "c"], "facets": [["a", "b"], ["a", "b", "c"]]}),
        ("uncovered-vertex", {"id": "BAD-COVER", "vertices": ["a", "b", "c"], "facets": [["a", "b"]]}),
    ]
    for name, subject in malformed:
        rejected = False
        reason = ""
        try:
            validate_record(subject)
        except SimplicialRecordError as exc:
            rejected = True
            reason = str(exc)
        rows.append({
            "id": f"MF7073-X1-INVALID-{name}",
            "passed": rejected,
            "invalid_subject_state": "fail",
            "invalid_subject_success_credit": 0,
            "refusal_guard_state": "pass" if rejected else "fail",
            "reason": reason,
        })
    return rows


def run_x2_tests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    keys = ("dimension", "nonempty_face_count", "f_vector", "component_count", "boundary_ranks", "betti_numbers", "euler_characteristic")
    for record in fixtures():
        baseline = analyze(record)
        changed = analyze(relabel(record))
        rows.append({
            "id": f"MF7073-X2-RELABEL-{record['id']}",
            "passed": all(baseline[key] == changed[key] for key in keys),
            "baseline": {key: baseline[key] for key in keys},
            "changed": {key: changed[key] for key in keys},
        })
    for record in fixtures():
        baseline = analyze(record)
        subdivision = barycentric_subdivision_f_vector(record)
        subdivision_euler = sum((1 if dimension % 2 == 0 else -1) * count for dimension, count in enumerate(subdivision))
        rows.append({
            "id": f"MF7073-X2-SUBDIVISION-{record['id']}",
            "passed": subdivision_euler == baseline["euler_characteristic"],
            "baseline_euler": baseline["euler_characteristic"],
            "subdivision_euler": subdivision_euler,
            "subdivision_f_vector": subdivision,
        })
    return rows


if __name__ == "__main__":
    payload = {
        "fixtures": fixtures(),
        "analyses": [analyze(record) for record in fixtures()],
        "x1": run_x1_tests(),
        "x2": run_x2_tests(),
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
