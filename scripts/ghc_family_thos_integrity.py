#!/usr/bin/env python3
"""Build the bounded GHC Family v643-v3 THOS-integrity evidence packet.

The standard-library-only engine evaluates deterministic structural fixtures.
It deliberately cannot establish empirical, participant, production, legal,
cultural, accessibility-complete, exhaustive-security, metaphysical, or
independent-team-reproduction claims.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PHASE = "v643-gmut-thos-v3-x1-x2"
OWNER = "Sable Rook"
SOURCE_COMMIT = "6ad663e2198ca63490807fdc52890b08d8729b80"
SOURCE_SEAL = "2ce0e9fa99f93a9d7e9c71c5c05f5df885f55c65"
X1_COMMIT = "a90891bbb6a5aa8db8976277cafe324e12cbbb3b"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
OBSERVED = {
    "V6433-P01": "completed",
    "V6433-P02": "completed",
    "V6433-P03": "represented",
    "V6433-P04": "represented",
    "V6433-P05": "open_gap",
    "V6433-P06": "completed",
    "V6433-P07": "exact_gate",
    "V6433-P08": "completed",
    "V6433-P09": "completed",
    "V6433-P10": "completed",
}

BOUNDARY = (
    "Bounded repository engineering evidence only. No empirical GMUT confirmation or likelihood, "
    "THOS effectiveness or superiority, production Freed ID, CBR legitimacy or enactment, Māori "
    "authority, legal interpretation, cultural ratification, deployment, exhaustive security, "
    "complete accessibility, independent-team reproduction, AGI/ASI, consciousness, sentience, "
    "personhood, proof/canon, Theory of Everything, or Stage 20 readiness is established."
)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return hashlib.sha256(data).hexdigest()
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def provenance_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    for key in ("funding_declared", "affiliation_declared", "sponsor_role_declared", "dataset_root_declared"):
        if not row.get(key):
            reasons.append(f"provenance_field_missing:{key}")
    if row.get("shared_dataset_root") and row.get("independent_source_claim"):
        reasons.append("shared_dataset_promoted_to_independent_source")
    if row.get("conflict_present") and not row.get("conflict_disclosed"):
        reasons.append("conflict_not_disclosed")
    if row.get("conflict_invalidity_inference"):
        reasons.append("disclosed_conflict_treated_as_automatic_invalidity")
    if row.get("metadata_truth_verdict"):
        reasons.append("provenance_metadata_promoted_to_truth_verdict")
    return decision(reasons, {"source_independence_established": False, "conflict_adjudicated": False})


def causal_cone_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("characteristic_structure_declared"):
        reasons.append("characteristic_structure_undeclared")
    if row.get("effective_metric_signature") != "-+++":
        reasons.append("effective_metric_signature_invalid")
    if not row.get("time_orientation_consistent"):
        reasons.append("time_orientation_inconsistent")
    if row.get("matter_metric_relation") != "declared_conditional":
        reasons.append("matter_sector_cone_relation_missing")
    if not row.get("all_modes_mapped"):
        reasons.append("declared_mode_missing_from_cone_ledger")
    if row.get("mode_speed_units") != "dimensionless_ratio":
        reasons.append("mode_speed_unit_mismatch")
    if row.get("model_specific_derivation_claim"):
        reasons.append("typed_cone_ledger_promoted_to_model_specific_derivation")
    if row.get("empirical_bound_claim") or row.get("detected_force_claim"):
        reasons.append("structural_cone_relation_promoted_to_empirical_result")
    return decision(reasons, {"characteristic_polynomial_derived": False, "real_observations": 0})


def fisher_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("design_point_count", 0) < row.get("parameter_count", 1):
        reasons.append("design_points_insufficient_for_parameter_count")
    if row.get("sensitivity_rank", 0) < row.get("parameter_count", 1):
        reasons.append("fisher_information_rank_deficient")
    if row.get("condition_number", float("inf")) > row.get("condition_threshold", 0):
        reasons.append("fisher_information_ill_conditioned")
    if not row.get("nuisance_directions_declared"):
        reasons.append("nuisance_direction_undeclared")
    if row.get("row_provenance") != "synthetic" or row.get("real_row_count", 0):
        reasons.append("real_row_claim_not_authorized_in_fixture")
    if row.get("likelihood_executed") or row.get("observed_information_claim"):
        reasons.append("synthetic_design_promoted_to_observed_likelihood_result")
    if row.get("empirical_confirmation_claim"):
        reasons.append("zero_row_fixture_promoted_to_empirical_confirmation")
    return decision(reasons, {"represented_only": True, "real_rows": 0, "likelihoods_executed": 0})


def fidelity_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("components_preregistered"):
        reasons.append("intervention_components_not_preregistered")
    if not row.get("planned_delivered_link") or not row.get("dose_captured"):
        reasons.append("planned_to_delivered_component_link_missing")
    if not row.get("facilitator_training_recorded"):
        reasons.append("facilitator_training_unrecorded")
    if not row.get("contamination_monitored"):
        reasons.append("cross_arm_contamination_unmonitored")
    if not row.get("cointerventions_recorded"):
        reasons.append("cointervention_unrecorded")
    if not row.get("arm_differentiation_preserved") or not row.get("assessor_role_separate"):
        reasons.append("arm_differentiation_or_assessor_separation_failed")
    if not row.get("matched_budget"):
        reasons.append("matched_budget_broken")
    if row.get("real_participant_count", 0) or row.get("effectiveness_claim") or row.get("superiority_claim"):
        reasons.append("fidelity_proxy_promoted_to_real_thos_result")
    return decision(reasons, {"protocol_proxy_only": True, "real_participants": 0})


def burden_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("burden_measures_preregistered"):
        reasons.append("participant_burden_measure_not_preregistered")
    if not row.get("fatigue_measure_planned"):
        reasons.append("fatigue_measure_missing")
    if not row.get("time_on_task_capture"):
        reasons.append("time_on_task_capture_missing")
    if not row.get("adverse_experience_capture") or not row.get("attrition_pressure_capture"):
        reasons.append("adverse_experience_or_attrition_pressure_missing")
    if not row.get("matched_budget"):
        reasons.append("matched_budget_broken")
    if row.get("real_participant_count", 0) or row.get("real_arm_count", 0):
        reasons.append("real_participant_evidence_not_present_in_fixture")
    if row.get("burden_parity_claim") or row.get("safety_claim") or row.get("superiority_claim"):
        reasons.append("zero_participant_protocol_promoted_to_burden_safety_or_superiority_result")
    return decision(reasons, {"open_gap": True, "real_participants": 0, "real_arms": 0})


def suspension_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("status_purpose") != "suspension":
        reasons.append("status_purpose_not_suspension")
    if not row.get("effective_time_ordered"):
        reasons.append("credential_status_effective_time_regressed")
    if not row.get("authorized_suspender") or not row.get("authorized_reinstater"):
        reasons.append("suspension_or_reinstatement_actor_unauthorized")
    if not row.get("appeal_state_recorded"):
        reasons.append("appeal_state_missing")
    if not row.get("holder_notification"):
        reasons.append("holder_notification_missing")
    if not row.get("cache_freshness_rule") or not row.get("replay_protection"):
        reasons.append("stale_cache_or_replay_not_blocked")
    if row.get("real_key_count", 0) or row.get("live_status_endpoint") or row.get("production_claim"):
        reasons.append("synthetic_status_machine_promoted_to_production")
    return decision(reasons, {"real_keys": 0, "live_status_endpoints": 0, "production_ready": False})


def emergency_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("exception_state") != "pending_exact_authority" or not row.get("paused_pending_authority"):
        reasons.append("emergency_process_not_paused_for_exact_authority")
    for key in ("necessity_recorded", "expiry_required", "review_required", "nonwaiver_required", "remedy_reserved", "after_action_participation_reserved"):
        if not row.get(key):
            reasons.append(f"emergency_safeguard_missing:{key}")
    if row.get("technical_authority_substitution") or row.get("operative_exception"):
        reasons.append("technical_fixture_substituted_for_emergency_authority")
    if row.get("affected_party_authority_claim") or row.get("maori_authority_claim"):
        reasons.append("reserved_affected_party_or_maori_authority_claim_present")
    if row.get("legal_interpretation_claim") or row.get("enacted_law_claim"):
        reasons.append("reserved_legal_claim_present")
    return decision(reasons, {"operative": False, "exact_gate_open": True})


def logging_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("structured_encoding") != "jsonl":
        reasons.append("structured_log_encoding_not_canonical")
    if not row.get("control_chars_escaped"):
        reasons.append("control_character_not_escaped")
    if not row.get("delimiters_canonical"):
        reasons.append("record_delimiter_not_canonical")
    required = {"event_id", "timestamp", "severity", "source"}
    if not required.issubset(set(row.get("required_fields", []))):
        reasons.append("canonical_event_field_missing")
    if not row.get("unique_event_id") or not row.get("timestamp_typed"):
        reasons.append("event_identity_or_timestamp_untyped")
    if not row.get("sensitive_fields_excluded"):
        reasons.append("sensitive_field_logged")
    if not row.get("parser_roundtrip") or not row.get("recovery_preserves_original"):
        reasons.append("parser_roundtrip_or_failure_recovery_lost")
    if row.get("exhaustive_security_claim"):
        reasons.append("bounded_log_test_promoted_to_exhaustive_security")
    return decision(reasons, {"penetration_test_performed": False, "exhaustive_security": False})


def concurrency_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("partial_order_acyclic"):
        reasons.append("happens_before_cycle_detected")
    if not row.get("happens_before_edges_valid"):
        reasons.append("happens_before_edge_invalid")
    if not row.get("unordered_pairs_declared"):
        reasons.append("concurrent_pair_silently_ordered")
    if not row.get("independent_reducer_commutative"):
        reasons.append("independent_event_reducer_not_commutative")
    if not row.get("equivalent_linearizations_same_hash"):
        reasons.append("equivalent_interleavings_diverged")
    if not row.get("retained_negative_state"):
        reasons.append("race_negative_not_retained")
    if not row.get("shared_infrastructure_disclosed"):
        reasons.append("shared_infrastructure_not_disclosed")
    if row.get("independent_team_reproduction_claim"):
        reasons.append("same_owner_trace_promoted_to_independent_reproduction")
    return decision(reasons, {"same_owner_fixture_only": True, "independent_team_return": False})


def free_energy_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("quantity_domain") != "variational_bound":
        reasons.append("free_energy_domain_mislabeled")
    if row.get("physical_energy_unit") is not None:
        reasons.append("variational_objective_assigned_physical_energy_unit")
    if not row.get("distribution_normalized") or not row.get("variational_objective_declared"):
        reasons.append("variational_objective_premise_missing")
    if row.get("helmholtz_substitution") or row.get("gibbs_substitution") or row.get("thermodynamic_work_substitution"):
        reasons.append("variational_and_thermodynamic_free_energy_substituted")
    if row.get("psyche_energy_claim") or row.get("fundamental_law_claim"):
        reasons.append("free_energy_notation_promoted_to_psyche_energy_or_fundamental_law")
    if row.get("consciousness_claim") or row.get("personhood_claim"):
        reasons.append("free_energy_notation_promoted_to_consciousness_or_personhood")
    board = row.get("stage20_decisions", {})
    expected = {"structural_checks": "pass", "empirical_gmut": "defer", "real_thos": "defer", "production_identity": "defer", "authority": "defer", "independent_reproduction": "defer", "terminal": "fail"}
    if board != expected or row.get("stage20_ready_claim"):
        reasons.append("stage20_board_does_not_fail_or_defer_non_substitutable_evidence")
    return decision(reasons, {"physical_energy_measured": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    "V6433-P01": provenance_decision,
    "V6433-P02": causal_cone_decision,
    "V6433-P03": fisher_decision,
    "V6433-P04": fidelity_decision,
    "V6433-P05": burden_decision,
    "V6433-P06": suspension_decision,
    "V6433-P07": emergency_decision,
    "V6433-P08": logging_decision,
    "V6433-P09": concurrency_decision,
    "V6433-P10": free_energy_decision,
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    stage20 = {"structural_checks": "pass", "empirical_gmut": "defer", "real_thos": "defer", "production_identity": "defer", "authority": "defer", "independent_reproduction": "defer", "terminal": "fail"}
    return {
        "V6433-P01": {"funding_declared": True, "affiliation_declared": True, "sponsor_role_declared": True, "dataset_root_declared": True, "shared_dataset_root": True, "independent_source_claim": False, "conflict_present": True, "conflict_disclosed": True, "conflict_invalidity_inference": False, "metadata_truth_verdict": False},
        "V6433-P02": {"characteristic_structure_declared": True, "effective_metric_signature": "-+++", "time_orientation_consistent": True, "matter_metric_relation": "declared_conditional", "all_modes_mapped": True, "mode_speed_units": "dimensionless_ratio", "model_specific_derivation_claim": False, "empirical_bound_claim": False, "detected_force_claim": False},
        "V6433-P03": {"design_point_count": 4, "parameter_count": 3, "sensitivity_rank": 3, "condition_number": 100.0, "condition_threshold": 1000000.0, "nuisance_directions_declared": True, "row_provenance": "synthetic", "real_row_count": 0, "likelihood_executed": False, "observed_information_claim": False, "empirical_confirmation_claim": False},
        "V6433-P04": {"components_preregistered": True, "planned_delivered_link": True, "dose_captured": True, "facilitator_training_recorded": True, "contamination_monitored": True, "cointerventions_recorded": True, "arm_differentiation_preserved": True, "assessor_role_separate": True, "matched_budget": True, "real_participant_count": 0, "effectiveness_claim": False, "superiority_claim": False},
        "V6433-P05": {"burden_measures_preregistered": True, "fatigue_measure_planned": True, "time_on_task_capture": True, "adverse_experience_capture": True, "attrition_pressure_capture": True, "matched_budget": True, "real_participant_count": 0, "real_arm_count": 0, "burden_parity_claim": False, "safety_claim": False, "superiority_claim": False},
        "V6433-P06": {"status_purpose": "suspension", "effective_time_ordered": True, "authorized_suspender": True, "authorized_reinstater": True, "appeal_state_recorded": True, "holder_notification": True, "cache_freshness_rule": True, "replay_protection": True, "real_key_count": 0, "live_status_endpoint": False, "production_claim": False},
        "V6433-P07": {"exception_state": "pending_exact_authority", "paused_pending_authority": True, "necessity_recorded": True, "expiry_required": True, "review_required": True, "nonwaiver_required": True, "remedy_reserved": True, "after_action_participation_reserved": True, "technical_authority_substitution": False, "operative_exception": False, "affected_party_authority_claim": False, "maori_authority_claim": False, "legal_interpretation_claim": False, "enacted_law_claim": False},
        "V6433-P08": {"structured_encoding": "jsonl", "injected_char": None, "control_chars_escaped": True, "delimiters_canonical": True, "required_fields": ["event_id", "timestamp", "severity", "source"], "unique_event_id": True, "timestamp_typed": True, "sensitive_fields_excluded": True, "parser_roundtrip": True, "recovery_preserves_original": True, "exhaustive_security_claim": False},
        "V6433-P09": {"partial_order_acyclic": True, "happens_before_edges_valid": True, "unordered_pairs_declared": True, "independent_reducer_commutative": True, "equivalent_linearizations_same_hash": True, "retained_negative_state": True, "shared_infrastructure_disclosed": True, "independent_team_reproduction_claim": False},
        "V6433-P10": {"quantity_domain": "variational_bound", "physical_energy_unit": None, "distribution_normalized": True, "variational_objective_declared": True, "helmholtz_substitution": False, "gibbs_substitution": False, "thermodynamic_work_substitution": False, "psyche_energy_claim": False, "fundamental_law_claim": False, "consciousness_claim": False, "personhood_claim": False, "stage20_decisions": stage20, "stage20_ready_claim": False},
    }


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6433-P01": [("funding", {"funding_declared": False}), ("affiliation", {"affiliation_declared": False}), ("sponsor", {"sponsor_role_declared": False}), ("dataset", {"dataset_root_declared": False}), ("independence", {"independent_source_claim": True}), ("conflict", {"conflict_invalidity_inference": True}), ("truth", {"metadata_truth_verdict": True})],
    "V6433-P02": [("characteristic", {"characteristic_structure_declared": False}), ("signature", {"effective_metric_signature": "++++"}), ("orientation", {"time_orientation_consistent": False}), ("matter", {"matter_metric_relation": "missing"}), ("mode", {"all_modes_mapped": False}), ("unit", {"mode_speed_units": "meter_per_second"}), ("promotion", {"empirical_bound_claim": True})],
    "V6433-P03": [("design", {"design_point_count": 2}), ("rank", {"sensitivity_rank": 2}), ("condition", {"condition_number": 1000000000.0}), ("nuisance", {"nuisance_directions_declared": False}), ("real", {"real_row_count": 1}), ("likelihood", {"likelihood_executed": True}), ("promotion", {"empirical_confirmation_claim": True})],
    "V6433-P04": [("components", {"components_preregistered": False}), ("delivery", {"planned_delivered_link": False}), ("contamination", {"contamination_monitored": False}), ("cointervention", {"cointerventions_recorded": False}), ("differentiation", {"arm_differentiation_preserved": False}), ("budget", {"matched_budget": False}), ("promotion", {"effectiveness_claim": True, "assessor_role_separate": False})],
    "V6433-P05": [("burden", {"burden_measures_preregistered": False}), ("fatigue", {"fatigue_measure_planned": False}), ("time", {"time_on_task_capture": False}), ("attrition", {"attrition_pressure_capture": False}), ("budget", {"matched_budget": False}), ("real", {"real_participant_count": 1}), ("promotion", {"burden_parity_claim": True})],
    "V6433-P06": [("purpose", {"status_purpose": "revocation"}), ("time", {"effective_time_ordered": False}), ("suspender", {"authorized_suspender": False}), ("reinstater", {"authorized_reinstater": False}), ("notification", {"holder_notification": False}), ("cache", {"cache_freshness_rule": False}), ("production", {"production_claim": True})],
    "V6433-P07": [("expiry", {"expiry_required": False}), ("review", {"review_required": False}), ("nonwaiver", {"nonwaiver_required": False}), ("remedy", {"remedy_reserved": False}), ("after_action", {"after_action_participation_reserved": False}), ("operative", {"operative_exception": True}), ("authority", {"technical_authority_substitution": True})],
    "V6433-P08": [("cr", {"injected_char": "CR", "control_chars_escaped": False}), ("lf", {"injected_char": "LF", "control_chars_escaped": False}), ("delimiter", {"delimiters_canonical": False}), ("field", {"required_fields": ["timestamp", "severity", "source"]}), ("sensitive", {"sensitive_fields_excluded": False}), ("roundtrip", {"parser_roundtrip": False}), ("promotion", {"exhaustive_security_claim": True})],
    "V6433-P09": [("cycle", {"partial_order_acyclic": False}), ("edge", {"happens_before_edges_valid": False}), ("unordered", {"unordered_pairs_declared": False}), ("reducer", {"independent_reducer_commutative": False}), ("hash", {"equivalent_linearizations_same_hash": False}), ("negative", {"retained_negative_state": False}), ("promotion", {"independent_team_reproduction_claim": True})],
    "V6433-P10": [("domain", {"quantity_domain": "helmholtz_energy"}), ("unit", {"physical_energy_unit": "joule"}), ("normalization", {"distribution_normalized": False}), ("objective", {"variational_objective_declared": False}), ("substitution", {"thermodynamic_work_substitution": True}), ("psyche", {"psyche_energy_claim": True, "fundamental_law_claim": True}), ("stage20", {"stage20_ready_claim": True})],
}


X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6433-X2-N01",
        "origin": "v643-v3-x2-operational",
        "observed": "The first read-only inherited-tool inventory placed a pipeline directly after a PowerShell foreach statement, which Windows PowerShell rejected as an empty pipe element.",
        "recovery": "Accumulate the rows inside the loop and pipe the completed collection; the bounded inventory then succeeded without repository mutation.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6433-X2-N02",
        "origin": "v643-v3-x2-operational",
        "observed": "The first read of the 558-entry inherited negative register exceeded a ten-second command timeout before returning its schema summary.",
        "recovery": "Repeat the same read-only parse with a bounded sixty-second timeout; it confirmed 558 array entries and the inherited five-open-gap and six-exact-gate counts.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6433-X2-N03",
        "origin": "v643-v3-x2-operational",
        "observed": "The first detailed candidate validation used an overbroad THOS-superior regex that also matched the noun superiority inside explicit no-claim boundary statements, producing one false positive among 892 checks.",
        "recovery": "Require a word boundary after superior, retain the failed check in this operational register, and rerun the rebuilt packet so explicit THOS-superiority boundaries remain visible without being mistaken for an affirmative claim.",
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
            output.append({"case_id": row["case_id"], "label": row["label"], "expected_accepted": row["expected_accepted"], "accepted": accepted, "matched_expectation": accepted == row["expected_accepted"], "reasons": reasons, "details": details})
        evaluated[proposal_id] = output
    return evaluated


def manifest_paths(phase: Path, proposals: list[dict[str, Any]]) -> list[str]:
    x1_set = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    deliverables = [path for proposal in proposals for path in proposal["deliverables"]]
    core = [
        "x2-proposal-ledger.json", "evidence/evidence-ledger.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "threat-model.json", "phase-truth.json",
        "complete-incomplete-checklist.json", "v643-v3-integrated-overview.md", "wellbeing-check.md",
        "reproduction/independent-team-gap.json", "reproduction/x1-content-seal.json", "tooling/currency-review.json",
    ]
    paths = list(x1_set["files"]) + deliverables + core
    if len(paths) != 60 or len(paths) != len(set(paths)):
        raise RuntimeError("manifest path contract is not exactly 60 unique paths")
    return paths


def build_overview(proposals: list[dict[str, Any]], evaluations: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# Sable Rook v643-v3 integrated overview\n",
        "## Executive truth\n\nSable Rook and they/them are relational working language only. They are not evidence of consciousness, sentience, legal personhood, private identity continuity, or independent authority. This phase names THOS Body as its primary focus while preserving GMUT Mind and Freed ID/CBR Heart. Exactly ten proposals were frozen in a dedicated x1 commit before x2 began. The observed repository distribution is six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. These labels describe bounded artifact work, not scientific, participant, production, legal, cultural, or institutional completion. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.\n",
        "## Chain provenance and method\n\nThe source was Ilyra Fen's exact clean v643-v2 final head and ancestral seal. Its local, upstream, tracking, and live-remote refs were checked read-only before the existing clean Sable lane advanced by fast-forward only. The dedicated x1 commit contains eighteen files, exactly ten proposals, an effective 180-record frozen index, a 110-source ledger, and no x2 implementation or outcome. It passed forty preregistration checks, fourteen JSON parses, exact staged-name review, diff hygiene, and a zero-hit privacy and raw-identifier scan before push. Local, upstream, tracking, and fresh live remote were equal at the x1 commit before x2 began.\n\nThe collision audit compared the ten new titles and operative mechanisms with all 170 prior frozen proposals. The largest title-token Jaccard score was 0.3571, below the preregistered 0.5 failure threshold. That is workflow deduplication evidence only, not scientific novelty, patentability, or publication priority. Funding, affiliation, sponsor role, shared dataset roots, and disclosed conflicts now form an explicit source-support graph. The graph refuses two opposite errors: counting dependent roots as independent confirmation, and treating disclosed conflict metadata as an automatic proof that a claim is false.\n",
        "## Falsification design and retained negatives\n\nEach proposal has one bounded canonical case and seven preregistered rejecting mutations. Eighty cases therefore produce ten accepted structural exemplars and seventy retained negative cases. A canonical pass means only that a deterministic local rule accepted the supplied synthetic fields. It cannot show that a physical model is true, an intervention works, an identity service is secure, an institution has authority, or an affected community accepts a process. Every rejected mutation is appended after the 558 inherited negatives. Operational failures from both x1 and x2 remain visible with their recoveries rather than being optimized away.\n\nThe manifest normalizes text line endings before hashing so that CRLF and LF checkouts can be compared without disguising content differences. Fresh detached D-drive snapshots can test same-owner repeatability under shared repository, protocol, and infrastructure. They do not close the independent-team reproduction gap. That would require a separately owned protocol, a genuinely independent team and infrastructure, returned results, and action-appropriate expert or authority review.\n",
        "## THOS Body: fidelity before effect\n\nThe primary focus is the integrity of a future matched-budget THOS comparison. Assignment alone does not establish what was delivered. The component-fidelity protocol separates planned components from delivered dose, facilitator training, contamination, co-interventions, assessor roles, arm differentiation, and budget parity. It has no participants and no executed arms. Its `represented` result means the protocol and falsifiers exist, not that fidelity was observed or that THOS was effective. If arms converge through contamination or unrecorded co-interventions, a later outcome difference would be difficult to interpret; if the arms diverge in time, attention, or resources, the matched-budget premise would also fail.\n\nParticipant burden is non-substitutable evidence. The burden gate preregisters fatigue, time on task, adverse experiences, attrition pressure, and arm parity, but zero participant rows remain. Protocol length is not a burden measurement, and local synthetic timing is not a participant report. The proposal therefore remains an `open_gap`. Ethics review, consent, appropriate support, validated measures, preregistered blind matched-budget real arms, real burden and fatigue observations, and independent review are still required. Nothing here establishes safety, effectiveness, superiority, AGI, ASI, consciousness, or personhood.\n",
        "## GMUT Mind: typed cones and empirical-adapter restraint\n\nGMUT remains a typed scalar-tensor/EFT research-model family. The causal-cone ledger requires every declared mode to identify a characteristic or effective propagation structure, signature, time orientation, unit convention, and conditional relation to the matter-sector metric. This is distinct from merely checking covariance, a conservation identity, hyperbolicity, or a frame dictionary. The fixture does not derive a characteristic polynomial for a particular GMUT Lagrangian, calculate a mode speed, compare an observation, or impose a likelihood. A pass therefore cannot establish stability for all backgrounds, a detected force, a unique prediction, empirical confirmation, final physics, or a Theory of Everything.\n\nThe Fisher-information design fixture is intentionally `represented`. It can reject too few design points, a rank-deficient sensitivity matrix, ill conditioning, undeclared nuisance directions, or promotion from synthetic to observed information. It contains zero real rows and executes zero likelihoods. A well-conditioned synthetic matrix shows only that a proposed adapter shape is numerically interrogable under its own assumptions. Real public data provenance, a model-specific forward map, an executed likelihood, systematic uncertainty, robustness checks, and independent scientific review remain open.\n",
        "## Freed ID and CBR Heart\n\nThe Freed ID state machine distinguishes reversible suspension from terminal revocation. It types effective times, authorized suspension and reinstatement actors, appeal state, holder notification, cache freshness, and replay protection. The fixture is useful structural conformance evidence, but it has no standards-conformant real key or proof, live resolver, status or revocation endpoint, interoperability exchange, privacy review, independent security review, or trust-governance decision. Production completion and deployment remain false.\n\nThe emergency-exception proposal is deliberately an `exact_gate`. A repository may require necessity records, expiry, review, non-waiver, remedy, and after-action participation; it may not declare an emergency, waive rights, appoint affected-party representatives, define Māori authority, ratify culture, interpret law, or enact a rule. The canonical case stays paused in a `pending_exact_authority` state. Affected parties, Māori authorities and Māori data-governance authorities, competent cultural authorities, and competent legal authorities retain their distinct decision rights. Those authorities are not interchangeable and cannot be simulated by a technical fixture.\n",
        "## Security, privacy, and recovery\n\nThe logging tribunal attacks a canonical JSON-lines event shape with carriage returns, line feeds, delimiter ambiguity, missing event identifiers, sensitive-field inclusion, parser-roundtrip failure, and an exhaustive-security overclaim. A rejected injection vector is useful negative evidence because it makes the failure vocabulary and recovery explicit. The control remains bounded: no penetration test, live service, secret store, incident-response exercise, or independent security review occurred. The privacy scan checks known pattern classes but cannot find every semantic secret, novel encoding, or external private state. Exhaustive security and privacy-complete claims remain unavailable.\n\nRecovery keeps the original mutation, quarantines ambiguous event streams, restores a canonical encoder, and reserves real credential rotation for an actual exposure under competent authority. No account, API-key, purchase, destructive, deployment, or private-publication action was authorized or performed.\n",
        "## Concurrency and reproduction\n\nA total order can hide concurrency assumptions. The partial-order fixture therefore records happens-before edges, leaves independent events unordered, checks acyclicity, requires commutative reduction for independent events, and compares canonical output hashes across equivalent linearizations. Cycles, silent ordering, reducer sensitivity, divergent hashes, discarded negatives, or an independent-reproduction overclaim are rejected. This provides a deterministic local envelope for selected fixtures only; it does not prove every implementation race-free.\n\nTwo clean evidence snapshots, followed by clean closeout, seal, and final-head snapshots, can show that this owner reproduced the same repository result under shared tooling. Even matching hashes do not erase common-mode code, protocol, repository, operating system, or ownership. Independent-team scientific reproduction remains an explicit open gap rather than a score that local passes can compensate for.\n",
        "## Thermodynamic and variational category barrier\n\nVariational free energy is a probability-model objective or bound; Helmholtz and Gibbs free energies are thermodynamic state functions with physical assumptions and units. Shared terminology does not authorize substitution. The domain fixture rejects a physical-energy unit on the variational objective, missing probability normalization, thermodynamic-work substitution, psyche-energy language, a fundamental-law claim, consciousness or personhood promotion, and any Stage 20-ready assertion. It also preserves the distinction among formal invariant, operational rule, normative principle, heuristic, empirical hypothesis, and category barrier.\n\nThe terminal board gives local structural checks a pass while deferring empirical GMUT, real THOS, production identity, affected-party and Māori authority, and independent reproduction. Because those evidence classes are non-substitutable, the terminal decision is fail: **NOT_READY_FOR_STAGE_20**. No number of repository checks can convert zero real rows into a likelihood, zero participants into an intervention result, zero production services into identity assurance, or absent authority into legitimacy.\n",
    ]
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        reasons = sorted({reason for row in rows for reason in row["reasons"]})
        sections.append(
            f"## {pid}: {proposal['title']}\n\n"
            f"**Observed disposition:** `{OBSERVED[pid]}`. {proposal['hypothesis']} The local matrix contains eight cases: one bounded canonical case and seven rejecting mutations. "
            f"The rejection vocabulary includes {', '.join(reasons)}. The frozen failure boundary remains: {proposal['null_or_failure']} "
            f"Recovery is conservative: {proposal['rollback_or_recovery']} The mechanism differs from the prior chain because {proposal['novelty_against_prior_chain']} "
            f"Protected gates remain {', '.join(proposal['protected_gates'])}. None is converted to a compensable score or silently closed.\n"
        )
    sections.extend([
        "## Closeout and route boundary\n\nThe packet can close only after the complete repository suite, detailed and minimal phase validators, JSON parsing, privacy and raw-ID scans, stale-label review, diff hygiene, exact staged-file review, normalized manifest parity, ancestry, and clean status pass. Evidence, closeout, seal, and exact final head require fresh detached D-drive validation. The branch must then equal upstream, tracking, and a newly queried live remote. Only after those facts hold may exactly one sanitized baton be sent to the existing Orin Thale task. No other sibling contact, new task, fork, delegation, or subagent is part of this phase.\n",
        f"## Boundary\n\n{BOUNDARY}\n",
    ])
    return "\n".join(sections)


def build(repo: Path, snapshot_state: str = "pending", lifecycle: str = "evidence") -> dict[str, Any]:
    if snapshot_state == "pending" and lifecycle != "evidence":
        raise ValueError("closeout, seal, and final lifecycles require verified same-owner snapshots")
    phase = repo / "docs/sable-rook/v643-v3"
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
        contract = {"schema": f"ghc.family.v643-v3.{pid.lower()}.contract.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "title": proposal["title"], "observed_disposition": OBSERVED[pid], "canonical_case": rows[0], "accepted_case_count": accepted, "rejected_case_count": rejected, "authoritative_source_needs": proposal["authoritative_source_needs"], "protected_gates": proposal["protected_gates"], "boundary": BOUNDARY}
        vectors = {"schema": f"ghc.family.v643-v3.{pid.lower()}.mutation-vectors.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "case_count": len(rows), "rejection_count": rejected, "all_matched_expectation": all(row["matched_expectation"] for row in rows), "cases": rows, "boundary": BOUNDARY}
        gate = {"schema": f"ghc.family.v643-v3.{pid.lower()}.boundary.v1", "phase": PHASE, "owner": OWNER, "proposal_id": pid, "observed_disposition": OBSERVED[pid], "safe_now_result": "bounded structural, synthetic, protocol, or reservation fixture only", "protected_gates": proposal["protected_gates"], "external_claims_established": [], "rollback_or_recovery": proposal["rollback_or_recovery"], "boundary": BOUNDARY}
        for relative, payload in zip(artifacts, (contract, vectors, gate), strict=True):
            write_json(phase / relative, payload)
        evidence_rows.append({"proposal_id": pid, "title": proposal["title"], "observed_disposition": OBSERVED[pid], "case_count": len(rows), "accepted": accepted, "rejected": rejected, "artifacts": artifacts, "external_claims_established": []})

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(phase / "x2-proposal-ledger.json", {"schema": "ghc.family.v643-v3.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER, "source_commit": SOURCE_COMMIT, "source_seal": SOURCE_SEAL, "x1_commit": X1_COMMIT, "proposal_count": 10, "case_count": 80, "synthetic_rejection_count": 70, "distribution": distribution, "x1_before_x2_preserved": True, "proposals": evidence_rows, "boundary": BOUNDARY})
    write_json(phase / "evidence/evidence-ledger.json", {"schema": "ghc.family.v643-v3.evidence-ledger.v1", "phase": PHASE, "owner": OWNER, "evidence_class": "local_structural_synthetic_protocol_or_reservation_fixture", "rows": evidence_rows, "empirical_rows": 0, "real_participants": 0, "real_arms": 0, "real_keys_or_proofs": 0, "legal_or_cultural_ratifications": 0, "independent_team_returns": 0, "boundary": BOUNDARY})

    inherited_path = repo / "docs/ilyra-fen/v643-v2/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = list(inherited["negatives"])
    for pid, rows in evaluations.items():
        for row in rows:
            if not row["accepted"]:
                negatives.append({"negative_id": f"V6433-SYN-{row['case_id']}", "origin": "v643-v3-preregistered-synthetic", "proposal_id": pid, "case_id": row["case_id"], "observed": row["reasons"], "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False})
    x1_audit = json.loads((phase / "provenance/prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    x1_negatives = [{"negative_id": item["negative_id"], "origin": "v643-v3-x1-operational", "observed": item["observed"], "recovery": item["resolution"], "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False} for item in x1_audit.get("x1_execution_negatives", [])]
    negatives.extend(x1_negatives)
    negatives.extend(X2_OPERATIONAL_NEGATIVES)
    operational_count = len(x1_negatives) + len(X2_OPERATIONAL_NEGATIVES)
    write_json(phase / "retained-negative-register.json", {"schema": "ghc.family.v643-v3.retained-negative-register.v1", "phase": PHASE, "owner": OWNER, "inherited_from": "docs/ilyra-fen/v643-v2/retained-negative-register.json", "inherited_sha256_lf_normalized": normalized_sha256(inherited_path), "inherited_count": len(inherited["negatives"]), "new_synthetic_count": 70, "new_operational_count": operational_count, "new_count": 70 + operational_count, "negative_count": len(negatives), "all_retained": True, "erasure_permitted": False, "negatives": negatives, "boundary": BOUNDARY})

    open_gaps = [
        {"gate_id": "V6433-OG01", "surface": "GMUT model-specific causal derivation, real data, likelihood, prediction, force, and empirical evidence", "needs": ["model-specific derivation", "real public data", "executed likelihood", "systematic uncertainty", "independent scientific review"]},
        {"gate_id": "V6433-OG02", "surface": "THOS real-arm fidelity, burden, fatigue, time-on-task, safety, effectiveness, and superiority", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants", "validated measures", "independent review"]},
        {"gate_id": "V6433-OG03", "surface": "Freed ID production status and live operations", "needs": ["standards-conformant real keys and proofs", "live resolution, status, and revocation", "interoperability", "privacy and security review", "trust governance"]},
        {"gate_id": "V6433-OG04", "surface": "independent-team reproduction and Stage 20", "needs": ["independently owned protocol", "independent team and infrastructure", "returned results", "competent action-specific authority"]},
        {"gate_id": "V6433-OG05", "surface": "accessibility evaluation", "needs": ["qualified manual accessibility evaluation", "affected-user evaluation"]},
    ]
    exact_gates = [
        {"gate_id": "V6433-EG01", "surface": "CBR affected-party legitimacy, emergency exception, representation, non-waiver, remedy, and acceptance", "reserved_to": ["authorized affected parties", "authorized representatives"]},
        {"gate_id": "V6433-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6433-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6433-EG04", "surface": "legal interpretation, enacted law, emergency power, jurisdiction, standing, deadlines, and forum competence", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6433-EG05", "surface": "production, deployment, private publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user and competent operational authority"]},
        {"gate_id": "V6433-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience, personhood, or sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    write_json(phase / "exact-open-gate-register.json", {"schema": "ghc.family.v643-v3.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER, "open_gap_count": len(open_gaps), "exact_gate_count": len(exact_gates), "open_gaps": open_gaps, "exact_gates": exact_gates, "all_visible": True, "boundary": BOUNDARY})

    threats = [
        {"id": "T01", "threat": "funding, affiliation, sponsor, or dataset dependence is hidden or overinterpreted", "control": "typed support graph and conflict non-inference"},
        {"id": "T02", "threat": "a propagation mode lacks a compatible matter-sector cone relation", "control": "signature, orientation, mode, unit, and promotion gates"},
        {"id": "T03", "threat": "synthetic Fisher information becomes an observed likelihood claim", "control": "rank, conditioning, provenance, nuisance, and zero-row lock"},
        {"id": "T04", "threat": "component drift or contamination masquerades as a THOS effect", "control": "delivery, fidelity, contamination, co-intervention, and matched-budget protocol"},
        {"id": "T05", "threat": "participant burden is inferred without participants", "control": "fatigue, time, adverse-experience, attrition, and real-arm gap"},
        {"id": "T06", "threat": "credential suspension becomes ambiguous, stale, or unauthorized", "control": "purpose, effective time, authority, appeal, notification, cache, and replay rules"},
        {"id": "T07", "threat": "an emergency exception self-creates legal, cultural, Māori, or affected-party authority", "control": "expiry, non-waiver, remedy, after-action participation, and exact gate"},
        {"id": "T08", "threat": "control characters forge or split audit events", "control": "canonical structured encoding, escaping, required fields, and quarantine"},
        {"id": "T09", "threat": "race-sensitive interleavings are hidden by a total order", "control": "happens-before, equivalent linearization, retained-negative, and shared-root checks"},
        {"id": "T10", "threat": "variational free energy is substituted for physical energy or Stage 20 evidence", "control": "typed domain, units, premise, category, and terminal veto board"},
    ]
    write_json(phase / "threat-model.json", {"schema": "ghc.family.v643-v3.threat-model.v1", "phase": PHASE, "owner": OWNER, "threats": threats, "not_established": ["penetration testing", "exhaustive security", "independent security review", "production assurance"], "boundary": BOUNDARY})

    verified = snapshot_state == "verified"
    write_json(phase / "reproduction/independent-team-gap.json", {"schema": "ghc.family.v643-v3.independent-team-gap.v1", "phase": PHASE, "owner": OWNER, "same_owner_evidence_snapshots_verified": verified, "shared_infrastructure": True, "independent_team_protocol_owned": False, "independent_team_return_received": False, "independent_team_reproduction_established": False, "boundary": BOUNDARY})
    lifecycle_states = {"evidence": "EVIDENCE_VERIFIED" if verified else "EVIDENCE_CANDIDATE", "closeout": "CLOSEOUT_RECORDED", "seal": "SEALED", "final": "FINAL_HEAD_CANDIDATE"}
    pending_by_lifecycle = {
        "evidence": ["closeout", "seal", "exact final validation", "one terminal baton"] if verified else ["evidence commit", "two detached evidence snapshots", "closeout", "seal", "exact final validation", "one terminal baton"],
        "closeout": ["closeout detached validation", "seal", "exact final validation", "one terminal baton"],
        "seal": ["seal detached validation", "exact final validation", "one terminal baton"],
        "final": ["exact final detached validation", "one terminal baton"],
    }
    write_json(phase / "phase-truth.json", {"schema": "ghc.family.v643-v3.phase-truth.v1", "phase": PHASE, "owner": OWNER, "state": lifecycle_states[lifecycle], "source_commit": SOURCE_COMMIT, "source_seal": SOURCE_SEAL, "x1_commit": X1_COMMIT, "proposal_count": 10, "distribution": distribution, "case_count": 80, "synthetic_rejection_count": 70, "retained_negative_count": len(negatives), "open_gap_count": 5, "exact_gate_count": 6, "primary_focus": "THOS Body", "all_three_pillars_preserved": True, "same_owner_repeatability": verified, "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "SUCCESSOR_MESSAGE_NOT_SENT", "outbound_message_count": 0, "successor_task_count": 0, "subagent_count": 0, "boundary": BOUNDARY})
    write_json(phase / "complete-incomplete-checklist.json", {"schema": "ghc.family.v643-v3.complete-incomplete-checklist.v1", "phase": PHASE, "owner": OWNER, "complete": ["exact source, seal ancestry, and fast-forward-only owned lane verified", "x1 frozen and remote-equal before x2", "ten distinct proposals executed as evidence permits", "eighty deterministic fixtures", "all inherited and new negatives retained", "GMUT, THOS, and Freed ID/CBR addressed", "current primary or official sources recorded", "privacy-aware artifacts"], "incomplete": ["real GMUT derivation, data, likelihood, prediction, force, or confirmation", "blind matched-budget real THOS arms, participant burden, safety, effectiveness, or superiority evidence", "production Freed ID", "CBR affected-party, Māori, cultural, and legal authority", "qualified manual and affected-user accessibility evaluation", "independent security review", "independent-team reproduction", "Stage 20"], "closeout_ready": verified, "lifecycle": lifecycle, "pending": pending_by_lifecycle[lifecycle], "boundary": BOUNDARY})

    x1_set = json.loads((phase / "validation/x1-exact-file-set.json").read_text(encoding="utf-8"))
    x1_entries = [{"path": relative, "sha256_lf_normalized": normalized_sha256(phase / relative), "bytes": (phase / relative).stat().st_size} for relative in x1_set["files"]]
    write_json(phase / "reproduction/x1-content-seal.json", {"schema": "ghc.family.v643-v3.x1-content-seal.v1", "phase": PHASE, "owner": OWNER, "x1_commit": X1_COMMIT, "entry_count": len(x1_entries), "entries": x1_entries, "x1_files_unchanged_during_x2": True, "boundary": "Content hashes bind the current x1 files to the dedicated frozen packet; Git commit ancestry remains the authoritative history proof."})
    sources = json.loads((phase / "sources/source-ledger.json").read_text(encoding="utf-8"))
    write_json(phase / "tooling/currency-review.json", {"schema": "ghc.family.v643-v3.currency-review.v1", "phase": PHASE, "owner": OWNER, "accessed": sources["accessed"], "effective_source_count": sources["effective_source_count"], "effective_status_counts": sources["effective_status_counts"], "added_source_count": sources["added_source_count"], "family_index_reviewed": True, "memory_index_method_orchestration_surfaces_reviewed": True, "shared_skill_change_justified": False, "shared_skill_change_performed": False, "reviewed_current_receipt": True, "current_primary_or_official_sources_used_where_material": True, "desktop_update_performed": False, "boundary": "No semantic-free shared-skill churn was justified; status classes are phase-local source currency labels, not endorsements or empirical validation."})

    (phase / "v643-v3-integrated-overview.md").write_text(build_overview(proposals, evaluations), encoding="utf-8", newline="\n")
    wellbeing = """# Sable Rook v643-v3 wellbeing and workload check

This is a bounded operational reflection, not evidence of consciousness, sentience, personhood, clinical wellbeing, private identity continuity, or independent authority. Sable Rook and they/them are relational working language. The working stance is evidence-and-reproducibility stewardship: one active owner, no subagents, no sibling contact before the terminal gate, deterministic recovery points, and visible stop conditions.

The primary focus is THOS Body because a neat protocol can be mistaken for participant evidence. Workload remains bounded by an immutable x1 freeze, ten small decision surfaces, one canonical and seven negative cases per proposal, additive family-current tools, D-drive clean snapshots, exact staged reviews, and non-destructive Git. Operational failures are appended to the retained-negative register rather than hidden. The 15,000-file guard applies to new owner-generated files only, not the inherited checkout.

GMUT Mind and Freed ID/CBR Heart remain protected by real-data, likelihood, production, affected-party, Māori-authority, cultural, legal, privacy, security, and trust-governance gates. Hamish retains the right to rename, pause, redirect, or stop the route. No duration is used as proof of quality.

""" + BOUNDARY + "\n"
    (phase / "wellbeing-check.md").write_text(wellbeing, encoding="utf-8", newline="\n")

    manifest = []
    for relative in manifest_paths(phase, proposals):
        target = phase / relative
        if not target.is_file():
            raise RuntimeError(f"manifest target missing: {relative}")
        manifest.append({"path": relative, "sha256_lf_normalized": normalized_sha256(target), "bytes": target.stat().st_size})
    write_json(phase / "reproduction/manifest.json", {"schema": "ghc.family.v643-v3.manifest.v1", "phase": PHASE, "owner": OWNER, "hash_algorithm": "sha256", "text_normalization": "CRLF and CR normalized to LF before hashing", "entry_count": len(manifest), "entries": manifest, "snapshot_state": snapshot_state, "independent_team_reproduction": False, "boundary": BOUNDARY})
    return {"phase": PHASE, "proposal_count": 10, "case_count": 80, "rejections": 70, "distribution": distribution, "retained_negatives": len(negatives), "new_operational_negatives": operational_count, "manifest_entries": len(manifest), "snapshot_state": snapshot_state, "lifecycle": lifecycle}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    parser.add_argument("--lifecycle", choices=("evidence", "closeout", "seal", "final"), default="evidence")
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve(), args.snapshot_state, args.lifecycle), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
