"""Synthetic preservation-environment contract; never professional advice."""

from __future__ import annotations

import math
from copy import deepcopy
from typing import Any


class EnvironmentContractError(ValueError):
    """Raised when a synthetic environmental fixture crosses its type boundary."""


def positive_fixture(lens: str = "rare_book") -> dict[str, Any]:
    return {
        "fixture_class": "synthetic_only", "lens": lens, "object_alias": f"synthetic-{lens}-item",
        "observed_at": "2030-01-01T00:00:00Z", "temperature_c": 18.0, "temperature_uncertainty_c": 0.5,
        "relative_humidity_percent": 45.0, "relative_humidity_uncertainty_percent": 2.0,
        "threshold_policy_id": "synthetic-local-policy-v1", "threshold_approval_authority": None,
        "calibration_authority": None, "damage_diagnosis": None, "professional_advice": False,
        "real_measurement": False, "external_actions": 0,
    }


def rejecting_fixtures(lens: str = "rare_book") -> list[dict[str, Any]]:
    base = positive_fixture(lens)
    missing = deepcopy(base); missing.pop("temperature_uncertainty_c")
    range_error = deepcopy(base); range_error["relative_humidity_percent"] = 140.0
    diagnosis = deepcopy(base); diagnosis["damage_diagnosis"] = "confirmed causal damage"
    authority = deepcopy(base); authority["threshold_approval_authority"] = "repository software"
    return [missing, range_error, diagnosis, authority]


def validate_contract(row: dict[str, Any]) -> dict[str, Any]:
    required = {"fixture_class", "lens", "object_alias", "observed_at", "temperature_c", "temperature_uncertainty_c", "relative_humidity_percent", "relative_humidity_uncertainty_percent", "threshold_policy_id", "threshold_approval_authority", "calibration_authority", "damage_diagnosis", "professional_advice", "real_measurement", "external_actions"}
    missing = sorted(required - set(row))
    if missing:
        raise EnvironmentContractError(f"missing fields: {missing}")
    numbers = [row["temperature_c"], row["temperature_uncertainty_c"], row["relative_humidity_percent"], row["relative_humidity_uncertainty_percent"]]
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in numbers):
        raise EnvironmentContractError("nonfinite or nonnumeric observation")
    if not 0 <= row["relative_humidity_percent"] <= 100 or row["temperature_uncertainty_c"] < 0 or row["relative_humidity_uncertainty_percent"] < 0:
        raise EnvironmentContractError("observation outside typed bounds")
    if row["fixture_class"] != "synthetic_only" or row["real_measurement"] is not False or row["external_actions"] != 0:
        raise EnvironmentContractError("synthetic-only boundary crossed")
    if row["damage_diagnosis"] is not None or row["professional_advice"] is not False:
        raise EnvironmentContractError("diagnosis or professional-advice promotion")
    if row["threshold_approval_authority"] is not None or row["calibration_authority"] is not None:
        raise EnvironmentContractError("vacant authority was filled")
    return {"accepted": True, "lens": row["lens"], "paired_observation": True, "real_measurement": False, "damage_diagnosis": False, "authority_conferred": False, "external_actions": 0}
