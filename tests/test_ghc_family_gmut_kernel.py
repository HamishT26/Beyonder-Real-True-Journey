from __future__ import annotations

import math
import unittest

from scripts.ghc_family_gmut_kernel import (
    BackgroundState,
    ConstantPotential,
    QuadraticPotential,
    assess_effective_stability,
    continuity_residual,
    convergence_report,
    equation_of_state,
    exchange_residual,
    friedmann_residual,
    omega_component,
    scalar_energy_density,
    scalar_pressure,
    simulate_flat_flrw,
    validate_coefficient_ledger,
    validate_term_registry,
)


class ScalarIdentityTests(unittest.TestCase):
    def test_frozen_positive_potential_has_w_minus_one(self) -> None:
        rho = scalar_energy_density(0.0, 2.5)
        pressure = scalar_pressure(0.0, 2.5)
        self.assertEqual(rho, 2.5)
        self.assertEqual(pressure, -2.5)
        self.assertEqual(equation_of_state(rho, pressure), -1.0)

    def test_kinetic_dominated_scalar_has_w_plus_one(self) -> None:
        rho = scalar_energy_density(2.0, 0.0)
        pressure = scalar_pressure(2.0, 0.0)
        self.assertEqual(equation_of_state(rho, pressure), 1.0)

    def test_zero_density_equation_of_state_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            equation_of_state(0.0, 0.0)

    def test_wrong_sign_kinetic_normalization_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            scalar_energy_density(1.0, 0.0, z=-1.0)

    def test_null_extension_has_zero_omega(self) -> None:
        self.assertEqual(omega_component(0.0, planck_mass=3.0), 0.0)


class ConservationTests(unittest.TestCase):
    def test_equal_and_opposite_exchange_cancels(self) -> None:
        self.assertEqual(exchange_residual(0.75, -0.75), 0.0)

    def test_flat_friedmann_identity(self) -> None:
        rho_matter = 0.8
        rho_extension = 0.4
        hubble = math.sqrt((rho_matter + rho_extension) / 3.0)
        self.assertAlmostEqual(
            friedmann_residual(hubble, rho_matter, rho_extension), 0.0, places=14
        )

    def test_continuity_residual(self) -> None:
        hubble = 0.2
        rho = 1.5
        pressure = 0.1
        rho_dot = -3.0 * hubble * (rho + pressure)
        self.assertAlmostEqual(continuity_residual(rho_dot, hubble, rho, pressure), 0.0)


class ToySimulationTests(unittest.TestCase):
    def test_simulation_is_finite_and_deterministic(self) -> None:
        initial = BackgroundState(time=0.0, phi=0.2, phi_dot=0.0, rho_matter=1.0)
        potential = QuadraticPotential(mass=0.1, offset=0.2)
        first = simulate_flat_flrw(initial, potential, dt=0.01, steps=12)
        second = simulate_flat_flrw(initial, potential, dt=0.01, steps=12)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 13)
        self.assertLess(first[-1].rho_matter, first[0].rho_matter)
        self.assertTrue(all(math.isfinite(sample.hubble) for sample in first))
        self.assertLess(max(abs(sample.friedmann_residual) for sample in first), 1e-12)

    def test_constant_potential_frozen_without_matter_is_fixed(self) -> None:
        samples = simulate_flat_flrw(
            BackgroundState(time=0.0, phi=1.0, phi_dot=0.0, rho_matter=0.0),
            ConstantPotential(0.5),
            dt=0.1,
            steps=4,
        )
        self.assertTrue(all(sample.phi == 1.0 for sample in samples))
        self.assertTrue(all(sample.phi_dot == 0.0 for sample in samples))
        self.assertTrue(all(sample.w_phi == -1.0 for sample in samples))

    def test_rk4_self_convergence_is_reported(self) -> None:
        report = convergence_report(
            BackgroundState(time=0.0, phi=0.3, phi_dot=0.0, rho_matter=0.8),
            QuadraticPotential(mass=0.2, offset=0.1),
            horizon=0.5,
            coarse_steps=10,
        )
        self.assertTrue(report["convergent"])
        self.assertGreater(report["observed_order"], 2.5)

    def test_minimal_stability_gate_rejects_bad_regime(self) -> None:
        valid = assess_effective_stability(
            kinetic_normalization=1.0,
            sound_speed_squared=1.0,
            energy_to_cutoff_ratio=0.2,
        )
        invalid = assess_effective_stability(
            kinetic_normalization=-1.0,
            sound_speed_squared=-0.1,
            energy_to_cutoff_ratio=1.2,
        )
        self.assertTrue(valid.valid)
        self.assertFalse(invalid.valid)
        self.assertIn("outside_declared_eft_regime", invalid.issues)


class EpistemicGateTests(unittest.TestCase):
    def test_complete_physical_term_passes(self) -> None:
        result = validate_term_registry(
            [
                {
                    "name": "canonical_scalar_stress",
                    "claim_type": "physical",
                    "enters_spacetime_equation": True,
                    "physical_projection": "variation of scalar action with respect to metric",
                    "tensor_rank": "rank-2 symmetric covariant",
                    "units": "energy density",
                    "source_action": "S_phi",
                    "null_limit": "phi constant and potential absorbed into Lambda",
                    "observable": "expansion and fifth-force signatures",
                    "falsifier": "excluded parameter region or failed stability",
                }
            ]
        )
        self.assertTrue(result.valid)
        self.assertEqual(result.issues, ())

    def test_incomplete_physical_term_fails(self) -> None:
        result = validate_term_registry(
            [{"name": "mystery_tensor", "claim_type": "physical"}]
        )
        self.assertFalse(result.valid)
        self.assertIn("incomplete_physical_term", {issue.code for issue in result.issues})

    def test_normative_term_cannot_enter_spacetime_equation_directly(self) -> None:
        result = validate_term_registry(
            [
                {
                    "name": "dignity",
                    "claim_type": "normative",
                    "enters_spacetime_equation": True,
                    "physical_projection": "none",
                }
            ]
        )
        self.assertFalse(result.valid)
        self.assertIn("category_collapse", {issue.code for issue in result.issues})

    def test_complete_coefficient_row_passes(self) -> None:
        result = validate_coefficient_ledger(
            [
                {
                    "name": "beta",
                    "domain": "conformal matter coupling",
                    "units": "dimensionless",
                    "prior_or_range": "preregistered finite interval",
                    "null_condition": "beta=0",
                    "observable": "equivalence-principle violation",
                    "rejection_rule": "exclude values outside the likelihood bound",
                }
            ]
        )
        self.assertTrue(result.valid)

    def test_incomplete_coefficient_row_fails(self) -> None:
        result = validate_coefficient_ledger([{"name": "alpha"}])
        self.assertFalse(result.valid)
        self.assertEqual(result.issues[0].code, "incomplete_coefficient")


if __name__ == "__main__":
    unittest.main()
