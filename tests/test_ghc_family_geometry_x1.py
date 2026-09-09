"""Independent invariants, distinct from the 100 frozen example lookups."""
import copy
from itertools import combinations, permutations
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ghc_family_geometry_x1 as g
from ghc_family_geometry_cli import parse_json


class GeometryX1Tests(unittest.TestCase):
    def test_every_tetrahedron_orientation_cancels(self):
        for cell in permutations([1, 4, 8, 12]):
            self.assertEqual(g.boundary(g.boundary({cell: 7})), {})

    def test_orientation_changes_under_adjacent_exchange(self):
        for cell in permutations([1, 2, 3, 4]):
            changed = list(cell)
            changed[1], changed[2] = changed[2], changed[1]
            self.assertEqual(g.orientation(changed), -g.orientation(cell))

    def test_triangle_orientation_reversal_negates_chain(self):
        a = g.boundary({(2, 5, 9): 3})
        b = g.boundary({(5, 2, 9): 3})
        self.assertEqual(a, {key: -value for key, value in b.items()})

    def test_full_tetrahedron_has_exact_face_counts(self):
        cells = g.complex_cells([[0, 1, 2, 3]])
        self.assertEqual(list(map(len, cells)), [4, 6, 4, 1])

    def test_tetrahedral_surface_betti_and_euler(self):
        facets = [list(x) for x in combinations(range(4), 3)]
        self.assertEqual(g.compute('betti_numbers', {'facets': facets}), [1, 0, 1])
        self.assertEqual(g.compute('euler_characteristic', {'facets': facets}), 2)

    def test_full_tetrahedron_is_contractible(self):
        self.assertEqual(g.compute('betti_numbers', {'facets': [[0, 1, 2, 3]]}), [1, 0, 0, 0])

    def test_unfilled_loop_does_not_bound(self):
        payload = {'facets': [[0, 1], [0, 2], [1, 2]],
                   'chain': [[[0, 1], 1], [[0, 2], -1], [[1, 2], 1]]}
        self.assertFalse(g.compute('chain_boundary', payload))
        payload['facets'] = [[0, 1, 2]]
        self.assertTrue(g.compute('chain_boundary', payload))

    def test_zero_chain_is_boundary_without_faces(self):
        self.assertTrue(g.compute('chain_boundary', {'facets': [[0, 1]], 'chain': []}))

    def test_rank_exact_rational_dependence(self):
        self.assertEqual(g.rank([[2, 3], [4, 6], [6, 9]]), 1)
        self.assertEqual(g.rank([[2, 3], [4, 7]]), 2)

    def test_isolated_vertices_are_preserved(self):
        self.assertEqual(g.components([9, 3, 5], [[9, 3]]), [[3, 9], [5]])

    def test_cycle_rank_matches_union_find_oracle(self):
        rng = random.Random(6895)
        for _ in range(40):
            vertices = list(range(8))
            edges = [list(x) for x in combinations(vertices, 2) if rng.randrange(4) == 0]
            parent = list(vertices)
            def root(v):
                while parent[v] != v:
                    v = parent[v]
                return v
            loops = 0
            for a, b in edges:
                ra, rb = root(a), root(b)
                if ra == rb:
                    loops += 1
                else:
                    parent[rb] = ra
            self.assertEqual(g.compute('graph_cycle_rank', {'vertices': vertices, 'edges': edges}), loops)

    def test_boolean_vertex_is_rejected(self):
        result = g.evaluate({'op': 'simplex_faces', 'payload': {'simplex': [0, True]}, 'synthetic': True})
        self.assertEqual(result['error'], 'E_INTEGER')

    def test_capacity_is_checked_before_matrix_work(self):
        with self.assertRaisesRegex(g.ContractError, 'E_CAPACITY'):
            g.complex_cells([[i] for i in range(33)])

    def test_duplicate_undirected_edge_is_rejected(self):
        with self.assertRaisesRegex(g.ContractError, 'E_DUPLICATE_EDGE'):
            g.graph({'vertices': [0, 1], 'edges': [[0, 1], [1, 0]]})

    def test_request_is_unchanged(self):
        request = {'op': 'chain_cycle', 'payload': {'vertices': [0, 1], 'edges': [[0, 1]], 'coefficients': [3]}, 'synthetic': True}
        before = copy.deepcopy(request)
        g.evaluate(request)
        self.assertEqual(request, before)

    def test_duplicate_json_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'E_DUPLICATE_JSON_KEY'):
            parse_json('{"x":1,"x":2}')

    def test_nonfinite_json_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'E_NONFINITE'):
            parse_json('{"x":NaN}')

    def test_incomplete_payload_is_rejected(self):
        result = g.evaluate({'op': 'triangle_boundary', 'payload': {'simplex': [0, 1, 2]}, 'synthetic': True})
        self.assertEqual(result['error'], 'E_PAYLOAD_FIELDS')


if __name__ == '__main__':
    unittest.main()
