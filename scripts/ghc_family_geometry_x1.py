"""Bounded exact simplicial and graph calculations on explicit synthetic inputs.

The evaluator never imports frozen expected values or reads source proposal tables.
All matrix ranks use rational elimination; torsion and real mesh geometry are out
of scope. Existing mathematical identities are not empirical GMUT evidence.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations


class ContractError(ValueError):
    """A typed refusal of this bounded input profile."""


def require(condition, code):
    if not condition:
        raise ContractError(code)


def integer(value):
    require(type(value) is int and abs(value) <= 1_000_000, 'E_INTEGER')
    return value


def fields(payload, names):
    require(type(payload) is dict, 'E_PAYLOAD')
    require(set(payload) == set(names), 'E_PAYLOAD_FIELDS')


def simplex(value):
    require(type(value) is list and 1 <= len(value) <= 4, 'E_SIMPLEX')
    for vertex in value:
        integer(vertex)
        require(vertex >= 0, 'E_VERTEX')
    require(len(set(value)) == len(value), 'E_DUPLICATE_VERTEX')
    return tuple(value)


def orientation(value):
    """Parity by permutation cycles, separate from the plan's inversion oracle."""
    ordered = sorted(value)
    ranks = {vertex: i for i, vertex in enumerate(ordered)}
    permutation = [ranks[vertex] for vertex in value]
    visited, cycles = set(), 0
    for start in range(len(value)):
        if start in visited:
            continue
        cycles += 1
        j = start
        while j not in visited:
            visited.add(j)
            j = permutation[j]
    return (-1) ** (len(value) - cycles)


def boundary(chain):
    result = defaultdict(int)
    for cell, coefficient in chain.items():
        if len(cell) == 1:
            continue
        for i in range(len(cell)):
            face = cell[:i] + cell[i + 1:]
            result[tuple(sorted(face))] += coefficient * (-1) ** i * orientation(face)
    return {cell: value for cell, value in result.items() if value}


def chain_list(chain):
    return [[list(cell), value] for cell, value in sorted(chain.items())]


def complex_cells(facets):
    require(type(facets) is list and 1 <= len(facets) <= 64, 'E_FACETS')
    parsed = [tuple(sorted(simplex(facet))) for facet in facets]
    require(len(set(parsed)) == len(parsed), 'E_DUPLICATE_FACET')
    all_cells = set()
    for facet in parsed:
        for size in range(1, len(facet) + 1):
            all_cells.update(combinations(facet, size))
    cells = [sorted(cell for cell in all_cells if len(cell) == size)
             for size in range(1, max(map(len, parsed)) + 1)]
    require(len(cells[0]) <= 32 and all(len(row) <= 64 for row in cells), 'E_CAPACITY')
    return cells


def boundary_matrix(cells, dimension):
    if dimension <= 0 or dimension >= len(cells):
        return []
    lower, upper = cells[dimension - 1], cells[dimension]
    rows = {cell: i for i, cell in enumerate(lower)}
    matrix = [[0] * len(upper) for _ in lower]
    for j, cell in enumerate(upper):
        for face, coefficient in boundary({cell: 1}).items():
            matrix[rows[face]][j] = coefficient
    return matrix


def rank(matrix):
    if not matrix:
        return 0
    width = len(matrix[0])
    require(len(matrix) <= 64 and width <= 65, 'E_CAPACITY')
    require(all(len(row) == width for row in matrix), 'E_MATRIX')
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(width):
        pivot = next((i for i in range(pivot_row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for i in range(len(work)):
            if i != pivot_row and work[i][column]:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def graph(payload):
    vertices, edges = payload['vertices'], payload['edges']
    require(type(vertices) is list and 1 <= len(vertices) <= 32, 'E_VERTICES')
    for vertex in vertices:
        integer(vertex)
        require(vertex >= 0, 'E_VERTEX')
    require(len(set(vertices)) == len(vertices), 'E_DUPLICATE_VERTEX')
    require(type(edges) is list and len(edges) <= 64, 'E_EDGES')
    seen = set()
    for edge in edges:
        require(type(edge) is list and len(edge) == 2, 'E_EDGE')
        for vertex in edge:
            integer(vertex)
        require(edge[0] != edge[1] and all(v in vertices for v in edge), 'E_EDGE')
        key = tuple(sorted(edge))
        require(key not in seen, 'E_DUPLICATE_EDGE')
        seen.add(key)
    return vertices, edges


def vector(value, length, positive=False):
    require(type(value) is list and len(value) == length, 'E_VECTOR')
    result = [integer(x) for x in value]
    if positive:
        require(all(x > 0 for x in result), 'E_WEIGHT')
    return result


def components(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    remaining, result = set(vertices), []
    while remaining:
        pending = [min(remaining)]
        visited = set()
        while pending:
            vertex = pending.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            pending.extend(adjacency[vertex] - visited)
        remaining.difference_update(visited)
        result.append(sorted(visited))
    return result


def graph_boundary(vertices, edges, coefficients):
    result = {vertex: 0 for vertex in vertices}
    for (a, b), coefficient in zip(edges, coefficients):
        result[a] -= coefficient
        result[b] += coefficient
    return [[vertex, value] for vertex, value in sorted(result.items()) if value]


SCHEMA = {
    'simplex_faces': ['simplex'],
    'simplex_orientation': ['simplex'],
    'triangle_boundary': ['simplex', 'coefficient'],
    'boundary_squared': ['simplex', 'coefficient'],
    'graph_components': ['vertices', 'edges'],
    'graph_cycle_rank': ['vertices', 'edges'],
    'euler_characteristic': ['facets'],
    'betti_numbers': ['facets'],
    'chain_cycle': ['vertices', 'edges', 'coefficients'],
    'chain_boundary': ['facets', 'chain'],
}


def compute(operation, payload):
    if operation in ['simplex_faces', 'simplex_orientation', 'triangle_boundary', 'boundary_squared']:
        cell = simplex(payload['simplex'])
        if operation == 'simplex_faces':
            return [list(face) for size in range(1, len(cell) + 1)
                    for face in combinations(sorted(cell), size)]
        if operation == 'simplex_orientation':
            return {'sorted': sorted(cell), 'sign': orientation(cell)}
        coefficient = integer(payload['coefficient'])
        require(len(cell) == (3 if operation == 'triangle_boundary' else 4), 'E_DIMENSION')
        result = boundary({cell: coefficient})
        if operation == 'boundary_squared':
            result = boundary(result)
        return chain_list(result)
    if operation in ['graph_components', 'graph_cycle_rank', 'chain_cycle']:
        vertices, edges = graph(payload)
        if operation == 'graph_components':
            return components(vertices, edges)
        if operation == 'graph_cycle_rank':
            return len(edges) - len(vertices) + len(components(vertices, edges))
        coefficients = vector(payload['coefficients'], len(edges))
        result = graph_boundary(vertices, edges, coefficients)
        return {'is_cycle': not result, 'boundary': result}
    cells = complex_cells(payload['facets'])
    if operation == 'euler_characteristic':
        return sum((-1) ** i * len(row) for i, row in enumerate(cells))
    if operation == 'betti_numbers':
        return [len(row) - rank(boundary_matrix(cells, i)) - rank(boundary_matrix(cells, i + 1))
                for i, row in enumerate(cells)]
    require(operation == 'chain_boundary', 'E_OPERATION')
    require(len(cells) >= 2, 'E_DIMENSION')
    rows = {cell: i for i, cell in enumerate(cells[1])}
    value = [0] * len(rows)
    terms = payload['chain']
    require(type(terms) is list and len(terms) <= 64, 'E_CHAIN')
    seen = set()
    for term in terms:
        require(type(term) is list and len(term) == 2, 'E_CHAIN')
        edge, coefficient = simplex(term[0]), integer(term[1])
        key = tuple(sorted(edge))
        require(len(edge) == 2 and key in rows and key not in seen, 'E_CHAIN')
        seen.add(key)
        value[rows[key]] = coefficient * orientation(edge)
    matrix = boundary_matrix(cells, 2) if len(cells) >= 3 else [[] for _ in rows]
    return rank(matrix) == rank([row + [value[i]] for i, row in enumerate(matrix)])


def evaluate(request):
    try:
        require(type(request) is dict and set(request) == {'op', 'payload', 'synthetic'}, 'E_FIELDS')
        require(request['synthetic'] is True, 'E_SYNTHETIC')
        operation = request['op']
        require(type(operation) is str and operation in SCHEMA, 'E_OPERATION')
        fields(request['payload'], SCHEMA[operation])
        return {'ok': True, 'value': compute(operation, request['payload']), 'error': None}
    except ContractError as error:
        return {'ok': False, 'value': None, 'error': str(error)}
