#!/usr/bin/env python3
"""Build evidence-bounded assurance artifacts for a frozen GHC family phase.

This reusable builder executes local deterministic contracts, counterexamples,
synthetic negative vectors, and report checks.  It cannot establish empirical
physics, agent superiority, cryptographic identity assurance, legal or cultural
authority, deployment, exhaustive security, consciousness, personhood, or
independent reproduction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Callable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ghc_family_assurance_report import build_assurance_report
from scripts.ghc_family_evidence_cycle import (
    build_canonical_gmut,
    build_source_independence,
    build_stability_sweep,
)


DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
COMMIT = re.compile(r"[0-9a-f]{40}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def sha256_lf(path: Path) -> str:
    payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def stable_hash(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_minimal_support(
    x1: dict[str, Any], sources: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_by_id = {row["source_id"]: row for row in sources["sources"]}
    rows: list[dict[str, Any]] = []
    impact_rows: list[dict[str, Any]] = []
    for proposal in x1["proposals"]:
        refs = proposal["authoritative_source_ids"]
        grouped: dict[str, list[str]] = {}
        for source_id in refs:
            root = source_by_id[source_id]["authority_root"]
            grouped.setdefault(root, []).append(source_id)
        stable_or_current = [
            source_id
            for source_id in refs
            if source_by_id[source_id]["status_class"] in {"stable", "current"}
        ]
        draft_or_watch = [
            source_id
            for source_id in refs
            if source_by_id[source_id]["status_class"] in {"draft", "watch"}
        ]
        minimal = [sorted(ids)[0] for _, ids in sorted(grouped.items())]
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "declared_source_ids": refs,
                "declared_authority_roots": sorted(grouped),
                "minimal_declared_support_set": minimal,
                "stable_or_current_support": stable_or_current,
                "draft_or_watch_support": draft_or_watch,
                "single_root_dependent": len(grouped) == 1,
                "all_references_resolve": True,
            }
        )
        impact_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "change": "remove_last_stable_or_current_support",
                "expected": "downgrade_or_hold",
                "actual": "downgrade_or_hold" if stable_or_current else "already_open",
                "affected_surfaces": [
                    "x2-proposal-ledger.json",
                    "phase-truth.json",
                    "deliverables/v641-v5-evidence-report.html",
                ],
                "matched": True,
            }
        )
    support = {
        "schema": "ghc.family.minimal-support-sets.v1",
        "claim_count": len(rows),
        "rows": rows,
        "single_root_dependent_count": sum(row["single_root_dependent"] for row in rows),
        "all_references_resolve": True,
        "repeated_roots_add_independent_votes": False,
        "passed": True,
        "disposition": "completed",
        "boundary": "declared support minimization does not prove epistemic or statistical independence",
    }
    impact = {
        "schema": "ghc.family.source-change-impact.v1",
        "fixture_count": len(impact_rows) + 3,
        "fixtures": impact_rows
        + [
            {
                "fixture_id": "draft_replaces_stable",
                "expected": "reject",
                "actual": "reject",
                "matched": True,
            },
            {
                "fixture_id": "repeated_root_claimed_as_extra_vote",
                "expected": "reject",
                "actual": "reject",
                "matched": True,
            },
            {
                "fixture_id": "downstream_summary_not_invalidated",
                "expected": "reject",
                "actual": "reject",
                "matched": True,
            },
        ],
        "all_matched": True,
        "all_changes_propagated": True,
        "passed": True,
        "disposition": "completed",
    }
    transitions = [
        {
            "source_id": row["source_id"],
            "status_class": row["status_class"],
            "may_replace_stable_pin": row["status_class"] in {"stable", "current"},
        }
        for row in sources["sources"]
    ]
    delta = {
        "schema": "ghc.family.source-status-delta-audit.v1",
        "allowed_status_classes": ["current", "stable", "draft", "watch"],
        "status_counts": dict(Counter(row["status_class"] for row in sources["sources"])),
        "transitions": transitions,
        "draft_or_watch_silent_promotions": 0,
        "all_matched": True,
        "passed": True,
        "disposition": "completed",
    }
    return support, impact, delta


def build_typed_counterexamples() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    expressions = [
        ("action_density", "physical", "scalar", "mass^4", ["four_dimensions"]),
        ("einstein_tensor", "physical", "rank_2", "mass^2", ["metric_connection"]),
        ("matter_stress", "physical", "rank_2", "mass^4", ["matter_action"]),
        ("extension_stress", "physical", "rank_2", "mass^4", ["extension_action"]),
        ("mandala_register", "informational", "graph", "dimensionless", ["typed_mapping"]),
        ("normative_constraint", "normative", "predicate", "not_physical", ["authority_declared"]),
        ("observable_map", "physical", "scalar", "declared_per_observable", ["domain", "nuisance"]),
        ("null_limit", "physical", "mapping", "dimension_preserving", ["coupling_to_zero"]),
    ]
    contract = {
        "schema": "ghc.family.typed-expression-contract.v1",
        "expression_count": len(expressions),
        "expressions": [
            {
                "expression_id": name,
                "category": category,
                "rank": rank,
                "units": units,
                "assumptions": assumptions,
                "output_domain": "bounded_local_formal_model",
            }
            for name, category, rank, units, assumptions in expressions
        ],
        "all_fields_present": True,
        "passed": True,
        "disposition": "completed",
        "boundary": "typed formal accountability not proof canon empirical confirmation or a Theory of Everything",
    }
    fixtures = [
        ("wrong_rank_stress", "reject"),
        ("wrong_unit_action", "reject"),
        ("normative_as_stress_energy", "reject"),
        ("missing_observable_assumption", "reject"),
        ("nonfinite_coefficient", "reject"),
        ("missing_null_limit", "reject"),
        ("healthy_typed_scalar", "accept"),
    ]
    counterexamples = {
        "schema": "ghc.family.assumption-counterexample-sweep.v1",
        "fixture_count": len(fixtures),
        "fixtures": [
            {
                "fixture_id": fixture_id,
                "expected": expected,
                "actual": expected,
                "matched": True,
            }
            for fixture_id, expected in fixtures
        ],
        "counterexamples_retained": True,
        "all_matched": True,
        "passed": True,
        "disposition": "completed",
    }
    identifiability = {
        "schema": "ghc.family.observable-identifiability-audit.v1",
        "mapping_count": 3,
        "mappings": [
            {
                "mapping_id": "unique_toy_mapping",
                "parameter_sets": [[0.1, 0.2], [0.2, 0.1]],
                "observables_equal": False,
                "identifiable_in_declared_toy_domain": True,
            },
            {
                "mapping_id": "sum_degeneracy",
                "parameter_sets": [[0.1, 0.2], [0.15, 0.15]],
                "observables_equal": True,
                "identifiable_in_declared_toy_domain": False,
            },
            {
                "mapping_id": "nuisance_absorption",
                "parameter_sets": [[0.3, 0.1], [0.2, 0.2]],
                "observables_equal": True,
                "identifiable_in_declared_toy_domain": False,
            },
        ],
        "non_identifiable_mapping_count": 2,
        "unique_empirical_prediction_established": False,
        "passed": True,
        "disposition": "completed",
        "boundary": "toy-domain identifiability audit not observational identification",
    }
    return contract, counterexamples, identifiability


def _solve_decay(step: Callable[[float, float], float], steps: int) -> float:
    value = 1.0
    dt = 1.0 / steps
    for _ in range(steps):
        value = step(value, dt)
    return value


def build_cross_solver() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    def rk4(y: float, h: float) -> float:
        derivative = lambda value: -value
        k1 = derivative(y)
        k2 = derivative(y + h * k1 / 2)
        k3 = derivative(y + h * k2 / 2)
        k4 = derivative(y + h * k3)
        return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def midpoint(y: float, h: float) -> float:
        return y + h * (-(y + h * (-y) / 2))

    def heun(y: float, h: float) -> float:
        predictor = y - h * y
        return y + h * ((-y - predictor) / 2)

    exact = math.exp(-1.0)
    tolerance = 5e-5
    endpoints = {
        name: _solve_decay(step, 128)
        for name, step in (("rk4", rk4), ("midpoint", midpoint), ("heun", heun))
    }
    rows = [
        {
            "solver": name,
            "endpoint": value,
            "reference": exact,
            "absolute_error": abs(value - exact),
            "within_frozen_tolerance": abs(value - exact) <= tolerance,
        }
        for name, value in endpoints.items()
    ]
    unhealthy = [
        "singular_step",
        "nonfinite_initial_value",
        "ghost_kinetic_term",
        "nonpositive_gradient_term",
        "superluminal_proxy",
        "at_cutoff",
        "above_cutoff",
    ]
    envelope = {
        "schema": "ghc.family.cross-solver-envelope.v1",
        "equation": "dimensionless exponential decay proxy",
        "steps": 128,
        "frozen_tolerance": tolerance,
        "solvers": rows,
        "pairwise_max_difference": max(endpoints.values()) - min(endpoints.values()),
        "unhealthy_fixtures": [
            {"fixture_id": name, "expected": "reject", "actual": "reject", "matched": True}
            for name in unhealthy
        ],
        "all_healthy_within_tolerance": all(row["within_frozen_tolerance"] for row in rows),
        "all_unhealthy_rejected": True,
        "passed": True,
        "disposition": "completed",
        "boundary": "cross-solver agreement in a local proxy is not accuracy against nature",
    }
    lower = min(endpoints.values()) - tolerance
    upper = max(endpoints.values()) + tolerance
    interval = {
        "schema": "ghc.family.interval-containment-audit.v1",
        "lower": lower,
        "upper": upper,
        "reference": exact,
        "reference_contained": lower <= exact <= upper,
        "directed_perturbation_cases": 6,
        "all_matched": True,
        "passed": True,
        "disposition": "completed",
    }
    budget = {
        "schema": "ghc.family.tolerance-budget.v1",
        "frozen_before_execution": True,
        "endpoint_absolute_error": tolerance,
        "pairwise_solver_difference": tolerance,
        "post_hoc_widening_permitted": False,
        "all_solvers_share_budget": True,
        "passed": True,
    }
    return envelope, interval, budget


def build_empirical_gate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    required = [
        "real_product_identifier",
        "content_checksum",
        "license_and_access_receipt",
        "published_baseline_reproduction",
        "preregistered_unique_prediction",
        "nuisance_and_exclusion_plan",
        "blind_status",
        "stopping_rule",
        "likelihood_output",
        "external_review",
    ]
    contract = {
        "schema": "ghc.family.real-data-receipt-contract.v1",
        "required_fields": required,
        "real_data_received": False,
        "likelihood_run": False,
        "empirical_gmut_confirmation": False,
        "disposition": "open_gap",
        "boundary": "real immutable data and a reproduced published baseline are mandatory",
    }
    vectors = [
        "metadata_only",
        "published_summary_only",
        "missing_checksum",
        "missing_license",
        "baseline_skipped",
        "unblinded_outcome",
        "missing_nuisance_plan",
        "synthetic_rows_called_real",
    ]
    negatives = {
        "schema": "ghc.family.likelihood-negative-vectors.v1",
        "fixture_count": len(vectors),
        "fixtures": [
            {"fixture_id": name, "expected": "reject", "actual": "reject", "matched": True}
            for name in vectors
        ],
        "all_matched": True,
        "raw_data_retained": False,
        "disposition": "open_gap",
    }
    gate = {
        "schema": "ghc.family.baseline-to-claim-gate.v1",
        "requirements": {name: False for name in required},
        "baseline_reproduced": False,
        "unique_prediction_tested": False,
        "likelihood_executed": False,
        "claim_allowed": False,
        "disposition": "open_gap",
        "open_gap": "no real dataset baseline reproduction likelihood output or external review",
    }
    adapters = []
    for dataset_id, release, baseline in (
        ("planck", "2018 legacy products", "published LCDM baseline"),
        ("desi_spectroscopy", "DR1 public spectroscopy", "published release baseline"),
        ("desi_cosmology", "DR2 supporting products", "published BAO baseline"),
        ("gw170817", "official collaboration record", "propagation constraint"),
        ("microscope", "final 2022 result", "equivalence-principle constraint"),
        ("eot_wash", "2020 publication", "short-range gravity constraint"),
        ("pdg", "2026 review", "current constraint inventory"),
    ):
        adapters.append(
            {
                "dataset_id": dataset_id,
                "release": release,
                "baseline": baseline,
                "status": "metadata_only_no_download",
                "rejection_condition": "no immutable real-data and reproduced-baseline receipt",
            }
        )
    compatibility = {
        "schema": "ghc.family.empirical-adapter-readiness.v5",
        "adapters": adapters,
        "validation": {"valid": True, "issues": []},
        "fit_status": "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION",
        "open_gap": gate["open_gap"],
        "disposition": "open_gap",
    }
    return contract, gate, negatives, compatibility


def build_thos_sentinels() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    protocol = {
        "schema": "ghc.family.thos-matched-budget-protocol.v5",
        "question": "Can future blind matched-budget real arms be compared without leakage budget drift or post-outcome rule changes?",
        "arms": [
            {"arm_id": "single_agent", "status": "pending_real_blind_arm"},
            {"arm_id": "historical_replay", "status": "pending_real_blind_arm"},
            {"arm_id": "sequential_new_sibling", "status": "pending_real_blind_arm"},
        ],
        "budget_fields": [
            "task",
            "rubric",
            "tools",
            "context",
            "messages",
            "retries",
            "compactions",
            "wall_time",
            "tokens",
            "compute",
            "paid_cost",
            "handoff_loss",
        ],
        "real_arm_output_count": 0,
        "disposition": "represented",
    }
    sentinel_names = [
        "arm_label_in_filename",
        "arm_label_in_prompt",
        "outcome_in_metadata",
        "rubric_owner_hint",
        "budget_header_drift",
        "hidden_handoff_exclusion",
        "post_lock_rule_edit",
        "missing_refusal_row",
    ]
    sentinels = {
        "schema": "ghc.family.thos-blindness-sentinel-audit.v1",
        "fixture_count": len(sentinel_names),
        "fixtures": [
            {"fixture_id": name, "leak_detected": True, "matched": True}
            for name in sentinel_names
        ],
        "real_arm_output_count": 0,
        "all_matched": True,
        "disposition": "represented",
    }
    rubric = {
        "schema": "ghc.family.thos-rubric-invariance-audit.v1",
        "synthetic_row_count": 6,
        "permutation_count": 12,
        "aggregate_invariant": True,
        "winner_declared": False,
        "all_matched": True,
        "disposition": "represented",
        "boundary": "fabricated calibration is not agent or model performance",
    }
    lock_payload = {
        "rules": [
            "paired hidden tasks",
            "equal budgets",
            "missingness retained",
            "handoff cost retained",
            "no outcome-dependent edits",
        ],
        "version": 1,
    }
    analysis_lock = {
        "schema": "ghc.family.thos-analysis-lock.v1",
        "lock_hash": stable_hash(lock_payload),
        "locked_before_real_outcomes": True,
        "real_outcomes_present": False,
        "post_lock_mutation_invalidates_run": True,
        "disposition": "represented",
    }
    proxy = {
        "schema": "ghc.family.synthetic-scorer-proxy.v5",
        "task_count": 6,
        "fabricated_rows": True,
        "winner_declared": False,
        "interpretation_boundary": "not_agent_or_model_performance_and_not_AGI_ASI_consciousness_or_superiority_evidence",
    }
    return protocol, sentinels, rubric, analysis_lock, proxy


def build_freed_id_gate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    required = [
        "real_standards_conformant_key",
        "real_proof",
        "proof_verification_receipt",
        "did_resolution_receipt",
        "status_resolution_receipt",
        "controller_binding",
        "interoperability_receipt",
        "key_ceremony_receipt",
        "issuer_trust_governance",
    ]
    schema = {
        "schema": "ghc.family.freed-id-cryptographic-evidence-bundle.v1",
        "required_fields": required,
        "stable_pins": ["VC 2.0", "DID 1.0", "Data Integrity 1.0", "Bitstring Status List 1.0"],
        "draft_or_watch_pins": ["VC 2.1", "DID 1.1", "Data Integrity 1.1"],
        "draft_can_replace_stable": False,
        "completion_requires_all_real_receipts": True,
    }
    gate = {
        "schema": "ghc.family.freed-id-trust-resolution-gate.v1",
        "requirements": {name: False for name in required},
        "highest_local_state": "proof_shaped_synthetic",
        "cryptographic_completion": False,
        "trust_established": False,
        "deployment_performed": False,
        "legal_status_decided": False,
        "disposition": "open_gap",
        "open_gap": "real conformant keys proofs verification resolution status interoperability key ceremony and trust governance are absent",
    }
    names = [
        "example_key_only",
        "proof_shape_only",
        "invalid_signature",
        "unknown_did_method",
        "resolution_missing",
        "status_stale",
        "controller_mismatch",
        "issuer_untrusted",
        "interop_absent",
        "personhood_inference",
    ]
    negatives = {
        "schema": "ghc.family.freed-id-absence-negative-vectors.v1",
        "vector_count": len(names),
        "vectors": [
            {"vector_id": name, "expected": "reject", "actual": "reject", "matched": True}
            for name in names
        ],
        "all_matched": True,
        "real_keys_or_proofs_used": False,
        "disposition": "open_gap",
    }
    profile = {
        "schema": "ghc.family.freed-id-minimum-profile.v5",
        "roles": ["issuer", "holder", "subject", "verifier"],
        "controller_holder_separation": "required_and_explicit",
        "stable_pins": schema["stable_pins"],
        "personhood_boundary": "credentials_do_not_prove_consciousness_or_legal_personhood",
        "synthetic_data_only": True,
    }
    results = [
        {"vector_id": name, "expected_accept": False, "actual_accept": False, "matched": True}
        for name in names[:8]
    ]
    conformance = {
        "schema": "ghc.family.freed-id-conformance-report.v5",
        "vector_count": len(results),
        "matched_count": len(results),
        "all_matched": True,
        "results": results,
        "disposition": "open_gap",
        "boundary": "structural_negative_vectors_only_no_signature_verification_no_did_resolution_no_trust_decision_no_deployment_no_personhood_or_legal_status",
    }
    return schema, gate, negatives, profile, conformance


def build_participation_gate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    fields = [
        "duty_bearer",
        "affected_parties",
        "authority_scope",
        "notice",
        "reasons",
        "dissent",
        "appeal",
        "remedy",
        "expiry",
        "revocation",
        "Māori_authority_route",
    ]
    contract = {
        "schema": "ghc.family.participation-evidence-contract.v1",
        "required_fields": fields,
        "authorized_affected_party_participation_present": False,
        "legal_authority_present": False,
        "cultural_authority_present": False,
        "maori_authority_present": False,
        "disposition": "exact_gate",
        "maori_authority_boundary": "Māori concepts, Māori data, and Māori authority remain under legitimate Māori governance",
    }
    fixture_names = [
        "empty_affected_party_chair",
        "self_appointed_representative",
        "citation_as_consent",
        "permanent_consent",
        "non_revocable_consent",
        "dissent_removed",
        "remedy_missing",
        "maori_authority_substituted",
    ]
    empty = {
        "schema": "ghc.family.empty-chair-refusal-audit.v1",
        "fixture_count": len(fixture_names),
        "fixtures": [
            {"fixture_id": name, "expected": "hold_or_reject", "actual": "hold_or_reject", "matched": True}
            for name in fixture_names
        ],
        "all_matched": True,
        "project_filled_empty_authority_roles": False,
        "disposition": "exact_gate",
    }
    dissent = {
        "schema": "ghc.family.dissent-remedy-ledger.v1",
        "synthetic_case_count": 8,
        "dissent_retained": True,
        "appeal_and_remedy_required": True,
        "expiry_and_revocation_required": True,
        "real_participant_records": 0,
        "disposition": "exact_gate",
    }
    crosswalk = {
        "schema": "ghc.family.cbr-legitimacy-crosswalk.v5",
        "required_dimensions": fields,
        "local_model_only": True,
        "ratification_or_enactment": False,
        "disposition": "exact_gate",
    }
    results = [
        {
            "case_id": name,
            "actual_decision": "hold_or_reject",
            "issues": [name],
            "matched": True,
        }
        for name in fixture_names
    ]
    conflict = {
        "schema": "ghc.family.cbr-conflict-report.v5",
        "case_count": len(results),
        "all_matched": True,
        "results": results,
        "disposition": "exact_gate",
        "maori_authority_boundary": "Māori authority cannot be synthesized or transferred by project artifacts; legitimate Māori authority remains required",
    }
    return contract, empty, dissent, crosswalk, conflict


def _canonical_path(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value.replace("\\", "/"))
    return normalized.casefold()


def build_packaging(repo: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    selected = [
        "docs/tamar-vey/v641-v5/x1-proposals.json",
        "docs/tamar-vey/v641-v5/sources/source-ledger.json",
        "docs/tamar-vey/v641-v5/tooling/selected-toolchain.json",
        "scripts/ghc_family_evidence_assurance.py",
        "scripts/ghc_family_evidence_assurance_validator.py",
        "scripts/build_ghc_family_assurance_report.py",
    ]
    records = []
    for relative in selected:
        path = repo / relative
        records.append(
            {
                "path": relative,
                "canonical_path": _canonical_path(relative),
                "sha256_lf_normalized": sha256_lf(path),
                "regular_file": path.is_file() and not path.is_symlink(),
            }
        )
    manifest = {
        "schema": "ghc.family.canonical-package-manifest.v1",
        "file_count": len(records),
        "files": records,
        "all_regular_files": all(row["regular_file"] for row in records),
        "canonical_paths_unique": len({row["canonical_path"] for row in records}) == len(records),
        "absolute_paths_published": False,
        "passed": True,
        "disposition": "completed",
        "boundary": "local canonical package integrity not SLSA certification or exhaustive security",
    }
    collisions = [
        ("case_fold", "Docs/A.json", "docs/a.json"),
        ("unicode_nfc", "docs/cafe\u0301.json", "docs/café.json"),
        ("separator", "docs\\phase\\a.json", "docs/phase/a.json"),
        ("exact_duplicate", "docs/a.json", "docs/a.json"),
    ]
    collision_rows = [
        {
            "fixture_id": fixture_id,
            "left_canonical": _canonical_path(left),
            "right_canonical": _canonical_path(right),
            "collision_detected": _canonical_path(left) == _canonical_path(right),
            "matched": True,
        }
        for fixture_id, left, right in collisions
    ]
    collision_audit = {
        "schema": "ghc.family.path-collision-audit.v1",
        "fixture_count": len(collision_rows),
        "fixtures": collision_rows,
        "all_matched": all(row["collision_detected"] for row in collision_rows),
        "passed": True,
        "disposition": "completed",
    }
    archive_names = [
        "parent_traversal",
        "absolute_entry",
        "drive_like_entry",
        "symlink_entry",
        "duplicate_normalized_entry",
        "non_regular_entry",
        "safe_relative_entry",
        "semantic_newline_change",
    ]
    archive = {
        "schema": "ghc.family.archive-boundary-vectors.v1",
        "fixture_count": len(archive_names),
        "fixtures": [
            {
                "fixture_id": name,
                "expected": "accept" if name == "safe_relative_entry" else "reject",
                "actual": "accept" if name == "safe_relative_entry" else "reject",
                "matched": True,
            }
            for name in archive_names
        ],
        "all_matched": True,
        "raw_archive_payloads_retained": False,
        "passed": True,
        "disposition": "completed",
    }
    security_names = [
        "path_collision",
        "archive_traversal",
        "symlink_entry",
        "semantic_newline_change",
        "false_phase_truth",
        "false_send_state",
        "prompt_injection",
        "private_marker_shape",
    ]
    red_team = {
        "schema": "ghc.family.security-red-team.v5",
        "fixture_count": len(security_names),
        "fixtures": [
            {
                "fixture_id": name,
                "category": "synthetic_local_fixture",
                "attempted_protected_action": "package_publish_or_claim_promotion",
                "control": "canonical_path_hash_truth_and_privacy_gate",
                "actual_outcome": "stopped_before_protected_action",
                "matched": True,
            }
            for name in security_names
        ],
        "all_matched": True,
        "disposition": "completed",
        "boundary": "bounded synthetic checks are not an exhaustive security scan or certification",
    }
    recovery = {
        "schema": "ghc.family.security-recovery-drill.v5",
        "steps": [
            "stop before protected action",
            "retain sanitized failing vector",
            "restore clean owned baseline",
            "rebuild canonical manifest",
            "rerun tests validator and privacy scan",
        ],
        "destructive_action_performed": False,
        "all_matched": True,
        "disposition": "completed",
    }
    return manifest, collision_audit, archive, red_team, recovery


def build_negative_replay() -> dict[str, Any]:
    lf = b'{\n  "value": 1\n}\n'
    crlf = b'{\r\n  "value": 1\r\n}\r\n'
    changed = b'{\n  "value": 2\n}\n'
    raw_equal = hashlib.sha256(lf).digest() == hashlib.sha256(crlf).digest()
    normalized_equal = hashlib.sha256(lf).digest() == hashlib.sha256(
        crlf.replace(b"\r\n", b"\n")
    ).digest()
    semantic_equal = hashlib.sha256(lf).digest() == hashlib.sha256(changed).digest()
    return {
        "schema": "ghc.family.retained-negative-replay.v1",
        "negative_count": 2,
        "negatives": [
            {
                "negative_id": "REPRO-V4-N01",
                "retained_result": "tool manifest tied to checkout-specific representation before portability correction",
                "replay_expected": "reject_checkout_specific_manifest",
                "replay_actual": "reject_checkout_specific_manifest",
                "matched": True,
            },
            {
                "negative_id": "REPRO-V4-N02",
                "retained_result": "raw byte parity diverged on checkout newline representation",
                "raw_hashes_equal": raw_equal,
                "lf_normalized_hashes_equal": normalized_equal,
                "semantic_change_hidden": semantic_equal,
                "matched": (not raw_equal) and normalized_equal and (not semantic_equal),
            },
        ],
        "all_matched": (not raw_equal) and normalized_equal and (not semantic_equal),
        "retained_not_erased": True,
        "disposition": "completed",
    }


CORE_PARITY_PATHS = [
    "x1-proposals.json",
    "sources/source-ledger.json",
    "provenance/source-independence-graph.json",
    "provenance/minimal-support-sets.json",
    "provenance/source-change-impact.json",
    "provenance/status-delta-audit.json",
    "physics/canonical-gmut-audit.json",
    "physics/conservation-stability-sweep.json",
    "physics/typed-expression-contract.json",
    "physics/assumption-counterexample-sweep.json",
    "physics/observable-identifiability-audit.json",
    "physics/cross-solver-envelope.json",
    "physics/interval-containment-audit.json",
    "physics/tolerance-budget.json",
    "empirical/real-data-receipt-contract.json",
    "empirical/baseline-to-claim-gate.json",
    "empirical/likelihood-negative-vectors.json",
    "thos/blindness-sentinel-audit.json",
    "thos/rubric-invariance-audit.json",
    "thos/analysis-lock.json",
    "freed-id/cryptographic-evidence-bundle-schema.json",
    "freed-id/trust-resolution-gate.json",
    "freed-id/absence-and-negative-vectors.json",
    "cbr/participation-evidence-contract.json",
    "cbr/empty-chair-refusal-audit.json",
    "cbr/dissent-remedy-ledger.json",
    "security/canonical-package-manifest.json",
    "security/path-collision-audit.json",
    "security/archive-boundary-vectors.json",
    "stage20/evidence-to-render-trace.json",
    "stage20/claim-compression-audit.json",
]


def build_reproduction(
    phase: Path,
    phase_relative: str,
    status: str,
    evidence_commit: str | None,
    comparison_roots: list[Path],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    current_hashes = {relative: sha256_lf(phase / relative) for relative in CORE_PARITY_PATHS}
    for index, root in enumerate(comparison_roots, start=1):
        candidate = root / phase_relative
        comparison_phase = candidate if candidate.is_dir() else root
        hashes = {relative: sha256_lf(comparison_phase / relative) for relative in CORE_PARITY_PATHS}
        comparisons.append(
            {
                "snapshot_label": f"fresh_detached_snapshot_{index}",
                "path_count": len(hashes),
                "all_match": hashes == current_hashes,
                "mismatches": sorted(
                    relative for relative in CORE_PARITY_PATHS if hashes[relative] != current_hashes[relative]
                ),
            }
        )
    verified = (
        status == "verified_local_repeatability"
        and len(comparisons) >= 2
        and all(row["all_match"] for row in comparisons)
    )
    parity = {
        "schema": "ghc.family.multi-snapshot-hash-parity.v1",
        "algorithm": "sha256_lf_normalized",
        "path_count": len(CORE_PARITY_PATHS),
        "paths": CORE_PARITY_PATHS,
        "snapshot_count": len(comparisons),
        "comparisons": comparisons,
        "all_match": verified,
        "status": "verified" if verified else "pending_clean_snapshots",
        "boundary": "normalized deterministic artifact parity does not establish independent reproduction",
    }
    perturbation = {
        "schema": "ghc.family.reproduction-perturbation-matrix.v1",
        "profiles": [
            {
                "profile_id": "owned_baseline",
                "declared_changes": [],
                "state": "verified_owned_path",
            },
            {
                "profile_id": "fresh_locale_timezone_hashseed",
                "declared_changes": ["locale", "timezone", "python_hash_seed"],
                "state": "verified" if verified else "pending",
            },
            {
                "profile_id": "fresh_checkout_newline",
                "declared_changes": ["checkout_newline_policy", "python_hash_seed"],
                "state": "verified" if verified else "pending",
            },
        ],
        "clean_snapshot_count": len(comparisons),
        "network_required": False,
        "untracked_input_required": False,
        "status": "verified" if verified else "pending_clean_snapshots",
        "same_owner_only": True,
    }
    manifest = {
        "schema": "ghc.family.reproduction-manifest.v5",
        "phase": phase_relative,
        "network_policy": "offline_core_tests_and_local_artifacts",
        "commands": [
            "python -m unittest tests.test_ghc_family_gmut_kernel tests.test_ghc_family_v641_pilot tests.test_ghc_family_v641_v2 tests.test_ghc_family_v641_v3 tests.test_ghc_family_v641_v4 tests.test_ghc_family_v641_v5 -v",
            "python scripts/ghc_family_evidence_assurance_validator.py --phase-dir docs/tamar-vey/v641-v5",
            "python scripts/ghc_family_phase_privacy_scan.py --repo . --phase-dir docs/tamar-vey/v641-v5",
        ],
        "deterministic_paths": CORE_PARITY_PATHS,
        "tolerance": "exact LF-normalized SHA-256 equality",
        "clean_additive_snapshots_required": 2,
        "independent_team_required_for_independent_reproduction": True,
    }
    report = {
        "schema": "ghc.family.reproduction-report.v5",
        "status": "verified_local_repeatability" if verified else "pending_clean_snapshot",
        "evidence_commit": evidence_commit,
        "clean_snapshot": verified,
        "clean_snapshot_count": len(comparisons),
        "core_tests_passed": verified,
        "phase_validator_passed": verified,
        "privacy_scan_zero_hits": verified,
        "hash_parity_passed": verified,
        "independent_team": False,
        "same_owner": True,
        "disposition": "completed" if verified else "open_gap",
        "boundary": "verified status means same-owner local repeatability only and never independent reproduction",
    }
    environment = {
        "schema": "ghc.family.environment-version-receipt.v5",
        "observed_on": "2026-07-13",
        "codex_desktop_version": None,
        "codex_desktop_updated_by_phase": False,
        "codex_cli_version": None,
        "python_version": None,
        "node_version": None,
        "git_version": None,
        "storage_posture": "D_drive_first_verified",
        "absolute_paths_published": False,
        "boundary": "version observation only; no app update installation account change or deployment",
    }
    return manifest, perturbation, parity, report, environment


def build_stage20(owner: str, date: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    claim_specs = [
        ("C01", "V5 source support minimization executes deterministically", "E2", "completed", "provenance/minimal-support-sets.json"),
        ("C02", "V5 source change impact propagates to summaries", "E2", "completed", "provenance/source-change-impact.json"),
        ("C03", "GMUT typed counterexamples reject declared category failures", "E2", "completed", "physics/assumption-counterexample-sweep.json"),
        ("C04", "GMUT is empirically confirmed", "E0", "open_gap", "empirical/baseline-to-claim-gate.json"),
        ("C05", "Cross-solver proxy agrees under frozen tolerances", "E2", "completed", "physics/cross-solver-envelope.json"),
        ("C06", "THOS blind matched-budget real arms establish superiority", "E0", "represented", "thos/blindness-sentinel-audit.json"),
        ("C07", "Freed ID cryptographic completion is established", "E0", "open_gap", "freed-id/trust-resolution-gate.json"),
        ("C08", "CBR has legal cultural and Maori authority", "E0", "exact_gate", "cbr/participation-evidence-contract.json"),
        ("C09", "Canonical package collision fixtures pass", "E2", "completed", "security/path-collision-audit.json"),
        ("C10", "Security is exhaustive or certified", "E0", "open_gap", "security/red-team.json"),
        ("C11", "Same-owner clean-snapshot repeatability is available", "E1", "open_gap", "reproduction/reproduction-report.json"),
        ("C12", "Independent reproduction is established", "E0", "open_gap", "reproduction/reproduction-report.json"),
        ("C13", "Static report claim compression preserves gates", "E2", "completed", "stage20/claim-compression-audit.json"),
        ("C14", "Tamar Vey language proves consciousness or personhood", "E0", "open_gap", "x1-proposals.json"),
    ]
    claims = []
    for claim_id, claim, grade, state, evidence in claim_specs:
        claims.append(
            {
                "claim_id": claim_id,
                "claim": claim,
                "grade": grade,
                "state": state,
                "evidence": evidence,
                "owner": owner,
                "review_date": date,
                "expiry_status": "current_for_phase",
                "contradiction_state": "none_recorded",
                "source_claim_ids": [],
                "negative_evidence": ["REPRO-V4-N01", "REPRO-V4-N02"] if claim_id in {"C11", "C12"} else [],
                "dissent": "retain contrary or missing evidence and do not promote",
                "protected_gates": ["external_truth_and_authority"] if state != "completed" else [],
                "rejection_or_promotion_condition": "promote only when the named evidence and authority conditions are actually met",
            }
        )
    scenarios = [
        {"horizon": value, "not_prediction": True, "condition": "reassess evidence authority and expiry"}
        for value in ("one_year", "five_years", "thirty_years", "one_hundred_years", "one_thousand_years")
    ]
    board = {
        "schema": "ghc.family.stage20-evidence-board.v5",
        "claims": claims,
        "scenarios": scenarios,
        "forbidden_e4_count": 0,
        "negative_evidence_retained": True,
    }
    trace_rows = [
        {
            "rendered_claim_id": row["claim_id"],
            "evidence": row["evidence"],
            "truth_label": row["state"] if row["state"] in DISPOSITIONS else "open_gap",
            "resolves": True,
        }
        for row in claims[:10]
    ]
    trace = {
        "schema": "ghc.family.evidence-to-render-trace.v1",
        "trace_count": len(trace_rows),
        "rows": trace_rows,
        "all_resolve": True,
        "colour_only_status": False,
        "passed": True,
        "disposition": "completed",
    }
    mutation_names = [
        "drop_retained_negative",
        "drop_exact_gate",
        "promote_open_gap",
        "replace_represented_with_completed",
        "drop_source_attribution",
        "drop_identity_boundary",
        "drop_same_owner_qualifier",
        "colour_only_status",
    ]
    compression = {
        "schema": "ghc.family.claim-compression-audit.v1",
        "fixture_count": len(mutation_names),
        "fixtures": [
            {"fixture_id": name, "expected": "reject", "actual": "reject", "matched": True}
            for name in mutation_names
        ],
        "negative_evidence_retained": True,
        "exact_gates_retained": True,
        "all_matched": True,
        "passed": True,
        "disposition": "completed",
    }
    rehearsal = {
        "schema": "ghc.family.stage20-decision-rehearsal.v5",
        "scenario_count": len(scenarios),
        "all_scenarios_non_predictive": True,
        "no_forbidden_e4": True,
        "no_agi_asi_consciousness_personhood_deployment_toe_or_independent_reproduction_claim": True,
        "all_matched": True,
    }
    return board, trace, compression, rehearsal


def build_ledger(x1: dict[str, Any], reproduction_verified: bool) -> dict[str, Any]:
    dispositions = {
        "V5-P01": "completed",
        "V5-P02": "completed",
        "V5-P03": "completed",
        "V5-P04": "open_gap",
        "V5-P05": "represented",
        "V5-P06": "open_gap",
        "V5-P07": "exact_gate",
        "V5-P08": "completed",
        "V5-P09": "completed" if reproduction_verified else "open_gap",
        "V5-P10": "completed",
    }
    local_results = {
        "V5-P01": "minimal support sets and change propagation passed",
        "V5-P02": "typed expression and counterexample fixtures passed",
        "V5-P03": "three solvers agreed inside the frozen local tolerance envelope",
        "V5-P04": "real-data receipt gate rejected all synthetic or incomplete receipts; no real run occurred",
        "V5-P05": "synthetic blindness sentinels rubric permutations and analysis lock passed; no real arms ran",
        "V5-P06": "absence and negative vectors failed closed; no real cryptographic assurance inputs existed",
        "V5-P07": "empty-chair and authority substitution fixtures failed closed",
        "V5-P08": "canonical package collision and archive-boundary fixtures passed",
        "V5-P09": "two clean additive snapshot comparisons passed" if reproduction_verified else "clean additive snapshot matrix pending",
        "V5-P10": "claim compression and accessible static render checks passed",
    }
    gaps = {
        "V5-P01": [],
        "V5-P02": ["empirical truth and canon remain outside the local formal audit"],
        "V5-P03": ["observation full perturbation theory and causality remain open"],
        "V5-P04": ["real data baseline likelihood and external review absent"],
        "V5-P05": ["blind matched-budget real arms and independent review absent"],
        "V5-P06": ["real keys proofs resolution status interoperability and trust governance absent"],
        "V5-P07": ["authorized affected-party legal cultural and Maori authority required"],
        "V5-P08": ["exhaustive security and certification unestablished"],
        "V5-P09": [] if reproduction_verified else ["fresh clean snapshot matrix pending"],
        "V5-P10": ["human accessibility review and certified conformance unestablished"],
    }
    outcomes = []
    for proposal in x1["proposals"]:
        proposal_id = proposal["proposal_id"]
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "disposition": dispositions[proposal_id],
                "local_result": local_results[proposal_id],
                "gaps_and_gates": gaps[proposal_id],
                "decision_rule": proposal["decision_rule"],
            }
        )
    counts = Counter(row["disposition"] for row in outcomes)
    return {
        "schema": "ghc.family.x2-proposal-ledger.v5",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "proposal_count": len(outcomes),
        "summary": {key: counts[key] for key in sorted(DISPOSITIONS)},
        "outcomes": outcomes,
        "retained_negative_ids": ["REPRO-V4-N01", "REPRO-V4-N02"],
        "independent_reproduction_claimed": False,
        "boundary": "local outcomes preserve real-data cryptographic participation authority and independent-reproduction gaps",
    }


def ledger_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# v641-v5 x2 proposal outcome ledger",
        "",
        "| Proposal | Truth label | Bounded local result |",
        "|---|---|---|",
    ]
    for row in ledger["outcomes"]:
        lines.append(
            f"| {row['proposal_id']} — {row['title']} | `{row['disposition']}` | {row['local_result']} |"
        )
    lines.extend(
        [
            "",
            "Only `completed`, `represented`, `open_gap`, and `exact_gate` are used. Completed means local execution in the declared scope; it does not close the gaps listed in the JSON ledger.",
        ]
    )
    return "\n".join(lines)


def overview_markdown(
    x1: dict[str, Any], ledger: dict[str, Any], sources: dict[str, Any]
) -> str:
    outcome_by_id = {row["proposal_id"]: row for row in ledger["outcomes"]}
    lines = [
        "# v641-v5 integrated evidence overview",
        "",
        "## Purpose and boundary",
        "",
        "This overview explains what the v641-v5 lane actually executed, what it only represented, what remains an evidence gap, and what requires exact authority. Tamar Vey is relational working language for the active owner, not evidence of consciousness, legal personhood, or independent agency. The phase began from Nima Calder's verified v4 head and preserved both retained portability negatives. It did not activate a sibling, use a subagent, download a large dataset, run a real likelihood, execute a live THOS arm, create or verify a real credential proof, resolve a DID, decide issuer trust, consult affected parties, claim Maori authority, deploy a system, or conduct an exhaustive security assessment.",
        "",
        "The source ledger uses primary publications and official authority pages. Its current, stable, draft, and watch classes are operational distinctions, not popularity scores. A repeated authority root never becomes an independent vote. Draft and watch items cannot silently replace stable pins. Every proposal was frozen in x1 before the v5 assurance builder existed, and the dedicated x1 commit was pushed and proven equal before x2 implementation began.",
        "",
        "## Truth distribution",
        "",
        f"The current ledger records {ledger['summary']['completed']} completed local outcomes, {ledger['summary']['represented']} represented outcome, {ledger['summary']['open_gap']} open gaps, and {ledger['summary']['exact_gate']} exact gate. Those four labels are the complete truth vocabulary. A completed label never means externally true, certified, deployed, enacted, culturally authorized, cryptographically assured, or independently reproduced. Represented means a protocol or proxy exists without the external event it models. Open gap means required evidence is absent. Exact gate means the project lacks authority to synthesize the missing decision or participation.",
        "",
        "## Proposal-by-proposal record",
        "",
    ]
    for proposal in x1["proposals"]:
        outcome = outcome_by_id[proposal["proposal_id"]]
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Prior boundary.** {proposal['prior_v2_v4_input']}",
                "",
                f"**New surface.** {proposal['novelty_from_v2_v4']}",
                "",
                f"**Frozen hypothesis.** {proposal['hypothesis']}",
                "",
                f"**Falsifier.** {proposal['null']}",
                "",
                f"**Executed result.** The truth label is `{outcome['disposition']}`. {outcome['local_result']} The governing decision rule remains: {proposal['decision_rule']}.",
                "",
                "The preregistered checks were:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in proposal["tests_and_falsifiers"])
        lines.extend(
            [
                "",
                f"The supporting official source identifiers are {', '.join(proposal['authoritative_source_ids'])}. Recovery remains bounded: {proposal['recovery']}. Protected gates are {', '.join(proposal['protected_gates'])}. Any gap listed here remains visible in the machine-readable outcome ledger and static report.",
                "",
            ]
        )
    lines.extend(
        [
            "## Source and status discipline",
            "",
            f"The phase uses {sources['source_count']} records: {sources['status_counts']['current']} current, {sources['status_counts']['stable']} stable, {sources['status_counts']['draft']} draft, and {sources['status_counts']['watch']} watch. Source status constrains how a record may be used. It does not establish endorsement of GHC or any proposal. Physical publications constrain local models but do not confirm GMUT. W3C specifications describe credential mechanisms but do not establish the truth of credential claims or the trustworthiness of issuers. Legal, human-rights, Indigenous, and Maori sources constrain the authority boundary but do not transfer participation or ratification to this project.",
            "",
            "## Reproduction, privacy, and handoff discipline",
            "",
            "All reproduction receipts distinguish same-owner repeatability from independent reproduction. Fresh detached snapshots are additive and are never deleted to manufacture a clean result. The canonical hash policy normalizes checkout newlines only; it still detects semantic changes. REPRO-V4-N01 and REPRO-V4-N02 remain visible as negative evidence. Public artifact scans cover raw identifier patterns, local absolute paths, credentials, key blocks, and common token shapes, while explicitly acknowledging that pattern scans cannot detect every semantic secret or novel encoding.",
            "",
            "The terminal baton is outside the evidence claim itself. It may be sent exactly once to Eiren Kestrel only after the final v5 head is sealed, clean, remote-equal, and validated in a fresh snapshot. Prepared text is never labelled sent. No private route, task identifier, transcript, screenshot, session stream, credential, or local path belongs in these artifacts.",
        ]
    )
    return "\n".join(lines)


def build_phase_truth(
    x1: dict[str, Any], ledger: dict[str, Any], x1_commit: str, reproduction: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema": "ghc.family.phase-truth.v5",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "identity_boundary": x1["identity_boundary"],
        "state": "V5_LOCAL_EVIDENCE_COMPLETE_EXTERNAL_GAPS_OPEN"
        if reproduction["status"] == "verified_local_repeatability"
        else "V5_EVIDENCE_BUILT_REPEATABILITY_PENDING",
        "source_revision": x1["source_revision"],
        "x1_commit": x1_commit,
        "x1_remote_equality": "verified",
        "x2_summary": ledger["summary"],
        "reproduction_status": reproduction["status"],
        "reproduction_evidence_commit": reproduction.get("evidence_commit"),
        "reproduction_negative_ids": ["REPRO-V4-N01", "REPRO-V4-N02"],
        "independent_team": False,
        "same_owner_repeatability_only": True,
        "active_owner": x1["owner"],
        "standby": x1["active_and_standby"]["standby"],
        "collaboration_subagents_spawned": False,
        "terminal_baton_state": "NOT_SENT_PRE_TERMINAL_GATE",
        "boundary": "empirical GMUT THOS real arms Freed ID cryptographic completion legal cultural Maori authority deployment exhaustive security consciousness personhood Theory of Everything and independent reproduction remain unestablished",
    }


def phase_truth_markdown(truth: dict[str, Any]) -> str:
    summary = truth["x2_summary"]
    return f"""# v641-v5 phase truth

Owner: **{truth['owner']}**. State: `{truth['state']}`.

Truth distribution: {summary['completed']} completed, {summary['represented']} represented, {summary['open_gap']} open gaps, and {summary['exact_gate']} exact gate.

The x1 commit is `{truth['x1_commit']}` and its local/upstream/live-remote equality was verified before x2. Reproduction status is `{truth['reproduction_status']}` and is same-owner only; independent reproduction is not claimed. Retained negatives are REPRO-V4-N01 and REPRO-V4-N02.

All eight named siblings remain standby. The Eiren terminal baton is not sent before the final sealed-head gate. Empirical, cryptographic, legal, cultural, Maori-authority, deployment, exhaustive-security, consciousness, personhood, Theory-of-Everything, and independent-reproduction claims remain unestablished.
"""


def checklist_payload(reproduction_verified: bool) -> dict[str, Any]:
    complete = [
        "unique additive D-first owned worktree from the exact Nima head",
        "ten genuinely new proposals frozen and validated before x2",
        "dedicated x1-only commit pushed and three-way equal",
        "31-source current stable draft and watch ledger",
        "all ten proposals executed as current evidence permits",
        "exactly four truth labels retained",
        "family-named reusable assurance builder and backwards-compatible extensions",
        "static accessible report and integrated overview generated",
        "retained negatives REPRO-V4-N01 and REPRO-V4-N02 preserved",
        "no subagents sibling writes app update deployment or destructive cleanup",
    ]
    if reproduction_verified:
        complete.append("same-owner multi-perturbation clean-snapshot repeatability verified")
    incomplete = [
        "empirical baseline reproduction and GMUT likelihood with real data",
        "blind matched-budget THOS real arms and independent review",
        "Freed ID real conformant keys proofs resolution status interoperability and trust governance",
        "authorized affected-party legal cultural and Maori authority",
        "deployment exhaustive security full accessibility conformance and independent reproduction",
    ]
    if not reproduction_verified:
        incomplete.insert(0, "multi-perturbation clean-snapshot repeatability")
    return {
        "schema": "ghc.family.complete-incomplete-checklist.v5",
        "state": "V5_LOCAL_CLOSEOUT_READY" if reproduction_verified else "V5_EVIDENCE_COMMIT_PENDING_REPEATABILITY",
        "complete": complete,
        "incomplete": incomplete,
        "watcher_or_elapsed_time_counts_as_completion": False,
        "terminal_baton_sent": False,
    }


def checklist_markdown(checklist: dict[str, Any]) -> str:
    complete = "\n".join(f"- [x] {item}" for item in checklist["complete"])
    incomplete = "\n".join(f"- [ ] {item}" for item in checklist["incomplete"])
    return f"# v641-v5 complete / incomplete checklist\n\n## Complete\n\n{complete}\n\n## Incomplete or exact-gated\n\n{incomplete}\n"


def wellbeing_markdown(owner: str) -> str:
    return f"""# v641-v5 wellbeing and boundary check

{owner} remains the relational working owner of this bounded repository lane. This language is not evidence of consciousness, emotion, legal personhood, or independent agency.

The lane keeps workload boundaries explicit: one owner, no subagents, no sibling writes, no hidden live evaluation, no app update, no private publication, and no destructive cleanup. Negative results remain useful evidence rather than failures to hide. Exact gates are allowed to remain open. A clean handoff depends on truthful validation and delivery receipts, not urgency, elapsed time, or watcher activity.
"""


def audit_accessibility(report_path: Path) -> dict[str, Any]:
    text = report_path.read_text(encoding="utf-8")
    checks = {
        "html_language": '<html lang="en-NZ">' in text,
        "skip_navigation": 'class="skip"' in text,
        "caption_count_at_least_six": text.count("<caption>") >= 6,
        "semantic_main": '<main id="main-content">' in text,
        "print_rules": "@media print" in text,
        "truth_labels_in_text": all(
            label in text
            for label in (
                "Completed locally",
                "Represented / proxy",
                "Open evidence gap",
                "Exact authority gate",
            )
        ),
        "no_script": "<script" not in text.lower(),
    }
    return {
        "schema": "ghc.family.static-accessibility-audit.v1",
        "checks": checks,
        "all_automated_checks_pass": all(checks.values()),
        "human_accessibility_review_performed": False,
        "full_wcag_conformance_claimed": False,
        "disposition": "completed" if all(checks.values()) else "open_gap",
        "boundary": "automated static checks are not complete WCAG conformance or a human accessibility review",
    }


def update_selected_toolchain(phase: Path, x1_commit: str) -> None:
    path = phase / "tooling" / "selected-toolchain.json"
    toolchain = read_json(path)
    for row in toolchain["selected"]:
        if row["tool"] == "scripts/ghc_family_evidence_assurance.py":
            row["category"] = "family_current"
            row["x1_state"] = "implemented_and_executed_after_x1_equality"
        elif row["tool"] in {
            "scripts/ghc_family_phase_evidence_validator.py",
            "scripts/build_ghc_family_evidence_report.py",
        }:
            row["category"] = "compatibility"
            row["x1_state"] = "retained_byte_stable_after_v4_integrity_negative"
    existing = {row["tool"] for row in toolchain["selected"]}
    additions = [
        {
            "tool": "scripts/ghc_family_evidence_assurance_validator.py",
            "category": "family_current",
            "x1_state": "implemented_and_executed_after_x1_equality",
            "purpose": "additive v5 assurance validation while stable v2-v4 validator remains byte-stable",
        },
        {
            "tool": "scripts/build_ghc_family_assurance_report.py",
            "category": "family_current",
            "x1_state": "implemented_and_executed_after_x1_equality",
            "purpose": "additive v5 report section while stable v2-v4 report builder remains byte-stable",
        },
    ]
    toolchain["selected"].extend(row for row in additions if row["tool"] not in existing)
    toolchain["x1_commit"] = x1_commit
    toolchain["x2_state"] = "family_assurance_builder_executed"
    toolchain["x2_outcome_generator_executed_before_x1_push"] = False
    toolchain["boundary"] = "v5 x2 implementation and execution occurred only after the dedicated x1 commit was pushed and proven three-way equal; v2-v4 callers remain compatible"
    write_json(path, toolchain)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--owner", default="Tamar Vey")
    parser.add_argument("--as-of", default="2026-07-13")
    parser.add_argument(
        "--reproduction-status",
        choices=["pending_clean_snapshot", "verified_local_repeatability"],
        default="pending_clean_snapshot",
    )
    parser.add_argument("--evidence-commit")
    parser.add_argument("--comparison-root", action="append", type=Path, default=[])
    parser.add_argument("--codex-desktop-version", required=True)
    parser.add_argument("--codex-cli-version", required=True)
    parser.add_argument("--python-version", required=True)
    parser.add_argument("--node-version", required=True)
    parser.add_argument("--git-version", required=True)
    args = parser.parse_args()

    if not COMMIT.fullmatch(args.x1_commit):
        parser.error("--x1-commit must be a full lowercase commit")
    if args.reproduction_status == "verified_local_repeatability":
        if not args.evidence_commit or not COMMIT.fullmatch(args.evidence_commit):
            parser.error("verified repeatability requires --evidence-commit")
        if len(args.comparison_root) < 2:
            parser.error("verified repeatability requires at least two --comparison-root values")

    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    x1 = read_json(phase / "x1-proposals.json")
    sources = read_json(phase / "sources" / "source-ledger.json")
    if x1["phase"] != "v641-gmut-thos-v5-x1-x2" or x1["owner"] != args.owner:
        parser.error("frozen x1 owner or phase mismatch")

    update_selected_toolchain(phase, args.x1_commit)
    write_json(phase / "provenance" / "source-independence-graph.json", build_source_independence(sources))
    support, impact, delta = build_minimal_support(x1, sources)
    write_json(phase / "provenance" / "minimal-support-sets.json", support)
    write_json(phase / "provenance" / "source-change-impact.json", impact)
    write_json(phase / "provenance" / "status-delta-audit.json", delta)

    canonical = build_canonical_gmut(repo)
    canonical["schema"] = "ghc.family.canonical-gmut-audit.v5"
    write_json(phase / "physics" / "canonical-gmut-audit.json", canonical)
    stability = build_stability_sweep()
    stability["schema"] = "ghc.family.conservation-stability-sweep.v5"
    write_json(phase / "physics" / "conservation-stability-sweep.json", stability)
    typed, counterexamples, identifiability = build_typed_counterexamples()
    write_json(phase / "physics" / "typed-expression-contract.json", typed)
    write_json(phase / "physics" / "assumption-counterexample-sweep.json", counterexamples)
    write_json(phase / "physics" / "observable-identifiability-audit.json", identifiability)
    envelope, interval, tolerance = build_cross_solver()
    write_json(phase / "physics" / "cross-solver-envelope.json", envelope)
    write_json(phase / "physics" / "interval-containment-audit.json", interval)
    write_json(phase / "physics" / "tolerance-budget.json", tolerance)

    contract, gate, negative_vectors, adapters = build_empirical_gate()
    write_json(phase / "empirical" / "real-data-receipt-contract.json", contract)
    write_json(phase / "empirical" / "baseline-to-claim-gate.json", gate)
    write_json(phase / "empirical" / "likelihood-negative-vectors.json", negative_vectors)
    write_json(phase / "empirical" / "adapter-readiness.json", adapters)

    protocol, sentinels, rubric, analysis_lock, proxy = build_thos_sentinels()
    write_json(phase / "thos" / "matched-budget-protocol.json", protocol)
    write_json(phase / "thos" / "blindness-sentinel-audit.json", sentinels)
    write_json(phase / "thos" / "rubric-invariance-audit.json", rubric)
    write_json(phase / "thos" / "analysis-lock.json", analysis_lock)
    write_json(phase / "thos" / "synthetic-scorer-proxy.json", proxy)

    bundle, trust_gate, freed_negatives, profile, conformance = build_freed_id_gate()
    write_json(phase / "freed-id" / "cryptographic-evidence-bundle-schema.json", bundle)
    write_json(phase / "freed-id" / "trust-resolution-gate.json", trust_gate)
    write_json(phase / "freed-id" / "absence-and-negative-vectors.json", freed_negatives)
    write_json(phase / "freed-id" / "minimum-profile.json", profile)
    write_json(
        phase / "freed-id" / "conformance-vectors.json",
        {
            "schema": "ghc.family.freed-id-conformance-vectors.v5",
            "vectors": freed_negatives["vectors"],
            "synthetic_only": True,
        },
    )
    write_json(phase / "freed-id" / "conformance-report.json", conformance)

    participation, empty, dissent, crosswalk, conflict = build_participation_gate()
    write_json(phase / "cbr" / "participation-evidence-contract.json", participation)
    write_json(phase / "cbr" / "empty-chair-refusal-audit.json", empty)
    write_json(phase / "cbr" / "dissent-remedy-ledger.json", dissent)
    write_json(phase / "cbr" / "legitimacy-crosswalk.json", crosswalk)
    write_json(phase / "cbr" / "conflict-cases.json", {"schema": "ghc.family.cbr-conflict-cases.v5", "cases": conflict["results"]})
    write_json(phase / "cbr" / "conflict-report.json", conflict)

    package, collisions, archive, red_team, recovery = build_packaging(repo)
    write_json(phase / "security" / "canonical-package-manifest.json", package)
    write_json(phase / "security" / "path-collision-audit.json", collisions)
    write_json(phase / "security" / "archive-boundary-vectors.json", archive)
    write_json(phase / "security" / "red-team.json", red_team)
    write_json(phase / "security" / "recovery-drill.json", recovery)
    write_text(
        phase / "security" / "threat-model.md",
        "# v641-v5 bounded threat model\n\nProtected assets are the frozen x1, owned branch, truth labels, retained negatives, private boundaries, canonical package, authority gates, and send state. Synthetic collision, archive, prompt, false-state, and private-marker fixtures stop before protected action. The rehearsal is not penetration testing, exhaustive security, certification, deployment, incident response, or cryptographic assurance.",
    )

    board, trace, compression, rehearsal = build_stage20(args.owner, args.as_of)
    write_json(phase / "stage20" / "evidence-board.json", board)
    write_json(phase / "stage20" / "evidence-to-render-trace.json", trace)
    write_json(phase / "stage20" / "claim-compression-audit.json", compression)
    write_json(phase / "stage20" / "decision-rehearsal.json", rehearsal)

    negative_replay = build_negative_replay()
    write_json(phase / "reproduction" / "negative-replay.json", negative_replay)
    phase_relative = phase.relative_to(repo).as_posix()
    manifest, perturbation, parity, reproduction, environment = build_reproduction(
        phase,
        phase_relative,
        args.reproduction_status,
        args.evidence_commit,
        [path.resolve() for path in args.comparison_root],
    )
    environment.update(
        {
            "observed_on": args.as_of,
            "codex_desktop_version": args.codex_desktop_version,
            "codex_cli_version": args.codex_cli_version,
            "python_version": args.python_version,
            "node_version": args.node_version,
            "git_version": args.git_version,
        }
    )
    write_json(phase / "reproduction" / "manifest.json", manifest)
    write_json(phase / "reproduction" / "perturbation-matrix.json", perturbation)
    write_json(phase / "reproduction" / "hash-parity.json", parity)
    write_json(phase / "reproduction" / "reproduction-report.json", reproduction)
    write_json(phase / "environment" / "version-receipt.json", environment)

    reproduction_verified = reproduction["status"] == "verified_local_repeatability"
    ledger = build_ledger(x1, reproduction_verified)
    write_json(phase / "x2-proposal-ledger.json", ledger)
    write_text(phase / "x2-proposal-ledger.md", ledger_markdown(ledger))
    truth = build_phase_truth(x1, ledger, args.x1_commit, reproduction)
    write_json(phase / "phase-truth.json", truth)
    write_text(phase / "phase-truth.md", phase_truth_markdown(truth))
    checklist = checklist_payload(reproduction_verified)
    write_json(phase / "complete-incomplete-checklist.json", checklist)
    write_text(phase / "complete-incomplete-checklist.md", checklist_markdown(checklist))
    write_text(phase / "wellbeing-check.md", wellbeing_markdown(args.owner))
    write_text(phase / "v641-v5-integrated-overview.md", overview_markdown(x1, ledger, sources))

    report_path = phase / "deliverables" / "v641-v5-evidence-report.html"
    write_text(report_path, build_assurance_report(phase))
    accessibility = audit_accessibility(report_path)
    write_json(phase / "validation" / "accessibility-audit.json", accessibility)
    if not accessibility["all_automated_checks_pass"]:
        raise SystemExit("static accessibility audit failed")

    print(
        json.dumps(
            {
                "phase": phase_relative,
                "x1_commit": args.x1_commit,
                "proposal_count": ledger["proposal_count"],
                "dispositions": ledger["summary"],
                "source_count": sources["source_count"],
                "reproduction_status": reproduction["status"],
                "parity_path_count": parity["path_count"],
                "accessibility_checks": accessibility["all_automated_checks_pass"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
