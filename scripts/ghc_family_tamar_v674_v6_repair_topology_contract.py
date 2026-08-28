"""Synthetic three-lens topology and observation-vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class ObservationContractError(ValueError):
    """Raised when a fixture asserts real observation, measurement, or authority."""


LENSES = {"umbrella_repair", "fountain_pen_repair", "marionette_maintenance", "accessible_status"}
VACANT_FIELDS = (
    "component_count",
    "topology_edge_count",
    "length_m",
    "alignment_ratio",
    "material_composition",
    "temperature_k",
    "condition_assessment",
    "repair_recommendation",
    "safety_release",
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
        "component_count": None,
        "topology_edge_count": None,
        "length_m": None,
        "alignment_ratio": None,
        "material_composition": None,
        "temperature_k": None,
        "condition_assessment": None,
        "repair_recommendation": None,
        "safety_release": None,
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
    base = positive_fixture("umbrella_repair")
    rows: list[dict[str, Any]] = []
    for field, value in (
        ("synthetic", False),
        ("real_people", 1),
        ("component_count", 42),
        ("authority_conferred", True),
        ("external_actions", 1),
    ):
        row = deepcopy(base)
        row[field] = value
        rows.append(row)
    return rows
