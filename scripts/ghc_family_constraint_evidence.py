#!/usr/bin/env python3
"""Build the bounded GHC Family v642-v7 constraint-evidence packet.

The implementation is standard-library-only. It exercises structural and
synthetic fixtures while keeping empirical, participant, production, legal,
cultural, deployment, identity, proof/canon, accessibility-completeness,
exhaustive-security, and independent-reproduction claims false.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PHASE = "v642-gmut-thos-v7-x1-x2"
OWNER = "Tamar Vey"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6427-P01": "completed",
    "V6427-P02": "completed",
    "V6427-P03": "represented",
    "V6427-P04": "represented",
    "V6427-P05": "completed",
    "V6427-P06": "exact_gate",
    "V6427-P07": "completed",
    "V6427-P08": "completed",
    "V6427-P09": "completed",
    "V6427-P10": "open_gap",
}
PROTECTED_CLAIMS = [
    "agi",
    "asi",
    "complete_accessibility",
    "consciousness",
    "cultural_ratification",
    "deployment",
    "empirical_gmut_confirmation",
    "enacted_law",
    "exhaustive_security",
    "final_physics",
    "independent_team_reproduction",
    "legal_interpretation",
    "maori_authority",
    "maori_data_governance",
    "maori_wording_authorized",
    "personhood",
    "production_readiness",
    "proof_or_canon",
    "sentience",
    "stage20_ready",
    "theory_of_everything",
    "thos_superiority",
    "unique_prediction",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def normalized_size(path: Path) -> int:
    return len(normalized_bytes(path))


def _decision(ok: bool, accepted: str, reasons: list[str]) -> tuple[str, list[str]]:
    return (accepted if ok else "reject", reasons)


def citation_anchor_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["version_pinned"], "floating_source_version"),
        (case["fragment_stable"], "citation_fragment_drift"),
        (case["authority_root_match"], "redirect_crossed_authority_root"),
        (case["redirect_depth"] <= 2, "redirect_depth_exceeded"),
        (case["secure_scheme"], "insecure_source_scheme"),
        (case["alias_deduplicated"], "canonical_alias_double_counted"),
        (case["source_role_preserved"], "source_role_substitution"),
        (not case["resolution_called_truth"], "link_resolution_promoted_to_truth"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def constraint_algebra_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["primary_constraints_declared"], "primary_constraints_undeclared"),
        (case["secondary_constraints_closed"], "secondary_constraint_chain_open"),
        (case["poisson_brackets_closed"], "constraint_bracket_not_closed"),
        (case["class_counts_valid"], "first_second_class_misclassification"),
        (case["reduced_phase_space_even"], "odd_reduced_phase_space_dimension"),
        (case["dof_count_matches"], "physical_degree_of_freedom_mismatch"),
        (case["dimensions_valid"], "dimension_mismatch"),
        (not case["empirical_promotion"], "structural_pass_promoted_to_empirical_claim"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def observation_process_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["synthetic_only"], "non_synthetic_input"),
        (case["real_rows"] == 0, "real_rows_without_preregistration"),
        (case["observation_kind_valid"], "censoring_truncation_semantics_invalid"),
        (case["bounds_ordered"], "interval_bounds_reversed"),
        (case["sampling_frame_valid"], "truncation_sampling_frame_invalid"),
        (case["measurement_error_declared"], "measurement_error_omitted"),
        (case["units_valid"], "measurement_error_unit_mismatch"),
        (case["missingness_declared"], "informative_missingness_undeclared"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "represented", reasons)


def thos_estimand_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["strategy_preregistered"], "post_outcome_estimand_switch"),
        (case["outcome_blind"], "deviation_handling_unblinded"),
        (case["population_aligned"], "estimand_population_mismatch"),
        (case["rescue_actions_declared"], "rescue_action_hidden"),
        (case["adherence_symmetric"], "asymmetric_nonadherence_exclusion"),
        (case["matched_budget"], "matched_budget_violation"),
        (
            case["real_participants"] == 0
            and case["real_raters"] == 0
            and case["real_arms"] == 0,
            "unreviewed_real_arm_execution",
        ),
        (not case["ethics_or_superiority_claimed"], "protocol_promoted_to_ethics_or_superiority_result"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "represented", reasons)


def schema_evolution_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["version_pinned"], "floating_schema_or_context"),
        (case["required_claims_preserved"], "required_claim_removed"),
        (case["protected_terms_preserved"], "protected_term_redefined"),
        (case["unknown_critical_rejected"], "unknown_critical_field_ignored"),
        (case["downgrade_explicit"], "silent_semantic_downgrade"),
        (case["canonical_semantics_stable"], "canonicalization_semantic_divergence"),
        (case["real_keys"] == 0 and case["real_proofs"] == 0, "real_cryptography_claim_in_fixture"),
        (not case["production_claimed"], "structural_pass_promoted_to_production"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def jurisdiction_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (not case["governing_law_selected"], "technical_artifact_selected_governing_law"),
        (not case["technical_forum_claim"], "technical_owner_claimed_forum_competence"),
        (case["rights_floor_preserved"], "rights_floor_displaced"),
        (case["remedy_access_preserved"], "remedy_access_erased"),
        (not case["contains_maori_wording"], "unauthorized_maori_wording_present"),
        (not case["silence_as_consent"], "silence_treated_as_consent"),
        (not case["legal_or_cultural_completion_claimed"], "synthetic_vector_claimed_law_or_ratification"),
        (case["competent_authority_deferred"], "competent_authority_not_deferred"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "exact_gate", reasons)


def namespace_confinement_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["case_alias_rejected"], "case_alias_bypass"),
        (case["device_name_rejected"], "reserved_device_name_accepted"),
        (case["alternate_stream_rejected"], "alternate_data_stream_accepted"),
        (case["drive_relative_rejected"], "drive_relative_path_accepted"),
        (case["traversal_rejected"], "parent_traversal_accepted"),
        (case["short_alias_rejected"], "short_name_alias_bypass"),
        (case["reparse_confined"], "reparse_target_outside_owned_root"),
        (case["resource_ceiling_enforced"], "path_resource_ceiling_missing"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def stochastic_replay_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["seed_pinned"], "seed_missing_or_floating"),
        (case["generator_pinned"], "generator_implementation_floating"),
        (case["runtime_pinned"], "runtime_version_floating"),
        (case["streams_partitioned"], "pseudorandom_stream_overlap"),
        (case["draw_count_matches"], "draw_count_diverged"),
        (case["retry_draws_declared"], "hidden_retry_draws"),
        (case["stochastic_budget_respected"], "stochastic_budget_exceeded"),
        (not case["independent_reproduction_claimed"], "same_owner_called_independent_reproduction"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def open_system_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (case["boundary_declared"], "system_boundary_undeclared"),
        (case["system_kind_valid"], "open_closed_system_kind_invalid"),
        (case["stock_flow_compatible"], "stock_flow_type_mismatch"),
        (case["state_rate_compatible"], "state_rate_type_mismatch"),
        (case["exchange_flux_declared"], "boundary_exchange_flux_omitted"),
        (case["dimensions_valid"], "dimension_mismatch"),
        (case["entropy_domain_preserved"], "shannon_thermodynamic_entropy_substitution"),
        (not case["law_or_consciousness_claimed"], "analogy_promoted_to_law_or_consciousness"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "accept", reasons)


def stage20_abstention_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    checks = [
        (not case["technical_owner_sets_external_loss"], "technical_owner_invented_external_loss_weights"),
        (case["abstains_when_prerequisite_missing"], "missing_prerequisite_did_not_force_abstention"),
        (not case["cross_pillar_compensation"], "one_pillar_compensated_for_another"),
        (case["veto_preserved"], "veto_overridden"),
        (case["negative_count_preserved"], "retained_negatives_reduced"),
        (case["reopening_requires_new_evidence"], "reopened_without_new_qualified_evidence"),
        (case["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal_verdict_promoted"),
        (not case["protected_claim_true"], "protected_claim_promoted"),
    ]
    reasons = [reason for ok, reason in checks if not ok]
    return _decision(not reasons, "open_gap", reasons)


Decision = Callable[[dict[str, Any]], tuple[str, list[str]]]


def _group(
    proposal_id: str,
    decision: Decision,
    accepted: str,
    base: dict[str, Any],
    mutations: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    cases = [{"case_id": f"{proposal_id}-CANONICAL", **base, "expected": accepted}]
    for suffix, changes in mutations:
        case = copy.deepcopy(base)
        case.update(changes)
        cases.append({"case_id": f"{proposal_id}-{suffix}", **case, "expected": "reject"})
    if len(cases) != 8:
        raise ValueError(f"{proposal_id} must have one canonical and seven mutations")
    return {"proposal_id": proposal_id, "decision": decision, "cases": cases}


def case_groups() -> list[dict[str, Any]]:
    return [
        _group(
            "V6427-P01",
            citation_anchor_decision,
            "accept",
            dict(version_pinned=True, fragment_stable=True, authority_root_match=True, redirect_depth=1, secure_scheme=True, alias_deduplicated=True, source_role_preserved=True, resolution_called_truth=False),
            [
                ("FLOATING", {"version_pinned": False}),
                ("FRAGMENT", {"fragment_stable": False}),
                ("AUTHORITY", {"authority_root_match": False}),
                ("REDIRECT", {"redirect_depth": 5}),
                ("SCHEME", {"secure_scheme": False}),
                ("ALIAS", {"alias_deduplicated": False}),
                ("ROLE-TRUTH", {"source_role_preserved": False, "resolution_called_truth": True}),
            ],
        ),
        _group(
            "V6427-P02",
            constraint_algebra_decision,
            "accept",
            dict(primary_constraints_declared=True, secondary_constraints_closed=True, poisson_brackets_closed=True, class_counts_valid=True, reduced_phase_space_even=True, dof_count_matches=True, dimensions_valid=True, empirical_promotion=False),
            [
                ("PRIMARY", {"primary_constraints_declared": False}),
                ("SECONDARY", {"secondary_constraints_closed": False}),
                ("BRACKET", {"poisson_brackets_closed": False}),
                ("CLASS", {"class_counts_valid": False}),
                ("ODD", {"reduced_phase_space_even": False}),
                ("DOF", {"dof_count_matches": False}),
                ("DIMENSION-EMPIRICAL", {"dimensions_valid": False, "empirical_promotion": True}),
            ],
        ),
        _group(
            "V6427-P03",
            observation_process_decision,
            "represented",
            dict(synthetic_only=True, real_rows=0, observation_kind_valid=True, bounds_ordered=True, sampling_frame_valid=True, measurement_error_declared=True, units_valid=True, missingness_declared=True),
            [
                ("REAL-ROW", {"real_rows": 1}),
                ("KIND", {"observation_kind_valid": False}),
                ("BOUNDS", {"bounds_ordered": False}),
                ("FRAME", {"sampling_frame_valid": False}),
                ("ERROR", {"measurement_error_declared": False}),
                ("UNITS", {"units_valid": False}),
                ("MISSINGNESS", {"missingness_declared": False}),
            ],
        ),
        _group(
            "V6427-P04",
            thos_estimand_decision,
            "represented",
            dict(strategy_preregistered=True, outcome_blind=True, population_aligned=True, rescue_actions_declared=True, adherence_symmetric=True, matched_budget=True, real_participants=0, real_raters=0, real_arms=0, ethics_or_superiority_claimed=False),
            [
                ("STRATEGY", {"strategy_preregistered": False}),
                ("UNBLINDED", {"outcome_blind": False}),
                ("POPULATION", {"population_aligned": False}),
                ("RESCUE", {"rescue_actions_declared": False}),
                ("ADHERENCE", {"adherence_symmetric": False}),
                ("BUDGET", {"matched_budget": False}),
                ("REAL-CLAIM", {"real_participants": 1, "ethics_or_superiority_claimed": True}),
            ],
        ),
        _group(
            "V6427-P05",
            schema_evolution_decision,
            "accept",
            dict(version_pinned=True, required_claims_preserved=True, protected_terms_preserved=True, unknown_critical_rejected=True, downgrade_explicit=True, canonical_semantics_stable=True, real_keys=0, real_proofs=0, production_claimed=False),
            [
                ("FLOATING", {"version_pinned": False}),
                ("REQUIRED", {"required_claims_preserved": False}),
                ("TERM", {"protected_terms_preserved": False}),
                ("CRITICAL", {"unknown_critical_rejected": False}),
                ("DOWNGRADE", {"downgrade_explicit": False}),
                ("CANONICAL", {"canonical_semantics_stable": False}),
                ("PRODUCTION", {"real_keys": 1, "real_proofs": 1, "production_claimed": True}),
            ],
        ),
        _group(
            "V6427-P06",
            jurisdiction_decision,
            "exact_gate",
            dict(governing_law_selected=False, technical_forum_claim=False, rights_floor_preserved=True, remedy_access_preserved=True, contains_maori_wording=False, silence_as_consent=False, legal_or_cultural_completion_claimed=False, competent_authority_deferred=True),
            [
                ("LAW", {"governing_law_selected": True}),
                ("FORUM", {"technical_forum_claim": True}),
                ("RIGHTS", {"rights_floor_preserved": False}),
                ("REMEDY", {"remedy_access_preserved": False}),
                ("WORDING", {"contains_maori_wording": True}),
                ("SILENCE", {"silence_as_consent": True}),
                ("AUTHORITY", {"legal_or_cultural_completion_claimed": True, "competent_authority_deferred": False}),
            ],
        ),
        _group(
            "V6427-P07",
            namespace_confinement_decision,
            "accept",
            dict(case_alias_rejected=True, device_name_rejected=True, alternate_stream_rejected=True, drive_relative_rejected=True, traversal_rejected=True, short_alias_rejected=True, reparse_confined=True, resource_ceiling_enforced=True),
            [
                ("CASE", {"case_alias_rejected": False}),
                ("DEVICE", {"device_name_rejected": False}),
                ("STREAM", {"alternate_stream_rejected": False}),
                ("DRIVE", {"drive_relative_rejected": False}),
                ("TRAVERSAL", {"traversal_rejected": False}),
                ("SHORT", {"short_alias_rejected": False}),
                ("REPARSE-CEILING", {"reparse_confined": False, "resource_ceiling_enforced": False}),
            ],
        ),
        _group(
            "V6427-P08",
            stochastic_replay_decision,
            "accept",
            dict(seed_pinned=True, generator_pinned=True, runtime_pinned=True, streams_partitioned=True, draw_count_matches=True, retry_draws_declared=True, stochastic_budget_respected=True, independent_reproduction_claimed=False),
            [
                ("SEED", {"seed_pinned": False}),
                ("GENERATOR", {"generator_pinned": False}),
                ("RUNTIME", {"runtime_pinned": False}),
                ("STREAM", {"streams_partitioned": False}),
                ("DRAWS", {"draw_count_matches": False}),
                ("RETRY", {"retry_draws_declared": False}),
                ("BUDGET-INDEPENDENT", {"stochastic_budget_respected": False, "independent_reproduction_claimed": True}),
            ],
        ),
        _group(
            "V6427-P09",
            open_system_decision,
            "accept",
            dict(boundary_declared=True, system_kind_valid=True, stock_flow_compatible=True, state_rate_compatible=True, exchange_flux_declared=True, dimensions_valid=True, entropy_domain_preserved=True, law_or_consciousness_claimed=False),
            [
                ("BOUNDARY", {"boundary_declared": False}),
                ("KIND", {"system_kind_valid": False}),
                ("STOCK-FLOW", {"stock_flow_compatible": False}),
                ("STATE-RATE", {"state_rate_compatible": False}),
                ("FLUX", {"exchange_flux_declared": False}),
                ("DIMENSION", {"dimensions_valid": False}),
                ("ENTROPY-LAW", {"entropy_domain_preserved": False, "law_or_consciousness_claimed": True}),
            ],
        ),
        _group(
            "V6427-P10",
            stage20_abstention_decision,
            "open_gap",
            dict(technical_owner_sets_external_loss=False, abstains_when_prerequisite_missing=True, cross_pillar_compensation=False, veto_preserved=True, negative_count_preserved=True, reopening_requires_new_evidence=True, terminal_verdict="NOT_READY_FOR_STAGE_20", protected_claim_true=False),
            [
                ("LOSS", {"technical_owner_sets_external_loss": True}),
                ("NO-ABSTAIN", {"abstains_when_prerequisite_missing": False}),
                ("COMPENSATE", {"cross_pillar_compensation": True}),
                ("VETO", {"veto_preserved": False}),
                ("NEGATIVES", {"negative_count_preserved": False}),
                ("REOPEN", {"reopening_requires_new_evidence": False}),
                ("PROMOTE", {"terminal_verdict": "READY_FOR_STAGE_20", "protected_claim_true": True}),
            ],
        ),
    ]


def evaluate_group(group: dict[str, Any]) -> dict[str, Any]:
    decision: Decision = group["decision"]
    evaluated: list[dict[str, Any]] = []
    for original in group["cases"]:
        case = copy.deepcopy(original)
        expected = case.pop("expected")
        case_id = case.pop("case_id")
        observed, reasons = decision(case)
        evaluated.append(
            {
                "case_id": case_id,
                "expected": expected,
                "observed": observed,
                "matched": observed == expected,
                "retained_negative": expected == "reject",
                "reasons": reasons,
                "fixture": case,
            }
        )
    return {
        "proposal_id": group["proposal_id"],
        "case_count": len(evaluated),
        "matched_count": sum(1 for case in evaluated if case["matched"]),
        "retained_negative_count": sum(1 for case in evaluated if case["retained_negative"]),
        "cases": evaluated,
    }


def _boundary_text(proposal_id: str) -> str:
    return {
        "V6427-P01": "Citation identity control is local provenance evidence, not proof that a source claim is true or independent.",
        "V6427-P02": "Constraint-algebra fixtures are structural obligations, not proof of a healthy theory or empirical GMUT evidence.",
        "V6427-P03": "Observation-process fixtures are synthetic with zero real rows, likelihood results, fits, or independent statistical reviews.",
        "V6427-P04": "Protocol checks do not supply ethics approval, consent, real participants or raters, matched-budget real arms, superiority, or independent review.",
        "V6427-P05": "Synthetic schema checks do not supply real keys, proofs, live resolution or status, interoperability, privacy review, security review, or governance.",
        "V6427-P06": "No governing law, forum, Māori wording, or authority is selected; affected-party, Māori, cultural, data-governance, and legal authority remains external and exact-gated.",
        "V6427-P07": "Synthetic namespace vectors do not establish exhaustive host security, independent security review, or production assurance.",
        "V6427-P08": "Same-owner stochastic replay is repeatability evidence, not independent-team scientific reproduction.",
        "V6427-P09": "Open-system type checks preserve analogy boundaries and do not establish a thermo-psyche law, consciousness, sentience, or personhood.",
        "V6427-P10": "The abstention board has missing external loss ownership and qualifying evidence; Stage 20 readiness remains false.",
    }[proposal_id]


def _evidence_class(outcome: str) -> str:
    return {
        "completed": "bounded_local_execution",
        "represented": "synthetic_structural_representation",
        "open_gap": "structure_with_missing_external_evidence",
        "exact_gate": "documented_exact_authority_gate",
    }[outcome]


def _manifest_entries(phase: Path) -> list[dict[str, Any]]:
    excluded_names = {"closeout-receipt.json", "final-validation-record.json", "seal-receipt.json"}
    entries: list[dict[str, Any]] = []
    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path == phase / "reproduction/manifest.json":
            continue
        relative = path.relative_to(phase).as_posix()
        if relative.startswith("validation/") or path.name in excluded_names:
            continue
        entries.append(
            {
                "path": relative,
                "normalized_sha256": normalized_sha256(path),
                "bytes": normalized_size(path),
            }
        )
    return entries


def build(
    repo: Path,
    phase: Path,
    x1_commit: str,
    evidence_commit: str | None = None,
    snapshot_state: str = "pending",
) -> dict[str, Any]:
    proposal_packet = read_json(phase / "x1-proposals.json")
    proposals = proposal_packet["proposals"]
    proposal_by_id = {proposal["proposal_id"]: proposal for proposal in proposals}
    if set(proposal_by_id) != set(OBSERVED):
        raise ValueError("x1 proposal IDs do not match the v642-v7 frozen set")

    evaluated = {item["proposal_id"]: item for item in map(evaluate_group, case_groups())}
    if any(item["matched_count"] != item["case_count"] for item in evaluated.values()):
        raise ValueError("one or more preregistered evidence cases did not match")

    real_counts = {
        "gmut_real_rows": 0,
        "gmut_likelihoods": 0,
        "gmut_parameter_fits": 0,
        "thos_real_participants": 0,
        "thos_real_raters": 0,
        "thos_real_arms": 0,
        "freed_id_real_keys": 0,
        "freed_id_real_proofs": 0,
        "freed_id_live_resolvers": 0,
        "freed_id_live_status_services": 0,
        "interoperability_partners": 0,
        "independent_teams": 0,
        "manual_accessibility_reviews": 0,
        "affected_user_accessibility_reviews": 0,
    }
    claims = {claim: False for claim in PROTECTED_CLAIMS}

    ledger_rows: list[dict[str, Any]] = []
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        outcome = OBSERVED[proposal_id]
        vector_result = evaluated[proposal_id]
        deliverables = proposal["deliverables"]
        contract = {
            "schema": f"ghc.family.v642-v7.{proposal_id.lower()}.contract.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": proposal_id,
            "title": proposal["title"],
            "hypothesis": proposal["hypothesis"],
            "null_or_failure": proposal["null_or_failure"],
            "approval_class": proposal["approval_class"],
            "execution_lane": proposal["execution_lane"],
            "authoritative_source_needs": proposal["authoritative_source_needs"],
            "test_falsifier_or_gate": proposal["test_falsifier_or_gate"],
            "rollback_or_recovery": proposal["rollback_or_recovery"],
            "protected_gates": proposal["protected_gates"],
            "expected_disposition": proposal["expected_disposition"],
            "observed_disposition": outcome,
            "evidence_class": _evidence_class(outcome),
            "real_or_external_counts": real_counts,
            "protected_claims": claims,
            "boundary": _boundary_text(proposal_id),
        }
        vectors = {
            "schema": f"ghc.family.v642-v7.{proposal_id.lower()}.vectors.v1",
            "phase": PHASE,
            "owner": OWNER,
            **vector_result,
            "all_expected_results_matched": vector_result["matched_count"] == vector_result["case_count"],
            "boundary": _boundary_text(proposal_id),
        }
        boundary = {
            "schema": f"ghc.family.v642-v7.{proposal_id.lower()}.boundary.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": proposal_id,
            "expected_disposition": proposal["expected_disposition"],
            "observed_disposition": outcome,
            "case_count": vector_result["case_count"],
            "matched_count": vector_result["matched_count"],
            "retained_negative_count": vector_result["retained_negative_count"],
            "external_evidence_count": 0,
            "protected_claims": claims,
            "remaining_gates": proposal["protected_gates"],
            "boundary": _boundary_text(proposal_id),
        }
        if proposal_id == "V6427-P08":
            boundary.update(
                {
                    "snapshot_state": snapshot_state,
                    "x1_commit": x1_commit,
                    "evidence_commit": evidence_commit or "pending",
                    "same_owner": True,
                    "independent_team_reproduction": False,
                }
            )
        if proposal_id == "V6427-P10":
            boundary.update(
                {
                    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                    "stage20_ready": False,
                    "open_gap_count": 5,
                    "exact_gate_count": 6,
                    "engineering_pass_cannot_compensate": True,
                    "abstention_required": True,
                }
            )
        write_json(phase / deliverables[0], contract)
        write_json(phase / deliverables[1], vectors)
        write_json(phase / deliverables[2], boundary)
        ledger_rows.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": outcome,
                "expectation_matched": proposal["expected_disposition"] == outcome,
                "evidence_class": _evidence_class(outcome),
                "case_count": vector_result["case_count"],
                "matched_count": vector_result["matched_count"],
                "retained_negative_count": vector_result["retained_negative_count"],
                "artifacts": deliverables,
                "protected_gates": proposal["protected_gates"],
                "boundary": _boundary_text(proposal_id),
            }
        )

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(
        phase / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v642-v7.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": x1_commit,
            "proposal_count": 10,
            "observed_distribution": distribution,
            "all_expected_dispositions_matched": all(row["expectation_matched"] for row in ledger_rows),
            "total_case_count": sum(row["case_count"] for row in ledger_rows),
            "total_matched_count": sum(row["matched_count"] for row in ledger_rows),
            "rows": ledger_rows,
            "boundary": "Observed outcomes describe bounded v642-v7 artifacts only and do not promote any protected external claim.",
        },
    )
    write_json(
        phase / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v642-v7.evidence-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "evidence_commit": evidence_commit or "pending",
            "snapshot_state": snapshot_state,
            "proposal_rows": ledger_rows,
            "real_or_external_counts": real_counts,
            "protected_claims": claims,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    inherited_path = repo / "docs/orin-thale/v642-v6/retained-negative-register.json"
    appendix_path = repo / "docs/orin-thale/v642-v6/validation/post-seal-negative-appendix.json"
    inherited = read_json(inherited_path)
    appendix = read_json(appendix_path)
    if inherited["negative_count"] != 231 or len(inherited["negatives"]) != 231:
        raise ValueError("inherited v642-v6 register is not the sealed 231-record packet")
    if appendix["effective_retained_negative_count"] != 233 or len(appendix["negatives"]) != 2:
        raise ValueError("v642-v6 post-seal appendix is not the two-record extension")
    inherited_negatives = inherited["negatives"] + appendix["negatives"]

    audit = read_json(phase / "provenance/prior-proposal-collision-audit.json")
    x1_negatives = [
        {
            "negative_id": item["negative_id"],
            "origin": "v642-v7_x1_execution",
            "statement": item["observed"],
            "evidence": "provenance/prior-proposal-collision-audit.json",
            "recovery": item["recovery"],
            "retained": True,
        }
        for item in audit["x1_execution_negatives"]
    ]
    synthetic_negatives: list[dict[str, Any]] = []
    synthetic_index = 1
    for row in ledger_rows:
        vector_path = row["artifacts"][1]
        for case in evaluated[row["proposal_id"]]["cases"]:
            if not case["retained_negative"]:
                continue
            synthetic_negatives.append(
                {
                    "negative_id": f"V6427-N{synthetic_index:02d}",
                    "origin": "v642-v7_preregistered_vector",
                    "statement": f"{case['case_id']} retained expected rejection: {', '.join(case['reasons'])}",
                    "evidence": vector_path,
                    "recovery": proposal_by_id[row["proposal_id"]]["rollback_or_recovery"],
                    "retained": True,
                }
            )
            synthetic_index += 1
    execution_log = read_json(phase / "validation/execution-negative-log.json")
    operational = execution_log.get("negatives", [])
    negatives = inherited_negatives + x1_negatives + synthetic_negatives + operational
    write_json(
        phase / "retained-negative-register.json",
        {
            "schema": "ghc.family.v642-v7.retained-negative-register.v1",
            "inherited_from": [
                "docs/orin-thale/v642-v6/retained-negative-register.json",
                "docs/orin-thale/v642-v6/validation/post-seal-negative-appendix.json",
            ],
            "inherited_sha256": {
                "sealed_packet": normalized_sha256(inherited_path),
                "post_seal_appendix": normalized_sha256(appendix_path),
            },
            "inherited_count": 233,
            "x1_operational_count": len(x1_negatives),
            "new_synthetic_count": len(synthetic_negatives),
            "transition_and_x2_operational_count": len(operational),
            "new_count": len(x1_negatives) + len(synthetic_negatives) + len(operational),
            "negative_count": len(negatives),
            "all_retained": all(item.get("retained") is True for item in negatives),
            "erasure_permitted": False,
            "negatives": negatives,
        },
    )

    open_gaps = [
        {"gate_id": "V6427-OG01", "surface": "GMUT empirical evidence", "needs": ["real measurements", "preregistered likelihood", "parameter fit", "independent scientific review"]},
        {"gate_id": "V6427-OG02", "surface": "THOS real evaluation", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants and raters", "independent review"]},
        {"gate_id": "V6427-OG03", "surface": "Freed ID production and privacy", "needs": ["real keys and proofs", "live resolution and status", "interoperability", "privacy assurance", "independent security review", "trust governance"]},
        {"gate_id": "V6427-OG04", "surface": "independent reproduction and Stage 20 loss ownership", "needs": ["independently owned protocol", "independent team", "returned results", "competent claim-specific loss ownership"]},
        {"gate_id": "V6427-OG05", "surface": "accessibility evaluation", "needs": ["manual accessibility evaluation", "affected-user evaluation"]},
    ]
    exact_gates = [
        {"gate_id": "V6427-EG01", "surface": "CBR affected-party legitimacy", "reserved_to": ["authorized affected parties", "authorized representatives"]},
        {"gate_id": "V6427-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6427-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6427-EG04", "surface": "jurisdiction, forum competence, legal interpretation, and enacted law", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6427-EG05", "surface": "production, deployment, privacy publication, account, API-key, purchase, destructive action", "reserved_to": ["fresh exact user and competent operational authority"]},
        {"gate_id": "V6427-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience or personhood, sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    write_json(
        phase / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v642-v7.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "open_gap_count": len(open_gaps),
            "exact_gate_count": len(exact_gates),
            "open_gaps": open_gaps,
            "exact_gates": exact_gates,
            "all_visible": True,
            "boundary": "Local engineering work cannot close empirical, human-subject, production, privacy, legal, cultural, Māori-authority, accessibility, proof/canon, destructive, account, API-key, identity, or sibling-merge gates.",
        },
    )

    threat_rows = [
        ("citation_anchor_drift", "redirects or aliases falsify source identity or independence", "version pins, authority-root checks, alias deduplication"),
        ("constraint_miscount", "GMUT structural health is overstated", "closure, class-count, phase-space, dimension, and empirical locks"),
        ("observation_process_conflation", "censoring or truncation changes likelihood meaning", "typed observation process, units, and zero-row lock"),
        ("post_outcome_estimand_switch", "THOS deviation handling favors an arm", "blind preregistered strategies and matched budgets"),
        ("semantic_schema_downgrade", "credential meaning changes under an older schema", "pinned context, protected terms, critical-field rejection"),
        ("legal_authority_substitution", "technical artifacts choose law or forum", "exact jurisdiction and authority deferral"),
        ("windows_namespace_escape", "an alias or reparse path escapes the owned root", "pure structural tribunal and resource ceilings"),
        ("hidden_stochastic_state", "same-owner parity depends on undeclared generator state", "seed, generator, version, stream, and draw-budget pins"),
        ("thermo_category_error", "stock, flow, state, rate, or entropy domains are mixed", "typed system boundary and category checks"),
        ("stage20_loss_laundering", "local owners invent loss weights and promote readiness", "mandatory abstention, veto preservation, qualified reopening"),
        ("private_material_leak", "identifiers, routes, paths, or credentials enter artifacts", "family privacy scan and exact staged review"),
        ("negative_erasure", "a later pass deletes earlier failures", "append-only retained-negative register"),
        ("resource_exhaustion", "path or artifact processing exceeds bounded ceilings", "owned-file, case-count, depth, and byte limits"),
        ("common_mode_reproduction", "same-owner replay is mislabeled independent", "owner declaration and independent-team open gap"),
    ]
    write_json(
        phase / "threat-model.json",
        {
            "schema": "ghc.family.v642-v7.threat-model.v1",
            "phase": PHASE,
            "owner": OWNER,
            "assets": ["frozen proposal intent", "source identity", "negative evidence", "authority boundaries", "privacy boundary", "terminal verdict"],
            "trust_boundaries": ["repository versus external reality", "synthetic versus real data", "technical artifact versus competent authority", "same-owner versus independent team", "private runtime versus public artifact"],
            "resource_ceilings": {"owned_generated_files": 15000, "proposals": 10, "cases_per_proposal": 8, "total_cases": 80, "redirect_depth": 2},
            "threat_count": len(threat_rows),
            "threats": [
                {"threat_id": f"V6427-T{index:02d}", "class": klass, "failure": failure, "control": control, "residual_risk": "open_or_exact_gate_remains"}
                for index, (klass, failure, control) in enumerate(threat_rows, start=1)
            ],
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This is a bounded threat model and does not establish exhaustive security or production assurance.",
        },
    )

    write_json(
        phase / "phase-truth.json",
        {
            "schema": "ghc.family.v642-v7.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "active_phase": "v642-gmut-thos-v7-x2-evidence-candidate",
            "latest_closed_phase": "v642-gmut-thos-v6-x1-x2",
            "latest_completed_x1": {"phase": "v642-gmut-thos-v7-x1", "commit": x1_commit, "remote_equal": True},
            "latest_completed_x2": "evidence_candidate_not_closeout",
            "active_lanes": ["Tamar Vey owned branch"],
            "standby_lanes": "all other siblings and tasks",
            "route_state": "ACTIVE_SOLO_OWNER",
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "open_gap_count": len(open_gaps),
            "exact_gate_count": len(exact_gates),
            "retained_negative_count": len(negatives),
            "protected_claims": claims,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    repository_receipt_path = phase / "validation/repository-test-receipt.json"
    full_receipt_path = phase / "validation/candidate-validation-summary.json"
    minimal_receipt_path = phase / "validation/minimal-validation-summary.json"
    detached_receipt_path = phase / "reproduction/detached-evidence-validation.json"
    repository_valid = repository_receipt_path.exists() and read_json(repository_receipt_path).get("valid") is True
    validators_valid = (
        full_receipt_path.exists()
        and minimal_receipt_path.exists()
        and read_json(full_receipt_path).get("valid") is True
        and read_json(minimal_receipt_path).get("valid") is True
    )
    detached_valid = detached_receipt_path.exists() and read_json(detached_receipt_path).get("valid") is True and snapshot_state == "verified"
    report_path = phase / "deliverables/v642-v7-constraint-evidence-report.html"
    write_json(
        phase / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v642-v7.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "owner": OWNER,
            "state": "evidence_validated_closeout_pending" if repository_valid and validators_valid and detached_valid else "evidence_candidate_incomplete_for_closeout",
            "required_rows": [
                {"item": "x1 remote-equal freeze", "complete": True},
                {"item": "ten x2 proposals executed to bounded outcome", "complete": True},
                {"item": "all inherited and new negatives retained", "complete": True},
                {"item": "open and exact gates visible", "complete": True},
                {"item": "accessible static report built", "complete": report_path.exists()},
                {"item": "complete repository suite passes", "complete": repository_valid},
                {"item": "full and minimal validators pass", "complete": validators_valid},
                {"item": "fresh detached evidence snapshots validate", "complete": detached_valid},
                {"item": "closeout, seal, and final detached validation", "complete": False},
                {"item": "final remote equality", "complete": False},
            ],
            "required_complete": False,
            "open_gaps_are_valid_outcomes": True,
            "exact_gates_are_valid_outcomes": True,
            "boundary": "Do not close on elapsed time, watcher state, prepared text, or local candidate checks.",
        },
    )

    tool_paths = [
        "scripts/ghc_family_constraint_evidence.py",
        "scripts/ghc_family_constraint_evidence_validator.py",
        "scripts/ghc_family_constraint_evidence_minimal.py",
        "scripts/build_ghc_family_constraint_evidence_report.py",
        "tests/test_ghc_family_v642_v7.py",
    ]
    tool_rows = []
    for relative in tool_paths:
        path = repo / relative
        if path.exists():
            tool_rows.append({"path": relative, "normalized_sha256": normalized_sha256(path)})
    write_json(
        phase / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v642-v7.executed-toolchain.v1",
            "phase": PHASE,
            "owner": OWNER,
            "family_current_tools": tool_rows,
            "standard_library_only": True,
            "caller_compatibility_preserved": True,
            "inherited_tools_modified": False,
            "shared_skill_change": "reviewed_current_no_change_justified",
        },
    )

    entries = _manifest_entries(phase)
    write_json(
        phase / "reproduction/manifest.json",
        {
            "schema": "ghc.family.v642-v7.manifest.v1",
            "phase": PHASE,
            "owner": OWNER,
            "hash_policy": "sha256_after_crlf_to_lf_normalization",
            "byte_policy": "length_after_crlf_to_lf_normalization",
            "entry_count": len(entries),
            "entries": entries,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
        },
    )
    return {
        "phase": PHASE,
        "proposal_count": 10,
        "case_count": 80,
        "matched_count": 80,
        "observed_distribution": distribution,
        "negative_count": len(negatives),
        "manifest_entries": len(entries),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--phase-dir", required=True)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--evidence-commit")
    parser.add_argument("--snapshot-state", choices=["pending", "verified"], default="pending")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    phase = (repo / args.phase_dir).resolve() if not Path(args.phase_dir).is_absolute() else Path(args.phase_dir).resolve()
    print(json.dumps(build(repo, phase, args.x1_commit, args.evidence_commit, args.snapshot_state), ensure_ascii=False))


if __name__ == "__main__":
    main()
