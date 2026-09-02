"""Phase-local bounded runner 06: ghc_family_provenance_cycle_guard_runner.py."""

from __future__ import annotations

from typing import Any


def evaluate(fixture: dict[str, Any]) -> dict[str, Any]:
    accepted = (
        fixture.get("synthetic") is True
        and fixture.get("real_row_count") == 0
        and fixture.get("authority_status") == "reserved"
        and fixture.get("claim_scope") == "bounded_synthetic_structure_only"
    )
    return {
        "runner_index": 6,
        "runner_name": "ghc_family_provenance_cycle_guard_runner.py",
        "accepted": accepted,
        "real_world_action": False,
        "authority_status": "reserved",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
