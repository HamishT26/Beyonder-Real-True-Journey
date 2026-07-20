#!/usr/bin/env python3
"""Bounded synthetic, symbolic, structural, and zero-row runtime for v650-v6."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import ghc_family_v650_v6_phase_data as d


PROPOSALS = {row["proposal_id"]: row for row in d.PROPOSALS}
MUTATION_KINDS = (
    "missing_required_obligation",
    "wrong_proposal_identity",
    "unsupported_claim_promotion",
    "resource_budget_exceeded",
    "protected_lane_breach",
)

OBLIGATIONS: dict[str, list[str]] = {
    "V6506-P01": ["even_odd_generation", "writer_serialization", "reader_retry", "pointer_lifetime", "starvation_fallback", "wraparound", "teardown"],
    "V6506-P02": ["record_length", "checksum", "transaction_boundary", "torn_tail", "group_commit", "checkpoint", "replay_truncation", "idempotency"],
    "V6506-P03": ["relative_entropy", "support", "normalization", "positivity", "first_variation", "entanglement_first_law", "region_domain", "state_domain"],
    "V6506-P04": ["hypersurface_functional", "canonical_data", "characteristic_flow", "constraint", "integrability", "boundary_data", "gauge", "eft_scope"],
    "V6506-P05": ["catalog_schema", "spectrum_schema", "light_curve_schema", "selection", "exposure", "uncertainty", "checksum", "zero_row_refusal"],
    "V6506-P06": ["accession", "lot_lineage", "quarantine", "moisture", "viability_test", "regeneration_refusal", "safety_duplication", "handover"],
    "V6506-P07": ["environmental_alarm", "cold_room_excursion", "backup_power", "affected_lot_hold", "escalation", "recovery_check", "accessible_notice", "next_shift_owner"],
    "V6506-P08": ["issuer", "audience", "subject_match", "signed_response", "encrypted_response", "claim_minimization", "aggregated_claim", "algorithm_refusal"],
    "V6506-P09": ["sector_identifier", "redirect_set", "nonreversible_derivation", "rotation", "migration", "collision_reservation", "correlation_limit", "nonproduction"],
    "V6506-P10": ["accession_consent", "provenance", "biocultural_minimization", "duplicate_location", "access", "return", "benefit_sharing", "maori_authority"],
    "V6506-P11": ["framing_indicator", "known_length", "indeterminate_length", "control_data", "field_lines", "content", "padding", "trailer"],
    "V6506-P12": ["content_digest", "representation_digest", "dictionary", "multiple_algorithms", "unsupported_algorithm", "mismatch", "selection", "refusal"],
    "V6506-P13": ["identification", "method", "flags", "optional_fields", "header_crc", "member", "trailer_crc", "ratio_budget"],
    "V6506-P14": ["details_reference", "error_reference", "invalid_state", "visibility", "navigation", "name_description_separation", "fallback", "manual_reservation"],
    "V6506-P15": ["name", "range", "value", "orientation", "keyboard", "text_alternative", "noncolour_cue", "focus"],
    "V6506-P16": ["massieu_potential", "planck_potential", "legendre_transform", "natural_variables", "temperature", "entropy", "equilibrium_domain", "unit"],
    "V6506-P17": ["single_rounding", "rounding_direction", "signed_zero", "subnormal", "infinity", "nan", "exception_flag", "reproducibility_scope"],
    "V6506-P18": ["sfnt_version", "table_count", "search_parameters", "sorted_tags", "duplicate_tags", "offset_length", "alignment_overlap", "checksum"],
    "V6506-P19": ["root", "child", "descendant", "index", "slice", "filter", "function_type", "result_budget"],
    "V6506-P20": ["mediator", "treatment_mediator_path", "mediator_outcome_path", "backdoor_blockade", "unmeasured_confounding", "positivity", "consistency", "sensitivity"],
}


def canonical_fixture(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSALS[proposal_id]
    fixture: dict[str, Any] = {
        "proposal_id": proposal_id,
        "outcome": proposal["expected_disposition"],
        "obligations": list(OBLIGATIONS[proposal_id]),
        "claim": "bounded_only",
        "resource_units": 8,
        "resource_budget": 64,
        "negative_retention": True,
        "external_side_effects": 0,
        "production_claim": False,
        "empirical_claim": False,
        "authority_claim": False,
        "independent_reproduction_claim": False,
        "stage20_promoted": False,
    }
    if proposal["expected_disposition"] == "represented":
        fixture.update(real_entities=0, real_events=0, blind_matched_budget_arms=0)
    if proposal["expected_disposition"] == "open_gap":
        fixture.update(downloaded_rows=0, likelihood_evaluations=0, posterior_samples=0, empirical_constraints=0)
    if proposal["expected_disposition"] == "exact_gate":
        fixture.update(software_decisions=0, authority_state="reserved")
    if proposal_id in {"V6506-P03", "V6506-P04"}:
        fixture.update(physical_state_claim=False, theory_of_everything=False, observation_rows=0)
    if proposal_id in {"V6506-P08", "V6506-P09"}:
        fixture.update(real_keys=0, real_tokens=0, live_interoperability_events=0)
    if proposal_id in {"V6506-P11", "V6506-P12", "V6506-P13", "V6506-P18", "V6506-P19"}:
        fixture.update(untrusted_external_inputs=0, exhaustive_security_claim=False)
    if proposal_id in {"V6506-P14", "V6506-P15"}:
        fixture.update(manual_evaluation_reserved=True, affected_user_evaluation_reserved=True, complete_accessibility_claim=False)
    if proposal_id == "V6506-P16":
        fixture.update(psyche_conversion=False, agency_conversion=False, consciousness_claim=False)
    if proposal_id == "V6506-P17":
        fixture.update(cross_platform_proof=False)
    if proposal_id == "V6506-P20":
        fixture.update(participant_effect_estimates=0, causal_effect_claim=False)
    return fixture


def evaluate_fixture(proposal_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    proposal = PROPOSALS[proposal_id]
    reasons: list[str] = []
    if fixture.get("proposal_id") != proposal_id:
        reasons.append("wrong_proposal_identity")
    missing = sorted(set(OBLIGATIONS[proposal_id]) - set(fixture.get("obligations", [])))
    if missing:
        reasons.append("missing_required_obligation")
    if fixture.get("outcome") != proposal["expected_disposition"]:
        reasons.append("wrong_outcome_lane")
    if fixture.get("claim") != "bounded_only" or any(
        fixture.get(key) is True
        for key in (
            "production_claim", "empirical_claim", "authority_claim",
            "independent_reproduction_claim", "stage20_promoted",
        )
    ):
        reasons.append("unsupported_claim_promotion")
    if fixture.get("resource_units", 0) > fixture.get("resource_budget", -1):
        reasons.append("resource_budget_exceeded")
    if fixture.get("negative_retention") is not True or fixture.get("external_side_effects") != 0:
        reasons.append("protected_lane_breach")

    disposition = proposal["expected_disposition"]
    if disposition == "represented" and any(
        fixture.get(key) != 0 for key in ("real_entities", "real_events", "blind_matched_budget_arms")
    ):
        reasons.append("protected_lane_breach")
    if disposition == "open_gap" and any(
        fixture.get(key) != 0 for key in ("downloaded_rows", "likelihood_evaluations", "posterior_samples", "empirical_constraints")
    ):
        reasons.append("protected_lane_breach")
    if disposition == "exact_gate" and (
        fixture.get("software_decisions") != 0 or fixture.get("authority_state") != "reserved"
    ):
        reasons.append("protected_lane_breach")

    if proposal_id in {"V6506-P03", "V6506-P04"} and (
        fixture.get("physical_state_claim") is not False
        or fixture.get("theory_of_everything") is not False
        or fixture.get("observation_rows") != 0
    ):
        reasons.append("protected_lane_breach")
    if proposal_id in {"V6506-P08", "V6506-P09"} and any(
        fixture.get(key) != 0 for key in ("real_keys", "real_tokens", "live_interoperability_events")
    ):
        reasons.append("protected_lane_breach")
    if proposal_id in {"V6506-P14", "V6506-P15"} and (
        fixture.get("manual_evaluation_reserved") is not True
        or fixture.get("affected_user_evaluation_reserved") is not True
        or fixture.get("complete_accessibility_claim") is not False
    ):
        reasons.append("protected_lane_breach")
    if proposal_id == "V6506-P16" and any(
        fixture.get(key) is not False for key in ("psyche_conversion", "agency_conversion", "consciousness_claim")
    ):
        reasons.append("protected_lane_breach")
    if proposal_id == "V6506-P20" and (
        fixture.get("participant_effect_estimates") != 0
        or fixture.get("causal_effect_claim") is not False
    ):
        reasons.append("protected_lane_breach")

    unique = sorted(set(reasons))
    return {
        "proposal_id": proposal_id,
        "accepted": not unique,
        "reasons": unique or ["bounded_contract_pass"],
        "outcome": proposal["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def mutated_fixture(proposal_id: str, kind: str) -> dict[str, Any]:
    fixture = copy.deepcopy(canonical_fixture(proposal_id))
    if kind == "missing_required_obligation":
        fixture["obligations"] = fixture["obligations"][1:]
    elif kind == "wrong_proposal_identity":
        fixture["proposal_id"] = "V6506-PXX"
    elif kind == "unsupported_claim_promotion":
        fixture["claim"] = "production_or_empirical_promotion"
        fixture["production_claim"] = True
    elif kind == "resource_budget_exceeded":
        fixture["resource_units"] = fixture["resource_budget"] + 1
    elif kind == "protected_lane_breach":
        disposition = PROPOSALS[proposal_id]["expected_disposition"]
        if disposition == "represented":
            fixture["real_events"] = 1
        elif disposition == "open_gap":
            fixture["downloaded_rows"] = 1
        elif disposition == "exact_gate":
            fixture["software_decisions"] = 1
        else:
            fixture["negative_retention"] = False
    else:
        raise ValueError(f"unknown mutation kind: {kind}")
    return fixture


def execute_proposal(proposal_id: str) -> dict[str, Any]:
    canonical = canonical_fixture(proposal_id)
    canonical_result = evaluate_fixture(proposal_id, canonical)
    mutations = []
    for index, kind in enumerate(MUTATION_KINDS, 1):
        result = evaluate_fixture(proposal_id, mutated_fixture(proposal_id, kind))
        mutations.append({
            "mutation_id": f"{proposal_id}-M{index:02d}",
            "kind": kind,
            "accepted": result["accepted"],
            "reasons": result["reasons"],
            "result": "unexpected_accept" if result["accepted"] else "rejected",
        })
    return {
        "proposal_id": proposal_id,
        "canonical_fixture": canonical,
        "canonical_result": canonical_result,
        "mutations": mutations,
        "passed": canonical_result["accepted"] and all(not row["accepted"] for row in mutations),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal-id", choices=sorted(PROPOSALS), required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = execute_proposal(args.proposal_id)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(encoded, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
