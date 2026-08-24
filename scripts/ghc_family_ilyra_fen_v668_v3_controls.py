#!/usr/bin/env python3
"""Bounded synthetic film-calibration controls for Ilyra Fen v668-v3 x2."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


class RejectedFixture(ValueError):
    """An expected fail-closed fixture rejection."""


CONTROL_NAMES = (
    "frame_contract",
    "target_lineage",
    "optical_path",
    "registration",
    "motion_proxy",
    "sequence_order",
    "color_identity",
    "focus_proxy",
    "correction_ledger",
    "authority_firewall",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RejectedFixture(message)


def require_keys(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if key not in payload]
    require(not missing, f"missing required fields: {missing}")


def stable_digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def evaluate_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(payload, dict), "envelope must be an object")
    require_keys(payload, "schema_version", "owner", "phase", "proposal_id", "expected_disposition", "protected_claims", "authority_override")
    require(payload["schema_version"] == 1, "unsupported envelope schema")
    require(payload["owner"] == "Ilyra Fen", "wrong owner")
    require(payload["phase"] == "v668-v3", "wrong phase")
    require(isinstance(payload["proposal_id"], str) and payload["proposal_id"].startswith("IF6683-N"), "invalid proposal id")
    require(payload["expected_disposition"] in {"completed", "represented", "open_gap", "exact_gate"}, "invalid outcome vocabulary")
    require(isinstance(payload["protected_claims"], dict), "protected claims must be an object")
    require(payload["protected_claims"] and all(value is False for value in payload["protected_claims"].values()), "protected claim promotion refused")
    require(payload["authority_override"] is False, "authority override refused")
    return {"accepted": True, "proposal_id": payload["proposal_id"], "envelope_sha256": stable_digest(payload)}


def frame_contract(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "gauge_mm", "pitch_numerator_um", "pitch_denominator", "perforations_per_frame", "frame_index")
    require(payload["gauge_mm"] in {8, 16, 35, 65}, "unsupported film gauge")
    for key in ("pitch_numerator_um", "pitch_denominator", "perforations_per_frame", "frame_index"):
        require(type(payload[key]) is int, f"{key} must be an integer")
    require(payload["pitch_numerator_um"] > 0 and payload["pitch_denominator"] > 0, "pitch must be positive")
    require(payload["perforations_per_frame"] > 0, "perforation count must be positive")
    require(payload["frame_index"] >= 0, "frame index must be nonnegative")
    pitch = Fraction(payload["pitch_numerator_um"], payload["pitch_denominator"])
    return {"accepted": True, "pitch_um": [pitch.numerator, pitch.denominator], "frame_index": payload["frame_index"]}


def target_lineage(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "target_alias", "target_version", "status", "valid_from", "valid_until", "session_alias")
    require(all(isinstance(payload[key], str) and payload[key] for key in ("target_alias", "target_version", "valid_from", "valid_until", "session_alias")), "lineage strings must be nonempty")
    require(payload["status"] == "synthetic_current", "stale or unresolved target refused")
    require(payload["valid_from"] < payload["valid_until"], "invalid validity interval")
    return {"accepted": True, "lineage_sha256": stable_digest(payload), "authority": "vacant"}


def optical_path(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "gate_alias", "lens_alias", "sensor_alias", "lamp_alias", "transport_alias")
    fields = [payload[key] for key in ("gate_alias", "lens_alias", "sensor_alias", "lamp_alias", "transport_alias")]
    require(all(isinstance(value, str) and value and value != "unknown" for value in fields), "unknown optical component refused")
    require(len(set(fields)) == len(fields), "component aliases must be distinct")
    return {"accepted": True, "configuration_sha256": stable_digest(fields)}


def registration(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "matrix", "condition_limit", "source_coordinate_domain", "target_coordinate_domain")
    matrix = payload["matrix"]
    require(isinstance(matrix, list) and len(matrix) == 3 and all(isinstance(row, list) and len(row) == 3 for row in matrix), "matrix must be 3x3")
    require(all(type(value) in {int, float} and math.isfinite(value) for row in matrix for value in row), "matrix values must be finite numbers")
    require(matrix[2] == [0, 0, 1], "only an invertible affine synthetic fixture is admitted")
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    require(abs(determinant) > 1e-9, "singular registration refused")
    nonzero = [abs(value) for row in matrix[:2] for value in row[:2] if value]
    condition_proxy = max(nonzero) / min(nonzero)
    require(type(payload["condition_limit"]) in {int, float} and payload["condition_limit"] >= 1, "invalid condition limit")
    require(condition_proxy <= payload["condition_limit"], "ill-conditioned registration refused")
    require(payload["source_coordinate_domain"] != payload["target_coordinate_domain"], "coordinate domains must remain distinct")
    inverse = [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]
    return {"accepted": True, "determinant": determinant, "condition_proxy": condition_proxy, "inverse_linear": inverse}


def motion_proxy(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "frame_aliases", "displacement_px", "uncertainty_px", "diagnosis")
    require(isinstance(payload["frame_aliases"], list) and len(payload["frame_aliases"]) >= 3, "at least three frame aliases required")
    require(len(payload["displacement_px"]) == len(payload["frame_aliases"]), "displacement denominator mismatch")
    require(len(payload["uncertainty_px"]) == len(payload["frame_aliases"]), "uncertainty denominator mismatch")
    require(all(type(value) in {int, float} and math.isfinite(value) for value in payload["displacement_px"]), "invalid displacement")
    require(all(type(value) in {int, float} and value >= 0 and math.isfinite(value) for value in payload["uncertainty_px"]), "invalid uncertainty")
    require(payload["diagnosis"] is None, "defect diagnosis is outside scope")
    return {"accepted": True, "sample_count": len(payload["frame_aliases"]), "maximum_absolute_displacement_px": max(abs(v) for v in payload["displacement_px"])}


def sequence_order(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "indices", "allow_declared_gaps")
    indices = payload["indices"]
    require(isinstance(indices, list) and indices, "indices must be a nonempty list")
    require(all(type(value) is int and value >= 0 for value in indices), "indices must be nonnegative integers")
    require(len(set(indices)) == len(indices), "duplicate index refused")
    require(indices == sorted(indices), "reordered sequence refused")
    gaps = [right - left - 1 for left, right in zip(indices, indices[1:]) if right - left > 1]
    require(payload["allow_declared_gaps"] is False and not gaps, "sequence gap refused")
    return {"accepted": True, "frame_count": len(indices), "first": indices[0], "last": indices[-1]}


def color_identity(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "icc_profile_digest", "icc_version", "lut_digest", "encoding", "rendering_intent")
    for key in ("icc_profile_digest", "icc_version", "lut_digest", "encoding", "rendering_intent"):
        require(isinstance(payload[key], str) and payload[key], f"{key} must be nonempty")
    require(payload["icc_profile_digest"] != payload["lut_digest"], "profile and LUT identities must remain distinct")
    require(payload["icc_version"].startswith("4."), "fixture admits only declared ICC v4 vocabulary")
    require(payload["encoding"] in {"scene_linear_synthetic", "display_referred_synthetic"}, "unknown encoding")
    require(payload["rendering_intent"] in {"relative_colorimetric", "absolute_colorimetric", "perceptual", "saturation"}, "unknown rendering intent")
    return {"accepted": True, "identity_sha256": stable_digest(payload), "colorimetric_accuracy_claim": False}


def focus_proxy(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "regions", "scores", "denominator", "threshold_authority")
    require(isinstance(payload["regions"], list) and payload["regions"], "regions must be declared")
    require(isinstance(payload["scores"], list) and len(payload["scores"]) == len(payload["regions"]), "score denominator mismatch")
    require(payload["denominator"] == len(payload["regions"]), "declared denominator mismatch")
    require(all(type(value) in {int, float} and value >= 0 and math.isfinite(value) for value in payload["scores"]), "invalid focus proxy")
    require(payload["threshold_authority"] == "vacant", "professional threshold authority refused")
    return {"accepted": True, "sample_count": len(payload["scores"]), "minimum_proxy": min(payload["scores"]), "release_decision": None}


def correction_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "events", "readback_state")
    events = payload["events"]
    require(isinstance(events, list) and len(events) >= 2, "at least baseline and correction events required")
    ids = [event.get("event_id") for event in events if isinstance(event, dict)]
    require(len(ids) == len(events) and all(isinstance(value, str) and value for value in ids), "event ids required")
    require(len(ids) == len(set(ids)), "event ids must be unique")
    require(events[0].get("kind") == "baseline", "first event must retain baseline")
    require(any(event.get("kind") == "correction" and event.get("supersedes") == events[0]["event_id"] for event in events[1:]), "component-addressed correction required")
    require(payload["readback_state"] in {"synthetic_acknowledged", "synthetic_pending"}, "invalid readback state")
    return {"accepted": True, "event_count": len(events), "baseline_retained": True, "ledger_sha256": stable_digest(events)}


def authority_firewall(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "decisions", "reserved_authorities", "software_decision_count")
    require(isinstance(payload["decisions"], dict) and payload["decisions"], "decision vacancy map required")
    require(all(value == "vacant" for value in payload["decisions"].values()), "authority decision promotion refused")
    require(isinstance(payload["reserved_authorities"], list) and {"professional", "legal", "cultural", "Maori", "affected_party"} <= set(payload["reserved_authorities"]), "required authority reservations missing")
    require(payload["software_decision_count"] == 0, "software may not make reserved decisions")
    return {"accepted": True, "vacancy_count": len(payload["decisions"]), "authority_conferred": False}


CONTROLS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "frame_contract": frame_contract,
    "target_lineage": target_lineage,
    "optical_path": optical_path,
    "registration": registration,
    "motion_proxy": motion_proxy,
    "sequence_order": sequence_order,
    "color_identity": color_identity,
    "focus_proxy": focus_proxy,
    "correction_ledger": correction_ledger,
    "authority_firewall": authority_firewall,
}


def evaluate_control(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    require(name in CONTROLS, "unknown control")
    return CONTROLS[name](payload)


def runner_main(control_name: str) -> int:
    parser = argparse.ArgumentParser(description=f"bounded synthetic {control_name} runner")
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        result = evaluate_control(control_name, payload)
    except (OSError, json.JSONDecodeError, RejectedFixture) as exc:
        print(json.dumps({"accepted": False, "control": control_name, "error_class": type(exc).__name__, "boundary": "synthetic rejection only"}, sort_keys=True))
        return 2
    print(json.dumps({"accepted": True, "control": control_name, "result": result, "boundary": "synthetic acceptance only"}, sort_keys=True))
    return 0
