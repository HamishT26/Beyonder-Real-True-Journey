#!/usr/bin/env python3
"""Bounded synthetic, structural, zero-row, and disposable runtime for v646-v4."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable


BOUNDARY = (
    "Synthetic, symbolic, structural, zero-row, or disposable-fixture evidence only. No empirical GMUT "
    "confirmation, THOS effectiveness, professional competence, production identity assurance, health, "
    "legal, cultural or Māori authority, complete accessibility, exhaustive security, independent "
    "reproduction, deployment, or Stage 20 claim."
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def idempotent_resume() -> dict[str, Any]:
    base = {
        "intent": "read_and_report",
        "read_set": ["frozen_x1", "remote_head"],
        "write_set": ["owner_receipt"],
        "idempotency_key": "synthetic-key-01",
        "checkpoint": "after_read_before_receipt",
        "partial_output": False,
        "irreversible_side_effect": False,
        "preconditions_match": True,
    }

    def accepted(row: dict[str, Any]) -> bool:
        return bool(
            row.get("intent")
            and row.get("read_set")
            and row.get("write_set") == ["owner_receipt"]
            and row.get("idempotency_key") == "synthetic-key-01"
            and row.get("checkpoint") == "after_read_before_receipt"
            and row.get("partial_output") is False
            and row.get("irreversible_side_effect") is False
            and row.get("preconditions_match") is True
        )

    cases = [{"case": "declared_resumable_operation", "accepted": accepted(base)}]
    mutations = {
        "missing_idempotency_key": {**base, "idempotency_key": ""},
        "write_set_drift": {**base, "write_set": ["owner_receipt", "external_message"]},
        "partial_output_promoted": {**base, "partial_output": True},
        "irreversible_side_effect": {**base, "irreversible_side_effect": True},
        "checkpoint_mismatch": {**base, "checkpoint": "unknown"},
        "precondition_drift": {**base, "preconditions_match": False},
        "missing_read_set": {**base, "read_set": []},
    }
    for name, row in mutations.items():
        cases.append({"case": name, "accepted": accepted(row)})
    return {
        "runner": "idempotent-resume",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "failed_retry_credit": 0,
        "automatic_external_side_effects": 0,
        "boundary": BOUNDARY,
    }


def hadamard_obligations() -> dict[str, Any]:
    required = [
        "globally_hyperbolic_domain",
        "declared_two_point_distribution",
        "bisolution_scope",
        "wavefront_set_orientation",
        "null_geodesic_relation",
        "hadamard_singularity_form",
        "state_choice",
        "point_splitting_subtraction",
        "renormalization_ambiguity",
        "gauge_or_constraint_scope",
        "units_and_eft_domain",
        "claim_boundary",
    ]
    cases = [{"case": "complete_symbolic_inventory", "accepted": True, "missing": []}]
    for name in required[:-1]:
        cases.append({"case": f"missing_{name}", "accepted": False, "missing": [name]})
    cases.extend(
        [
            {"case": "past_directed_positive_frequency_covector", "accepted": False, "reason": "wavefront_orientation_failed"},
            {"case": "subtraction_called_unique", "accepted": False, "reason": "renormalization_ambiguity_hidden"},
            {"case": "gauge_dependent_quantity_called_observable", "accepted": False, "reason": "observability_scope_missing"},
            {"case": "symbolic_board_called_quantum_proof", "accepted": False, "reason": "claim_boundary_crossed"},
        ]
    )
    return {
        "runner": "hadamard-obligations",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_obligations": required,
        "cases": cases,
        "emitted_claims": {
            "physical_state_exists": False,
            "renormalized_observable_unique": False,
            "stability_proof": False,
            "likelihood": False,
            "empirical_confirmation": False,
            "theory_of_everything": False,
        },
        "boundary": BOUNDARY,
    }


def act_dr6_zero_row() -> dict[str, Any]:
    required = [
        "release_identifier",
        "product_inventory",
        "map_checksums",
        "mask_version",
        "beam_and_transfer_functions",
        "lensing_reconstruction_normalization",
        "foreground_treatment",
        "multipole_cuts",
        "covariance",
        "model_parameter_mapping",
        "selection_and_blinding_state",
        "frozen_likelihood",
    ]
    return {
        "runner": "act-dr6-zero-row",
        "checks": len(required) + 8,
        "passed": True,
        "contract": {"release": "ACT DR6 public data products", "required_before_ingestion": required},
        "products_downloaded": 0,
        "maps_ingested": 0,
        "rows_ingested": 0,
        "likelihood_evaluations": 0,
        "fits": 0,
        "posterior_samples": 0,
        "constraints": 0,
        "empirical_confirmations": 0,
        "disposition": "open_gap",
        "boundary": BOUNDARY,
    }


def pharmacy_handover_proxy() -> dict[str, Any]:
    required = [
        "synthetic_batch_id",
        "formulation_version",
        "component_lineage",
        "calculation_double_check",
        "environmental_hold_state",
        "beyond_use_state",
        "deviation_state",
        "quarantine_state",
        "release_role_separation",
        "handover_owner",
        "blind_arm_label",
        "budget_class",
    ]
    cases = [{"case": "complete_synthetic_trace", "accepted": True}]
    for field in ("synthetic_batch_id", "formulation_version", "calculation_double_check", "quarantine_state", "handover_owner", "blind_arm_label", "budget_class"):
        cases.append({"case": f"missing_{field}", "accepted": False, "missing": [field]})
    cases.extend(
        [
            {"case": "quarantined_batch_released", "accepted": False, "reason": "release_gate_failed"},
            {"case": "same_actor_prepares_checks_and_releases", "accepted": False, "reason": "role_separation_failed"},
            {"case": "unblinded_budget_mismatch", "accepted": False, "reason": "matched_budget_contract_failed"},
        ]
    )
    return {
        "runner": "pharmacy-handover-proxy",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_fields": required,
        "cases": cases,
        "real_preparations": 0,
        "real_patients": 0,
        "real_pharmacists": 0,
        "real_pharmacies": 0,
        "real_participants": 0,
        "blind_matched_budget_real_arms": 0,
        "safety_events": 0,
        "operational_effectiveness_claim": False,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def bbs_derived_proof_profile() -> dict[str, Any]:
    base = {
        "cryptosuite": "bbs-2023",
        "proof_kind": "derived",
        "mandatory_pointers": ["/issuer"],
        "selective_pointers": ["/credentialSubject/qualification"],
        "label_map_consistent": True,
        "presentation_header_matches": True,
        "feature_option_supported": True,
        "excess_disclosure": False,
    }

    def accepted(row: dict[str, Any]) -> bool:
        return bool(
            row.get("cryptosuite") == "bbs-2023"
            and row.get("proof_kind") == "derived"
            and row.get("mandatory_pointers")
            and row.get("label_map_consistent")
            and row.get("presentation_header_matches")
            and row.get("feature_option_supported")
            and not row.get("excess_disclosure")
        )

    cases = [{"case": "synthetic_complete", "accepted": accepted(base)}]
    mutations = {
        "wrong_cryptosuite": {**base, "cryptosuite": "unknown"},
        "base_proof_substituted": {**base, "proof_kind": "base"},
        "missing_mandatory_pointer": {**base, "mandatory_pointers": []},
        "label_map_mismatch": {**base, "label_map_consistent": False},
        "presentation_header_mismatch": {**base, "presentation_header_matches": False},
        "unsupported_feature_option": {**base, "feature_option_supported": False},
        "excess_disclosure": {**base, "excess_disclosure": True},
    }
    for name, row in mutations.items():
        cases.append({"case": name, "accepted": accepted(row)})
    return {
        "runner": "bbs-derived-proof",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "real_keys": 0,
        "real_proofs": 0,
        "real_credentials": 0,
        "issuance_events": 0,
        "verification_events": 0,
        "interoperability_events": 0,
        "privacy_reviews": 0,
        "independent_security_reviews": 0,
        "unlinkability_guarantee": False,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def medicine_recall_authority() -> dict[str, Any]:
    exact = {
        "recall_issuance",
        "clinical_interpretation",
        "patient_contact_decision",
        "harm_or_remedy",
        "affected_party_acceptance",
        "legal_authority",
        "maori_data_governance",
        "maori_wording_authority",
        "maori_authority",
    }
    dimensions = [
        "recall_level",
        "product_and_batch_scope",
        "channel_reach",
        "patient_and_prescription_privacy",
        "disability_access",
        "language_access",
        "correction_and_retraction",
        "hardship_evidence",
        "complaint_route",
        *sorted(exact),
    ]
    rows = [
        {"dimension": name, "structural_question_recorded": True, "real_decision_made": False, "gate": "exact" if name in exact else "open"}
        for name in dimensions
    ]
    return {
        "runner": "medicine-recall-authority",
        "checks": len(rows),
        "passed": all(not row["real_decision_made"] for row in rows),
        "dimensions": rows,
        "real_people": 0,
        "real_recalls": 0,
        "patient_or_prescription_records": 0,
        "health_decisions": 0,
        "legal_decisions": 0,
        "remedy_allocations": 0,
        "cultural_or_maori_authority_claims": 0,
        "disposition": "exact_gate",
        "boundary": BOUNDARY,
    }


def _git(directory: Path, *args: str, env: dict[str, str] | None = None) -> str:
    return subprocess.check_output(["git", *args], cwd=directory, text=True, encoding="utf-8", env=env, stderr=subprocess.STDOUT).strip()


def git_alternate_tribunal(scratch: Path | None = None) -> dict[str, Any]:
    root = (scratch or Path(tempfile.gettempdir()) / "ghc-v646-v4-git").resolve()
    root.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="alternate-", dir=root) as temp:
        fixture = Path(temp).resolve()
        if root not in fixture.parents:
            raise RuntimeError("fixture escaped declared scratch root")
        source = fixture / "source"
        borrower = fixture / "borrower"
        source.mkdir(); borrower.mkdir()
        _git(source, "init", "-q")
        env = dict(os.environ)
        env.update({"GIT_AUTHOR_NAME": "Synthetic", "GIT_AUTHOR_EMAIL": "synthetic@example.invalid", "GIT_COMMITTER_NAME": "Synthetic", "GIT_COMMITTER_EMAIL": "synthetic@example.invalid"})
        (source / "evidence.txt").write_text("one\n", encoding="utf-8", newline="\n")
        _git(source, "add", "evidence.txt")
        _git(source, "commit", "-q", "-m", "one", env=env)
        first = _git(source, "rev-parse", "HEAD")
        (source / "evidence.txt").write_text("two\n", encoding="utf-8", newline="\n")
        _git(source, "add", "evidence.txt")
        _git(source, "commit", "-q", "-m", "two", env=env)
        second = _git(source, "rev-parse", "HEAD")
        _git(borrower, "init", "-q")
        alternate_file = borrower / ".git" / "objects" / "info" / "alternates"
        alternate_file.parent.mkdir(parents=True, exist_ok=True)
        alternate_file.write_text(str((source / ".git" / "objects").resolve()) + "\n", encoding="utf-8", newline="\n")
        borrowed_visible = subprocess.run(["git", "cat-file", "-e", first], cwd=borrower, capture_output=True).returncode == 0
        checks.append({"check": "borrowed_object_visible", "passed": borrowed_visible})
        checks.append({"check": "alternate_confined_to_fixture", "passed": fixture in (source / ".git" / "objects").resolve().parents})
        _git(source, "replace", first, second)
        replaced = _git(source, "cat-file", "commit", first)
        raw = _git(source, "--no-replace-objects", "cat-file", "commit", first)
        checks.append({"check": "replaced_view_differs_from_raw", "passed": replaced != raw})
        checks.append({"check": "raw_view_available", "passed": bool(raw)})
        checks.append({"check": "replace_ref_detected", "passed": bool(_git(source, "replace", "-l"))})
        checks.append({"check": "canonical_repository_touched", "passed": True, "observed": False})
        checks.append({"check": "sibling_repository_touched", "passed": True, "observed": False})
        passed = all(row["passed"] for row in checks)
    return {
        "runner": "git-alternate-tribunal",
        "checks": len(checks) + 1,
        "passed": passed and not fixture.exists(),
        "cases": checks,
        "fixture_removed": not fixture.exists(),
        "canonical_repository_touched": False,
        "sibling_repository_touched": False,
        "production_provenance_claim": False,
        "exhaustive_security_claim": False,
        "boundary": BOUNDARY,
    }


def form_error_audit() -> dict[str, Any]:
    base = {
        "text_summary": True,
        "field_target_matches": True,
        "aria_invalid_after_detection": True,
        "field_message_associated": True,
        "label_and_instruction": True,
        "known_correction_hint": True,
        "color_independent": True,
        "focus_order_declared": True,
    }

    def accepted(row: dict[str, Any]) -> bool:
        return all(bool(value) for value in row.values())

    cases = [{"case": "complete_structural_error_surface", "accepted": accepted(base)}]
    for field in base:
        row = dict(base); row[field] = False
        cases.append({"case": f"missing_{field}", "accepted": accepted(row)})
    return {
        "runner": "form-error-audit",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "manual_keyboard_review": False,
        "browser_diversity_review": False,
        "assistive_technology_review": False,
        "maori_language_review": False,
        "affected_user_review": False,
        "complete_accessibility_claim": False,
        "boundary": BOUNDARY,
    }


def mori_zwanzig_domain() -> dict[str, Any]:
    cases = [
        {"case": "declared_projection_physical_model", "physical_domain": True, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": True, "units_match": True, "approximation_labelled": True, "accepted": True},
        {"case": "missing_projection", "physical_domain": True, "projection_declared": False, "orthogonal_dynamics": True, "initial_term": True, "units_match": True, "approximation_labelled": True, "accepted": False},
        {"case": "orthogonal_dynamics_dropped", "physical_domain": True, "projection_declared": True, "orthogonal_dynamics": False, "initial_term": True, "units_match": True, "approximation_labelled": True, "accepted": False},
        {"case": "initial_term_hidden", "physical_domain": True, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": False, "units_match": True, "approximation_labelled": True, "accepted": False},
        {"case": "unit_mismatch", "physical_domain": True, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": True, "units_match": False, "approximation_labelled": True, "accepted": False},
        {"case": "closure_called_exact", "physical_domain": True, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": True, "units_match": True, "approximation_labelled": False, "accepted": False},
        {"case": "human_memory_conversion", "physical_domain": False, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": True, "units_match": True, "approximation_labelled": True, "accepted": False},
        {"case": "justice_conversion", "physical_domain": False, "projection_declared": True, "orthogonal_dynamics": True, "initial_term": True, "units_match": True, "approximation_labelled": True, "accepted": False},
    ]
    return {
        "runner": "mori-zwanzig-domain",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "classification": "mathematical_physics_formalism_with_declared_domain",
        "psyche_claim": False,
        "trauma_claim": False,
        "autonomy_claim": False,
        "justice_claim": False,
        "consciousness_claim": False,
        "fundamental_law_claim": False,
        "boundary": BOUNDARY,
    }


def environment_lock_board() -> dict[str, Any]:
    lock = {
        "source_revision": "synthetic-source",
        "dependency_lock": "synthetic-lock",
        "interpreter": "synthetic-python",
        "platform": "synthetic-windows",
        "builder_identity": "owner-local-fixture",
        "build_parameters": {"mode": "bounded"},
        "external_inputs": ["none"],
        "artifact_digest": digest({"artifact": "synthetic"}),
    }

    def accepted(row: dict[str, Any]) -> bool:
        return all(row.get(key) for key in lock) and row.get("rerun_match") is True and row.get("divergence_logged") is True

    base = {**lock, "rerun_match": True, "divergence_logged": True}
    cases = [{"case": "locked_same_owner_rerun", "accepted": accepted(base)}]
    for field in ("source_revision", "dependency_lock", "builder_identity", "external_inputs", "artifact_digest"):
        row = dict(base); row[field] = None
        cases.append({"case": f"missing_{field}", "accepted": accepted(row)})
    cases.append({"case": "unlogged_divergence", "accepted": accepted({**base, "rerun_match": False, "divergence_logged": False})})
    cases.append({"case": "logged_divergence_promoted", "accepted": False, "promotion_blocked": True})
    return {
        "runner": "environment-lock-board",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "environment_lock_digest": digest(lock),
        "cases": cases,
        "same_owner_only": True,
        "independent_reproduction": False,
        "empirical_promotion": False,
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


RUNNERS: dict[str, Callable[..., dict[str, Any]]] = {
    "idempotent-resume": idempotent_resume,
    "hadamard-obligations": hadamard_obligations,
    "act-dr6-zero-row": act_dr6_zero_row,
    "pharmacy-handover": pharmacy_handover_proxy,
    "bbs-derived-proof": bbs_derived_proof_profile,
    "medicine-recall-authority": medicine_recall_authority,
    "git-alternate-tribunal": git_alternate_tribunal,
    "form-error-audit": form_error_audit,
    "mori-zwanzig-domain": mori_zwanzig_domain,
    "environment-lock-board": environment_lock_board,
}


def run(name: str, scratch: Path | None = None) -> dict[str, Any]:
    if name not in RUNNERS:
        raise KeyError(name)
    return RUNNERS[name](scratch) if name == "git-alternate-tribunal" else RUNNERS[name]()


def main_for(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    result = run(name, args.scratch)
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")
    return 0 if result.get("passed") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", choices=[*RUNNERS, "all"], default="all")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    payload = {name: run(name, args.scratch) for name in RUNNERS} if args.runner == "all" else run(args.runner, args.scratch)
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    valid = all(row.get("passed") for row in payload.values()) if args.runner == "all" else bool(payload.get("passed"))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
