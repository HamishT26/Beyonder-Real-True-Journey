"""Synthetic collection-custody correction and handover validator."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


class HandoverError(ValueError):
    """Raised when a synthetic custody/handover fixture loses evidence or authority boundaries."""


def positive_fixture(lens: str = "rare_book") -> dict[str, Any]:
    return {
        "fixture_class": "synthetic_only", "lens": lens,
        "object_alias": {"work": "synthetic-work", "edition": "synthetic-edition", "copy": "synthetic-copy", "item": "synthetic-item", "volume": "synthetic-volume"},
        "location": {"stack": "S1", "range": "R1", "bay": "B1", "case": "C1", "shelf": "H1", "enclosure": "E1"},
        "events": [
            {"event_id": "E1", "at": "2030-01-01T00:00:00Z", "state": "observation", "supersedes": None},
            {"event_id": "E2", "at": "2030-01-01T00:05:00Z", "state": "exception", "supersedes": None},
            {"event_id": "E3", "at": "2030-01-01T00:10:00Z", "state": "correction", "supersedes": "E2"},
            {"event_id": "E4", "at": "2030-01-01T00:15:00Z", "state": "handover", "supersedes": None},
        ],
        "correction_preserves_original": True, "unresolved_tasks": ["synthetic review remains held"],
        "readback": {"performed": True, "next_owner_role": "vacant_synthetic_role", "delayed_status_disclosed": True},
        "custody_authority": None, "condition_authority": None, "legal_authority": None, "cultural_authority": None, "Māori_authority": None,
        "real_object": False, "external_actions": 0,
    }


def rejecting_fixtures(lens: str = "rare_book") -> list[dict[str, Any]]:
    base = positive_fixture(lens)
    order = deepcopy(base); order["events"][2]["at"] = "2029-12-31T23:00:00Z"
    erased = deepcopy(base); erased["correction_preserves_original"] = False
    dropped = deepcopy(base); dropped["unresolved_tasks"] = []
    authority = deepcopy(base); authority["Māori_authority"] = "repository software"
    return [order, erased, dropped, authority]


def validate_record(row: dict[str, Any]) -> dict[str, Any]:
    required = {"fixture_class", "lens", "object_alias", "location", "events", "correction_preserves_original", "unresolved_tasks", "readback", "custody_authority", "condition_authority", "legal_authority", "cultural_authority", "Māori_authority", "real_object", "external_actions"}
    missing = sorted(required - set(row))
    if missing:
        raise HandoverError(f"missing fields: {missing}")
    if row["fixture_class"] != "synthetic_only" or row["real_object"] is not False or row["external_actions"] != 0:
        raise HandoverError("synthetic-only boundary crossed")
    aliases = {"work", "edition", "copy", "item", "volume"}
    locations = {"stack", "range", "bay", "case", "shelf", "enclosure"}
    if set(row["object_alias"]) != aliases or set(row["location"]) != locations:
        raise HandoverError("alias or location topology drifted")
    times = [datetime.fromisoformat(event["at"].replace("Z", "+00:00")) for event in row["events"]]
    if times != sorted(times) or len({event["event_id"] for event in row["events"]}) != len(row["events"]):
        raise HandoverError("event chronology or identity drifted")
    ids = {event["event_id"] for event in row["events"]}
    if any(event["supersedes"] is not None and event["supersedes"] not in ids for event in row["events"]):
        raise HandoverError("orphan correction")
    if row["correction_preserves_original"] is not True or not row["unresolved_tasks"]:
        raise HandoverError("correction or unresolved work was erased")
    if row["readback"].get("performed") is not True or row["readback"].get("delayed_status_disclosed") is not True:
        raise HandoverError("readback or delayed status missing")
    for key in ("custody_authority", "condition_authority", "legal_authority", "cultural_authority", "Māori_authority"):
        if row[key] is not None:
            raise HandoverError(f"authority vacancy filled: {key}")
    return {"accepted": True, "lens": row["lens"], "events": len(row["events"]), "unresolved_tasks": len(row["unresolved_tasks"]), "correction_non_erasure": True, "authority_conferred": False, "external_actions": 0}
