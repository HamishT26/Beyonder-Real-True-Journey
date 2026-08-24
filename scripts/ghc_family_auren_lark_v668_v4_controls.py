#!/usr/bin/env python3
"""Bounded synthetic microscope-slide calibration controls for Auren Lark v668-v4 x2."""

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
    "tile_contract",
    "slide_lineage",
    "optical_path",
    "registration",
    "z_plane_order",
    "tile_coverage",
    "color_attachment",
    "focus_measure",
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
    require(payload["owner"] == "Auren Lark", "wrong owner")
    require(payload["phase"] == "v668-v4", "wrong phase")
    require(isinstance(payload["proposal_id"], str) and payload["proposal_id"].startswith("AL6684-N"), "invalid proposal id")
    require(payload["expected_disposition"] in {"completed", "represented", "open_gap", "exact_gate"}, "invalid outcome vocabulary")
    require(isinstance(payload["protected_claims"], dict), "protected claims must be an object")
    require(payload["protected_claims"] and all(value is False for value in payload["protected_claims"].values()), "protected claim promotion refused")
    require(payload["authority_override"] is False, "authority override refused")
    return {"accepted": True, "proposal_id": payload["proposal_id"], "envelope_sha256": stable_digest(payload)}


def tile_contract(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(
        payload,
        "total_rows_px",
        "total_columns_px",
        "tile_row_px",
        "tile_column_px",
        "tile_height_px",
        "tile_width_px",
    )
    for key in (
        "total_rows_px",
        "total_columns_px",
        "tile_row_px",
        "tile_column_px",
        "tile_height_px",
        "tile_width_px",
    ):
        require(type(payload[key]) is int, f"{key} must be an integer")
    require(payload["total_rows_px"] > 0 and payload["total_columns_px"] > 0, "matrix dimensions must be positive")
    require(payload["tile_height_px"] > 0 and payload["tile_width_px"] > 0, "tile dimensions must be positive")
    require(payload["tile_row_px"] >= 0 and payload["tile_column_px"] >= 0, "tile origin must be nonnegative")
    row_end = payload["tile_row_px"] + payload["tile_height_px"]
    column_end = payload["tile_column_px"] + payload["tile_width_px"]
    require(row_end <= payload["total_rows_px"] and column_end <= payload["total_columns_px"], "tile exceeds declared matrix")
    return {
        "accepted": True,
        "tile_bounds": [payload["tile_row_px"], payload["tile_column_px"], row_end, column_end],
        "matrix_bounds": [payload["total_rows_px"], payload["total_columns_px"]],
    }


def slide_lineage(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "slide_alias", "lot_alias", "target_region_alias", "status", "valid_from", "valid_until", "session_alias")
    fields = ("slide_alias", "lot_alias", "target_region_alias", "valid_from", "valid_until", "session_alias")
    require(all(isinstance(payload[key], str) and payload[key] for key in fields), "lineage strings must be nonempty")
    require(payload["status"] == "synthetic_current", "stale or unresolved synthetic slide refused")
    require(payload["valid_from"] < payload["valid_until"], "invalid validity interval")
    return {"accepted": True, "lineage_sha256": stable_digest(payload), "authority": "vacant"}


def optical_path(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "objective_alias", "illumination_alias", "filter_alias", "sensor_alias", "stage_alias")
    fields = [payload[key] for key in ("objective_alias", "illumination_alias", "filter_alias", "sensor_alias", "stage_alias")]
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


def z_plane_order(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "plane_aliases", "z_offsets_um", "local_context_only", "absolute_depth_claim")
    aliases = payload["plane_aliases"]
    offsets = payload["z_offsets_um"]
    require(isinstance(aliases, list) and len(aliases) >= 3, "at least three focal-plane aliases required")
    require(len(set(aliases)) == len(aliases), "focal-plane aliases must be unique")
    require(isinstance(offsets, list) and len(offsets) == len(aliases), "Z-offset denominator mismatch")
    require(all(type(value) in {int, float} and math.isfinite(value) for value in offsets), "invalid Z offset")
    require(offsets == sorted(offsets) and len(set(offsets)) == len(offsets), "Z offsets must be strictly ordered")
    require(payload["local_context_only"] is True, "Z offsets must remain local-context values")
    require(payload["absolute_depth_claim"] is False, "absolute specimen-depth claim refused")
    return {"accepted": True, "plane_count": len(aliases), "z_span_um": offsets[-1] - offsets[0], "absolute_depth_claim": False}


def tile_coverage(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "declared_rows", "declared_columns", "coordinates", "allow_sparse")
    require(type(payload["declared_rows"]) is int and payload["declared_rows"] > 0, "declared rows must be positive")
    require(type(payload["declared_columns"]) is int and payload["declared_columns"] > 0, "declared columns must be positive")
    coordinates = payload["coordinates"]
    require(isinstance(coordinates, list) and coordinates, "tile coordinates must be a nonempty list")
    require(all(isinstance(pair, list) and len(pair) == 2 and all(type(value) is int for value in pair) for pair in coordinates), "tile coordinates must be integer pairs")
    tuples = [tuple(pair) for pair in coordinates]
    require(len(tuples) == len(set(tuples)), "duplicate tile coordinate refused")
    expected = {(row, column) for row in range(payload["declared_rows"]) for column in range(payload["declared_columns"])}
    require(set(tuples) <= expected, "out-of-bounds tile coordinate refused")
    require(payload["allow_sparse"] is False and set(tuples) == expected, "tile gap or sparse coverage refused")
    return {"accepted": True, "tile_count": len(tuples), "complete_coverage": True}


def color_attachment(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "profile_digest", "declared_revision", "lookup_digest", "encoding", "rendering_intent")
    for key in ("profile_digest", "declared_revision", "lookup_digest", "encoding", "rendering_intent"):
        require(isinstance(payload[key], str) and payload[key], f"{key} must be nonempty")
    require(len(payload["profile_digest"]) == 64 and len(payload["lookup_digest"]) == 64, "attachment digests must be 64 characters")
    require(payload["profile_digest"] != payload["lookup_digest"], "profile and lookup identities must remain distinct")
    require(payload["declared_revision"].startswith("synthetic-"), "only a declared synthetic revision is admitted")
    require(payload["encoding"] in {"synthetic_scene_linear", "synthetic_display_referred"}, "unknown encoding")
    require(payload["rendering_intent"] in {"relative_colorimetric", "absolute_colorimetric", "perceptual", "saturation"}, "unknown rendering intent")
    return {"accepted": True, "identity_sha256": stable_digest(payload), "colorimetric_accuracy_claim": False}


def focus_measure(payload: dict[str, Any]) -> dict[str, Any]:
    require_keys(payload, "tile_aliases", "plane_aliases", "scores", "denominator", "metric_revision", "threshold_authority")
    require(isinstance(payload["tile_aliases"], list) and payload["tile_aliases"], "tile aliases must be declared")
    require(isinstance(payload["plane_aliases"], list) and len(payload["plane_aliases"]) == len(payload["tile_aliases"]), "plane denominator mismatch")
    require(isinstance(payload["scores"], list) and len(payload["scores"]) == len(payload["tile_aliases"]), "score denominator mismatch")
    require(payload["denominator"] == len(payload["tile_aliases"]), "declared denominator mismatch")
    require(all(type(value) in {int, float} and value >= 0 and math.isfinite(value) for value in payload["scores"]), "invalid focus proxy")
    require(isinstance(payload["metric_revision"], str) and payload["metric_revision"].startswith("synthetic-"), "metric revision must remain synthetic")
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
    "tile_contract": tile_contract,
    "slide_lineage": slide_lineage,
    "optical_path": optical_path,
    "registration": registration,
    "z_plane_order": z_plane_order,
    "tile_coverage": tile_coverage,
    "color_attachment": color_attachment,
    "focus_measure": focus_measure,
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
