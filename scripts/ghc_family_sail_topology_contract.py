"""Synthetic sail topology and observation-vacancy contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class ObservationContractError(ValueError):
    """Raised when a fixture asserts real observation, measurement, or authority."""


LENSES = {"loft_pattern", "panel_seam", "attachment_handover", "accessible_status"}
VACANT_FIELDS = ("panel_count", "seam_edge_count", "length_m", "width_m", "angle_rad", "material_composition", "seam_state", "attachment_state", "condition_assessment", "treatment_recommendation", "safety_release")


def positive_fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise ObservationContractError(f"unknown lens: {lens}")
    row = {"lens": lens, "synthetic": True, "real_people": 0, "real_objects": 0, "real_measurements": 0, "external_actions": 0, "observation_state": "unknown_not_observed", "professional_interpretation": False, "authority_conferred": False}
    row.update({field: None for field in VACANT_FIELDS})
    return row


def validate_contract(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("lens") not in LENSES or row.get("synthetic") is not True:
        raise ObservationContractError("declared synthetic lens required")
    if any(row.get(field) != 0 for field in ("real_people", "real_objects", "real_measurements", "external_actions")):
        raise ObservationContractError("real or external activity rejected")
    if any(row.get(field) is not None for field in VACANT_FIELDS):
        raise ObservationContractError("unobserved sail fields must remain vacant")
    if row.get("observation_state") != "unknown_not_observed":
        raise ObservationContractError("observation vacancy must remain explicit")
    if row.get("professional_interpretation") is not False or row.get("authority_conferred") is not False:
        raise ObservationContractError("professional or authority promotion rejected")
    return {**row, "accepted": True}


def rejecting_fixtures() -> list[dict[str, Any]]:
    base = positive_fixture("loft_pattern")
    rows: list[dict[str, Any]] = []
    for field, value in (("synthetic", False), ("real_people", 1), ("panel_count", 42), ("authority_conferred", True), ("external_actions", 1)):
        row = deepcopy(base)
        row[field] = value
        rows.append(row)
    return rows
