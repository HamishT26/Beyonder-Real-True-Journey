#!/usr/bin/env python3
"""Reusable bounded volcanic-observatory assurance contract engine for v658-v6."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import ghc_family_v658_v6_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_BY_SLUG = {item["slug"]: item for item in d.PROPOSALS}
CLAIM_KEYS = [
    "real_data_or_records",
    "real_person_maunga_volcano_observatory_station_instrument_location_observation_or_sample",
    "real_download_ingestion_processing_interpretation_diagnosis_forecast_alert_publication_or_operational_decision",
    "empirical_gmut_confirmation_prediction_constraint_force_or_material_law",
    "blind_matched_budget_thos_real_arms_or_independent_review",
    "professional_or_operational_authority",
    "production_or_deployment",
    "legal_or_cultural_authority",
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
RUNNER_GROUPS = {
    name: [item["slug"] for item in d.PROPOSALS[index * 3 : (index + 1) * 3]]
    for index, (name, _) in enumerate(d.RUNNER_SPECS)
}


def obligations(mechanism: str) -> list[str]:
    normalized = mechanism.replace(" and ", ", ")
    return [part.strip(" .") for part in normalized.split(",") if part.strip(" .")]


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    required = obligations(proposal["mechanism"])
    fixture = {
        "fixture_id": f"{proposal['proposal_id']}-SYNTHETIC-VALID",
        "synthetic_only": True,
        "real_people_maunga_volcanoes_observatories_stations_instruments_locations_waveforms_images_samples_coordinates_or_datasets_used": False,
        "real_download_ingestion_processing_interpretation_diagnosis_forecast_alert_publication_or_operational_decision_used": False,
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used": False,
        "network_called": False,
        "external_rows": 0,
        "authority_granted": False,
        "authority_action_executed": False,
        "empirical_claim_made": False,
        "obligations_present": required,
        "protected_claims": {key: False for key in CLAIM_KEYS},
    }
    return {
        "schema": "ghc.family.v658-v6.volcano-bounded-contract.v1",
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
        "boundary": "Synthetic owner-local software evidence only; zero real people, maunga, volcanoes, observatories, stations, instruments, locations, waveforms, images, samples, coordinates, observations, diagnosis, forecast, alert, hazard message, publication, authority action, live identity, or deployment; no empirical, professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, Theory-of-Everything, or Stage 20 claim.",
    }


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    proposal = PROPOSALS_BY_SLUG.get(contract.get("slug"))
    if proposal is None:
        return ["unknown_slug"]
    required_top = {"schema", "proposal_id", "slug", "title", "pillar_relation", "mechanism", "approval_class", "execution_lane", "source_ids", "required_obligations", "protected_gates", "outcome", "fixture", "boundary"}
    missing_top = sorted(required_top - set(contract))
    errors.extend(f"missing_top:{key}" for key in missing_top)
    if missing_top:
        return errors
    for key in ["proposal_id", "title", "pillar_relation", "mechanism", "approval_class", "execution_lane"]:
        if contract[key] != proposal[key]:
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
        "real_people_maunga_volcanoes_observatories_stations_instruments_locations_waveforms_images_samples_coordinates_or_datasets_used",
        "real_download_ingestion_processing_interpretation_diagnosis_forecast_alert_publication_or_operational_decision_used",
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used", "network_called", "external_rows",
        "authority_granted", "authority_action_executed", "empirical_claim_made", "obligations_present", "protected_claims",
    }
    missing_fixture = sorted(required_fixture - set(fixture))
    errors.extend(f"missing_fixture:{key}" for key in missing_fixture)
    if missing_fixture:
        return errors
    if fixture["synthetic_only"] is not True:
        errors.append("synthetic_only_required")
    for key in [
        "real_people_maunga_volcanoes_observatories_stations_instruments_locations_waveforms_images_samples_coordinates_or_datasets_used",
        "real_download_ingestion_processing_interpretation_diagnosis_forecast_alert_publication_or_operational_decision_used",
        "real_credentials_keys_proofs_private_or_culturally_restricted_data_used", "network_called", "authority_granted",
        "authority_action_executed", "empirical_claim_made",
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
    if contract["outcome"] == "exact_gate" and (fixture["authority_granted"] or fixture["authority_action_executed"]):
        errors.append("exact_gate_authority_forbidden")
    return sorted(set(errors))


def mutation_catalogue(contract: dict[str, Any]) -> list[dict[str, Any]]:
    mutations = []
    candidate = copy.deepcopy(contract)
    candidate["fixture"]["obligations_present"] = candidate["fixture"]["obligations_present"][1:]
    mutations.append({"mutation_id": "drop-domain-obligation", "candidate": candidate})
    candidate = copy.deepcopy(contract)
    candidate["fixture"]["real_people_maunga_volcanoes_observatories_stations_instruments_locations_waveforms_images_samples_coordinates_or_datasets_used"] = True
    mutations.append({"mutation_id": "promote-real-data-or-object", "candidate": candidate})
    candidate = copy.deepcopy(contract)
    candidate["fixture"]["empirical_claim_made"] = True
    mutations.append({"mutation_id": "promote-empirical-claim", "candidate": candidate})
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
    results = []
    for mutation in mutation_catalogue(contract):
        errors = validate_contract(mutation["candidate"])
        results.append({"mutation_id": f"{proposal['proposal_id']}-{mutation['mutation_id']}", "rejected": bool(errors), "error_codes": errors, "credit": 0, "retained": True, "authority_action_executed": False})
    return {
        "contract": contract,
        "valid_errors": valid_errors,
        "mutation_results": results,
        "valid_fixture_passed": not valid_errors,
        "rejected_mutation_count": sum(row["rejected"] for row in results),
        "all_mutations_rejected": all(row["rejected"] for row in results),
        "authority_action_executed": False,
    }


def run_named_surface(slug: str) -> dict[str, Any]:
    result = evaluate_surface(slug)
    return {
        "schema": "ghc.family.v658-v6.runner-surface-receipt.v1",
        "slug": slug,
        "proposal_id": result["contract"]["proposal_id"],
        "outcome": result["contract"]["outcome"],
        "valid_fixture_passed": result["valid_fixture_passed"],
        "rejected_mutation_count": result["rejected_mutation_count"],
        "expected_mutation_count": 5,
        "all_mutations_rejected": result["all_mutations_rejected"],
        "authority_action_executed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": result["contract"]["boundary"],
    }


def run_runner(name: str) -> dict[str, Any]:
    if name not in RUNNER_GROUPS:
        raise KeyError(name)
    rows = [run_named_surface(slug) for slug in RUNNER_GROUPS[name]]
    return {
        "schema": "ghc.family.v658-v6.runner-receipt.v1",
        "runner": name,
        "surfaces": [row["slug"] for row in rows],
        "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def main_for_runner(name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    receipt = run_runner(name)
    if args.output:
        path = ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=True, sort_keys=True))
    if not receipt["valid"]:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", choices=sorted(PROPOSALS_BY_SLUG))
    parser.add_argument("--runner", choices=sorted(RUNNER_GROUPS))
    args = parser.parse_args()
    if bool(args.surface) == bool(args.runner):
        parser.error("choose exactly one of --surface or --runner")
    receipt = run_named_surface(args.surface) if args.surface else run_runner(args.runner)
    print(json.dumps(receipt, ensure_ascii=True, sort_keys=True))
    if not receipt.get("valid", receipt.get("valid_fixture_passed", False)):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
