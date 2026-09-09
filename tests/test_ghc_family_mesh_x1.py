"""Independent x1 invariants, separate from the 100 frozen cases."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ghc_family_mesh_x1 as mesh
from ghc_family_mesh_cli import parse_json


class MeshX1Tests(unittest.TestCase):
    def test_uniform_grid_endpoints_and_width(self):
        result = mesh.compute("uniform_grid", {"start": "-1/2", "stop": "3/2", "intervals": 4})
        self.assertEqual(result, ["-1/2", "0", "1/2", "1", "3/2"])

    def test_uniform_grid_refuses_reversed_interval(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_INTERVAL"):
            mesh.compute("uniform_grid", {"start": 2, "stop": 1, "intervals": 2})

    def test_cell_widths_preserve_nonuniformity(self):
        self.assertEqual(mesh.compute("cell_widths", {"nodes": [0, 1, 3, 6]}), [1, 2, 3])

    def test_cell_widths_refuse_duplicate_node(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_MONOTONE"):
            mesh.compute("cell_widths", {"nodes": [0, 1, 1]})

    def test_linear_interpolation_is_affine(self):
        self.assertEqual(mesh.compute("linear_interpolate", {"x0": 0, "x1": 4, "y0": 2, "y1": 10, "x": 1}), "4")

    def test_linear_interpolation_refuses_extrapolation(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_INTERPOLATION_DOMAIN"):
            mesh.compute("linear_interpolate", {"x0": 0, "x1": 1, "y0": 0, "y1": 1, "x": 2})

    def test_forward_and_backward_have_expected_alignment(self):
        payload = {"values": [0, 1, 4, 9], "h": 1}
        self.assertEqual(mesh.compute("forward_difference", payload), ["1", "3", "5"])
        self.assertEqual(mesh.compute("backward_difference", payload), ["1", "3", "5"])

    def test_central_difference_is_exact_for_quadratic(self):
        self.assertEqual(mesh.compute("central_difference", {"values": [0, 1, 4, 9, 16], "h": 1}), ["2", "4", "6"])

    def test_second_difference_is_exact_for_quadratic(self):
        self.assertEqual(mesh.compute("second_difference", {"values": [0, 1, 4, 9, 16], "h": 1}), ["2", "2", "2"])

    def test_spacing_must_be_positive(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_SPACING"):
            mesh.compute("forward_difference", {"values": [0, 1], "h": 0})

    def test_trapezoid_is_exact_for_linear_data(self):
        self.assertEqual(mesh.compute("trapezoid_integral", {"values": [0, 2, 4, 6], "h": "1/2"}), "9/2")

    def test_l1_error_requires_equal_lengths(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_VECTOR_LENGTH"):
            mesh.compute("l1_grid_error", {"approx": [0, 1], "exact": [0, 1, 2]})

    def test_l1_error_exact_rational(self):
        self.assertEqual(mesh.compute("l1_grid_error", {"approx": [0, 2, 2], "exact": [0, 1, 4]}), "1")

    def test_observed_order_exact(self):
        self.assertEqual(mesh.compute("observed_order", {"errors": [16, 4, 1], "refinement_ratio": 2})["orders"], ["2", "2"])

    def test_observed_order_refuses_nonexact_power(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_ORDER_EXACT"):
            mesh.compute("observed_order", {"errors": [10, 3, 1], "refinement_ratio": 2})

    def test_request_remains_unchanged(self):
        request = {"op": "uniform_grid", "payload": {"start": 0, "stop": 1, "intervals": 4}, "synthetic": True}
        before = copy.deepcopy(request)
        mesh.evaluate(request)
        self.assertEqual(request, before)

    def test_boolean_is_not_an_integer_scalar(self):
        result = mesh.evaluate({"op": "uniform_grid", "payload": {"start": True, "stop": 1, "intervals": 4}, "synthetic": True})
        self.assertEqual(result["error"], "E_SCALAR")

    def test_duplicate_json_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "E_DUPLICATE_JSON_KEY"):
            parse_json('{"x": 1, "x": 2}')

    def test_nonfinite_json_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "E_NONFINITE"):
            parse_json('{"x": NaN}')

    def test_unexpected_payload_field_is_rejected(self):
        result = mesh.evaluate({"op": "cell_widths", "payload": {"nodes": [0, 1], "extra": 1}, "synthetic": True})
        self.assertEqual(result["error"], "E_PAYLOAD_FIELDS")


if __name__ == "__main__":
    unittest.main()
