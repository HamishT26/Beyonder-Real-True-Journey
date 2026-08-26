"""Synthetic astronomical plate-lineage correction and handover validator."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


class HandoverError(ValueError):
    """Raised when a synthetic lineage fixture loses evidence or authority boundaries."""


def positive_fixture(lens: str = "photographic_plate") -> dict[str, Any]:
    return {
        "fixture_class": "synthetic_only",
        "lens": lens,
        "identity_aliases": {
            "plate": "synthetic-plate", "envelope": "synthetic-envelope",
            "night_log": "synthetic-night-log", "scan_master": "synthetic-master",
            "access_derivative": "synthetic-access",
        },
        "cross_reference": {
            "plate_to_envelope": "synthetic-match",
            "envelope_to_log": "synthetic-match",
            "log_to_scan": "synthetic-match",
        },
        "events": [
            {"event_id": "E1", "at": "2030-01-01T00:00:00Z", "state": "catalogue", "supersedes": None},
            {"event_id": "E2", "at": "2030-01-01T00:05:00Z", "state": "scan", "supersedes": None},
            {"event_id": "E3", "at": "2030-01-01T00:10:00Z", "state": "correction", "supersedes": "E1"},
            {"event_id": "E4", "at": "2030-01-01T00:15:00Z", "state": "handover", "supersedes": None},
        ],
        "correction_preserves_original": True,
        "unresolved_tasks": ["synthetic professional review remains held"],
        "readback": {
            "performed": True, "next_owner_role": "vacant_synthetic_role",
            "delayed_status_disclosed": True,
        },
        "access_authority": None,
        "professional_authority": None,
        "legal_authority": None,
        "cultural_authority": None,
        "Māori_authority": None,
        "real_object": False,
        "external_actions": 0,
    }


def rejecting_fixtures(lens: str = "photographic_plate") -> list[dict[str, Any]]:
    base = positive_fixture(lens)
    order = deepcopy(base)
    order["events"][2]["at"] = "2029-12-31T23:00:00Z"
    erased = deepcopy(base)
    erased["correction_preserves_original"] = False
    dropped = deepcopy(base)
    dropped["unresolved_tasks"] = []
    authority = deepcopy(base)
    authority["Māori_authority"] = "repository software"
    return [order, erased, dropped, authority]


def validate_record(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "fixture_class", "lens", "identity_aliases", "cross_reference", "events",
        "correction_preserves_original", "unresolved_tasks", "readback",
        "access_authority", "professional_authority", "legal_authority",
        "cultural_authority", "Māori_authority", "real_object", "external_actions",
    }
    missing = sorted(required - set(row))
    if missing:
        raise HandoverError(f"missing fields: {missing}")
    if row["fixture_class"] != "synthetic_only" or row["real_object"] is not False or row["external_actions"] != 0:
        raise HandoverError("synthetic-only boundary crossed")
    aliases = {"plate", "envelope", "night_log", "scan_master", "access_derivative"}
    links = {"plate_to_envelope", "envelope_to_log", "log_to_scan"}
    if set(row["identity_aliases"]) != aliases or set(row["cross_reference"]) != links:
        raise HandoverError("identity alias or cross-reference topology drifted")
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
    for key in ("access_authority", "professional_authority", "legal_authority", "cultural_authority", "Māori_authority"):
        if row[key] is not None:
            raise HandoverError(f"authority vacancy filled: {key}")
    return {
        "accepted": True, "lens": row["lens"], "events": len(row["events"]),
        "cross_references": len(row["cross_reference"]),
        "unresolved_tasks": len(row["unresolved_tasks"]),
        "correction_non_erasure": True, "authority_conferred": False,
        "external_actions": 0,
    }
