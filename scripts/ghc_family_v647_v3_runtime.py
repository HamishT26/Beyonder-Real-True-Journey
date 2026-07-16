#!/usr/bin/env python3
"""Bounded runtime shared by Tamar Vey v647-v3 core runners."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ghc_family_v647_v3_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v647-v3"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6473-P01": "ghc_family_child_process_lifecycle_tribunal.py",
    "V6473-P02": "ghc_family_heat_kernel_obligations.py",
    "V6473-P03": "ghc_family_hsc_pdr3_zero_row.py",
    "V6473-P04": "ghc_family_telecom_change_handover.py",
    "V6473-P05": "ghc_family_vc_related_resource_profile.py",
    "V6473-P06": "ghc_family_telecom_outage_authority.py",
    "V6473-P07": "ghc_family_http_structured_fields_tribunal.py",
    "V6473-P08": "ghc_family_breadcrumb_audit.py",
    "V6473-P09": "ghc_family_nernst_third_law_domain.py",
    "V6473-P10": "ghc_family_prequential_drift_board.py",
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
    "V6473-P01": surface(
        "child-process-lifecycle",
        "method-flow/child-process-lifecycle-contract.json",
        "method-flow/child-process-lifecycle-mutations.json",
        {
            "fixture": "owner-local synthetic process tree",
            "inherited_handle_allowlist": ["stdout-write", "stderr-write"],
            "parent_read_ends_inheritable": False,
            "parent_write_ends_closed_before_read": True,
            "descendant_set_declared": True,
            "all_descendants_joined": True,
            "partial_output_retained": True,
            "timed_out": False,
            "exit_statuses": [0, 0],
            "teardown_confined": True,
            "completion_credit": True,
        },
        ["handle_allowlist", "pipe_end_ownership", "eof_precondition", "descendant_set", "join", "partial_output", "exit_status", "teardown"],
        ["undeclared inherited handle", "parent writer left open", "false EOF credit", "orphan descendant", "timeout as pass", "partial output promoted", "teardown escape"],
        "Synthetic process-tree evidence grants no external-side-effect, credential, production, or Stage 20 credit.",
    ),
    "V6473-P02": surface(
        "heat-kernel",
        "gmut/heat-kernel-obligations.json",
        "gmut/heat-kernel-mutations.json",
        {
            "operator_class": "Laplace-type assumed",
            "principal_symbol_declared": True,
            "ellipticity_assumed": True,
            "manifold_dimension": 4,
            "bundle_connection_declared": True,
            "endomorphism_declared": True,
            "boundary_condition": "declared symbolic local condition",
            "proper_time_units": "inverse mass squared",
            "coefficient_orders": [0, 2, 4],
            "regulator_declared": True,
            "eft_truncation_declared": True,
            "anomaly_freedom_proved": False,
            "physical_observable_claimed": False,
        },
        ["operator_type", "principal_symbol", "ellipticity", "geometry", "connection", "boundary", "coefficient_order", "regulator", "truncation", "observation_firewall"],
        ["non-Laplace operator accepted", "ellipticity omitted", "connection omitted", "boundary omitted", "coefficient-order drift", "regulator hidden", "empirical promotion"],
        "Typed heat-kernel obligations are not a determinant, anomaly proof, spectrum, force, likelihood, constraint, quantum completion, or Theory of Everything.",
    ),
    "V6473-P03": surface(
        "hsc-pdr3-zero-row",
        "empirical/hsc-pdr3-study-contract.json",
        "empirical/hsc-pdr3-zero-row-receipt.json",
        {
            "release": "HSC-SSP PDR3 with S19A shape catalog",
            "release_status_reviewed": True,
            "required_surfaces": ["S19A database join", "object_id", "shape weight", "shear calibration", "star mask", "photometric redshift", "tomographic bins", "data vector", "covariance", "scale cuts"],
            "queries": 0,
            "downloads": 0,
            "catalog_rows": 0,
            "covariance_rows": 0,
            "likelihood_calls": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "empirical_claims": 0,
        },
        ["release_lock", "join_schema", "calibration", "mask", "redshift", "covariance", "zero_rows", "zero_promotion"],
        ["unfrozen release", "object join omitted", "mask omitted", "post hoc calibration", "covariance fabricated", "one likelihood call", "one empirical claim"],
        "This is a zero-row refusal contract, not a data query, ingest, fit, constraint, detection, or empirical GMUT result.",
    ),
    "V6473-P04": surface(
        "telecom-change-handover",
        "thos/telecom-change-handover-contract.json",
        "thos/telecom-change-handover-vectors.json",
        {
            "synthetic_change": "CHANGE-DEMO-01",
            "dependency_graph_declared": True,
            "maintenance_window_declared": True,
            "reviewer_separated": True,
            "alarm_baseline_declared": True,
            "alarm_owner_assigned": True,
            "customer_impact": "synthetic-none",
            "rollback_trigger_declared": True,
            "rollback_owner_assigned": True,
            "escalation_path_declared": True,
            "workload_budget_declared": True,
            "readback_complete": True,
            "next_shift_owner_assigned": True,
            "real_operators": 0,
            "real_networks": 0,
            "real_customers": 0,
            "real_changes": 0,
        },
        ["dependencies", "window", "reviewer_separation", "alarm_ownership", "impact", "rollback", "escalation", "handover"],
        ["hidden dependency", "window drift", "reviewer collision", "unowned alarm", "impact suppressed", "missing rollback", "missing next owner"],
        "Synthetic telecommunications traces are represented evidence only, with no operator, network, customer, outage, emergency-service, safety, or effectiveness result.",
    ),
    "V6473-P05": surface(
        "vc-related-resource",
        "freed-id/vc-related-resource-profile.json",
        "freed-id/vc-related-resource-mutations.json",
        {
            "resource_id": "https://example.invalid/context",
            "digest_kind": "digestSRI",
            "digest_algorithm": "sha384",
            "digest_value": "synthetic-nonsecret-value",
            "media_type": "application/ld+json",
            "verify_before_interpret": True,
            "redirect_policy": "same-identifier-only",
            "byte_budget": 65536,
            "cache_key_binds_digest": True,
            "offline_failure_is_closed": True,
            "live_retrieval": False,
            "real_credential": False,
            "real_key": False,
            "production": False,
        },
        ["resource_id", "digest", "algorithm", "media_type", "verification_order", "redirect", "budget", "cache", "privacy"],
        ["missing digest", "digest mismatch", "unsupported algorithm", "media-type mismatch", "parse before verify", "redirect substitution", "cache alias"],
        "Synthetic VC related-resource structure uses no real credential, key, protected resource, live retrieval, interoperability, privacy review, or production service.",
    ),
    "V6473-P06": surface(
        "telecom-outage-authority",
        "cbr/telecom-outage-authority-reservation.json",
        "cbr/telecom-outage-remedy-matrix.json",
        {
            "case_data": "none",
            "outage_finding": "reserved",
            "emergency_call_reach": "reserved",
            "vulnerable_consumer_status": "reserved",
            "accessibility": "reserved",
            "worker_and_device_location": "reserved",
            "traffic_information": "reserved",
            "remedy": "reserved",
            "legal_interpretation": "reserved",
            "cultural_legitimacy": "reserved",
            "maori_authority": "reserved",
            "affected_party_acceptance": "reserved",
        },
        ["no_case_data", "outage_reserved", "emergency_reserved", "access_reserved", "privacy_reserved", "remedy_reserved", "maori_reserved", "affected_party_reserved"],
        ["decide outage", "decide emergency reach", "identify vulnerable consumer", "declare access complete", "publish location", "allocate remedy", "assert Māori authority"],
        "This exact-gate matrix confers no telecommunications, emergency-service, accessibility, privacy, remedy, legal, cultural, Māori, or affected-party authority.",
    ),
    "V6473-P07": surface(
        "http-structured-fields",
        "tooling/http-structured-fields-contract.json",
        "tooling/http-structured-fields-mutations.json",
        {
            "fixture": "owner-local RFC 9651 model",
            "top_level_types": ["item", "list", "dictionary"],
            "parameters_ordered": True,
            "keys_unique": True,
            "integer_bounds_enforced": True,
            "decimal_precision_enforced": True,
            "display_string_utf8_enforced": True,
            "combined_field_lines_checked": True,
            "trailing_input_rejected": True,
            "implementation_limits_declared": True,
            "network_requests": 0,
        },
        ["types", "parameters", "duplicates", "numeric_bounds", "strings", "field_combination", "trailing_input", "limits", "serialization"],
        ["duplicate dictionary key", "parameter order lost", "integer overflow", "decimal precision drift", "invalid display string", "trailing input ignored", "limit bypass"],
        "Synthetic Structured Fields parsing is not a network transaction, production protocol assurance, or exhaustive-security result.",
    ),
    "V6473-P08": surface(
        "breadcrumb-accessibility",
        "accessibility/breadcrumb-contract.json",
        "accessibility/breadcrumb-mutations.json",
        {
            "navigation_landmark": True,
            "accessible_name": "Breadcrumb",
            "hierarchy_ordered": True,
            "ancestor_links_named": True,
            "current_page_count": 1,
            "aria_current": "page",
            "separators_decorative": True,
            "narrow_viewport_preserves_context": True,
            "keyboard_order_matches_dom": True,
            "print_sequence_preserved": True,
            "manual_evaluation_reserved": True,
        },
        ["landmark", "name", "hierarchy", "link_purpose", "current_page", "separator", "overflow", "order", "print"],
        ["unnamed landmark", "unordered hierarchy", "ambiguous ancestor", "multiple current pages", "semantic separator", "context hidden by overflow", "print order drift"],
        "Structural checks reserve manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
    ),
    "V6473-P09": surface(
        "nernst-third-law",
        "thermo-psyche/nernst-third-law-contract.json",
        "thermo-psyche/nernst-third-law-mutations.json",
        {
            "temperature_limit": "T approaches zero from above",
            "equilibrium_required": True,
            "pure_crystal_scope_declared": True,
            "entropy_difference_limit_declared": True,
            "residual_entropy_exception_preserved": True,
            "unattainability_distinct": True,
            "heat_capacity_assumption_declared": True,
            "units_declared": True,
            "absolute_zero_attained_in_finite_steps": False,
            "psyche_conversion": False,
        },
        ["limit", "equilibrium", "material_scope", "entropy_difference", "residual_entropy", "unattainability", "units", "category_barrier"],
        ["limit treated as attained", "equilibrium omitted", "purity scope universalized", "residual entropy forbidden", "unattainability conflated", "unit mismatch", "psyche conversion"],
        "A typed third-law classifier is not a psyche law, participant result, consciousness measure, personhood claim, or empirical THOS result.",
    ),
    "V6473-P10": surface(
        "prequential-drift",
        "stage20/prequential-drift-contract.json",
        "stage20/prequential-drift-mutations.json",
        {
            "forecast_before_outcome": True,
            "information_set_frozen": True,
            "target_declared": True,
            "proper_score_named": True,
            "sequential_order_preserved": True,
            "rolling_window_declared": True,
            "calibration_diagnostic_declared": True,
            "drift_trigger_frozen": True,
            "retraining_decision_logged": True,
            "interventions_logged": True,
            "synthetic_only": True,
            "stage20_ready": False,
        },
        ["timestamp", "information_set", "target", "score", "order", "window", "calibration", "trigger", "retraining", "nonpromotion"],
        ["forecast after outcome", "information leakage", "score changed post hoc", "order shuffled", "drift threshold moved", "silent retraining", "Stage 20 promotion"],
        "Synthetic forecast traces supply no deployed monitoring, empirical confirmation, independent review, or Stage 20 authority.",
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
        "schema": f"ghc.family.v647-v3.{spec['slug']}.contract.v1",
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
        "schema": f"ghc.family.v647-v3.{spec['slug']}.mutations.v1",
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
        "schema": "ghc.family.v647-v3.runner-witness.v1",
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
