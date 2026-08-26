"""Fail-closed synthetic hold and release-state checks."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

try:
    from scripts.ghc_family_grain_milling_contracts import ContractError
except ModuleNotFoundError:  # Direct script execution resolves from scripts/.
    from ghc_family_grain_milling_contracts import ContractError

ALLOWED_STATES = {"planned", "active", "held", "quarantined", "stopped", "released", "unknown"}


def evaluate_hold(record: Mapping[str, Any]) -> dict[str, Any]:
    state = record.get("state")
    if state not in ALLOWED_STATES:
        raise ContractError("unknown_hold_state")
    if record.get("real_lot", False) or record.get("external_action", False):
        raise ContractError("real_or_external_surface_prohibited")
    evidence = record.get("evidence", {})
    if not isinstance(evidence, Mapping):
        raise ContractError("invalid_evidence")
    release_requested = state == "released"
    fixture_authority = record.get("fixture_authority") == "SYNTHETIC_TEST_ONLY"
    evidence_complete = all(
        evidence.get(field) is True
        for field in ("identity_checked", "correction_reviewed", "hold_reason_resolved")
    )
    if release_requested and not (fixture_authority and evidence_complete):
        raise ContractError("release_gate_not_satisfied")
    return {
        "accepted": True,
        "state": state,
        "release_requested": release_requested,
        "synthetic_gate_satisfied": fixture_authority and evidence_complete,
        "real_release_authorized": False,
        "external_actions": 0,
    }


def positive_fixture() -> dict[str, Any]:
    return evaluate_hold(
        {
            "state": "held",
            "real_lot": False,
            "external_action": False,
            "evidence": {
                "identity_checked": True,
                "correction_reviewed": True,
                "hold_reason_resolved": False,
            },
        }
    )
