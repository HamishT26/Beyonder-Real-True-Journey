"""Bounded x2 validators for Vesper Arlen v671-v7.

The validators operate only on synthetic JSON fixtures. They inspect, handle,
wind, start, stop, sound, time, calibrate, repair, treat, authenticate, value,
transfer, or publish no real metronome, score, recording, collection object,
person, place, identity, measurement, result, or record.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from ghc_family_vesper_arlen_v671_v7_archive import PROTECTED_GATES
except ModuleNotFoundError:  # package import under repository-root test discovery
    from scripts.ghc_family_vesper_arlen_v671_v7_archive import PROTECTED_GATES

REQUIRED_ZERO_COUNTERS = [
    "real_people",
    "real_metronomes",
    "real_scores",
    "real_media",
    "real_measurements",
    "handling_actions",
    "winding_actions",
    "operation_actions",
    "sounding_actions",
    "timing_or_calibration_actions",
    "treatment_actions",
    "professional_actions",
    "external_actions",
    "authority_actions",
]


def validate_synthetic_contract(payload: dict[str, Any], expected_slug: str) -> dict[str, Any]:
    failures: list[str] = []
    if payload.get("semantic_slug") != expected_slug:
        failures.append("semantic_slug_mismatch")
    if payload.get("synthetic_only") is not True:
        failures.append("synthetic_only_required")
    if payload.get("typed_state") != "documented_zero-real-row_fixture":
        failures.append("typed_state_must_be_unambiguous")
    zero = payload.get("zero_counters", {})
    if any(zero.get(key) != 0 for key in REQUIRED_ZERO_COUNTERS):
        failures.append("all_real_world_counters_must_be_zero")
    if payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        failures.append("terminal_nonpromotion_required")
    if payload.get("protected_gates") != PROTECTED_GATES:
        failures.append("protected_gate_set_mismatch")
    return {
        "schema": "ghc.family.synthetic-contract-validation.v1",
        "expected_slug": expected_slug,
        "passed": not failures,
        "failures": failures,
        "external_actions": 0,
    }


def runner_main(expected_slug: str) -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: runner <contract.json>")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = validate_synthetic_contract(payload, expected_slug)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
