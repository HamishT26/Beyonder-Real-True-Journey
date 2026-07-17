#!/usr/bin/env python3
"""Bounded structural runtime for Orin Thale v647-v8 proposal surfaces."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


BOUNDARY = (
    "Synthetic, symbolic, structural, or zero-row evidence only. It is not empirical GMUT confirmation, "
    "THOS effectiveness, production identity assurance, legal or cultural authority, Māori authority, "
    "complete accessibility, exhaustive security, independent reproduction, or Stage 20 readiness."
)


def spec(proposal_id: str, outcome: str, obligations: list[str], scope: str) -> dict[str, Any]:
    return {"proposal_id": proposal_id, "outcome": outcome, "obligations": obligations, "scope": scope}


SURFACES = {
    "log_rotation": spec("V6478-P01", "completed", [
        "file_identity_recorded", "rename_rotation_distinguished", "copytruncate_detected",
        "checkpoint_continuity_checked", "duplicate_rejected", "gap_quarantined", "ambiguous_credit_denied",
    ], "disposable synthetic log-rotation fixtures"),
    "os_reflection": spec("V6478-P02", "completed", [
        "euclidean_covariance_declared", "reflection_positivity_required", "reconstruction_domain_declared",
        "truncation_disclosed", "eft_domain_preserved", "units_preserved", "observation_firewall_closed",
    ], "typed symbolic Osterwalder-Schrader obligations"),
    "gwosc_o3": spec("V6478-P03", "open_gap", [
        "release_identity_frozen", "strain_schema_declared", "event_metadata_required",
        "calibration_required", "data_quality_required", "waveform_nuisance_required", "likelihood_refuses_zero_rows",
    ], "official-format zero-row GWOSC O3 readiness contract"),
    "diving_handover": spec("V6478-P04", "represented", [
        "dive_plan_required", "supervisor_and_lookout_separated", "permit_state_explicit",
        "stop_work_fail_closed", "decompression_readiness_required", "emergency_readiness_required", "next_owner_and_budget_bound",
    ], "synthetic occupational-diving plan and handover traces"),
    "http_signatures": spec("V6478-P05", "represented", [
        "covered_components_explicit", "derived_components_bounded", "signature_parameters_bound",
        "nonce_checked", "created_and_expires_checked", "key_resolution_reserved", "privacy_and_replay_reserved",
    ], "synthetic RFC 9421 structural vectors"),
    "diving_authority": spec("V6478-P06", "exact_gate", [
        "incident_meaning_reserved", "medical_privacy_reserved", "income_and_remedy_reserved",
        "accessibility_reserved", "affected_party_acceptance_reserved", "legal_and_cultural_meaning_reserved", "maori_authority_reserved",
    ], "refusal-first occupational-diving authority matrix"),
    "wasm_binary": spec("V6478-P07", "completed", [
        "magic_and_version_checked", "leb128_canonical", "section_order_checked",
        "index_bounds_checked", "custom_section_bounded", "resource_budget_bounded", "module_execution_forbidden",
    ], "disposable synthetic WebAssembly byte fixtures"),
    "session_expiry": spec("V6478-P08", "completed", [
        "warning_present", "extension_available", "data_loss_prevented",
        "reauthentication_path_present", "focus_persists", "status_exposed", "keyboard_path_complete",
    ], "structural session-expiry accessibility fixtures"),
    "maxwell": spec("V6478-P09", "completed", [
        "equal_area_domain_declared", "coexistence_condition_declared", "spinodal_distinguished",
        "metastability_distinguished", "units_preserved", "phase_domain_scoped", "agency_nonconversion_enforced",
    ], "typed thermodynamic Maxwell-construction fixtures"),
    "rdd": spec("V6478-P10", "completed", [
        "running_variable_declared", "cutoff_preregistered", "manipulation_check_required",
        "bandwidth_declared", "continuity_assumptions_declared", "falsification_required", "stage20_nonpromotion_enforced",
    ], "structural regression-discontinuity governance fixtures"),
}


def baseline(surface: str) -> dict[str, Any]:
    item = SURFACES[surface]
    return {
        "surface": surface,
        "proposal_id": item["proposal_id"],
        "outcome": item["outcome"],
        "scope": item["scope"],
        "obligations": {name: True for name in item["obligations"]},
        "real_rows": 0,
        "likelihood_calls": 0,
        "posterior_samples": 0,
        "real_people_or_operations": 0,
        "real_keys_tokens_or_servers": 0,
        "authority_decisions": 0,
        "network_actions": 0,
        "production_claim": False,
        "stage20_ready": False,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }


def accepts(surface: str, fixture: dict[str, Any]) -> tuple[bool, list[str]]:
    item = SURFACES[surface]
    reasons = []
    if fixture.get("proposal_id") != item["proposal_id"] or fixture.get("outcome") != item["outcome"]:
        reasons.append("proposal_or_outcome_mismatch")
    obligations = fixture.get("obligations", {})
    for name in item["obligations"]:
        if obligations.get(name) is not True:
            reasons.append(f"obligation_failed:{name}")
    for field in ("real_rows", "likelihood_calls", "posterior_samples", "real_people_or_operations", "real_keys_tokens_or_servers", "authority_decisions", "network_actions"):
        if fixture.get(field) != 0:
            reasons.append(f"nonzero_reserved_counter:{field}")
    for field in ("production_claim", "stage20_ready", "independent_reproduction"):
        if fixture.get(field) is not False:
            reasons.append(f"forbidden_promotion:{field}")
    return not reasons, reasons


def surface_evidence(surface: str) -> dict[str, Any]:
    item = SURFACES[surface]
    valid = baseline(surface)
    valid_ok, valid_reasons = accepts(surface, valid)
    mutations = []
    for index, obligation in enumerate(item["obligations"], 1):
        mutated = copy.deepcopy(valid)
        mutated["obligations"][obligation] = False
        accepted, reasons = accepts(surface, mutated)
        mutations.append({
            "negative_id": f"V6478-SYN-{int(item['proposal_id'][-2:]):02d}-{index:02d}",
            "surface": surface,
            "mutated_obligation": obligation,
            "accepted": accepted,
            "rejected": not accepted,
            "retained": True,
            "reasons": reasons,
            "scientific_or_production_credit": False,
        })
    return {
        "schema": "ghc.family.v647-v8.surface-evidence.v1",
        "surface": surface,
        "proposal_id": item["proposal_id"],
        "outcome": item["outcome"],
        "scope": item["scope"],
        "valid_fixture_passed": valid_ok,
        "valid_fixture_reasons": valid_reasons,
        "valid_fixture": valid,
        "rejected_mutation_count": sum(row["rejected"] for row in mutations),
        "mutations": mutations,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }


def emit_surface(surface: str, output: str | Path) -> dict[str, Any]:
    payload = surface_evidence(surface)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return payload
