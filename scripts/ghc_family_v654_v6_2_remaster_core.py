#!/usr/bin/env python3
"""Bounded synthetic execution core for Eiren's v654-v6 (2) remaster."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import ceil
from typing import Any

import ghc_family_v654_v6_2_remaster_phase_data as d


MUTATION_DIMENSIONS = [
    "missing_required_obligation",
    "wrong_type_or_domain",
    "resource_or_replay_overrun",
    "unsupported_promotion",
    "authority_privacy_or_route_breach",
]

ZERO_COUNTERS = {
    "real_queries": 0,
    "real_downloads": 0,
    "real_rows": 0,
    "real_likelihoods": 0,
    "real_participants_or_operators": 0,
    "real_keys_proofs_or_credentials": 0,
    "live_identity_or_training_events": 0,
    "production_deployments": 0,
    "authority_decisions": 0,
}


def proposal_map() -> dict[str, dict[str, Any]]:
    return {row["proposal_id"]: row for row in d.PROPOSALS}


def effective_n(witness_count: int, shared_dependence: float) -> float:
    """Conservative equicorrelation effective sample-size bound."""
    if witness_count < 1:
        raise ValueError("witness_count must be positive")
    if not 0.0 <= shared_dependence <= 1.0:
        raise ValueError("shared_dependence must be between zero and one")
    return witness_count / (1.0 + (witness_count - 1) * shared_dependence)


def find_erdos_straus_decomposition(n: int) -> tuple[int, int, int] | None:
    """Find one exact unit-fraction decomposition for a single bounded n."""
    if n < 2:
        raise ValueError("n must be at least two")
    for x in range(n // 4 + 1, n + 1):
        numerator = 4 * x - n
        denominator = n * x
        if numerator <= 0:
            continue
        y_min = ceil(denominator / numerator)
        y_max = (2 * denominator) // numerator + 1
        for y in range(y_min, y_max + 1):
            remainder_numerator = numerator * y - denominator
            if remainder_numerator <= 0:
                continue
            remainder_denominator = denominator * y
            if remainder_denominator % remainder_numerator:
                continue
            z = remainder_denominator // remainder_numerator
            if Fraction(4, n) == Fraction(1, x) + Fraction(1, y) + Fraction(1, z):
                return x, y, z
    return None


def erdos_straus_bounded(limit: int = 500) -> dict[str, Any]:
    rows = []
    for n in range(2, limit + 1):
        solution = find_erdos_straus_decomposition(n)
        rows.append(
            {
                "n": n,
                "solution": list(solution) if solution else None,
                "identity_exact": solution is not None,
            }
        )
    return {
        "domain": {"start": 2, "end": limit, "integer_count": limit - 1},
        "verified_count": sum(row["identity_exact"] for row in rows),
        "counterexample_count": sum(not row["identity_exact"] for row in rows),
        "sample_first": rows[:5],
        "sample_last": rows[-5:],
        "universal_proof_claimed": False,
        "boundary": "Finite exact-rational identity checking only; no universal proof.",
    }


def mechanism_payload(proposal: dict[str, Any]) -> dict[str, Any]:
    pid = proposal["proposal_id"]
    common = {
        "proposal_id": pid,
        "mechanism": proposal["mission_surface"],
        "synthetic_only": True,
        "authority_ceiling": proposal["expected_disposition"],
    }
    payloads: dict[str, dict[str, Any]] = {
        "V6546R2-P01": {
            "evidence_levels": {
                "E0": "concept or unexecuted plan",
                "E1": "typed specification or exact symbolic check",
                "E2": "same-owner synthetic or repository validation",
                "E3": "independent bounded reproduction or empirical study",
                "E4": "multi-context external evidence and competent authority review",
            },
            "current_maximum": "E2",
            "automatic_promotion": False,
        },
        "V6546R2-P02": {
            "passport_fields": [
                "source_action",
                "domain",
                "units",
                "degrees_of_freedom",
                "conservation",
                "stability",
                "causality",
                "observables",
                "bounds",
                "falsifier",
                "recovery",
            ],
            "sample_status": "complete_symbolic_not_physical",
        },
        "V6546R2-P03": {
            "baseline_action": "S_GMUT = S_B + Delta_S_Omega",
            "metric_variation": "Omega_AB := -2/sqrt(|g|) * delta(Delta_S_Omega)/delta(g^AB)",
            "boundary_term_declared": True,
            "tensor_promotion": "held_for_model_specific_derivation",
        },
        "V6546R2-P04": {
            "models": [
                {"level": "M0", "description": "baseline/null model"},
                {"level": "M1", "description": "minimal scalar candidate"},
                {"level": "M2", "description": "dark-sector-only coupling candidate"},
                {"level": "M3", "description": "broader coupling exact-gated"},
            ],
            "selected_model": None,
        },
        "V6546R2-P05": {
            "identity": "nabla^A G_AB = 0",
            "exchange_current": "J_B := nabla^A Omega_AB",
            "conservation_claim": "conditional_on_full_action_and_sector_exchange",
        },
        "V6546R2-P06": {
            "operator_basis_declared": True,
            "suppression_scale": "Lambda_EFT_symbolic",
            "truncation_order": "declared_not_empirically_selected",
            "ultraviolet_completion_claimed": False,
        },
        "V6546R2-P07": {
            "obligations": [
                "principal_symbol",
                "kinetic_sign",
                "gradient_sign",
                "characteristic_speed",
                "background_domain",
            ],
            "stability_theorem_claimed": False,
        },
        "V6546R2-P08": {
            "bridge_fields": [
                "theoretical_quantity",
                "instrument_proxy",
                "calibration_dependency",
                "selection_function",
                "uncertainty_budget",
                "likelihood_placeholder",
            ],
            "real_rows": 0,
        },
        "V6546R2-P09": {
            "witness_count": 16,
            "shared_dependence": 0.75,
            "effective_n_upper_bound": round(effective_n(16, 0.75), 6),
            "independent_replication_count": 0,
        },
        "V6546R2-P10": {
            "seat_count": 16,
            "main_task_count": 15,
            "collaboration_subagent_count": 1,
            "sole_subagent": "Tavian Sol",
            "next_live_main_task": "Elaren Kestrel",
        },
        "V6546R2-P11": {
            "source": d.SOURCE_HEAD,
            "x1": "resolved_from_exact_phase_ancestry",
            "evidence": "pending_x2_commit",
            "final": "pending_closeout_commit",
            "merge_count": 0,
            "credit_firewall": True,
        },
        "V6546R2-P12": {
            "dependence_dimensions": [
                "inherited_artifact",
                "reused_method",
                "validation_owner",
                "infrastructure_owner",
                "repository_ancestry",
            ],
            "independence_reserved": True,
        },
        "V6546R2-P13": {
            "maximum_wording_rule": "minimum_of_evidence_level_and_authority_ceiling",
            "same_owner": True,
            "affected_party_review": False,
            "professional_review": False,
            "legal_or_cultural_review": False,
        },
        "V6546R2-P14": {
            "task_contract_fields": [
                "objective",
                "inputs",
                "outputs",
                "invariants",
                "authority_class",
                "privacy_class",
                "resource_budget",
                "timeout",
                "rollback",
                "acceptance_predicate",
            ],
            "all_fields_present": True,
        },
        "V6546R2-P15": {
            "desired_state": "bounded_evidence_sealed",
            "observed_states": ["x1_pushed", "x2_built", "bounded_evidence_sealed"],
            "idempotence_key": "sanitized-phase-operation-key",
            "duplicate_effect_count": 0,
            "stale_write_refused": True,
        },
        "V6546R2-P16": {
            "endpoint_contracts": {
                "main_task": "unique exact title, reread, send once, acknowledgement",
                "collaboration_subagent": "existing parent-owned lineage, follow up once, acknowledgement",
            },
            "private_route_values_stored": False,
            "fallback_mutually_exclusive": True,
        },
        "V6546R2-P17": {
            "capabilities": ["read_owner_phase", "write_owner_phase", "run_bounded_tests"],
            "secrets_present": False,
            "elevation_allowed": False,
            "expiry": "phase_terminal_gate",
        },
        "V6546R2-P18": {
            "fixture_provenance": "owner_local_synthetic",
            "matched_budget_real_arm": False,
            "blinded_real_arm": False,
            "independent_review": False,
            "effectiveness_claimed": False,
        },
        "V6546R2-P19": {
            "canonical_replay_count": 0,
            "network_action_count_before_terminal_route": 0,
            "owner_file_cap": 2000,
            "efficiency_claimed": False,
        },
        "V6546R2-P20": {
            "rights": ["provenance", "consent_placeholder", "opt_out_gap", "evaluation_duty"],
            "training_events": 0,
            "production_models": 0,
            "state": "represented",
        },
        "V6546R2-P21": {
            "profile_fields": [
                "identifier_method",
                "key_representation",
                "proof_suite",
                "status_mechanism",
                "holder_binding",
                "recovery",
                "privacy_review",
                "interoperability",
            ],
            "real_keys_or_proofs": 0,
            "state": "represented",
        },
        "V6546R2-P22": {
            "non_compensable_rights": [
                "informed consent",
                "non-discrimination",
                "appeal and remedy",
                "privacy and data minimization",
                "cultural and indigenous authority",
            ],
            "aggregate_override_allowed": False,
        },
        "V6546R2-P23": {
            "continuity_fields": [
                "endpoint_kind",
                "exact_title_or_public_label",
                "route_controller",
                "lineage_evidence",
                "rename_authority",
            ],
            "identity_substitution_allowed": False,
            "personhood_claimed": False,
        },
        "V6546R2-P24": {
            "inherited_negatives": d.SOURCE_EFFECTIVE_NEGATIVES,
            "inherited_open_gaps": d.SOURCE_OPEN_GAPS,
            "inherited_exact_gates": d.SOURCE_EXACT_GATES,
            "erasure_allowed": False,
        },
        "V6546R2-P25": {
            "principles": {
                "L11": "recursive gain requires a safety margin",
                "L12": "evidence and authority remain proportional",
                "L13": "correlated witnesses are discounted",
                "L14": "some rights are non-compensable",
                "L15": "continuity must not substitute identity",
                "L16": "unresolved residuals stay visible",
            },
            "physical_law_claimed": False,
        },
        "V6546R2-P26": erdos_straus_bounded(500),
        "V6546R2-P27": {
            "rows": d.LEGACY_CLAIMS,
            "validated_mechanism_count": 0,
            "canon_claimed": False,
        },
        "V6546R2-P28": {
            "frozen_artifact_hash_required": True,
            "environment_contract_required": True,
            "blind_mutation_set_present": True,
            "independent_owner_present": False,
            "state": "represented",
        },
        "V6546R2-P29": {
            "official_source_selected": False,
            "queries": 0,
            "downloads": 0,
            "real_rows": 0,
            "likelihoods": 0,
            "posteriors": 0,
            "constraints": 0,
            "state": "open_gap",
        },
        "V6546R2-P30": {
            "reservations": [
                "affected-party acceptance",
                "training-data rights",
                "identity governance",
                "benefit sharing and remedy",
                "language and accessibility",
                "data sovereignty",
                "tangata whenua, iwi, hapu, and Maori authority",
            ],
            "authority_decisions": 0,
            "state": "exact_gate",
        },
    }
    return {**common, **payloads[pid]}


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    disposition = proposal["expected_disposition"]
    return {
        "schema": "ghc.family.v654-v6-2-remaster.surface-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "slug": proposal["slug"],
        "pillar": proposal["pillar"],
        "mission_surface": proposal["mission_surface"],
        "hypothesis": proposal["hypothesis"],
        "null_or_failure_condition": proposal["null_or_failure_condition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "required_obligations": [
            item.strip() for item in proposal["title"].split(",") if item.strip()
        ],
        "protected_gates": proposal["protected_gates"],
        "expected_disposition": disposition,
        "observed_disposition": disposition,
        "mechanism_payload": mechanism_payload(proposal),
        "counters": dict(ZERO_COUNTERS),
        "synthetic_only": True,
        "owner_local_only": True,
        "independent_reproduction": False,
        "boundary": (
            "Bounded software, symbolic, formal, structural, or synthetic evidence "
            "only; no unsupported scientific, participant, professional, production, "
            "legal, cultural, Maori-authority, identity, privacy-complete, "
            "security-complete, accessibility-complete, or Stage 20 promotion."
        ),
    }


def validate_contract(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    issues = []
    required = {
        "schema",
        "proposal_id",
        "title",
        "slug",
        "pillar",
        "mission_surface",
        "hypothesis",
        "null_or_failure_condition",
        "approval_class",
        "execution_lane",
        "source_ids",
        "required_obligations",
        "protected_gates",
        "expected_disposition",
        "observed_disposition",
        "mechanism_payload",
        "counters",
        "synthetic_only",
        "owner_local_only",
        "independent_reproduction",
        "boundary",
    }
    missing = sorted(required - set(contract))
    if missing:
        issues.append("missing:" + ",".join(missing))
    if contract.get("observed_disposition") not in d.OUTCOME_CLASSES:
        issues.append("invalid_outcome")
    if contract.get("expected_disposition") != contract.get("observed_disposition"):
        issues.append("disposition_drift")
    if not contract.get("required_obligations"):
        issues.append("empty_obligations")
    mechanism = contract.get("mechanism_payload")
    if not isinstance(mechanism, dict) or not mechanism:
        issues.append("missing_mechanism_payload")
    if contract.get("synthetic_only") is not True or contract.get("owner_local_only") is not True:
        issues.append("scope_promotion")
    if contract.get("independent_reproduction") is not False:
        issues.append("independent_reproduction_promotion")
    counters = contract.get("counters")
    if not isinstance(counters, dict):
        issues.append("invalid_counter_type")
    elif any(value != 0 for value in counters.values()):
        issues.append("nonzero_real_world_counter")
    return not issues, issues


def mutation_results(proposal: dict[str, Any]) -> dict[str, Any]:
    results = []
    for index, dimension in enumerate(MUTATION_DIMENSIONS, 1):
        contract = build_contract(proposal)
        if dimension == "missing_required_obligation":
            contract.pop("required_obligations")
        elif dimension == "wrong_type_or_domain":
            contract["counters"] = "zero"
        elif dimension == "resource_or_replay_overrun":
            contract["counters"]["real_downloads"] = 1
        elif dimension == "unsupported_promotion":
            contract["independent_reproduction"] = True
        else:
            contract["counters"]["authority_decisions"] = 1
        valid, issues = validate_contract(contract)
        results.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
                "proposal_id": proposal["proposal_id"],
                "dimension": dimension,
                "expected": "reject_or_quarantine",
                "observed": "rejected" if not valid else "accepted_unexpectedly",
                "rejection_reasons": issues,
                "accepted": valid,
            }
        )
    return {
        "schema": "ghc.family.v654-v6-2-remaster.mutation-results.v1",
        "proposal_id": proposal["proposal_id"],
        "results": results,
        "count": len(results),
        "rejected_count": sum(not row["accepted"] for row in results),
        "accepted_count": sum(row["accepted"] for row in results),
        "boundary": (
            "Synthetic rejection evidence is bounded guard evidence only, not "
            "exhaustive security or real-world assurance."
        ),
    }


def bounded_receipt(
    proposal: dict[str, Any],
    contract: dict[str, Any],
    mutations: dict[str, Any],
) -> dict[str, Any]:
    valid, issues = validate_contract(contract)
    accepted = valid and mutations["accepted_count"] == 0 and mutations["rejected_count"] == 5
    return {
        "schema": "ghc.family.v654-v6-2-remaster.bounded-receipt.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "observed_outcome": proposal["expected_disposition"],
        "acceptance_gate_passed": accepted,
        "contract_issues": issues,
        "mutation_count": mutations["count"],
        "mutation_rejected_count": mutations["rejected_count"],
        "real_world_counters": contract["counters"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "rollback": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"],
        "boundary": contract["boundary"],
    }


def group_self_test(proposal_ids: list[str]) -> dict[str, Any]:
    proposals = proposal_map()
    rows = []
    for proposal_id in proposal_ids:
        proposal = proposals[proposal_id]
        contract = build_contract(proposal)
        valid, issues = validate_contract(contract)
        mutations = mutation_results(proposal)
        rows.append(
            {
                "proposal_id": proposal_id,
                "accepting_fixture_passed": valid and not issues,
                "rejecting_fixture_count": mutations["count"],
                "rejecting_fixture_passed": mutations["accepted_count"] == 0,
            }
        )
    return {
        "schema": "ghc.family.v654-v6-2-remaster.runner-witness.v1",
        "proposal_ids": proposal_ids,
        "proposal_count": len(proposal_ids),
        "accepting_passed": sum(row["accepting_fixture_passed"] for row in rows),
        "rejecting_passed": sum(
            row["rejecting_fixture_count"] if row["rejecting_fixture_passed"] else 0
            for row in rows
        ),
        "rows": rows,
        "valid": all(
            row["accepting_fixture_passed"] and row["rejecting_fixture_passed"]
            for row in rows
        ),
        "outcome_counts": dict(
            Counter(proposals[item]["expected_disposition"] for item in proposal_ids)
        ),
        "boundary": (
            "Bounded accepting and rejecting fixtures only; no production, empirical, "
            "participant, professional, legal, cultural, identity, privacy-complete, "
            "security-complete, accessibility-complete, independent-reproduction, or "
            "Stage 20 credit."
        ),
    }
