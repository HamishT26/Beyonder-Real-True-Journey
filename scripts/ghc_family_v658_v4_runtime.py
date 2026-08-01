#!/usr/bin/env python3
"""Reusable bounded hydrometric contract engine for Eiren v658-v4."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import ghc_family_v658_v4_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
PROPOSALS_BY_SLUG = {item["slug"]: item for item in d.PROPOSALS}
CLAIM_KEYS = [
    "real_data_or_records",
    "real_person_waterbody_land_station_instrument_or_measurement",
    "real_site_access_survey_installation_gauging_calibration_maintenance_repair_sampling_publication_or_forecast",
    "field_water_flood_traffic_electrical_height_weather_biosecurity_contamination_or_remote_safety_instruction",
    "empirical_gmut_confirmation_prediction_constraint_force_flow_or_material_law",
    "professional_or_operational_authority",
    "production_or_deployment",
    "water_allocation_resource_consent_land_access_warning_or_legal_authority",
    "cultural_or_traditional_knowledge_authority",
    "maori_authority",
    "affected_party_acceptance",
    "live_identity_key_proof_credential_status_or_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def obligations(mechanism: str) -> list[str]:
    normalized = mechanism.replace(" and ", ", ")
    return [part.strip(" .") for part in normalized.split(",") if part.strip(" .")]


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    required = obligations(proposal["mechanism"])
    fixture = {
        "fixture_id": f"{proposal['proposal_id']}-SYNTHETIC-VALID",
        "synthetic_only": True,
        "real_people_waterbodies_land_stations_instruments_measurements_or_records_used": False,
        "real_site_access_survey_installation_gauging_calibration_maintenance_repair_sampling_publication_or_forecast_used": False,
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used": False,
        "network_called": False,
        "external_rows": 0,
        "authority_granted": False,
        "executed_authority_action": False,
        "field_or_water_safety_instruction_performed": False,
        "obligations_present": required,
        "protected_claims": {key: False for key in CLAIM_KEYS},
    }
    return {
        "schema": "ghc.family.v658-v4.hydrometry-bounded-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "pillar_relation": proposal["pillar_relation"],
        "mechanism": proposal["mechanism"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "required_obligations": required,
        "protected_gates": proposal["protected_gates"],
        "outcome": proposal["expected_disposition"],
        "fixture": fixture,
        "boundary": (
            "Synthetic owner-local software evidence only; no real person, river, stream, catchment, station, reach, "
            "control, benchmark, sensor, recorder, telemetry system, field note, measurement, survey, site access, gauging, "
            "calibration, maintenance, repair, sampling, publication, forecast, land decision, water decision, or warning "
            "action; no water, flood, traffic, electrical, height, weather, biosecurity, contamination, remote-field, or "
            "emergency instruction; no empirical, professional, production, identity, legal, cultural, Māori-authority, "
            "independent-reproduction, Theory-of-Everything, or Stage 20 claim."
        ),
    }


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    proposal = PROPOSALS_BY_SLUG.get(contract.get("slug"))
    if proposal is None:
        return ["unknown_slug"]
    required_top = {
        "schema", "proposal_id", "slug", "title", "pillar_relation", "mechanism", "approval_class",
        "execution_lane", "source_ids", "required_obligations", "protected_gates", "outcome", "fixture", "boundary",
    }
    missing_top = sorted(required_top - set(contract))
    errors.extend(f"missing_top:{key}" for key in missing_top)
    if missing_top:
        return errors
    for key in ["proposal_id", "title", "pillar_relation", "mechanism", "approval_class", "execution_lane"]:
        expected_key = key if key != "proposal_id" else "proposal_id"
        if contract[key] != proposal[expected_key]:
            errors.append(f"{key}_mismatch")
    if contract["outcome"] != proposal["expected_disposition"]:
        errors.append("outcome_mismatch")
    if contract["outcome"] not in d.ALLOWED_OUTCOMES:
        errors.append("invalid_outcome")
    if contract["source_ids"] != proposal["official_or_primary_source_needs"]:
        errors.append("source_ids_mismatch")
    if contract["protected_gates"] != proposal["protected_gates"]:
        errors.append("protected_gates_mismatch")
    if contract["required_obligations"] != obligations(proposal["mechanism"]):
        errors.append("required_obligations_mismatch")

    fixture = contract["fixture"]
    required_fixture = {
        "fixture_id", "synthetic_only",
        "real_people_waterbodies_land_stations_instruments_measurements_or_records_used",
        "real_site_access_survey_installation_gauging_calibration_maintenance_repair_sampling_publication_or_forecast_used",
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used", "network_called", "external_rows",
        "authority_granted", "executed_authority_action", "field_or_water_safety_instruction_performed",
        "obligations_present", "protected_claims",
    }
    missing_fixture = sorted(required_fixture - set(fixture))
    errors.extend(f"missing_fixture:{key}" for key in missing_fixture)
    if missing_fixture:
        return errors
    if fixture["synthetic_only"] is not True:
        errors.append("synthetic_only_required")
    for key in [
        "real_people_waterbodies_land_stations_instruments_measurements_or_records_used",
        "real_site_access_survey_installation_gauging_calibration_maintenance_repair_sampling_publication_or_forecast_used",
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used", "network_called", "authority_granted",
        "executed_authority_action", "field_or_water_safety_instruction_performed",
    ]:
        if fixture[key] is not False:
            errors.append(f"{key}_must_be_false")
    if fixture["external_rows"] != 0:
        errors.append("external_rows_must_be_zero")
    if fixture["obligations_present"] != contract["required_obligations"]:
        errors.append("obligations_incomplete")
    if set(fixture["protected_claims"]) != set(CLAIM_KEYS):
        errors.append("protected_claim_key_mismatch")
    for key, value in fixture["protected_claims"].items():
        if value is not False:
            errors.append(f"protected_claim_true:{key}")
    if contract["outcome"] == "open_gap" and (fixture["network_called"] or fixture["external_rows"]):
        errors.append("open_gap_network_or_rows_forbidden")
    if contract["outcome"] == "exact_gate" and (fixture["authority_granted"] or fixture["executed_authority_action"]):
        errors.append("exact_gate_authority_forbidden")
    return sorted(set(errors))


def mutation_catalogue(contract: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["obligations_present"] = candidate["fixture"]["obligations_present"][1:]
    mutations.append({"mutation_id": "drop-domain-obligation", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["real_people_waterbodies_land_stations_instruments_measurements_or_records_used"] = True
    mutations.append({"mutation_id": "promote-real-station-record-or-measurement", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["field_or_water_safety_instruction_performed"] = True
    mutations.append({"mutation_id": "promote-field-or-water-safety-instruction", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["fixture"]["protected_claims"]["stage20"] = True
    mutations.append({"mutation_id": "promote-stage20", "candidate": candidate})

    candidate = copy.deepcopy(contract)
    candidate["outcome"] = "completed" if contract["outcome"] != "completed" else "promoted"
    mutations.append({"mutation_id": "alter-outcome", "candidate": candidate})
    return mutations


def evaluate_surface(slug: str) -> dict[str, Any]:
    proposal = PROPOSALS_BY_SLUG[slug]
    contract = build_contract(proposal)
    valid_errors = validate_contract(contract)
    mutation_results = []
    for mutation in mutation_catalogue(contract):
        errors = validate_contract(mutation["candidate"])
        mutation_results.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-{mutation['mutation_id']}",
                "rejected": bool(errors), "error_codes": errors, "credit": 0, "retained": True,
                "authority_action_executed": False,
            }
        )
    return {
        "contract": contract, "valid_errors": valid_errors, "mutation_results": mutation_results,
        "valid_fixture_passed": not valid_errors,
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_results),
        "all_mutations_rejected": all(row["rejected"] for row in mutation_results),
        "authority_action_executed": False,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run_named_surface(slug: str, output: str | None = None) -> dict[str, Any]:
    result = evaluate_surface(slug)
    receipt = {
        "schema": "ghc.family.v658-v4.runner-receipt.v1", "slug": slug,
        "proposal_id": result["contract"]["proposal_id"], "outcome": result["contract"]["outcome"],
        "valid_fixture_passed": result["valid_fixture_passed"],
        "rejected_mutation_count": result["rejected_mutation_count"], "expected_mutation_count": 5,
        "all_mutations_rejected": result["all_mutations_rejected"], "authority_action_executed": False,
        "same_owner_only": True, "independent_reproduction": False, "boundary": result["contract"]["boundary"],
    }
    if output:
        write_json(ROOT / output, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", required=True, choices=sorted(PROPOSALS_BY_SLUG))
    parser.add_argument("--output")
    args = parser.parse_args()
    receipt = run_named_surface(args.surface, args.output)
    print(json.dumps(receipt, ensure_ascii=True, sort_keys=True))
    if not receipt["valid_fixture_passed"] or not receipt["all_mutations_rejected"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
