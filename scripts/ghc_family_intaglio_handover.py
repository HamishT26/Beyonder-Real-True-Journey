from __future__ import annotations

from typing import Any


def validate_handover(payload: dict[str, Any]) -> dict[str, Any]:
    events = payload.get("events", [])
    errors: list[str] = []
    sequences = [event.get("sequence") for event in events]
    if sequences != list(range(1, len(events) + 1)):
        errors.append("sequence")
    if any(event.get("operation") == "delete" for event in events):
        errors.append("destructive_operation")
    if payload.get("challenge_open") and payload.get("remedy_authority_present"):
        errors.append("invented_remedy_authority")
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_lock")
    return {"passed": not errors, "errors": errors, "event_count": len(events)}
