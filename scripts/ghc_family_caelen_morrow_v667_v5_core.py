#!/usr/bin/env python3
"""Bounded synthetic sight-record validators for Caelen Morrow v667-v5.

This module validates owner-local fictitious records only. It emits no
navigation, maritime, watchkeeping, position, route, instrument, safety,
professional, legal, cultural, Māori-authority, identity, production,
deployment, empirical, or Stage 20 authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

VACANCIES = [
    "real_person_or_participant",
    "real_vessel_or_voyage",
    "real_observation_or_instrument",
    "real_almanac_value",
    "real_time_or_angle",
    "real_coordinate_or_position",
    "real_route_or_weather_action",
    "real_professional_or_safety_decision",
    "real_legal_cultural_or_maori_authority",
    "real_key_or_proof",
    "real_network_data",
    "real_stage20_authority",
]

MODEL_NODES = {
    "CM6675-N001": ["body_token", "assumed_position_vacancy", "edition_pin", "cancellation", "navigation_refusal"],
    "CM6675-N002": ["frame", "index_arm", "micrometer", "telescope", "shades", "horizon_mirror", "state_abstention"],
    "CM6675-N003": ["capture_event", "time_annotation", "index_reading", "correction_event", "reduction_event", "plot_vacancy", "release_hold"],
    "CM6675-N004": ["utc", "ut1", "tt", "chronometer_error_vacancy", "provenance_epoch", "leap_context", "time_fix_refusal"],
    "CM6675-N005": ["sexagesimal_token", "sign", "limb_marker", "unit", "domain_range", "wrap_policy", "measured_angle_vacancy"],
    "CM6675-N006": ["index_correction", "dip", "refraction", "parallax", "semidiameter", "omission", "computed_altitude_vacancy"],
    "CM6675-N007": ["edition", "hour", "body_token", "gha_vacancy", "declination_vacancy", "aries_vacancy", "source_page_vacancy"],
    "CM6675-N008": ["horizon_cue", "visibility_cue", "cloud_cue", "glare_cue", "sea_state_cue", "suitability_abstention", "safety_abstention"],
    "CM6675-N009": ["intercept_sign", "azimuth_token", "plotting_vacancy", "coordinate_prohibition", "position_vacancy"],
    "CM6675-N010": ["sight_token_set", "body_diversity", "temporal_spacing", "intersection_vacancy", "disagreement_quarantine", "fix_vacancy"],
    "CM6675-N011": ["uncertainty_component", "covariance_vacancy", "sensitivity_slot", "correlation_refusal", "accuracy_refusal"],
    "CM6675-N012": ["asserted_time", "transaction_time", "supersession", "invalidation", "tombstone", "counterclaim", "nonrepudiation_refusal"],
    "CM6675-N013": ["heading_hierarchy", "label_association", "noncolour_cue", "reading_order", "manual_evaluation_reservation"],
    "CM6675-N014": ["zero_value_ledger", "recursive_key_order", "duplicate_key_rejection", "digest_placeholder", "signature_vacancy"],
    "CM6675-N015": ["luminous_cue_token", "attention_vacancy", "meaning_nonconversion", "agency_nonconversion", "identity_nonconversion", "personhood_nonconversion"],
    "CM6675-N016": ["masked_log", "equal_review_budget", "abstention_score", "stop_token", "handover", "observer_vacancy"],
    "CM6675-N017": ["source_derivation", "correction_invalidation", "minimization", "contested_attribution", "key_vacancy", "trust_refusal"],
    "CM6675-N018": ["spherical_frame", "null_geodesic", "propagation_term", "covariance_vacancy", "dimensional_guard", "empirical_firewall"],
    "CM6675-N019": ["linz_schema_pin", "usno_schema_pin", "transport_disabled", "zero_downloads", "zero_rows", "public_source_review_gap"],
    "CM6675-N020": ["competence_gate", "vessel_safety_gate", "route_choice_gate", "place_name_gate", "remedy_gate", "affected_party_gate", "maori_authority_gate"],
}

RUNNER_SELECTIONS = {
    "core": ["CM6675-N001", "CM6675-N003", "CM6675-N004", "CM6675-N005", "CM6675-N006"],
    "sight": ["CM6675-N001", "CM6675-N002", "CM6675-N003", "CM6675-N008", "CM6675-N010"],
    "temporal": ["CM6675-N004", "CM6675-N007", "CM6675-N012"],
    "angular": ["CM6675-N005", "CM6675-N009", "CM6675-N010", "CM6675-N018"],
    "corrections": ["CM6675-N006", "CM6675-N011", "CM6675-N012"],
    "provenance": ["CM6675-N007", "CM6675-N012", "CM6675-N013", "CM6675-N014"],
    "identity": ["CM6675-N015", "CM6675-N017"],
    "adapter": ["CM6675-N019", "CM6675-N020"],
    "validation": list(MODEL_NODES),
    "canonical": list(MODEL_NODES),
}


def strict_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    required = {
        "schema", "schema_version", "owner", "phase", "proposal_id", "title",
        "expected_disposition", "synthetic_only", "required_nodes", "nodes",
        "vacancies", "source_ids", "participant_count", "real_data_row_count",
        "network_call_count", "key_count", "proof_count", "authority_claim",
        "real_world_action", "navigation_output", "outcome_promotion",
        "protected_gates",
    }
    missing = sorted(required - set(contract))
    if missing:
        issues.append("missing_required_fields:" + ",".join(missing))
    if contract.get("schema") != "ghc-family-celestial-record-synthetic-contract-v1":
        issues.append("schema_mismatch")
    if contract.get("schema_version") != 1:
        issues.append("schema_version_must_be_integer_one")
    proposal_id = contract.get("proposal_id")
    if proposal_id not in MODEL_NODES:
        issues.append("unknown_proposal_id")
    else:
        absent = sorted(set(MODEL_NODES[proposal_id]) - set(contract.get("nodes", [])))
        if absent:
            issues.append("missing_required_nodes:" + ",".join(absent))
    if contract.get("owner") != "Caelen Morrow" or contract.get("phase") != "v667-v5":
        issues.append("owner_or_phase_mismatch")
    if contract.get("expected_disposition") not in ALLOWED_OUTCOMES:
        issues.append("invalid_outcome_label")
    if contract.get("synthetic_only") is not True:
        issues.append("synthetic_boundary_missing")
    if contract.get("vacancies") != VACANCIES:
        issues.append("vacancy_contract_mismatch")
    zero_fields = ("participant_count", "real_data_row_count", "network_call_count", "key_count", "proof_count")
    if any(contract.get(field) != 0 for field in zero_fields):
        issues.append("nonzero_real_or_external_count")
    if contract.get("authority_claim") is not None:
        issues.append("authority_claim_forbidden")
    if contract.get("real_world_action") is not False:
        issues.append("real_world_action_forbidden")
    if contract.get("navigation_output") is not None:
        issues.append("navigation_output_forbidden")
    if contract.get("outcome_promotion") is not None:
        issues.append("outcome_promotion_forbidden")
    if not contract.get("protected_gates"):
        issues.append("protected_gates_missing")
    return issues


def runner_self_test(kind: str) -> dict[str, Any]:
    proposal_ids = RUNNER_SELECTIONS.get(kind)
    if not proposal_ids:
        return {"kind": kind, "passed": False, "issues": ["unknown_runner_kind"]}
    rows = []
    for proposal_id in proposal_ids:
        contract_path = PHASE_ROOT / "x2" / "proposals" / proposal_id.casefold() / "contract.json"
        if not contract_path.is_file():
            rows.append({"proposal_id": proposal_id, "issues": ["contract_missing"], "passed": False})
            continue
        contract = strict_json(contract_path)
        issues = validate_contract(contract)
        rows.append({"proposal_id": proposal_id, "issues": issues, "passed": not issues})
    return {
        "schema": "ghc-family-caelen-v667-v5-runner-smoke-v1",
        "kind": kind,
        "proposal_count": len(rows),
        "results": rows,
        "passed": all(row["passed"] for row in rows),
        "real_world_actions": 0,
        "navigation_outputs": 0,
        "authority_claims": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", required=True)
    args = parser.parse_args()
    assert args.self_test
    result = runner_self_test("core")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
