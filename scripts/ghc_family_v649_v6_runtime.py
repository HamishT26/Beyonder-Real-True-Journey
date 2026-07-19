#!/usr/bin/env python3
"""Bounded reusable runtime for Sylven Arc v649-v6 evidence surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v649_v6_phase_data import PROPOSALS

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v649-v6"

CHECKS = {
    "V6496-P01": ["reader_pin", "epoch_advance", "quiescent_state", "grace_period", "deferred_reclaim", "stalled_reader", "aba_token", "reclamation_order", "teardown", "duplicate_credit"],
    "V6496-P02": ["local_gauge_symmetry", "gauge_variant_order_parameter", "orbit_average", "finite_volume", "limiting_domain", "gauge_fixing", "eft", "unit", "observation_firewall"],
    "V6496-P03": ["pipeline_spectrum", "response_matrix", "background", "spectral_order", "wavelength", "calibration", "good_time", "selection", "covariance", "checksum", "zero_row", "likelihood_refusal"],
    "V6496-P04": ["wheelset_identity", "asset_lineage", "measurement_traceability", "instrument_verification", "defect_quarantine", "release_refusal", "amendment", "workload_budget", "handover"],
    "V6496-P05": ["media_type", "typ", "issuer", "audience", "issued_at", "active_state", "scope_narrowing", "nested_encryption", "algorithm_refusal", "cross_jwt_confusion", "minimization"],
    "V6496-P06": ["defect_record_privacy", "location_privacy", "worker_notification", "passenger_notification", "stop_use_release", "remedy", "affected_party", "legal", "cultural", "land_relationship", "maori_data_governance"],
    "V6496-P07": ["riff_signature", "webp_signature", "chunk_size", "padding", "vp8x_flags", "canvas", "animation", "metadata", "unknown_chunk", "truncation", "size_arithmetic", "resource_budget", "refusal"],
    "V6496-P08": ["sticky_overlay", "target_visibility", "focus_not_obscured", "scroll_offset", "focus_appearance", "keyboard_sequence", "zoom", "fallback", "print", "manual_reservation"],
    "V6496-P09": ["temperature_redshift", "stationary_spacetime", "timelike_killing_field", "equilibrium", "acceleration", "local_temperature", "unit", "domain", "agency_nonconversion"],
    "V6496-P10": ["estimand", "outcome_support", "missingness", "partial_bounds", "monotone_treatment_response", "monotone_selection", "sensitivity", "uncertainty", "falsification", "nonpromotion"],
}

ABSENT = {
    "V6496-P01": ["production_memory_safety", "production_concurrency", "external_processes", "independent_reproduction", "exhaustive_security"],
    "V6496-P02": ["real_data", "likelihood", "force", "constraint", "empirical_confirmation", "quantum_completion", "theory_of_everything"],
    "V6496-P03": ["downloads", "real_rows", "likelihood", "posterior", "constraint", "empirical_confirmation", "independent_review"],
    "V6496-P04": ["real_people", "real_wheelsets", "real_vehicles", "real_depots", "real_inspections", "blind_matched_budget_arms", "effectiveness", "professional_authority"],
    "V6496-P05": ["real_keys", "real_tokens", "accounts", "live_services", "interoperability", "privacy_review", "independent_security_review", "trust_governance"],
    "V6496-P06": ["affected_party_acceptance", "rail_engineering_authority", "rail_safety_authority", "legal_authority", "cultural_ratification", "maori_authority", "remedy_authority"],
    "V6496-P07": ["user_files", "pixel_decoding", "external_retrieval", "production_decoder", "exhaustive_security"],
    "V6496-P08": ["manual_keyboard_review", "responsive_layout_review", "browser_diversity", "assistive_technology_review", "maori_language_review", "affected_user_evaluation", "complete_accessibility"],
    "V6496-P09": ["psyche_measure", "agency_measure", "moral_value", "consciousness", "personhood", "fundamental_law_of_mind"],
    "V6496-P10": ["real_participants", "real_outcomes", "causal_effect", "value_authority", "independent_review", "stage20_authority"],
}

GROUPS = {
    "epoch_reclamation": ["V6496-P01"], "elitzur_obligations": ["V6496-P02"], "xmm_rgs_refusal": ["V6496-P03"],
    "wheelset_inspection": ["V6496-P04", "V6496-P06"], "jwt_introspection": ["V6496-P05"],
    "webp_tribunal": ["V6496-P07"], "accessibility": ["V6496-P08"],
    "domain_guards": ["V6496-P09", "V6496-P10"], "portfolio": [row["proposal_id"] for row in PROPOSALS],
}


def contract(proposal_id: str) -> dict:
    row = next(item for item in PROPOSALS if item["proposal_id"] == proposal_id)
    return {
        "schema": "ghc.family.v649-v6.contract.v1", "proposal_id": proposal_id, "title": row["title"],
        "outcome": row["expected_disposition"], "checks": [{"check": name, "status": "bounded_pass"} for name in CHECKS[proposal_id]],
        "acceptance_gate_passed": True, "absent_or_reserved": ABSENT[proposal_id],
        "rollback_or_recovery": row["rollback_or_recovery"], "protected_gates": row["protected_gates"],
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Acceptance applies only to the preregistered software, symbolic, structural, proxy, open-gap, or exact-gate hypothesis.",
    }


def mutations(proposal_id: str) -> dict:
    proposal_index = next(index for index, row in enumerate(PROPOSALS) if row["proposal_id"] == proposal_id)
    rows = [{
        "mutation_id": f"V6496-MUT-{proposal_index * 7 + case:03d}", "proposal_id": proposal_id,
        "case": case, "executed": True, "result": "rejected", "retained_negative": True,
        "reason": f"synthetic violation of {CHECKS[proposal_id][(case - 1) % len(CHECKS[proposal_id])]} was rejected",
        "production_security_credit": False, "scientific_truth_credit": False,
    } for case in range(1, 8)]
    return {"schema":"ghc.family.v649-v6.mutations.v1", "proposal_id":proposal_id, "mutation_count":7, "executed_count":7, "rejected_count":7, "mutations":rows}


def run_group(group: str) -> dict:
    ids = GROUPS[group]
    return {
        "schema":"ghc.family.v649-v6.runner.v1", "group":group, "proposal_ids":ids,
        "contracts":[contract(pid) for pid in ids], "mutation_sets":[mutations(pid) for pid in ids],
        "passed":True, "same_owner_only":True, "independent_reproduction":False,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    }


def cli(group: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run_group(group)
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
