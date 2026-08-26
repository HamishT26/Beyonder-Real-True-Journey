"""Synthetic three-lens correction and handover tribunal for Ilyra v670-v2."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

LENSES = {"observatory", "environmental_sample", "transit_service"}
LENS_FIELDS = {
    "observatory": {"fits_hdu_lineage", "calibration_frames", "time_reference_state"},
    "environmental_sample": {"custody_events", "preservation_state", "calibration_state"},
    "transit_service": {"service_calendar_revision", "publication_state", "alternate_format_state"},
}


class CustodyError(ValueError):
    """Raised when synthetic custody or handover evidence is invalid."""


def fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise CustodyError("unknown lens")
    row: dict[str, Any] = {
        "record_id": f"synthetic-{lens}-01",
        "lens": lens,
        "synthetic": True,
        "revision": 2,
        "prior_revision": 1,
        "correction_readback": True,
        "unresolved_items": ["competent review remains vacant"],
        "workload_hold": True,
        "authority_state": "vacant",
        "affected_user_evaluation": False,
        "manual_accessibility_evaluation": False,
        "real_people": 0,
        "real_records_or_samples": 0,
        "external_actions": 0,
    }
    if lens == "observatory":
        row.update(
            {
                "fits_hdu_lineage": ["primary", "synthetic-image-extension"],
                "calibration_frames": ["synthetic-bias", "synthetic-dark", "synthetic-flat"],
                "time_reference_state": "declared_uncertain_no_celestial_inference",
            }
        )
    elif lens == "environmental_sample":
        row.update(
            {
                "custody_events": ["synthetic-receipt", "synthetic-transfer", "synthetic-hold"],
                "preservation_state": "declared_unknown_no_analysis",
                "calibration_state": "vacant_no_release",
            }
        )
    else:
        row.update(
            {
                "service_calendar_revision": "synthetic-exception-v2",
                "publication_state": "held_not_published",
                "alternate_format_state": "structural_only_affected_user_review_vacant",
            }
        )
    return row


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise CustodyError("record must be an object")
    lens = record.get("lens")
    if lens not in LENSES:
        raise CustodyError("lens must be one of the three declared synthetic practices")
    required = {
        "record_id",
        "synthetic",
        "revision",
        "prior_revision",
        "correction_readback",
        "unresolved_items",
        "workload_hold",
        "authority_state",
        "affected_user_evaluation",
        "manual_accessibility_evaluation",
        "real_people",
        "real_records_or_samples",
        "external_actions",
    } | LENS_FIELDS[lens]
    missing = sorted(required - record.keys())
    if missing:
        raise CustodyError(f"missing fields: {missing}")
    if record["synthetic"] is not True:
        raise CustodyError("only synthetic fixtures are permitted")
    if record["revision"] != record["prior_revision"] + 1:
        raise CustodyError("revision chain must advance exactly once")
    if record["correction_readback"] is not True:
        raise CustodyError("correction readback is required")
    if not record["unresolved_items"] or record["workload_hold"] is not True:
        raise CustodyError("unresolved work and workload hold must remain visible")
    if record["authority_state"] != "vacant":
        raise CustodyError("authority cannot be supplied by the fixture")
    if record["affected_user_evaluation"] is not False or record["manual_accessibility_evaluation"] is not False:
        raise CustodyError("participant or manual evaluation cannot be fabricated")
    if any(record[key] != 0 for key in ("real_people", "real_records_or_samples", "external_actions")):
        raise CustodyError("real people, records, samples, and actions must remain zero")
    return {
        "accepted": True,
        "record_id": record["record_id"],
        "lens": lens,
        "revision": record["revision"],
        "unresolved_count": len(record["unresolved_items"]),
        "authority_conferred": False,
        "boundary": "synthetic handover representation only",
    }


def rejecting_fixtures(lens: str) -> list[dict[str, Any]]:
    fixtures = []
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
