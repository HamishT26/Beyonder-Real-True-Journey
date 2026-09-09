"""Cochain invariants and singularity/authority counterexamples."""
import copy
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ghc_family_geometry_x2 as g


class GeometryX2Tests(unittest.TestCase):
    def test_edge_reversal_negates_gradient(self):
        self.assertEqual(g.gradient([0, 1], [[0, 1]], [3, 8]), [5])
        self.assertEqual(g.gradient([0, 1], [[1, 0]], [3, 8]), [-5])

    def test_constant_shift_cancels(self):
        edges = [[0, 1], [2, 1]]
        self.assertEqual(g.gradient([0, 1, 2], edges, [1, 8, 4]), g.gradient([0, 1, 2], edges, [19, 26, 22]))

    def test_stokes_all_triangle_orientations(self):
        for cell in permutations([0, 1, 2]):
            result = g.compute('discrete_stokes', {'simplex': list(cell), 'cochain': [2, 5, 11]})
            self.assertEqual(result['boundary_pairing'], result['coboundary_pairing'])
            self.assertEqual(abs(result['boundary_pairing']), 8)

    def test_laplacian_is_symmetric_and_has_zero_rowsums(self):
        matrix = g.laplacian([0, 1, 2], [[0, 2], [1, 2]], [2, 5])
        self.assertEqual(matrix, [list(row) for row in zip(*matrix)])
        self.assertEqual(list(map(sum, matrix)), [0, 0, 0])

    def test_negative_weight_refused(self):
        request = {'op': 'harmonic_dimension', 'payload': {'vertices': [0, 1], 'edges': [[0, 1]], 'weights': [-1]}, 'synthetic': True}
        self.assertEqual(g.evaluate(request)['error'], 'E_WEIGHT')

    def test_boolean_weight_refused(self):
        request = {'op': 'harmonic_dimension', 'payload': {'vertices': [0, 1], 'edges': [[0, 1]], 'weights': [True]}, 'synthetic': True}
        self.assertEqual(g.evaluate(request)['error'], 'E_INTEGER')

    def test_unconstrained_component_refused(self):
        with self.assertRaisesRegex(g.ContractError, 'E_UNCONSTRAINED_COMPONENT'):
            g.dirichlet([0, 1, 2], [[0, 1]], [1], [[0, 0]])

    def test_duplicate_boundary_refused(self):
        with self.assertRaisesRegex(g.ContractError, 'E_BOUNDARY'):
            g.dirichlet([0, 1], [[0, 1]], [1], [[0, 0], [0, 1]])

    def test_external_boundary_vertex_refused(self):
        with self.assertRaisesRegex(g.ContractError, 'E_BOUNDARY'):
            g.dirichlet([0, 1], [[0, 1]], [1], [[2, 0]])

    def test_unequal_weight_solution_is_exact_fraction(self):
        self.assertEqual(g.dirichlet([0, 1, 2], [[0, 1], [1, 2]], [1, 3], [[0, 0], [2, 1]]), ['0', '3/4', '1'])

    def test_positive_energy_on_random_small_inputs(self):
        rng = random.Random(68952)
        for _ in range(40):
            p = {'vertices': list(range(7)), 'edges': [[i, i + 1] for i in range(6)],
                 'weights': [rng.randrange(1, 8) for _ in range(6)], 'potential': [rng.randrange(-20, 21) for _ in range(7)]}
            result = g.compute('energy_identity', p)
            self.assertGreaterEqual(result['edge_energy'], 0)
            self.assertEqual(result['edge_energy'], result['quadratic_energy'])

    def test_adjoint_pairing_with_nonstandard_vertex_order(self):
        p = {'vertices': [9, 2, 5], 'edges': [[2, 9], [5, 2]], 'potential': [1, 4, 7], 'edge_values': [2, 3]}
        result = g.compute('adjoint_pairing', p)
        self.assertEqual(result, {'gradient_pairing': -15, 'adjoint_pairing': -15})

    def test_connected_kernel_dimension(self):
        self.assertEqual(g.compute('harmonic_dimension', {'vertices': [0, 1, 2], 'edges': [[0, 1], [1, 2]], 'weights': [2, 7]}), 1)

    def test_disconnected_kernel_dimension(self):
        self.assertEqual(g.compute('harmonic_dimension', {'vertices': [0, 1, 2], 'edges': [[0, 1]], 'weights': [2]}), 2)

    def test_digest_match_does_not_transfer_authority(self):
        record = {'value': 7}
        digest = g.hashlib.sha256(g.json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        result = g.compute('provenance_binding', {'record': record, 'declared_digest': digest})
        self.assertTrue(result['matches'])
        self.assertFalse(result['authority_transferred'])

    def test_authority_execution_refused(self):
        request = {'op': 'authority_reservation', 'payload': {'requested_scope': 'stage20', 'evidence_class': 'synthetic', 'execute': True}, 'synthetic': True}
        self.assertEqual(g.evaluate(request)['error'], 'E_EXECUTION_RESERVED')

    def test_extra_payload_refused(self):
        request = {'op': 'discrete_stokes', 'payload': {'simplex': [0, 1, 2], 'cochain': [1, 2, 3], 'extra': 0}, 'synthetic': True}
        self.assertEqual(g.evaluate(request)['error'], 'E_PAYLOAD_FIELDS')

    def test_exact_solver_and_request_do_not_mutate_inputs(self):
        matrix, right = [[4, -1], [-1, 3]], [1, 2]
        before = copy.deepcopy((matrix, right))
        self.assertEqual(g.solve_exact(matrix, right), [Fraction(5, 11), Fraction(9, 11)])
        self.assertEqual((matrix, right), before)


if __name__ == '__main__':
    unittest.main()
