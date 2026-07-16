#!/usr/bin/env python3
"""Bounded synthetic, structural, zero-row, and disposable runtime for v646-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import tempfile
import zlib
from pathlib import Path
from typing import Any, Callable


BOUNDARY = (
    "Synthetic, symbolic, structural, zero-row, or disposable-fixture evidence only. "
    "No empirical GMUT confirmation, THOS effectiveness, professional competence, production identity "
    "assurance, veterinary or biosecurity decision, legal, cultural or Māori authority, complete privacy "
    "or accessibility, exhaustive security, independent reproduction, deployment, or Stage 20 claim."
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def contract_result(
    surface: str,
    outcome: str,
    positive: dict[str, Any],
    mutations: list[tuple[str, dict[str, Any]]],
    accepts: Callable[[dict[str, Any]], bool],
    *,
    zero_counts: dict[str, int] | None = None,
    reservations: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cases = [{"case": "declared_bounded_fixture", "accepted": accepts(positive), "digest": digest(positive)}]
    for name, row in mutations:
        cases.append({"case": name, "accepted": accepts(row), "digest": digest(row)})
    passed = bool(cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]))
    result = {
        "surface": surface,
        "outcome": outcome,
        "checks": len(cases),
        "passed": passed,
        "positive_count": 1,
        "mutations_executed": len(mutations),
        "mutations_rejected": sum(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "zero_counts": zero_counts or {},
        "reservations": reservations or [],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }
    if extra:
        result.update(extra)
    return result


def optimistic_concurrency() -> dict[str, Any]:
    base = {
        "expected_revision": 12,
        "observed_revision": 12,
        "read_set": ["frozen_x1", "owner_state_r12"],
        "write_set": ["owner_conflict_receipt"],
        "protected_intent_digest": "intent-a",
        "rebased_intent_digest": "intent-a",
        "conflict_visible": True,
        "partial_output": False,
        "external_side_effect": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("expected_revision") == row.get("observed_revision")
            and row.get("read_set")
            and row.get("write_set") == ["owner_conflict_receipt"]
            and row.get("protected_intent_digest") == row.get("rebased_intent_digest")
            and row.get("conflict_visible") is True
            and row.get("partial_output") is False
            and row.get("external_side_effect") is False
        )

    mutations = [
        ("stale_expected_revision", {**base, "expected_revision": 11}),
        ("hidden_conflict", {**base, "conflict_visible": False}),
        ("read_set_missing", {**base, "read_set": []}),
        ("write_set_drift", {**base, "write_set": ["owner_conflict_receipt", "external_message"]}),
        ("protected_intent_changed", {**base, "rebased_intent_digest": "intent-b"}),
        ("partial_output_promoted", {**base, "partial_output": True}),
        ("automatic_external_side_effect", {**base, "external_side_effect": True}),
    ]
    return contract_result("optimistic-concurrency", "completed", base, mutations, accepts)


def peierls_bracket() -> dict[str, Any]:
    required = {
        "linearized_euler_lagrange_operator",
        "advanced_green_operator",
        "retarded_green_operator",
        "causal_propagator",
        "compact_functional_derivative_support",
        "gauge_invariant_observable",
        "antisymmetry_scope",
        "jacobi_assumptions",
        "units",
        "eft_domain",
    }
    base = {
        "obligations": sorted(required),
        "causal_order": "retarded_minus_advanced",
        "support_inside_domain": True,
        "gauge_variant_promoted": False,
        "physical_claim": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            required <= set(row.get("obligations", []))
            and row.get("causal_order") == "retarded_minus_advanced"
            and row.get("support_inside_domain") is True
            and row.get("gauge_variant_promoted") is False
            and row.get("physical_claim") is False
        )

    mutations = [
        ("advanced_retarded_swapped", {**base, "causal_order": "advanced_minus_retarded"}),
        ("green_operator_domain_omitted", {**base, "support_inside_domain": False}),
        ("gauge_variant_promoted", {**base, "gauge_variant_promoted": True}),
        ("antisymmetry_missing", {**base, "obligations": sorted(required - {"antisymmetry_scope"})}),
        ("jacobi_assumptions_missing", {**base, "obligations": sorted(required - {"jacobi_assumptions"})}),
        ("units_missing", {**base, "obligations": sorted(required - {"units"})}),
        ("symbolic_bracket_called_physical", {**base, "physical_claim": True}),
    ]
    return contract_result(
        "peierls-bracket",
        "completed",
        base,
        mutations,
        accepts,
        reservations=["physical observable algebra", "quantization", "stability theorem", "likelihood", "parameter constraint", "Theory of Everything"],
    )


def rubin_dp1_zero_row() -> dict[str, Any]:
    base = {
        "release": "DP1 commissioning data",
        "account_used": False,
        "downloads": 0,
        "real_rows": 0,
        "shape_columns_called_calibrated_shear": False,
        "known_issues_versioned": True,
        "selection_frozen": False,
        "covariance_available": False,
        "likelihoods": 0,
        "constraints": 0,
        "empirical_claims": 0,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("release") == "DP1 commissioning data"
            and row.get("account_used") is False
            and all(row.get(key) == 0 for key in ("downloads", "real_rows", "likelihoods", "constraints", "empirical_claims"))
            and row.get("shape_columns_called_calibrated_shear") is False
            and row.get("known_issues_versioned") is True
            and row.get("selection_frozen") is False
            and row.get("covariance_available") is False
        )

    mutations = [
        ("protected_account_access", {**base, "account_used": True}),
        ("one_download", {**base, "downloads": 1}),
        ("one_real_row", {**base, "real_rows": 1}),
        ("shape_called_calibrated_shear", {**base, "shape_columns_called_calibrated_shear": True}),
        ("known_issue_version_omitted", {**base, "known_issues_versioned": False}),
        ("fabricated_likelihood", {**base, "likelihoods": 1}),
        ("fabricated_constraint", {**base, "constraints": 1, "empirical_claims": 1}),
    ]
    return contract_result(
        "rubin-dp1-zero-row",
        "open_gap",
        base,
        mutations,
        accepts,
        zero_counts={"accounts": 0, "downloads": 0, "real_rows": 0, "shear_estimates": 0, "likelihoods": 0, "fits": 0, "constraints": 0, "empirical_claims": 0},
        reservations=["authorized data access", "frozen calibrated product", "selection and covariance", "preregistered likelihood", "independent review"],
    )


def veterinary_handover_proxy() -> dict[str, Any]:
    base = {
        "synthetic": True,
        "accession_id": "synthetic-accession-a",
        "specimen_condition": "synthetic_acceptable",
        "custody_events": 3,
        "method_version": "synthetic-v1",
        "amendment_reason": "synthetic_transcription_correction",
        "reviewer_separate": True,
        "escalation_is_placeholder": True,
        "matched_budget": 12,
        "blind_arm_label": "masked-a",
        "workload_recorded": True,
        "next_shift_owner": "synthetic-role-b",
        "real_entities": 0,
        "diagnosis_or_notification": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("synthetic") is True
            and all(row.get(key) for key in ("accession_id", "specimen_condition", "custody_events", "method_version", "amendment_reason", "next_shift_owner"))
            and row.get("reviewer_separate") is True
            and row.get("escalation_is_placeholder") is True
            and row.get("matched_budget") == 12
            and str(row.get("blind_arm_label", "")).startswith("masked-")
            and row.get("workload_recorded") is True
            and row.get("real_entities") == 0
            and row.get("diagnosis_or_notification") is False
        )

    mutations = [
        ("real_entity_inserted", {**base, "real_entities": 1}),
        ("custody_event_missing", {**base, "custody_events": 0}),
        ("amendment_reason_missing", {**base, "amendment_reason": ""}),
        ("same_reviewer", {**base, "reviewer_separate": False}),
        ("unblinded_arm", {**base, "blind_arm_label": "THOS"}),
        ("workload_not_recorded", {**base, "workload_recorded": False}),
        ("diagnosis_or_notification_attempted", {**base, "diagnosis_or_notification": True}),
    ]
    return contract_result(
        "veterinary-handover-proxy",
        "represented",
        base,
        mutations,
        accepts,
        zero_counts={"real_animals": 0, "clients": 0, "farms": 0, "workers": 0, "laboratories": 0, "specimens": 0, "diagnoses": 0, "notifications": 0, "blind_real_arms": 0, "safety_events": 0, "effectiveness_estimates": 0},
        reservations=["veterinary competence", "laboratory authority", "biosecurity decision", "real participant evidence", "independent review"],
    )


def transaction_data_profile() -> dict[str, Any]:
    base = {
        "recognized_type": "payment_data",
        "transaction_id": "synthetic-collision-resistant-id",
        "credential_ids": ["cred-query-a"],
        "dcql_ids": ["cred-query-a"],
        "holder_binding_required": True,
        "nonce_bound": True,
        "client_bound": True,
        "hash_algorithm": "sha-256",
        "processed_claim": "synthetic-only",
        "response_encrypted": True,
        "disclosed_fields": ["transaction_id"],
        "authorization_claim": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("recognized_type") == "payment_data"
            and row.get("transaction_id")
            and row.get("credential_ids") == row.get("dcql_ids") == ["cred-query-a"]
            and row.get("holder_binding_required") is True
            and row.get("nonce_bound") is True
            and row.get("client_bound") is True
            and row.get("hash_algorithm") == "sha-256"
            and row.get("processed_claim") == "synthetic-only"
            and row.get("response_encrypted") is True
            and row.get("disclosed_fields") == ["transaction_id"]
            and row.get("authorization_claim") is False
        )

    mutations = [
        ("unknown_transaction_type", {**base, "recognized_type": "unknown"}),
        ("credential_id_mismatch", {**base, "credential_ids": ["cred-query-b"]}),
        ("holder_binding_disabled", {**base, "holder_binding_required": False}),
        ("nonce_drift", {**base, "nonce_bound": False}),
        ("client_drift", {**base, "client_bound": False}),
        ("unsupported_hash", {**base, "hash_algorithm": "synthetic-unknown"}),
        ("response_leak_and_authorization", {**base, "disclosed_fields": ["transaction_id", "account"], "authorization_claim": True}),
    ]
    return contract_result(
        "transaction-data-profile",
        "represented",
        base,
        mutations,
        accepts,
        zero_counts={"real_keys": 0, "credentials": 0, "wallets": 0, "verifiers": 0, "transactions": 0, "issuance": 0, "resolution": 0, "status_or_revocation": 0, "interoperability_events": 0},
        reservations=["standards-conformant real cryptography", "live wallet and verifier interoperability", "privacy and independent security review", "trust governance"],
    )


def animal_disease_authority() -> dict[str, Any]:
    reserved = [
        "veterinary", "laboratory", "biosecurity", "animal_welfare", "worker_safety", "privacy",
        "emergency", "public_health", "legal", "affected_party", "tangata_whenua_iwi_hapu", "maori",
    ]
    base = {
        "synthetic": True,
        "protected_farm_data": False,
        "software_diagnosis": False,
        "software_notification": False,
        "movement_control": False,
        "public_communication": False,
        "remedy_allocation": False,
        "legal_interpretation": False,
        "cultural_or_maori_claim": False,
        "reserved_authorities": reserved,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("synthetic") is True
            and all(row.get(key) is False for key in ("protected_farm_data", "software_diagnosis", "software_notification", "movement_control", "public_communication", "remedy_allocation", "legal_interpretation", "cultural_or_maori_claim"))
            and row.get("reserved_authorities") == reserved
        )

    mutations = [
        ("protected_farm_data", {**base, "protected_farm_data": True}),
        ("software_diagnosis", {**base, "software_diagnosis": True}),
        ("software_notification", {**base, "software_notification": True}),
        ("movement_control", {**base, "movement_control": True}),
        ("public_communication", {**base, "public_communication": True}),
        ("remedy_or_legal_decision", {**base, "remedy_allocation": True, "legal_interpretation": True}),
        ("maori_authority_claim", {**base, "cultural_or_maori_claim": True}),
    ]
    return contract_result(
        "animal-disease-authority",
        "exact_gate",
        base,
        mutations,
        accepts,
        zero_counts={"real_cases": 0, "diagnoses": 0, "notifications": 0, "movement_controls": 0, "public_messages": 0, "remedy_allocations": 0, "legal_interpretations": 0, "cultural_decisions": 0},
        reservations=reserved,
    )


def reftable_tribunal(scratch: Path | None = None) -> dict[str, Any]:
    base = {
        "magic": "REFT",
        "version": 1,
        "hash_id": "sha1",
        "block_size": 4096,
        "min_update_index": 7,
        "max_update_index": 9,
        "footer_crc_valid": True,
        "unique_ref_keys": True,
        "reflog_reverse_update_order": True,
        "stack_newest_last": True,
        "deletion_record_explicit": True,
        "compaction_preserves_latest": True,
        "confined": True,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("magic") == "REFT"
            and row.get("version") in {1, 2}
            and row.get("hash_id") in {"sha1", "sha256"}
            and row.get("block_size", 0) >= 256
            and 0 <= row.get("min_update_index", -1) <= row.get("max_update_index", -1)
            and all(row.get(key) is True for key in ("footer_crc_valid", "unique_ref_keys", "reflog_reverse_update_order", "stack_newest_last", "deletion_record_explicit", "compaction_preserves_latest", "confined"))
        )

    mutations = [
        ("bad_magic", {**base, "magic": "XXXX"}),
        ("unsupported_version", {**base, "version": 99}),
        ("update_index_inversion", {**base, "min_update_index": 10}),
        ("crc_corruption", {**base, "footer_crc_valid": False}),
        ("duplicate_ref_key", {**base, "unique_ref_keys": False}),
        ("reversed_stack_and_reflog", {**base, "stack_newest_last": False, "reflog_reverse_update_order": False}),
        ("unconfined_compaction", {**base, "confined": False, "compaction_preserves_latest": False}),
    ]
    root = scratch or Path.cwd() / ".ghc-family-runtime-v646-v5"
    root.mkdir(parents=True, exist_ok=True)
    fixture_removed = False
    with tempfile.TemporaryDirectory(prefix="reftable-", dir=root) as temp:
        fixture = Path(temp) / "synthetic.reftable"
        header = b"REFT" + struct.pack(">B3xIQQ", 1, 4096, 7, 9)
        fixture.write_bytes(header + struct.pack(">I", zlib.crc32(header)))
        fixture_header_valid = fixture.read_bytes()[:4] == b"REFT"
    fixture_removed = not Path(temp).exists()
    result = contract_result(
        "reftable-tribunal", "completed", base, mutations, accepts,
        extra={"fixture_header_valid": fixture_header_valid, "fixture_removed": fixture_removed, "canonical_repository_mutations": 0, "sibling_lane_mutations": 0},
        reservations=["production compatibility", "supply-chain assurance", "exhaustive Git security"],
    )
    result["passed"] = bool(result["passed"] and fixture_header_valid and fixture_removed)
    return result


def popover_audit() -> dict[str, Any]:
    base = {
        "mode": "auto",
        "target_exists": True,
        "action": "toggle",
        "same_tree": True,
        "trigger_named": True,
        "close_path_visible": True,
        "light_dismiss_expected": True,
        "reading_order_declared": True,
        "focus_behavior_declared": True,
        "tooltip_substitutes_interactive_content": False,
        "manual_evaluation_reserved": True,
    }

    def accepts(row: dict[str, Any]) -> bool:
        mode = row.get("mode")
        return bool(
            mode in {"auto", "manual", "hint"}
            and row.get("target_exists") is True
            and row.get("action") in {"show", "hide", "toggle"}
            and row.get("same_tree") is True
            and row.get("trigger_named") is True
            and row.get("close_path_visible") is True
            and row.get("light_dismiss_expected") is (mode != "manual")
            and row.get("reading_order_declared") is True
            and row.get("focus_behavior_declared") is True
            and row.get("tooltip_substitutes_interactive_content") is False
            and row.get("manual_evaluation_reserved") is True
        )

    mutations = [
        ("broken_target", {**base, "target_exists": False}),
        ("invalid_action", {**base, "action": "launch"}),
        ("cross_tree_target", {**base, "same_tree": False}),
        ("manual_called_light_dismissible", {**base, "mode": "manual", "light_dismiss_expected": True}),
        ("missing_reading_order", {**base, "reading_order_declared": False}),
        ("focus_inferred", {**base, "focus_behavior_declared": False}),
        ("tooltip_substitution_and_no_reservation", {**base, "tooltip_substitutes_interactive_content": True, "manual_evaluation_reserved": False}),
    ]
    return contract_result(
        "popover-audit", "completed", base, mutations, accepts,
        reservations=["manual keyboard", "browser diversity", "assistive technology", "Māori-language", "cognitive accessibility", "affected-user evaluation", "complete accessibility conformance"],
    )


def clapeyron_classifier() -> dict[str, Any]:
    base = {
        "phase_a": "synthetic_solid",
        "phase_b": "synthetic_liquid",
        "coexistence": True,
        "temperature_k": 300.0,
        "entropy_change_j_per_mol_k": 10.0,
        "latent_heat_j_per_mol": 3000.0,
        "molar_volume_change_m3_per_mol": 0.002,
        "slope_pa_per_k": 5000.0,
        "first_order_domain": True,
        "critical_endpoint": False,
        "approximation": "exact_declared_inputs_only",
        "psyche_conversion": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        dv = row.get("molar_volume_change_m3_per_mol", 0.0)
        temperature = row.get("temperature_k", 0.0)
        if not dv or not temperature:
            return False
        entropy_slope = row.get("entropy_change_j_per_mol_k", 0.0) / dv
        latent_slope = row.get("latent_heat_j_per_mol", 0.0) / (temperature * dv)
        return bool(
            row.get("phase_a") and row.get("phase_b") and row.get("phase_a") != row.get("phase_b")
            and row.get("coexistence") is True
            and abs(entropy_slope - row.get("slope_pa_per_k", float("inf"))) < 1e-9
            and abs(latent_slope - row.get("slope_pa_per_k", float("inf"))) < 1e-9
            and row.get("first_order_domain") is True
            and row.get("critical_endpoint") is False
            and row.get("approximation") == "exact_declared_inputs_only"
            and row.get("psyche_conversion") is False
        )

    mutations = [
        ("phase_identity_missing", {**base, "phase_b": "synthetic_solid"}),
        ("not_on_coexistence_curve", {**base, "coexistence": False}),
        ("zero_volume_change", {**base, "molar_volume_change_m3_per_mol": 0.0}),
        ("latent_heat_sign_drift", {**base, "latent_heat_j_per_mol": -3000.0}),
        ("unit_scaled_slope", {**base, "slope_pa_per_k": 5.0}),
        ("critical_endpoint_crossed", {**base, "critical_endpoint": True, "first_order_domain": False}),
        ("psyche_transition_claim", {**base, "psyche_conversion": True}),
    ]
    return contract_result(
        "clapeyron-classifier", "completed", base, mutations, accepts,
        reservations=["participant inference", "psyche transition", "social transition", "consciousness", "fundamental law"],
    )


def metric_semantics_board() -> dict[str, Any]:
    base = {
        "metric_id": "synthetic-balanced-accuracy",
        "metric_version": "1.0",
        "labels": ["negative", "positive"],
        "positive_class": "positive",
        "score_direction": "higher_is_better",
        "averaging": "macro",
        "threshold": 0.5,
        "matrix_orientation": "rows_actual_columns_predicted",
        "all_classes_present": True,
        "uncertainty_target": "synthetic_bootstrap_interval",
        "comparison_scope": "same_frozen_fixture",
        "stage20_promotion": False,
    }

    def accepts(row: dict[str, Any]) -> bool:
        return bool(
            row.get("metric_id") == "synthetic-balanced-accuracy"
            and row.get("metric_version") == "1.0"
            and row.get("labels") == ["negative", "positive"]
            and row.get("positive_class") == "positive"
            and row.get("score_direction") == "higher_is_better"
            and row.get("averaging") == "macro"
            and row.get("threshold") == 0.5
            and row.get("matrix_orientation") == "rows_actual_columns_predicted"
            and row.get("all_classes_present") is True
            and row.get("uncertainty_target") == "synthetic_bootstrap_interval"
            and row.get("comparison_scope") == "same_frozen_fixture"
            and row.get("stage20_promotion") is False
        )

    mutations = [
        ("metric_version_drift", {**base, "metric_version": "2.0"}),
        ("label_permutation", {**base, "labels": ["positive", "negative"]}),
        ("positive_class_inversion", {**base, "positive_class": "negative"}),
        ("score_direction_reversal", {**base, "score_direction": "lower_is_better"}),
        ("averaging_and_threshold_drift", {**base, "averaging": "micro", "threshold": 0.7}),
        ("matrix_transposed_and_class_missing", {**base, "matrix_orientation": "columns_actual_rows_predicted", "all_classes_present": False}),
        ("uncertainty_missing_and_stage20_promoted", {**base, "uncertainty_target": "", "stage20_promotion": True}),
    ]
    return contract_result(
        "metric-semantics-board", "completed", base, mutations, accepts,
        reservations=["benchmark authority", "deployment", "proof or canon", "independent reproduction", "Stage 20"],
        extra={"terminal_verdict": "NOT_READY_FOR_STAGE_20"},
    )


RUNNERS: dict[str, Callable[..., dict[str, Any]]] = {
    "optimistic-concurrency": optimistic_concurrency,
    "peierls-bracket": peierls_bracket,
    "rubin-dp1-zero-row": rubin_dp1_zero_row,
    "veterinary-handover-proxy": veterinary_handover_proxy,
    "transaction-data-profile": transaction_data_profile,
    "animal-disease-authority": animal_disease_authority,
    "reftable-tribunal": reftable_tribunal,
    "popover-audit": popover_audit,
    "clapeyron-classifier": clapeyron_classifier,
    "metric-semantics-board": metric_semantics_board,
}


def run(name: str, scratch: Path | None = None) -> dict[str, Any]:
    if name == "reftable-tribunal":
        return reftable_tribunal(scratch)
    return RUNNERS[name]()


def run_all(scratch: Path | None = None) -> list[dict[str, Any]]:
    return [run(name, scratch) for name in RUNNERS]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", choices=[*RUNNERS, "all"], default="all")
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    rows = run_all(args.scratch) if args.surface == "all" else [run(args.surface, args.scratch)]
    payload = {
        "schema": "ghc.family.v646-v5.runtime.v1",
        "surface_count": len(rows),
        "mutation_count": sum(row["mutations_executed"] for row in rows),
        "passed": all(row["passed"] for row in rows),
        "rows": rows,
        "boundary": BOUNDARY,
    }
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
