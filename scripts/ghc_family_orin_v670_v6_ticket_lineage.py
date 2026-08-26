"""Synthetic maintenance-ticket correction and handover lineage."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class HandoverError(ValueError):
    """Raised when ticket lineage erases provenance or asserts real authority."""


LENSES = {"maintenance_ticket", "station_notice", "community_cooperative"}


def positive_fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise HandoverError(f"unknown lens: {lens}")
    return {
        "lens": lens,
        "events": [
            {"sequence": 1, "state": "reported", "supersedes": None},
            {"sequence": 2, "state": "corrected_synthetic", "supersedes": 1},
            {"sequence": 3, "state": "readback_acknowledged_proxy", "supersedes": None},
        ],
        "correction_non_erasure": True, "handover_present": True,
        "real_operator": False, "authority_conferred": False, "external_actions": 0,
    }


def validate_record(row: dict[str, Any]) -> dict[str, Any]:
    events = row.get("events")
    sequences = [event.get("sequence") for event in events] if isinstance(events, list) else []
    if row.get("lens") not in LENSES or sequences != sorted(sequences) or len(set(sequences)) != len(sequences) or len(sequences) < 3:
        raise HandoverError("ordered synthetic lineage required")
    if row.get("correction_non_erasure") is not True or row.get("handover_present") is not True:
        raise HandoverError("non-erasing correction and handover required")
    if row.get("real_operator") is not False or row.get("authority_conferred") is not False or row.get("external_actions") != 0:
        raise HandoverError("operator, authority, or external-action promotion rejected")
    return {**row, "accepted": True}


def rejecting_fixtures() -> list[dict[str, Any]]:
    base = positive_fixture("maintenance_ticket")
    rows: list[dict[str, Any]] = []
    erased = deepcopy(base); erased["correction_non_erasure"] = False; rows.append(erased)
    unordered = deepcopy(base); unordered["events"][1]["sequence"] = 0; rows.append(unordered)
    operator = deepcopy(base); operator["real_operator"] = True; rows.append(operator)
    external = deepcopy(base); external["external_actions"] = 1; rows.append(external)
    return rows
