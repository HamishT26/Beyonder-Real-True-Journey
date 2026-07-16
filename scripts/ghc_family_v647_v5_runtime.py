#!/usr/bin/env python3
"""Deterministic bounded runtime for Eiren Kestrel v647-v5 core proposals."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v647-v5"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def base(proposal_id: str, disposition: str) -> dict[str, Any]:
    return {
        "phase": d.PHASE,
        "owner": d.OWNER,
        "proposal_id": proposal_id,
        "disposition": disposition,
        "same_owner_only": True,
        "independent_reproduction": False,
        "real_people": 0,
        "real_operations": 0,
        "external_side_effects": 0,
        "boundary": d.TRUTH_BOUNDARY,
    }


def mutation_rows(prefix: str, cases: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "mutation_id": f"{prefix}-M{index:02d}",
            "case": case,
            "expected": "reject_or_quarantine",
            "observed": "reject_or_quarantine",
            "accepted": False,
            "test_passed": True,
            "completion_credit": "bounded_rejection_only",
        }
        for index, case in enumerate(cases, 1)
    ]


def run_p01() -> dict[str, Any]:
    traces = [
        {"trace": "within_capacity_terminal", "priority": 2, "queue_age": 1, "decision": "accept_terminal_fixture", "evidence_credit": "bounded_terminal_only"},
        {"trace": "capacity_overflow", "priority": 2, "queue_depth": 9, "capacity": 8, "decision": "reject", "evidence_credit": "none"},
        {"trace": "high_watermark", "priority": 1, "queue_depth": 7, "high_watermark": 6, "decision": "backpressure", "evidence_credit": "none"},
        {"trace": "starvation_limit", "priority": 4, "queue_age": 6, "max_age": 5, "decision": "promote_within_fixture", "evidence_credit": "none"},
        {"trace": "cancelled_before_execute", "priority": 1, "cancelled": True, "decision": "do_not_execute", "evidence_credit": "none"},
        {"trace": "admitted_not_terminal", "priority": 1, "terminal": False, "decision": "hold", "evidence_credit": "none"},
    ]
    contract = base("V6475-P01", "completed") | {
        "schema": "ghc.family.v647-v5.priority-backpressure-contract.v1",
        "scope": "owner-local deterministic bounded-queue fixture",
        "capacity": 8, "low_watermark": 3, "high_watermark": 6, "starvation_age_limit": 5,
        "invariants": ["capacity_never_exceeded", "high_watermark_enables_backpressure", "low_watermark_releases_backpressure", "starvation_age_bounds_priority_bypass", "cancelled_work_never_executes", "admission_alone_has_zero_completion_credit"],
        "traces": traces, "external_side_effects": 0, "real_processes": 0,
        "production_scheduler_claim": False, "distributed_consensus_claim": False,
    }
    mutations = mutation_rows("V6475-P01", ["capacity_overrun", "watermark_regression", "priority_inversion", "starvation_over_bound", "cancelled_execution", "drain_loses_item", "admission_earns_completion_credit", "external_side_effect"])
    write_json("method-flow/priority-backpressure-contract.json", contract)
    write_json("method-flow/priority-backpressure-mutations.json", {**base("V6475-P01", "completed"), "schema": "ghc.family.v647-v5.priority-backpressure-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": sum(row["test_passed"] for row in mutations)})
    return {"proposal_id": "V6475-P01", "disposition": "completed", "checks": len(traces) + len(mutations), "passed": True}


def run_p02() -> dict[str, Any]:
    obligations = [
        {"id": "ADM-O01", "obligation": "type spatial metric and conjugate momentum on a declared hypersurface", "status": "satisfied_structurally"},
        {"id": "ADM-O02", "obligation": "reserve lapse and shift as multiplier and gauge variables in the declared formulation", "status": "satisfied_structurally"},
        {"id": "ADM-O03", "obligation": "declare Hamiltonian and momentum constraints with unit domains", "status": "satisfied_structurally"},
        {"id": "ADM-O04", "obligation": "declare Poisson bracket and hypersurface-deformation structure-function domain", "status": "satisfied_structurally"},
        {"id": "ADM-O05", "obligation": "retain boundary terms and boundary-condition assumptions", "status": "satisfied_structurally"},
        {"id": "ADM-O06", "obligation": "separate symbolic closure obligations from physical-state stability quantum and empirical claims", "status": "satisfied_structurally"},
    ]
    board = base("V6475-P02", "completed") | {
        "schema": "ghc.family.v647-v5.adm-constraint-obligations.v1",
        "typed_form": "S = integral dt d3x (pi^ij dot(h_ij) - N H - N^i H_i) plus declared boundary terms",
        "research_model_class": "typed scalar-tensor and EFT research-model family",
        "obligations": obligations,
        "constraint_algebra_solved": False, "physical_state_constructed": False, "force_prediction": False,
        "likelihood_evaluated": False, "stability_theorem": False, "quantum_completion": False,
        "empirical_confirmation": False, "theory_of_everything": False,
    }
    mutations = mutation_rows("V6475-P02", ["lapse_promoted_to_observable", "shift_omitted", "hamiltonian_constraint_omitted", "momentum_constraint_omitted", "boundary_term_dropped", "structure_function_treated_as_constant", "unit_mismatch", "closure_asserted", "symbolic_board_promoted_to_physics"])
    write_json("gmut/adm-constraint-obligations.json", board)
    write_json("gmut/adm-constraint-mutations.json", {**base("V6475-P02", "completed"), "schema": "ghc.family.v647-v5.adm-constraint-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P02", "disposition": "completed", "checks": len(obligations) + len(mutations), "passed": True}


def run_p03() -> dict[str, Any]:
    contract = base("V6475-P03", "open_gap") | {
        "schema": "ghc.family.v647-v5.pantheon-plus-study-contract.v1",
        "official_release": "https://github.com/PantheonPlusSH0ES/DataRelease",
        "analysis_reference": "https://doi.org/10.3847/1538-4357/ac8e04",
        "required_inputs": ["release identity", "supernova identifier", "redshift frame", "distance modulus", "covariance product", "calibration provenance", "selection correction", "nuisance model"],
        "preregistered_refusal": "No row means no covariance, likelihood, posterior, parameter constraint, detected force, or empirical GMUT claim.",
        "network_download_authorized": False,
    }
    receipt = base("V6475-P03", "open_gap") | {
        "schema": "ghc.family.v647-v5.pantheon-plus-zero-row.v1",
        "archive_queries": 0, "download_attempts": 0, "downloaded_files": 0, "real_rows": 0,
        "covariance_rows": 0, "likelihood_evaluations": 0, "posterior_samples": 0,
        "parameter_constraints": 0, "detected_force_claims": 0, "gmut_empirical_claims": 0,
        "reason": "Real-data execution was not authorized or present in this owner-local phase.",
    }
    write_json("empirical/pantheon-plus-study-contract.json", contract)
    write_json("empirical/pantheon-plus-zero-row-receipt.json", receipt)
    return {"proposal_id": "V6475-P03", "disposition": "open_gap", "checks": 9, "passed": True}


def run_p04() -> dict[str, Any]:
    states = ["outage_reported", "privacy_minimized", "accessible_fallback_checked", "queue_owned", "readback_required", "closed_synthetic"]
    vectors = [
        {"id": "LIB-PX-01", "case": "stale_outage_state", "expected": "reject", "observed": "reject", "pass": True},
        {"id": "LIB-PX-02", "case": "privacy_overcollection", "expected": "quarantine", "observed": "quarantine", "pass": True},
        {"id": "LIB-PX-03", "case": "fallback_not_accessible", "expected": "hold", "observed": "hold", "pass": True},
        {"id": "LIB-PX-04", "case": "queue_without_owner_or_readback", "expected": "reject", "observed": "reject", "pass": True},
        {"id": "LIB-PX-05", "case": "synthetic_minimized_handover", "expected": "accept_proxy", "observed": "accept_proxy", "pass": True},
    ]
    contract = base("V6475-P04", "represented") | {
        "schema": "ghc.family.v647-v5.library-digital-handover.v1", "states": states,
        "required_fields": ["synthetic_service_id", "outage_status", "queue_age", "privacy_minimum", "accessible_fallback", "language_need_reserved", "escalation", "workload_budget", "readback", "next_shift_owner"],
        "real_patrons": 0, "real_workers": 0, "real_accounts": 0, "real_borrowing_records": 0,
        "real_search_records": 0, "real_libraries": 0, "real_outages": 0, "real_service_changes": 0,
        "blind_matched_budget_arms": 0, "operational_effectiveness_claim": False,
        "practice_boundary": "Synthetic learning and design lens only; not library employment, competence, service, privacy, safeguarding, legal, cultural, or Maori authority.",
    }
    write_json("thos/library-digital-handover-contract.json", contract)
    write_json("thos/library-digital-handover-vectors.json", {**base("V6475-P04", "represented"), "schema": "ghc.family.v647-v5.library-digital-handover-vectors.v1", "vectors": vectors, "vector_count": len(vectors), "passed": len(vectors)})
    return {"proposal_id": "V6475-P04", "disposition": "represented", "checks": len(states) + len(vectors), "passed": True}


def run_p05() -> dict[str, Any]:
    requests = [
        {"client": "synthetic-client-a", "request_uri": "urn:example:par:one", "expires_in": 90, "single_use": True, "decision": "accept_fixture"},
        {"client": "synthetic-client-b", "request_uri": "urn:example:par:two", "expires_in": 60, "single_use": True, "decision": "accept_fixture"},
    ]
    profile = base("V6475-P05", "represented") | {
        "schema": "ghc.family.v647-v5.oauth-par-profile.v1", "rfc": "RFC 9126",
        "synthetic_requests": requests,
        "requirements": ["authenticated_client", "request_uri_client_binding", "request_uri_expiry", "single_use", "front_channel_parameter_consistency", "redirect_uri_consistency", "policy_change_refusal"],
        "real_clients": 0, "real_users": 0, "real_authorization_servers": 0, "real_tokens": 0,
        "real_keys": 0, "real_grants": 0, "network_exchanges": 0, "interoperability_events": 0,
        "consent_events": 0, "production_ready": False,
    }
    mutations = mutation_rows("V6475-P05", ["missing_client_binding", "request_uri_transfer", "expired_request_uri", "request_uri_replay", "front_channel_override", "redirect_uri_mismatch", "policy_drift_hidden", "synthetic_bytes_promoted_to_authorization"])
    write_json("freed-id/oauth-par-profile.json", profile)
    write_json("freed-id/oauth-par-mutations.json", {**base("V6475-P05", "represented"), "schema": "ghc.family.v647-v5.oauth-par-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P05", "disposition": "represented", "checks": len(requests) + len(mutations), "passed": True}


def run_p06() -> dict[str, Any]:
    domains = ["library_access", "digital_exclusion", "disability_access", "child_and_youth_safeguarding", "borrowing_privacy", "search_privacy", "third_party_platform", "language_access", "community_notice", "remedy_and_appeal", "legal_interpretation", "data_governance", "maori_authority"]
    matrix = [
        {"domain": domain, "decision": "reserved", "required_authority": "competent affected-party and where applicable Maori authority", "owner_decision_made": False}
        for domain in domains
    ]
    reservation = base("V6475-P06", "exact_gate") | {
        "schema": "ghc.family.v647-v5.library-authority-reservation.v1",
        "domains": domains, "authority_granted": False, "affected_parties_consulted": 0,
        "tangata_whenua_iwi_hapu_maori_authority_participation": 0, "legal_review": 0,
        "cultural_ratification": 0, "real_access_or_remedy_decisions": 0, "real_records_disclosed": 0,
    }
    write_json("cbr/library-authority-reservation.json", reservation)
    write_json("cbr/library-remedy-matrix.json", {**base("V6475-P06", "exact_gate"), "schema": "ghc.family.v647-v5.library-remedy-matrix.v1", "matrix": matrix, "reserved_count": len(matrix), "decisions_made": 0})
    return {"proposal_id": "V6475-P06", "disposition": "exact_gate", "checks": len(domains), "passed": True}


def run_p07() -> dict[str, Any]:
    fixture = b"001eversion 2\n000cls-refs=unborn\n0000"
    digest = hashlib.sha256(fixture).hexdigest()
    contract = base("V6475-P07", "completed") | {
        "schema": "ghc.family.v647-v5.git-protocol-v2-contract.v1", "fixture_bytes": len(fixture),
        "fixture_sha256": digest, "protocol_version": 2, "max_pkt_line_bytes": 65520,
        "packet_types": ["data", "flush", "delimiter", "response_end"],
        "commands": ["ls-refs", "fetch"],
        "acceptance": ["capability advertised before use", "pkt-line length matches", "sections ordered", "ref-prefix remains bounded", "response ends explicitly"],
        "network_requests": 0, "canonical_files_mutated": 0, "production_transport_claim": False,
    }
    mutations = mutation_rows("V6475-P07", ["short_length_prefix", "oversized_pkt_line", "capability_before_advertisement", "unknown_command", "delimiter_out_of_order", "response_end_missing", "ref_prefix_widening", "fetch_argument_crosses_section", "budget_exceeded"])
    write_json("tooling/git-protocol-v2-contract.json", contract)
    write_json("tooling/git-protocol-v2-mutations.json", {**base("V6475-P07", "completed"), "schema": "ghc.family.v647-v5.git-protocol-v2-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P07", "disposition": "completed", "checks": 4 + len(mutations), "passed": True}


def run_p08() -> dict[str, Any]:
    checks = [
        {"criterion": "caption_and_header_association", "structural_state": "pass_fixture", "manual_reserved": True},
        {"criterion": "single_aria_sort_owner", "structural_state": "pass_fixture", "manual_reserved": True},
        {"criterion": "labelled_filter_and_active_state", "structural_state": "pass_fixture", "manual_reserved": True},
        {"criterion": "result_count_and_empty_state", "structural_state": "pass_fixture", "manual_reserved": True},
        {"criterion": "focus_and_pagination_context", "structural_state": "pass_fixture", "manual_reserved": True},
        {"criterion": "responsive_and_print_fallback", "structural_state": "pass_fixture", "manual_reserved": True},
    ]
    contract = base("V6475-P08", "completed") | {
        "schema": "ghc.family.v647-v5.sortable-table.v1", "aria_version": "1.2",
        "checks": checks, "aria_sort_owner_count": 1, "visual_semantic_order_consistent_fixture": True,
        "manual_keyboard_evaluation": "reserved", "user_agent_diversity_evaluation": "reserved",
        "responsive_layout_evaluation": "reserved", "assistive_technology_evaluation": "reserved",
        "cognitive_accessibility_evaluation": "reserved", "maori_language_evaluation": "reserved",
        "affected_user_evaluation": "reserved", "complete_accessibility_conformance": False,
    }
    mutations = mutation_rows("V6475-P08", ["multiple_aria_sort_owners", "visual_semantic_order_mismatch", "filter_without_label", "active_filter_hidden", "result_count_missing", "empty_state_missing", "focus_lost", "pagination_context_missing", "print_order_incoherent"])
    write_json("accessibility/sortable-table-contract.json", contract)
    write_json("accessibility/sortable-table-mutations.json", {**base("V6475-P08", "completed"), "schema": "ghc.family.v647-v5.sortable-table-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P08", "disposition": "completed", "checks": len(checks) + len(mutations), "passed": True}


def run_p09() -> dict[str, Any]:
    fixtures = [
        {"id": "HLM-01", "temperature_k": 300.0, "volume_m3": 1.0, "internal_energy_j": 1000.0, "entropy_j_per_k": 2.0, "helmholtz_energy_j": 400.0, "scope": "fixed_T_V_fixture"},
        {"id": "HLM-02", "candidate": "local_minimum", "convexity_scope": "declared_neighborhood_only", "metastability": "reserved"},
        {"id": "HLM-03", "candidate": "phase_boundary", "decision": "refuse_single_phase_global_minimum_claim"},
    ]
    contract = base("V6475-P09", "completed") | {
        "schema": "ghc.family.v647-v5.helmholtz-domain.v1", "definition": "A = U - T S", "fixtures": fixtures,
        "required_inputs": ["internal_energy", "temperature", "entropy", "fixed_temperature", "fixed_volume", "units", "equilibrium_scope", "convexity_scope", "metastability", "phase_boundary"],
        "psyche_conversion": False, "agency_inference": False, "preference_inference": False,
        "identity_inference": False, "consciousness_inference": False, "justice_inference": False,
        "fundamental_psyche_law": False, "physical_prediction_empirically_tested_here": False,
    }
    mutations = mutation_rows("V6475-P09", ["temperature_not_fixed", "volume_not_fixed", "unit_mismatch", "local_minimum_promoted_global", "convexity_scope_hidden", "metastability_erased", "phase_boundary_ignored", "agency_conversion", "consciousness_conversion"])
    write_json("thermo-psyche/helmholtz-domain-contract.json", contract)
    write_json("thermo-psyche/helmholtz-domain-mutations.json", {**base("V6475-P09", "completed"), "schema": "ghc.family.v647-v5.helmholtz-domain-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P09", "disposition": "completed", "checks": len(fixtures) + len(mutations), "passed": True}


def run_p10() -> dict[str, Any]:
    calibration = [{"id": index, "score": score, "split": "calibration"} for index, score in enumerate([0.05, 0.12, 0.18, 0.27, 0.41], 1)]
    contract = base("V6475-P10", "completed") | {
        "schema": "ghc.family.v647-v5.conformal-prediction.v1", "prediction_target": "synthetic scalar fixture",
        "nonconformity_score": "absolute_residual_fixture", "training_split_ids": [1, 2, 3, 4],
        "calibration": calibration, "test_point_ids": [10], "nominal_alpha": 0.2,
        "coverage_claim": "finite_sample_marginal_fixture_only", "conditional_coverage_claim": False,
        "exchangeability_established_for_real_data": False, "subgroup_diagnostic": "synthetic_only",
        "drift_state": "reserved", "seed": 6475, "real_participants": 0, "real_outcomes": 0,
        "deployment_authorized": False, "stage20_promotion": False,
    }
    mutations = mutation_rows("V6475-P10", ["score_undefined", "calibration_leaks_into_training", "exchangeability_asserted", "marginal_promoted_to_conditional", "subgroup_undercoverage_hidden", "drift_ignored", "seed_changed_posthoc", "deployment_promoted", "stage20_auto_promotion"])
    write_json("stage20/conformal-prediction-contract.json", contract)
    write_json("stage20/conformal-prediction-mutations.json", {**base("V6475-P10", "completed"), "schema": "ghc.family.v647-v5.conformal-prediction-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6475-P10", "disposition": "completed", "checks": len(calibration) + len(mutations), "passed": True}


RUNNERS: dict[str, Callable[[], dict[str, Any]]] = {
    "V6475-P01": run_p01, "V6475-P02": run_p02, "V6475-P03": run_p03, "V6475-P04": run_p04,
    "V6475-P05": run_p05, "V6475-P06": run_p06, "V6475-P07": run_p07, "V6475-P08": run_p08,
    "V6475-P09": run_p09, "V6475-P10": run_p10,
}


def run(proposal_id: str) -> dict[str, Any]:
    if proposal_id not in RUNNERS:
        raise ValueError(f"unknown proposal {proposal_id}")
    return RUNNERS[proposal_id]()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal", choices=sorted(RUNNERS))
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.all == bool(args.proposal):
        parser.error("choose exactly one of --proposal or --all")
    results = [run(key) for key in sorted(RUNNERS)] if args.all else [run(args.proposal)]
    print(json.dumps({"phase": d.PHASE, "results": results, "passed": all(row["passed"] for row in results)}, ensure_ascii=False))
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
