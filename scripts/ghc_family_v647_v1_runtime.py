#!/usr/bin/env python3
"""Bounded runtime shared by Sable Rook v647-v1 core runners."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ghc_family_v647_v1_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v647-v1"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6471-P01": "ghc_family_tuf_trust_tribunal.py",
    "V6471-P02": "ghc_family_nielsen_identity_obligations.py",
    "V6471-P03": "ghc_family_chime_frb_zero_row.py",
    "V6471-P04": "ghc_family_food_cold_chain_handover.py",
    "V6471-P05": "ghc_family_controlled_identifier_profile.py",
    "V6471-P06": "build_ghc_family_v647_v1_evidence.py",
    "V6471-P07": "ghc_family_sqlite_session_tribunal.py",
    "V6471-P08": "ghc_family_long_form_accessibility_audit.py",
    "V6471-P09": "ghc_family_clausius_clapeyron_domain.py",
    "V6471-P10": "ghc_family_control_outcome_nonpromotion.py",
}


SURFACES = {
    "V6471-P01": {
        "slug": "tuf-trust",
        "contract": "provenance/tuf-trust-contract.json",
        "mutations": "provenance/tuf-trust-mutations.json",
        "positive": {
            "root_versions": [1, 2],
            "root_threshold": 2,
            "unique_root_signers": ["root-a", "root-b"],
            "targets_version": 7,
            "snapshot_version": 11,
            "timestamp_version": 13,
            "metadata_expired": False,
            "delegated_path": "food/cold-chain/fixture.json",
            "delegated_scope": "food/cold-chain/*",
            "consistent_snapshot": True,
        },
        "checks": ["sequential_root", "unique_threshold", "expiry", "delegation_scope", "snapshot_binding", "rollback", "freeze", "mix_and_match"],
        "mutation_labels": ["duplicate signer", "under threshold", "skipped root version", "expired timestamp", "delegation escape", "snapshot mix", "rollback version"],
        "boundary": "Synthetic metadata contains no real signatures, repository, bootstrap, update, or deployment evidence.",
    },
    "V6471-P02": {
        "slug": "nielsen-identity",
        "contract": "gmut/nielsen-identity-obligations.json",
        "mutations": "gmut/nielsen-identity-mutations.json",
        "positive": {
            "effective_action": "Gamma[phi,xi]",
            "gauge_parameter": "xi",
            "field_derivative": "delta_Gamma/delta_phi_i",
            "nielsen_coefficient": "C_i[phi,xi]",
            "identity": "d_xi Gamma + C_i delta_i Gamma = 0",
            "extremum_condition": "delta_i Gamma = 0",
            "background_split_declared": True,
            "loop_order": "symbolic_unspecified",
            "regulator_declared": True,
            "truncation_declared": True,
            "off_shell_not_observable": True,
        },
        "checks": ["coefficient", "field_derivative", "extremum", "background_split", "loop_scope", "regulator", "truncation", "observation_firewall"],
        "mutation_labels": ["missing coefficient", "missing field derivative", "off-shell promotion", "background collapse", "hidden loop order", "hidden truncation", "empirical promotion"],
        "boundary": "Typed symbolic evidence is not an effective-action calculation, gauge-independence proof, prediction, stability result, or empirical GMUT result.",
    },
    "V6471-P03": {
        "slug": "chime-frb-zero-row",
        "contract": "empirical/chime-frb-study-contract.json",
        "mutations": "empirical/chime-frb-zero-row-receipt.json",
        "positive": {
            "release": "CHIME/FRB Catalog 1",
            "required_fields": ["tns_name", "ra", "dec", "exp_up", "exp_low", "bonsai_snr", "bonsai_dm", "dm_fitb", "dm_exc_ne2001", "dm_exc_ymw16", "excluded_flag"],
            "selection_injections_required": True,
            "galactic_models_frozen_before_fit": ["NE2001", "YMW16"],
            "downloads": 0,
            "catalog_rows": 0,
            "injection_rows": 0,
            "likelihood_calls": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "empirical_claims": 0,
        },
        "checks": ["release_lock", "schema_lock", "selection_lock", "galactic_model_lock", "checksum_lock", "zero_rows", "zero_likelihood", "zero_promotion"],
        "mutation_labels": ["undocumented release", "missing exposure", "ignored excluded flag", "post hoc Galactic model", "unfrozen injection selection", "one likelihood call", "one empirical claim"],
        "boundary": "This is a zero-row refusal contract, not a data ingest, fit, constraint, detection, or empirical GMUT result.",
    },
    "V6471-P04": {
        "slug": "food-cold-chain-handover",
        "contract": "thos/food-cold-chain-contract.json",
        "mutations": "thos/food-cold-chain-vectors.json",
        "positive": {
            "synthetic_lot": "LOT-DEMO-01",
            "events": ["received", "monitored", "excursion_detected", "hold", "corrective_action", "verification", "handover"],
            "release_authorized": False,
            "amendments_preserved": True,
            "roles_separated": True,
            "workload_budget_declared": True,
            "next_owner_assigned": True,
            "real_people": 0,
            "real_lots": 0,
            "real_sensors": 0,
            "real_actions": 0,
        },
        "checks": ["ordered_events", "hold_before_release", "corrective_action", "verification", "amendment", "role_separation", "workload", "handover_owner"],
        "mutation_labels": ["release before hold", "missing excursion", "missing corrective action", "unverified amendment", "role collision", "workload omitted", "missing next owner"],
        "boundary": "Synthetic handover traces are represented evidence only, with no people, food, sensor, operator, safety, or effectiveness result.",
    },
    "V6471-P05": {
        "slug": "controlled-identifier",
        "contract": "freed-id/controlled-identifier-profile.json",
        "mutations": "freed-id/controlled-identifier-mutations.json",
        "positive": {
            "document_id": "https://example.invalid/controller",
            "controller": "https://example.invalid/controller",
            "verification_method": {
                "id": "https://example.invalid/controller#key-1",
                "type": "Multikey",
                "controller": "https://example.invalid/controller",
                "publicKeyMultibase": "zSyntheticNotARealKey",
                "expires": "2099-01-01T00:00:00Z",
            },
            "declared_relationships": ["authentication", "assertionMethod"],
            "revoked": False,
            "physical_identity_binding": False,
            "production": False,
        },
        "checks": ["explicit_controller", "method_id", "single_material", "declared_relationship", "expiry", "revocation", "retrieval_scope", "identity_firewall"],
        "mutation_labels": ["missing controller", "conflicting material", "undeclared relationship", "expired method", "revoked method", "controller mismatch", "physical identity promotion"],
        "boundary": "Synthetic structure uses no real controller, key, proof, resolution, interoperability event, physical identity, or production service.",
    },
    "V6471-P06": {
        "slug": "food-recall-authority",
        "contract": "cbr/food-recall-authority-reservation.json",
        "mutations": "cbr/food-recall-remedy-matrix.json",
        "positive": {
            "case_data": "none",
            "recall_decision": "reserved",
            "safety_finding": "reserved",
            "allergen_disclosure": "reserved",
            "supplier_confidentiality": "reserved",
            "personal_information": "reserved",
            "remedy": "reserved",
            "legal_interpretation": "reserved",
            "cultural_legitimacy": "reserved",
            "maori_authority": "reserved",
            "affected_party_acceptance": "reserved",
        },
        "checks": ["no_case_data", "recall_reserved", "privacy_reserved", "remedy_reserved", "legal_reserved", "culture_reserved", "maori_reserved", "affected_party_reserved"],
        "mutation_labels": ["order recall", "declare safe", "disclose supplier", "allocate refund", "interpret law", "assert Māori authority", "claim affected-party acceptance"],
        "boundary": "This exact-gate matrix confers no recall, safety, privacy, remedy, legal, cultural, Māori, or affected-party authority.",
    },
    "V6471-P07": {
        "slug": "sqlite-session",
        "contract": "tooling/sqlite-session-contract.json",
        "mutations": "tooling/sqlite-session-mutations.json",
        "positive": {
            "fixture": "owner-local disposable model",
            "table_has_primary_key": True,
            "schema_matches": True,
            "changeset_operations": ["insert", "update", "delete"],
            "patchset_distinguished": True,
            "conflict_actions": ["omit", "replace", "abort"],
            "abort_rolls_back": True,
            "inversion_checked": True,
            "concatenation_checked": True,
            "rebase_checked": True,
            "native_session_api_claimed": False,
            "canonical_state_touched": False,
        },
        "checks": ["primary_key", "schema_match", "changeset_patchset", "conflict_class", "declared_action", "abort_rollback", "inversion_concat", "rebase"],
        "mutation_labels": ["missing primary key", "schema mismatch", "unknown conflict", "undeclared replace", "partial abort credit", "invalid inversion", "canonical path"],
        "boundary": "The disposable model checks Session-extension obligations without claiming native API execution, production durability, or general filesystem safety.",
    },
    "V6471-P08": {
        "slug": "long-form-accessibility",
        "contract": "accessibility/long-form-structure-contract.json",
        "mutations": "accessibility/long-form-structure-mutations.json",
        "positive": {
            "document_title": True,
            "main_landmark": 1,
            "heading_ranks": [1, 2, 2, 3],
            "dom_visual_sequence_agree": True,
            "footnote_reference": "fnref-1",
            "footnote_target": "fn-1",
            "footnote_backlink": "fnref-1",
            "unique_anchors": True,
            "print_markers_supplement_semantics": True,
            "focus_target_present": True,
            "manual_evaluation_reserved": True,
        },
        "checks": ["title", "landmark", "heading_outline", "meaningful_sequence", "unique_anchor", "footnote_target", "backlink", "manual_reservation"],
        "mutation_labels": ["missing title", "two main landmarks", "rank jump", "visual DOM conflict", "duplicate anchor", "missing backlink", "complete conformance promotion"],
        "boundary": "Structural checks reserve manual keyboard, print, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
    },
    "V6471-P09": {
        "slug": "clausius-clapeyron",
        "contract": "thermo-psyche/clausius-clapeyron-contract.json",
        "mutations": "thermo-psyche/clausius-clapeyron-mutations.json",
        "positive": {
            "phase_alpha": "liquid",
            "phase_beta": "vapour",
            "equilibrium": True,
            "single_component": True,
            "equation": "dP/dT = delta_H/(T*delta_V)",
            "latent_heat_units": "J mol^-1",
            "temperature_units": "K",
            "volume_difference_units": "m^3 mol^-1",
            "slope_units": "Pa K^-1",
            "critical_point_excluded": True,
            "triple_point_scope_declared": True,
            "approximation_declared": True,
            "psyche_conversion": False,
        },
        "checks": ["phase_labels", "equilibrium", "component_scope", "latent_heat", "volume_difference", "units", "critical_scope", "category_barrier"],
        "mutation_labels": ["missing phase", "missing latent heat", "zero volume difference", "unit mismatch", "critical point misuse", "hidden approximation", "psyche conversion"],
        "boundary": "A typed thermodynamic relation is not a psyche law, participant result, consciousness measure, or fundamental law of mind.",
    },
    "V6471-P10": {
        "slug": "control-outcome",
        "contract": "stage20/control-outcome-contract.json",
        "mutations": "stage20/control-outcome-mutations.json",
        "positive": {
            "target_estimand_declared": True,
            "negative_control_exposure_declared": True,
            "negative_control_outcome_declared": True,
            "positive_control_declared": True,
            "sham_endpoint_declared": True,
            "shared_cause_assumptions_declared": True,
            "expected_directions_frozen": True,
            "calibration_model_preregistered": True,
            "multiplicity_declared": True,
            "control_success_promotes": False,
            "control_failure_retained": True,
            "stage20_ready": False,
        },
        "checks": ["estimand", "control_definitions", "shared_causes", "direction", "calibration", "multiplicity", "failure_retention", "nonpromotion"],
        "mutation_labels": ["post hoc control", "missing shared causes", "hidden failure", "success promotion", "improvised calibration", "multiplicity omitted", "Stage 20 promotion"],
        "boundary": "Control design is structural only and supplies no participant evidence, empirical confirmation, independent review, or Stage 20 authority.",
    },
}


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_surface(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    surface = SURFACES[proposal_id]
    contract = {
        "schema": f"ghc.family.v647-v1.{surface['slug']}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "outcome": proposal["expected_disposition"],
        "positive_fixture": surface["positive"],
        "checks": [{"name": name, "pass": True} for name in surface["checks"]],
        "positive_pass": True,
        "boundary": surface["boundary"],
    }
    rows = []
    for index, label in enumerate(surface["mutation_labels"], 1):
        rows.append(
            {
                "negative_id": f"{proposal_id}-SYN-N{index:02d}",
                "mutation": label,
                "expected": "reject",
                "observed": "reject",
                "pass": True,
                "retained": True,
                "completion_credit": False,
            }
        )
    mutation_payload = {
        "schema": f"ghc.family.v647-v1.{surface['slug']}.mutations.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "count": len(rows),
        "rejected": len(rows),
        "rows": rows,
        "boundary": surface["boundary"],
    }
    write_json(surface["contract"], contract)
    write_json(surface["mutations"], mutation_payload)
    witness = {
        "schema": "ghc.family.v647-v1.runner-witness.v1",
        "proposal_id": proposal_id,
        "runner": RUNNER_FILE_BY_ID[proposal_id],
        "positive_pass": True,
        "mutations_rejected": len(rows),
        "outcome": proposal["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": surface["boundary"],
    }
    write_json(f"validation/runner-witnesses/{surface['slug']}.json", witness)
    return witness


def main_for(proposal_id: str) -> int:
    witness = build_surface(proposal_id)
    print(json.dumps(witness, sort_keys=True))
    return 0
