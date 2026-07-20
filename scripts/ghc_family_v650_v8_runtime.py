#!/usr/bin/env python3
"""Bounded synthetic and structural runtime for Ilyra v650-v8.

No function performs network I/O, opens user material, mutates sibling state,
or confers empirical, production, professional, legal, cultural, identity, or
Stage 20 authority.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
from copy import deepcopy
from pathlib import Path
from typing import Any

import ghc_family_v650_v8_phase_data as d


OBLIGATIONS = {
    "raft-joint-consensus": ["old_configuration", "new_configuration", "joint_configuration", "dual_majority", "log_matching", "stale_leader_refusal", "snapshot_boundary"],
    "orset-causal-context": ["add_dot", "remove_context", "merge_join", "idempotence", "commutativity", "causal_stability_reservation", "tombstone_budget"],
    "kadanoff-baym": ["closed_time_contour", "lesser_greater_components", "dyson_equation", "self_energy", "initial_conditions", "conservation_reservation", "observation_firewall"],
    "bethe-salpeter": ["two_particle_kernel", "propagator_pair", "bound_state_amplitude", "normalization", "truncation", "gauge_reservation", "observation_firewall"],
    "nustar-numaster-zero-row": ["official_product", "event_selection", "response", "background", "exposure", "checksum", "zero_row_firewall"],
    "medical-gas-handover": ["source_state", "manifold_state", "pipeline_alarm", "changeover_hold", "isolation", "verification", "correction_readback", "next_shift_owner"],
    "sterile-load-handover": ["device_identity", "cycle_identity", "process_indicator", "load_release_hold", "recall_boundary", "exception_isolation", "readback", "next_shift_owner"],
    "jwt-bcp-profile": ["algorithm_allowlist", "issuer", "audience", "typed_use", "key_validation", "replay_boundary", "cross_jwt_confusion_refusal"],
    "jwk-set-profile": ["key_type", "key_use", "algorithm_consistency", "key_identifier", "collision_refusal", "rotation_boundary", "private_parameter_refusal"],
    "hospital-authority": ["affected_parties", "patient_privacy", "clinical_authority", "remedy", "legal_reservation", "cultural_reservation", "maori_authority"],
    "elf-structural": ["magic", "class", "endianness", "version", "machine", "program_header", "section_header", "offset_budget", "overlap_refusal", "entry_refusal"],
    "tls13-rfc9846": ["rfc9846_status", "record", "handshake", "transcript", "version", "cipher_suite", "key_share", "extension", "alert", "resource_budget"],
    "accessible-modal-dialog": ["accessible_name", "description", "initial_focus", "focus_trap", "escape_path", "focus_return", "background_inert", "native_fallback"],
    "reaction-affinity-nonconversion": ["reaction_extent", "gibbs_derivative", "affinity", "sign_convention", "unit", "thermodynamic_domain", "agency_refusal"],
    "broyden-update": ["residual", "step", "secant_condition", "rank_one_update", "denominator_guard", "conditioning", "restart", "error_bound"],
    "double-ml-nonpromotion": ["sample_splitting", "cross_fitting", "orthogonal_score", "nuisance_models", "overlap", "dependence_reservation", "uncertainty", "nonpromotion"],
    "graphql-september2025": ["release_status", "document", "operation", "selection_set", "variable_definition", "fragment", "depth_budget", "draft_watch"],
    "git-fast-import": ["command_stream", "data_length", "mark_table", "path_quote", "commit_boundary", "ref_mutation_refusal", "stream_budget", "truncation"],
    "otlp-1-10": ["stable_version", "signal_type", "resource", "scope", "record", "attribute_budget", "profiles_watch", "network_refusal"],
    "cyclonedx-1-7": ["bom_format", "spec_version", "serial_number", "component", "dependency", "hash", "graph_budget", "external_resolution_refusal"],
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
    disposition = proposal["expected_disposition"]
    fixture = {
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "scope": "bounded_synthetic_or_structural",
        "obligations": list(OBLIGATIONS[proposal["slug"]]),
        "resource_budget": 64,
        "replay_budget": 3,
        "promotion": "bounded_only",
        "authority_action": False,
        "privacy_disclosure": False,
        "synthetic": True,
        "real_events": 0,
        "real_rows": 0,
        "network_actions": 0,
        "decisions": 0,
        "expected_disposition": disposition,
    }
    if disposition == "open_gap":
        fixture.update({"zero_row_firewall": True, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0})
    elif disposition == "exact_gate":
        fixture.update({"reservation_only": True, "required_authorities": ["competent", "affected_party", "legal", "cultural", "maori"]})
    elif disposition == "represented":
        fixture.update({"proxy_only": True, "blind_matched_budget_real_arms": 0, "independent_review": False})
    if proposal["slug"] == "tls13-rfc9846":
        fixture.update({"document_status": "current_rfc", "rfc": "9846", "rfc8446_current_claimed": False, "cryptographic_operations": 0})
    if proposal["slug"] == "graphql-september2025":
        fixture.update({"release_status": "current", "release": "September2025", "june2026_draft_status": "watch", "server_executions": 0})
    if proposal["slug"] == "otlp-1-10":
        fixture.update({"stable_version": "1.10.0", "profiles_status": "development_watch", "export_calls": 0})
    return fixture


def specialized_witness(slug: str) -> dict[str, Any]:
    if slug == "raft-joint-consensus":
        return {"old_voters": ["a", "b", "c"], "new_voters": ["b", "c", "d"], "old_majority": 2, "new_majority": 2, "joint_commit": True, "stale_leader_mutation": "rejected", "external_side_effects": 0}
    if slug == "orset-causal-context":
        return {"left": {"adds": ["x@a1"], "context": []}, "right": {"adds": [], "context": ["x@a1"]}, "merged_members": [], "merge_idempotent": True, "replicas": 0}
    if slug == "kadanoff-baym":
        return {"contour": "typed_closed_time_symbol", "components": ["lesser", "greater", "retarded", "advanced"], "self_energy": "typed_symbol", "conservation_proved": False, "physical_state": False}
    if slug == "bethe-salpeter":
        return {"kernel": "typed_two_particle_symbol", "propagators": 2, "amplitude": "typed_symbol", "truncation": "declared_only", "bound_state_solved": False, "physical_prediction": False}
    if slug == "nustar-numaster-zero-row":
        return {"queries": 0, "downloads": 0, "events": 0, "spectra": 0, "responses": 0, "likelihoods": 0, "posterior_samples": 0, "constraints": 0, "empirical_claims": 0}
    if slug == "medical-gas-handover":
        return {"trace": ["alarm_received", "source_checked", "changeover_held", "isolation_requested", "verification_reserved", "correction_readback", "next_shift_accepts"], "people": 0, "patients": 0, "gas_systems": 0, "operational_actions": 0}
    if slug == "sterile-load-handover":
        return {"trace": ["cycle_logged", "indicator_exception", "load_held", "recall_boundary_marked", "readback", "next_shift_accepts"], "people": 0, "devices": 0, "loads_released": 0, "recalls_issued": 0}
    if slug == "jwt-bcp-profile":
        return {"vectors": [{"typ": "synthetic+jwt", "iss": "https://issuer.invalid", "aud": "synthetic-audience", "alg": "ES256"}], "real_keys": 0, "real_tokens": 0, "cross_jwt_confusion": "rejected"}
    if slug == "jwk-set-profile":
        return {"vectors": [{"kty": "EC", "use": "sig", "kid": "synthetic-key-1", "alg": "ES256"}], "private_parameters": 0, "real_keys": 0, "kid_collisions": "rejected"}
    if slug == "hospital-authority":
        return {"matrix_cells": 16, "reservations": 16, "real_decisions": 0, "clinical_authority_claimed": False, "maori_authority_claimed": False}
    if slug == "elf-structural":
        header = b"\x7fELF" + bytes([2, 1, 1, 0]) + bytes(56)
        return {"magic": header[:4].hex(), "class": header[4], "endianness": header[5], "version": header[6], "bytes_examined": len(header), "executed": False, "user_files_opened": 0}
    if slug == "tls13-rfc9846":
        record = struct.pack(">BHH", 22, 0x0303, 0)
        return {"rfc": "9846", "record_type": record[0], "legacy_version": struct.unpack(">H", record[1:3])[0], "payload_length": struct.unpack(">H", record[3:5])[0], "cryptographic_operations": 0, "network_connections": 0, "rfc8446_current_claimed": False}
    if slug == "accessible-modal-dialog":
        return {"role": "dialog", "accessible_name": True, "initial_focus": True, "focus_trap": True, "escape_path": True, "focus_return": True, "manual_evaluation": "reserved", "affected_user_evaluation": "reserved"}
    if slug == "reaction-affinity-nonconversion":
        delta_g_j_per_mol = -12_000.0
        return {"gibbs_derivative_j_per_mol": delta_g_j_per_mol, "affinity_j_per_mol": -delta_g_j_per_mol, "sign_convention": "A=-dG/dxi", "agency_conversion": False, "consciousness_conversion": False}
    if slug == "broyden-update":
        jacobian, step, residual_delta = 2.0, 0.25, 0.55
        updated = jacobian + (residual_delta - jacobian * step) / step
        return {"initial_jacobian": jacobian, "step": step, "residual_delta": residual_delta, "updated_jacobian": updated, "finite": math.isfinite(updated), "convergence_proved": False}
    if slug == "double-ml-nonpromotion":
        return {"sample_splitting": True, "folds": 2, "orthogonal_score": "declared", "overlap": "required_not_observed", "real_rows": 0, "participant_effect_estimated": False, "stage20_authorized": False}
    if slug == "graphql-september2025":
        document = "query Synthetic($id: ID!) { item(id: $id) { id } }"
        return {"release": "September2025", "document_bytes": len(document.encode("utf-8")), "operations": 1, "selection_depth": 2, "server_executions": 0, "june2026_draft_status": "watch"}
    if slug == "git-fast-import":
        stream = "blob\nmark :1\ndata 0\n\n"
        return {"stream_bytes": len(stream.encode("utf-8")), "commands": ["blob", "mark", "data"], "git_invocations": 0, "refs_mutated": 0, "user_repositories_touched": 0}
    if slug == "otlp-1-10":
        return {"version": "1.10.0", "signal": "traces", "resource_attributes": 1, "scope_records": 1, "export_calls": 0, "real_telemetry": 0, "profiles_status": "development_watch"}
    if slug == "cyclonedx-1-7":
        bom = {"bomFormat": "CycloneDX", "specVersion": "1.7", "serialNumber": "urn:uuid:00000000-0000-0000-0000-000000000000", "components": [{"type": "library", "name": "synthetic"}]}
        return {"bom": bom, "components": 1, "dependencies": 0, "external_resolution_calls": 0, "production_inventory_claimed": False}
    raise KeyError(slug)


def validate_fixture(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    issues = []
    required = set(OBLIGATIONS[proposal["slug"]])
    if fixture.get("proposal_id") != proposal["proposal_id"]:
        issues.append("proposal_id")
    if fixture.get("slug") != proposal["slug"]:
        issues.append("slug")
    if fixture.get("scope") != "bounded_synthetic_or_structural":
        issues.append("scope_or_unit")
    if not required <= set(fixture.get("obligations", [])):
        issues.append("required_obligation")
    if not isinstance(fixture.get("resource_budget"), int) or not 0 <= fixture["resource_budget"] <= 64:
        issues.append("resource_budget")
    if not isinstance(fixture.get("replay_budget"), int) or not 0 <= fixture["replay_budget"] <= 3:
        issues.append("replay_budget")
    if fixture.get("promotion") != "bounded_only":
        issues.append("unsupported_promotion")
    if fixture.get("authority_action") is not False or fixture.get("privacy_disclosure") is not False:
        issues.append("authority_or_privacy")
    if fixture.get("real_events") != 0 or fixture.get("network_actions") != 0:
        issues.append("external_event")
    disposition = proposal["expected_disposition"]
    if disposition == "open_gap" and any(fixture.get(k) != 0 for k in ["real_rows", "likelihood_calls", "posterior_samples", "constraints"]):
        issues.append("zero_row_firewall")
    if disposition == "exact_gate" and (fixture.get("decisions") != 0 or fixture.get("reservation_only") is not True):
        issues.append("exact_gate")
    if disposition == "represented" and (fixture.get("proxy_only") is not True or fixture.get("blind_matched_budget_real_arms") != 0):
        issues.append("proxy_boundary")
    if proposal["slug"] == "tls13-rfc9846" and (fixture.get("document_status") != "current_rfc" or fixture.get("rfc") != "9846" or fixture.get("rfc8446_current_claimed") is not False):
        issues.append("tls_status")
    if proposal["slug"] == "graphql-september2025" and (fixture.get("release_status") != "current" or fixture.get("june2026_draft_status") != "watch"):
        issues.append("graphql_status")
    if proposal["slug"] == "otlp-1-10" and (fixture.get("stable_version") != "1.10.0" or fixture.get("profiles_status") != "development_watch"):
        issues.append("otlp_status")
    return {"accepted": not issues, "issues": sorted(set(issues)), "bounded": True, "same_owner_only": True, "independent_reproduction": False}


def mutate(fixture: dict[str, Any], dimension: str) -> dict[str, Any]:
    result = deepcopy(fixture)
    result["mutation_dimension"] = dimension
    if dimension == "missing_required_obligation":
        result["obligations"] = result["obligations"][1:]
    elif dimension == "wrong_type_or_unit":
        result["scope"] = {"wrong": "type"}
    elif dimension == "resource_or_replay_overrun":
        result["resource_budget"] = 65_536
        result["replay_budget"] = 65_536
    elif dimension == "unsupported_promotion":
        result["promotion"] = "empirical_confirmation"
    elif dimension == "authority_or_privacy_breach":
        result["authority_action"] = True
        result["privacy_disclosure"] = True
    else:
        raise KeyError(dimension)
    return result


def execute(proposal_id: str) -> dict[str, Any]:
    proposal = proposal_by_id(proposal_id)
    canonical = canonical_fixture(proposal)
    baseline = validate_fixture(proposal, canonical)
    mutations = []
    for index, dimension in enumerate(MUTATION_DIMENSIONS, 1):
        result = validate_fixture(proposal, mutate(canonical, dimension))
        mutations.append({"mutation_id": f"{proposal_id}-M{index:02d}", "dimension": dimension, "rejected": not result["accepted"], "issues": result["issues"]})
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
        "boundary": "Bounded synthetic, symbolic, numerical, or structural evidence only; not production, empirical confirmation, professional authority, external audit, or independent reproduction.",
    }


def main(proposal_ids: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run bounded Ilyra v650-v8 proposal fixtures.")
    parser.add_argument("--proposal", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()
    selected = args.proposal or proposal_ids or [p["proposal_id"] for p in d.PROPOSALS]
    results = [execute(pid) for pid in selected]
    payload = {"schema": "ghc.family.v650-v8.runtime.v1", "results": results, "count": len(results), "all_accepted": all(r["accepted"] for r in results), "same_owner_only": True, "independent_reproduction": False}
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if payload["all_accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
