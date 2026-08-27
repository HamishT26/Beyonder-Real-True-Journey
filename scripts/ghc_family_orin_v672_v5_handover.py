"""Synthetic correction, workload, pause, and handover contract for v672-v5."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class HandoverError(ValueError):
    """Raised when a bounded handover fixture fails closed."""


def positive_fixture(lens: str) -> dict[str, Any]:
    return {
        "lens": lens,
        "queue_id": f"synthetic-{lens}-queue",
        "open_items": 2,
        "queue_cap": 4,
        "pause_requested": False,
        "stop_requested": False,
        "unresolved_hold_count": 1,
        "correction_readback": True,
        "handover_acknowledged": True,
        "synthetic": True,
        "real_operators": 0,
        "external_actions": 0,
        "release_authority": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def rejecting_fixtures(lens: str) -> list[dict[str, Any]]:
    base = positive_fixture(lens)
    overload = deepcopy(base)
    overload["open_items"] = 5
    no_readback = deepcopy(base)
    no_readback["correction_readback"] = False
    real_operator = deepcopy(base)
    real_operator["real_operators"] = 1
    release = deepcopy(base)
    release["release_authority"] = True
    promotion = deepcopy(base)
    promotion["terminal_verdict"] = "READY_FOR_STAGE_20"
    return [overload, no_readback, real_operator, release, promotion]


def validate_handover(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "lens",
        "queue_id",
        "open_items",
        "queue_cap",
        "pause_requested",
        "stop_requested",
        "unresolved_hold_count",
        "correction_readback",
        "handover_acknowledged",
        "synthetic",
        "real_operators",
        "external_actions",
        "release_authority",
        "terminal_verdict",
    }
    missing = sorted(required - row.keys())
    if missing:
        raise HandoverError(f"missing handover fields: {missing}")
    if row["open_items"] > row["queue_cap"]:
        raise HandoverError("queue cap exceeded")
    if not row["correction_readback"] or not row["handover_acknowledged"]:
        raise HandoverError("correction or handover acknowledgement absent")
    if row["synthetic"] is not True or row["real_operators"] != 0:
        raise HandoverError("real operator or nonsynthetic state prohibited")
    if row["external_actions"] != 0 or row["release_authority"] is not False:
        raise HandoverError("external action or release authority prohibited")
    if row["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise HandoverError("terminal verdict promotion prohibited")
    return {
        "accepted": True,
        "lens": row["lens"],
        "queue_within_cap": True,
        "hold_preserved": row["unresolved_hold_count"] > 0,
        "external_actions": 0,
        "release_authority": False,
    }
