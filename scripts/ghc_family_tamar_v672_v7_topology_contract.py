"""Synthetic three-lens topology and observation-vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class ObservationContractError(ValueError):
    """Raised when a fixture asserts real observation, measurement, or authority."""


LENSES = {"stained_glass_panel", "dry_stone_wall", "ornamental_plaster", "accessible_status"}
VACANT_FIELDS = (
    "panel_piece_count",
    "came_junction_count",
    "course_elevation_m",
    "wall_batter_ratio",
    "plaster_layer_thickness_m",
    "temperature_k",
    "condition_assessment",
    "stability_assessment",
    "treatment_recommendation",
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
        "panel_piece_count": None,
        "came_junction_count": None,
        "course_elevation_m": None,
        "wall_batter_ratio": None,
        "plaster_layer_thickness_m": None,
        "temperature_k": None,
        "condition_assessment": None,
        "stability_assessment": None,
        "treatment_recommendation": None,
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
    base = positive_fixture("stained_glass_panel")
    rows: list[dict[str, Any]] = []
    for field, value in (
        ("synthetic", False),
        ("real_people", 1),
        ("panel_piece_count", 42),
        ("authority_conferred", True),
        ("external_actions", 1),
    ):
        row = deepcopy(base)
        row[field] = value
        rows.append(row)
    return rows
