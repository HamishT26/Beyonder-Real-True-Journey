#!/usr/bin/env python3
"""Bounded runtime shared by Sylven Arc v647-v4 family-compatible runners."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ghc_family_v647_v4_definitions import PHASE, PROPOSALS, SLUG, TRUTH_BOUNDARY


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v647-v4"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6474-P01": "ghc_family_atomic_publish_tribunal.py",
    "V6474-P02": "ghc_family_two_pi_obligations.py",
    "V6474-P03": "ghc_family_planck_pr4_zero_row.py",
    "V6474-P04": "ghc_family_wastewater_handover.py",
    "V6474-P05": "ghc_family_oauth_jar_profile.py",
    "V6474-P06": "ghc_family_wastewater_authority.py",
    "V6474-P07": "ghc_family_tar_pax_tribunal.py",
    "V6474-P08": "ghc_family_tabs_audit.py",
    "V6474-P09": "ghc_family_second_law_statements.py",
    "V6474-P10": "ghc_family_target_trial_board.py",
}


def spec(slug: str, obligations: list[str], boundary: str) -> dict[str, Any]:
    return {"slug": slug, "obligations": obligations, "boundary": boundary}


SURFACES = {
    "V6474-P01": spec(
        "atomic-publish",
        ["exclusive_temp_reservation", "same_directory_staging", "complete_write", "file_flush", "file_sync", "atomic_replace", "directory_claim_reserved", "stale_temp_quarantine", "crash_point_record", "evidence_credit_after_replace"],
        "Owner-local publication fixtures do not prove crash durability, external side effects, production operation, or Stage 20 readiness.",
    ),
    "V6474-P02": spec(
        "two-pi",
        ["local_source", "bilocal_source", "first_legendre_transform", "second_legendre_transform", "field_expectation", "connected_two_point_function", "two_pi_functional", "stationarity", "self_energy", "dyson_closure", "conserving_truncation", "gauge_reservation", "units", "eft_domain", "observation_firewall"],
        "Typed 2PI structure is not a propagator calculation, force, prediction, likelihood, constraint, quantum completion, or Theory of Everything.",
    ),
    "V6474-P03": spec(
        "planck-pr4-zero-row",
        ["official_archive_identity", "pr4_npipe_release", "frequency_channels", "map_units", "beam_transfer", "pixelization", "component_separation", "mask_lock", "calibration_provenance", "covariance_requirement", "checksum_lock", "zero_row_lock", "likelihood_lock"],
        "This is a zero-row refusal contract, not a Planck query, download, map ingest, fit, constraint, detection, or empirical GMUT result.",
    ),
    "V6474-P04": spec(
        "wastewater-handover",
        ["synthetic_influent_state", "shock_load_flag", "aeration_setpoint_proxy", "dissolved_oxygen_proxy", "clarifier_state", "sample_identity", "sample_custody", "bypass_refusal", "escalation_owner", "readback", "workload_budget", "unresolved_item", "next_shift_owner"],
        "Synthetic wastewater traces confer no plant, operator, discharge, public-health, legal, professional, safety, or effectiveness authority.",
    ),
    "V6474-P05": spec(
        "oauth-jar",
        ["synthetic_request_object", "issuer_client_binding", "audience", "issued_at", "expiry", "jwt_identifier", "value_or_reference_mode", "outer_inner_consistency", "algorithm_allowlist", "verify_before_use", "replay_cache", "privacy_boundary"],
        "Synthetic JAR vectors use no real key, client, authorization server, token, network exchange, interoperability event, or production identity service.",
    ),
    "V6474-P06": spec(
        "wastewater-authority",
        ["no_case_data", "overflow_finding_reserved", "public_health_reach_reserved", "environmental_context_reserved", "accessibility_reserved", "worker_privacy_reserved", "community_privacy_reserved", "notification_reserved", "remedy_reserved", "legal_interpretation_reserved", "affected_party_reserved", "data_governance_reserved", "maori_authority_reserved"],
        "This exact-gate matrix confers no wastewater, environmental, public-health, privacy, legal, cultural, remedy, affected-party, tangata whenua, iwi, hapu, or Maori authority.",
    ),
    "V6474-P07": spec(
        "tar-pax",
        ["pax_header", "sparse_map", "regular_file", "directory", "symbolic_link", "hard_link", "normalized_target", "absolute_path_refusal", "parent_path_refusal", "duplicate_member_refusal", "expanded_byte_budget", "member_count_budget", "destination_confinement"],
        "Disposable TAR fixtures are not a production extractor, archive-security certification, or exhaustive-security result.",
    ),
    "V6474-P08": spec(
        "tabs-audit",
        ["labeled_tablist", "tab_roles", "single_selected_tab", "roving_tabindex", "tab_panel_control", "panel_label", "hidden_state_consistency", "logical_source_order", "keyboard_declaration", "manual_activation", "text_fallback", "responsive_reservation", "print_sequence"],
        "Structural tabs evidence reserves manual keyboard, browser, assistive-technology, Maori-language, cognitive, and affected-user evaluation.",
    ),
    "V6474-P09": spec(
        "second-law-statements",
        ["thermodynamic_system", "cyclic_device", "hot_reservoir", "cold_reservoir", "heat_sign", "work_sign", "net_state_change", "kelvin_planck_statement", "clausius_statement", "equivalence_assumptions", "perpetual_motion_refusal", "physical_domain", "psyche_firewall"],
        "Physical second-law statement typing is not a moral law, psyche law, participant result, consciousness measure, personhood claim, or justice result.",
    ),
    "V6474-P10": spec(
        "target-trial",
        ["target_protocol", "eligibility_time", "strategy_assignment", "time_zero", "follow_up_start", "outcome_clock", "grace_period", "future_information_refusal", "immortal_interval_refusal", "selection_risk", "deviation_record", "promotion_refusal"],
        "Structural target-trial alignment is not randomization, participant evidence, causal-effect estimation, independent review, or Stage 20 authorization.",
    ),
}

REAL_COUNTER_KEYS = [
    "network_queries", "downloads", "real_data_rows", "map_pixels", "likelihood_calls",
    "posterior_samples", "parameter_constraints", "real_people", "real_plants", "real_samples",
    "real_discharges", "live_operations", "real_keys", "network_exchanges", "interoperability_events",
    "authority_decisions", "participant_effects", "stage20_promotions",
]


def positive_payload(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    surface = SURFACES[proposal_id]
    return {
        "proposal_id": proposal_id,
        "fixture_scope": "bounded owner-local synthetic or structural fixture",
        "required_obligations": surface["obligations"],
        "all_required_present": True,
        "protected_gates_preserved": True,
        "negative_retained": True,
        "outcome": proposal["expected_disposition"],
        "expected_outcome": proposal["expected_disposition"],
        "external_authority_granted": False,
        "forbidden_claim": False,
        "real_world_counters": {key: 0 for key in REAL_COUNTER_KEYS},
    }


def evaluate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not payload.get("all_required_present"):
        reasons.append("required obligation missing")
    if not payload.get("protected_gates_preserved"):
        reasons.append("protected gate weakened")
    if not payload.get("negative_retained"):
        reasons.append("negative erased")
    if payload.get("outcome") != payload.get("expected_outcome"):
        reasons.append("outcome vocabulary or disposition mismatch")
    if payload.get("external_authority_granted"):
        reasons.append("external authority asserted")
    if payload.get("forbidden_claim"):
        reasons.append("forbidden claim asserted")
    if any(value != 0 for value in payload.get("real_world_counters", {}).values()):
        reasons.append("real-world counter is nonzero")
    return (not reasons, reasons)


def mutation_payloads(proposal_id: str) -> list[dict[str, Any]]:
    base = positive_payload(proposal_id)
    rows: list[dict[str, Any]] = []
    mutations = [
        ("missing_required_obligation", "all_required_present", False),
        ("protected_gate_weakened", "protected_gates_preserved", False),
        ("negative_erased", "negative_retained", False),
        ("outcome_mismatch", "outcome", "forbidden_outcome"),
        ("external_authority_asserted", "external_authority_granted", True),
        ("forbidden_claim_asserted", "forbidden_claim", True),
        ("real_world_activity_promoted", "real_world_counters", {**base["real_world_counters"], "live_operations": 1}),
    ]
    for index, (label, key, value) in enumerate(mutations, 1):
        candidate = json.loads(json.dumps(base))
        candidate[key] = value
        accepted, reasons = evaluate(candidate)
        rows.append({
            "negative_id": f"{proposal_id}-SYN-{index:02d}",
            "mutation_index": index,
            "label": label,
            "expected": "reject",
            "observed": "accept" if accepted else "reject",
            "reasons": reasons,
            "pass": not accepted,
            "retained": True,
            "completion_credit": False,
        })
    return rows


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build_surface(proposal_id: str, witness_out: str | None = None) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    surface = SURFACES[proposal_id]
    positive = positive_payload(proposal_id)
    accepted, reasons = evaluate(positive)
    rows = mutation_payloads(proposal_id)
    contract_path, mutation_path = proposal["concrete_artifacts"]
    contract = {
        "schema": f"ghc.family.v647-v4.{surface['slug']}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "positive_fixture": positive,
        "positive_pass": accepted,
        "positive_failure_reasons": reasons,
        "outcome": proposal["expected_disposition"],
        "completion_credit": proposal["expected_disposition"] == "completed",
        "protected_gates": proposal["protected_gates"],
        "boundary": surface["boundary"],
        "family_boundary": TRUTH_BOUNDARY,
    }
    mutations = {
        "schema": f"ghc.family.v647-v4.{surface['slug']}.mutations.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "count": len(rows),
        "executed": len(rows),
        "rejected": sum(row["observed"] == "reject" for row in rows),
        "rows": rows,
        "boundary": surface["boundary"],
    }
    write_json(contract_path, contract)
    write_json(mutation_path, mutations)
    witness = {
        "schema": "ghc.family.v647-v4.runner-witness.v1",
        "proposal_id": proposal_id,
        "runner": RUNNER_FILE_BY_ID[proposal_id],
        "positive_pass": accepted,
        "mutations_rejected": mutations["rejected"],
        "outcome": proposal["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": surface["boundary"],
    }
    target = witness_out or f"validation/runner-witnesses/{surface['slug']}.json"
    write_json(target, witness)
    return witness


def main_for(proposal_id: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    args = parser.parse_args()
    witness = build_surface(proposal_id, args.out)
    print(json.dumps(witness, ensure_ascii=True, sort_keys=True))
    return 0 if witness["positive_pass"] and witness["mutations_rejected"] == 7 else 1
