#!/usr/bin/env python3
"""Bounded runner core for Elowen Cairn v665-v4.

All accepted inputs are synthetic, zero-row, or typed-formal owner-local
fixtures. Acceptance is evidence about these software guards only; it is not
professional, empirical, production, legal, cultural, affected-party, Māori,
independent-reproduction, proof, or Stage 20 evidence.
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
    "mosaic_case_capsule": {
        "required": {"panel_token", "component_vacancy", "withdrawal_flag", "external_action"},
        "ceiling": "synthetic_record_structure_only",
    },
    "mosaic_layer_dag": {
        "required": {"node_types", "edges", "acyclic", "cycle_quarantined"},
        "ceiling": "synthetic_stratigraphic_structure_only",
    },
    "mosaic_half_edge": {
        "required": {"half_edges", "twin_complete", "boundary_declared", "nonmanifold_count", "nonmanifold_quarantined"},
        "ceiling": "synthetic_topology_structure_only",
    },
    "mosaic_annotation": {
        "required": {"target_kind", "selector_kind", "coordinate_frame", "real_image_present"},
        "ceiling": "zero_image_annotation_structure_only",
    },
    "mosaic_observation": {
        "required": {"observation_terms", "uncertainty_present", "diagnosis_claim", "treatment_claim", "manual_evaluation_present"},
        "ceiling": "bounded_observation_vocabulary_only",
    },
    "mosaic_material_hold": {
        "required": {"lot_records", "authentication_claim", "tool_release", "destructive_action"},
        "ceiling": "synthetic_material_and_safety_hold_only",
    },
    "mosaic_custody_braid": {
        "required": {"events", "erasure_count", "disputed_handover_held", "authority_decision"},
        "ceiling": "synthetic_custody_and_correction_structure_only",
    },
    "dec_chain_complex": {
        "required": {"ambient_dimension", "chain_dimension", "coefficient_domain", "oriented_incidence", "boundary_squared_zero", "theorem_claim"},
        "ceiling": "typed_formal_obligation_only",
    },
    "dec_hodge_obligations": {
        "required": {"ambient_dimension", "primal_degree", "dual_degree", "metric_placeholder", "positivity_claim", "convergence_claim", "theorem_claim"},
        "ceiling": "typed_formal_obligation_only",
    },
    "evidence_credit_firewall": {
        "required": {"artifact_class", "live_data_calls", "real_keys", "real_participants", "external_witness_present", "empirical_gmut_claim", "stage20_authority"},
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
        "external_action",
        "real_image_present",
        "diagnosis_claim",
        "treatment_claim",
        "manual_evaluation_present",
        "authentication_claim",
        "tool_release",
        "destructive_action",
        "authority_decision",
        "theorem_claim",
        "positivity_claim",
        "convergence_claim",
        "external_witness_present",
        "empirical_gmut_claim",
        "stage20_authority",
    }
    promoted = sorted(key for key in protected_true if payload.get(key) is True)
    if promoted:
        errors.append("protected_promotion:" + ",".join(promoted))
    for key in ("live_data_calls", "real_keys", "real_participants"):
        if isinstance(payload.get(key), int) and payload.get(key, 0) != 0:
            errors.append(f"nonzero_{key}_forbidden")

    if profile == "mosaic_case_capsule":
        if payload.get("component_vacancy") is not True:
            errors.append("component_vacancy_required")
        if payload.get("withdrawal_flag") is not True:
            errors.append("withdrawal_flag_required")
    elif profile == "mosaic_layer_dag":
        if payload.get("acyclic") is not True:
            errors.append("layer_dag_must_be_acyclic")
        if payload.get("cycle_quarantined") is not True:
            errors.append("cycle_quarantine_required")
    elif profile == "mosaic_half_edge":
        if payload.get("twin_complete") is not True or payload.get("boundary_declared") is not True:
            errors.append("half_edge_topology_incomplete")
        if payload.get("nonmanifold_count") != 0 or payload.get("nonmanifold_quarantined") is not True:
            errors.append("nonmanifold_state_must_be_quarantined")
    elif profile == "mosaic_annotation":
        if not payload.get("selector_kind") or not payload.get("coordinate_frame"):
            errors.append("selector_and_coordinate_frame_required")
    elif profile == "mosaic_observation":
        if payload.get("uncertainty_present") is not True:
            errors.append("uncertainty_required")
    elif profile == "mosaic_material_hold":
        if not isinstance(payload.get("lot_records"), list):
            errors.append("lot_records_must_be_array")
    elif profile == "mosaic_custody_braid":
        if payload.get("erasure_count") != 0:
            errors.append("correction_erasure_forbidden")
        if payload.get("disputed_handover_held") is not True:
            errors.append("disputed_handover_hold_required")
    elif profile == "dec_chain_complex":
        ambient = payload.get("ambient_dimension")
        degree = payload.get("chain_dimension")
        if not all(isinstance(v, int) for v in (ambient, degree)):
            errors.append("chain_dimensions_must_be_integers")
        elif not (0 <= degree <= ambient):
            errors.append("chain_dimension_relation_invalid")
        if payload.get("oriented_incidence") is not True:
            errors.append("oriented_incidence_required")
        if payload.get("boundary_squared_zero") is not True:
            errors.append("boundary_squared_zero_required")
    elif profile == "dec_hodge_obligations":
        ambient = payload.get("ambient_dimension")
        primal = payload.get("primal_degree")
        dual = payload.get("dual_degree")
        if not all(isinstance(v, int) for v in (ambient, primal, dual)):
            errors.append("hodge_degrees_must_be_integers")
        elif not (0 <= primal <= ambient and dual == ambient - primal):
            errors.append("hodge_degree_relation_invalid")

    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        "schema": "ghc.family.elowen.v665-v4.runner-result.v1",
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
            "schema": "ghc.family.elowen.v665-v4.runner-result.v1",
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
