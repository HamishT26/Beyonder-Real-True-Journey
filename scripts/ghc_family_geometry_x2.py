"""Exact cochain calculations and finite evidence reservations.

Uses frozen x1 algebra helpers without changing that module. Integer-valued JSON
results are exact in Python; consumers must preserve large integer tokens.
"""
from fractions import Fraction
import hashlib
import json
import re

from ghc_family_geometry_x1 import (
    ContractError, boundary, components, fields, graph, integer, rank,
    require, simplex, vector,
)


def gradient(vertices, edges, potential):
    index = {vertex: i for i, vertex in enumerate(vertices)}
    return [potential[index[b]] - potential[index[a]] for a, b in edges]


def laplacian(vertices, edges, weights):
    index = {vertex: i for i, vertex in enumerate(vertices)}
    matrix = [[0] * len(vertices) for _ in vertices]
    for (a, b), weight in zip(edges, weights):
        i, j = index[a], index[b]
        matrix[i][i] += weight
        matrix[j][j] += weight
        matrix[i][j] -= weight
        matrix[j][i] -= weight
    return matrix


def multiply(matrix, values):
    return [sum(a * b for a, b in zip(row, values)) for row in matrix]


def solve_exact(matrix, right):
    if not matrix:
        return []
    count = len(matrix)
    require(count <= 32 and all(len(row) == count for row in matrix), 'E_MATRIX')
    require(len(right) == count, 'E_VECTOR')
    work = [[Fraction(value) for value in row] + [Fraction(right[i])]
            for i, row in enumerate(matrix)]
    for column in range(count):
        pivot = next((i for i in range(column, count) if work[i][column]), None)
        require(pivot is not None, 'E_SINGULAR')
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [value / divisor for value in work[column]]
        for i in range(count):
            if i != column:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[column])]
    return [row[-1] for row in work]


def dirichlet(vertices, edges, weights, constraints):
    require(type(constraints) is list and 1 <= len(constraints) <= len(vertices), 'E_BOUNDARY')
    fixed = {}
    for row in constraints:
        require(type(row) is list and len(row) == 2, 'E_BOUNDARY')
        vertex, value = integer(row[0]), integer(row[1])
        require(vertex in vertices and vertex not in fixed, 'E_BOUNDARY')
        fixed[vertex] = Fraction(value)
    require(all(any(v in fixed for v in group) for group in components(vertices, edges)), 'E_UNCONSTRAINED_COMPONENT')
    matrix = laplacian(vertices, edges, weights)
    index = {vertex: i for i, vertex in enumerate(vertices)}
    free = [vertex for vertex in vertices if vertex not in fixed]
    reduced = [[matrix[index[a]][index[b]] for b in free] for a in free]
    right = [-sum(matrix[index[a]][index[b]] * value for b, value in fixed.items()) for a in free]
    solution = fixed | dict(zip(free, solve_exact(reduced, right)))
    return [str(solution[vertex]) for vertex in vertices]


SCHEMA = {
    'coboundary_gradient': ['vertices', 'edges', 'potential'],
    'discrete_stokes': ['simplex', 'cochain'],
    'adjoint_pairing': ['vertices', 'edges', 'potential', 'edge_values'],
    'weighted_laplacian': ['vertices', 'edges', 'potential', 'weights'],
    'dirichlet_solution': ['vertices', 'edges', 'weights', 'boundary'],
    'energy_identity': ['vertices', 'edges', 'potential', 'weights'],
    'gauge_invariance': ['vertices', 'edges', 'potential', 'shift'],
    'harmonic_dimension': ['vertices', 'edges', 'weights'],
    'provenance_binding': ['record', 'declared_digest'],
    'authority_reservation': ['requested_scope', 'evidence_class', 'execute'],
}
REPRESENTABLE = {'software_example', 'record_digest', 'mathematical_identity', 'local_test', 'documentation'}
RESERVED = {'physical_law', 'credential_issuance', 'public_policy', 'maori_authority', 'stage20'}


def compute(operation, payload):
    if operation == 'provenance_binding':
        record = payload['record']
        require(type(record) is dict, 'E_RECORD')
        declared = payload['declared_digest']
        require(type(declared) is str and re.fullmatch('[0-9a-f]{64}', declared) is not None, 'E_DIGEST')
        try:
            encoded = json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')
        except (TypeError, ValueError, RecursionError) as error:
            raise ContractError('E_RECORD') from error
        require(len(encoded) <= 20_000, 'E_CAPACITY')
        observed = hashlib.sha256(encoded).hexdigest()
        return {'observed_digest': observed, 'matches': observed == declared, 'authority_transferred': False}
    if operation == 'authority_reservation':
        requested = payload['requested_scope']
        require(type(requested) is str and requested in REPRESENTABLE | RESERVED, 'E_SCOPE')
        require(payload['evidence_class'] == 'synthetic' and type(payload['evidence_class']) is str, 'E_EVIDENCE_CLASS')
        require(payload['execute'] is False, 'E_EXECUTION_RESERVED')
        return {'scope': requested, 'executed': False, 'disposition': 'represented' if requested in REPRESENTABLE else 'exact_gate'}
    if operation == 'discrete_stokes':
        cell = simplex(payload['simplex'])
        require(len(cell) == 3, 'E_DIMENSION')
        cochain = vector(payload['cochain'], 3)
        chain = boundary({cell: 1})
        basis = sorted(chain)
        pairing = sum(chain[edge] * value for edge, value in zip(basis, cochain))
        # The dual coefficient is independently assembled from the signed basis column.
        column = [chain[edge] for edge in basis]
        coboundary = sum(cochain[i] * column[i] for i in range(3))
        return {'boundary_pairing': pairing, 'coboundary_pairing': coboundary}
    vertices, edges = graph(payload)
    if operation in ['weighted_laplacian', 'dirichlet_solution', 'energy_identity', 'harmonic_dimension']:
        weights = vector(payload['weights'], len(edges), positive=True)
        matrix = laplacian(vertices, edges, weights)
        if operation == 'dirichlet_solution':
            return dirichlet(vertices, edges, weights, payload['boundary'])
        if operation == 'harmonic_dimension':
            return len(vertices) - rank(matrix)
    potential = vector(payload['potential'], len(vertices))
    differences = gradient(vertices, edges, potential)
    if operation == 'coboundary_gradient':
        return differences
    if operation == 'adjoint_pairing':
        edge_values = vector(payload['edge_values'], len(edges))
        index = {vertex: i for i, vertex in enumerate(vertices)}
        adjoint = [0] * len(vertices)
        for (a, b), value in zip(edges, edge_values):
            adjoint[index[a]] -= value
            adjoint[index[b]] += value
        return {'gradient_pairing': sum(a * b for a, b in zip(differences, edge_values)),
                'adjoint_pairing': sum(a * b for a, b in zip(potential, adjoint))}
    if operation == 'weighted_laplacian':
        return multiply(matrix, potential)
    if operation == 'energy_identity':
        edge_energy = sum(weight * value * value for weight, value in zip(weights, differences))
        quadratic = sum(a * b for a, b in zip(potential, multiply(matrix, potential)))
        return {'edge_energy': edge_energy, 'quadratic_energy': quadratic}
    require(operation == 'gauge_invariance', 'E_OPERATION')
    shift = integer(payload['shift'])
    shifted = gradient(vertices, edges, [value + shift for value in potential])
    return {'difference': [a - b for a, b in zip(shifted, differences)], 'gradient': differences}


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
