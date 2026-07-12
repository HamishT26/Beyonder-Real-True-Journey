#!/usr/bin/env python3
"""Deterministic validation scaffold for the GMUT physical seed.

This module implements elementary scalar-field identities, a dimensionless
homogeneous FLRW toy integrator, and claim/term registry gates.  It is not a
cosmological likelihood engine and does not provide empirical validation.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol, Sequence


class Potential(Protocol):
    def value(self, phi: float) -> float: ...

    def gradient(self, phi: float) -> float: ...


@dataclass(frozen=True)
class ConstantPotential:
    value_0: float

    def value(self, phi: float) -> float:
        del phi
        return float(self.value_0)

    def gradient(self, phi: float) -> float:
        del phi
        return 0.0


@dataclass(frozen=True)
class QuadraticPotential:
    mass: float
    offset: float = 0.0

    def value(self, phi: float) -> float:
        return 0.5 * self.mass * self.mass * phi * phi + self.offset

    def gradient(self, phi: float) -> float:
        return self.mass * self.mass * phi


@dataclass(frozen=True)
class ExponentialPotential:
    amplitude: float
    slope: float
    planck_mass: float = 1.0

    def value(self, phi: float) -> float:
        return self.amplitude * math.exp(-self.slope * phi / self.planck_mass)

    def gradient(self, phi: float) -> float:
        return -(self.slope / self.planck_mass) * self.value(phi)


@dataclass(frozen=True)
class BackgroundState:
    time: float
    phi: float
    phi_dot: float
    rho_matter: float


@dataclass(frozen=True)
class BackgroundSample:
    time: float
    phi: float
    phi_dot: float
    rho_matter: float
    rho_phi: float
    pressure_phi: float
    w_phi: float | None
    hubble: float
    friedmann_residual: float


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    issues: tuple[ValidationIssue, ...]


@dataclass(frozen=True)
class StabilityAssessment:
    valid: bool
    kinetic_normalization: float
    sound_speed_squared: float
    energy_to_cutoff_ratio: float
    issues: tuple[str, ...]


def require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def scalar_energy_density(phi_dot: float, potential_value: float, z: float = 1.0) -> float:
    phi_dot = require_finite("phi_dot", phi_dot)
    potential_value = require_finite("potential_value", potential_value)
    z = require_finite("z", z)
    if z <= 0:
        raise ValueError("z must be positive to avoid a wrong-sign canonical kinetic term")
    return 0.5 * z * phi_dot * phi_dot + potential_value


def scalar_pressure(phi_dot: float, potential_value: float, z: float = 1.0) -> float:
    phi_dot = require_finite("phi_dot", phi_dot)
    potential_value = require_finite("potential_value", potential_value)
    z = require_finite("z", z)
    if z <= 0:
        raise ValueError("z must be positive to avoid a wrong-sign canonical kinetic term")
    return 0.5 * z * phi_dot * phi_dot - potential_value


def equation_of_state(energy_density: float, pressure: float, *, atol: float = 1e-15) -> float:
    energy_density = require_finite("energy_density", energy_density)
    pressure = require_finite("pressure", pressure)
    if abs(energy_density) <= atol:
        raise ValueError("equation of state is undefined when energy density is zero")
    return pressure / energy_density


def omega_component(extension_stress_component: float, planck_mass: float = 1.0) -> float:
    """Return Omega_component = T_extension_component / M_Pl^2."""
    extension_stress_component = require_finite(
        "extension_stress_component", extension_stress_component
    )
    planck_mass = require_finite("planck_mass", planck_mass)
    if planck_mass <= 0:
        raise ValueError("planck_mass must be positive")
    return extension_stress_component / (planck_mass * planck_mass)


def friedmann_residual(
    hubble: float,
    rho_matter: float,
    rho_extension: float,
    *,
    planck_mass: float = 1.0,
) -> float:
    """Residual of 3 M_Pl^2 H^2 = rho_matter + rho_extension."""
    hubble = require_finite("hubble", hubble)
    rho_matter = require_finite("rho_matter", rho_matter)
    rho_extension = require_finite("rho_extension", rho_extension)
    planck_mass = require_finite("planck_mass", planck_mass)
    if planck_mass <= 0:
        raise ValueError("planck_mass must be positive")
    return 3.0 * planck_mass * planck_mass * hubble * hubble - (
        rho_matter + rho_extension
    )


def exchange_residual(q_matter: float, q_extension: float) -> float:
    """Equal-and-opposite sector exchange must sum to zero."""
    return require_finite("q_matter", q_matter) + require_finite(
        "q_extension", q_extension
    )


def continuity_residual(
    rho_dot_total: float,
    hubble: float,
    rho_total: float,
    pressure_total: float,
) -> float:
    """Residual of homogeneous total conservation."""
    return require_finite("rho_dot_total", rho_dot_total) + 3.0 * require_finite(
        "hubble", hubble
    ) * (
        require_finite("rho_total", rho_total)
        + require_finite("pressure_total", pressure_total)
    )


def assess_effective_stability(
    *, kinetic_normalization: float, sound_speed_squared: float, energy_to_cutoff_ratio: float
) -> StabilityAssessment:
    """Apply minimal local EFT gates without claiming full perturbative stability."""
    kinetic_normalization = require_finite("kinetic_normalization", kinetic_normalization)
    sound_speed_squared = require_finite("sound_speed_squared", sound_speed_squared)
    energy_to_cutoff_ratio = require_finite("energy_to_cutoff_ratio", energy_to_cutoff_ratio)
    issues: list[str] = []
    if kinetic_normalization <= 0:
        issues.append("non_positive_kinetic_normalization")
    if sound_speed_squared <= 0:
        issues.append("non_positive_sound_speed_squared")
    if sound_speed_squared > 1:
        issues.append("superluminal_effective_sound_speed_requires_model_specific_review")
    if not 0 <= energy_to_cutoff_ratio < 1:
        issues.append("outside_declared_eft_regime")
    return StabilityAssessment(
        valid=not issues,
        kinetic_normalization=kinetic_normalization,
        sound_speed_squared=sound_speed_squared,
        energy_to_cutoff_ratio=energy_to_cutoff_ratio,
        issues=tuple(issues),
    )


def _derivative(
    state: tuple[float, float, float],
    potential: Potential,
    matter_w: float,
    planck_mass: float,
) -> tuple[float, float, float]:
    phi, phi_dot, rho_matter = state
    rho_phi = scalar_energy_density(phi_dot, potential.value(phi))
    rho_total = rho_matter + rho_phi
    if rho_total < 0:
        raise ValueError("total energy density became negative in the toy model")
    hubble = math.sqrt(rho_total / (3.0 * planck_mass * planck_mass))
    return (
        phi_dot,
        -3.0 * hubble * phi_dot - potential.gradient(phi),
        -3.0 * hubble * (1.0 + matter_w) * rho_matter,
    )


def _rk4_step(
    state: tuple[float, float, float],
    dt: float,
    potential: Potential,
    matter_w: float,
    planck_mass: float,
) -> tuple[float, float, float]:
    def add(base: Sequence[float], delta: Sequence[float], scale: float) -> tuple[float, ...]:
        return tuple(b + scale * d for b, d in zip(base, delta, strict=True))

    k1 = _derivative(state, potential, matter_w, planck_mass)
    k2 = _derivative(add(state, k1, 0.5 * dt), potential, matter_w, planck_mass)
    k3 = _derivative(add(state, k2, 0.5 * dt), potential, matter_w, planck_mass)
    k4 = _derivative(add(state, k3, dt), potential, matter_w, planck_mass)
    return tuple(
        state[i] + dt * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
        for i in range(3)
    )


def _sample(state: BackgroundState, potential: Potential, planck_mass: float) -> BackgroundSample:
    value = potential.value(state.phi)
    rho_phi = scalar_energy_density(state.phi_dot, value)
    pressure_phi = scalar_pressure(state.phi_dot, value)
    rho_total = state.rho_matter + rho_phi
    if rho_total < 0:
        raise ValueError("total energy density must be non-negative")
    hubble = math.sqrt(rho_total / (3.0 * planck_mass * planck_mass))
    try:
        w_phi: float | None = equation_of_state(rho_phi, pressure_phi)
    except ValueError:
        w_phi = None
    return BackgroundSample(
        time=state.time,
        phi=state.phi,
        phi_dot=state.phi_dot,
        rho_matter=state.rho_matter,
        rho_phi=rho_phi,
        pressure_phi=pressure_phi,
        w_phi=w_phi,
        hubble=hubble,
        friedmann_residual=friedmann_residual(
            hubble, state.rho_matter, rho_phi, planck_mass=planck_mass
        ),
    )


def simulate_flat_flrw(
    initial: BackgroundState,
    potential: Potential,
    *,
    dt: float,
    steps: int,
    matter_w: float = 0.0,
    planck_mass: float = 1.0,
) -> list[BackgroundSample]:
    """Integrate a canonical homogeneous scalar plus perfect-fluid matter.

    Units are dimensionless and M_Pl defaults to one.  This routine is for
    numerical sanity checks and teaching only; it performs no data fitting.
    """
    dt = require_finite("dt", dt)
    matter_w = require_finite("matter_w", matter_w)
    planck_mass = require_finite("planck_mass", planck_mass)
    if dt <= 0:
        raise ValueError("dt must be positive")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    if planck_mass <= 0:
        raise ValueError("planck_mass must be positive")
    if initial.rho_matter < 0:
        raise ValueError("initial matter density must be non-negative")

    current = initial
    result = [_sample(current, potential, planck_mass)]
    vector = (current.phi, current.phi_dot, current.rho_matter)
    for index in range(steps):
        vector = _rk4_step(vector, dt, potential, matter_w, planck_mass)
        # Tiny negative density from floating-point drift is projected to zero;
        # a material negative value remains a failure.
        if vector[2] < -1e-12:
            raise ValueError("matter density became materially negative")
        vector = (vector[0], vector[1], max(0.0, vector[2]))
        current = BackgroundState(
            time=initial.time + (index + 1) * dt,
            phi=vector[0],
            phi_dot=vector[1],
            rho_matter=vector[2],
        )
        result.append(_sample(current, potential, planck_mass))
    return result


def convergence_report(
    initial: BackgroundState,
    potential: Potential,
    *,
    horizon: float,
    coarse_steps: int,
    matter_w: float = 0.0,
    planck_mass: float = 1.0,
) -> dict[str, Any]:
    """Compare RK4 endpoint errors under two successive step halvings."""
    horizon = require_finite("horizon", horizon)
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if coarse_steps < 2:
        raise ValueError("coarse_steps must be at least two")

    endpoints = []
    for factor in (1, 2, 4):
        steps = coarse_steps * factor
        samples = simulate_flat_flrw(
            initial,
            potential,
            dt=horizon / steps,
            steps=steps,
            matter_w=matter_w,
            planck_mass=planck_mass,
        )
        last = samples[-1]
        endpoints.append((last.phi, last.phi_dot, last.rho_matter))

    def distance(left: Sequence[float], right: Sequence[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    coarse_error = distance(endpoints[0], endpoints[1])
    fine_error = distance(endpoints[1], endpoints[2])
    if fine_error == 0.0:
        observed_order: float | None = None
        convergent = coarse_error == 0.0
    else:
        observed_order = math.log2(coarse_error / fine_error) if coarse_error > 0 else None
        convergent = coarse_error > fine_error and observed_order is not None and observed_order > 2.5
    return {
        "schema": "ghc.family.gmut-rk4-convergence.v1",
        "horizon": horizon,
        "coarse_steps": coarse_steps,
        "coarse_to_medium_error": coarse_error,
        "medium_to_fine_error": fine_error,
        "observed_order": observed_order,
        "convergent": convergent,
        "boundary": "endpoint_self_convergence_not_accuracy_against_empirical_data",
    }


PHYSICAL_REQUIRED = {
    "tensor_rank",
    "units",
    "source_action",
    "null_limit",
    "observable",
    "falsifier",
}
VALID_CLAIM_TYPES = {"physical", "informational", "normative", "spiritual", "metaphorical"}


def validate_term_registry(terms: Iterable[dict[str, Any]]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for index, term in enumerate(terms):
        path = f"terms[{index}]"
        name = str(term.get("name", "")).strip()
        if not name:
            issues.append(ValidationIssue(path, "missing_name", "term requires a non-empty name"))
        elif name in seen:
            issues.append(ValidationIssue(path, "duplicate_name", f"duplicate term name: {name}"))
        else:
            seen.add(name)

        claim_type = term.get("claim_type")
        if claim_type not in VALID_CLAIM_TYPES:
            issues.append(
                ValidationIssue(
                    path,
                    "invalid_claim_type",
                    f"claim_type must be one of {sorted(VALID_CLAIM_TYPES)}",
                )
            )
            continue

        enters = bool(term.get("enters_spacetime_equation", False))
        if claim_type == "physical":
            missing = sorted(
                field for field in PHYSICAL_REQUIRED if not str(term.get(field, "")).strip()
            )
            if missing:
                issues.append(
                    ValidationIssue(
                        path,
                        "incomplete_physical_term",
                        "physical term is missing: " + ", ".join(missing),
                    )
                )
        elif enters:
            issues.append(
                ValidationIssue(
                    path,
                    "category_collapse",
                    f"{claim_type} term cannot enter a spacetime equation without a typed physical map",
                )
            )

        if enters and not str(term.get("physical_projection", "")).strip():
            issues.append(
                ValidationIssue(
                    path,
                    "missing_physical_projection",
                    "term entering a spacetime equation requires physical_projection",
                )
            )
    return ValidationResult(valid=not issues, issues=tuple(issues))


COEFFICIENT_REQUIRED = {
    "name",
    "domain",
    "units",
    "prior_or_range",
    "null_condition",
    "observable",
    "rejection_rule",
}


def validate_coefficient_ledger(rows: Iterable[dict[str, Any]]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    for index, row in enumerate(rows):
        missing = sorted(field for field in COEFFICIENT_REQUIRED if not str(row.get(field, "")).strip())
        if missing:
            issues.append(
                ValidationIssue(
                    f"coefficients[{index}]",
                    "incomplete_coefficient",
                    "coefficient is missing: " + ", ".join(missing),
                )
            )
    return ValidationResult(valid=not issues, issues=tuple(issues))


def demo_payload() -> dict[str, Any]:
    frozen = ConstantPotential(0.7)
    rho_frozen = scalar_energy_density(0.0, frozen.value(0.0))
    p_frozen = scalar_pressure(0.0, frozen.value(0.0))
    simulation = simulate_flat_flrw(
        BackgroundState(time=0.0, phi=0.3, phi_dot=0.0, rho_matter=0.8),
        QuadraticPotential(mass=0.2, offset=0.1),
        dt=0.02,
        steps=25,
    )
    convergence = convergence_report(
        BackgroundState(time=0.0, phi=0.3, phi_dot=0.0, rho_matter=0.8),
        QuadraticPotential(mass=0.2, offset=0.1),
        horizon=0.5,
        coarse_steps=10,
    )
    stability = assess_effective_stability(
        kinetic_normalization=1.0,
        sound_speed_squared=1.0,
        energy_to_cutoff_ratio=0.1,
    )
    return {
        "schema": "gmut.kernel.demo.v1",
        "claim_status": "deterministic_toy_validation_not_empirical_confirmation",
        "identities": {
            "frozen_field_rho": rho_frozen,
            "frozen_field_pressure": p_frozen,
            "frozen_field_w": equation_of_state(rho_frozen, p_frozen),
            "balanced_exchange_residual": exchange_residual(0.125, -0.125),
            "null_omega_component": omega_component(0.0),
        },
        "simulation": {
            "units": "dimensionless_planck_units",
            "model": "flat_FLRW_canonical_scalar_plus_dust",
            "samples": [asdict(sample) for sample in simulation],
            "maximum_absolute_friedmann_residual": max(
                abs(sample.friedmann_residual) for sample in simulation
            ),
        },
        "convergence": convergence,
        "minimal_stability_gate": asdict(stability),
    }


def _result_payload(result: ValidationResult) -> dict[str, Any]:
    return {"valid": result.valid, "issues": [asdict(issue) for issue in result.issues]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser("demo", help="emit deterministic identity and toy-simulation output")
    demo.add_argument("--output", type=Path)
    registry = subparsers.add_parser("validate-registry", help="validate a JSON term registry")
    registry.add_argument("input", type=Path)
    ledger = subparsers.add_parser("validate-coefficients", help="validate a JSON coefficient ledger")
    ledger.add_argument("input", type=Path)
    args = parser.parse_args()

    if args.command == "demo":
        payload = demo_payload()
    elif args.command == "validate-registry":
        data = json.loads(args.input.read_text(encoding="utf-8"))
        terms = data["terms"] if isinstance(data, dict) else data
        payload = _result_payload(validate_term_registry(terms))
    else:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        rows = data["coefficients"] if isinstance(data, dict) else data
        payload = _result_payload(validate_coefficient_ledger(rows))

    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.command == "demo" and args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if payload.get("valid", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
