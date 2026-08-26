"""Synthetic mechanical-calculator trace and observation-vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class ObservationContractError(ValueError):
    """Raised when a fixture asserts real observation, measurement, or authority."""


LENSES = {"collection_intake", "mechanism_trace", "arithmetic_trace", "accessible_status"}
VACANT_FIELDS = (
    "input_register_value",
    "result_register_value",
    "crank_turn_count",
    "carriage_position",
    "measured_force_n",
    "temperature_k",
    "condition_assessment",
    "accuracy_claim",
)


def positive_fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise ObservationContractError(f"unknown lens: {lens}")
    return {
        "lens": lens,
        "synthetic": True,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "external_actions": 0,
        "input_register_value": None,
        "result_register_value": None,
        "crank_turn_count": None,
        "carriage_position": None,
        "measured_force_n": None,
        "temperature_k": None,
        "condition_assessment": None,
        "accuracy_claim": None,
        "observation_state": "unknown_not_observed",
        "professional_interpretation": False,
        "authority_conferred": False,
    }


def validate_contract(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("lens") not in LENSES or row.get("synthetic") is not True:
        raise ObservationContractError("declared synthetic lens required")
    if any(
        row.get(field) != 0
        for field in ("real_people", "real_objects", "real_measurements", "external_actions")
    ):
        raise ObservationContractError("real or external activity rejected")
    if any(row.get(field) is not None for field in VACANT_FIELDS):
        raise ObservationContractError("unobserved measurement fields must remain vacant")
    if row.get("observation_state") != "unknown_not_observed":
        raise ObservationContractError("observation vacancy must remain explicit")
    if row.get("professional_interpretation") is not False or row.get("authority_conferred") is not False:
        raise ObservationContractError("professional or authority promotion rejected")
    return {**row, "accepted": True}


def rejecting_fixtures() -> list[dict[str, Any]]:
    base = positive_fixture("collection_intake")
    rows: list[dict[str, Any]] = []
    for field, value in (
        ("synthetic", False),
        ("real_people", 1),
        ("result_register_value", 42),
        ("authority_conferred", True),
        ("external_actions", 1),
    ):
        row = deepcopy(base)
        row[field] = value
        rows.append(row)
    return rows
