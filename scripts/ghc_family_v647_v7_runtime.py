#!/usr/bin/env python3
"""Bounded structural runtime for Sable Rook v647-v7 proposal surfaces."""

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
    "attestation": spec("V6477-P01", "completed", [
        "subject_digest_exact", "materials_digest_exact", "predicate_type_known", "builder_boundary_explicit",
        "dependency_graph_acyclic", "duplicate_credit_quarantined", "inherited_credit_isolated",
    ], "bounded attestation and evidence-credit fixtures"),
    "picard_lefschetz": spec("V6477-P02", "completed", [
        "canonical_scaffold_typed", "contour_orientation_declared", "thimble_flow_declared", "intersection_number_sourced",
        "stokes_wall_reserved", "units_covariance_conservation_preserved", "observation_firewall_closed",
    ], "typed symbolic contour and EFT obligations"),
    "spt3g_d1": spec("V6477-P03", "open_gap", [
        "release_identity_frozen", "bandpower_schema_declared", "beam_and_window_required", "calibration_required",
        "covariance_required", "nuisance_model_required", "likelihood_refuses_zero_rows",
    ], "official-format zero-row readiness contract"),
    "building_handover": spec("V6477-P04", "represented", [
        "revision_monotone", "defect_hold_fail_closed", "reinspection_condition_explicit", "amendment_reason_required",
        "correction_readback_required", "accessible_notice_reserved", "next_owner_and_budget_bound",
    ], "synthetic building-inspection event and handover traces"),
    "oauth_resource": spec("V6477-P05", "represented", [
        "resource_identifier_bound", "authorization_server_bound", "signed_metadata_precedence", "cache_freshness_checked",
        "redirect_scope_not_widened", "downgrade_rejected", "metadata_correlation_reserved",
    ], "synthetic OAuth protected-resource metadata vectors"),
    "building_authority": spec("V6477-P06", "exact_gate", [
        "access_authority_reserved", "tenant_and_owner_interests_reserved", "disability_access_reserved", "privacy_reserved",
        "remedy_and_appeal_reserved", "legal_and_cultural_meaning_reserved", "maori_authority_reserved",
    ], "refusal-first building authority and remedy matrix"),
    "dns_wire": spec("V6477-P07", "completed", [
        "label_length_bounded", "name_length_bounded", "compression_cycle_rejected", "pointer_offset_bounded",
        "section_counts_consistent", "edns_size_bounded", "truncation_rejected",
    ], "disposable synthetic DNS wire fixtures with no network resolution"),
    "virtualized_feed": spec("V6477-P08", "completed", [
        "position_and_setsize_coherent", "busy_state_exposed", "focus_persists", "updates_throttled",
        "pause_control_present", "nonvirtual_fallback_complete", "export_alternative_complete",
    ], "structural virtualized-feed accessibility fixtures"),
    "fugacity": spec("V6477-P09", "completed", [
        "standard_state_declared", "logarithm_dimensionless", "temperature_and_phase_scoped", "activity_coefficient_typed",
        "chemical_potential_relation_typed", "ideal_limit_declared", "agency_nonconversion_enforced",
    ], "typed thermodynamic fugacity and category-barrier fixtures"),
    "rosenbaum": spec("V6477-P10", "completed", [
        "matched_design_declared", "gamma_interpretation_bounded", "sharp_null_declared", "test_statistic_declared",
        "outcome_model_not_substituted", "subgroup_failures_retained", "stage20_nonpromotion_enforced",
    ], "structural hidden-bias sensitivity and abstention fixtures"),
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
        "real_people_or_properties": 0,
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
    for field in ("real_rows", "likelihood_calls", "posterior_samples", "real_people_or_properties", "real_keys_tokens_or_servers", "authority_decisions", "network_actions"):
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
            "negative_id": f"V6477-SYN-{int(item['proposal_id'][-2:]):02d}-{index:02d}",
            "surface": surface,
            "mutated_obligation": obligation,
            "accepted": accepted,
            "rejected": not accepted,
            "retained": True,
            "reasons": reasons,
            "scientific_or_production_credit": False,
        })
    return {
        "schema": "ghc.family.v647-v7.surface-evidence.v1",
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
