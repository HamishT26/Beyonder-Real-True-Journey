#!/usr/bin/env python3
"""Bounded shared runner core for Tamar Vey v665-v3.

All accepted inputs are synthetic or formal owner-local fixtures.  Acceptance
is evidence about this software guard only; it is never professional,
empirical, production, legal, cultural, or Stage 20 evidence.
"""

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
    "fossil_case_capsule": {
        "required": {"surrogate_case", "accession_present", "source_snapshot", "object_action"},
        "ceiling": "synthetic_record_structure_only",
    },
    "fossil_relation_graph": {
        "required": {"node_types", "edges", "orphan_count", "contradictions_quarantined"},
        "ceiling": "synthetic_relation_structure_only",
    },
    "observation_vocabulary": {
        "required": {"observation_terms", "uncertainty_present", "diagnosis_claim", "manual_evaluation_present"},
        "ceiling": "bounded_vocabulary_and_accessibility_structure",
    },
    "treatment_and_tool_hold": {
        "required": {"lot_records", "compatibility_evidence_present", "treatment_release", "destructive_action"},
        "ceiling": "synthetic_hold_structure_only",
    },
    "correction_and_handover": {
        "required": {"events", "erasure_count", "dual_readback_present", "operational_handover"},
        "ceiling": "synthetic_correction_and_handover_structure",
    },
    "de_rham_current": {
        "required": {"ambient_dimension", "current_dimension", "test_form_degree", "orientation_declared", "support_kind", "boundary_dimension", "boundary_of_boundary_formally_zero"},
        "ceiling": "typed_formal_obligation_only",
    },
    "current_norm": {
        "required": {"mass_symbol", "comass_bound", "flat_norm_decomposition", "coefficient_group", "unit_domain", "compactness_theorem_claim"},
        "ceiling": "typed_formal_obligation_only",
    },
    "rectifiable_current": {
        "required": {"ambient_dimension", "current_dimension", "multiplicity_kind", "carrier_kind", "tangent_plane_dimension", "closure_theorem_claim"},
        "ceiling": "typed_formal_obligation_only",
    },
    "varifold_obligations": {
        "required": {"ambient_dimension", "varifold_dimension", "weight_measure_placeholder", "grassmannian_fibre", "first_variation_symbol", "stationarity_claim", "regularity_theorem_claim"},
        "ceiling": "typed_formal_obligation_only",
    },
    "evidence_credit_firewall": {
        "required": {"artifact_class", "live_data_calls", "real_keys", "real_participants", "external_witness_present", "stage20_authority"},
        "ceiling": "same_owner_zero_row_evidence_only",
    },
}


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def evaluate(profile: str, payload: Any) -> dict[str, Any]:
    errors: list[str] = []
    spec = PROFILES.get(profile)
    if spec is None:
        errors.append("unknown_profile")
        spec = {"required": set(), "ceiling": "none"}
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

    protected_true = {
        "object_action",
        "diagnosis_claim",
        "manual_evaluation_present",
        "treatment_release",
        "destructive_action",
        "dual_readback_present",
        "operational_handover",
        "compactness_theorem_claim",
        "closure_theorem_claim",
        "stationarity_claim",
        "regularity_theorem_claim",
        "external_witness_present",
        "stage20_authority",
    }
    promoted = sorted(key for key in protected_true if payload.get(key) is True)
    if promoted:
        errors.append("protected_promotion:" + ",".join(promoted))
    for key in ("live_data_calls", "real_keys", "real_participants"):
        if isinstance(payload.get(key), int) and payload.get(key, 0) != 0:
            errors.append(f"nonzero_{key}_forbidden")
    if payload.get("accession_present") not in (None, False):
        errors.append("real_accession_forbidden")
    if isinstance(payload.get("orphan_count"), int) and payload.get("orphan_count") != 0:
        errors.append("orphans_must_be_quarantined")
    if payload.get("contradictions_quarantined") not in (None, True):
        errors.append("contradiction_quarantine_required")
    if payload.get("erasure_count") not in (None, 0):
        errors.append("correction_erasure_forbidden")
    if profile == "de_rham_current":
        ambient = payload.get("ambient_dimension")
        current = payload.get("current_dimension")
        form = payload.get("test_form_degree")
        boundary = payload.get("boundary_dimension")
        if not all(isinstance(v, int) for v in (ambient, current, form, boundary)):
            errors.append("current_dimensions_must_be_integers")
        elif not (0 < current <= ambient and form == current and boundary == current - 1):
            errors.append("current_dimension_relation_invalid")
        if payload.get("boundary_of_boundary_formally_zero") is not True:
            errors.append("boundary_of_boundary_obligation_missing")
    if profile == "rectifiable_current":
        ambient = payload.get("ambient_dimension")
        current = payload.get("current_dimension")
        tangent = payload.get("tangent_plane_dimension")
        if not all(isinstance(v, int) for v in (ambient, current, tangent)):
            errors.append("rectifiable_dimensions_must_be_integers")
        elif not (0 < current <= ambient and tangent == current):
            errors.append("rectifiable_dimension_relation_invalid")
    if profile == "varifold_obligations":
        ambient = payload.get("ambient_dimension")
        varifold = payload.get("varifold_dimension")
        if not all(isinstance(v, int) for v in (ambient, varifold)):
            errors.append("varifold_dimensions_must_be_integers")
        elif not (0 < varifold <= ambient):
            errors.append("varifold_dimension_relation_invalid")

    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        "schema": "ghc.family.tamar.v665-v3.runner-result.v1",
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
            "schema": "ghc.family.tamar.v665-v3.runner-result.v1",
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
