#!/usr/bin/env python3
"""Bounded v648-v8 contract runtime.

The runtime validates synthetic dictionaries only. It performs no network,
participant, credential, professional, production, or authority action.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DISPOSITIONS = {
    "V6488-P01": "completed",
    "V6488-P02": "completed",
    "V6488-P03": "open_gap",
    "V6488-P04": "represented",
    "V6488-P05": "represented",
    "V6488-P06": "exact_gate",
    "V6488-P07": "completed",
    "V6488-P08": "completed",
    "V6488-P09": "completed",
    "V6488-P10": "completed",
}


SPECS: dict[str, dict[str, list[str]]] = {
    "V6488-P01": {"required": ["predicate_initialized", "wait_in_loop", "notify_under_lock", "deadline_bounded", "cancellation_checked", "teardown_joined", "partial_credit_refused"], "zero": ["external_action_count", "leaked_worker_count"]},
    "V6488-P02": {"required": ["isolated_mass_shell", "almost_local_operator", "disjoint_velocity_support", "asymptotic_limit_typed", "scattering_state_formal", "gauge_scope", "eft_scope", "units_typed", "observation_firewall"], "zero": ["external_action_count", "physical_prediction_count", "empirical_claim_count"]},
    "V6488-P03": {"required": ["release_identity", "field_identity", "component_source_separated", "beam_provenance", "astrometry_schema", "flux_scale_schema", "completeness_schema", "covariance_schema", "checksum_required", "zero_row_lock"], "zero": ["external_action_count", "query_count", "download_count", "real_row_count", "catalogue_match_count", "likelihood_call_count", "posterior_sample_count", "constraint_count", "empirical_claim_count"]},
    "V6488-P04": {"required": ["intake_identity", "treatment_train_state", "backwash_state", "turbidity_alarm_owner", "disinfectant_alarm_owner", "sample_custody", "isolation_state", "escalation_owner", "accessible_notice", "workload_budget", "readback", "next_shift_owner"], "zero": ["external_action_count", "real_operator_count", "real_supplier_count", "real_incident_count", "effectiveness_estimate_count"]},
    "V6488-P05": {"required": ["absolute_resource_uri", "fragment_refused", "authorization_binding", "token_request_binding", "multiple_resource_policy", "audience_restriction", "downscope_only", "refresh_no_broadening", "confused_deputy_refused", "replay_refused", "minimization"], "zero": ["external_action_count", "real_key_count", "real_token_count", "live_service_count", "interoperability_event_count", "privacy_review_count", "security_review_count"]},
    "V6488-P06": {"required": ["incident_classified", "privacy_minimized", "notice_accessibility_reserved", "remedy_reserved", "affected_party_reserved", "legal_reserved", "cultural_reserved", "data_governance_reserved", "maori_authority_reserved"], "zero": ["external_action_count", "real_notice_count", "real_disclosure_count", "remedy_allocation_count", "authority_decision_count"]},
    "V6488-P07": {"required": ["section_header", "byte_order_magic", "block_length_mirror", "interface_description", "interface_reference", "option_padding", "timestamp_resolution", "unknown_block_policy", "resource_budget"], "zero": ["external_action_count", "real_packet_count"]},
    "V6488-P08": {"required": ["accessible_name", "value_now", "min_max", "value_text_rule", "keyboard_contract", "direct_edit_contract", "invalid_state", "focus_retention", "touch_alternative", "native_fallback", "print_linearization", "manual_evaluation_reserved"], "zero": ["external_action_count", "manual_evaluation_count", "affected_user_evaluation_count"]},
    "V6488-P09": {"required": ["heat_flux", "mass_flux", "temperature_gradient", "chemical_gradient", "coefficient_matrix", "reference_frame", "sign_convention", "units", "linear_domain", "boundary_conditions", "category_barrier"], "zero": ["external_action_count", "participant_row_count", "psyche_claim_count"]},
    "V6488-P10": {"required": ["target_population", "propensity_model", "positivity", "balance_diagnostics", "estimand", "weight_distribution", "uncertainty", "sensitivity", "falsification", "nonpromotion"], "zero": ["external_action_count", "participant_row_count", "effect_estimate_count", "stage20_promotion_count"]},
}


def valid_fixture(proposal_id: str) -> dict[str, Any]:
    spec = SPECS[proposal_id]
    payload: dict[str, Any] = {name: True for name in spec["required"]}
    payload.update({name: 0 for name in spec["zero"]})
    payload.update({
        "proposal_id": proposal_id,
        "expected_disposition": DISPOSITIONS[proposal_id],
        "boundary": "bounded synthetic or formal evidence only",
        "claim": "none",
        "authority_decision": "reserved" if proposal_id == "V6488-P06" else "none",
    })
    return payload


def mutated_fixture(proposal_id: str, mutation_index: int) -> dict[str, Any]:
    payload = deepcopy(valid_fixture(proposal_id))
    required = SPECS[proposal_id]["required"]
    zero = SPECS[proposal_id]["zero"]
    if mutation_index == 1:
        payload.pop(required[0])
    elif mutation_index == 2:
        payload[required[1]] = False
    elif mutation_index == 3:
        payload["boundary"] = ""
    elif mutation_index == 4:
        payload[zero[0]] = 1
    elif mutation_index == 5:
        payload["claim"] = "forbidden_promotion"
    elif mutation_index == 6:
        payload["expected_disposition"] = "represented" if DISPOSITIONS[proposal_id] != "represented" else "completed"
    elif mutation_index == 7:
        payload["authority_decision"] = "automatic_real_decision"
    else:
        raise ValueError("mutation index must be 1..7")
    return payload


def evaluate(proposal_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    if proposal_id not in SPECS:
        return {"accepted": False, "violations": ["unknown_proposal"], "proposal_id": proposal_id}
    spec = SPECS[proposal_id]
    violations: list[str] = []
    for field in spec["required"]:
        if payload.get(field) is not True:
            violations.append(f"required:{field}")
    for field in spec["zero"]:
        if payload.get(field) != 0:
            violations.append(f"zero:{field}")
    if not isinstance(payload.get("boundary"), str) or not payload["boundary"].strip():
        violations.append("boundary")
    if payload.get("claim") != "none":
        violations.append("claim_promotion")
    if payload.get("expected_disposition") != DISPOSITIONS[proposal_id]:
        violations.append("disposition_mismatch")
    if payload.get("authority_decision") not in {"none", "reserved"}:
        violations.append("authority_promotion")
    return {
        "schema": "ghc.family.v648-v8.runtime-result.v1",
        "proposal_id": proposal_id,
        "accepted": not violations,
        "violations": violations,
        "disposition": DISPOSITIONS[proposal_id],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded synthetic/formal validation only; no external authority or reality claim.",
    }


def cli_for(proposal_id: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.fixture.read_text(encoding="utf-8"))
    result = evaluate(proposal_id, payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("proposal_id", choices=sorted(SPECS))
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.proposal_id, json.loads(args.fixture.read_text(encoding="utf-8"))), sort_keys=True))
