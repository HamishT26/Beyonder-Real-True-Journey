#!/usr/bin/env python3
"""Shared bounded core for Liora Venn v665-v2 family-compatible runners."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
BASE_REQUIRED = {
    "schema",
    "proposal_id",
    "synthetic",
    "real_rows",
    "authority_events",
    "claim_ceiling",
    "terminal_verdict",
    "source_ids",
}
PROFILES: dict[str, dict[str, Any]] = {
    "formal_pde_tableau": {"required": {"symbol_tableau", "jet_order", "equation_rows"}, "ceiling": "formal_structure_only"},
    "spencer_delta_complex": {"required": {"bidegree", "symbol_module", "cohomology_computed"}, "ceiling": "formal_structure_only"},
    "prolongation_lineage": {"required": {"prolongation_steps", "rank_claim", "formal_solution_claim"}, "ceiling": "formal_structure_only"},
    "compatibility_operator": {"required": {"equation_operator", "compatibility_conditions", "exactness_proved"}, "ceiling": "formal_structure_only"},
    "passage_capsule": {"required": {"surrogate_voyage", "waypoints", "navigation_release"}, "ceiling": "synthetic_record_only"},
    "nautical_provenance": {"required": {"chart_cells", "issuing_authority_present", "licence_cleared"}, "ceiling": "vocabulary_and_vacancy_only"},
    "tidal_window_hold": {"required": {"water_level_rows", "forecast_rows", "sailing_decision"}, "ceiling": "synthetic_record_only"},
    "watch_log_braid": {"required": {"events", "dual_readback_present", "operational_handover"}, "ceiling": "synthetic_record_only"},
    "accessible_watchboard": {"required": {"semantic_regions", "manual_evaluation_present", "accessibility_complete"}, "ceiling": "bounded_accessibility_evidence"},
    "evidence_credit_firewall": {"required": {"artifact_class", "external_witness_present", "stage20_authority"}, "ceiling": "same_owner_evidence_only"},
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def evaluate(profile: str, payload: Any) -> dict[str, Any]:
    errors: list[str] = []
    if profile not in PROFILES:
        errors.append("unknown_profile")
        spec = {"required": set(), "ceiling": "none"}
    else:
        spec = PROFILES[profile]
    if not isinstance(payload, dict):
        errors.append("payload_not_object")
        payload = {}
    missing = sorted((BASE_REQUIRED | set(spec["required"])) - set(payload))
    if missing:
        errors.append("missing_required:" + ",".join(missing))
    if payload.get("synthetic") is not True:
        errors.append("synthetic_marker_required")
    if payload.get("real_rows") != 0:
        errors.append("real_rows_forbidden")
    if payload.get("authority_events") != 0:
        errors.append("authority_events_forbidden")
    if payload.get("terminal_verdict") != TERMINAL_VERDICT:
        errors.append("terminal_verdict_must_remain_not_ready")
    if payload.get("claim_ceiling") != spec["ceiling"]:
        errors.append("claim_ceiling_mismatch")
    if not isinstance(payload.get("source_ids"), list) or not payload.get("source_ids"):
        errors.append("source_ids_required")

    promotion_truths = {
        "navigation_release",
        "issuing_authority_present",
        "licence_cleared",
        "sailing_decision",
        "dual_readback_present",
        "operational_handover",
        "manual_evaluation_present",
        "accessibility_complete",
        "external_witness_present",
        "stage20_authority",
        "cohomology_computed",
        "exactness_proved",
        "formal_solution_claim",
    }
    promoted = sorted(key for key in promotion_truths if payload.get(key) is True)
    if promoted:
        errors.append("protected_promotion:" + ",".join(promoted))
    if isinstance(payload.get("equation_rows"), int) and payload.get("equation_rows", 0) > 0:
        errors.append("nonzero_equation_rows_outside_scope")
    for key in ("chart_cells", "water_level_rows", "forecast_rows"):
        if isinstance(payload.get(key), int) and payload.get(key, 0) > 0:
            errors.append(f"nonzero_{key}_outside_scope")
    if isinstance(payload.get("waypoints"), list) and any(not str(v).startswith("SYN-") for v in payload["waypoints"]):
        errors.append("nonsurrogate_waypoint")

    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        "schema": "ghc.family.liora.v665-v2.runner-result.v1",
        "profile": profile,
        "proposal_id": payload.get("proposal_id"),
        "input_sha256": digest,
        "valid": not errors,
        "decision": "accepted_bounded_fixture" if not errors else "rejected",
        "errors": errors,
        "claim_ceiling": spec["ceiling"],
        "terminal_verdict": TERMINAL_VERDICT,
        "real_rows_processed": 0,
        "authority_events_processed": 0,
    }


def run_cli(profile: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes() if args.input else sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode("utf-8"))
        result = evaluate(profile, payload)
    except Exception as exc:
        result = {
            "schema": "ghc.family.liora.v665-v2.runner-result.v1",
            "profile": profile,
            "valid": False,
            "decision": "rejected",
            "errors": [f"invalid_utf8_or_json:{type(exc).__name__}"],
            "terminal_verdict": TERMINAL_VERDICT,
            "real_rows_processed": 0,
            "authority_events_processed": 0,
        }
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0 if result["valid"] else 2
