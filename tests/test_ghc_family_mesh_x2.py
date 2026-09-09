"""Independent x2 invariants, separate from the 100 frozen cases."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ghc_family_mesh_x2 as mesh


class MeshX2Tests(unittest.TestCase):
    def test_poisson_manufactured_solution(self):
        self.assertEqual(mesh.compute("poisson_dirichlet_1d", {"intervals": 4, "forcing": 2, "left": 0, "right": 0}), ["0", "3", "4", "3", "0"])

    def test_poisson_linear_boundary_solution(self):
        self.assertEqual(mesh.compute("poisson_dirichlet_1d", {"intervals": 2, "forcing": 0, "left": 0, "right": 2}), ["0", "1", "2"])

    def test_poisson_residual_zero(self):
        self.assertEqual(mesh.compute("poisson_residual", {"values": [0, 3, 4, 3, 0], "forcing": 2}), ["0", "0", "0"])

    def test_poisson_residual_detects_difference(self):
        self.assertEqual(mesh.compute("poisson_residual", {"values": [0, 3, 5, 3, 0], "forcing": 2}), ["-1", "2", "-1"])

    def test_flux_balance_telescopes(self):
        self.assertEqual(mesh.compute("flux_balance", {"values": [0, 1, 4, 9], "h": 1}), {"interior_divergence_sum": "4", "boundary_flux_difference": "4"})

    def test_flux_requires_positive_spacing(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_SPACING"):
            mesh.compute("flux_balance", {"values": [0, 1, 4], "h": 0})

    def test_richardson_exact_elimination(self):
        self.assertEqual(mesh.compute("richardson_extrapolate", {"coarse": "5/4", "fine": "17/16", "order": 2, "refinement_ratio": 2}), "1")

    def test_richardson_refuses_unit_ratio(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_REFINEMENT_RATIO"):
            mesh.compute("richardson_extrapolate", {"coarse": 2, "fine": 1, "order": 2, "refinement_ratio": 1})

    def test_adaptive_split_strict_threshold(self):
        result = mesh.compute("adaptive_split", {"intervals": [[0, 1], [1, 2]], "errors": ["1/2", "1/4"], "threshold": "1/4"})
        self.assertEqual(result, [["0", "1/2"], ["1/2", "1"], ["1", "2"]])

    def test_adaptive_split_refuses_overlap(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_INTERVALS"):
            mesh.compute("adaptive_split", {"intervals": [[0, 2], [1, 3]], "errors": [1, 1], "threshold": 0})

    def test_cfl_selected_bound(self):
        self.assertTrue(mesh.compute("cfl_number", {"speed": 2, "dt": "1/4", "dx": 1})["stable_under_selected_bound"])
        self.assertFalse(mesh.compute("cfl_number", {"speed": 2, "dt": 1, "dx": 1})["stable_under_selected_bound"])

    def test_cfl_refuses_zero_spacing(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_CFL_DOMAIN"):
            mesh.compute("cfl_number", {"speed": 1, "dt": 1, "dx": 0})

    def test_heat_step_preserves_fixed_boundaries(self):
        self.assertEqual(mesh.compute("heat_step", {"values": [0, 2, 0], "alpha": "1/2", "fixed_boundary": True}), ["0", "0", "0"])

    def test_heat_step_refuses_unstable_profile(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_ALPHA"):
            mesh.compute("heat_step", {"values": [0, 2, 0], "alpha": "3/4", "fixed_boundary": True})

    def test_discrete_energy_nonnegative_and_shift_invariant(self):
        first = mesh.compute("discrete_energy", {"values": [0, 1, 4]})
        shifted = mesh.compute("discrete_energy", {"values": [7, 8, 11]})
        self.assertEqual(first, shifted)
        self.assertEqual(first, "5")

    def test_provenance_digest_is_key_order_stable(self):
        self.assertEqual(mesh.canonical_digest({"a": 1, "b": 2}), mesh.canonical_digest({"b": 2, "a": 1}))

    def test_provenance_match_and_mismatch(self):
        record = {"kind": "synthetic", "value": 1}
        digest = mesh.canonical_digest(record)
        self.assertTrue(mesh.compute("provenance_binding", {"record": record, "declared_digest": digest})["matches"])
        self.assertFalse(mesh.compute("provenance_binding", {"record": record, "declared_digest": "0" * 64})["matches"])

    def test_claim_reservation_preserves_gate(self):
        result = mesh.compute("claim_reservation", {"requested_scope": "maori_authority", "evidence_class": "synthetic", "execute": False})
        self.assertEqual(result["disposition"], "exact_gate")

    def test_claim_execution_is_refused(self):
        with self.assertRaisesRegex(mesh.ContractError, "E_EXECUTION_RESERVED"):
            mesh.compute("claim_reservation", {"requested_scope": "software_example", "evidence_class": "synthetic", "execute": True})

    def test_request_remains_unchanged(self):
        request = {"op": "cfl_number", "payload": {"speed": 1, "dt": 1, "dx": 2}, "synthetic": True}
        before = copy.deepcopy(request)
        mesh.evaluate(request)
        self.assertEqual(request, before)

    def test_x1_operation_is_outside_x2_surface(self):
        result = mesh.evaluate({"op": "uniform_grid", "payload": {"start": 0, "stop": 1, "intervals": 2}, "synthetic": True})
        self.assertEqual(result["error"], "E_OPERATION")


if __name__ == "__main__":
    unittest.main()
