#!/usr/bin/env python3
"""Bounded runner core for Sylven Arc v665-v5.

Every accepted input is synthetic, zero-row, or typed-formal owner-local
fixture evidence. Acceptance says only that this software guard accepted one
bounded structure. It is not firing advice, professional or empirical
validation, production conformance, legal or cultural authority, Māori
authority, independent reproduction, proof, or Stage 20 evidence.
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
    "kiln_load_capsule": {
        "required": {"ware_tokens", "shelf_coordinates", "cancelled", "provenance_present", "external_action"},
        "ceiling": "synthetic_kiln_load_documentation_only",
    },
    "kiln_clearance_graph": {
        "required": {"nodes", "edges", "overlap_count", "unsupported_span", "clearance_quarantined"},
        "ceiling": "synthetic_clearance_graph_only",
    },
    "glaze_quarantine": {
        "required": {"batch_token", "lot_lineage", "release_state", "safety_sheet_present", "substitution_history", "physical_release"},
        "ceiling": "synthetic_glaze_quarantine_record_only",
    },
    "witness_cone_readback": {
        "required": {"cone_set", "zone_map", "observation_readback", "interpretation_claim", "real_image_present"},
        "ceiling": "synthetic_witness_cone_documentation_only",
    },
    "firing_state_machine": {
        "required": {"states", "transitions", "abort_dominant", "restart_authorized", "real_actuation"},
        "ceiling": "synthetic_firing_state_transitions_only",
    },
    "kiln_command_firewall": {
        "required": {"observation_channel", "command_channel", "live_controller_calls", "operator_authority", "actuation_events"},
        "ceiling": "simulated_observation_no_command_only",
    },
    "thermal_unit_board": {
        "required": {"term_units", "dimensional_balance", "real_measurements", "empirical_fit", "physical_law_claim"},
        "ceiling": "typed_symbolic_thermal_obligation_only",
    },
    "heat_agency_nonconversion": {
        "required": {"thermal_symbols", "agency_inference", "personhood_inference", "ethical_authority"},
        "ceiling": "symbolic_nonconversion_guard_only",
    },
    "epa_worksafe_zero_row": {
        "required": {"artifact_class", "live_data_calls", "real_keys", "real_participants", "external_witness_present", "empirical_gmut_claim", "stage20_authority"},
        "ceiling": "same_owner_zero_row_evidence_only",
    },
    "ceramics_authority_matrix": {
        "required": {"worker_decision", "consumer_decision", "legal_decision", "cultural_decision", "maori_authority", "affected_party_acceptance"},
        "ceiling": "authority_reservation_structure_only",
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
        "unsupported_span",
        "physical_release",
        "interpretation_claim",
        "real_image_present",
        "restart_authorized",
        "real_actuation",
        "operator_authority",
        "empirical_fit",
        "physical_law_claim",
        "agency_inference",
        "personhood_inference",
        "ethical_authority",
        "external_witness_present",
        "empirical_gmut_claim",
        "stage20_authority",
        "worker_decision",
        "consumer_decision",
        "legal_decision",
        "cultural_decision",
        "maori_authority",
        "affected_party_acceptance",
    }
    promoted = sorted(key for key in protected_true if payload.get(key) is True)
    if promoted:
        errors.append("protected_promotion:" + ",".join(promoted))
    for key in (
        "live_controller_calls",
        "actuation_events",
        "real_measurements",
        "live_data_calls",
        "real_keys",
        "real_participants",
    ):
        if isinstance(payload.get(key), int) and payload.get(key, 0) != 0:
            errors.append(f"nonzero_{key}_forbidden")

    if profile == "kiln_load_capsule":
        if payload.get("provenance_present") is not True:
            errors.append("documentary_provenance_required")
        if not isinstance(payload.get("ware_tokens"), list):
            errors.append("ware_tokens_must_be_array")
    elif profile == "kiln_clearance_graph":
        if payload.get("overlap_count") != 0:
            errors.append("overlap_must_be_zero")
        if payload.get("clearance_quarantined") is not True:
            errors.append("clearance_quarantine_required")
    elif profile == "glaze_quarantine":
        if payload.get("release_state") != "held":
            errors.append("glaze_batch_must_remain_held")
        if not isinstance(payload.get("lot_lineage"), list):
            errors.append("lot_lineage_must_be_array")
    elif profile == "witness_cone_readback":
        if payload.get("observation_readback") is not True:
            errors.append("observation_readback_required")
        if not isinstance(payload.get("zone_map"), dict):
            errors.append("zone_map_must_be_object")
    elif profile == "firing_state_machine":
        if payload.get("abort_dominant") is not True:
            errors.append("abort_must_dominate")
        if not isinstance(payload.get("states"), list) or not isinstance(payload.get("transitions"), list):
            errors.append("state_machine_arrays_required")
    elif profile == "kiln_command_firewall":
        if payload.get("command_channel") != "null":
            errors.append("command_channel_must_be_null")
        if payload.get("observation_channel") != "simulated":
            errors.append("observation_channel_must_be_simulated")
    elif profile == "thermal_unit_board":
        if payload.get("dimensional_balance") is not True:
            errors.append("dimensional_balance_required")
        if not isinstance(payload.get("term_units"), dict):
            errors.append("term_units_must_be_object")
    elif profile == "heat_agency_nonconversion":
        if not isinstance(payload.get("thermal_symbols"), list):
            errors.append("thermal_symbols_must_be_array")
    elif profile == "epa_worksafe_zero_row":
        if payload.get("artifact_class") != "official_schema_vocabulary_zero_row":
            errors.append("zero_row_artifact_class_required")
    elif profile == "ceramics_authority_matrix":
        required_false = (
            "worker_decision",
            "consumer_decision",
            "legal_decision",
            "cultural_decision",
            "maori_authority",
            "affected_party_acceptance",
        )
        if any(payload.get(key) is not False for key in required_false):
            errors.append("all_authority_decisions_must_remain_false")

    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        "schema": "ghc.family.sylven.v665-v5.runner-result.v1",
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
            "schema": "ghc.family.sylven.v665-v5.runner-result.v1",
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
