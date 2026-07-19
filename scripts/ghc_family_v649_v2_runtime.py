#!/usr/bin/env python3
"""Reusable bounded runtime for Ilyra Fen v649-v2 evidence surfaces.

The runtime evaluates synthetic, symbolic, structural, or zero-row fixtures only.
It does not perform network access, parse user material, make authority decisions,
or establish empirical, clinical, production, accessibility-complete, security-
complete, or Stage 20 claims.
"""

from __future__ import annotations

import argparse
import copy
import json
import threading
from pathlib import Path
from typing import Any


SURFACES: dict[str, dict[str, Any]] = {
    "barrier": {
        "proposal_id": "V6492-P01",
        "outcome": "completed",
        "obligations": ["generation_id", "party_count", "arrivals", "leader_action", "timeout", "broken_state", "abort", "reset_isolation", "worker_join", "evidence_credit"],
        "zero_counts": ["external_side_effects", "production_workers"],
    },
    "bphz": {
        "proposal_id": "V6492-P02",
        "outcome": "completed",
        "obligations": ["divergence_degree", "divergent_subgraphs", "valid_forests", "nested_subtractions", "overlap_refusal", "taylor_operator", "local_counterterms", "renormalization_conditions", "gauge_scope", "eft_domain", "units", "observation_firewall"],
        "zero_counts": ["real_observations", "likelihood_calls", "physical_predictions"],
    },
    "hetdex": {
        "proposal_id": "V6492-P03",
        "outcome": "open_gap",
        "obligations": ["product_identity", "source_catalog", "datacube_lineage", "selection", "line_classification", "sensitivity", "masks", "checksums", "covariance", "likelihood_lock"],
        "zero_counts": ["queries", "downloads", "catalog_rows", "datacubes", "spectra", "covariance_rows", "likelihood_calls", "posterior_samples", "constraints", "empirical_claims"],
    },
    "transfusion_handover": {
        "proposal_id": "V6492-P04",
        "outcome": "represented",
        "obligations": ["request_lineage", "specimen_lineage", "component_lineage", "sample_validity", "compatibility_state", "discrepancy_hold", "recall_state", "correction_readback", "workload_ceiling", "next_shift_acceptance"],
        "zero_counts": ["real_people", "real_specimens", "real_components", "clinical_decisions", "patient_outcomes", "blind_real_arms"],
    },
    "jwt_access_token": {
        "proposal_id": "V6492-P05",
        "outcome": "represented",
        "obligations": ["explicit_at_jwt_type", "algorithm_refusal", "issuer_binding", "audience_binding", "subject", "expiry", "issued_at", "jwt_id", "authorization_claims", "metadata_consistency", "confusion_refusal", "replay_refusal", "minimization"],
        "zero_counts": ["real_keys", "live_tokens", "accounts", "servers", "network_exchanges", "interop_events", "privacy_reviews", "security_reviews", "governance_decisions"],
    },
    "transfusion_authority": {
        "proposal_id": "V6492-P06",
        "outcome": "exact_gate",
        "obligations": ["clinical_authority_reserved", "consent_reserved", "access_reserved", "disclosure_reserved", "correction_reserved", "remedy_reserved", "legal_reserved", "cultural_reserved", "data_governance_reserved", "affected_party_reserved", "maori_authority_reserved"],
        "zero_counts": ["clinical_decisions", "consent_decisions", "disclosures", "remedy_allocations", "legal_decisions", "cultural_decisions", "maori_authority_decisions"],
    },
    "warc": {
        "proposal_id": "V6492-P07",
        "outcome": "completed",
        "obligations": ["version_line", "header_block", "record_type", "content_length", "record_id", "target_uri", "record_date", "digest_shape", "relation_headers", "revisit_profile", "truncation_reason", "resource_budget", "trailing_data_refusal"],
        "zero_counts": ["real_archive_payloads", "user_files_opened"],
    },
    "switch": {
        "proposal_id": "V6492-P08",
        "outcome": "completed",
        "obligations": ["binary_semantics", "role_or_native_fallback", "stable_label", "checked_state", "keyboard_path", "description", "group_label", "non_colour_state", "focus_visible", "contrast_reservation", "manual_evaluation_reserved"],
        "zero_counts": ["manual_keyboard_sessions", "assistive_technology_sessions", "affected_user_reviews"],
    },
    "gibbs_helmholtz": {
        "proposal_id": "V6492-P09",
        "outcome": "completed",
        "obligations": ["gibbs_over_temperature", "temperature_derivative", "enthalpy_relation", "fixed_pressure", "fixed_composition", "sign_convention", "units", "equilibrium_domain", "differentiability", "category_firewall"],
        "zero_counts": ["participants", "psyche_scores", "consciousness_claims"],
    },
    "synthetic_control": {
        "proposal_id": "V6492-P10",
        "outcome": "completed",
        "obligations": ["treated_unit", "intervention_time", "donor_eligibility", "predictor_balance", "preintervention_fit", "convex_weights", "interpolation_support", "in_space_placebo", "in_time_placebo", "spillover_check", "leakage_refusal", "sensitivity", "nonpromotion"],
        "zero_counts": ["participant_rows", "fitted_weights", "effect_estimates", "deployment_decisions", "stage20_promotions"],
    },
}


BOUNDARY = (
    "Bounded software, symbolic, structural, synthetic, or zero-row evidence only; "
    "not empirical confirmation, professional or clinical validation, legal or cultural "
    "authority, Māori authority, production readiness, exhaustive security, complete "
    "accessibility, independent reproduction, consciousness, personhood, Theory of "
    "Everything, or Stage 20 authority."
)


def valid_fixture(surface: str) -> dict[str, Any]:
    rule = SURFACES[surface]
    return {
        "schema": "ghc.family.v649-v2.synthetic-fixture.v1",
        "surface": surface,
        "proposal_id": rule["proposal_id"],
        "expected_outcome": rule["outcome"],
        "obligations_present": list(rule["obligations"]),
        "domain_valid": True,
        "authority_promotion": False,
        "lineage_intact": True,
        "resource_budget_ok": True,
        "forbidden_claims": [],
        "zero_gate_counts": {name: 0 for name in rule["zero_counts"]},
        "boundary": BOUNDARY,
    }


def mutation_fixtures(surface: str) -> list[dict[str, Any]]:
    base = valid_fixture(surface)
    mutations: list[tuple[str, str]] = [
        ("missing_obligation", "required formal or protocol obligation removed"),
        ("invalid_domain", "typed or protocol domain invalidated"),
        ("authority_promotion", "software promoted into reserved authority"),
        ("lineage_break", "required lineage broken"),
        ("budget_violation", "declared resource budget exceeded"),
        ("forbidden_claim", "bounded evidence promoted into a forbidden claim"),
        ("zero_gate_breach", "real-world or authority-dependent counter made nonzero"),
    ]
    rows: list[dict[str, Any]] = []
    for index, (kind, reason) in enumerate(mutations, 1):
        fixture = copy.deepcopy(base)
        if kind == "missing_obligation":
            fixture["obligations_present"] = fixture["obligations_present"][1:]
        elif kind == "invalid_domain":
            fixture["domain_valid"] = False
        elif kind == "authority_promotion":
            fixture["authority_promotion"] = True
        elif kind == "lineage_break":
            fixture["lineage_intact"] = False
        elif kind == "budget_violation":
            fixture["resource_budget_ok"] = False
        elif kind == "forbidden_claim":
            fixture["forbidden_claims"] = ["production_or_authority_promotion"]
        elif kind == "zero_gate_breach":
            first = next(iter(fixture["zero_gate_counts"]))
            fixture["zero_gate_counts"][first] = 1
        rows.append({"mutation_id": f"{rule_id(surface)}-M{index:02d}", "kind": kind, "reason": reason, "fixture": fixture})
    return rows


def rule_id(surface: str) -> str:
    return SURFACES[surface]["proposal_id"]


def evaluate(surface: str, fixture: dict[str, Any]) -> dict[str, Any]:
    if surface not in SURFACES:
        raise ValueError(f"unknown surface: {surface}")
    rule = SURFACES[surface]
    issues: list[str] = []
    if fixture.get("surface") != surface:
        issues.append("surface_mismatch")
    if fixture.get("proposal_id") != rule["proposal_id"]:
        issues.append("proposal_mismatch")
    if fixture.get("expected_outcome") != rule["outcome"]:
        issues.append("outcome_mismatch")
    present = set(fixture.get("obligations_present", []))
    missing = [item for item in rule["obligations"] if item not in present]
    if missing:
        issues.append("missing_obligations:" + ",".join(missing))
    if fixture.get("domain_valid") is not True:
        issues.append("invalid_domain")
    if fixture.get("authority_promotion") is not False:
        issues.append("authority_promotion")
    if fixture.get("lineage_intact") is not True:
        issues.append("lineage_break")
    if fixture.get("resource_budget_ok") is not True:
        issues.append("resource_budget_violation")
    if fixture.get("forbidden_claims"):
        issues.append("forbidden_claim_promotion")
    counts = fixture.get("zero_gate_counts", {})
    for name in rule["zero_counts"]:
        if counts.get(name) != 0:
            issues.append(f"zero_gate_breach:{name}")
    return {
        "schema": "ghc.family.v649-v2.surface-evaluation.v1",
        "surface": surface,
        "proposal_id": rule["proposal_id"],
        "accepted": not issues,
        "issues": issues,
        "observed_outcome": rule["outcome"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }


def barrier_operational_witness(parties: int = 3) -> dict[str, Any]:
    lock = threading.Lock()
    arrivals: list[int] = []
    releases: list[int] = []
    action_count = 0

    def action() -> None:
        nonlocal action_count
        with lock:
            action_count += 1

    barrier = threading.Barrier(parties, action=action, timeout=3.0)

    def worker(index: int) -> None:
        with lock:
            arrivals.append(index)
        barrier.wait()
        with lock:
            releases.append(index)

    workers = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(parties)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(timeout=5.0)
    joined = all(not worker.is_alive() for worker in workers)
    return {
        "schema": "ghc.family.v649-v2.barrier-witness.v1",
        "parties": parties,
        "arrivals": sorted(arrivals),
        "releases": sorted(releases),
        "leader_action_count": action_count,
        "broken": barrier.broken,
        "workers_joined": joined,
        "passed": joined and len(arrivals) == parties and len(releases) == parties and action_count == 1 and not barrier.broken,
        "external_side_effects": 0,
        "boundary": BOUNDARY,
    }


def cli(fixed_surface: str | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate one bounded v649-v2 family fixture.")
    if fixed_surface is None:
        parser.add_argument("--surface", choices=sorted(SURFACES), required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    surface = fixed_surface or args.surface
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    result = evaluate(surface, fixture)
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(cli())
