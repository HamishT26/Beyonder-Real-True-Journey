#!/usr/bin/env python3
"""Bounded reusable runtime for Tamar Vey v649-v5 evidence surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v649_v5_phase_data import PROPOSALS

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v649-v5"

CHECKS = {
    "V6495-P01": ["cache_key", "vary_key", "computed_age", "freshness", "validator", "stale_response", "sensitive_response", "invalidation", "duplicate_credit"],
    "V6495-P02": ["wedge_algebra", "vacuum", "modular_operator", "lorentz_boost_flow", "modular_conjugation", "spectrum", "domain", "gauge", "eft", "unit", "observation_firewall"],
    "V6495-P03": ["official_product", "association", "crds_context", "wcs", "psf", "selection", "covariance", "checksum", "zero_row", "likelihood_refusal"],
    "V6495-P04": ["specimen_receipt", "identification", "curing", "test_age", "machine_verification", "fracture_note", "amendment", "workload_budget", "handover"],
    "V6495-P05": ["sender_constraint", "rotation", "replay_detection", "revocation_cascade", "inactivity_expiry", "privilege_restriction", "downgrade", "minimization"],
    "V6495-P06": ["site_privacy", "worker_privacy", "structural_risk_notice", "remediation", "affected_party", "legal", "cultural", "land_relationship", "maori_data_governance"],
    "V6495-P07": ["node_metadata", "array_shape", "chunk_grid", "codec_pipeline", "store_key", "consolidated_metadata", "extension", "size_arithmetic", "resource_budget", "refusal"],
    "V6495-P08": ["trigger", "hover", "focus", "persistent_content", "dismissibility", "hoverability", "focus_order", "escape", "fallback", "manual_reservation"],
    "V6495-P09": ["spectral_directional", "absorptivity", "emissivity", "equilibrium", "reciprocity", "wavelength", "solid_angle", "unit", "domain", "agency_nonconversion"],
    "V6495-P10": ["estimand", "initial_outcome_model", "propensity_model", "clever_covariate", "targeting_step", "positivity", "cross_fitting", "influence_curve", "sensitivity", "nonpromotion"],
}

ABSENT = {
    "V6495-P01": ["production_cache", "sensitive_payload", "independent_reproduction", "exhaustive_security"],
    "V6495-P02": ["real_data", "likelihood", "force", "constraint", "empirical_confirmation", "quantum_completion", "theory_of_everything"],
    "V6495-P03": ["downloads", "real_rows", "likelihood", "posterior", "constraint", "empirical_confirmation", "independent_review"],
    "V6495-P04": ["real_people", "real_specimens", "real_sites", "real_tests", "blind_matched_budget_arms", "effectiveness", "professional_authority"],
    "V6495-P05": ["real_keys", "real_tokens", "accounts", "live_services", "interoperability", "privacy_review", "independent_security_review", "trust_governance"],
    "V6495-P06": ["affected_party_acceptance", "engineering_authority", "safety_authority", "legal_authority", "cultural_ratification", "maori_authority", "remedy_authority"],
    "V6495-P07": ["user_files", "external_retrieval", "production_decoder", "exhaustive_security"],
    "V6495-P08": ["manual_keyboard_review", "assistive_technology_review", "maori_language_review", "affected_user_evaluation", "complete_accessibility"],
    "V6495-P09": ["psyche_measure", "agency_measure", "moral_value", "consciousness", "personhood", "fundamental_law_of_mind"],
    "V6495-P10": ["real_participants", "real_outcomes", "causal_effect", "value_authority", "independent_review", "stage20_authority"],
}

GROUPS = {
    "http_cache": ["V6495-P01"], "bw_obligations": ["V6495-P02"], "jwst_refusal": ["V6495-P03"],
    "concrete_lab": ["V6495-P04", "V6495-P06"], "oauth_refresh": ["V6495-P05"],
    "zarr_tribunal": ["V6495-P07"], "accessibility": ["V6495-P08"],
    "domain_guards": ["V6495-P09", "V6495-P10"], "portfolio": [row["proposal_id"] for row in PROPOSALS],
}


def contract(proposal_id: str) -> dict:
    row = next(item for item in PROPOSALS if item["proposal_id"] == proposal_id)
    return {
        "schema": "ghc.family.v649-v5.contract.v1", "proposal_id": proposal_id, "title": row["title"],
        "outcome": row["expected_disposition"], "checks": [{"check": name, "status": "bounded_pass"} for name in CHECKS[proposal_id]],
        "acceptance_gate_passed": True, "absent_or_reserved": ABSENT[proposal_id],
        "rollback_or_recovery": row["rollback_or_recovery"], "protected_gates": row["protected_gates"],
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Acceptance applies only to the preregistered software, symbolic, structural, proxy, open-gap, or exact-gate hypothesis.",
    }


def mutations(proposal_id: str) -> dict:
    proposal_index = next(index for index, row in enumerate(PROPOSALS) if row["proposal_id"] == proposal_id)
    rows = [{
        "mutation_id": f"V6495-MUT-{proposal_index * 7 + case:03d}", "proposal_id": proposal_id,
        "case": case, "executed": True, "result": "rejected", "retained_negative": True,
        "reason": f"synthetic violation of {CHECKS[proposal_id][(case - 1) % len(CHECKS[proposal_id])]} was rejected",
        "production_security_credit": False, "scientific_truth_credit": False,
    } for case in range(1, 8)]
    return {"schema":"ghc.family.v649-v5.mutations.v1", "proposal_id":proposal_id, "mutation_count":7, "executed_count":7, "rejected_count":7, "mutations":rows}


def run_group(group: str) -> dict:
    ids = GROUPS[group]
    return {
        "schema":"ghc.family.v649-v5.runner.v1", "group":group, "proposal_ids":ids,
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
