"""Synthetic three-lens drawing revision and handover tribunal for v672-v1."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

LENSES = {"architectural_revision", "external_reference_transmittal", "accessible_register"}
LENS_FIELDS = {
    "architectural_revision": {"sheet_revision_map", "supersession_state", "change_cloud_state"},
    "external_reference_transmittal": {"reference_revision_map", "transmittal_state", "receipt_readback"},
    "accessible_register": {"register_columns", "status_announcement", "manual_evaluation_state"},
}


class RevisionTribunalError(ValueError):
    """Raised when synthetic revision or handover evidence is invalid."""


def fixture(lens: str) -> dict[str, Any]:
    """Return a synthetic record for one declared lens."""

    if lens not in LENSES:
        raise RevisionTribunalError("unknown lens")
    row: dict[str, Any] = {
        "record_id": f"synthetic-{lens}-01",
        "lens": lens,
        "synthetic": True,
        "revision": 2,
        "prior_revision": 1,
        "correction_readback": True,
        "unresolved_items": ["competent review and issue authority remain vacant"],
        "workload_hold": True,
        "authority_state": "vacant",
        "rights_state": "vacant",
        "affected_user_evaluation": False,
        "manual_accessibility_evaluation": False,
        "real_people": 0,
        "real_drawings_or_transmittals": 0,
        "external_actions": 0,
    }
    if lens == "architectural_revision":
        row.update(
            {
                "sheet_revision_map": {"SYN-A-001": 2, "SYN-A-101": 2},
                "supersession_state": "prior_synthetic_revision_retained_as_superseded",
                "change_cloud_state": "declared_fixture_only_not_professional_markup",
            }
        )
    elif lens == "external_reference_transmittal":
        row.update(
            {
                "reference_revision_map": {"synthetic-structure": 2, "synthetic-services": 2},
                "transmittal_state": "held_not_delivered",
                "receipt_readback": True,
            }
        )
    else:
        row.update(
            {
                "register_columns": ["sheet identifier", "title", "revision", "status", "unresolved note"],
                "status_announcement": "structural status text present",
                "manual_evaluation_state": "reserved",
            }
        )
    return row


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic record while retaining every authority vacancy."""

    if not isinstance(record, dict):
        raise RevisionTribunalError("record must be an object")
    lens = record.get("lens")
    if lens not in LENSES:
        raise RevisionTribunalError("lens must be one of the three declared synthetic practices")
    required = {
        "record_id",
        "synthetic",
        "revision",
        "prior_revision",
        "correction_readback",
        "unresolved_items",
        "workload_hold",
        "authority_state",
        "rights_state",
        "affected_user_evaluation",
        "manual_accessibility_evaluation",
        "real_people",
        "real_drawings_or_transmittals",
        "external_actions",
    } | LENS_FIELDS[lens]
    missing = sorted(required - record.keys())
    if missing:
        raise RevisionTribunalError(f"missing fields: {missing}")
    if record["synthetic"] is not True:
        raise RevisionTribunalError("only synthetic fixtures are permitted")
    if record["revision"] != record["prior_revision"] + 1:
        raise RevisionTribunalError("revision chain must advance exactly once")
    if record["correction_readback"] is not True:
        raise RevisionTribunalError("correction readback is required")
    if not record["unresolved_items"] or record["workload_hold"] is not True:
        raise RevisionTribunalError("unresolved work and workload hold must remain visible")
    if record["authority_state"] != "vacant" or record["rights_state"] != "vacant":
        raise RevisionTribunalError("authority and rights cannot be supplied by the fixture")
    if record["affected_user_evaluation"] is not False or record["manual_accessibility_evaluation"] is not False:
        raise RevisionTribunalError("participant or manual evaluation cannot be fabricated")
    if any(record[key] != 0 for key in ("real_people", "real_drawings_or_transmittals", "external_actions")):
        raise RevisionTribunalError("real people, drawings, transmittals, and actions must remain zero")
    if lens == "external_reference_transmittal" and record["transmittal_state"] != "held_not_delivered":
        raise RevisionTribunalError("synthetic transmittal must remain undelivered")
    if lens == "accessible_register" and record["manual_evaluation_state"] != "reserved":
        raise RevisionTribunalError("manual accessibility evaluation must remain reserved")
    return {
        "accepted": True,
        "record_id": record["record_id"],
        "lens": lens,
        "revision": record["revision"],
        "unresolved_count": len(record["unresolved_items"]),
        "authority_conferred": False,
        "boundary": "synthetic drawing handover representation only",
    }


def rejecting_fixtures(lens: str) -> list[dict[str, Any]]:
    """Return four rejecting fixtures for the selected lens."""

    fixtures: list[dict[str, Any]] = []
    for mutator in (
        lambda row: row.update({"revision": row["prior_revision"]}),
        lambda row: row.update({"correction_readback": False}),
        lambda row: row.update({"authority_state": "granted"}),
        lambda row: row.update({"external_actions": 1}),
    ):
        row = deepcopy(fixture(lens))
        mutator(row)
        fixtures.append(row)
    return fixtures
