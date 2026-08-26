"""Synthetic footwear component and observation-vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class ObservationContractError(ValueError):
    """Raised when a fixture asserts real observation, measurement, or authority."""


LENSES = {"footwear_intake", "component_topology", "assembly_sequence", "accessible_status"}
VACANT_FIELDS = (
    "last_length_mm",
    "pattern_allowance_mm",
    "upper_material_identity",
    "sole_layer_thickness_mm",
    "stitch_count",
    "adhesive_cure_minutes",
    "fit_assessment",
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
        "last_length_mm": None,
        "pattern_allowance_mm": None,
        "upper_material_identity": None,
        "sole_layer_thickness_mm": None,
        "stitch_count": None,
        "adhesive_cure_minutes": None,
        "fit_assessment": None,
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
    base = positive_fixture("footwear_intake")
    rows: list[dict[str, Any]] = []
    for field, value in (
        ("synthetic", False),
        ("real_people", 1),
        ("last_length_mm", 270),
        ("authority_conferred", True),
        ("external_actions", 1),
    ):
        row = deepcopy(base)
        row[field] = value
        rows.append(row)
    return rows
