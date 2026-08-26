"""Typed synthetic sieve-stack and fraction-reconciliation checks."""

from __future__ import annotations

import itertools
from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

try:
    from scripts.ghc_family_grain_milling_contracts import ContractError
except ModuleNotFoundError:  # Direct script execution resolves from scripts/.
    from ghc_family_grain_milling_contracts import ContractError


def validate_sieve_stack(apertures_um: Sequence[int]) -> dict[str, Any]:
    if len(apertures_um) < 2:
        raise ContractError("insufficient_sieve_stack")
    if any(not isinstance(value, int) or value <= 0 for value in apertures_um):
        raise ContractError("invalid_aperture")
    if len(set(apertures_um)) != len(apertures_um):
        raise ContractError("duplicate_aperture")
    if list(apertures_um) != sorted(apertures_um, reverse=True):
        raise ContractError("apertures_not_descending")
    intervals = [
        {"upper_um": upper, "lower_um": lower, "upper_closed": True, "lower_closed": False}
        for upper, lower in itertools.pairwise(apertures_um)
    ]
    return {
        "accepted": True,
        "apertures_um": list(apertures_um),
        "intervals": intervals,
        "calibration_verified": False,
        "grading_authorized": False,
    }


def reconcile_fractions(
    input_g: float,
    fractions_g: Mapping[str, float],
    *,
    tolerance_g: float = 0.01,
) -> dict[str, Any]:
    total_input = Decimal(str(input_g))
    tolerance = Decimal(str(tolerance_g))
    if not total_input.is_finite() or total_input <= 0:
        raise ContractError("invalid_fraction_input")
    if not fractions_g:
        raise ContractError("missing_fractions")
    fraction_total = Decimal(0)
    for label, value in fractions_g.items():
        amount = Decimal(str(value))
        if not label or not amount.is_finite() or amount < 0:
            raise ContractError("invalid_fraction")
        fraction_total += amount
    variance = total_input - fraction_total
    return {
        "accepted": abs(variance) <= tolerance,
        "input_g": str(total_input),
        "fraction_total_g": str(fraction_total),
        "variance_g": str(variance),
        "measurement_claim": False,
        "grade_claim": False,
    }


def positive_fixture() -> dict[str, Any]:
    return {
        "stack": validate_sieve_stack([1000, 500, 250, 125]),
        "fractions": reconcile_fractions(
            100.0,
            {"oversize": 10.0, "coarse": 25.0, "mid": 35.0, "fine": 30.0},
        ),
    }
