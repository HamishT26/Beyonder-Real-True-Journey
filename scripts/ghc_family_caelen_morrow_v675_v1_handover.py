from __future__ import annotations

from typing import Any


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    events = payload.get("events")
    if not isinstance(events, list) or not events:
        reasons.append("events_missing")
        events = []
    sequences = [row.get("sequence") for row in events if isinstance(row, dict)]
    if sequences != list(range(1, len(sequences) + 1)):
        reasons.append("sequence_not_contiguous")
    ids = {row.get("event_id") for row in events if isinstance(row, dict)}
    for row in events:
        if isinstance(row, dict) and row.get("kind") == "correction" and row.get("supersedes") not in ids:
            reasons.append("correction_target_missing")
    if payload.get("professional_release") not in (None, False):
        reasons.append("professional_release_promoted")
    if payload.get("authority_conferred") not in (None, False):
        reasons.append("authority_promoted")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "events": len(events),
        "correction_non_erasure": bool(events),
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
