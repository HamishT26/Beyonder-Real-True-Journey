"""Synthetic three-lens correction, readback, and handover lineage."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class HandoverError(ValueError):
    """Raised when lineage erases provenance or asserts a real operator or authority."""


LENSES = {"umbrella_repair", "fountain_pen_repair", "marionette_maintenance", "accessible_status"}


def positive_fixture(lens: str) -> dict[str, Any]:
    if lens not in LENSES:
        raise HandoverError(f"unknown lens: {lens}")
    return {
        "lens": lens,
        "events": [
            {"sequence": 1, "state": "repair_record_reported_synthetic", "supersedes": None},
            {"sequence": 2, "state": "repair_record_corrected_synthetic", "supersedes": 1},
            {"sequence": 3, "state": "readback_acknowledged_proxy", "supersedes": None},
            {"sequence": 4, "state": "handover_ready_proxy", "supersedes": None},
        ],
        "correction_non_erasure": True,
        "handover_present": True,
        "workload_release_claimed": False,
        "real_operator": False,
        "authority_conferred": False,
        "external_actions": 0,
    }


def validate_record(row: dict[str, Any]) -> dict[str, Any]:
    events = row.get("events")
    sequences = [event.get("sequence") for event in events] if isinstance(events, list) else []
    if row.get("lens") not in LENSES or len(sequences) < 4:
        raise HandoverError("declared lens and four-event synthetic lineage required")
    if sequences != sorted(sequences) or len(set(sequences)) != len(sequences):
        raise HandoverError("strictly ordered unique event sequence required")
    if row.get("correction_non_erasure") is not True or row.get("handover_present") is not True:
        raise HandoverError("non-erasing correction and handover required")
    if row.get("workload_release_claimed") is not False:
        raise HandoverError("workload release claim rejected")
    if row.get("real_operator") is not False or row.get("authority_conferred") is not False:
        raise HandoverError("operator or authority promotion rejected")
    if row.get("external_actions") != 0:
        raise HandoverError("external action promotion rejected")
    return {**row, "accepted": True}


def rejecting_fixtures() -> list[dict[str, Any]]:
    base = positive_fixture("umbrella_repair")
    rows: list[dict[str, Any]] = []
    erased = deepcopy(base)
    erased["correction_non_erasure"] = False
    rows.append(erased)
    unordered = deepcopy(base)
    unordered["events"][1]["sequence"] = 0
    rows.append(unordered)
    duplicate = deepcopy(base)
    duplicate["events"][2]["sequence"] = 2
    rows.append(duplicate)
    operator = deepcopy(base)
    operator["real_operator"] = True
    rows.append(operator)
    external = deepcopy(base)
    external["external_actions"] = 1
    rows.append(external)
    return rows
