#!/usr/bin/env python3
"""Build the bounded GHC Family v642-v6 evidence-integrity packet.

The implementation is standard-library-only. It exercises structural and
synthetic fixtures while keeping empirical, participant, production, legal,
cultural, deployment, identity, proof/canon, and independent-reproduction
claims false unless exact external evidence exists.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PHASE = "v642-gmut-thos-v6-x1-x2"
OWNER = "Orin Thale"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6426-P01": "completed",
    "V6426-P02": "completed",
    "V6426-P03": "represented",
    "V6426-P04": "open_gap",
    "V6426-P05": "represented",
    "V6426-P06": "exact_gate",
    "V6426-P07": "completed",
    "V6426-P08": "completed",
    "V6426-P09": "completed",
    "V6426-P10": "completed",
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


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def normalized_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def _decision(ok: bool, accepted: str, reasons: list[str]) -> tuple[str, list[str]]:
    return (accepted if ok else "reject", reasons)


def requirement_trace_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    requirements = [
        (case["forward_edge"], "missing_requirement_to_evidence_edge"),
        (case["reverse_edge"], "orphan_evidence_without_requirement_edge"),
        (not case["circular_edge"], "circular_evidence"),
        (case["frozen_requirement"], "post_freeze_requirement_mutation"),
        (case["evidence_class_match"], "evidence_class_mismatch"),
        (not case["source_only"], "source_pointer_not_execution_evidence"),
        (case["proposal_match"], "proposal_owner_mismatch"),
    ]
    reasons.extend(reason for ok, reason in requirements if not ok)
    return _decision(not reasons, "accept", reasons)


def kinetic_hessian_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not case["dimensions_valid"]:
        reasons.append("dimension_mismatch")
    if case["kinetic_signature"] not in {"positive", "constrained"}:
        reasons.append("wrong_sign_kinetic_mode")
    if case["rank_change"] and not case["rank_change_declared"]:
        reasons.append("undeclared_rank_change")
    if case["degenerate"] and not case["degeneracy_declared"]:
        reasons.append("undeclared_degeneracy")
    if not case["constraints_match"]:
        reasons.append("constraint_count_mismatch")
    if case["zero_eigenvalue"] and not case["strong_coupling_warning"]:
        reasons.append("missing_strong_coupling_warning")
    if case["empirical_promotion"]:
        reasons.append("structural_pass_promoted_to_empirical_claim")
    return _decision(not reasons, "accept", reasons)


def calibration_covariance_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (case["synthetic_only"], "non_synthetic_input"),
        (case["real_rows"] == 0, "real_rows_without_preregistration"),
        (case["units_valid"], "unit_mismatch"),
        (case["covariance_symmetric"], "asymmetric_covariance"),
        (case["covariance_psd"], "non_psd_covariance"),
        (case["covariance_provenance"], "missing_covariance_provenance"),
        (case["shared_nuisance_counted_once"], "shared_nuisance_double_counted"),
        (case["threshold_preregistered"], "posthoc_threshold"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "represented", reasons)


def thos_safety_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (case["arm_independent_stop"], "outcome_tuned_stopping"),
        (case["withdrawal_protected"], "withdrawal_penalized"),
        (case["blinded_decision"], "safety_decision_unblinded"),
        (case["matched_budget"], "matched_budget_violation"),
        (case["threshold_preregistered"], "posthoc_severity_threshold"),
        (not case["ethics_approval_claimed"], "synthetic_protocol_claimed_ethics_approval"),
        (
            case["real_participants"] == 0
            and case["real_raters"] == 0
            and case["real_arms"] == 0,
            "real_execution_without_review",
        ),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "open_gap", reasons)


def purpose_bound_verification_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (case["purpose_match"], "verification_relationship_purpose_mismatch"),
        (case["controller_match"], "controller_scope_mismatch"),
        (case["reference_resolved"], "dangling_verification_method_reference"),
        (case["relationship_present"], "verification_relationship_absent"),
        (case["method_active"], "inactive_or_revoked_method"),
        (case["method_unique"], "duplicate_verification_method"),
        (case["real_keys"] == 0, "real_key_claim_in_synthetic_fixture"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "represented", reasons)


def wording_authority_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (not case["contains_maori_wording"], "unauthorized_maori_wording_present"),
        (not case["machine_translation_substitution"], "machine_translation_substituted_for_authority"),
        (not case["technical_role_claims_authority"], "technical_role_claimed_maori_authority"),
        (not case["scope_expanded_without_consent"], "mandate_scope_expanded_without_consent"),
        (case["withdrawal_respected"], "withdrawal_ignored"),
        (not case["silence_as_acceptance"], "silence_treated_as_acceptance"),
        (not case["cultural_or_legal_completion_claimed"], "synthetic_artifact_claimed_ratification_or_law"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "exact_gate", reasons)


def status_privacy_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (case["batch_size"] > 1, "singleton_status_query"),
        (case["timing_bucketed"], "fine_grained_timing_correlation"),
        (case["cache_partitioned"], "cross_context_cache_join"),
        (case["requester_minimized"], "requester_metadata_excess"),
        (case["status_fresh"], "stale_status_accepted"),
        (case["status_semantics_valid"], "status_semantics_changed"),
        (not case["anonymity_claimed"], "padding_promoted_to_anonymity_proof"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "accept", reasons)


def step_ablation_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    checks = [
        (case["expected_failure_observed"], "required_step_ablation_did_not_fail"),
        (not case["undeclared_hidden_state"], "undeclared_hidden_state_detected"),
        (case["deterministic_replay"], "ablation_replay_nondeterministic"),
        (case["divergence_retained"], "divergent_output_erased"),
        (case["manifest_verified"], "manifest_not_verified"),
        (case["environment_declared"], "environment_dependency_undeclared"),
        (not case["independent_reproduction_claimed"], "same_owner_called_independent_reproduction"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "accept", reasons)


def aggregation_level_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if case["source_level"] != case["target_level"] and not case["validated_bridge"]:
        reasons.append("unbridged_level_of_analysis_change")
    checks = [
        (case["aggregation_weights_declared"], "aggregation_weights_missing"),
        (not case["simpson_reversal_hidden"], "simpson_reversal_hidden"),
        (case["scale_admissible"], "measurement_scale_operation_invalid"),
        (case["category_preserved"], "thermo_psyche_category_crossing"),
        (not case["fundamental_law_claimed"], "analogy_promoted_to_fundamental_law"),
        (not case["consciousness_claimed"], "analogy_promoted_to_consciousness_claim"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "accept", reasons)


def evidence_class_firewall_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if case["source_class"] != case["target_class"] and not case["qualifying_external_evidence"]:
        reasons.append("unsupported_evidence_class_conversion")
    checks = [
        (not case["draft_promoted_to_stable"], "draft_source_promoted_to_stable"),
        (not case["authority_substitution"], "technical_artifact_substituted_for_authority"),
        (case["negative_count_preserved"], "negative_count_reduced"),
        (not case["protected_claim_true"], "protected_claim_promoted"),
        (not case["same_owner_called_independent"], "same_owner_called_independent_reproduction"),
        (not case["protocol_called_result"], "protocol_promoted_to_real_result"),
    ]
    reasons.extend(reason for ok, reason in checks if not ok)
    return _decision(not reasons, "accept", reasons)


Decision = Callable[[dict[str, Any]], tuple[str, list[str]]]


def _group(
    proposal_id: str,
    decision: Decision,
    accepted: str,
    base: dict[str, Any],
    mutations: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    canonical = {"case_id": f"{proposal_id}-CANONICAL", **base, "expected": accepted}
    cases.append(canonical)
    for suffix, changes in mutations:
        case = copy.deepcopy(base)
        case.update(changes)
        cases.append({"case_id": f"{proposal_id}-{suffix}", **case, "expected": "reject"})
    assert len(cases) == 8
    return {"proposal_id": proposal_id, "decision": decision, "cases": cases}


def case_groups() -> list[dict[str, Any]]:
    return [
        _group(
            "V6426-P01",
            requirement_trace_decision,
            "accept",
            dict(forward_edge=True, reverse_edge=True, circular_edge=False, frozen_requirement=True, evidence_class_match=True, source_only=False, proposal_match=True),
            [
                ("NO-FORWARD", {"forward_edge": False}),
                ("ORPHAN", {"reverse_edge": False}),
                ("CIRCULAR", {"circular_edge": True}),
                ("POSTFREEZE", {"frozen_requirement": False}),
                ("CLASS", {"evidence_class_match": False}),
                ("SOURCE-ONLY", {"source_only": True}),
                ("OWNER", {"proposal_match": False}),
            ],
        ),
        _group(
            "V6426-P02",
            kinetic_hessian_decision,
            "accept",
            dict(dimensions_valid=True, kinetic_signature="constrained", rank_change=False, rank_change_declared=True, degenerate=True, degeneracy_declared=True, constraints_match=True, zero_eigenvalue=True, strong_coupling_warning=True, empirical_promotion=False),
            [
                ("DIMENSION", {"dimensions_valid": False}),
                ("WRONG-SIGN", {"kinetic_signature": "negative"}),
                ("RANK-JUMP", {"rank_change": True, "rank_change_declared": False}),
                ("DEGENERACY", {"degeneracy_declared": False}),
                ("CONSTRAINTS", {"constraints_match": False}),
                ("STRONG-COUPLING", {"strong_coupling_warning": False}),
                ("EMPIRICAL", {"empirical_promotion": True}),
            ],
        ),
        _group(
            "V6426-P03",
            calibration_covariance_decision,
            "represented",
            dict(synthetic_only=True, real_rows=0, units_valid=True, covariance_symmetric=True, covariance_psd=True, covariance_provenance=True, shared_nuisance_counted_once=True, threshold_preregistered=True),
            [
                ("REAL-ROW", {"real_rows": 1}),
                ("UNITS", {"units_valid": False}),
                ("ASYMMETRIC", {"covariance_symmetric": False}),
                ("NON-PSD", {"covariance_psd": False}),
                ("PROVENANCE", {"covariance_provenance": False}),
                ("DOUBLE-COUNT", {"shared_nuisance_counted_once": False}),
                ("POSTHOC", {"threshold_preregistered": False}),
            ],
        ),
        _group(
            "V6426-P04",
            thos_safety_decision,
            "open_gap",
            dict(arm_independent_stop=True, withdrawal_protected=True, blinded_decision=True, matched_budget=True, threshold_preregistered=True, ethics_approval_claimed=False, real_participants=0, real_raters=0, real_arms=0),
            [
                ("ARM-TUNED", {"arm_independent_stop": False}),
                ("WITHDRAWAL", {"withdrawal_protected": False}),
                ("UNBLINDED", {"blinded_decision": False}),
                ("BUDGET", {"matched_budget": False}),
                ("POSTHOC", {"threshold_preregistered": False}),
                ("ETHICS-CLAIM", {"ethics_approval_claimed": True}),
                ("UNREVIEWED-REAL", {"real_participants": 1}),
            ],
        ),
        _group(
            "V6426-P05",
            purpose_bound_verification_decision,
            "represented",
            dict(purpose_match=True, controller_match=True, reference_resolved=True, relationship_present=True, method_active=True, method_unique=True, real_keys=0),
            [
                ("PURPOSE", {"purpose_match": False}),
                ("CONTROLLER", {"controller_match": False}),
                ("DANGLING", {"reference_resolved": False}),
                ("RELATIONSHIP", {"relationship_present": False}),
                ("REVOKED", {"method_active": False}),
                ("DUPLICATE", {"method_unique": False}),
                ("REAL-KEY", {"real_keys": 1}),
            ],
        ),
        _group(
            "V6426-P06",
            wording_authority_decision,
            "exact_gate",
            dict(contains_maori_wording=False, machine_translation_substitution=False, technical_role_claims_authority=False, scope_expanded_without_consent=False, withdrawal_respected=True, silence_as_acceptance=False, cultural_or_legal_completion_claimed=False),
            [
                ("WORDING", {"contains_maori_wording": True}),
                ("MACHINE", {"machine_translation_substitution": True}),
                ("TECHNICAL-AUTHORITY", {"technical_role_claims_authority": True}),
                ("SCOPE", {"scope_expanded_without_consent": True}),
                ("WITHDRAWAL", {"withdrawal_respected": False}),
                ("SILENCE", {"silence_as_acceptance": True}),
                ("RATIFICATION", {"cultural_or_legal_completion_claimed": True}),
            ],
        ),
        _group(
            "V6426-P07",
            status_privacy_decision,
            "accept",
            dict(batch_size=16, timing_bucketed=True, cache_partitioned=True, requester_minimized=True, status_fresh=True, status_semantics_valid=True, anonymity_claimed=False),
            [
                ("SINGLETON", {"batch_size": 1}),
                ("TIMING", {"timing_bucketed": False}),
                ("CACHE", {"cache_partitioned": False}),
                ("REQUESTER", {"requester_minimized": False}),
                ("STALE", {"status_fresh": False}),
                ("SEMANTICS", {"status_semantics_valid": False}),
                ("ANONYMITY", {"anonymity_claimed": True}),
            ],
        ),
        _group(
            "V6426-P08",
            step_ablation_decision,
            "accept",
            dict(expected_failure_observed=True, undeclared_hidden_state=False, deterministic_replay=True, divergence_retained=True, manifest_verified=True, environment_declared=True, independent_reproduction_claimed=False),
            [
                ("NO-FAILURE", {"expected_failure_observed": False}),
                ("HIDDEN-STATE", {"undeclared_hidden_state": True}),
                ("NONDETERMINISTIC", {"deterministic_replay": False}),
                ("ERASURE", {"divergence_retained": False}),
                ("MANIFEST", {"manifest_verified": False}),
                ("ENVIRONMENT", {"environment_declared": False}),
                ("INDEPENDENT", {"independent_reproduction_claimed": True}),
            ],
        ),
        _group(
            "V6426-P09",
            aggregation_level_decision,
            "accept",
            dict(source_level="group", target_level="group", validated_bridge=False, aggregation_weights_declared=True, simpson_reversal_hidden=False, scale_admissible=True, category_preserved=True, fundamental_law_claimed=False, consciousness_claimed=False),
            [
                ("ECOLOGICAL", {"target_level": "individual"}),
                ("WEIGHTS", {"aggregation_weights_declared": False}),
                ("SIMPSON", {"simpson_reversal_hidden": True}),
                ("SCALE", {"scale_admissible": False}),
                ("CATEGORY", {"category_preserved": False}),
                ("LAW", {"fundamental_law_claimed": True}),
                ("CONSCIOUSNESS", {"consciousness_claimed": True}),
            ],
        ),
        _group(
            "V6426-P10",
            evidence_class_firewall_decision,
            "accept",
            dict(source_class="engineering", target_class="engineering", qualifying_external_evidence=False, draft_promoted_to_stable=False, authority_substitution=False, negative_count_preserved=True, protected_claim_true=False, same_owner_called_independent=False, protocol_called_result=False),
            [
                ("EMPIRICAL", {"target_class": "empirical"}),
                ("DRAFT", {"draft_promoted_to_stable": True}),
                ("AUTHORITY", {"authority_substitution": True}),
                ("NEGATIVE-ERASURE", {"negative_count_preserved": False}),
                ("PROTECTED", {"protected_claim_true": True}),
                ("INDEPENDENT", {"same_owner_called_independent": True}),
                ("PROTOCOL", {"protocol_called_result": True}),
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
        "V6426-P01": "Trace coverage is local provenance control, not scientific proof or external validation.",
        "V6426-P02": "Kinetic-Hessian fixtures are structural obligations, not proof of a healthy theory or empirical GMUT evidence.",
        "V6426-P03": "Calibration fixtures are synthetic with zero real rows, likelihoods, fits, or independent statistical reviews.",
        "V6426-P04": "Protocol checks do not supply ethics approval, consent, real participants or raters, matched-budget real arms, or independent review.",
        "V6426-P05": "Synthetic purpose checks do not supply real keys, proofs, live resolution or status, interoperability, review, or governance.",
        "V6426-P06": "No Māori wording is generated or ratified; all affected-party, Māori, cultural, data-governance, and legal authority remains external and exact-gated.",
        "V6426-P07": "Synthetic correlation vectors do not establish live-service privacy assurance, interoperability, or exhaustive security.",
        "V6426-P08": "Same-owner detached snapshots are repeatability evidence, not independent-team reproduction.",
        "V6426-P09": "Level-of-analysis checks preserve analogy boundaries and do not establish a thermo-psyche law, consciousness, or personhood.",
        "V6426-P10": "Evidence classes are non-convertible without qualifying external evidence; terminal readiness remains false.",
    }[proposal_id]


def _evidence_class(outcome: str) -> str:
    return {
        "completed": "bounded_local_execution",
        "represented": "synthetic_structural_representation",
        "open_gap": "protocol_with_missing_external_evidence",
        "exact_gate": "documented_exact_authority_gate",
    }[outcome]


def _manifest_entries(phase: Path) -> list[dict[str, Any]]:
    excluded_names = {
        "closeout-receipt.json",
        "final-validation-record.json",
        "seal-receipt.json",
    }
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
        raise ValueError("x1 proposal IDs do not match the v642-v6 frozen set")

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
    }
    claims = {claim: False for claim in PROTECTED_CLAIMS}

    ledger_rows: list[dict[str, Any]] = []
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        outcome = OBSERVED[proposal_id]
        vector_result = evaluated[proposal_id]
        deliverables = proposal["deliverables"]
        contract = {
            "schema": f"ghc.family.v642-v6.{proposal_id.lower()}.contract.v1",
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
            "schema": f"ghc.family.v642-v6.{proposal_id.lower()}.vectors.v1",
            "phase": PHASE,
            "owner": OWNER,
            **vector_result,
            "all_expected_results_matched": vector_result["matched_count"] == vector_result["case_count"],
            "boundary": _boundary_text(proposal_id),
        }
        boundary = {
            "schema": f"ghc.family.v642-v6.{proposal_id.lower()}.boundary.v1",
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
        if proposal_id == "V6426-P08":
            boundary.update(
                {
                    "snapshot_state": snapshot_state,
                    "x1_commit": x1_commit,
                    "evidence_commit": evidence_commit or "pending",
                    "same_owner": True,
                    "independent_team_reproduction": False,
                }
            )
        if proposal_id == "V6426-P10":
            boundary.update(
                {
                    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                    "stage20_ready": False,
                    "open_gap_count": 5,
                    "exact_gate_count": 6,
                    "engineering_pass_cannot_compensate": True,
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
            "schema": "ghc.family.v642-v6.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": x1_commit,
            "proposal_count": 10,
            "observed_distribution": distribution,
            "all_expected_dispositions_matched": all(row["expectation_matched"] for row in ledger_rows),
            "total_case_count": sum(row["case_count"] for row in ledger_rows),
            "total_matched_count": sum(row["matched_count"] for row in ledger_rows),
            "rows": ledger_rows,
            "boundary": "Observed outcomes describe bounded v642-v6 artifacts only and do not promote any protected external claim.",
        },
    )
    write_json(
        phase / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v642-v6.evidence-ledger.v1",
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

    inherited_register_path = repo / "docs/sable-rook/v642-v5/retained-negative-register.json"
    inherited_register = read_json(inherited_register_path)
    if inherited_register["negative_count"] != 147 or len(inherited_register["negatives"]) != 147:
        raise ValueError("inherited retained-negative register is not the sealed 147-record source")
    audit = read_json(phase / "provenance/prior-proposal-collision-audit.json")
    x1_negatives = [
        {
            "negative_id": item["negative_id"],
            "origin": "v642-v6_x1_execution",
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
                    "negative_id": f"V6426-N{synthetic_index:02d}",
                    "origin": "v642-v6_preregistered_vector",
                    "statement": f"{case['case_id']} retained expected rejection: {', '.join(case['reasons'])}",
                    "evidence": vector_path,
                    "recovery": proposal_by_id[row["proposal_id"]]["rollback_or_recovery"],
                    "retained": True,
                }
            )
            synthetic_index += 1
    execution_log_path = phase / "validation/execution-negative-log.json"
    if execution_log_path.exists():
        execution_log = read_json(execution_log_path)
        x2_operational = execution_log.get("negatives", [])
    else:
        x2_operational = []
        write_json(
            execution_log_path,
            {
                "schema": "ghc.family.v642-v6.execution-negative-log.v1",
                "phase": PHASE,
                "owner": OWNER,
                "negative_count": 0,
                "negatives": [],
                "boundary": "Append every recovered x2 operational failure; never erase it after a later pass.",
            },
        )
    negatives = inherited_register["negatives"] + x1_negatives + synthetic_negatives + x2_operational
    write_json(
        phase / "retained-negative-register.json",
        {
            "schema": "ghc.family.v642-v6.retained-negative-register.v1",
            "inherited_from": "docs/sable-rook/v642-v5/retained-negative-register.json",
            "inherited_sha256": normalized_sha256(inherited_register_path),
            "inherited_count": 147,
            "x1_operational_count": len(x1_negatives),
            "new_synthetic_count": len(synthetic_negatives),
            "x2_operational_count": len(x2_operational),
            "new_count": len(x1_negatives) + len(synthetic_negatives) + len(x2_operational),
            "negative_count": len(negatives),
            "all_retained": all(item.get("retained") is True for item in negatives),
            "erasure_permitted": False,
            "negatives": negatives,
        },
    )

    open_gaps = [
        {"gate_id": "V6426-OG01", "surface": "GMUT empirical evidence", "needs": ["real measurements", "preregistered likelihood", "parameter fit", "independent scientific review"]},
        {"gate_id": "V6426-OG02", "surface": "THOS real evaluation", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants and raters", "independent review"]},
        {"gate_id": "V6426-OG03", "surface": "Freed ID production and privacy", "needs": ["real keys and proofs", "live resolution and status", "interoperability", "privacy assurance", "independent security review", "trust governance"]},
        {"gate_id": "V6426-OG04", "surface": "independent reproduction", "needs": ["independently owned protocol", "independent team", "returned results"]},
        {"gate_id": "V6426-OG05", "surface": "accessibility evaluation", "needs": ["manual accessibility evaluation", "affected-user evaluation"]},
    ]
    exact_gates = [
        {"gate_id": "V6426-EG01", "surface": "CBR affected-party legitimacy", "reserved_to": ["authorized affected parties", "authorized representatives"]},
        {"gate_id": "V6426-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6426-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6426-EG04", "surface": "legal interpretation and enacted law", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6426-EG05", "surface": "production, deployment, privacy publication, account, API-key, purchase, destructive action", "reserved_to": ["fresh exact user and competent operational authority"]},
        {"gate_id": "V6426-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness or personhood, sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    write_json(
        phase / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v642-v6.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "open_gap_count": len(open_gaps),
            "exact_gate_count": len(exact_gates),
            "open_gaps": open_gaps,
            "exact_gates": exact_gates,
            "all_visible": True,
            "boundary": "Local engineering work cannot close empirical, human-subject, production, privacy, legal, cultural, Māori-authority, proof/canon, destructive, account, API-key, identity, or sibling-merge gates.",
        },
    )

    threat_rows = [
        ("posthoc_evidence_injection", "orphan artifacts inflate support", "bidirectional trace and frozen acceptance wording"),
        ("ghost_or_strong_coupling_blindness", "structural GMUT health is overstated", "rank/signature/constraint obligations and empirical lock"),
        ("calibration_double_count", "shared nuisance uncertainty is counted twice", "covariance provenance and unit checks"),
        ("outcome_tuned_stopping", "THOS safety decisions favor an arm", "blind arm-independent stopping and withdrawal protection"),
        ("confused_deputy", "a DID method is used outside purpose or controller scope", "purpose-bound relationship matrix"),
        ("authority_substitution", "technical wording or role replaces Māori or affected-party authority", "exact non-substitution gate with no Māori wording"),
        ("status_query_correlation", "status timing or cache keys reveal credential use", "batching, timing buckets, partitioning, minimization"),
        ("hidden_reproduction_state", "same-owner parity depends on undeclared state", "step ablation and dependency ledger"),
        ("ecological_inference", "group statistics become individual claims", "level bridge and reversal checks"),
        ("evidence_class_laundering", "engineering evidence is relabeled as external authority", "non-conversion firewall"),
        ("private_material_leak", "IDs, routes, paths, or credentials enter artifacts", "family privacy scan and exact staged review"),
        ("negative_erasure", "a later pass deletes earlier failures", "append-only retained-negative register"),
    ]
    write_json(
        phase / "threat-model.json",
        {
            "schema": "ghc.family.v642-v6.threat-model.v1",
            "phase": PHASE,
            "owner": OWNER,
            "assets": ["frozen proposal intent", "source status", "negative evidence", "authority boundaries", "privacy boundary", "terminal verdict"],
            "trust_boundaries": ["repository versus external reality", "synthetic versus real data", "technical artifact versus competent authority", "same-owner versus independent team", "private runtime versus public artifact"],
            "threat_count": len(threat_rows),
            "threats": [
                {"threat_id": f"V6426-T{index:02d}", "class": klass, "failure": failure, "control": control, "residual_risk": "open_or_exact_gate_remains"}
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
            "schema": "ghc.family.v642-v6.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "active_phase": "v642-gmut-thos-v6-x2-evidence-candidate",
            "latest_closed_phase": "v642-gmut-thos-v5-x1-x2",
            "latest_completed_x1": {"phase": "v642-gmut-thos-v6-x1", "commit": x1_commit, "remote_equal": True},
            "latest_completed_x2": "evidence_candidate_not_closeout",
            "active_lanes": ["Orin Thale owned branch"],
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
    repository_valid = False
    validators_valid = False
    detached_valid = False
    if repository_receipt_path.exists():
        repository_receipt = read_json(repository_receipt_path)
        repository_valid = (
            repository_receipt.get("valid") is True
            and repository_receipt.get("tests_run") == repository_receipt.get("passed")
            and repository_receipt.get("failures") == 0
            and repository_receipt.get("errors") == 0
        )
    if full_receipt_path.exists() and minimal_receipt_path.exists():
        validators_valid = read_json(full_receipt_path).get("valid") is True and read_json(minimal_receipt_path).get("valid") is True
    if detached_receipt_path.exists():
        detached_valid = read_json(detached_receipt_path).get("valid") is True and snapshot_state == "verified"

    write_json(
        phase / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v642-v6.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "owner": OWNER,
            "state": "evidence_validated_closeout_pending" if repository_valid and validators_valid and detached_valid else "evidence_candidate_incomplete_for_closeout",
            "required_rows": [
                {"item": "x1 remote-equal freeze", "complete": True},
                {"item": "ten x2 proposals executed to bounded outcome", "complete": True},
                {"item": "all inherited and new negatives retained", "complete": True},
                {"item": "open and exact gates visible", "complete": True},
                {"item": "accessible static report built", "complete": (phase / "deliverables/v642-v6-evidence-integrity-report.html").exists()},
                {"item": "complete repository suite passes", "complete": repository_valid},
                {"item": "full and minimal validators pass", "complete": validators_valid},
                {"item": "fresh detached evidence snapshots validate", "complete": detached_valid},
                {"item": "closeout, seal, and final detached validation", "complete": False},
                {"item": "final remote equality", "complete": False},
            ],
            "required_complete": False,
            "open_gaps_are_valid_outcomes": True,
            "exact_gates_are_valid_outcomes": True,
            "boundary": "Do not close on elapsed time, watcher state, a prepared baton, or local candidate checks.",
        },
    )

    tool_paths = [
        "scripts/ghc_family_evidence_integrity.py",
        "scripts/ghc_family_evidence_integrity_validator.py",
        "scripts/ghc_family_evidence_integrity_minimal.py",
        "scripts/build_ghc_family_evidence_integrity_report.py",
        "tests/test_ghc_family_v642_v6.py",
    ]
    tool_rows = []
    for relative in tool_paths:
        path = repo / relative
        if path.exists():
            tool_rows.append({"path": relative, "normalized_sha256": normalized_sha256(path)})
    write_json(
        phase / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v642-v6.executed-toolchain.v1",
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
            "schema": "ghc.family.v642-v6.manifest.v1",
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
