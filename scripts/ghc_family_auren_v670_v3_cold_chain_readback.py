"""Synthetic three-lens cold-chain correction tribunal for Auren v670-v3."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

LENSES = {"seed_bank", "herbarium_freezer", "reagent_cold_chain"}
LENS_FIELDS = {
    "seed_bank": {"accession_alias", "seed_lot_lineage", "chamber_location_state"},
    "herbarium_freezer": {"specimen_alias", "defrost_exception_state", "transfer_destination_state"},
    "reagent_cold_chain": {"reagent_alias", "custody_state", "hazard_review_state"},
}


class ReadbackError(ValueError):
    """Raised when synthetic correction or handover evidence is invalid."""


def fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise ReadbackError("unknown lens")
    row: dict[str, Any] = {
        "record_id": f"synthetic-{lens}-01",
        "lens": lens,
        "synthetic": True,
        "revision": 2,
        "prior_revision": 1,
        "excursion_state": "synthetic_threshold_crossing_unverified",
        "correction_readback": True,
        "unresolved_items": ["competent review remains vacant"],
        "workload_hold": True,
        "authority_state": "vacant",
        "affected_user_evaluation": False,
        "manual_accessibility_evaluation": False,
        "real_people": 0,
        "real_records_or_measurements": 0,
        "external_actions": 0,
    }
    if lens == "seed_bank":
        row.update(
            {
                "accession_alias": "synthetic-accession-A",
                "seed_lot_lineage": ["synthetic-parent-lot", "synthetic-held-packet"],
                "chamber_location_state": "synthetic_rack_location_unverified",
            }
        )
    elif lens == "herbarium_freezer":
        row.update(
            {
                "specimen_alias": "synthetic-specimen-B",
                "defrost_exception_state": "held_for_competent_review",
                "transfer_destination_state": "vacant_not_transferred",
            }
        )
    else:
        row.update(
            {
                "reagent_alias": "synthetic-reagent-C",
                "custody_state": "held_not_released",
                "hazard_review_state": "vacant_no_safety_claim",
            }
        )
    return row


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ReadbackError("record must be an object")
    lens = record.get("lens")
    if lens not in LENSES:
        raise ReadbackError("lens must be one of the three declared synthetic practices")
    required = {
        "record_id",
        "synthetic",
        "revision",
        "prior_revision",
        "excursion_state",
        "correction_readback",
        "unresolved_items",
        "workload_hold",
        "authority_state",
        "affected_user_evaluation",
        "manual_accessibility_evaluation",
        "real_people",
        "real_records_or_measurements",
        "external_actions",
    } | LENS_FIELDS[lens]
    missing = sorted(required - record.keys())
    if missing:
        raise ReadbackError(f"missing fields: {missing}")
    if record["synthetic"] is not True:
        raise ReadbackError("only synthetic fixtures are permitted")
    if record["revision"] != record["prior_revision"] + 1:
        raise ReadbackError("revision chain must advance exactly once")
    if record["correction_readback"] is not True:
        raise ReadbackError("correction readback is required")
    if not record["unresolved_items"] or record["workload_hold"] is not True:
        raise ReadbackError("unresolved work and workload hold must remain visible")
    if record["authority_state"] != "vacant":
        raise ReadbackError("authority cannot be supplied by the fixture")
    if record["affected_user_evaluation"] is not False or record["manual_accessibility_evaluation"] is not False:
        raise ReadbackError("participant or manual evaluation cannot be fabricated")
    if any(record[key] != 0 for key in ("real_people", "real_records_or_measurements", "external_actions")):
        raise ReadbackError("real people, records, measurements, and actions must remain zero")
    return {
        "accepted": True,
        "record_id": record["record_id"],
        "lens": lens,
        "revision": record["revision"],
        "unresolved_count": len(record["unresolved_items"]),
        "authority_conferred": False,
        "boundary": "synthetic cold-chain handover representation only",
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
