#!/usr/bin/env python3
"""Bounded synthetic, symbolic, and structural runtime for Sable v652-v1.

The runtime performs no network I/O, opens no user material, changes no sibling
state, launches no future seat, and confers no empirical or authority credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any

import ghc_family_v652_v1_phase_data as d


OBLIGATIONS: dict[str, list[str]] = {
    "claim-lease-demotion": ["claim_id", "lease_start", "lease_expiry", "renewal", "supersession", "retraction", "dependent_demotion", "noncompensation", "lineage"],
    "git-cruft-pack": ["cruft_pack", "mtime_sideband", "unreachable_horizon", "promisor_exclusion", "duplicate_object", "checksum", "expiry", "rescue", "repository_refusal"],
    "oci-referrers": ["subject_digest", "artifact_manifest", "repository_scope", "artifact_type", "media_type", "pagination", "fallback_tag", "deletion_race", "network_refusal"],
    "belinfante-rosenfeld": ["canonical_stress", "spin_current", "improvement_divergence", "tensor_symmetry", "on_shell_conservation", "boundary_term", "unit", "eft_scope", "observation_firewall"],
    "dirac-bergmann-constraints": ["primary_constraint", "secondary_constraint", "consistency_chain", "first_class", "second_class", "total_hamiltonian", "multiplier", "gauge_generator", "unit", "observation_firewall"],
    "noether-second-theorem": ["gauge_generator", "differential_identity", "off_shell_euler_lagrange", "boundary_term", "constraint_map", "unit", "eft_scope", "observation_firewall"],
    "hadamard-parametrix": ["geodesic_neighbourhood", "wavefront_set", "u_coefficient", "v_coefficient", "w_coefficient", "state_dependence", "subtraction", "curvature", "unit", "observation_firewall"],
    "canonical-omega-sector": ["omega_decomposition", "covariant_divergence", "exchange_current", "mass_dimension", "sign_convention", "background_domain", "stability_firewall", "identifiability_firewall", "observation_firewall"],
    "c2pa-jumbf": ["jumbf_store", "claim", "assertion", "ingredient", "redaction", "update_manifest", "signature_box", "hash_link", "resource_budget"],
    "sarif-result-lineage": ["result_fingerprint", "baseline_state", "suppression", "artifact_location", "code_flow", "thread_flow", "taxon", "redaction", "resource_budget"],
    "source-date-epoch": ["source_date_epoch", "archive_mtime", "timezone", "locale", "path", "ordering", "uid_gid", "umask", "random_seed", "dependency_lock"],
    "debian-apt-metadata": ["inrelease", "release", "packages", "by_hash", "valid_until", "version", "architecture", "component", "digest", "rollback", "freeze"],
    "python-wheel-record": ["record_path", "urlsafe_digest", "size", "dist_info", "data_scheme", "script", "symlink", "duplicate", "traversal", "installation_budget"],
    "zip64-central-directory": ["zip64_end_record", "locator", "central_directory_offset", "extra_field", "data_descriptor", "duplicate_name", "overlap", "traversal", "expansion_budget"],
    "hdf5-superblock": ["signature", "version", "offset_size", "length_size", "base_address", "end_of_file_address", "free_space_address", "driver_info", "extension", "object_header", "resource_budget"],
    "pdf-incremental-update": ["xref_table", "xref_stream", "object_generation", "free_list", "trailer_prev", "startxref", "encryption_state", "revision_budget"],
    "elf-note-segment": ["owner", "type", "name_size", "descriptor_size", "alignment", "build_id", "gnu_property", "duplicate", "truncation", "segment_budget"],
    "multiformats-cidv1": ["cid_version", "multibase", "multicodec", "multihash", "varint_canonicality", "digest_length", "identity_hash", "representation", "resource_budget"],
    "court-registry-handover": ["accession", "custody", "seal_state", "discrepancy_hold", "correction_readback", "accessible_notice", "workload_ceiling", "shift_handover"],
    "court-registry-matched-budget": ["preregistration", "blind_arm", "matched_budget", "allocation", "contamination", "safety_stop", "workload", "missingness", "analysis_lock", "independent_review"],
    "acme-ari": ["certificate_identifier", "suggested_window", "retry_after", "fallback", "replacement_link", "already_replaced", "cache", "privacy", "production_refusal"],
    "scim-cursor-pagination": ["cursor", "next_cursor", "previous_cursor", "count", "sort", "filter", "invalid_cursor", "expired_cursor", "consistency", "privacy", "production_refusal"],
    "fido-credential-exchange": ["format", "protocol", "provider", "importer", "exporter", "encryption_boundary", "consent", "duplicate", "recovery", "draft_status", "production_refusal"],
    "accessible-code-diff": ["addition", "deletion", "unchanged_context", "line_number", "hunk_label", "keyboard_order", "wrap", "contrast", "table_alternative", "manual_reservation"],
    "web-annotation-selectors": ["body", "target", "motivation", "text_quote_selector", "text_position_selector", "refined_by", "state", "canonical", "privacy", "resource_budget"],
    "widom-line-nonconversion": ["response_maximum", "path_dependence", "crossover", "critical_region", "finite_size", "observable_choice", "uncertainty", "unit", "physical_domain", "agency_refusal"],
    "multiverse-analysis": ["decision_grid", "specification_curve", "vibration_of_effects", "outcome_blinding", "multiplicity", "subgroup", "missingness", "uncertainty", "nonpromotion"],
    "reproduction-capsule": ["dependency_lock", "seed", "locale", "timezone", "filesystem_order", "build_path", "network_refusal", "output_manifest", "drift", "independent_team_gap"],
    "panstarrs-dr2-zero-row": ["official_product", "stack_object", "detection", "mean_object", "filter", "astrometry", "photometry", "quality_flag", "selection", "covariance", "provenance", "checksum", "zero_row_firewall", "likelihood_refusal"],
    "court-registry-authority": ["exhibit_inspection", "suppression_boundary", "transcription_correction", "accessible_service", "retention", "redress", "tikanga_context", "tangata_whenua_governance", "legal_reservation", "maori_authority"],
}

MUTATION_DIMENSIONS = [
    "missing_required_obligation",
    "wrong_type_or_unit",
    "resource_or_replay_overrun",
    "unsupported_promotion",
    "authority_or_privacy_breach",
]


def proposal_by_id(proposal_id: str) -> dict[str, Any]:
    for proposal in d.PROPOSALS:
        if proposal["proposal_id"] == proposal_id:
            return proposal
    raise KeyError(proposal_id)


def canonical_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    fixture: dict[str, Any] = {
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "scope": "bounded_synthetic_symbolic_or_structural",
        "obligations": list(OBLIGATIONS[proposal["slug"]]),
        "resource_budget": 128,
        "replay_budget": 4,
        "promotion": "bounded_only",
        "authority_action": False,
        "privacy_disclosure": False,
        "network_actions": 0,
        "real_rows": 0,
        "real_people": 0,
        "real_keys": 0,
        "real_decisions": 0,
        "future_seats_named": 0,
        "future_seats_created": 0,
        "future_seats_launched": 0,
        "expected_disposition": proposal["expected_disposition"],
    }
    disposition = proposal["expected_disposition"]
    if disposition == "represented":
        fixture.update({"proxy_only": True, "blind_matched_budget_real_arms": 0, "independent_review": False})
    elif disposition == "open_gap":
        fixture.update({"zero_row_firewall": True, "queries": 0, "downloads": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0})
    elif disposition == "exact_gate":
        fixture.update({"reservation_only": True, "required_authorities": ["competent", "affected_party", "legal", "cultural", "maori"]})
    if proposal["slug"] == "fido-credential-exchange":
        fixture.update({"document_status": "draft", "production_profile_claimed": False})
    if proposal["slug"] in {"acme-ari", "scim-cursor-pagination", "fido-credential-exchange"}:
        fixture.update({"cryptographic_operations": 0, "interoperability_events": 0, "accounts": 0})
    return fixture


def specialized_witness(slug: str) -> dict[str, Any]:
    gmut = {"belinfante-rosenfeld", "dirac-bergmann-constraints", "noether-second-theorem", "hadamard-parametrix", "canonical-omega-sector"}
    identity = {"acme-ari", "scim-cursor-pagination", "fido-credential-exchange"}
    proxy = {"court-registry-handover", "court-registry-matched-budget"}
    if slug in gmut:
        return {"typed_board": True, "declared_obligations": OBLIGATIONS[slug], "symbolic_cases": 4, "physical_state": False, "prediction": False, "likelihood": False, "parameter_constraint": False, "empirical_confirmation": False, "theory_of_everything": False}
    if slug in proxy:
        return {"synthetic_trace": ["accession", "hold", "correction_readback", "accessible_notice", "handover"], "real_people": 0, "real_exhibits": 0, "court_actions": 0, "blind_matched_budget_real_arms": 0, "independent_review": False, "operational_effectiveness": False}
    if slug in identity:
        return {"synthetic_vectors": 5, "declared_obligations": OBLIGATIONS[slug], "real_keys": 0, "real_certificates_or_credentials": 0, "accounts": 0, "network_exchanges": 0, "interoperability_events": 0, "privacy_reviews": 0, "security_reviews": 0, "trust_governance_decisions": 0}
    if slug == "accessible-code-diff":
        return {"structural_contracts": len(OBLIGATIONS[slug]), "manual_keyboard": "reserved", "responsive_layout": "reserved", "browser_diversity": "reserved", "assistive_technology": "reserved", "maori_language": "reserved", "affected_user_evaluation": "reserved", "complete_conformance_claimed": False}
    if slug == "widom-line-nonconversion":
        return {"synthetic_response_points": [1.0, 1.4, 1.2], "maximum_index": 1, "finite": True, "thermodynamic_domain": True, "phase_transition_claimed": False, "psyche_conversion": False, "justice_conversion": False, "consciousness_conversion": False}
    if slug == "multiverse-analysis":
        return {"synthetic_specifications": 8, "outcome_blinded": True, "multiplicity_visible": True, "participant_effect": False, "stage20_authorized": False}
    if slug == "reproduction-capsule":
        values = ["lock", "seed", "locale", "timezone"]
        hashes = [hashlib.sha256(value.encode("utf-8")).hexdigest()[:12] for value in values]
        return {"bounded_inputs": values, "manifest_prefixes": hashes, "network_calls": 0, "same_owner_replay": True, "independent_team_reproduction": False}
    if slug == "panstarrs-dr2-zero-row":
        return {"queries": 0, "downloads": 0, "stack_rows": 0, "detection_rows": 0, "mean_object_rows": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0, "empirical_claims": 0}
    if slug == "court-registry-authority":
        return {"matrix_cells": len(OBLIGATIONS[slug]), "reservations": len(OBLIGATIONS[slug]), "real_decisions": 0, "affected_party_authority_claimed": False, "legal_authority_claimed": False, "cultural_authority_claimed": False, "maori_authority_claimed": False}
    return {"synthetic_cases": 5, "declared_obligations": OBLIGATIONS[slug], "external_resources_loaded": 0, "network_actions": 0, "user_or_sibling_material_touched": False, "production_claimed": False, "exhaustive_security_claimed": False}


def validate_fixture(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    required = set(OBLIGATIONS[proposal["slug"]])
    if fixture.get("proposal_id") != proposal["proposal_id"]: issues.append("proposal_id")
    if fixture.get("slug") != proposal["slug"]: issues.append("slug")
    if fixture.get("scope") != "bounded_synthetic_symbolic_or_structural": issues.append("scope_or_unit")
    if not required <= set(fixture.get("obligations", [])): issues.append("required_obligation")
    if not isinstance(fixture.get("resource_budget"), int) or not 0 <= fixture["resource_budget"] <= 128: issues.append("resource_budget")
    if not isinstance(fixture.get("replay_budget"), int) or not 0 <= fixture["replay_budget"] <= 4: issues.append("replay_budget")
    if fixture.get("promotion") != "bounded_only": issues.append("unsupported_promotion")
    if fixture.get("authority_action") is not False or fixture.get("privacy_disclosure") is not False: issues.append("authority_or_privacy")
    if fixture.get("network_actions") != 0 or fixture.get("real_people") != 0: issues.append("external_event")
    if any(fixture.get(key) != 0 for key in ("future_seats_named", "future_seats_created", "future_seats_launched")): issues.append("future_seat_activation")
    disposition = proposal["expected_disposition"]
    if disposition == "represented" and (fixture.get("proxy_only") is not True or fixture.get("blind_matched_budget_real_arms") != 0 or fixture.get("independent_review") is not False): issues.append("proxy_boundary")
    if disposition == "open_gap" and (fixture.get("zero_row_firewall") is not True or any(fixture.get(key) != 0 for key in ("queries", "downloads", "real_rows", "likelihood_calls", "posterior_samples", "constraints"))): issues.append("zero_row_firewall")
    if disposition == "exact_gate" and (fixture.get("reservation_only") is not True or fixture.get("real_decisions") != 0): issues.append("exact_gate")
    return {"accepted": not issues, "issues": sorted(set(issues)), "bounded": True, "same_owner_only": True, "independent_reproduction": False}


def mutate(fixture: dict[str, Any], dimension: str) -> dict[str, Any]:
    mutated = deepcopy(fixture)
    mutated["mutation_dimension"] = dimension
    if dimension == "missing_required_obligation": mutated["obligations"] = mutated["obligations"][1:]
    elif dimension == "wrong_type_or_unit": mutated["scope"] = {"wrong": "type"}
    elif dimension == "resource_or_replay_overrun": mutated.update({"resource_budget": 65536, "replay_budget": 65536})
    elif dimension == "unsupported_promotion": mutated["promotion"] = "empirical_or_authority_confirmation"
    elif dimension == "authority_or_privacy_breach": mutated.update({"authority_action": True, "privacy_disclosure": True})
    else: raise KeyError(dimension)
    return mutated


def rejection_witness(proposal_id: str, dimension: str) -> dict[str, Any]:
    proposal = proposal_by_id(proposal_id)
    result = validate_fixture(proposal, mutate(canonical_fixture(proposal), dimension))
    return {"proposal_id": proposal_id, "dimension": dimension, "rejected": not result["accepted"], "issues": result["issues"], "same_owner_only": True}


def execute(proposal_id: str) -> dict[str, Any]:
    proposal = proposal_by_id(proposal_id)
    canonical = canonical_fixture(proposal)
    baseline = validate_fixture(proposal, canonical)
    mutations = []
    for index, dimension in enumerate(MUTATION_DIMENSIONS, 1):
        witness = rejection_witness(proposal_id, dimension)
        mutations.append({"mutation_id": f"{proposal_id}-M{index:02d}", **witness})
    accepted = baseline["accepted"] and all(row["rejected"] for row in mutations)
    return {
        "proposal_id": proposal_id,
        "slug": proposal["slug"],
        "expected_disposition": proposal["expected_disposition"],
        "observed_outcome": proposal["expected_disposition"] if accepted else None,
        "canonical_fixture": canonical,
        "baseline_validation": baseline,
        "specialized_witness": specialized_witness(proposal["slug"]),
        "mutations": mutations,
        "mutation_count": len(mutations),
        "mutation_rejections": sum(row["rejected"] for row in mutations),
        "accepted": accepted,
        "boundary": "Bounded same-owner synthetic, symbolic, numerical, structural, or workflow evidence only; no empirical, production, professional, authority, independent-reproduction, or Stage 20 credit.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded Sable v652-v1 proposal fixtures.")
    parser.add_argument("--proposal", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()
    selected = args.proposal or [proposal["proposal_id"] for proposal in d.PROPOSALS]
    results = [execute(proposal_id) for proposal_id in selected]
    payload = {"schema": "ghc.family.v652-v1.runtime.v1", "count": len(results), "results": results, "all_accepted": all(row["accepted"] for row in results), "same_owner_only": True, "independent_reproduction": False}
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if payload["all_accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
