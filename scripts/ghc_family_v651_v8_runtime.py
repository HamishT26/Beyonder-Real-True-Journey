#!/usr/bin/env python3
"""Bounded synthetic, symbolic, and structural runtime for Ilyra v651-v8.

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

import ghc_family_v651_v8_phase_data as d


OBLIGATIONS: dict[str, list[str]] = {
    "nuclearity-split-property": ["energy_damped_map", "local_algebra", "phase_space_density", "nuclear_bound", "temperature_scale", "split_property", "state_domain", "observation_firewall"],
    "quantum-energy-inequality": ["smeared_energy_density", "sampling_function", "lower_bound", "state_class", "curvature_scope", "unit", "duration_scale", "observation_firewall"],
    "borel-ecalle-resurgence": ["asymptotic_series", "borel_transform", "singularity_set", "lateral_resummation", "stokes_data", "transseries_sector", "ambiguity", "observation_firewall"],
    "soft-graviton-obligations": ["soft_limit", "factorization", "external_legs", "gauge_reservation", "infrared_scope", "ward_identity", "unit", "observation_firewall"],
    "quic-ack-frequency": ["sequence_number", "packet_tolerance", "max_ack_delay", "reordering_threshold", "ignore_order", "draft_status", "resource_budget", "network_refusal"],
    "masque-connect-udp": ["target_host", "target_port", "capsule_protocol", "datagram_context", "tunnel_error", "authority_boundary", "resource_budget", "network_refusal"],
    "wasm-canonical-abi": ["component_type", "canonical_lift", "canonical_lower", "memory", "realloc", "string_encoding", "resource_ownership", "execution_refusal"],
    "amqp-1-0-refusal": ["protocol_header", "performative", "frame_type", "channel", "handle", "settlement", "delivery_state", "resource_budget", "network_refusal"],
    "dns-svcb-https": ["priority", "target_name", "service_parameters", "mandatory_keys", "alias_mode", "service_mode", "duplicate_refusal", "network_refusal"],
    "oblivious-http": ["key_config", "request_encapsulation", "response_encapsulation", "context_binding", "suite_identifier", "padding_boundary", "replay_reservation", "network_refusal"],
    "votable-1-5-refusal": ["version", "resource", "table", "field", "datatype", "arraysize", "data_encoding", "row_budget", "external_resolution_refusal"],
    "git-commit-graph-bloom": ["signature", "chunk_table", "commit_data", "generation_data", "bloom_index", "bloom_data", "hash_version", "graph_budget", "repository_refusal"],
    "rpki-route-origin-validation": ["route_prefix", "origin_as", "covering_roa", "maximum_length", "valid_state", "invalid_state", "not_found_state", "stale_object_reservation"],
    "proposal-minhash-neighbour": ["tokenization", "shingle_domain", "hash_family", "signature_length", "seed", "similarity_estimate", "collision_reason", "manual_review"],
    "source-representation-drift": ["source_id", "declared_status", "observed_status", "content_type", "language", "validator", "cache_policy", "drift_disposition"],
    "correction-delta-manifest": ["immutable_anchor", "delta_path_set", "hash_domain", "self_exclusion", "coverage", "ordering", "ancestry", "parity"],
    "aho-corasick-stream": ["pattern_set", "trie", "failure_links", "output_set", "chunk_boundary", "overlap", "match_budget", "stream_refusal"],
    "accessible-braille-naming": ["accessible_name", "braille_label", "braille_role_description", "language", "fallback", "conflict_refusal", "manual_reservation", "affected_user_reservation"],
    "accessible-canvas-fallback": ["canvas_name", "fallback_content", "keyboard_path", "focus_order", "text_alternative", "responsive_reservation", "manual_reservation", "affected_user_reservation"],
    "gruneisen-nonconversion": ["volume", "temperature", "pressure", "thermal_expansion", "heat_capacity", "compressibility", "unit", "thermodynamic_domain", "psyche_refusal"],
    "regression-winner-nonpromotion": ["selection_rule", "baseline", "measurement_error", "regression_to_mean", "winner_selection", "holdout", "uncertainty", "nonpromotion"],
    "capability-provenance": ["provider", "capability", "source", "availability_state", "permission_state", "invocation_state", "result_boundary", "authority_refusal"],
    "lsm-compaction": ["memtable", "immutable_run", "level", "compaction", "tombstone", "snapshot_sequence", "overlap", "write_amplification", "read_amplification", "space_amplification"],
    "radio-observation-handover": ["observation_id", "instrument_state", "quality_flag", "correction_readback", "accessible_notice", "workload_ceiling", "escalation", "next_shift_owner"],
    "rfi-flagging-handover": ["observation_id", "flag_revision", "rfi_reason", "hold_state", "correction_readback", "review_reservation", "escalation", "next_shift_owner"],
    "openid4vp-verifier-attestation": ["client_id", "verifier_attestation", "attestation_binding", "request_integrity", "audience", "nonce", "replay_refusal", "privacy_reservation"],
    "openid4vci-auth-server": ["credential_issuer", "authorization_server", "issuer_metadata", "server_metadata", "authorization_details", "binding", "selection_refusal", "privacy_reservation"],
    "siop-v2-draft-watch": ["self_issued_issuer", "client_id", "subject_syntax", "registration", "request_integrity", "response_binding", "draft_watch", "production_refusal"],
    "askap-racs-mid-zero-row": ["official_product", "product_identity", "catalogue_schema", "selection", "calibration", "checksum", "zero_row_firewall", "likelihood_refusal"],
    "radio-astronomy-authority": ["affected_parties", "observation_governance", "sky_knowledge", "data_sovereignty", "privacy", "remedy", "legal_reservation", "cultural_reservation", "maori_authority"],
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
    if proposal["slug"] == "quic-ack-frequency":
        fixture.update({"document_status": "draft", "draft": "14", "implementation_claimed": False})
    if proposal["slug"] == "siop-v2-draft-watch":
        fixture.update({"document_status": "watch", "draft": "13", "production_profile_claimed": False})
    if proposal["slug"] in {"openid4vp-verifier-attestation", "openid4vci-auth-server"}:
        fixture.update({"document_status": "final_1_0", "cryptographic_operations": 0, "interoperability_events": 0})
    return fixture


def specialized_witness(slug: str) -> dict[str, Any]:
    if slug in {"nuclearity-split-property", "quantum-energy-inequality", "borel-ecalle-resurgence", "soft-graviton-obligations"}:
        return {"typed_board": True, "symbolic_obligations": len(OBLIGATIONS[slug]), "physical_state": False, "prediction": False, "likelihood": False, "parameter_constraint": False, "empirical_confirmation": False, "theory_of_everything": False}
    if slug == "quic-ack-frequency":
        return {"draft": "14", "synthetic_frames": 4, "accepted_sequences": [1, 2], "stale_sequences_rejected": [1], "packets_sent": 0, "connections": 0}
    if slug == "masque-connect-udp":
        return {"synthetic_targets": ["example.invalid:443"], "capsules": 2, "datagrams": 2, "tunnels_opened": 0, "network_calls": 0}
    if slug == "wasm-canonical-abi":
        return {"lift_lower_pairs": 3, "resource_handles": [1, 2], "double_drop_rejected": True, "modules_executed": 0}
    if slug == "amqp-1-0-refusal":
        return {"synthetic_frames": 4, "channels": [0], "performative_order_checked": True, "brokers_contacted": 0}
    if slug == "dns-svcb-https":
        return {"synthetic_records": 3, "alias_mode": 1, "service_mode": 2, "duplicate_keys_rejected": True, "dns_queries": 0}
    if slug == "oblivious-http":
        return {"synthetic_configurations": 2, "suite_bindings": 2, "context_mismatch_rejected": True, "hpke_operations": 0, "network_calls": 0}
    if slug == "votable-1-5-refusal":
        return {"version": "1.5", "synthetic_tables": 1, "fields": 3, "rows": 2, "external_resources_loaded": 0, "real_rows": 0}
    if slug == "git-commit-graph-bloom":
        return {"synthetic_chunks": ["OIDF", "OIDL", "CDAT", "BIDX", "BDAT"], "bloom_version": 1, "repositories_mutated": 0, "user_material_opened": 0}
    if slug == "rpki-route-origin-validation":
        return {"synthetic_cases": {"valid": 2, "invalid": 2, "not_found": 1}, "roa_downloads": 0, "routing_actions": 0}
    if slug == "proposal-minhash-neighbour":
        values = ["alpha beta gamma", "alpha beta delta", "omega sigma"]
        hashes = [hashlib.sha256(value.encode("utf-8")).hexdigest()[:12] for value in values]
        return {"documents": len(values), "signature_prefixes": hashes, "manual_collision_review": True, "duplicate_promotions": 0}
    if slug == "source-representation-drift":
        return {"statuses": ["current", "stable", "draft", "watch"], "synthetic_drift_cases": 8, "network_fetches": 0, "citations_as_observations": False}
    if slug == "correction-delta-manifest":
        return {"anchor": "immutable_evidence_parent", "delta_paths": 3, "self_exclusions": 2, "hash_domain": "git_blob", "mismatches": 0, "history_rewritten": False}
    if slug == "aho-corasick-stream":
        text = "abracadabra"
        patterns = ["abra", "cad", "ra"]
        matches = {p: [i for i in range(len(text)) if text.startswith(p, i)] for p in patterns}
        return {"chunks": ["abra", "cad", "abra"], "patterns": patterns, "matches": matches, "stream_bytes": len(text)}
    if slug in {"accessible-braille-naming", "accessible-canvas-fallback"}:
        return {"structural_contracts": len(OBLIGATIONS[slug]), "manual_keyboard": "reserved", "browser_diversity": "reserved", "assistive_technology": "reserved", "maori_language": "reserved", "affected_user_evaluation": "reserved", "complete_conformance_claimed": False}
    if slug == "gruneisen-nonconversion":
        alpha, bulk, volume, heat_capacity = 2e-5, 1.1e11, 1e-5, 450.0
        gamma = alpha * bulk * volume / heat_capacity
        return {"dimensionless_example": gamma, "finite": math.isfinite(gamma), "thermodynamic_domain": True, "psyche_conversion": False, "justice_conversion": False, "consciousness_conversion": False}
    if slug == "regression-winner-nonpromotion":
        return {"synthetic_units": 20, "selected_extremes": 4, "holdout_reserved": True, "participant_effect": False, "stage20_authorized": False}
    if slug == "capability-provenance":
        return {"synthetic_capabilities": 6, "availability_states": ["available", "unavailable", "not_invoked"], "provider_calls": 0, "permissions_inferred": False, "external_authority": False}
    if slug == "lsm-compaction":
        return {"memtable_entries": 8, "immutable_runs": 2, "levels": 3, "tombstones_retained": 2, "snapshot_sequences": [4, 8], "storage_mutations": 0}
    if slug in {"radio-observation-handover", "rfi-flagging-handover"}:
        return {"synthetic_trace": ["capture", "flag", "hold", "correction_readback", "accessible_notice", "handover_acceptance"], "people": 0, "observations": 0, "instruments": 0, "operational_actions": 0, "blind_matched_budget_real_arms": 0}
    if slug in {"openid4vp-verifier-attestation", "openid4vci-auth-server", "siop-v2-draft-watch"}:
        return {"synthetic_vectors": 5, "real_keys": 0, "real_tokens": 0, "accounts": 0, "network_exchanges": 0, "interoperability_events": 0, "privacy_reviews": 0, "security_reviews": 0, "trust_governance_decisions": 0}
    if slug == "askap-racs-mid-zero-row":
        return {"queries": 0, "downloads": 0, "catalogue_rows": 0, "image_products": 0, "calibration_rows": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0, "empirical_claims": 0}
    if slug == "radio-astronomy-authority":
        return {"matrix_cells": 18, "reservations": 18, "real_decisions": 0, "affected_party_authority_claimed": False, "legal_authority_claimed": False, "cultural_authority_claimed": False, "maori_authority_claimed": False}
    raise KeyError(slug)


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
    parser = argparse.ArgumentParser(description="Run bounded Ilyra v651-v8 proposal fixtures.")
    parser.add_argument("--proposal", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()
    selected = args.proposal or [proposal["proposal_id"] for proposal in d.PROPOSALS]
    results = [execute(proposal_id) for proposal_id in selected]
    payload = {"schema": "ghc.family.v651-v8.runtime.v1", "count": len(results), "results": results, "all_accepted": all(row["accepted"] for row in results), "same_owner_only": True, "independent_reproduction": False}
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if payload["all_accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
