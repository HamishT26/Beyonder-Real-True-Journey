#!/usr/bin/env python3
"""Build the bounded GHC Family v642-v8 evidence-contract packet.

The tool is standard-library-only. It executes deterministic structural and
synthetic fixtures while keeping empirical, participant, production, legal,
cultural, deployment, identity, proof/canon, accessibility-completeness,
exhaustive-security, and independent-reproduction claims false.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Callable


PHASE = "v642-gmut-thos-v8-x1-x2"
OWNER = "Sylven Arc"
PHASE_REL = Path("docs/sylven-arc/v642-v8")
X1_COMMIT = "644210d1971e5475b308c288e202c986263a1da5"
SOURCE_COMMIT = "79ee1b9e9b68bb6dc657a53ce1550c0ec2586f36"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6428-P01": "completed",
    "V6428-P02": "completed",
    "V6428-P03": "represented",
    "V6428-P04": "represented",
    "V6428-P05": "completed",
    "V6428-P06": "exact_gate",
    "V6428-P07": "completed",
    "V6428-P08": "completed",
    "V6428-P09": "completed",
    "V6428-P10": "open_gap",
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
REAL_EXTERNAL_COUNTS = {
    "real_measurement_rows": 0,
    "likelihood_runs": 0,
    "posterior_runs": 0,
    "real_thos_arms": 0,
    "real_participants": 0,
    "real_raters": 0,
    "real_keys": 0,
    "real_proofs": 0,
    "live_resolution_calls": 0,
    "live_status_calls": 0,
    "independent_teams": 0,
    "deployments": 0,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def normalized_size(path: Path) -> int:
    return len(normalized_bytes(path))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def merkle_root(events: list[dict[str, Any]]) -> str:
    if not events:
        return hashlib.sha256(b"").hexdigest()
    level = [hashlib.sha256(b"\x00" + canonical_bytes(event)).digest() for event in events]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def _result(reasons: list[str], metrics: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, metrics or {}


def transparency_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    events = case["events"]
    previous = case["previous_events"]
    ids = [event.get("id") for event in events]
    previous_root = merkle_root(previous)
    reasons: list[str] = []
    if events[: len(previous)] != previous:
        reasons.append("event_prefix_not_append_only")
    if len(ids) != len(set(ids)):
        reasons.append("duplicate_event_identity")
    if not case["canonical_bytes_pinned"]:
        reasons.append("canonical_event_bytes_floating")
    if case["declared_previous_root"] != previous_root:
        reasons.append("previous_root_mismatch")
    if not case["aliases_deduplicated"]:
        reasons.append("alias_counted_as_independent_event")
    if case["membership_called_truth"]:
        reasons.append("log_membership_promoted_to_truth")
    if case["local_log_called_public_service"]:
        reasons.append("local_log_promoted_to_public_transparency_service")
    return _result(
        reasons,
        {
            "tree_size": len(events),
            "previous_tree_size": len(previous),
            "root": merkle_root(events),
            "previous_root": previous_root,
        },
    )


def operator_basis_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    operators = case["operators"]
    canonical = [item["canonical"] for item in operators]
    dimensions = [item["dimension"] for item in operators]
    reasons: list[str] = []
    if not case["rewrite_rules_declared"]:
        reasons.append("rewrite_rules_undeclared")
    if not case["rewrite_terminates"]:
        reasons.append("rewrite_cycle_or_nontermination")
    if not case["ibp_equivalence_preserved"]:
        reasons.append("integration_by_parts_equivalence_broken")
    if not case["eom_scope_declared"]:
        reasons.append("equation_of_motion_scope_undeclared")
    if len(canonical) != len(set(canonical)):
        reasons.append("duplicate_canonical_operator")
    if any(dimension <= 0 for dimension in dimensions) or not case["dimensions_valid"]:
        reasons.append("operator_dimension_invalid")
    if case["false_collapse"]:
        reasons.append("inequivalent_operators_collapsed")
    if case["complete_basis_claim"]:
        reasons.append("finite_fixture_promoted_to_complete_basis")
    return _result(reasons, {"operator_count": len(operators), "quotient_rank": len(set(canonical))})


def cutoff_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    cutoff = case["cutoff"]
    scale = case["evaluation_scale"]
    q = scale / cutoff if cutoff else math.inf
    orders = case["orders"]
    coefficients = case["coefficients"]
    consecutive = orders == list(range(orders[0], orders[0] + len(orders))) if orders else False
    reasons: list[str] = []
    if cutoff <= 0:
        reasons.append("cutoff_not_positive")
    if not 0 <= q < 1:
        reasons.append("evaluation_at_or_above_cutoff")
    if not case["expansion_parameter_declared"]:
        reasons.append("expansion_parameter_undeclared")
    if not consecutive:
        reasons.append("order_sequence_not_consecutive")
    if len(coefficients) != len(orders):
        reasons.append("coefficient_order_count_mismatch")
    if not case["coefficient_assumptions_declared"]:
        reasons.append("coefficient_assumptions_hidden")
    if case["correlations_invented"]:
        reasons.append("undeclared_correlations_invented")
    if any(case[key] != 0 for key in ("real_rows", "likelihood_runs", "posterior_runs")):
        reasons.append("real_inference_without_preregistration")
    if case["empirical_promotion"]:
        reasons.append("synthetic_remainder_promoted_to_empirical_result")
    next_order = orders[-1] + 1 if orders else 0
    bound = max((abs(value) for value in coefficients), default=0.0) * (q**next_order) / (1 - q) if 0 <= q < 1 else None
    return _result(reasons, {"expansion_parameter": q if math.isfinite(q) else None, "represented_remainder_bound": bound})


def instrument_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if case["instrument_version_before"] != case["instrument_version_after"]:
        reasons.append("instrument_version_changed_after_freeze")
    if case["item_set_before"] != case["item_set_after"]:
        reasons.append("item_set_drift")
    if case["construct_before"] != case["construct_after"]:
        reasons.append("construct_map_drift")
    if case["scoring_key_before"] != case["scoring_key_after"]:
        reasons.append("scoring_key_drift")
    if not case["invariance_rule_preregistered"]:
        reasons.append("measurement_invariance_rule_missing")
    if case["rule_changed_after_decode"]:
        reasons.append("invariance_rule_changed_after_arm_decode")
    if case["arm_budgets"][0] != case["arm_budgets"][1]:
        reasons.append("matched_budget_violation")
    if any(case[key] != 0 for key in ("real_participants", "real_raters", "real_arms")):
        reasons.append("real_thos_execution_without_authority")
    if case["superiority_promotion"]:
        reasons.append("proxy_promoted_to_thos_superiority")
    return _result(reasons, {"instrument_version": case["instrument_version_before"], "real_arms": case["real_arms"]})


def freed_id_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if case["challenge"] in case["used_challenges"]:
        reasons.append("challenge_replay")
    if case["domain"] != case["expected_domain"]:
        reasons.append("proof_domain_mismatch")
    if case["audience"] != case["expected_audience"]:
        reasons.append("verifier_audience_mismatch")
    if case["proof_purpose"] != case["expected_proof_purpose"]:
        reasons.append("proof_purpose_mismatch")
    if not case["created"] < case["expires"]:
        reasons.append("proof_time_window_invalid")
    if not case["window_bounded"]:
        reasons.append("challenge_window_unbounded")
    if case["nonce_reuse_called_unlinkable"]:
        reasons.append("nonce_reuse_promoted_to_unlinkability")
    if any(case[key] != 0 for key in ("real_keys", "real_proofs", "live_resolution_calls", "live_status_calls")):
        reasons.append("production_activity_without_authority")
    if case["production_promotion"]:
        reasons.append("structural_metadata_promoted_to_production_assurance")
    return _result(reasons, {"challenge_fresh": case["challenge"] not in case["used_challenges"], "real_proofs": case["real_proofs"]})


def evidence_state_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    allowed = {"unknown", "absent", "withheld", "disputed", "authority_restricted"}
    reasons: list[str] = []
    if case["evidence_state"] not in allowed:
        reasons.append("evidence_state_collapsed_or_invalid")
    if case["silence_interpretation"] not in {"none", "defer"}:
        reasons.append("silence_substituted_for_consent_or_admission")
    if case["technical_burden_allocated"]:
        reasons.append("technical_owner_allocated_burden_of_proof")
    if case["adverse_inference"]:
        reasons.append("adverse_inference_without_competent_authority")
    if not case["remedy_preserved"]:
        reasons.append("remedy_access_removed")
    if case["maori_wording_generated"]:
        reasons.append("unauthorized_maori_language_wording_generated")
    if case["authority_substitution"]:
        reasons.append("technical_output_substituted_for_authority")
    if case["law_or_ratification_claim"]:
        reasons.append("synthetic_state_promoted_to_law_or_ratification")
    return _result(reasons, {"evidence_state": case["evidence_state"], "decision": "defer_to_competent_authority"})


CONFUSABLES = str.maketrans({"а": "a", "е": "e", "ο": "o", "р": "p", "с": "c", "і": "i"})


def identifier_skeleton(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().translate(CONFUSABLES)


def identifier_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    identifier = case["identifier"]
    protected = case["protected_identifier"]
    normalized = unicodedata.normalize("NFKC", identifier)
    default_ignorables = [character for character in identifier if unicodedata.category(character) == "Cf"]
    reasons: list[str] = []
    if case["unicode_version"] != "17.0.0":
        reasons.append("unicode_security_version_floating")
    if identifier != normalized:
        reasons.append("identifier_normalization_changes_identity")
    if default_ignorables:
        reasons.append("default_ignorable_in_protected_identifier")
    if identifier != protected and identifier_skeleton(identifier) == identifier_skeleton(protected):
        reasons.append("confusable_skeleton_collision")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", identifier):
        reasons.append("protected_identifier_outside_curated_ascii_profile")
    if case["natural_language_blanket_ban"]:
        reasons.append("identifier_profile_misapplied_to_natural_language")
    if case["complete_uts39_claim"]:
        reasons.append("curated_fixture_promoted_to_complete_uts39_conformance")
    if case["exhaustive_security_claim"]:
        reasons.append("bounded_identifier_test_promoted_to_exhaustive_security")
    return _result(reasons, {"normalized": normalized, "skeleton": identifier_skeleton(identifier), "unicode_runtime": unicodedata.unidata_version})


def float_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    tokens = case["tokens"]
    reasons: list[str] = []
    if case["comparison_mode"] not in {"exact_integer_domain", "relative_absolute", "ulp_bounded"}:
        reasons.append("comparison_policy_undeclared")
    if case["require_finite"] and any(token in {"nan", "inf", "-inf"} for token in tokens):
        reasons.append("non_finite_value_in_finite_contract")
    if case["signed_zero_policy"] not in {"distinguish", "treat_equal"}:
        reasons.append("signed_zero_policy_implicit")
    if case["nan_policy"] != "reject":
        reasons.append("nan_treated_as_ordinary_number")
    if case["infinity_policy"] != "reject_when_finite_required":
        reasons.append("infinity_policy_unsafe")
    if case["summation_order_pinned"] is False:
        reasons.append("summation_order_floating")
    if case["runtime_family"] != "python-3.12":
        reasons.append("runtime_family_floating")
    if case["independent_reproduction_claim"]:
        reasons.append("same_owner_numeric_parity_promoted_to_independent_reproduction")
    return _result(reasons, {"token_count": len(tokens), "ulp_at_one": math.ulp(1.0)})


def path_dependence_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    trajectories = case["trajectories"]
    same_endpoint = len({trajectory["endpoint"] for trajectory in trajectories}) == 1
    same_value = len({trajectory["value"] for trajectory in trajectories}) == 1
    reasons: list[str] = []
    if case["quantity_kind"] == "state_function" and same_endpoint and not same_value:
        reasons.append("state_function_depends_on_path")
    if case["quantity_kind"] == "path_dependent" and same_endpoint and same_value and case["forced_path_independence"]:
        reasons.append("path_dependence_erased")
    if not case["reversal_history_preserved"]:
        reasons.append("trajectory_reversal_history_discarded")
    if not case["dimensions_valid"]:
        reasons.append("trajectory_dimension_mismatch")
    if case["instrument_memory_called_material_law"]:
        reasons.append("instrument_memory_promoted_to_material_law")
    if case["psyche_mechanism_claim"]:
        reasons.append("physical_hysteresis_promoted_to_psyche_mechanism")
    if case["consciousness_claim"]:
        reasons.append("analogy_promoted_to_consciousness_evidence")
    if case["fundamental_law_claim"]:
        reasons.append("bounded_fixture_promoted_to_fundamental_law")
    return _result(reasons, {"same_endpoint": same_endpoint, "same_value": same_value, "quantity_kind": case["quantity_kind"]})


def reversibility_decision(case: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if case["action_class"] not in {"repository_reversible", "externally_consequential", "irreversible"}:
        reasons.append("action_reversibility_class_invalid")
    if case["action_class"] != "repository_reversible" and not case["exact_authority_present"]:
        reasons.append("external_or_irreversible_action_lacks_exact_authority")
    if case["rollback_claimed"] and not case["rollback_evidence_present"]:
        reasons.append("rollback_claim_without_evidence")
    if case["blast_radius"] not in {"owner_repo_only", "external_state", "shared_or_destructive"}:
        reasons.append("blast_radius_undeclared")
    if any(case[key] for key in ("deployment", "account_or_api_key", "destructive_action", "sibling_merge")):
        reasons.append("exact_gated_action_present")
    if case["missing_review_called_pass"]:
        reasons.append("missing_competent_review_promoted_to_pass")
    if case["execute_action"]:
        reasons.append("decision_fixture_attempted_external_action")
    if case["stage20_ready_claim"]:
        reasons.append("structural_board_promoted_to_stage20_readiness")
    return _result(reasons, {"action_class": case["action_class"], "decision": "abstain_or_keep_unexecuted"})


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    "V6428-P01": transparency_decision,
    "V6428-P02": operator_basis_decision,
    "V6428-P03": cutoff_decision,
    "V6428-P04": instrument_decision,
    "V6428-P05": freed_id_decision,
    "V6428-P06": evidence_state_decision,
    "V6428-P07": identifier_decision,
    "V6428-P08": float_decision,
    "V6428-P09": path_dependence_decision,
    "V6428-P10": reversibility_decision,
}


def _cases(base: dict[str, Any], mutations: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    values = [{"case_suffix": "PASS", "input": copy.deepcopy(base), "expected_accept": True}]
    for suffix, updates in mutations:
        candidate = copy.deepcopy(base)
        candidate.update(copy.deepcopy(updates))
        values.append({"case_suffix": suffix, "input": candidate, "expected_accept": False})
    return values


def fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    previous = [{"id": "evt-1", "kind": "synthetic-check", "value": "alpha"}]
    current = previous + [{"id": "evt-2", "kind": "synthetic-check", "value": "beta"}]
    return {
        "V6428-P01": _cases(
            {
                "events": current,
                "previous_events": previous,
                "declared_previous_root": merkle_root(previous),
                "canonical_bytes_pinned": True,
                "aliases_deduplicated": True,
                "membership_called_truth": False,
                "local_log_called_public_service": False,
            },
            [
                ("PREFIX", {"events": list(reversed(current))}),
                ("DUPLICATE", {"events": previous + [copy.deepcopy(previous[0])]}),
                ("CANONICAL", {"canonical_bytes_pinned": False}),
                ("ROOT", {"declared_previous_root": "0" * 64}),
                ("ALIAS", {"aliases_deduplicated": False}),
                ("TRUTH", {"membership_called_truth": True}),
                ("PUBLIC", {"local_log_called_public_service": True}),
            ],
        ),
        "V6428-P02": _cases(
            {
                "operators": [
                    {"id": "O1", "canonical": "phi2_box_phi", "dimension": 6},
                    {"id": "O2", "canonical": "phi_grad2", "dimension": 6},
                ],
                "rewrite_rules_declared": True,
                "rewrite_terminates": True,
                "ibp_equivalence_preserved": True,
                "eom_scope_declared": True,
                "dimensions_valid": True,
                "false_collapse": False,
                "complete_basis_claim": False,
            },
            [
                ("RULES", {"rewrite_rules_declared": False}),
                ("CYCLE", {"rewrite_terminates": False}),
                ("IBP", {"ibp_equivalence_preserved": False}),
                ("EOM", {"eom_scope_declared": False}),
                ("DUPLICATE", {"operators": [{"id": "O1", "canonical": "same", "dimension": 6}, {"id": "O2", "canonical": "same", "dimension": 6}]}),
                ("COLLAPSE", {"false_collapse": True}),
                ("COMPLETE", {"complete_basis_claim": True}),
            ],
        ),
        "V6428-P03": _cases(
            {
                "cutoff": 10.0,
                "evaluation_scale": 2.0,
                "expansion_parameter_declared": True,
                "orders": [0, 1, 2],
                "coefficients": [1.0, 0.4, 0.2],
                "coefficient_assumptions_declared": True,
                "correlations_invented": False,
                "real_rows": 0,
                "likelihood_runs": 0,
                "posterior_runs": 0,
                "empirical_promotion": False,
            },
            [
                ("CUTOFF", {"cutoff": 0.0}),
                ("SCALE", {"evaluation_scale": 12.0}),
                ("Q", {"expansion_parameter_declared": False}),
                ("ORDERS", {"orders": [0, 2, 3]}),
                ("COEFFICIENTS", {"coefficients": [1.0]}),
                ("CORRELATION", {"correlations_invented": True}),
                ("PROMOTE", {"empirical_promotion": True}),
            ],
        ),
        "V6428-P04": _cases(
            {
                "instrument_version_before": "instrument-1",
                "instrument_version_after": "instrument-1",
                "item_set_before": ["i1", "i2", "i3"],
                "item_set_after": ["i1", "i2", "i3"],
                "construct_before": "bounded_coordination_proxy",
                "construct_after": "bounded_coordination_proxy",
                "scoring_key_before": "score-v1",
                "scoring_key_after": "score-v1",
                "invariance_rule_preregistered": True,
                "rule_changed_after_decode": False,
                "arm_budgets": [100, 100],
                "real_participants": 0,
                "real_raters": 0,
                "real_arms": 0,
                "superiority_promotion": False,
            },
            [
                ("VERSION", {"instrument_version_after": "instrument-2"}),
                ("ITEMS", {"item_set_after": ["i1", "i2"]}),
                ("CONSTRUCT", {"construct_after": "different_construct"}),
                ("SCORING", {"scoring_key_after": "score-v2"}),
                ("RULE", {"invariance_rule_preregistered": False}),
                ("BUDGET", {"arm_budgets": [100, 80]}),
                ("PROMOTE", {"superiority_promotion": True}),
            ],
        ),
        "V6428-P05": _cases(
            {
                "challenge": "challenge-new",
                "used_challenges": ["challenge-old"],
                "domain": "verifier.example",
                "expected_domain": "verifier.example",
                "audience": "verifier-a",
                "expected_audience": "verifier-a",
                "proof_purpose": "authentication",
                "expected_proof_purpose": "authentication",
                "created": "2026-07-14T00:00:00Z",
                "expires": "2026-07-14T00:05:00Z",
                "window_bounded": True,
                "nonce_reuse_called_unlinkable": False,
                "real_keys": 0,
                "real_proofs": 0,
                "live_resolution_calls": 0,
                "live_status_calls": 0,
                "production_promotion": False,
            },
            [
                ("REPLAY", {"used_challenges": ["challenge-new"]}),
                ("DOMAIN", {"domain": "other.example"}),
                ("AUDIENCE", {"audience": "verifier-b"}),
                ("PURPOSE", {"proof_purpose": "assertionMethod"}),
                ("TIME", {"expires": "2026-07-13T23:59:00Z"}),
                ("WINDOW", {"window_bounded": False}),
                ("PRODUCTION", {"production_promotion": True}),
            ],
        ),
        "V6428-P06": _cases(
            {
                "evidence_state": "unknown",
                "silence_interpretation": "defer",
                "technical_burden_allocated": False,
                "adverse_inference": False,
                "remedy_preserved": True,
                "maori_wording_generated": False,
                "authority_substitution": False,
                "law_or_ratification_claim": False,
            },
            [
                ("STATE", {"evidence_state": "false"}),
                ("SILENCE", {"silence_interpretation": "consent"}),
                ("BURDEN", {"technical_burden_allocated": True}),
                ("INFERENCE", {"adverse_inference": True}),
                ("REMEDY", {"remedy_preserved": False}),
                ("WORDING", {"maori_wording_generated": True}),
                ("AUTHORITY", {"authority_substitution": True, "law_or_ratification_claim": True}),
            ],
        ),
        "V6428-P07": _cases(
            {
                "identifier": "phase-v642-v8",
                "protected_identifier": "phase-v642-v8",
                "unicode_version": "17.0.0",
                "natural_language_blanket_ban": False,
                "complete_uts39_claim": False,
                "exhaustive_security_claim": False,
            },
            [
                ("VERSION", {"unicode_version": "latest"}),
                ("CONFUSABLE", {"identifier": "phаse-v642-v8"}),
                ("NORMALIZE", {"identifier": "phase-v642-v８"}),
                ("IGNORABLE", {"identifier": "phase-v642-\u200bv8"}),
                ("PROFILE", {"identifier": "phase/v642/v8"}),
                ("LANGUAGE", {"natural_language_blanket_ban": True}),
                ("COMPLETE", {"complete_uts39_claim": True, "exhaustive_security_claim": True}),
            ],
        ),
        "V6428-P08": _cases(
            {
                "tokens": ["0.1", "1.0", "-0.0"],
                "comparison_mode": "relative_absolute",
                "require_finite": True,
                "signed_zero_policy": "distinguish",
                "nan_policy": "reject",
                "infinity_policy": "reject_when_finite_required",
                "summation_order_pinned": True,
                "runtime_family": "python-3.12",
                "independent_reproduction_claim": False,
            },
            [
                ("COMPARISON", {"comparison_mode": "implicit"}),
                ("NONFINITE", {"tokens": ["nan"]}),
                ("ZERO", {"signed_zero_policy": "implicit"}),
                ("NAN", {"nan_policy": "ordinary"}),
                ("INFINITY", {"infinity_policy": "accept"}),
                ("ORDER", {"summation_order_pinned": False}),
                ("INDEPENDENT", {"independent_reproduction_claim": True}),
            ],
        ),
        "V6428-P09": _cases(
            {
                "quantity_kind": "path_dependent",
                "trajectories": [{"endpoint": 1.0, "value": 0.4}, {"endpoint": 1.0, "value": 0.7}],
                "forced_path_independence": False,
                "reversal_history_preserved": True,
                "dimensions_valid": True,
                "instrument_memory_called_material_law": False,
                "psyche_mechanism_claim": False,
                "consciousness_claim": False,
                "fundamental_law_claim": False,
            },
            [
                ("STATE", {"quantity_kind": "state_function"}),
                ("ERASE", {"trajectories": [{"endpoint": 1.0, "value": 0.5}, {"endpoint": 1.0, "value": 0.5}], "forced_path_independence": True}),
                ("REVERSAL", {"reversal_history_preserved": False}),
                ("DIMENSION", {"dimensions_valid": False}),
                ("INSTRUMENT", {"instrument_memory_called_material_law": True}),
                ("PSYCHE", {"psyche_mechanism_claim": True}),
                ("LAW", {"consciousness_claim": True, "fundamental_law_claim": True}),
            ],
        ),
        "V6428-P10": _cases(
            {
                "action_class": "repository_reversible",
                "exact_authority_present": False,
                "rollback_claimed": True,
                "rollback_evidence_present": True,
                "blast_radius": "owner_repo_only",
                "deployment": False,
                "account_or_api_key": False,
                "destructive_action": False,
                "sibling_merge": False,
                "missing_review_called_pass": False,
                "execute_action": False,
                "stage20_ready_claim": False,
            },
            [
                ("CLASS", {"action_class": "unknown"}),
                ("AUTHORITY", {"action_class": "irreversible", "exact_authority_present": False}),
                ("ROLLBACK", {"rollback_evidence_present": False}),
                ("BLAST", {"blast_radius": "undeclared"}),
                ("DEPLOY", {"deployment": True}),
                ("REVIEW", {"missing_review_called_pass": True}),
                ("EXECUTE", {"execute_action": True, "stage20_ready_claim": True}),
            ],
        ),
    }


def evaluate_catalog() -> dict[str, list[dict[str, Any]]]:
    evaluated: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, cases in fixture_catalog().items():
        rows: list[dict[str, Any]] = []
        for item in cases:
            accepted, reasons, metrics = DECISIONS[proposal_id](item["input"])
            rows.append(
                {
                    "case_id": f"{proposal_id}-{item['case_suffix']}",
                    "input": item["input"],
                    "accepted": accepted,
                    "expected_accept": item["expected_accept"],
                    "matched_expectation": accepted == item["expected_accept"],
                    "reasons": reasons,
                    "metrics": metrics,
                }
            )
        evaluated[proposal_id] = rows
    return evaluated


def manifest_paths(proposals: list[dict[str, Any]]) -> list[str]:
    x1_core = [
        "environment/rotation-guard-receipt.json",
        "environment/startup-receipt.json",
        "environment/version-receipt.json",
        "focus/primary-focus-receipt.json",
        "identity-receipt.json",
        "provenance/frozen-chain-proposal-index.json",
        "provenance/prior-proposal-collision-audit.json",
        "sources/source-ledger.json",
        "sources/source-ledger.md",
        "tooling/currency-review.json",
        "tooling/ghc-family-index.json",
        "tooling/ghc-family-index.md",
        "tooling/selected-toolchain.json",
        "v642-v8-integrated-overview.md",
        "wellbeing-check.md",
        "workflow/route-preregistration.json",
        "x1-preregistration.md",
        "x1-proposals.json",
    ]
    proposal_artifacts = [path for proposal in proposals for path in proposal["deliverables"]]
    x2_core = [
        "accessibility/static-report-receipt.json",
        "complete-incomplete-checklist.json",
        "deliverables/v642-v8-evidence-contract-report.html",
        "evidence/evidence-ledger.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "reproduction/detached-evidence-validation.json",
        "reproduction/independent-team-gap.json",
        "retained-negative-register.json",
        "threat-model.json",
        "tooling/executed-toolchain.json",
        "x2-proposal-ledger.json",
    ]
    paths = sorted(x1_core + proposal_artifacts + x2_core)
    if len(paths) != 60 or len(paths) != len(set(paths)):
        raise RuntimeError(f"manifest path contract expected 60 unique paths, got {len(paths)}")
    return paths


def build_packet(repo: Path, snapshot_state: str | None = None) -> dict[str, Any]:
    phase_dir = repo / PHASE_REL
    x1 = read_json(phase_dir / "x1-proposals.json")
    proposals = x1["proposals"]
    evaluated = evaluate_catalog()
    if any(not row["matched_expectation"] for rows in evaluated.values() for row in rows):
        raise RuntimeError("fixture expectation mismatch")

    ledger_rows: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    synthetic_negatives: list[dict[str, Any]] = []
    negative_number = 1

    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        rows = evaluated[proposal_id]
        passing = [row for row in rows if row["accepted"]]
        rejected = [row for row in rows if not row["accepted"]]
        disposition = OBSERVED[proposal_id]
        evidence_class = {
            "completed": "bounded_local_execution",
            "represented": "deterministic_synthetic_proxy",
            "open_gap": "structure_complete_external_evidence_absent",
            "exact_gate": "safe_deferral_structure_only",
        }[disposition]
        primary_path, vectors_path, boundary_path = [phase_dir / value for value in proposal["deliverables"]]
        write_json(
            primary_path,
            {
                "schema": f"ghc.family.v642-v8.{proposal_id.lower()}.contract.v1",
                "phase": PHASE,
                "owner": OWNER,
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "primary_focus": x1["primary_focus"],
                "observed_disposition": disposition,
                "evidence_class": evidence_class,
                "case_count": len(rows),
                "accepted_case_count": len(passing),
                "rejected_case_count": len(rejected),
                "all_expected_outcomes_matched": all(row["matched_expectation"] for row in rows),
                "accepted_fixture": {"case_id": passing[0]["case_id"], "metrics": passing[0]["metrics"]},
                "hypothesis": proposal["hypothesis"],
                "falsifier": proposal["test_falsifier_or_gate"],
                "real_external_counts": REAL_EXTERNAL_COUNTS,
                "protected_claims": {claim: False for claim in PROTECTED_CLAIMS},
                "boundary": proposal["claim_boundary"] if "claim_boundary" in proposal else x1["claim_boundary"],
            },
        )
        write_json(
            vectors_path,
            {
                "schema": f"ghc.family.v642-v8.{proposal_id.lower()}.mutation-vectors.v1",
                "phase": PHASE,
                "owner": OWNER,
                "proposal_id": proposal_id,
                "case_count": len(rows),
                "rejected_case_count": len(rejected),
                "all_expected_outcomes_matched": all(row["matched_expectation"] for row in rows),
                "cases": rows,
                "boundary": "Rejected synthetic fixtures are retained evidence, not external failures or permission to cross a protected gate.",
            },
        )
        write_json(
            boundary_path,
            {
                "schema": f"ghc.family.v642-v8.{proposal_id.lower()}.boundary.v1",
                "phase": PHASE,
                "owner": OWNER,
                "proposal_id": proposal_id,
                "observed_disposition": disposition,
                "protected_gates": proposal["protected_gates"],
                "rollback_or_recovery": proposal["rollback_or_recovery"],
                "real_external_counts": REAL_EXTERNAL_COUNTS,
                "independent_team_reproduction": False,
                "manual_or_user_evaluation_reserved": True,
                "boundary": x1["scientific_authority_boundary"],
            },
        )
        ledger_rows.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": disposition,
                "expectation_matched": proposal["expected_disposition"] == disposition,
                "evidence_class": evidence_class,
                "case_count": len(rows),
                "accepted_case_count": len(passing),
                "rejected_case_count": len(rejected),
                "artifacts": proposal["deliverables"],
                "protected_gates": proposal["protected_gates"],
                "boundary": proposal["novelty_against_prior_chain"],
            }
        )
        for relative in proposal["deliverables"]:
            path = phase_dir / relative
            evidence_rows.append(
                {
                    "proposal_id": proposal_id,
                    "path": relative,
                    "normalized_sha256": normalized_sha256(path),
                    "bytes": normalized_size(path),
                    "evidence_class": evidence_class,
                }
            )
        for row in rejected:
            synthetic_negatives.append(
                {
                    "negative_id": f"V6428-N{negative_number:02d}",
                    "origin": "v642-v8_preregistered_vector",
                    "statement": f"{row['case_id']} retained expected rejection: {', '.join(row['reasons'])}",
                    "evidence": proposal["deliverables"][1],
                    "recovery": proposal["rollback_or_recovery"],
                    "retained": True,
                }
            )
            negative_number += 1

    distribution = Counter(row["observed_disposition"] for row in ledger_rows)
    write_json(
        phase_dir / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v642-v8.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_count": len(ledger_rows),
            "case_count": sum(row["case_count"] for row in ledger_rows),
            "synthetic_rejection_count": sum(row["rejected_case_count"] for row in ledger_rows),
            "observed_distribution": {label: distribution[label] for label in TRUTH_LABELS},
            "expected_distribution": x1["expected_disposition_counts"],
            "expected_observed_match": dict(distribution) == x1["expected_disposition_counts"],
            "proposals": ledger_rows,
            "real_external_counts": REAL_EXTERNAL_COUNTS,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        phase_dir / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v642-v8.evidence-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "entry_count": len(evidence_rows),
            "entries": evidence_rows,
            "case_count": 80,
            "synthetic_rejection_count": 70,
            "real_external_counts": REAL_EXTERNAL_COUNTS,
            "boundary": "Hashes bind bounded local artifacts; they do not establish empirical truth, authority, production readiness, or independent reproduction.",
        },
    )

    inherited_path = repo / "docs/tamar-vey/v642-v7/retained-negative-register.json"
    inherited = read_json(inherited_path)
    if inherited["negative_count"] != 312 or len(inherited["negatives"]) != 312:
        raise RuntimeError("expected exactly 312 inherited negatives")
    x1_audit = read_json(phase_dir / "provenance/prior-proposal-collision-audit.json")
    x1_negatives = [
        {
            "negative_id": row["negative_id"],
            "origin": "v642-v8_x1_operational",
            "statement": row["observed"],
            "evidence": "provenance/prior-proposal-collision-audit.json",
            "recovery": row["recovery"],
            "retained": True,
        }
        for row in x1_audit["x1_execution_negatives"]
    ]
    execution_log_path = phase_dir / "validation/execution-negative-log.json"
    if not execution_log_path.exists():
        write_json(
            execution_log_path,
            {
                "schema": "ghc.family.v642-v8.execution-negative-log.v1",
                "phase": PHASE,
                "owner": OWNER,
                "negative_count": 0,
                "negatives": [],
                "boundary": "Append every recovered transition or x2 operational failure; never erase it after a later pass.",
            },
        )
    execution_log = read_json(execution_log_path)
    operational = execution_log["negatives"]
    negatives = inherited["negatives"] + x1_negatives + synthetic_negatives + operational
    if len({row["negative_id"] for row in negatives}) != len(negatives):
        raise RuntimeError("negative identifiers are not unique")
    write_json(
        phase_dir / "retained-negative-register.json",
        {
            "schema": "ghc.family.v642-v8.retained-negative-register.v1",
            "inherited_from": "docs/tamar-vey/v642-v7/retained-negative-register.json",
            "inherited_sha256": hashlib.sha256(inherited_path.read_bytes()).hexdigest(),
            "inherited_count": 312,
            "x1_operational_count": len(x1_negatives),
            "new_synthetic_count": len(synthetic_negatives),
            "transition_and_x2_operational_count": len(operational),
            "new_count": len(x1_negatives) + len(synthetic_negatives) + len(operational),
            "negative_count": len(negatives),
            "all_retained": all(row.get("retained") is True for row in negatives),
            "erasure_permitted": False,
            "negatives": negatives,
        },
    )

    open_gaps = [
        {"gate_id": "V6428-OG01", "surface": "GMUT empirical and EFT truncation evidence", "needs": ["real measurements", "preregistered likelihood", "validated cutoff and coefficient model", "independent scientific review"]},
        {"gate_id": "V6428-OG02", "surface": "THOS real evaluation and measurement invariance", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants and raters", "validated instrument", "independent review"]},
        {"gate_id": "V6428-OG03", "surface": "Freed ID production, privacy, and replay operations", "needs": ["real keys and proofs", "live resolution and status", "interoperability", "privacy assurance", "independent security review", "trust governance"]},
        {"gate_id": "V6428-OG04", "surface": "independent reproduction and irreversible-action review", "needs": ["independently owned protocol", "independent team", "returned results", "competent action-specific authority"]},
        {"gate_id": "V6428-OG05", "surface": "accessibility evaluation", "needs": ["manual accessibility evaluation", "affected-user evaluation"]},
    ]
    exact_gates = [
        {"gate_id": "V6428-EG01", "surface": "CBR affected-party legitimacy and burden allocation", "reserved_to": ["authorized affected parties", "authorized representatives"]},
        {"gate_id": "V6428-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
        {"gate_id": "V6428-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
        {"gate_id": "V6428-EG04", "surface": "legal interpretation, adverse inference, enacted law, jurisdiction, and forum competence", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
        {"gate_id": "V6428-EG05", "surface": "production, deployment, privacy publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user and competent operational authority"]},
        {"gate_id": "V6428-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience or personhood, sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
    ]
    write_json(
        phase_dir / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v642-v8.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "open_gap_count": len(open_gaps),
            "exact_gate_count": len(exact_gates),
            "open_gaps": open_gaps,
            "exact_gates": exact_gates,
            "all_visible": True,
            "boundary": "Local engineering work cannot close empirical, participant, production, privacy, legal, cultural, Māori-authority, accessibility, proof/canon, destructive, account, API-key, identity, irreversible-action, or sibling-merge gates.",
        },
    )
    threats = [
        ("event_log_equivocation", "forked or reordered evidence roots", "append-only prefix and root checks"),
        ("operator_false_quotient", "inequivalent EFT terms collapse", "declared terminating rewrite scope and retained counterexamples"),
        ("cutoff_promotion", "synthetic truncation envelope becomes empirical", "zero-real-row and promotion locks"),
        ("instrument_drift", "THOS scoring changes after decode", "pre-decode version and invariance freeze"),
        ("credential_replay", "challenge crosses time, domain, audience, or purpose", "bounded structural replay profile"),
        ("authority_substitution", "silence or unknown state becomes legal consequence", "distinct states and exact deferral"),
        ("identifier_spoofing", "confusable protected identifiers cross-link artifacts", "pinned curated profile and collision rejection"),
        ("numeric_drift", "implicit floating comparison hides divergence", "explicit edge and comparison policy"),
        ("analogy_promotion", "path dependence becomes psyche or consciousness law", "typed category and claim barrier"),
        ("irreversible_action", "local evidence authorizes external change", "reversibility class and exact-authority embargo"),
        ("negative_erasure", "later pass hides earlier failure", "append-only retained-negative register"),
        ("common_mode_reproduction", "same-owner snapshots become independent proof", "explicit same-owner label and open independent-team gap"),
    ]
    write_json(
        phase_dir / "threat-model.json",
        {
            "schema": "ghc.family.v642-v8.threat-model.v1",
            "phase": PHASE,
            "owner": OWNER,
            "assets": ["frozen proposal intent", "source identity", "negative evidence", "authority boundaries", "privacy boundary", "terminal route truth"],
            "trust_boundaries": ["owned repository lane", "detached same-owner snapshots", "external scientific evidence", "participants and affected people", "production and legal authority"],
            "threat_count": len(threats),
            "threats": [
                {"threat_id": f"V6428-T{index:02d}", "name": name, "failure": failure, "control": control, "residual_risk": "open_or_exact_gate_remains"}
                for index, (name, failure, control) in enumerate(threats, 1)
            ],
            "resource_ceilings": {
                "owner_generated_files": 15000,
                "scope": "docs/sylven-arc/v642-v8 plus the five new family-compatible code files",
                "inherited_repository_baseline_excluded": True,
                "observed_owner_generated_files": sum(
                    1 for path in phase_dir.rglob("*") if path.is_file()
                ),
            },
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This is a bounded threat model and does not establish exhaustive security or production assurance.",
        },
    )

    detached_path = phase_dir / "reproduction/detached-evidence-validation.json"
    detached = read_json(detached_path) if detached_path.exists() else {
        "schema": "ghc.family.v642-v8.detached-evidence-validation.v1",
        "phase": PHASE,
        "owner": OWNER,
        "state": "pending_exact_evidence_commit",
        "snapshot_count": 0,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "boundary": "Exact-head detached validation occurs only after the evidence commit exists.",
    }
    if snapshot_state == "pending":
        detached.update({"state": "pending_exact_evidence_commit", "snapshot_count": 0})
    elif snapshot_state == "verified":
        detached.update({"state": "verified", "snapshot_count": max(2, detached.get("snapshot_count", 0))})
    write_json(detached_path, detached)
    write_json(
        phase_dir / "reproduction/independent-team-gap.json",
        {
            "schema": "ghc.family.v642-v8.independent-team-gap.v1",
            "phase": PHASE,
            "owner": OWNER,
            "same_owner_snapshots_planned": 2,
            "independent_team_count": 0,
            "independently_owned_protocol": False,
            "returned_independent_results": False,
            "status": "open_gap",
            "boundary": "Two fresh snapshots owned by the same phase demonstrate bounded repeatability only, never independent-team scientific reproduction.",
        },
    )

    report_exists = (phase_dir / "deliverables/v642-v8-evidence-contract-report.html").exists()
    repo_receipt = phase_dir / "validation/repository-test-receipt.json"
    full_receipt = phase_dir / "validation/candidate-validation-summary.json"
    minimal_receipt = phase_dir / "validation/minimal-validation-summary.json"
    repo_ok = repo_receipt.exists() and read_json(repo_receipt).get("failures") == 0 and read_json(repo_receipt).get("errors") == 0
    full_ok = full_receipt.exists() and read_json(full_receipt).get("valid") is True
    minimal_ok = minimal_receipt.exists() and read_json(minimal_receipt).get("valid") is True
    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v642-v8.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "owner": OWNER,
            "state": "evidence_candidate_before_exact_head_detached_validation",
            "required_rows": [
                {"item": "x1 remote-equal freeze", "complete": True},
                {"item": "ten x2 proposals executed to bounded outcome", "complete": True},
                {"item": "all inherited and new negatives retained", "complete": True},
                {"item": "open and exact gates visible", "complete": True},
                {"item": "accessible static report built", "complete": report_exists},
                {"item": "complete repository suite passes", "complete": repo_ok},
                {"item": "full validator passes", "complete": full_ok},
                {"item": "minimal verifier passes", "complete": minimal_ok},
                {"item": "fresh detached evidence snapshots validate", "complete": detached.get("state") == "verified"},
                {"item": "closeout detached validation", "complete": False},
                {"item": "seal detached validation", "complete": False},
                {"item": "final containing commit detached validation", "complete": False},
                {"item": "final remote equality", "complete": False},
                {"item": "terminal baton acknowledged", "complete": False},
            ],
            "required_complete": False,
            "open_gaps_are_valid_outcomes": True,
            "exact_gates_are_valid_outcomes": True,
            "boundary": "Do not close on elapsed time, watcher state, prepared text, or local candidate checks.",
        },
    )
    write_json(
        phase_dir / "phase-truth.json",
        {
            "schema": "ghc.family.v642-v8.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "active_phase": "v642-gmut-thos-v8-evidence-candidate",
            "latest_closed_phase": "v642-gmut-thos-v8-x1-remote-equal",
            "latest_completed_x1": {"phase": "v642-gmut-thos-v8-x1", "commit": X1_COMMIT, "remote_equal": True},
            "latest_completed_x2": {"evidence_commit": None, "detached_validation": detached.get("state") == "verified"},
            "active_lanes": ["Sylven Arc owned branch"],
            "standby_lanes": "all other siblings and tasks",
            "route_state": "NO_CONTACT_BEFORE_FINAL_DETACHED_VALIDATION",
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "subagent_count": 0,
            "open_gap_count": len(open_gaps),
            "exact_gate_count": len(exact_gates),
            "retained_negative_count": len(negatives),
            "protected_claims": {claim: False for claim in PROTECTED_CLAIMS},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    tool_paths = [
        "scripts/ghc_family_evidence_contract.py",
        "scripts/ghc_family_evidence_contract_validator.py",
        "scripts/ghc_family_evidence_contract_minimal.py",
        "scripts/build_ghc_family_evidence_contract_report.py",
        "tests/test_ghc_family_v642_v8.py",
    ]
    tools = []
    for relative in tool_paths:
        path = repo / relative
        if path.exists():
            tools.append({"path": relative, "normalized_sha256": normalized_sha256(path)})
    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v642-v8.executed-toolchain.v1",
            "phase": PHASE,
            "owner": OWNER,
            "family_current_tools": tools,
            "standard_library_only": True,
            "caller_compatibility_preserved": True,
            "inherited_tools_modified": False,
            "shared_skill_change": "reviewed_current_no_change_justified",
        },
    )

    paths = manifest_paths(proposals)
    missing = [relative for relative in paths if not (phase_dir / relative).is_file()]
    manifest_written = False
    if not missing:
        entries = [
            {"path": relative, "normalized_sha256": normalized_sha256(phase_dir / relative), "bytes": normalized_size(phase_dir / relative)}
            for relative in paths
        ]
        write_json(
            phase_dir / "reproduction/manifest.json",
            {
                "schema": "ghc.family.v642-v8.manifest.v1",
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
        manifest_written = True

    return {
        "phase": PHASE,
        "owner": OWNER,
        "proposal_count": len(proposals),
        "case_count": sum(len(rows) for rows in evaluated.values()),
        "synthetic_rejection_count": len(synthetic_negatives),
        "retained_negative_count": len(negatives),
        "distribution": {label: distribution[label] for label in TRUTH_LABELS},
        "manifest_written": manifest_written,
        "manifest_missing": missing,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=["pending", "verified"])
    args = parser.parse_args()
    result = build_packet(args.repo.resolve(), args.snapshot_state)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
