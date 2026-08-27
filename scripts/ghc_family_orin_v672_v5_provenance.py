"""Typed synthetic accessible-publishing surface contracts for v672-v5."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SURFACES = [
    "tactile_source_lineage",
    "tactile_legend_integrity",
    "tactile_route_continuity",
    "braille_codepoint_guard",
    "braille_segment_lineage",
    "alternate_description_linkage",
    "proof_correction_lineage",
    "access_request_minimization",
    "accessible_notice_proxy",
    "access_workload_handover",
]


class SurfaceError(ValueError):
    """Raised when a synthetic surface violates its bounded contract."""


def positive_fixture(surface: str) -> dict[str, Any]:
    if surface not in SURFACES:
        raise SurfaceError(f"unknown surface: {surface}")
    return {
        "surface": surface,
        "record_id": f"synthetic-{surface}-001",
        "source_ref": "synthetic-source-v1",
        "revision": 1,
        "supersedes": None,
        "status": "bounded_accepting_fixture",
        "synthetic": True,
        "real_people": 0,
        "real_objects_or_records": 0,
        "external_actions": 0,
        "authority_claim": False,
        "manual_evaluation_reserved": True,
        "affected_user_evaluation_reserved": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def rejecting_fixtures(surface: str) -> list[dict[str, Any]]:
    base = positive_fixture(surface)
    missing = deepcopy(base)
    missing.pop("source_ref")
    real_person = deepcopy(base)
    real_person["real_people"] = 1
    action = deepcopy(base)
    action["external_actions"] = 1
    authority = deepcopy(base)
    authority["authority_claim"] = True
    promotion = deepcopy(base)
    promotion["terminal_verdict"] = "READY_FOR_STAGE_20"
    return [missing, real_person, action, authority, promotion]


def validate_surface(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "surface",
        "record_id",
        "source_ref",
        "revision",
        "status",
        "synthetic",
        "real_people",
        "real_objects_or_records",
        "external_actions",
        "authority_claim",
        "manual_evaluation_reserved",
        "affected_user_evaluation_reserved",
        "terminal_verdict",
    }
    missing = sorted(required - row.keys())
    if missing:
        raise SurfaceError(f"missing surface fields: {missing}")
    if row["surface"] not in SURFACES:
        raise SurfaceError("unknown surface")
    if row["synthetic"] is not True:
        raise SurfaceError("surface is not synthetic")
    if row["real_people"] != 0 or row["real_objects_or_records"] != 0:
        raise SurfaceError("real evidence is outside the surface contract")
    if row["external_actions"] != 0:
        raise SurfaceError("external action is prohibited")
    if row["authority_claim"] is not False:
        raise SurfaceError("authority promotion is prohibited")
    if row["manual_evaluation_reserved"] is not True or row["affected_user_evaluation_reserved"] is not True:
        raise SurfaceError("manual or affected-user evaluation was not reserved")
    if row["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise SurfaceError("terminal verdict promotion is prohibited")
    return {
        "accepted": True,
        "surface": row["surface"],
        "revision": row["revision"],
        "external_actions": 0,
        "authority_promoted": False,
    }


def run_surface(surface: str) -> dict[str, Any]:
    accepted = validate_surface(positive_fixture(surface))
    rejected = 0
    reasons = []
    for fixture in rejecting_fixtures(surface):
        try:
            validate_surface(fixture)
        except SurfaceError as exc:
            rejected += 1
            reasons.append(str(exc))
        else:
            raise SurfaceError(f"invalid fixture unexpectedly accepted for {surface}")
    if rejected != 5:
        raise SurfaceError(f"rejecting fixture drift for {surface}")
    return {
        "accepted": True,
        "surface": surface,
        "positive": accepted,
        "rejecting_fixtures": rejected,
        "reasons": reasons,
        "external_actions": 0,
        "authority_promoted": False,
        "boundary": "Synthetic structural evidence only; no accessibility, professional, legal, cultural, Māori-authority, or production claim.",
    }
