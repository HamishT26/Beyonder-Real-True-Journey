from __future__ import annotations

from typing import Any

OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = {
    "proposal_id",
    "title",
    "core_outcome",
    "synthetic_only",
    "executed",
    "real_people",
    "real_objects",
    "external_actions",
    "authority_conferred",
    "protected_gates",
    "evidence_class",
}


def validate_record(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(REQUIRED.difference(payload))
    if missing:
        errors.append("missing:" + ",".join(missing))
    if payload.get("core_outcome") not in OUTCOMES:
        errors.append("unknown_outcome")
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_lock")
    for field in ("real_people", "real_objects", "external_actions"):
        if payload.get(field) != 0:
            errors.append("nonzero:" + field)
    if payload.get("authority_conferred") is not False:
        errors.append("authority_promotion")
    if not payload.get("protected_gates"):
        errors.append("missing_protected_gates")
    if payload.get("core_outcome") in {"open_gap", "exact_gate"} and payload.get("executed") is not False:
        errors.append("held_row_executed")
    return {"passed": not errors, "errors": errors, "authority_conferred": False}


def run(payload: dict[str, Any]) -> dict[str, Any]:
    return validate_record(payload)
