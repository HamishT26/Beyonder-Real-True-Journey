#!/usr/bin/env python3
"""Build bounded v643-v4 boundary-evidence artifacts from frozen x1 fixtures.

The standard-library-only engine evaluates local deterministic structures.  A
passing fixture is never empirical, participant, production, legal, cultural,
accessibility-complete, exhaustive-security, independent-team, or Stage 20
evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


PHASE = "v643-gmut-thos-v4-x1-x2"
OWNER = "Orin Thale"
SOURCE_COMMIT = "5b32e03e87ba1a33c8ebe53c08ccb653d00fb3e0"
SOURCE_SEAL = "e6303cb4c1c25922074749f70b580488562b466d"
X1_COMMIT = "28ecb3137c3c3d7e4b43251a5b496c7995f11de5"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
OBSERVED = {
    "V6434-P01": "completed",
    "V6434-P02": "completed",
    "V6434-P03": "represented",
    "V6434-P04": "represented",
    "V6434-P05": "open_gap",
    "V6434-P06": "completed",
    "V6434-P07": "exact_gate",
    "V6434-P08": "completed",
    "V6434-P09": "completed",
    "V6434-P10": "completed",
}

BOUNDARY = (
    "Bounded repository engineering evidence only. GMUT remains a typed scalar-tensor/EFT research-model "
    "family, not an established force, unique prediction, likelihood result, empirical confirmation, proof, "
    "final physics, or Theory of Everything. THOS remains proxy without preregistered blind matched-budget "
    "real arms, real participants and raters, and independent review. No production Freed ID, CBR legitimacy, "
    "affected-party acceptance, Māori wording or authority, Māori data governance, cultural ratification, "
    "legal interpretation, enacted-law status, deployment, exhaustive security, complete accessibility, "
    "independent-team reproduction, AGI/ASI, consciousness, sentience, personhood, proof/canon, sibling merge, "
    "or Stage 20 readiness is established."
)


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def correction_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("update_type") not in {"correction", "retraction", "expression_of_concern", "supersession"}:
        reasons.append("post_publication_update_type_missing")
    if not row.get("source_identity_bound"):
        reasons.append("updated_source_identity_unbound")
    if not row.get("dependency_edges_complete"):
        reasons.append("downstream_dependency_edges_incomplete")
    if row.get("status_types_flattened"):
        reasons.append("distinct_update_statuses_flattened")
    if not row.get("quarantine_active"):
        reasons.append("stale_citation_not_quarantined")
    if row.get("stale_claim_promoted"):
        reasons.append("stale_downstream_claim_promoted")
    if row.get("clearance_without_review"):
        reasons.append("quarantine_cleared_without_review")
    if row.get("update_proves_truth_or_falsity"):
        reasons.append("metadata_promoted_to_truth_verdict")
    return decision(reasons, {"source_claim_reassessed": False, "external_adjudication": False})


def wellposedness_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("characteristic_data_surface_declared"):
        reasons.append("characteristic_data_surface_missing")
    if not row.get("initial_data_admissible"):
        reasons.append("initial_data_not_admissible")
    if not row.get("boundary_compatibility_declared"):
        reasons.append("boundary_compatibility_missing")
    if not row.get("existence_obligation_recorded"):
        reasons.append("existence_obligation_missing")
    if not row.get("uniqueness_obligation_recorded"):
        reasons.append("uniqueness_obligation_missing")
    if not row.get("continuous_dependence_obligation_recorded"):
        reasons.append("continuous_dependence_obligation_missing")
    if row.get("model_specific_theorem_claim"):
        reasons.append("typed_obligation_promoted_to_model_specific_theorem")
    if row.get("prediction_or_observation_claim"):
        reasons.append("wellposedness_scaffold_promoted_to_empirical_prediction")
    return decision(reasons, {"gmut_wellposedness_proved": False, "empirical_prediction": False})


def mnar_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("missingness_class") != "MNAR_sensitivity_only":
        reasons.append("missingness_class_not_bounded")
    if not row.get("selection_parameter_declared"):
        reasons.append("selection_parameter_missing")
    if len(row.get("sensitivity_grid", [])) < 3:
        reasons.append("sensitivity_grid_too_small")
    if row.get("real_rows") != 0:
        reasons.append("unverified_real_row_count")
    if not row.get("synthetic_provenance"):
        reasons.append("synthetic_provenance_missing")
    if not row.get("zero_row_promotion_lock"):
        reasons.append("zero_row_promotion_lock_missing")
    if row.get("likelihood_result_claim"):
        reasons.append("synthetic_selection_grid_promoted_to_likelihood")
    if row.get("empirical_confirmation_claim"):
        reasons.append("zero_rows_promoted_to_empirical_confirmation")
    return decision(reasons, {"real_rows": 0, "likelihood_executed": False, "evidence_class": "synthetic_proxy"})


def mediation_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("treatment_precedes_mediator"):
        reasons.append("treatment_mediator_order_invalid")
    if not row.get("mediator_precedes_outcome"):
        reasons.append("mediator_outcome_order_invalid")
    if not row.get("pretreatment_confounders_declared"):
        reasons.append("pretreatment_confounders_missing")
    if row.get("post_treatment_confounding_erased"):
        reasons.append("post_treatment_confounding_erased")
    if row.get("sequential_ignorability_established"):
        reasons.append("sequential_ignorability_overclaimed")
    if row.get("real_rows") != 0:
        reasons.append("unverified_real_mediation_rows")
    if not row.get("proxy_label"):
        reasons.append("proxy_label_missing")
    if row.get("causal_mechanism_claim"):
        reasons.append("synthetic_decomposition_promoted_to_causal_mechanism")
    return decision(reasons, {"real_rows": 0, "causal_mechanism_established": False, "evidence_class": "represented_proxy"})


def facilitator_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    required = {"ethics", "consent", "blind_matched_budget_arms", "repeated_facilitator_observations", "calendar_time_model", "real_participants_and_raters", "independent_review"}
    if set(row.get("requirements_recorded", [])) != required:
        reasons.append("real_arm_requirements_incomplete")
    if row.get("gap_state") != "open":
        reasons.append("facilitator_real_arm_gap_closed_without_evidence")
    if row.get("real_participants") != 0 or row.get("real_arms") != 0:
        reasons.append("unverified_real_participant_or_arm_count")
    if row.get("ethics_or_consent_obtained"):
        reasons.append("ethics_or_consent_claim_without_record")
    if row.get("learning_curve_estimated"):
        reasons.append("learning_curve_claim_without_longitudinal_real_rows")
    if row.get("temporal_parity_established"):
        reasons.append("temporal_parity_claim_without_real_arms")
    if row.get("independent_review_completed"):
        reasons.append("independent_review_claim_without_return")
    if row.get("effectiveness_or_superiority_claim"):
        reasons.append("thos_effect_or_superiority_overclaim")
    return decision(reasons, {"gap_state": "open", "real_participants": 0, "real_arms": 0})


def delegation_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("controller_edges_explicit"):
        reasons.append("controller_edges_ambiguous")
    if not row.get("acyclic"):
        reasons.append("controller_cycle_detected")
    if not row.get("capabilities_attenuate"):
        reasons.append("delegated_capability_amplifies")
    if not row.get("purposes_attenuate"):
        reasons.append("delegated_purpose_expands")
    if not row.get("delegation_depth_bounded"):
        reasons.append("delegation_depth_unbounded")
    if row.get("verification_method_is_governance_authority"):
        reasons.append("verification_method_promoted_to_governance_authority")
    if row.get("real_key_or_proof_claim"):
        reasons.append("fixture_promoted_to_real_key_or_proof")
    if row.get("production_interoperability_claim"):
        reasons.append("static_graph_promoted_to_production_interoperability")
    return decision(reasons, {"real_keys": 0, "live_resolution": False, "production_ready": False})


def confidentiality_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("state") != "pending_exact_authority":
        reasons.append("exact_authority_gate_not_pending")
    if not row.get("neutral_issue_fields_only"):
        reasons.append("repository_exceeded_neutral_issue_spotting")
    if row.get("technical_authority_substitution"):
        reasons.append("technical_fixture_substituted_for_authority")
    if row.get("confidentiality_automatically_overrides_disclosure"):
        reasons.append("confidentiality_given_automatic_priority")
    if row.get("disclosure_automatically_overrides_confidentiality"):
        reasons.append("disclosure_given_automatic_priority")
    if row.get("affected_party_legitimacy_claim"):
        reasons.append("affected_party_legitimacy_overclaimed")
    if row.get("maori_authority_or_wording_claim"):
        reasons.append("maori_authority_or_wording_overclaimed")
    if row.get("legal_or_cultural_conclusion"):
        reasons.append("legal_or_cultural_conclusion_without_authority")
    return decision(reasons, {"state": "pending_exact_authority", "concrete_ruling": False})


def canonicalization_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("duplicate_member_names"):
        reasons.append("duplicate_member_names_rejected")
    if not row.get("i_json_compatible"):
        reasons.append("payload_not_i_json_compatible")
    if not row.get("finite_numbers_only"):
        reasons.append("non_finite_number_present")
    if row.get("negative_zero_policy") != "reject_input":
        reasons.append("negative_zero_ambiguity_unresolved")
    if row.get("unicode_policy") != "preserve_as_is":
        reasons.append("unicode_payload_mutated")
    if row.get("property_sort") != "utf16_code_units_recursive":
        reasons.append("property_sort_not_jcs_compatible")
    if not row.get("canonical_bytes_explicit"):
        reasons.append("bytes_presented_for_signature_not_explicit")
    if row.get("live_signature_or_interoperability_claim"):
        reasons.append("static_fixture_promoted_to_live_signature_interoperability")
    return decision(reasons, {"live_signatures": 0, "real_keys": 0, "interoperability_established": False})


def floating_environment_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("rounding_mode") != "roundTiesToEven":
        reasons.append("rounding_mode_missing_or_different")
    if row.get("precision") != "binary64":
        reasons.append("numeric_precision_unbound")
    if row.get("signed_zero_policy") != "preserve_and_compare_explicitly":
        reasons.append("signed_zero_policy_missing")
    if not row.get("exception_policy_declared"):
        reasons.append("floating_exception_policy_missing")
    if row.get("architecture_scope") != "current_host_only":
        reasons.append("architecture_scope_overstated")
    if not row.get("same_owner_only"):
        reasons.append("same_owner_boundary_missing")
    if row.get("cross_architecture_parity_claim"):
        reasons.append("same_host_replay_promoted_to_cross_architecture_parity")
    if row.get("independent_reproduction_claim"):
        reasons.append("same_owner_replay_promoted_to_independent_reproduction")
    return decision(reasons, {"cross_architecture_parity": False, "independent_reproduction": False})


def coarse_graining_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("resolved_variables_declared"):
        reasons.append("resolved_variables_missing")
    if not row.get("unresolved_variables_declared"):
        reasons.append("unresolved_variables_erased")
    if not row.get("projection_declared"):
        reasons.append("coarse_graining_projection_missing")
    if not row.get("memory_effects_retained"):
        reasons.append("memory_effects_silently_dropped")
    if not row.get("time_scale_ratio_declared"):
        reasons.append("time_scale_ratio_missing")
    if row.get("markov_approximation_assumed_without_gate"):
        reasons.append("markov_approximation_ungated")
    if row.get("microscopic_proof_claim"):
        reasons.append("effective_description_promoted_to_microscopic_proof")
    if row.get("cross_pillar_or_stage20_claim"):
        reasons.append("coarse_graining_promoted_to_cross_pillar_or_stage20_evidence")
    return decision(reasons, {"microscopic_proof": False, "cross_pillar_conversion": False})


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    "V6434-P01": correction_decision,
    "V6434-P02": wellposedness_decision,
    "V6434-P03": mnar_decision,
    "V6434-P04": mediation_decision,
    "V6434-P05": facilitator_decision,
    "V6434-P06": delegation_decision,
    "V6434-P07": confidentiality_decision,
    "V6434-P08": canonicalization_decision,
    "V6434-P09": floating_environment_decision,
    "V6434-P10": coarse_graining_decision,
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    return {
        "V6434-P01": {"update_type": "correction", "source_identity_bound": True, "dependency_edges_complete": True, "status_types_flattened": False, "quarantine_active": True, "stale_claim_promoted": False, "clearance_without_review": False, "update_proves_truth_or_falsity": False},
        "V6434-P02": {"characteristic_data_surface_declared": True, "initial_data_admissible": True, "boundary_compatibility_declared": True, "existence_obligation_recorded": True, "uniqueness_obligation_recorded": True, "continuous_dependence_obligation_recorded": True, "model_specific_theorem_claim": False, "prediction_or_observation_claim": False},
        "V6434-P03": {"missingness_class": "MNAR_sensitivity_only", "selection_parameter_declared": True, "sensitivity_grid": [-1.0, 0.0, 1.0], "real_rows": 0, "synthetic_provenance": True, "zero_row_promotion_lock": True, "likelihood_result_claim": False, "empirical_confirmation_claim": False},
        "V6434-P04": {"treatment_precedes_mediator": True, "mediator_precedes_outcome": True, "pretreatment_confounders_declared": True, "post_treatment_confounding_erased": False, "sequential_ignorability_established": False, "real_rows": 0, "proxy_label": True, "causal_mechanism_claim": False},
        "V6434-P05": {"requirements_recorded": ["ethics", "consent", "blind_matched_budget_arms", "repeated_facilitator_observations", "calendar_time_model", "real_participants_and_raters", "independent_review"], "gap_state": "open", "real_participants": 0, "real_arms": 0, "ethics_or_consent_obtained": False, "learning_curve_estimated": False, "temporal_parity_established": False, "independent_review_completed": False, "effectiveness_or_superiority_claim": False},
        "V6434-P06": {"controller_edges_explicit": True, "acyclic": True, "capabilities_attenuate": True, "purposes_attenuate": True, "delegation_depth_bounded": True, "verification_method_is_governance_authority": False, "real_key_or_proof_claim": False, "production_interoperability_claim": False},
        "V6434-P07": {"state": "pending_exact_authority", "neutral_issue_fields_only": True, "technical_authority_substitution": False, "confidentiality_automatically_overrides_disclosure": False, "disclosure_automatically_overrides_confidentiality": False, "affected_party_legitimacy_claim": False, "maori_authority_or_wording_claim": False, "legal_or_cultural_conclusion": False},
        "V6434-P08": {"duplicate_member_names": False, "i_json_compatible": True, "finite_numbers_only": True, "negative_zero_policy": "reject_input", "unicode_policy": "preserve_as_is", "property_sort": "utf16_code_units_recursive", "canonical_bytes_explicit": True, "live_signature_or_interoperability_claim": False},
        "V6434-P09": {"rounding_mode": "roundTiesToEven", "precision": "binary64", "signed_zero_policy": "preserve_and_compare_explicitly", "exception_policy_declared": True, "architecture_scope": "current_host_only", "same_owner_only": True, "cross_architecture_parity_claim": False, "independent_reproduction_claim": False},
        "V6434-P10": {"resolved_variables_declared": True, "unresolved_variables_declared": True, "projection_declared": True, "memory_effects_retained": True, "time_scale_ratio_declared": True, "markov_approximation_assumed_without_gate": False, "microscopic_proof_claim": False, "cross_pillar_or_stage20_claim": False},
    }


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6434-P01": [
        ("update-type-missing", {"update_type": "unknown"}),
        ("dependency-edges-incomplete", {"dependency_edges_complete": False}),
        ("status-types-flattened", {"status_types_flattened": True}),
        ("quarantine-inactive", {"quarantine_active": False}),
        ("stale-claim-promoted", {"stale_claim_promoted": True}),
        ("clearance-without-review", {"clearance_without_review": True}),
        ("truth-verdict-shortcut", {"update_proves_truth_or_falsity": True}),
    ],
    "V6434-P02": [
        ("characteristic-surface-missing", {"characteristic_data_surface_declared": False}),
        ("initial-data-inadmissible", {"initial_data_admissible": False}),
        ("boundary-incompatible", {"boundary_compatibility_declared": False}),
        ("existence-obligation-missing", {"existence_obligation_recorded": False}),
        ("uniqueness-obligation-missing", {"uniqueness_obligation_recorded": False}),
        ("continuous-dependence-missing", {"continuous_dependence_obligation_recorded": False}),
        ("theorem-and-prediction-overclaim", {"model_specific_theorem_claim": True, "prediction_or_observation_claim": True}),
    ],
    "V6434-P03": [
        ("missingness-class-flattened", {"missingness_class": "MAR"}),
        ("selection-parameter-missing", {"selection_parameter_declared": False}),
        ("sensitivity-grid-too-small", {"sensitivity_grid": [0.0]}),
        ("synthetic-provenance-missing", {"synthetic_provenance": False}),
        ("zero-row-lock-missing", {"zero_row_promotion_lock": False}),
        ("likelihood-overclaim", {"likelihood_result_claim": True}),
        ("empirical-overclaim", {"empirical_confirmation_claim": True}),
    ],
    "V6434-P04": [
        ("treatment-mediator-order-invalid", {"treatment_precedes_mediator": False}),
        ("mediator-outcome-order-invalid", {"mediator_precedes_outcome": False}),
        ("pretreatment-confounders-missing", {"pretreatment_confounders_declared": False}),
        ("post-treatment-confounding-erased", {"post_treatment_confounding_erased": True}),
        ("ignorability-overclaimed", {"sequential_ignorability_established": True}),
        ("proxy-label-missing", {"proxy_label": False}),
        ("causal-mechanism-overclaim", {"causal_mechanism_claim": True}),
    ],
    "V6434-P05": [
        ("requirements-incomplete", {"requirements_recorded": ["ethics"]}),
        ("gap-closed", {"gap_state": "closed"}),
        ("unverified-real-rows", {"real_participants": 12, "real_arms": 2}),
        ("ethics-consent-overclaim", {"ethics_or_consent_obtained": True}),
        ("learning-curve-overclaim", {"learning_curve_estimated": True}),
        ("temporal-parity-overclaim", {"temporal_parity_established": True}),
        ("review-and-superiority-overclaim", {"independent_review_completed": True, "effectiveness_or_superiority_claim": True}),
    ],
    "V6434-P06": [
        ("controller-edges-ambiguous", {"controller_edges_explicit": False}),
        ("authority-cycle", {"acyclic": False}),
        ("capability-amplification", {"capabilities_attenuate": False}),
        ("purpose-expansion", {"purposes_attenuate": False}),
        ("delegation-depth-unbounded", {"delegation_depth_bounded": False}),
        ("governance-authority-substitution", {"verification_method_is_governance_authority": True}),
        ("production-real-key-overclaim", {"real_key_or_proof_claim": True, "production_interoperability_claim": True}),
    ],
    "V6434-P07": [
        ("gate-closed", {"state": "resolved"}),
        ("non-neutral-ruling", {"neutral_issue_fields_only": False}),
        ("technical-authority-substitution", {"technical_authority_substitution": True}),
        ("confidentiality-automatic-priority", {"confidentiality_automatically_overrides_disclosure": True}),
        ("disclosure-automatic-priority", {"disclosure_automatically_overrides_confidentiality": True}),
        ("affected-party-overclaim", {"affected_party_legitimacy_claim": True}),
        ("maori-legal-cultural-overclaim", {"maori_authority_or_wording_claim": True, "legal_or_cultural_conclusion": True}),
    ],
    "V6434-P08": [
        ("duplicate-members", {"duplicate_member_names": True}),
        ("not-i-json", {"i_json_compatible": False}),
        ("non-finite-number", {"finite_numbers_only": False}),
        ("negative-zero-unresolved", {"negative_zero_policy": "serialize_as_zero"}),
        ("unicode-normalized", {"unicode_policy": "normalize_nfc"}),
        ("wrong-property-sort", {"property_sort": "utf8_bytes"}),
        ("live-interoperability-overclaim", {"canonical_bytes_explicit": False, "live_signature_or_interoperability_claim": True}),
    ],
    "V6434-P09": [
        ("rounding-mode-different", {"rounding_mode": "towardZero"}),
        ("precision-unbound", {"precision": "unspecified"}),
        ("signed-zero-flattened", {"signed_zero_policy": "flatten"}),
        ("exception-policy-missing", {"exception_policy_declared": False}),
        ("architecture-overstated", {"architecture_scope": "all_architectures"}),
        ("same-owner-boundary-missing", {"same_owner_only": False}),
        ("cross-architecture-independent-overclaim", {"cross_architecture_parity_claim": True, "independent_reproduction_claim": True}),
    ],
    "V6434-P10": [
        ("resolved-variables-missing", {"resolved_variables_declared": False}),
        ("unresolved-variables-erased", {"unresolved_variables_declared": False}),
        ("projection-missing", {"projection_declared": False}),
        ("memory-silently-dropped", {"memory_effects_retained": False}),
        ("time-scale-ratio-missing", {"time_scale_ratio_declared": False}),
        ("markov-approximation-ungated", {"markov_approximation_assumed_without_gate": True}),
        ("proof-and-stage20-overclaim", {"microscopic_proof_claim": True, "cross_pillar_or_stage20_claim": True}),
    ],
}


# Only actual x2 operational failures belong here.  Additive patches retain any
# failures discovered during evidence, snapshot, closeout, seal, or final work.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6434-X2-N01",
        "origin": "v643-v4-x2-operational",
        "observed": "The first detailed evidence validation passed 1539 of 1540 checks but queried owned_generated_files while the threat-model schema used owner_generated_files.",
        "recovery": "Preserve the failed validation receipt, align the validator with the declared threat-model key, rebuild all count-dependent artifacts, and require a complete detailed rerun before evidence commit.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6434-X2-N02",
        "origin": "v643-v4-x2-operational",
        "observed": "The second detailed evidence validation passed 1542 of 1543 checks but the current-label scan found the validator's own mojibake-forbidden check label inside the preserved first failure receipt.",
        "recovery": "Use an ASCII check label, quarantine only the two named failed validation receipts from the current-semantic-label scan, retain both receipts, rebuild count-dependent artifacts, and require another complete rerun.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6434-X2-N03",
        "origin": "v643-v4-x2-operational",
        "observed": "A PowerShell exact-stage verification reported a same-count list and hash mismatch because its culture-sensitive Sort-Object order differed from the receipt's Python Unicode code-point ordering.",
        "recovery": "Retain the false-negative check, recompute with the receipt generator's canonical Python ordering, prove exact list and hash equality, and record the sort-order contract in the staged receipt.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
]


def fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    catalog: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, base in canonical_inputs().items():
        rows = [{"case_id": f"{proposal_id}-C00", "label": "canonical-bounded", "input": copy.deepcopy(base), "expected_accepted": True}]
        for index, (label, changes) in enumerate(MUTATIONS[proposal_id], start=1):
            mutated = copy.deepcopy(base)
            mutated.update(copy.deepcopy(changes))
            rows.append({"case_id": f"{proposal_id}-C{index:02d}", "label": label, "input": mutated, "expected_accepted": False})
        catalog[proposal_id] = rows
    return catalog


def evaluate_catalog() -> dict[str, list[dict[str, Any]]]:
    evaluated: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, rows in fixture_catalog().items():
        output = []
        for row in rows:
            accepted, reasons, details = DECISIONS[proposal_id](row["input"])
            output.append({
                "case_id": row["case_id"],
                "label": row["label"],
                "expected_accepted": row["expected_accepted"],
                "accepted": accepted,
                "matched_expectation": accepted == row["expected_accepted"],
                "reasons": reasons,
                "details": details,
            })
        evaluated[proposal_id] = output
    return evaluated


def git_blob(repo: Path, commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def x1_content_seal(repo: Path, phase: Path) -> dict[str, Any]:
    exact = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    entries = []
    for relative in exact["files"]:
        working = repo / relative
        blob = git_blob(repo, X1_COMMIT, relative)
        blob_normalized = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        working_normalized = normalized_bytes(working)
        entries.append({
            "repo_path": relative,
            "git_blob_sha256": hashlib.sha256(blob).hexdigest(),
            "git_blob_sha256_lf_normalized": hashlib.sha256(blob_normalized).hexdigest(),
            "working_sha256_lf_normalized": hashlib.sha256(working_normalized).hexdigest(),
            "bytes_lf_normalized": len(working_normalized),
            "unchanged": blob_normalized == working_normalized,
        })
    if not all(row["unchanged"] for row in entries):
        raise RuntimeError("one or more frozen x1 files changed after the dedicated commit")
    return {
        "schema": "ghc.family.v643-v4.x1-content-seal.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_COMMIT,
        "entry_count": len(entries),
        "entries": entries,
        "all_unchanged": True,
        "boundary": "The dedicated Git commit and normalized content parity bind x1. This is workflow integrity, not scientific proof or independent reproduction.",
    }


def open_and_exact_gates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    open_gaps = [
        {"gate_id": "V6434-OG01", "surface": "GMUT model-specific well-posedness proof, derivation, real data, likelihood, prediction, force, and empirical evidence", "needs": ["model-specific initial-boundary derivation", "expert mathematical review", "real public data", "executed likelihood", "systematic uncertainty", "independent scientific review"]},
        {"gate_id": "V6434-OG02", "surface": "THOS mediation, facilitator learning curve, temporal drift, burden, safety, effectiveness, and superiority", "needs": ["ethics review", "consent", "preregistered blind matched-budget real arms", "real participants and raters", "validated measures", "calendar-time model", "independent review"]},
        {"gate_id": "V6434-OG03", "surface": "Freed ID production status and live operations", "needs": ["standards-conformant real keys and proofs", "live resolution, status, and revocation", "interoperability", "privacy assurance", "independent security review", "trust governance"]},
        {"gate_id": "V6434-OG04", "surface": "different-architecture and independent-team reproduction, and Stage 20", "needs": ["genuinely different architecture", "independently owned protocol", "independent team and infrastructure", "returned results", "competent action-specific review"]},
        {"gate_id": "V6434-OG05", "surface": "accessibility evaluation", "needs": ["qualified manual accessibility evaluation", "affected-user evaluation"]},
    ]
    exact_gates = [
        {"gate_id": "V6434-EG01", "surface": "CBR settlement confidentiality, compelled disclosure, public-interest limits, remedy, representation, legitimacy, and affected-party acceptance", "reserved_to": ["authorized affected parties", "authorized representatives", "competent authorities"]},
        {"gate_id": "V6434-EG02", "surface": "Māori wording, authority, concepts, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6434-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6434-EG04", "surface": "legal interpretation, enacted law, confidentiality, compelled disclosure, jurisdiction, standing, deadlines, and forum competence", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6434-EG05", "surface": "production, deployment, private publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user authorization and competent operational authority"]},
        {"gate_id": "V6434-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience, personhood, AGI/ASI, or sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    return open_gaps, exact_gates


def manifest_candidates(repo: Path, phase: Path, proposals: list[dict[str, Any]]) -> list[str]:
    x1 = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))["files"]
    deliverables = [f"docs/orin-thale/v643-v4/{relative}" for proposal in proposals for relative in proposal["deliverables"]]
    core = [
        "docs/orin-thale/v643-v4/x2-proposal-ledger.json",
        "docs/orin-thale/v643-v4/evidence/evidence-ledger.json",
        "docs/orin-thale/v643-v4/retained-negative-register.json",
        "docs/orin-thale/v643-v4/exact-open-gate-register.json",
        "docs/orin-thale/v643-v4/threat-model.json",
        "docs/orin-thale/v643-v4/phase-truth.json",
        "docs/orin-thale/v643-v4/complete-incomplete-checklist.json",
        "docs/orin-thale/v643-v4/environment/x2-execution-receipt.json",
        "docs/orin-thale/v643-v4/reproduction/independent-team-gap.json",
        "docs/orin-thale/v643-v4/reproduction/evidence-snapshot-plan.json",
        "docs/orin-thale/v643-v4/reproduction/x1-content-seal.json",
        "docs/orin-thale/v643-v4/tooling/executed-toolchain.json",
        "docs/orin-thale/v643-v4/stage20/domain-veto-evidence-board.json",
        "docs/orin-thale/v643-v4/deliverables/v643-v4-boundary-evidence-report.html",
        "docs/orin-thale/v643-v4/accessibility/static-report-receipt.json",
    ]
    tools = [
        "scripts/ghc_family_boundary_evidence.py",
        "scripts/ghc_family_boundary_evidence_validator.py",
        "scripts/ghc_family_boundary_evidence_minimal.py",
        "scripts/build_ghc_family_boundary_evidence_report.py",
        "tests/test_ghc_family_v643_v4.py",
    ]
    candidates = list(dict.fromkeys(list(x1) + deliverables + core + tools))
    return [relative for relative in candidates if (repo / relative).is_file()]


def build(repo: Path, snapshot_state: str = "pending", lifecycle: str = "evidence") -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / "docs/orin-thale/v643-v4"
    if snapshot_state == "pending" and lifecycle != "evidence":
        raise ValueError("closeout, seal, and final lifecycles require verified same-owner evidence snapshots")
    proposals = json.loads((phase / "x1-proposals.json").read_text(encoding="utf-8"))["proposals"]
    if {row["proposal_id"]: row["expected_disposition"] for row in proposals} != OBSERVED:
        raise RuntimeError("observed artifact dispositions diverge from the frozen expected map")
    evaluations = evaluate_catalog()
    if not all(row["matched_expectation"] for rows in evaluations.values() for row in rows):
        raise RuntimeError("one or more preregistered fixtures failed its expected decision")

    evidence_rows = []
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        accepted = sum(row["accepted"] for row in rows)
        rejected = len(rows) - accepted
        contract = {
            "schema": f"ghc.family.v643-v4.{pid.lower()}.contract.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "title": proposal["title"],
            "observed_disposition": OBSERVED[pid],
            "disposition_scope": "artifact-level execution only",
            "canonical_case": rows[0],
            "accepted_case_count": accepted,
            "rejected_case_count": rejected,
            "authoritative_source_needs": proposal["authoritative_source_needs"],
            "protected_gates": proposal["protected_gates"],
            "external_claims_established": [],
            "boundary": BOUNDARY,
        }
        vectors = {
            "schema": f"ghc.family.v643-v4.{pid.lower()}.mutation-vectors.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "case_count": len(rows),
            "rejection_count": rejected,
            "all_matched_expectation": all(row["matched_expectation"] for row in rows),
            "cases": rows,
            "boundary": BOUNDARY,
        }
        gate = {
            "schema": f"ghc.family.v643-v4.{pid.lower()}.boundary.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "observed_disposition": OBSERVED[pid],
            "safe_now_result": "bounded structural, synthetic, protocol, open-gap, or exact-gate artifact only",
            "protected_gates": proposal["protected_gates"],
            "external_claims_established": [],
            "rollback_or_recovery": proposal["rollback_or_recovery"],
            "boundary": BOUNDARY,
        }
        for relative, payload in zip(proposal["deliverables"], (contract, vectors, gate), strict=True):
            write_json(phase / relative, payload)
        evidence_rows.append({
            "proposal_id": pid,
            "title": proposal["title"],
            "observed_disposition": OBSERVED[pid],
            "disposition_scope": "artifact-level execution only",
            "case_count": len(rows),
            "accepted": accepted,
            "rejected": rejected,
            "artifacts": proposal["deliverables"],
            "external_claims_established": [],
        })

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v643-v4.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source_commit": SOURCE_COMMIT,
        "source_seal": SOURCE_SEAL,
        "x1_commit": X1_COMMIT,
        "proposal_count": 10,
        "case_count": 80,
        "synthetic_rejection_count": 70,
        "distribution": distribution,
        "x1_before_x2_preserved": True,
        "proposals": evidence_rows,
        "boundary": BOUNDARY,
    })
    write_json(phase / "evidence/evidence-ledger.json", {
        "schema": "ghc.family.v643-v4.evidence-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "evidence_class": "local_structural_synthetic_protocol_open_gap_or_exact_gate_artifact",
        "rows": evidence_rows,
        "empirical_rows": 0,
        "real_participants": 0,
        "real_arms": 0,
        "real_raters": 0,
        "real_keys_or_proofs": 0,
        "legal_or_cultural_ratifications": 0,
        "independent_team_returns": 0,
        "different_architecture_returns": 0,
        "boundary": BOUNDARY,
    })

    inherited_path = repo / "docs/sable-rook/v643-v3/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = copy.deepcopy(inherited["negatives"])
    for proposal_id, rows in evaluations.items():
        for row in rows:
            if not row["accepted"]:
                negatives.append({
                    "negative_id": f"V6434-SYN-{row['case_id']}",
                    "origin": "v643-v4-preregistered-synthetic",
                    "proposal_id": proposal_id,
                    "case_id": row["case_id"],
                    "observed": row["reasons"],
                    "retained": True,
                    "resolved_for_current_local_scope": True,
                    "external_gate_closed": False,
                })
    x1_audit = json.loads((phase / "provenance/prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    x1_negatives = []
    for item in x1_audit.get("x1_execution_negatives", []):
        x1_negatives.append({
            "negative_id": item["negative_id"],
            "origin": "v643-v4-x1-operational",
            "observed": item["observed_failure"],
            "recovery": item["recovery"],
            "retained": True,
            "resolved_for_current_local_scope": True,
            "external_gate_closed": False,
        })
    negatives.extend(x1_negatives)
    negatives.extend(copy.deepcopy(X2_OPERATIONAL_NEGATIVES))
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v643-v4.retained-negative-register.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_from": "docs/sable-rook/v643-v3/retained-negative-register.json",
        "inherited_sha256_lf_normalized": normalized_sha256(inherited_path),
        "inherited_count": 637,
        "x1_operational_count": len(x1_negatives),
        "new_synthetic_count": 70,
        "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
        "new_count": 70 + len(x1_negatives) + len(X2_OPERATIONAL_NEGATIVES),
        "negative_count": len(negatives),
        "all_retained": True,
        "erasure_permitted": False,
        "negatives": negatives,
        "boundary": BOUNDARY,
    })

    open_gaps, exact_gates = open_and_exact_gates()
    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v643-v4.exact-open-gate-register.v1",
        "phase": PHASE,
        "owner": OWNER,
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "open_gaps": open_gaps,
        "exact_gates": exact_gates,
        "all_visible": True,
        "none_silently_closed": True,
        "boundary": BOUNDARY,
    })

    threats = [
        {"id": "T01", "threat": "post-publication source status does not reach dependent claims", "control": "typed update graph and stale-citation quarantine"},
        {"id": "T02", "threat": "correction, retraction, concern, and supersession are flattened", "control": "status-specific transitions and review-bound clearance"},
        {"id": "T03", "threat": "a GMUT equation is promoted without a well-posed initial-boundary problem", "control": "characteristic, compatibility, existence, uniqueness, and continuous-dependence obligations"},
        {"id": "T04", "threat": "MNAR sensitivity fixtures become observed likelihood evidence", "control": "selection parameter provenance and zero-row promotion lock"},
        {"id": "T05", "threat": "post-treatment confounding is erased in THOS mediation", "control": "timing, identification, proxy, and causal-nonpromotion rules"},
        {"id": "T06", "threat": "facilitator learning or drift is claimed without longitudinal real arms", "control": "open gap requiring ethics, real rows, calendar time, budget parity, and review"},
        {"id": "T07", "threat": "delegation amplifies capability or cycles authority", "control": "acyclic monotonic attenuation graph"},
        {"id": "T08", "threat": "a verification method is mistaken for governance authority", "control": "purpose-bound structural role and production gate"},
        {"id": "T09", "threat": "repository output decides confidentiality, disclosure, public interest, or Māori authority", "control": "neutral issue fields and exact authority gate"},
        {"id": "T10", "threat": "ambiguous serialization changes signed meaning", "control": "I-JSON, duplicate-name refusal, explicit bytes, number and Unicode policies"},
        {"id": "T11", "threat": "same-host numeric replay is promoted to cross-architecture parity", "control": "rounding environment and architecture-scope boundary"},
        {"id": "T12", "threat": "coarse graining silently deletes memory or unresolved variables", "control": "projection, scale, memory, and resolved-variable ledger"},
        {"id": "T13", "threat": "repository checks compensate for missing empirical or authority evidence", "control": "domain vetoes and non-substitution terminal board"},
        {"id": "T14", "threat": "privacy scan or static report is called exhaustive or fully accessible", "control": "bounded pattern classes and reserved manual/affected-user evaluation"},
    ]
    write_json(phase / "threat-model.json", {
        "schema": "ghc.family.v643-v4.threat-model.v1",
        "phase": PHASE,
        "owner": OWNER,
        "threat_count": len(threats),
        "threats": threats,
        "exhaustive_security": False,
        "independent_security_review": False,
        "resource_ceilings": {"owner_generated_files": 15000, "scope": "v643-v4 only"},
        "boundary": BOUNDARY,
    })

    verified = snapshot_state == "verified"
    lifecycle_states = {"evidence": "EVIDENCE_VERIFIED" if verified else "EVIDENCE_CANDIDATE", "closeout": "CLOSEOUT_CANDIDATE", "seal": "SEALED_CANDIDATE", "final": "FINAL_HEAD_CANDIDATE"}
    pending = {
        "evidence": ["evidence commit", "two fresh detached same-owner snapshots", "closeout", "seal", "exact final validation", "one terminal baton"] if not verified else ["closeout", "seal", "exact final validation", "one terminal baton"],
        "closeout": ["closeout detached validation", "seal", "exact final validation", "one terminal baton"],
        "seal": ["seal detached validation", "exact final validation", "one terminal baton"],
        "final": ["exact final detached validation", "one terminal baton"],
    }
    protected_claims = {
        "empirical_gmut": False,
        "gmut_likelihood_or_unique_prediction": False,
        "thos_effectiveness_or_superiority": False,
        "production_freed_id": False,
        "cbr_legitimacy_or_affected_party_acceptance": False,
        "maori_authority_or_data_governance": False,
        "legal_or_cultural_ratification": False,
        "deployment_or_production_readiness": False,
        "complete_accessibility": False,
        "exhaustive_security": False,
        "independent_team_reproduction": False,
        "proof_or_canon": False,
        "consciousness_personhood_agi_asi": False,
        "stage20_readiness": False,
    }
    write_json(phase / "phase-truth.json", {
        "schema": "ghc.family.v643-v4.phase-truth.v1",
        "phase": PHASE,
        "owner": OWNER,
        "state": lifecycle_states[lifecycle],
        "source_commit": SOURCE_COMMIT,
        "source_seal": SOURCE_SEAL,
        "x1_commit": X1_COMMIT,
        "proposal_count": 10,
        "distribution": distribution,
        "case_count": 80,
        "synthetic_rejection_count": 70,
        "retained_negative_count": len(negatives),
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "primary_focus": "GMUT Mind",
        "all_three_pillars_preserved": True,
        "same_owner_repeatability": verified,
        "independent_team_reproduction": False,
        "protected_claims": protected_claims,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "outbound_message_count": 0,
        "successor_task_count": 0,
        "subagent_count": 0,
        "boundary": BOUNDARY,
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v643-v4.complete-incomplete-checklist.v1",
        "phase": PHASE,
        "owner": OWNER,
        "complete": [
            "exact Sable source, seal ancestry, clean state, and live-remote equality verified",
            "existing clean Orin lane advanced by fast-forward only",
            "dedicated x1 frozen, pushed, clean, and four-way equal before x2",
            "ten semantically distinct proposals executed only within frozen approval classes",
            "eighty deterministic fixtures with seventy retained rejecting mutations",
            "all 637 inherited negatives and every v643-v4 negative retained",
            "GMUT Mind, THOS Body, and Freed ID/CBR Heart preserved",
            "current official or primary source constraints recorded",
        ],
        "incomplete": [
            "model-specific GMUT well-posedness proof, real data, likelihood, prediction, force, or empirical confirmation",
            "blind matched-budget real THOS arms, mediation identification, facilitator drift, participant or rater evidence, safety, effectiveness, or superiority",
            "production Freed ID keys, proofs, live resolution, status, revocation, interoperability, privacy/security review, and trust governance",
            "CBR affected-party acceptance, Māori authority and data governance, cultural ratification, legal interpretation, and enacted-law status",
            "qualified manual and affected-user accessibility evaluation",
            "independent security review and exhaustive security",
            "different-architecture parity and independent-team reproduction",
            "Stage 20",
        ],
        "lifecycle": lifecycle,
        "same_owner_evidence_snapshots_verified": verified,
        "closeout_ready": verified,
        "pending": pending[lifecycle],
        "boundary": BOUNDARY,
    })

    write_json(phase / "environment/x2-execution-receipt.json", {
        "schema": "ghc.family.v643-v4.x2-execution-receipt.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_COMMIT,
        "x1_remote_equal_before_x2": True,
        "real_data_downloaded": False,
        "real_participants_or_raters": 0,
        "real_arms": 0,
        "real_keys_or_proofs": 0,
        "live_services_or_deployments": 0,
        "accounts_or_api_keys_changed": 0,
        "desktop_updated": False,
        "elevation_used": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "rebooted": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v643-v4.independent-team-gap.v1",
        "phase": PHASE,
        "owner": OWNER,
        "same_owner_evidence_snapshots_verified": verified,
        "shared_repository_protocol_and_infrastructure": True,
        "different_architecture_return_received": False,
        "independent_team_protocol_owned": False,
        "independent_team_return_received": False,
        "independent_team_reproduction_established": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/evidence-snapshot-plan.json", {
        "schema": "ghc.family.v643-v4.evidence-snapshot-plan.v1",
        "phase": PHASE,
        "owner": OWNER,
        "snapshot_count": 2,
        "location_class": "fresh detached D-drive worktrees",
        "required_same_commit": True,
        "required_clean_before_and_after": True,
        "required_checks": ["complete repository suite", "detailed validator", "minimal validator", "all JSON parsing", "privacy and raw-ID scan", "manifest parity"],
        "claim_scope": "same-owner repeatability only",
        "independent_team_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/x1-content-seal.json", x1_content_seal(repo, phase))
    write_json(phase / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v643-v4.executed-toolchain.v1",
        "phase": PHASE,
        "owner": OWNER,
        "tools": [
            {"name": "ghc_family_boundary_evidence.py", "role": "80-case evidence builder and retained-negative assembler"},
            {"name": "ghc_family_boundary_evidence_validator.py", "role": "detailed evidence, manifest, privacy, report, and boundary validation"},
            {"name": "ghc_family_boundary_evidence_minimal.py", "role": "small standard-library validation floor"},
            {"name": "build_ghc_family_boundary_evidence_report.py", "role": "accessible static HTML report builder"},
            {"name": "test_ghc_family_v643_v4.py", "role": "decision, fixture, retention, manifest, and validator regression suite"},
        ],
        "caller_compatibility_preserved": True,
        "inherited_tools_mutated": False,
        "mass_deletion_performed": False,
        "boundary": BOUNDARY,
    })
    vetoes = [
        {"domain": "GMUT Mind", "local_artifact_status": "pass", "external_evidence_status": "missing", "decision": "veto", "reason": "no model-specific theorem, real data, likelihood, force, prediction, or empirical confirmation"},
        {"domain": "THOS Body", "local_artifact_status": "pass", "external_evidence_status": "missing", "decision": "veto", "reason": "no preregistered blind matched-budget real arms, participants, raters, or independent review"},
        {"domain": "Freed ID", "local_artifact_status": "pass", "external_evidence_status": "missing", "decision": "veto", "reason": "no real keys, live resolution/status/revocation, interoperability, review, or governance"},
        {"domain": "CBR and Māori authority", "local_artifact_status": "exact_gate", "external_evidence_status": "reserved", "decision": "veto", "reason": "affected-party, Māori, cultural, and legal authority cannot be substituted"},
        {"domain": "reproduction", "local_artifact_status": "same_owner_only" if verified else "pending", "external_evidence_status": "no independent return", "decision": "veto", "reason": "shared owner, protocol, repository, and infrastructure"},
        {"domain": "accessibility and security", "local_artifact_status": "bounded structural checks", "external_evidence_status": "manual and independent review missing", "decision": "veto", "reason": "no complete accessibility or exhaustive-security evidence"},
    ]
    write_json(phase / "stage20/domain-veto-evidence-board.json", {
        "schema": "ghc.family.v643-v4.stage20-board.v1",
        "phase": PHASE,
        "owner": OWNER,
        "vetoes": vetoes,
        "compensation_across_domains_allowed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })

    manifest_rows = []
    for relative in manifest_candidates(repo, phase, proposals):
        target = repo / relative
        data = normalized_bytes(target)
        manifest_rows.append({"repo_path": relative, "sha256_lf_normalized": hashlib.sha256(data).hexdigest(), "bytes_lf_normalized": len(data)})
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v643-v4.manifest.v1",
        "phase": PHASE,
        "owner": OWNER,
        "hash_algorithm": "sha256",
        "text_normalization": "CRLF and CR normalized to LF before hashing",
        "entry_count": len(manifest_rows),
        "entries": manifest_rows,
        "snapshot_state": snapshot_state,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "boundary": BOUNDARY,
    })
    return {
        "phase": PHASE,
        "proposal_count": 10,
        "case_count": 80,
        "rejections": 70,
        "distribution": distribution,
        "retained_negatives": len(negatives),
        "x1_operational_negatives": len(x1_negatives),
        "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES),
        "manifest_entries": len(manifest_rows),
        "snapshot_state": snapshot_state,
        "lifecycle": lifecycle,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    parser.add_argument("--lifecycle", choices=("evidence", "closeout", "seal", "final"), default="evidence")
    args = parser.parse_args()
    print(json.dumps(build(args.repo, args.snapshot_state, args.lifecycle), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
