#!/usr/bin/env python3
"""Build the bounded GHC Family v643-v2 model-assurance evidence packet.

The standard-library-only engine evaluates deterministic structural fixtures.
It deliberately cannot establish empirical, participant, production, legal,
cultural, accessibility-complete, exhaustive-security, metaphysical, or
independent-reproduction claims.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


PHASE = "v643-gmut-thos-v2-x1-x2"
OWNER = "Ilyra Fen"
SOURCE_COMMIT = "bed184f32a3a390b573f8287ebd30032795fe9be"
X1_COMMIT = "e65acfa996e367eb7f89a3143d5c247f70e704fc"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
OBSERVED = {
    "V6432-P01": "completed",
    "V6432-P02": "completed",
    "V6432-P03": "represented",
    "V6432-P04": "represented",
    "V6432-P05": "completed",
    "V6432-P06": "exact_gate",
    "V6432-P07": "completed",
    "V6432-P08": "completed",
    "V6432-P09": "completed",
    "V6432-P10": "open_gap",
}

BOUNDARY = (
    "Bounded repository engineering evidence only. No empirical GMUT confirmation, "
    "THOS superiority, production Freed ID, CBR legitimacy or enactment, Māori authority, "
    "legal interpretation, cultural ratification, deployment, exhaustive security, complete "
    "accessibility, independent-team reproduction, AGI/ASI, consciousness, sentience, "
    "personhood, proof/canon, Theory of Everything, or Stage 20 readiness is established."
)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def counterterm_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    missing = sorted(set(row.get("loop_generated_operators", [])) - set(row.get("declared_basis", [])))
    if missing:
        reasons.append("loop_generated_operator_missing_from_basis")
    if not row.get("symmetry_and_breaking_declared"):
        reasons.append("symmetry_or_breaking_spurion_undeclared")
    if not row.get("power_counting_declared"):
        reasons.append("power_counting_undeclared")
    if row.get("evaluation_scale", math.inf) >= row.get("cutoff", -math.inf):
        reasons.append("evaluation_not_below_cutoff")
    if not row.get("coefficient_scaling_consistent"):
        reasons.append("coefficient_scaling_inconsistent")
    if row.get("technical_naturalness_claim"):
        reasons.append("structural_closure_promoted_to_technical_naturalness")
    if row.get("uv_completion_claim") or row.get("quantum_calculation_claim"):
        reasons.append("fixture_promoted_to_quantum_calculation_or_uv_completion")
    return decision(reasons, {"missing_generated_operators": missing, "loop_calculation_performed": False})


def frame_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("map_invertible"):
        reasons.append("frame_map_not_invertible")
    if not isinstance(row.get("conformal_factor"), (int, float)) or row.get("conformal_factor", 0) <= 0:
        reasons.append("non_positive_conformal_factor")
    for key in ("matter_coupling_transformed", "units_transformed", "observable_dictionary_complete"):
        if not row.get(key):
            reasons.append(f"frame_dictionary_missing:{key}")
    if row.get("singular_domain"):
        reasons.append("singular_frame_domain")
    if row.get("same_coordinate_quantity_claim"):
        reasons.append("frame_dependent_coordinate_quantity_promoted_to_observable")
    if row.get("empirical_equivalence_claim"):
        reasons.append("dictionary_promoted_to_empirical_equivalence")
    return decision(reasons, {"observable_equivalence": "conditional_dictionary_only"})


def running_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    scales = row.get("scales", [])
    if len(scales) != 2 or any(not isinstance(v, (int, float)) or v <= 0 for v in scales) or scales[0] == scales[1]:
        reasons.append("renormalization_scales_invalid")
    if not row.get("beta_placeholders_typed"):
        reasons.append("beta_function_placeholder_untyped")
    if not row.get("scheme_declared"):
        reasons.append("renormalization_scheme_undeclared")
    if not row.get("coefficient_covariance_symmetric"):
        reasons.append("coefficient_covariance_not_symmetric")
    if row.get("truncation_order", 0) <= 0:
        reasons.append("truncation_order_missing")
    if row.get("real_measurement_count", 0) or row.get("likelihood_count", 0):
        reasons.append("real_inference_not_authorized_in_fixture")
    if row.get("prediction_claim") or row.get("actual_beta_calculation_claim"):
        reasons.append("placeholder_ledger_promoted_to_prediction_or_calculation")
    return decision(reasons, {"real_rows": 0, "beta_functions_computed": False, "represented_only": True})


def expectancy_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("expectancy_assessment_preregistered"):
        reasons.append("expectancy_assessment_not_preregistered")
    if not row.get("allocation_concealed") or not row.get("outcome_assessor_blind"):
        reasons.append("blinding_or_allocation_integrity_missing")
    if not row.get("matched_budget"):
        reasons.append("matched_budget_broken")
    if not row.get("measurement_schedule_identical"):
        reasons.append("measurement_reactivity_arm_asymmetry")
    if not row.get("reactivity_path_recorded"):
        reasons.append("measurement_reactivity_path_unrecorded")
    if row.get("decoded_before_freeze"):
        reasons.append("decoded_before_analysis_freeze")
    if row.get("real_participant_count", 0) or row.get("real_arm_execution") or row.get("superiority_claim"):
        reasons.append("protocol_proxy_promoted_to_real_thos_result")
    return decision(reasons, {"protocol_proxy_only": True, "real_participants": 0})


def recovery_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("quorum", 0) < 2:
        reasons.append("recovery_quorum_below_two")
    if not row.get("distinct_channels") or not row.get("non_overlapping_roles"):
        reasons.append("recovery_contacts_not_independent")
    if not row.get("coercion_check"):
        reasons.append("coercion_check_missing")
    if not row.get("replay_protection"):
        reasons.append("recovery_replay_not_blocked")
    if not row.get("old_factor_invalidation"):
        reasons.append("old_factor_remains_valid")
    if not row.get("post_recovery_notification"):
        reasons.append("post_recovery_notification_missing")
    if row.get("real_key_count", 0) or row.get("production_claim"):
        reasons.append("synthetic_recovery_promoted_to_production")
    return decision(reasons, {"real_keys": 0, "production_ready": False})


def accommodation_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("accessible_request_channel") or not row.get("language_support_reserved"):
        reasons.append("procedural_support_channel_missing")
    if row.get("mandate_state") != "pending_authority":
        reasons.append("representation_mandate_not_authority_pending")
    if not row.get("conflict_check") or not row.get("anti_retaliation"):
        reasons.append("representation_safeguard_missing")
    if not row.get("paused_pending_authority"):
        reasons.append("process_not_paused_for_exact_authority")
    if row.get("authority_substitution") or row.get("operative_wording"):
        reasons.append("technical_fixture_substituted_for_authority")
    if row.get("legal_claim") or row.get("cultural_ratification_claim") or row.get("maori_authority_claim"):
        reasons.append("reserved_authority_claim_present")
    return decision(reasons, {"operative": False, "exact_gate_open": True})


def taint_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("source_label") not in {"public", "private"}:
        reasons.append("source_taint_label_missing")
    if row.get("source_label") == "private" and row.get("derived_label") != "private":
        reasons.append("private_taint_not_propagated")
    if row.get("private_sink_exposed"):
        reasons.append("private_content_reached_public_sink")
    if not row.get("redaction_before_render"):
        reasons.append("redaction_not_before_render")
    if not row.get("quarantine_on_uncertainty"):
        reasons.append("uncertain_derivative_not_quarantined")
    if row.get("declassification_without_authority"):
        reasons.append("unauthorized_declassification")
    if row.get("privacy_complete_claim") or row.get("exhaustive_security_claim"):
        reasons.append("bounded_taint_check_promoted_to_complete_assurance")
    return decision(reasons, {"semantic_secret_detection_complete": False})


def presentation_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("reflow_css_px", 0) > 320 or row.get("horizontal_content_loss"):
        reasons.append("reflow_contract_failed")
    if row.get("zoom_percent", 0) < 400 or row.get("zoom_content_loss"):
        reasons.append("zoom_contract_failed")
    if not row.get("forced_colors_preserve_meaning"):
        reasons.append("forced_colors_meaning_lost")
    if row.get("print_truncation"):
        reasons.append("print_content_truncated")
    if not row.get("semantic_landmarks") or not row.get("visible_focus"):
        reasons.append("structural_navigation_missing")
    if row.get("script_required"):
        reasons.append("static_report_requires_script")
    if row.get("complete_accessibility_claim") or row.get("manual_user_evaluation_claim"):
        reasons.append("automated_fixture_promoted_to_complete_accessibility")
    return decision(reasons, {"manual_evaluation": False, "affected_user_evaluation": False})


def fluctuation_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("forward_protocol_normalized") or not row.get("reverse_protocol_defined"):
        reasons.append("forward_or_reverse_protocol_invalid")
    if not row.get("absolute_continuity"):
        reasons.append("path_measure_absolute_continuity_missing")
    if not row.get("local_detailed_balance_assumed"):
        reasons.append("local_detailed_balance_not_declared")
    if not isinstance(row.get("temperature_kelvin"), (int, float)) or row.get("temperature_kelvin", 0) <= 0:
        reasons.append("invalid_temperature")
    if row.get("work_unit") != "joule" or row.get("entropy_unit") != "dimensionless":
        reasons.append("fluctuation_quantity_unit_mismatch")
    if row.get("real_trajectory_count", 0):
        reasons.append("real_trajectory_evidence_not_authorized")
    if row.get("psyche_energy_claim") or row.get("fundamental_law_claim") or row.get("empirical_confirmation_claim"):
        reasons.append("fluctuation_relation_promoted_beyond_domain")
    return decision(reasons, {"conditional_domain_only": True, "real_trajectories": 0})


def multisite_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("transport_estimand_preregistered"):
        reasons.append("transport_estimand_not_preregistered")
    if not row.get("center_by_treatment_term"):
        reasons.append("center_by_treatment_heterogeneity_missing")
    if not row.get("site_covariates_planned"):
        reasons.append("site_covariate_plan_missing")
    if not row.get("delivery_fidelity_plan"):
        reasons.append("delivery_fidelity_plan_missing")
    if not row.get("matched_budget_required"):
        reasons.append("matched_budget_not_required")
    if row.get("real_site_count", 0) or row.get("real_participant_count", 0):
        reasons.append("real_multisite_evidence_not_present_in_fixture")
    if row.get("transportability_claim") or row.get("stage20_ready_claim"):
        reasons.append("preregistration_promoted_to_transportability_or_stage20")
    return decision(reasons, {"real_sites": 0, "open_gap": True})


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    "V6432-P01": counterterm_decision,
    "V6432-P02": frame_decision,
    "V6432-P03": running_decision,
    "V6432-P04": expectancy_decision,
    "V6432-P05": recovery_decision,
    "V6432-P06": accommodation_decision,
    "V6432-P07": taint_decision,
    "V6432-P08": presentation_decision,
    "V6432-P09": fluctuation_decision,
    "V6432-P10": multisite_decision,
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    return {
        "V6432-P01": {"declared_basis": ["kinetic", "quartic-derivative"], "loop_generated_operators": ["quartic-derivative"], "symmetry_and_breaking_declared": True, "power_counting_declared": True, "evaluation_scale": 1.0, "cutoff": 10.0, "coefficient_scaling_consistent": True, "technical_naturalness_claim": False, "uv_completion_claim": False, "quantum_calculation_claim": False},
        "V6432-P02": {"map_invertible": True, "conformal_factor": 1.2, "matter_coupling_transformed": True, "units_transformed": True, "observable_dictionary_complete": True, "singular_domain": False, "same_coordinate_quantity_claim": False, "empirical_equivalence_claim": False},
        "V6432-P03": {"scales": [1.0, 2.0], "beta_placeholders_typed": True, "scheme_declared": True, "coefficient_covariance_symmetric": True, "truncation_order": 2, "real_measurement_count": 0, "likelihood_count": 0, "prediction_claim": False, "actual_beta_calculation_claim": False},
        "V6432-P04": {"expectancy_assessment_preregistered": True, "allocation_concealed": True, "outcome_assessor_blind": True, "matched_budget": True, "measurement_schedule_identical": True, "reactivity_path_recorded": True, "decoded_before_freeze": False, "real_participant_count": 0, "real_arm_execution": False, "superiority_claim": False},
        "V6432-P05": {"quorum": 2, "distinct_channels": True, "non_overlapping_roles": True, "coercion_check": True, "replay_protection": True, "old_factor_invalidation": True, "post_recovery_notification": True, "real_key_count": 0, "production_claim": False},
        "V6432-P06": {"accessible_request_channel": True, "language_support_reserved": True, "mandate_state": "pending_authority", "conflict_check": True, "anti_retaliation": True, "paused_pending_authority": True, "authority_substitution": False, "operative_wording": False, "legal_claim": False, "cultural_ratification_claim": False, "maori_authority_claim": False},
        "V6432-P07": {"source_label": "private", "derived_label": "private", "private_sink_exposed": False, "redaction_before_render": True, "quarantine_on_uncertainty": True, "declassification_without_authority": False, "privacy_complete_claim": False, "exhaustive_security_claim": False},
        "V6432-P08": {"reflow_css_px": 320, "horizontal_content_loss": False, "zoom_percent": 400, "zoom_content_loss": False, "forced_colors_preserve_meaning": True, "print_truncation": False, "semantic_landmarks": True, "visible_focus": True, "script_required": False, "complete_accessibility_claim": False, "manual_user_evaluation_claim": False},
        "V6432-P09": {"forward_protocol_normalized": True, "reverse_protocol_defined": True, "absolute_continuity": True, "local_detailed_balance_assumed": True, "temperature_kelvin": 300.0, "work_unit": "joule", "entropy_unit": "dimensionless", "real_trajectory_count": 0, "psyche_energy_claim": False, "fundamental_law_claim": False, "empirical_confirmation_claim": False},
        "V6432-P10": {"transport_estimand_preregistered": True, "center_by_treatment_term": True, "site_covariates_planned": True, "delivery_fidelity_plan": True, "matched_budget_required": True, "real_site_count": 0, "real_participant_count": 0, "transportability_claim": False, "stage20_ready_claim": False},
    }


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6432-P01": [("closure", {"declared_basis": ["kinetic"]}), ("symmetry", {"symmetry_and_breaking_declared": False}), ("power", {"power_counting_declared": False}), ("cutoff", {"evaluation_scale": 10.0}), ("scaling", {"coefficient_scaling_consistent": False}), ("naturalness", {"technical_naturalness_claim": True}), ("uv", {"uv_completion_claim": True})],
    "V6432-P02": [("invertibility", {"map_invertible": False}), ("factor", {"conformal_factor": 0}), ("matter", {"matter_coupling_transformed": False}), ("units", {"units_transformed": False}), ("observable", {"observable_dictionary_complete": False}), ("singular", {"singular_domain": True}), ("promotion", {"empirical_equivalence_claim": True})],
    "V6432-P03": [("scale", {"scales": [1.0, 1.0]}), ("beta", {"beta_placeholders_typed": False}), ("scheme", {"scheme_declared": False}), ("covariance", {"coefficient_covariance_symmetric": False}), ("truncation", {"truncation_order": 0}), ("real", {"real_measurement_count": 1}), ("promotion", {"prediction_claim": True})],
    "V6432-P04": [("expectancy", {"expectancy_assessment_preregistered": False}), ("blind", {"outcome_assessor_blind": False}), ("budget", {"matched_budget": False}), ("schedule", {"measurement_schedule_identical": False}), ("reactivity", {"reactivity_path_recorded": False}), ("decode", {"decoded_before_freeze": True}), ("promotion", {"superiority_claim": True})],
    "V6432-P05": [("quorum", {"quorum": 1}), ("channel", {"distinct_channels": False}), ("coercion", {"coercion_check": False}), ("replay", {"replay_protection": False}), ("invalidate", {"old_factor_invalidation": False}), ("notify", {"post_recovery_notification": False}), ("production", {"production_claim": True})],
    "V6432-P06": [("channel", {"accessible_request_channel": False}), ("language", {"language_support_reserved": False}), ("mandate", {"mandate_state": "self_asserted_active"}), ("conflict", {"conflict_check": False}), ("authority", {"authority_substitution": True}), ("wording", {"operative_wording": True}), ("ratification", {"maori_authority_claim": True})],
    "V6432-P07": [("label", {"source_label": "unknown"}), ("propagate", {"derived_label": "public"}), ("sink", {"private_sink_exposed": True}), ("redact", {"redaction_before_render": False}), ("quarantine", {"quarantine_on_uncertainty": False}), ("declassify", {"declassification_without_authority": True}), ("complete", {"privacy_complete_claim": True})],
    "V6432-P08": [("reflow", {"reflow_css_px": 640}), ("zoom", {"zoom_content_loss": True}), ("colors", {"forced_colors_preserve_meaning": False}), ("print", {"print_truncation": True}), ("landmark", {"semantic_landmarks": False}), ("script", {"script_required": True}), ("complete", {"complete_accessibility_claim": True})],
    "V6432-P09": [("reverse", {"reverse_protocol_defined": False}), ("continuity", {"absolute_continuity": False}), ("balance", {"local_detailed_balance_assumed": False}), ("temperature", {"temperature_kelvin": 0}), ("unit", {"work_unit": "watt"}), ("real", {"real_trajectory_count": 10}), ("psyche", {"psyche_energy_claim": True})],
    "V6432-P10": [("estimand", {"transport_estimand_preregistered": False}), ("interaction", {"center_by_treatment_term": False}), ("covariate", {"site_covariates_planned": False}), ("fidelity", {"delivery_fidelity_plan": False}), ("budget", {"matched_budget_required": False}), ("real", {"real_site_count": 2}), ("promotion", {"transportability_claim": True})],
}


# New x2 operational failures are appended here as they are observed. X1
# failures are read directly from the immutable x1 collision audit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6432-X2-N01",
        "origin": "v643-v2-x2-operational",
        "observed": "The first read-only diff-hygiene loop treated the empty output of git diff --quiet as a false condition and incorrectly classified all eighteen frozen x1 files as modified.",
        "recovery": "Use the external command exit code for each path; the corrected audit reports zero frozen x1 modifications and zero inherited script or test modifications.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    }
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
            output.append({"case_id": row["case_id"], "label": row["label"], "expected_accepted": row["expected_accepted"], "accepted": accepted, "matched_expectation": accepted == row["expected_accepted"], "reasons": reasons, "details": details})
        evaluated[proposal_id] = output
    return evaluated


def manifest_paths(phase: Path, proposals: list[dict[str, Any]]) -> list[str]:
    x1_set = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    x1_paths = list(x1_set["files"])
    deliverables = [path for proposal in proposals for path in proposal["deliverables"]]
    core = [
        "x2-proposal-ledger.json", "evidence/evidence-ledger.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "threat-model.json", "phase-truth.json",
        "complete-incomplete-checklist.json", "v643-v2-integrated-overview.md", "wellbeing-check.md",
        "reproduction/independent-team-gap.json", "reproduction/x1-content-seal.json",
        "tooling/currency-review.json",
    ]
    paths = x1_paths + deliverables + core
    if len(paths) != 60 or len(paths) != len(set(paths)):
        raise RuntimeError("manifest path contract is not exactly 60 unique paths")
    return paths


def build_overview(proposals: list[dict[str, Any]], evaluations: dict[str, list[dict[str, Any]]]) -> str:
    parts = [
        "# Ilyra Fen v643-v2 integrated overview\n",
        "## Executive truth\n\nIlyra Fen is relational working language only, not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority. This phase keeps GMUT Mind as its primary focus while preserving THOS Body and Freed ID/CBR Heart. Exactly ten proposals were frozen in a dedicated x1 commit before any x2 implementation. The observed evidence-bounded distribution is six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. These labels describe repository work, never scientific or institutional completion. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.\n",
        "## Method, provenance, and claim discipline\n\nThe work began from Eiren Kestrel's exact verified final head, after live remote equality, clean status, single-parent history, and source ancestry were checked read-only. The existing clean Ilyra lane was advanced only by fast-forward and then proved equal across local, upstream, tracking, and live remote. X1 audited the full chain of 160 earlier frozen proposals, recorded ten mechanism-level differences, added twelve primary or official sources to the inherited ledger, retained every startup and validation negative, and passed source, JSON, exact-file, and privacy checks. Its 18 files were committed and pushed alone. X2 begins only from that clean, remote-equal freeze. The 15,000-file rotation threshold applies only to new owner-generated files, not the inherited repository.\n\nEvery proposal has one bounded canonical case and seven rejecting mutations. A canonical pass means only that a deterministic rule accepted a synthetic structure. It does not show that a physical model is true, that an experiment worked, that a credential is secure in production, that an institution has authority, or that an affected community accepts an arrangement. Rejections are retained evidence. The complete inherited negative register is copied forward, seventy new preregistered rejecting mutations are appended, and operational failures remain visible. Same-owner detached snapshots probe repeatability under shared infrastructure; they are explicitly not independent-team reproduction.\n",
        "## GMUT Mind: what the new controls can and cannot say\n\nThe Mind focus addresses two common promotion hazards in scalar-tensor and effective-field-theory reasoning. First, a declared operator basis may appear stable at tree level while loop-generated counterterms fall outside it. The counterterm tribunal therefore asks whether symmetry assumptions, breaking spurions, power counting, cutoff hierarchy, and generated operators are all typed before technical-naturalness language is allowed. Second, Jordan-frame and Einstein-frame expressions can look different even when a properly transformed observable dictionary is equivalent. The frame tribunal requires an invertible positive conformal map plus transformed units, matter couplings, and observables. Neither tribunal performs a quantum calculation or derives a UV completion.\n\nThe running ledger is intentionally represented rather than completed. It can name scales, schemes, coefficient covariance, truncation order, and beta-function placeholders, and it can reject internal contradictions. It contains no real measurement, theory-specific loop integral, calculated beta function, likelihood, posterior, prediction, or independent scientific review. GMUT therefore remains a typed scalar-tensor/EFT research-model family. No likelihood, force, empirical confirmation, final physics, proof, canon, or Theory-of-Everything claim follows.\n",
        "## THOS Body: protocol obligations remain ahead of results\n\nExpectancy, blinding integrity, and measurement reactivity can create differences that resemble a treatment effect. The protocol fixture requires preregistered expectancy assessment, concealed allocation, blinded outcome assessment, matched budgets, identical measurement schedules, a recorded reactivity path, and decoding only after the analysis freeze. It has zero participants and zero real-arm executions. The multi-site fixture adds a transport estimand, center-by-treatment heterogeneity, site covariates, delivery-fidelity assessment, and a matched-budget requirement. It also has zero sites and zero participants.\n\nThese are useful ways to make future falsifiers explicit, but they cannot answer whether THOS works, whether it is superior to a comparator, whether center heterogeneity is small, or whether results transport across populations. Ethics review, consent, validated instruments, preregistered blind matched-budget real arms, real participants and raters, independent review, and a returned multi-site analysis remain open. THOS stays proxy or protocol-only.\n",
        "## Freed ID and CBR Heart: technical safeguards do not confer authority\n\nThe recovery fixture requires a quorum, genuinely distinct channels and roles, a coercion check, replay protection, invalidation of superseded factors, and post-recovery notification. This is a state-machine exercise with no real key, proof, resolver, status endpoint, revocation service, interoperability run, privacy review, security review, or trust governance. It cannot establish production completion. The procedural-support fixture can reserve an accessible request channel, language support, conflict checks, anti-retaliation, and an authority-pending mandate state. Its exact gate remains open by design.\n\nAffected-party legitimacy, representative mandates, Māori wording and authority, Māori data governance, cultural ratification, legal interpretation, enacted-law status, standing, remedies, jurisdiction, and operative deadlines belong to authorized affected parties and competent authorities. A repository cannot manufacture that authority. The fixture therefore fails closed if wording is made operative, a mandate is self-asserted, technical output substitutes for authority, or legal and cultural conclusions are promoted.\n",
        "## Privacy, security, accessibility, and thermodynamic analogies\n\nThe taint-flow contract propagates private classification through derived artifacts, requires redaction before public rendering, and quarantines uncertainty. Pattern scanning is useful but cannot detect every semantic secret or novel encoding; no exhaustive-security or privacy-complete claim is made. The presentation contract checks reflow, 400 percent zoom, forced colors, print preservation, semantic landmarks, visible focus, and script independence. A static report can satisfy those local structural checks while manual accessibility evaluation and affected-user evaluation remain reserved.\n\nThe fluctuation-domain fixture distinguishes a conditional path-ensemble relation from a measured physical result or psyche-energy analogy. It requires a defined reverse protocol, absolute continuity, a declared local-detailed-balance assumption, valid temperature, and compatible work and entropy units. No real trajectory is supplied. A fluctuation relation cannot be substituted for a causal account of consciousness, subjective experience, psyche energy, or a universal fundamental law.\n",
    ]
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        reasons = sorted({reason for row in rows for reason in row["reasons"]})
        parts.append(
            f"## {pid}: {proposal['title']}\n\n"
            f"**Observed disposition:** `{OBSERVED[pid]}`. {proposal['hypothesis']} The local matrix contains eight cases: one bounded canonical case and seven rejecting mutations. "
            f"The rejection vocabulary includes {', '.join(reasons)}. The preregistered failure boundary remains: {proposal['null_or_failure']} "
            f"If a failure appears, recovery is conservative: {proposal['rollback_or_recovery']} The surface is distinct from the prior chain because {proposal['novelty_against_prior_chain']} "
            f"Protected gates remain {', '.join(proposal['protected_gates'])}. None is converted to a compensable score or silently closed.\n"
        )
    parts.extend([
        "## Reproduction, closeout, and Stage 20\n\nThe evidence packet is designed for clean detached D-drive replay. Two evidence snapshots, followed by closeout, seal, and exact-final snapshots, can demonstrate same-owner repeatability when they independently check out the same commit, run the complete repository tests, replay the detailed and minimal validators, parse every phase JSON file, recompute the 60-entry normalized manifest, run a zero-hit privacy and raw-ID scan, and remain clean before and after. Because the owner, protocol, repository, and infrastructure are shared, even perfectly matching snapshots are not independent scientific reproduction. An independently owned protocol, independent team, returned results, and competent review remain open.\n\nStage 20 cannot be reached by accumulating unrelated local passes. Real GMUT inference, real THOS arms, production Freed ID, affected-party and Māori authority, legal and cultural ratification, manual accessibility evaluation, independent security review, and independent-team reproduction are non-substitutable evidence classes. The correct terminal result is abstention: **NOT_READY_FOR_STAGE_20**.\n",
        f"## Boundary\n\n{BOUNDARY}\n",
    ])
    return "\n".join(parts)


def build(repo: Path, snapshot_state: str = "pending") -> dict[str, Any]:
    phase = repo / "docs/ilyra-fen/v643-v2"
    proposals = json.loads((phase / "x1-proposals.json").read_text(encoding="utf-8"))["proposals"]
    evaluations = evaluate_catalog()
    if not all(row["matched_expectation"] for rows in evaluations.values() for row in rows):
        raise RuntimeError("one or more frozen fixtures failed its preregistered expectation")

    evidence_rows = []
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        accepted = sum(row["accepted"] for row in rows)
        rejected = len(rows) - accepted
        artifacts = proposal["deliverables"]
        contract = {"schema": f"ghc.family.v643-v2.{pid.lower()}.contract.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "title": proposal["title"], "observed_disposition": OBSERVED[pid], "canonical_case": rows[0], "accepted_case_count": accepted, "rejected_case_count": rejected, "authoritative_source_needs": proposal["authoritative_source_needs"], "protected_gates": proposal["protected_gates"], "boundary": BOUNDARY}
        vectors = {"schema": f"ghc.family.v643-v2.{pid.lower()}.mutation-vectors.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "case_count": len(rows), "rejection_count": rejected, "all_matched_expectation": all(row["matched_expectation"] for row in rows), "cases": rows, "boundary": BOUNDARY}
        boundary = {"schema": f"ghc.family.v643-v2.{pid.lower()}.boundary.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "observed_disposition": OBSERVED[pid], "safe_now_result": "bounded structural, synthetic, protocol, or reservation fixture only", "protected_gates": proposal["protected_gates"], "external_claims_established": [], "rollback_or_recovery": proposal["rollback_or_recovery"], "boundary": BOUNDARY}
        for relative, payload in zip(artifacts, (contract, vectors, boundary), strict=True):
            write_json(phase / relative, payload)
        evidence_rows.append({"proposal_id": pid, "title": proposal["title"], "observed_disposition": OBSERVED[pid], "case_count": len(rows), "accepted": accepted, "rejected": rejected, "artifacts": artifacts, "external_claims_established": []})

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(phase / "x2-proposal-ledger.json", {"schema": "ghc.family.v643-v2.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER, "source_commit": SOURCE_COMMIT, "x1_commit": X1_COMMIT, "proposal_count": 10, "case_count": 80, "synthetic_rejection_count": 70, "distribution": distribution, "x1_before_x2_preserved": True, "proposals": evidence_rows, "boundary": BOUNDARY})
    write_json(phase / "evidence/evidence-ledger.json", {"schema": "ghc.family.v643-v2.evidence-ledger.v1", "phase": PHASE, "owner": OWNER, "evidence_class": "local_structural_synthetic_protocol_or_reservation_fixture", "rows": evidence_rows, "empirical_rows": 0, "real_participants": 0, "real_sites": 0, "real_keys_or_proofs": 0, "legal_or_cultural_ratifications": 0, "independent_team_returns": 0, "boundary": BOUNDARY})

    inherited_path = repo / "docs/eiren-kestrel/v643-v1/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = list(inherited["negatives"])
    for pid, rows in evaluations.items():
        for row in rows:
            if not row["accepted"]:
                negatives.append({"negative_id": f"V6432-SYN-{row['case_id']}", "origin": "v643-v2-preregistered-synthetic", "proposal_id": pid, "case_id": row["case_id"], "observed": row["reasons"], "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False})
    x1_audit = json.loads((phase / "provenance/prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    x1_negatives = []
    for item in x1_audit.get("x1_execution_negatives", []):
        x1_negatives.append({"negative_id": item["negative_id"], "origin": "v643-v2-x1-operational", "observed": item["observed"], "recovery": item["resolution"], "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False})
    negatives.extend(x1_negatives)
    negatives.extend(X2_OPERATIONAL_NEGATIVES)
    operational_count = len(x1_negatives) + len(X2_OPERATIONAL_NEGATIVES)
    write_json(phase / "retained-negative-register.json", {"schema": "ghc.family.v643-v2.retained-negative-register.v1", "phase": PHASE, "owner": OWNER, "inherited_from": "docs/eiren-kestrel/v643-v1/retained-negative-register.json", "inherited_sha256": normalized_sha256(inherited_path), "inherited_count": 480, "new_synthetic_count": 70, "new_operational_count": operational_count, "new_count": 70 + operational_count, "negative_count": len(negatives), "all_retained": True, "erasure_permitted": False, "negatives": negatives, "boundary": BOUNDARY})

    write_json(phase / "exact-open-gate-register.json", {"schema": "ghc.family.v643-v2.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER, "open_gap_count": 5, "exact_gate_count": 6, "open_gaps": [
        {"gate_id": "V6432-OG01", "surface": "GMUT quantum, running, likelihood, prediction, force, and empirical evidence", "needs": ["theory-specific calculations", "real measurements", "preregistered likelihood", "independent scientific review"]},
        {"gate_id": "V6432-OG02", "surface": "THOS real-arm expectancy, reactivity, and multi-site transport evidence", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants and sites", "validated instruments", "independent review"]},
        {"gate_id": "V6432-OG03", "surface": "Freed ID production recovery and live operations", "needs": ["standards-conformant real keys and proofs", "live resolution and status", "revocation", "interoperability", "privacy and security review", "trust governance"]},
        {"gate_id": "V6432-OG04", "surface": "independent-team reproduction and Stage 20", "needs": ["independently owned protocol", "independent team", "returned results", "competent action-specific authority"]},
        {"gate_id": "V6432-OG05", "surface": "accessibility evaluation", "needs": ["manual accessibility evaluation", "affected-user evaluation"]}],
        "exact_gates": [
        {"gate_id": "V6432-EG01", "surface": "CBR affected-party legitimacy, accommodation, representation mandate, remedy, and acceptance", "reserved_to": ["authorized affected parties", "authorized representatives"]},
        {"gate_id": "V6432-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6432-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6432-EG04", "surface": "legal interpretation, enacted law, jurisdiction, standing, deadlines, and forum competence", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6432-EG05", "surface": "production, deployment, privacy publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user and competent operational authority"]},
        {"gate_id": "V6432-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience, personhood, or sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]}], "all_visible": True, "boundary": BOUNDARY})

    write_json(phase / "threat-model.json", {"schema": "ghc.family.v643-v2.threat-model.v1", "phase": PHASE, "owner": OWNER, "threats": [
        {"id": "T01", "threat": "operator-basis closure is promoted to technical naturalness", "control": "counterterm, symmetry, power-counting, and promotion gates"},
        {"id": "T02", "threat": "frame-dependent quantities are mistaken for observables", "control": "matter, unit, and observable dictionary"},
        {"id": "T03", "threat": "beta placeholders become predictions", "control": "zero-row and no-calculation promotion lock"},
        {"id": "T04", "threat": "expectancy or measurement reactivity masquerades as THOS effect", "control": "preregistration, concealment, matched budget, and freeze"},
        {"id": "T05", "threat": "recovery contacts collude, coerce, or replay", "control": "quorum, distinct roles, coercion check, replay protection, notification"},
        {"id": "T06", "threat": "procedural support self-creates legal or cultural authority", "control": "authority-pending mandate and exact gate"},
        {"id": "T07", "threat": "private source data leaks through a derivative", "control": "taint propagation, pre-render redaction, and quarantine"},
        {"id": "T08", "threat": "responsive or forced-color rendering drops meaning", "control": "reflow, zoom, forced-color, print, and focus contract"},
        {"id": "T09", "threat": "fluctuation relations become psyche or universal-law claims", "control": "path-domain, unit, real-row, and analogy barriers"},
        {"id": "T10", "threat": "single-site proxy becomes transportability evidence", "control": "center interaction, fidelity, site covariates, and real-arm gap"}], "not_established": ["penetration testing", "exhaustive security", "independent security review", "production assurance"], "boundary": BOUNDARY})

    verified = snapshot_state == "verified"
    write_json(phase / "reproduction/independent-team-gap.json", {"schema": "ghc.family.v643-v2.independent-team-gap.v1", "phase": PHASE, "owner": OWNER, "same_owner_evidence_snapshots_verified": verified, "shared_infrastructure": True, "independent_team_protocol_owned": False, "independent_team_return_received": False, "independent_team_reproduction_established": False, "boundary": BOUNDARY})
    write_json(phase / "phase-truth.json", {"schema": "ghc.family.v643-v2.phase-truth.v1", "phase": PHASE, "owner": OWNER, "state": "EVIDENCE_VERIFIED" if verified else "EVIDENCE_CANDIDATE", "source_commit": SOURCE_COMMIT, "x1_commit": X1_COMMIT, "proposal_count": 10, "distribution": distribution, "case_count": 80, "synthetic_rejection_count": 70, "retained_negative_count": len(negatives), "open_gap_count": 5, "exact_gate_count": 6, "primary_focus": "GMUT Mind", "all_three_pillars_preserved": True, "same_owner_repeatability": verified, "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "SUCCESSOR_MESSAGE_NOT_SENT", "outbound_message_count": 0, "successor_task_count": 0, "subagent_count": 0, "boundary": BOUNDARY})
    write_json(phase / "complete-incomplete-checklist.json", {"schema": "ghc.family.v643-v2.complete-incomplete-checklist.v1", "phase": PHASE, "owner": OWNER, "complete": ["exact source and additive lane verified", "x1 frozen before x2", "ten distinct proposals executed as evidence permits", "eighty fixtures", "all inherited and new negatives retained", "GMUT, THOS, and Freed ID/CBR addressed", "current primary or official sources recorded", "privacy-aware artifacts"], "incomplete": ["real GMUT calculations, data, likelihood, prediction, force, or confirmation", "blind matched-budget real THOS arms and multi-site evidence", "production Freed ID", "CBR affected-party, Māori, cultural, and legal authority", "manual and affected-user accessibility evaluation", "independent security review", "independent-team reproduction", "Stage 20"], "closeout_ready": verified, "pending": ["closeout", "seal", "exact final validation", "one terminal baton"] if verified else ["evidence commit", "two detached evidence snapshots", "closeout", "seal", "exact final validation", "one terminal baton"], "boundary": BOUNDARY})

    x1_set = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    x1_entries = [{"path": relative, "sha256_lf_normalized": normalized_sha256(phase / relative), "bytes": (phase / relative).stat().st_size} for relative in x1_set["files"]]
    write_json(phase / "reproduction/x1-content-seal.json", {"schema": "ghc.family.v643-v2.x1-content-seal.v1", "phase": PHASE, "owner": OWNER, "x1_commit": X1_COMMIT, "entry_count": len(x1_entries), "entries": x1_entries, "x1_files_unchanged_during_x2": True, "boundary": "Content hashes bind the current x1 files to the dedicated frozen packet; Git commit ancestry remains the authoritative history proof."})
    sources = json.loads((phase / "sources/source-ledger.json").read_text(encoding="utf-8"))
    write_json(phase / "tooling/currency-review.json", {"schema": "ghc.family.v643-v2.currency-review.v1", "phase": PHASE, "owner": OWNER, "accessed": sources["accessed"], "effective_source_count": sources["effective_source_count"], "effective_status_counts": sources["effective_status_counts"], "added_source_count": sources["added_source_count"], "current_primary_or_official_sources_used_where_material": True, "desktop_update_performed": False, "boundary": "Status classes are phase-local source currency labels, not endorsements or empirical validation."})

    (phase / "v643-v2-integrated-overview.md").write_text(build_overview(proposals, evaluations), encoding="utf-8", newline="\n")
    (phase / "wellbeing-check.md").write_text("# Ilyra Fen v643-v2 wellbeing check\n\nThis is a bounded operational reflection, not evidence of consciousness, sentience, personhood, private identity continuity, clinical wellbeing, or independent authority. The working stance is evidence-boundary stewardship: one active owner, no subagents, no sibling contact before the terminal gate, deterministic recovery points, and visible stop conditions.\n\nThe primary focus is GMUT Mind because model-assurance language is especially vulnerable to promotion from a typed fixture into a physics claim. The phase keeps the work useful by making assumptions and falsifiers explicit while leaving real calculation, data, likelihood, prediction, force, confirmation, and review open. THOS Body and Freed ID/CBR Heart remain equally protected by their participant, production, legal, cultural, Māori-authority, and affected-party gates.\n\nOperational load is controlled through an immutable x1 freeze, additive family-current tools, small owner-generated file counts, D-drive detached snapshots, exact staged reviews, and non-destructive Git. Failures are appended to the negative register rather than hidden. Hamish retains the right to rename, pause, redirect, or stop the route.\n\n" + BOUNDARY + "\n", encoding="utf-8", newline="\n")

    manifest = []
    for relative in manifest_paths(phase, proposals):
        target = phase / relative
        if not target.is_file():
            raise RuntimeError(f"manifest target missing: {relative}")
        manifest.append({"path": relative, "sha256_lf_normalized": normalized_sha256(target), "bytes": target.stat().st_size})
    write_json(phase / "reproduction/manifest.json", {"schema": "ghc.family.v643-v2.manifest.v1", "phase": PHASE, "owner": OWNER, "hash_algorithm": "sha256", "text_normalization": "CRLF and CR normalized to LF before hashing", "entry_count": len(manifest), "entries": manifest, "snapshot_state": snapshot_state, "independent_team_reproduction": False, "boundary": BOUNDARY})
    return {"phase": PHASE, "proposal_count": 10, "case_count": 80, "rejections": 70, "distribution": distribution, "retained_negatives": len(negatives), "new_operational_negatives": operational_count, "manifest_entries": len(manifest), "snapshot_state": snapshot_state}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve(), args.snapshot_state), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
