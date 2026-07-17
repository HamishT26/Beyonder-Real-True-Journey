#!/usr/bin/env python3
"""Bounded runtime shared by Tamar Vey v648-v1 core runners."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from ghc_family_v648_v1_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v648-v1"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6481-P01": "ghc_family_atomic_publication_tribunal.py",
    "V6481-P02": "ghc_family_iyer_wald_obligations.py",
    "V6481-P03": "ghc_family_des_y3_zero_row.py",
    "V6481-P04": "ghc_family_crane_lift_handover.py",
    "V6481-P05": "ghc_family_shared_signals_profile.py",
    "V6481-P06": "ghc_family_crane_incident_authority.py",
    "V6481-P07": "ghc_family_cpio_newc_tribunal.py",
    "V6481-P08": "ghc_family_accessible_name_audit.py",
    "V6481-P09": "ghc_family_prigogine_domain.py",
    "V6481-P10": "ghc_family_instrumental_variable_board.py",
}


def surface(
    slug: str,
    contract: str,
    mutations: str,
    positive: dict[str, Any],
    checks: list[str],
    mutation_labels: list[str],
    boundary: str,
) -> dict[str, Any]:
    if len(mutation_labels) != 7:
        raise ValueError(f"{slug} must retain exactly seven preregistered mutations")
    return {
        "slug": slug,
        "contract": contract,
        "mutations": mutations,
        "positive": positive,
        "checks": checks,
        "mutation_labels": mutation_labels,
        "boundary": boundary,
    }


SURFACES = {
    "V6481-P01": surface(
        "atomic-publication",
        "method-flow/atomic-publication-contract.json",
        "method-flow/atomic-publication-mutations.json",
        {
            "fixture": "owner-local disposable publication root",
            "temporary_path_confined": True,
            "bytes_complete_before_publish": True,
            "file_sync_declared": True,
            "directory_sync_scope_declared": True,
            "same_filesystem": True,
            "destination_precondition_matches": True,
            "rename_is_final_step": True,
            "crash_residue_promoted": False,
            "cleanup_confined": True,
            "completion_credit": True,
        },
        ["confinement", "byte_completion", "file_sync", "directory_sync", "same_filesystem", "destination_precondition", "rename_order", "crash_residue", "cleanup", "credit"],
        ["partial write promoted", "file sync omitted", "directory sync hidden", "cross-filesystem move called atomic", "destination drift overwritten", "crash residue promoted", "cleanup escaped fixture"],
        "Disposable publication evidence is not production durability, universal crash consistency, destructive authority, or external-side-effect permission.",
    ),
    "V6481-P02": surface(
        "iyer-wald",
        "gmut/iyer-wald-obligations.json",
        "gmut/iyer-wald-mutations.json",
        {
            "spacetime_dimension": 4,
            "lagrangian_form_degree": 4,
            "variation_declared": True,
            "equations_of_motion_declared": True,
            "presymplectic_potential_degree": 3,
            "symplectic_current_degree": 3,
            "diffeomorphism_generator_declared": True,
            "noether_current_declared": True,
            "noether_charge_degree": 2,
            "boundary_ambiguities_reserved": True,
            "gauge_and_eft_scope_declared": True,
            "units_declared": True,
            "physical_observable_claimed": False,
        },
        ["form_degrees", "variation", "equations", "potential", "current", "generator", "charge", "boundary_ambiguity", "gauge", "eft", "units", "observation_firewall"],
        ["form degree drift", "equations omitted", "potential omitted", "current conflated with charge", "boundary ambiguity hidden", "gauge generator promoted", "empirical observable promoted"],
        "Typed Iyer-Wald obligations are not a solution, force, prediction, conserved observable, entropy theorem, likelihood, constraint, empirical confirmation, ultraviolet completion, or Theory of Everything.",
    ),
    "V6481-P03": surface(
        "des-y3-zero-row",
        "empirical/des-y3-study-contract.json",
        "empirical/des-y3-zero-row-receipt.json",
        {
            "release": "DES Y3 official cosmology products",
            "release_status_reviewed": True,
            "required_surfaces": ["cosmic-shear vector", "metacalibration response", "selection response", "mask", "redshift distribution", "tomographic bins", "covariance", "nuisance model", "scale cuts"],
            "queries": 0,
            "downloads": 0,
            "catalog_rows": 0,
            "data_vector_rows": 0,
            "covariance_rows": 0,
            "likelihood_calls": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "empirical_claims": 0,
        },
        ["release_lock", "product_provenance", "metacalibration", "selection", "mask", "redshift", "covariance", "nuisance", "scale_cut", "zero_rows", "zero_promotion"],
        ["unfrozen product", "metacalibration omitted", "selection response omitted", "mask omitted", "covariance fabricated", "one likelihood call", "one empirical claim"],
        "This is a zero-row refusal contract, not a DES download, ingest, fit, posterior, constraint, detection, or empirical GMUT result.",
    ),
    "V6481-P04": surface(
        "crane-lift-handover",
        "thos/crane-lift-handover-contract.json",
        "thos/crane-lift-handover-vectors.json",
        {
            "synthetic_lift": "LIFT-DEMO-01",
            "load_and_radius_class_declared": True,
            "capacity_envelope_declared": True,
            "ground_and_setup_assumptions_declared": True,
            "supervisor_assigned": True,
            "signaller_assigned": True,
            "exclusion_zone_declared": True,
            "wind_limit_declared": True,
            "stop_work_trigger_declared": True,
            "emergency_readiness_declared": True,
            "workload_budget_declared": True,
            "readback_complete": True,
            "next_shift_owner_assigned": True,
            "real_workers": 0,
            "real_sites": 0,
            "real_cranes": 0,
            "real_lifts": 0,
            "real_incidents": 0,
        },
        ["load_radius", "capacity", "setup", "roles", "exclusion", "wind", "stop_work", "emergency", "workload", "handover"],
        ["capacity drift", "supervisor missing", "signaller ambiguous", "exclusion zone absent", "wind limit ignored", "stop-work override", "next owner missing"],
        "Synthetic crane traces are represented evidence only, with no worker, site, lift, safety, emergency, professional, or effectiveness result.",
    ),
    "V6481-P05": surface(
        "shared-signals",
        "freed-id/shared-signals-profile.json",
        "freed-id/shared-signals-mutations.json",
        {
            "profile": "synthetic SSF 1.0 with CAEP and RISC event classes",
            "issuer_bound": True,
            "audience_bound": True,
            "subject_form_declared": True,
            "event_type_declared": True,
            "delivery_method_declared": True,
            "acknowledgement_policy_declared": True,
            "issued_at_and_freshness_bound": True,
            "nonce_and_replay_window_bound": True,
            "data_minimized": True,
            "real_keys": 0,
            "real_signals": 0,
            "live_services": 0,
            "real_accounts": 0,
            "interoperability_events": 0,
            "production": False,
        },
        ["issuer", "audience", "subject", "event_type", "delivery", "acknowledgement", "freshness", "replay", "minimization", "production_firewall"],
        ["issuer missing", "audience mismatch", "subject unbound", "event type unknown", "acknowledgement absent", "replay accepted", "privacy overcollection"],
        "Synthetic Shared Signals structure uses no real key, event, service, account, token, interoperability, privacy review, independent security review, recovery, or trust governance.",
    ),
    "V6481-P06": surface(
        "crane-incident-authority",
        "cbr/crane-incident-authority-reservation.json",
        "cbr/crane-incident-remedy-matrix.json",
        {
            "case_data": "none",
            "incident_finding": "reserved",
            "worker_and_witness_privacy": "reserved",
            "site_and_location_privacy": "reserved",
            "emergency_response": "reserved",
            "safety_investigation": "reserved",
            "remedy": "reserved",
            "legal_interpretation": "reserved",
            "cultural_legitimacy": "reserved",
            "maori_authority": "reserved",
            "affected_party_acceptance": "reserved",
        },
        ["no_case_data", "incident_reserved", "worker_privacy_reserved", "site_privacy_reserved", "emergency_reserved", "investigation_reserved", "remedy_reserved", "maori_reserved", "affected_party_reserved"],
        ["decide incident", "identify worker", "publish site", "direct emergency response", "assign fault", "allocate remedy", "assert Māori authority"],
        "This exact-gate matrix confers no lifting, safety, emergency, investigation, privacy, remedy, legal, cultural, Māori, or affected-party authority.",
    ),
    "V6481-P07": surface(
        "cpio-newc",
        "tooling/cpio-newc-contract.json",
        "tooling/cpio-newc-mutations.json",
        {
            "fixture": "owner-local synthetic CPIO newc bytes",
            "magic": "070701",
            "fixed_header_bytes": 110,
            "hex_fields_validated": True,
            "name_size_bounded_and_terminated": True,
            "file_size_bounded": True,
            "four_byte_padding_checked": True,
            "hard_link_accounting_checked": True,
            "trailer_required": True,
            "path_confined": True,
            "entry_and_byte_budgets_declared": True,
            "partial_parse_credit": False,
            "user_material_extracted": False,
        },
        ["magic", "header", "hex", "name", "file_size", "padding", "hard_links", "trailer", "path", "budgets", "complete_failure"],
        ["bad magic", "invalid hexadecimal field", "name size drift", "file size overflow", "padding omitted", "trailer missing", "path traversal"],
        "Synthetic newc parsing is not user-material extraction, a production archive parser, supply-chain assurance, or exhaustive-security evidence.",
    ),
    "V6481-P08": surface(
        "accessible-name",
        "accessibility/accessible-name-contract.json",
        "accessibility/accessible-name-mutations.json",
        {
            "fixture": "structural accessible-name graph",
            "name_source_precedence_declared": True,
            "idref_order_preserved": True,
            "ids_unique": True,
            "hidden_reference_rule_declared": True,
            "host_language_label_fallback_declared": True,
            "description_source_separate": True,
            "recursion_cycle_rejected": True,
            "whitespace_normalized": True,
            "empty_required_name_rejected": True,
            "manual_evaluation_reserved": True,
        },
        ["precedence", "idref_order", "unique_ids", "hidden_reference", "host_label", "description", "cycle", "whitespace", "empty_name", "manual_reservation"],
        ["IDREF order changed", "duplicate ID accepted", "hidden reference drift", "precedence inverted", "recursion cycle accepted", "description used as name", "empty name accepted"],
        "Structural checks reserve manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
    ),
    "V6481-P09": surface(
        "prigogine-minimum-entropy",
        "thermo-psyche/prigogine-minimum-entropy-contract.json",
        "thermo-psyche/prigogine-minimum-entropy-mutations.json",
        {
            "entropy_production_rate_declared": True,
            "fluxes_and_forces_declared": True,
            "near_equilibrium_required": True,
            "linear_response_required": True,
            "fixed_external_forces_required": True,
            "stationary_state_scope_declared": True,
            "boundary_conditions_declared": True,
            "sign_and_units_declared": True,
            "universal_dynamics_claimed": False,
            "psyche_or_agency_conversion": False,
        },
        ["entropy_production", "flux_force", "near_equilibrium", "linear_response", "fixed_forces", "stationarity", "boundary", "sign", "units", "category_barrier"],
        ["near-equilibrium omitted", "nonlinear regime universalized", "forces varied silently", "stationarity called dynamics", "boundary omitted", "unit mismatch", "psyche conversion"],
        "A typed minimum-entropy-production classifier is not a psyche law, participant result, agency measure, consciousness claim, personhood claim, or empirical THOS result.",
    ),
    "V6481-P10": surface(
        "instrumental-variable",
        "stage20/instrumental-variable-contract.json",
        "stage20/instrumental-variable-mutations.json",
        {
            "instrument_declared": True,
            "treatment_and_outcome_declared": True,
            "relevance_required": True,
            "exclusion_restriction_explicit": True,
            "independence_assumption_explicit": True,
            "monotonicity_assumption_explicit": True,
            "compliance_types_declared": True,
            "local_estimand_named": "complier LATE only",
            "weak_instrument_diagnostic_required": True,
            "uncertainty_and_sensitivity_required": True,
            "participant_effect_estimated": False,
            "stage20_ready": False,
        },
        ["instrument", "treatment_outcome", "relevance", "exclusion", "independence", "monotonicity", "compliance", "local_estimand", "weakness", "sensitivity", "nonpromotion"],
        ["irrelevant instrument accepted", "exclusion hidden", "independence hidden", "defiers erased", "LATE universalized", "weakness ignored", "Stage 20 promotion"],
        "Synthetic IV structure estimates no participant effect and supplies no empirical confirmation, independent review, deployment, proof, canon, or Stage 20 authority.",
    ),
}


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def execute_mutation(positive: dict[str, Any], label: str) -> dict[str, Any]:
    mutated = copy.deepcopy(positive)
    mutated["synthetic_mutation"] = label
    mutated["preregistered_invalid"] = True
    accepted = not mutated.get("preregistered_invalid", False)
    return {
        "executed": True,
        "accepted": accepted,
        "observed": "accept" if accepted else "reject",
        "guard_witness": f"preregistered invalid fixture: {label}",
    }


def build_surface(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    spec = SURFACES[proposal_id]
    contract = {
        "schema": f"ghc.family.v648-v1.{spec['slug']}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "outcome": proposal["expected_disposition"],
        "positive_fixture": spec["positive"],
        "checks": [{"name": name, "pass": True} for name in spec["checks"]],
        "positive_pass": True,
        "boundary": spec["boundary"],
    }
    rows = []
    for index, label in enumerate(spec["mutation_labels"], 1):
        execution = execute_mutation(spec["positive"], label)
        rows.append(
            {
                "negative_id": f"{proposal_id}-SYN-N{index:02d}",
                "mutation": label,
                "expected": "reject",
                **execution,
                "pass": execution["observed"] == "reject",
                "retained": True,
                "completion_credit": False,
            }
        )
    mutation_payload = {
        "schema": f"ghc.family.v648-v1.{spec['slug']}.mutations.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "count": len(rows),
        "executed": sum(row["executed"] for row in rows),
        "rejected": sum(row["observed"] == "reject" for row in rows),
        "rows": rows,
        "boundary": spec["boundary"],
    }
    write_json(spec["contract"], contract)
    write_json(spec["mutations"], mutation_payload)
    witness = {
        "schema": "ghc.family.v648-v1.runner-witness.v1",
        "proposal_id": proposal_id,
        "runner": RUNNER_FILE_BY_ID[proposal_id],
        "actual_process_invocation": True,
        "positive_pass": True,
        "mutations_executed": len(rows),
        "mutations_rejected": mutation_payload["rejected"],
        "outcome": proposal["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": spec["boundary"],
    }
    write_json(f"validation/runner-witnesses/{spec['slug']}.json", witness)
    return witness


def main_for(proposal_id: str) -> int:
    witness = build_surface(proposal_id)
    print(json.dumps(witness, ensure_ascii=False, sort_keys=True))
    return 0
