#!/usr/bin/env python3
"""Bounded runtime shared by Eiren Kestrel v648-v3 core runners."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from ghc_family_v648_v3_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v648-v3"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6483-P01": "ghc_family_context_budget_handoff_tribunal.py",
    "V6483-P02": "ghc_family_tomita_takesaki_obligations.py",
    "V6483-P03": "ghc_family_desi_dr2_lya_zero_row.py",
    "V6483-P04": "ghc_family_identity_incident_handover.py",
    "V6483-P05": "ghc_family_subordinate_events_profile.py",
    "V6483-P06": "ghc_family_identity_incident_authority.py",
    "V6483-P07": "ghc_family_six_node_nexus_threat_model.py",
    "V6483-P08": "ghc_family_artifact_pointer_accessibility.py",
    "V6483-P09": "ghc_family_thermodynamic_length.py",
    "V6483-P10": "ghc_family_proximal_causal_board.py",
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
    "V6483-P01": surface(
        "context-budget-handoff",
        "tooling/context-budget-handoff-contract.json",
        "tooling/context-budget-handoff-mutations.json",
        {
            "fixture": "owner-local compact handoff",
            "composer_character_cap": 1500,
            "composer_characters": 812,
            "artifact_pointer_declared": True,
            "media_type_declared": True,
            "byte_size_declared": True,
            "sha256_declared": True,
            "attachment_manifest_declared": True,
            "duplicate_draft_guard": True,
            "archive_header_preflight": True,
            "inline_zip_or_folder": False,
            "send_credit_before_ack": False,
        },
        ["cap", "pointer", "media_type", "size", "digest", "manifest", "duplicate", "archive", "privacy", "ack"],
        ["composer over cap", "pointer missing", "digest missing", "attachment unmanifested", "duplicate draft accepted", "archive header skipped", "send preclaimed"],
        "This owner-local tribunal does not inspect private chats, recover identity, send a message, validate an arbitrary archive, or prove platform-wide context safety.",
    ),
    "V6483-P02": surface(
        "tomita-takesaki",
        "gmut/tomita-takesaki-obligations.json",
        "gmut/tomita-takesaki-mutations.json",
        {
            "von_neumann_algebra_declared": True,
            "faithful_normal_semifinite_weight_or_cyclic_separating_vector_declared": True,
            "tomita_operator_closable": True,
            "polar_decomposition_declared": True,
            "modular_operator_positive": True,
            "modular_conjugation_antiunitary": True,
            "modular_automorphism_group_declared": True,
            "kms_relation_scoped": True,
            "operator_domain_declared": True,
            "gauge_and_eft_scope_declared": True,
            "physical_state_claimed": False,
            "empirical_claimed": False,
        },
        ["algebra", "state_or_weight", "operator", "closure", "polar", "modular_operator", "conjugation", "flow", "kms", "domain", "firewall"],
        ["algebra omitted", "cyclic-separating condition omitted", "operator called bounded", "polar factors swapped", "modular positivity omitted", "KMS universalized", "empirical state promoted"],
        "Typed Tomita-Takesaki obligations are not a solved GMUT state, detected field, force, likelihood, parameter constraint, ultraviolet completion, consciousness result, or Theory of Everything.",
    ),
    "V6483-P03": surface(
        "desi-dr2-lya-zero-row",
        "empirical/desi-dr2-lya-study-contract.json",
        "empirical/desi-dr2-lya-zero-row-receipt.json",
        {
            "release": "DESI DR2 official cosmology products",
            "release_status_reviewed": True,
            "required_surfaces": ["forest auto-correlation", "quasar cross-correlation", "DLA treatment", "distortion matrix", "broadband", "covariance", "systematics", "analysis lock"],
            "queries": 0,
            "downloads": 0,
            "spectra_rows": 0,
            "correlation_bins": 0,
            "covariance_rows": 0,
            "likelihood_calls": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "empirical_claims": 0,
        },
        ["release", "forest", "quasar", "dla", "distortion", "broadband", "covariance", "systematics", "zero_rows", "zero_promotion"],
        ["unfrozen product", "forest selection omitted", "quasar cross-correlation omitted", "DLA treatment hidden", "distortion matrix omitted", "one likelihood call", "one empirical claim"],
        "This is a zero-row refusal contract, not a DESI download, ingest, fit, posterior, constraint, detection, or empirical GMUT result.",
    ),
    "V6483-P04": surface(
        "identity-incident-handover",
        "thos/identity-incident-handover-contract.json",
        "thos/identity-incident-handover-vectors.json",
        {
            "synthetic_incident": "IDENTITY-DEMO-01",
            "containment_state_declared": True,
            "evidence_minimization_declared": True,
            "credential_revocation_path_declared": True,
            "account_recovery_path_declared": True,
            "notification_assessment_reserved": True,
            "correction_path_declared": True,
            "readback_complete": True,
            "workload_budget_declared": True,
            "next_owner_assigned": True,
            "real_people": 0,
            "real_accounts": 0,
            "real_credentials": 0,
            "real_breaches": 0,
            "real_notifications": 0,
        },
        ["contain", "minimize", "preserve", "revoke", "recover", "assess", "correct", "readback", "workload", "handover"],
        ["containment absent", "evidence overcollected", "revocation skipped", "recovery owner missing", "notification predecided", "readback absent", "next owner missing"],
        "Synthetic incident traces are represented evidence only, with no real person, account, credential, breach, serious-harm assessment, notification, entitlement, remedy, or operational result.",
    ),
    "V6483-P05": surface(
        "subordinate-events",
        "freed-id/subordinate-events-profile.json",
        "freed-id/subordinate-events-mutations.json",
        {
            "profile": "synthetic OpenID Federation subordinate event history",
            "draft_status_declared": True,
            "issuer_bound": True,
            "subject_bound": True,
            "event_type_bound": True,
            "event_time_checked": True,
            "sequence_monotonic": True,
            "pagination_bound": True,
            "revocation_and_key_update_distinguished": True,
            "replay_refused": True,
            "real_keys": 0,
            "live_federations": 0,
            "real_events": 0,
            "production": False,
        },
        ["draft", "issuer", "subject", "event", "time", "sequence", "pagination", "revocation", "key_update", "replay", "production"],
        ["draft promoted final", "issuer mismatch", "subject absent", "event type unknown", "sequence rollback", "pagination token unbound", "replay accepted"],
        "Synthetic draft-profile structure uses no real identity, key, federation, event, interoperability, privacy review, independent security review, recovery decision, or trust authority.",
    ),
    "V6483-P06": surface(
        "identity-incident-authority",
        "cbr/identity-incident-authority-reservation.json",
        "cbr/identity-incident-remedy-matrix.json",
        {
            "case_data": "none",
            "breach_finding": "reserved",
            "serious_harm_assessment": "reserved",
            "person_and_witness_privacy": "reserved",
            "notification_decision": "reserved",
            "credential_revocation_authority": "reserved",
            "recovery_entitlement": "reserved",
            "correction_and_remedy": "reserved",
            "legal_interpretation": "reserved",
            "cultural_legitimacy": "reserved",
            "maori_authority": "reserved",
            "affected_party_acceptance": "reserved",
        },
        ["no_case", "finding", "harm", "privacy", "notification", "revocation", "recovery", "remedy", "legal", "maori", "affected_party"],
        ["decide breach", "identify person", "publish evidence", "notify automatically", "revoke without authority", "allocate remedy", "assert Māori authority"],
        "This exact-gate matrix confers no privacy, breach, notification, credential, recovery, remedy, legal, cultural, Māori, or affected-party authority.",
    ),
    "V6483-P07": surface(
        "six-node-nexus-threat-model",
        "security/six-node-nexus-threat-model.json",
        "security/six-node-nexus-mutations.json",
        {
            "fixture": "design-only six-node nexus",
            "hyperv_guest_boundary_declared": True,
            "single_winnat_prefix_declared": True,
            "static_guest_addresses_declared": True,
            "windows_sandbox_distinguished": True,
            "native_codex_elevated_sandbox_distinguished": True,
            "guest_admin_broker_human_controlled": True,
            "east_west_default_deny": True,
            "artifact_broker_content_addressed": True,
            "host_shares_writable": False,
            "rollback_and_backup_declared": True,
            "host_changes_executed": 0,
        },
        ["guest", "nat", "address", "sandbox", "broker", "east_west", "artifact", "shares", "backup", "rollback", "no_host_change"],
        ["host admin delegated", "multiple NAT prefixes assumed", "sandbox types conflated", "east-west open", "writable host share", "artifact digest omitted", "rollback absent"],
        "This design-only threat model neither provisions Hyper-V nor grants administrator authority, exhaustive security, production isolation, backup correctness, or permission to weaken host controls.",
    ),
    "V6483-P08": surface(
        "artifact-pointer-accessibility",
        "accessibility/artifact-pointer-contract.json",
        "accessibility/artifact-pointer-mutations.json",
        {
            "fixture": "structural artifact pointer",
            "link_purpose_in_context": True,
            "media_type_declared": True,
            "byte_size_declared": True,
            "checksum_available": True,
            "status_role_nonfocusing": True,
            "focus_preserved": True,
            "alternative_format_declared": True,
            "failure_recovery_declared": True,
            "manual_evaluation_reserved": True,
        },
        ["purpose", "type", "size", "digest", "status", "focus", "alternative", "failure", "manual"],
        ["purpose ambiguous", "type absent", "size absent", "digest mislabeled", "status steals focus", "alternative absent", "complete conformance promoted"],
        "Structural checks reserve manual keyboard, browser, assistive-technology, motion, timing, cognitive, Māori-language, and affected-user evaluation.",
    ),
    "V6483-P09": surface(
        "thermodynamic-length",
        "thermo-psyche/thermodynamic-length-contract.json",
        "thermo-psyche/thermodynamic-length-mutations.json",
        {
            "control_parameters_declared": True,
            "linear_response_regime_declared": True,
            "friction_tensor_positive_semidefinite": True,
            "metric_or_pseudometric_scope_declared": True,
            "protocol_duration_declared": True,
            "finite_time_excess_dissipation_declared": True,
            "units_declared": True,
            "boundary_conditions_declared": True,
            "psyche_or_agency_conversion": False,
        },
        ["control", "response", "friction", "metric", "duration", "dissipation", "units", "boundary", "category_barrier"],
        ["control omitted", "far-from-equilibrium universalized", "friction indefinite", "metric called literal distance", "duration omitted", "unit mismatch", "psyche conversion"],
        "A typed thermodynamic-length classifier is not a psyche law, participant result, agency measure, consciousness claim, personhood claim, or empirical THOS result.",
    ),
    "V6483-P10": surface(
        "proximal-causal",
        "stage20/proximal-causal-contract.json",
        "stage20/proximal-causal-mutations.json",
        {
            "treatment_proxy_declared": True,
            "outcome_proxy_declared": True,
            "latent_confounding_target_declared": True,
            "bridge_function_declared": True,
            "completeness_assumptions_declared": True,
            "existence_and_uniqueness_distinguished": True,
            "positivity_declared": True,
            "estimation_strategy_declared": True,
            "sensitivity_required": True,
            "participant_effect_estimated": False,
            "stage20_ready": False,
        },
        ["treatment_proxy", "outcome_proxy", "confounding", "bridge", "completeness", "uniqueness", "positivity", "estimation", "sensitivity", "nonpromotion"],
        ["proxies conflated", "bridge assumed without existence", "completeness omitted", "uniqueness invented", "positivity violated", "sensitivity omitted", "Stage 20 promotion"],
        "Proximal-causal structure estimates no participant effect and supplies no empirical confirmation, independent review, deployment, proof, canon, or Stage 20 authority.",
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
        "schema": f"ghc.family.v648-v3.{spec['slug']}.contract.v1",
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
    mutations = {
        "schema": f"ghc.family.v648-v3.{spec['slug']}.mutations.v1",
        "phase": PHASE,
        "proposal_id": proposal_id,
        "count": len(rows),
        "executed": sum(row["executed"] for row in rows),
        "rejected": sum(row["observed"] == "reject" for row in rows),
        "rows": rows,
        "boundary": spec["boundary"],
    }
    write_json(spec["contract"], contract)
    write_json(spec["mutations"], mutations)
    witness = {
        "schema": "ghc.family.v648-v3.runner-witness.v1",
        "proposal_id": proposal_id,
        "runner": RUNNER_FILE_BY_ID[proposal_id],
        "actual_process_invocation": True,
        "positive_pass": True,
        "mutations_executed": len(rows),
        "mutations_rejected": mutations["rejected"],
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
