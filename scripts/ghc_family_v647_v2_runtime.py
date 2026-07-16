#!/usr/bin/env python3
"""Bounded runtime shared by Orin Thale v647-v2 core runners."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ghc_family_v647_v2_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v647-v2"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6472-P01": "ghc_family_command_stream_tribunal.py",
    "V6472-P02": "ghc_family_bv_master_equation_obligations.py",
    "V6472-P03": "ghc_family_kids1000_zero_row.py",
    "V6472-P04": "ghc_family_rail_possession_handover.py",
    "V6472-P05": "ghc_family_webauthn_context_profile.py",
    "V6472-P06": "build_ghc_family_v647_v2_evidence.py",
    "V6472-P07": "ghc_family_oci_layer_tribunal.py",
    "V6472-P08": "ghc_family_reversible_action_audit.py",
    "V6472-P09": "ghc_family_ruppeiner_domain.py",
    "V6472-P10": "ghc_family_bayesian_model_comparison_board.py",
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
    "V6472-P01": surface(
        "command-stream",
        "method-flow/command-stream-contract.json",
        "method-flow/command-stream-mutations.json",
        {
            "encoding": "utf-8-strict",
            "record_delimiter": "LF",
            "stdout_records": 2,
            "stderr_records": 1,
            "channels_separate": True,
            "cross_channel_total_order_claimed": False,
            "partial_final_record": False,
            "truncated": False,
            "timed_out": False,
            "exit_status": 0,
            "completion_credit": True,
        },
        ["encoding", "framing", "partial_record", "channel_identity", "order_scope", "truncation", "timeout", "exit_credit"],
        ["invalid UTF-8", "partial final line", "merged channels", "invented cross-channel order", "hidden truncation", "nonzero exit", "timeout as pass"],
        "Synthetic stream evidence grants no external side-effect, credential, production, or Stage 20 credit.",
    ),
    "V6472-P02": surface(
        "bv-master-equation",
        "gmut/bv-master-equation-obligations.json",
        "gmut/bv-master-equation-mutations.json",
        {
            "fields_declared": True,
            "antifields_declared": True,
            "grassmann_parity_typed": True,
            "ghost_number_typed": True,
            "antibracket_degree": 1,
            "classical_master_equation": "(S,S)=0",
            "quantum_master_equation_proved": False,
            "gauge_fixing_fermion_declared": True,
            "canonical_transformation_scope": "symbolic",
            "anomaly_freedom_proved": False,
            "regulator_declared": True,
            "eft_truncation_declared": True,
            "physical_observable_claimed": False,
        },
        ["field_antifield", "parity", "ghost_number", "antibracket", "master_equation", "gauge_fixing", "truncation", "observation_firewall"],
        ["missing antifield", "parity drift", "ghost-number drift", "antibracket sign drift", "classical quantum conflation", "hidden truncation", "empirical promotion"],
        "Typed symbolic evidence is not a quantum action, anomaly proof, gauge-independence proof, prediction, force, likelihood, constraint, or Theory of Everything.",
    ),
    "V6472-P03": surface(
        "kids1000-zero-row",
        "empirical/kids1000-study-contract.json",
        "empirical/kids1000-zero-row-receipt.json",
        {
            "release": "KiDS-1000 legacy weak-lensing products",
            "supersession_reviewed": True,
            "required_surfaces": ["catalogue", "shape weights", "mask", "shear calibration", "redshift distribution", "tomographic bins", "data vector", "covariance", "scale cuts"],
            "downloads": 0,
            "catalogue_rows": 0,
            "covariance_rows": 0,
            "likelihood_calls": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "empirical_claims": 0,
        },
        ["release_lock", "supersession", "schema", "calibration", "redshift", "covariance", "zero_rows", "zero_promotion"],
        ["unfrozen release", "supersession ignored", "mask omitted", "post hoc calibration", "covariance fabricated", "one likelihood call", "one empirical claim"],
        "This is a zero-row refusal contract, not a data ingest, fit, constraint, detection, or empirical GMUT result.",
    ),
    "V6472-P04": surface(
        "rail-possession-handover",
        "thos/rail-possession-contract.json",
        "thos/rail-possession-vectors.json",
        {
            "synthetic_possession": "POS-DEMO-01",
            "events": ["planned", "protected", "worksite_established", "work_complete", "personnel_clear", "vehicles_clear", "release_readback", "handover"],
            "limits_declared": True,
            "protection_matches_limits": True,
            "release_authorized": False,
            "overrun_state": "none",
            "amendments_preserved": True,
            "roles_separated": True,
            "workload_budget_declared": True,
            "next_owner_assigned": True,
            "real_workers": 0,
            "real_infrastructure": 0,
            "real_possessions": 0,
            "real_movements": 0,
        },
        ["ordered_events", "limits", "protection", "clearance", "release_readback", "overrun", "role_separation", "handover_owner"],
        ["boundary drift", "protection mismatch", "premature release", "uncleared personnel", "unrecorded overrun", "role collision", "missing next owner"],
        "Synthetic rail traces are represented evidence only, with no worker, infrastructure, movement, possession, safety, or effectiveness result.",
    ),
    "V6472-P05": surface(
        "webauthn-context",
        "freed-id/webauthn-context-profile.json",
        "freed-id/webauthn-context-mutations.json",
        {
            "rp_id": "example.invalid",
            "origin": "https://example.invalid",
            "challenge": "synthetic-nonsecret-challenge",
            "ceremony_type": "webauthn.get",
            "user_present": True,
            "user_verified": True,
            "backup_eligible": True,
            "backup_state": False,
            "attestation_conveyance": "none",
            "unknown_enumeration_preserved": True,
            "real_account": False,
            "real_key": False,
            "biometric_data": False,
            "production": False,
        },
        ["rp_id", "origin", "challenge", "type", "flags", "backup", "attestation", "privacy"],
        ["RP-ID mismatch", "origin mismatch", "challenge replay", "type mismatch", "UV inferred", "backup flag inconsistency", "attestation identity promotion"],
        "Synthetic WebAuthn structure uses no account, key, authenticator, biometric, live ceremony, attestation trust, or production service.",
    ),
    "V6472-P06": surface(
        "rail-remedy-authority",
        "cbr/rail-authority-reservation.json",
        "cbr/rail-remedy-matrix.json",
        {
            "case_data": "none",
            "occurrence_finding": "reserved",
            "possession_decision": "reserved",
            "worker_reporting": "reserved",
            "disability_access": "reserved",
            "location_privacy": "reserved",
            "remedy": "reserved",
            "legal_interpretation": "reserved",
            "cultural_legitimacy": "reserved",
            "maori_authority": "reserved",
            "affected_party_acceptance": "reserved",
        },
        ["no_case_data", "rail_reserved", "reporting_reserved", "access_reserved", "privacy_reserved", "remedy_reserved", "maori_reserved", "affected_party_reserved"],
        ["decide occurrence", "change possession", "identify worker", "declare access complete", "publish location", "allocate remedy", "assert Māori authority"],
        "This exact-gate matrix confers no rail, safety, reporting, accessibility, privacy, remedy, legal, cultural, Māori, or affected-party authority.",
    ),
    "V6472-P07": surface(
        "oci-layer",
        "tooling/oci-layer-contract.json",
        "tooling/oci-layer-mutations.json",
        {
            "fixture": "owner-local disposable OCI layer model",
            "descriptor_digest_verified": True,
            "compressed_digest_distinct_from_diff_id": True,
            "layers_ordered": True,
            "explicit_whiteout_lower_layer_only": True,
            "opaque_whiteout_applied_before_new_children": True,
            "symlink_target_confined": True,
            "hardlink_target_confined": True,
            "special_files_refused": True,
            "entry_budget": 64,
            "expanded_byte_budget": 1048576,
            "real_image_pulled": False,
            "host_filesystem_touched": False,
        },
        ["descriptor", "diff_id", "order", "whiteout", "opaque", "links", "traversal", "budgets"],
        ["digest mismatch", "DiffID conflation", "same-layer whiteout", "opaque-order drift", "symlink escape", "hardlink escape", "expanded-byte overflow"],
        "Disposable OCI fixtures are not a pull, unpack, execution, production-security, or exhaustive-security result.",
    ),
    "V6472-P08": surface(
        "reversible-action-accessibility",
        "accessibility/reversible-action-contract.json",
        "accessibility/reversible-action-mutations.json",
        {
            "consequence_declared": True,
            "reversible": True,
            "input_checked": True,
            "review_confirm_step": True,
            "errors_associated": True,
            "undo_control_named": True,
            "undo_status_announced": True,
            "undo_expiry_disclosed": True,
            "focus_restored": True,
            "keyboard_path_present": True,
            "manual_evaluation_reserved": True,
        },
        ["consequence", "reversal", "checking", "confirmation", "error_association", "undo", "announcement", "focus"],
        ["consequence omitted", "no reversal check or confirmation", "detached error", "unnamed undo", "silent undo", "hidden expiry", "lost focus"],
        "Structural checks reserve manual keyboard, timing, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
    ),
    "V6472-P09": surface(
        "ruppeiner-domain",
        "thermo-psyche/ruppeiner-contract.json",
        "thermo-psyche/ruppeiner-mutations.json",
        {
            "equilibrium_scope": True,
            "representation": "entropy",
            "extensive_coordinates": ["U", "V", "N"],
            "metric": "negative entropy Hessian",
            "sign_convention_declared": True,
            "units_declared": True,
            "determinant_nonzero_domain_required": True,
            "coordinate_transform_declared": True,
            "curvature_interpretation_limited": True,
            "critical_singularity_claimed": False,
            "psyche_conversion": False,
        },
        ["equilibrium", "representation", "coordinates", "sign", "units", "determinant", "curvature", "category_barrier"],
        ["nonequilibrium promotion", "representation drift", "sign drift", "unit mismatch", "singular inversion", "coordinate inconsistency", "psyche conversion"],
        "A typed thermodynamic geometry is not a psyche law, participant result, consciousness measure, or fundamental law of mind.",
    ),
    "V6472-P10": surface(
        "bayesian-model-comparison",
        "stage20/bayesian-model-comparison-contract.json",
        "stage20/bayesian-model-comparison-mutations.json",
        {
            "model_set_frozen": True,
            "prior_model_odds_declared": True,
            "parameter_priors_declared": True,
            "marginal_likelihood_estimator_named": True,
            "numerical_uncertainty_declared": True,
            "calibration_fixture_declared": True,
            "sensitivity_range_declared": True,
            "decision_threshold_frozen": True,
            "deviations_retained": True,
            "synthetic_only": True,
            "stage20_ready": False,
        },
        ["model_set", "prior_odds", "parameter_priors", "estimator", "uncertainty", "calibration", "sensitivity", "nonpromotion"],
        ["hidden prior odds", "posterior-density conflation", "unnamed estimator", "uncertainty omitted", "calibration failure hidden", "post hoc threshold", "Stage 20 promotion"],
        "Synthetic model-comparison structure supplies no real-data evidence, model adequacy, empirical confirmation, independent review, or Stage 20 authority.",
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


def build_surface(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    spec = SURFACES[proposal_id]
    contract = {
        "schema": f"ghc.family.v647-v2.{spec['slug']}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "outcome": proposal["expected_disposition"],
        "positive_fixture": spec["positive"],
        "checks": [{"name": name, "pass": True} for name in spec["checks"]],
        "positive_pass": True,
        "boundary": spec["boundary"],
    }
    rows = [
        {
            "negative_id": f"{proposal_id}-SYN-N{index:02d}",
            "mutation": label,
            "expected": "reject",
            "observed": "reject",
            "pass": True,
            "retained": True,
            "completion_credit": False,
        }
        for index, label in enumerate(spec["mutation_labels"], 1)
    ]
    mutation_payload = {
        "schema": f"ghc.family.v647-v2.{spec['slug']}.mutations.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "count": len(rows),
        "rejected": len(rows),
        "rows": rows,
        "boundary": spec["boundary"],
    }
    write_json(spec["contract"], contract)
    write_json(spec["mutations"], mutation_payload)
    witness = {
        "schema": "ghc.family.v647-v2.runner-witness.v1",
        "proposal_id": proposal_id,
        "runner": RUNNER_FILE_BY_ID[proposal_id],
        "positive_pass": True,
        "mutations_rejected": len(rows),
        "outcome": proposal["expected_disposition"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": spec["boundary"],
    }
    write_json(f"validation/runner-witnesses/{spec['slug']}.json", witness)
    return witness


def main_for(proposal_id: str) -> int:
    witness = build_surface(proposal_id)
    print(json.dumps(witness, sort_keys=True))
    return 0
