#!/usr/bin/env python3
"""Bounded synthetic and structural runtime for Eiren v650-v7.

No function performs network I/O, opens user material, mutates sibling state,
or confers empirical, production, professional, legal, cultural, identity, or
Stage 20 authority.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import struct
from copy import deepcopy
from pathlib import Path
from typing import Any

import ghc_family_v650_v7_phase_data as d


OBLIGATIONS = {
    "saga-compensation": ["idempotency_key", "partial_failure", "reverse_compensation", "retry_budget", "deadline", "teardown"],
    "mvcc-write-skew": ["snapshot", "read_set", "write_set", "predicate_conflict", "serialization_refusal", "bounded_retry"],
    "tomonaga-schwinger": ["spacelike_hypersurface", "local_deformation", "integrability", "microcausality", "gauge_reservation", "observation_firewall"],
    "bogoliubov-causality": ["local_s_matrix", "support_ordering", "causal_factorization", "unitarity_reservation", "eft_domain", "observation_firewall"],
    "xmm-4xmm-dr14-zero-row": ["official_product", "quality_flags", "energy_bands", "selection", "uncertainty", "zero_row_firewall"],
    "aquatic-water-handover": ["water_test", "disinfectant", "ph", "dosing_hold", "sample_custody", "readback", "next_shift_owner"],
    "aquatic-safety-handover": ["rescue_equipment", "accessibility_closure", "plant_alarm", "incident_isolation", "accessible_notice", "readback"],
    "oauth-introspection": ["active_boolean", "endpoint_authentication", "audience", "inactive_minimization", "cache_boundary", "privacy"],
    "jwt-cnf-pop": ["single_key", "confirmation_claim", "recipient_confirmation", "key_binding", "replay", "correlation_minimization"],
    "aquatic-authority": ["affected_parties", "privacy", "accessible_notice", "remedy", "legal_reservation", "cultural_reservation", "maori_authority"],
    "git-packfile": ["pack_signature", "version", "object_count", "type_size_varint", "delta_depth", "inflated_size", "trailer_checksum"],
    "dwarf": ["unit_header", "abbreviation", "die", "attribute_form", "section_offset", "line_program", "depth_budget"],
    "accessible-search": ["search_landmark", "unique_label", "query_name", "results_status", "focus_return", "empty_state", "native_fallback"],
    "gouy-stodola-nonconversion": ["ambient_temperature", "entropy_generation", "exergy_destruction", "sign", "unit", "domain", "agency_refusal"],
    "complex-step": ["analyticity", "step_size", "branch_cut", "nonfinite", "reference_derivative", "error_bound", "unit"],
    "negative-control-nonpromotion": ["negative_exposure", "negative_outcome", "shared_confounding", "no_causal_effect", "measurement_error", "sensitivity", "nonpromotion"],
    "cose-hpke-draft": ["draft_version", "recipient_structure", "kem", "kdf", "aead", "protected_header", "external_aad", "nonfinal_status"],
    "bundle-protocol": ["primary_block", "canonical_block", "endpoint", "creation_time", "lifetime", "fragmentation", "crc", "block_budget"],
    "dns-master-file": ["origin", "owner_inheritance", "ttl", "class", "type", "rdata", "quoting", "include_refusal", "record_budget"],
    "json-lines": ["utf8", "bom_refusal", "one_value_per_line", "blank_line_refusal", "line_terminator", "record_count", "record_size", "truncation"],
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
    if proposal["slug"] == "cose-hpke-draft":
        fixture.update({"document_status": "active_internet_draft", "draft_version": "25", "final_rfc_claimed": False})
    return fixture


def specialized_witness(slug: str) -> dict[str, Any]:
    if slug == "saga-compensation":
        return {"forward": ["reserve", "charge", "dispatch_fail"], "compensation": ["refund", "release"], "reverse_order": True, "external_side_effects": 0}
    if slug == "mvcc-write-skew":
        return {"snapshot": {"a": True, "b": True}, "transactions": ["disable_a", "disable_b"], "predicate_conflict": True, "commit_result": "serialization_refused"}
    if slug == "tomonaga-schwinger":
        return {"state_functional": "typed_symbol", "local_deformations": 2, "integrability_obligation": "commutator_zero_for_spacelike_support", "physical_state": False}
    if slug == "bogoliubov-causality":
        return {"local_s_matrix": "typed_symbol", "support_order": ["earlier", "later"], "factorization_obligation": True, "scattering_measurement": False}
    if slug == "xmm-4xmm-dr14-zero-row":
        return {"queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0, "posterior_samples": 0, "constraints": 0, "empirical_claims": 0}
    if slug == "aquatic-water-handover":
        return {"trace": ["sample_logged", "disinfectant_low", "dosing_hold", "supervisor_escalated", "readback", "next_shift_accepts"], "people": 0, "plants": 0, "operational_decisions": 0}
    if slug == "aquatic-safety-handover":
        return {"trace": ["equipment_check", "access_route_blocked", "closure_recommended", "notice_drafted", "readback"], "patrons": 0, "incidents": 0, "real_closures": 0}
    if slug == "oauth-introspection":
        return {"vectors": [{"active": False}], "real_tokens": 0, "real_endpoints": 0, "inactive_extra_claims": 0}
    if slug == "jwt-cnf-pop":
        return {"vectors": [{"cnf": {"jkt": "synthetic-thumbprint"}}], "real_keys": 0, "possession_events": 0, "correlation_authority": False}
    if slug == "aquatic-authority":
        return {"matrix_cells": 12, "reservations": 12, "real_decisions": 0, "maori_authority_claimed": False}
    if slug == "git-packfile":
        header = b"PACK" + struct.pack(">II", 2, 0)
        return {"signature": header[:4].decode("ascii"), "version": struct.unpack(">I", header[4:8])[0], "object_count": struct.unpack(">I", header[8:12])[0], "untrusted_payload_read": False}
    if slug == "dwarf":
        header = struct.pack("<IHB", 7, 5, 1)
        return {"unit_length": struct.unpack("<I", header[:4])[0], "version": struct.unpack("<H", header[4:6])[0], "unit_type": header[6], "section_reads": 1}
    if slug == "accessible-search":
        return {"landmarks": 1, "unique_labels": True, "query_name": True, "status_live_region": True, "manual_evaluation": "reserved"}
    if slug == "gouy-stodola-nonconversion":
        ambient_k, entropy_j_per_k = 298.15, 2.0
        return {"ambient_temperature_k": ambient_k, "entropy_generation_j_per_k": entropy_j_per_k, "exergy_destruction_j": ambient_k * entropy_j_per_k, "agency_conversion": False}
    if slug == "complex-step":
        x, h = 0.4, 1e-20
        estimate = cmath.sin(x + 1j * h).imag / h
        return {"x": x, "step": h, "estimate": estimate, "reference": math.cos(x), "absolute_error": abs(estimate - math.cos(x)), "analytic": True}
    if slug == "negative-control-nonpromotion":
        return {"negative_exposure_no_effect_assumed": True, "negative_outcome_no_effect_assumed": True, "measurement_error_reserved": True, "participant_effect_estimated": False}
    if slug == "cose-hpke-draft":
        return {"version": "draft-ietf-cose-hpke-25", "status": "active_internet_draft", "suite": {"kem": "synthetic", "kdf": "synthetic", "aead": "synthetic"}, "final_rfc_claimed": False, "real_keys": 0}
    if slug == "bundle-protocol":
        return {"version": 7, "primary_blocks": 1, "canonical_blocks": 1, "crc_present": True, "real_bundles": 0}
    if slug == "dns-master-file":
        lines = ["$ORIGIN example.invalid.", "@ 3600 IN SOA ns hostmaster 1 2 3 4 5", "www 300 IN A 192.0.2.1"]
        return {"line_count": len(lines), "origin": "example.invalid.", "records": 2, "includes_opened": 0, "real_zone": False}
    if slug == "json-lines":
        raw = '{"a":1}\n[2,3]\n'
        rows = [json.loads(line) for line in raw.splitlines() if line]
        return {"utf8": True, "records": rows, "record_count": len(rows), "blank_lines": 0, "bom": False}
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
    if proposal["slug"] == "cose-hpke-draft" and (fixture.get("document_status") != "active_internet_draft" or fixture.get("final_rfc_claimed") is not False):
        issues.append("draft_status")
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
    parser = argparse.ArgumentParser(description="Run bounded Eiren v650-v7 proposal fixtures.")
    parser.add_argument("--proposal", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()
    selected = args.proposal or proposal_ids or [p["proposal_id"] for p in d.PROPOSALS]
    results = [execute(pid) for pid in selected]
    payload = {"schema": "ghc.family.v650-v7.runtime.v1", "results": results, "count": len(results), "all_accepted": all(r["accepted"] for r in results), "same_owner_only": True, "independent_reproduction": False}
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
