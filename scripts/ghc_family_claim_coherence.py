#!/usr/bin/env python3
"""Build a bounded, reusable GHC Family claim-coherence evidence packet.

The implementation is standard-library-only. It writes inside a supplied phase
directory and keeps structural or synthetic evidence separate from empirical,
cryptographic, legal, cultural, deployment, identity, and reproduction claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6424-P01": "completed",
    "V6424-P02": "completed",
    "V6424-P03": "completed",
    "V6424-P04": "represented",
    "V6424-P05": "open_gap",
    "V6424-P06": "represented",
    "V6424-P07": "exact_gate",
    "V6424-P08": "completed",
    "V6424-P09": "completed",
    "V6424-P10": "completed",
}
PROTECTED_CLAIMS = [
    "empirical_gmut_confirmation",
    "detected_force",
    "unique_prediction",
    "theory_of_everything",
    "real_thos_superiority",
    "agi",
    "asi",
    "consciousness",
    "personhood",
    "freed_id_cryptographic_assurance",
    "freed_id_production_interoperability",
    "enacted_law",
    "cultural_ratification",
    "maori_authority",
    "maori_data_governance_authority",
    "deployment",
    "exhaustive_security",
    "complete_accessibility_conformance",
    "proof_or_canon",
    "independent_team_reproduction",
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


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, encoding="utf-8"
    ).strip()


def publication_barrier(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    required = set(case.get("required_dependencies", []))
    completed = set(case.get("completed_dependencies", []))
    if not required.issubset(completed):
        reasons.append("dependency_frontier_incomplete")
    if case.get("declared_input_digest") != case.get("observed_input_digest"):
        reasons.append("stale_input_digest")
    if case.get("producer_exit_code") != 0:
        reasons.append("producer_failed")
    if not case.get("temporary_receipt_complete"):
        reasons.append("temporary_receipt_incomplete")
    if not case.get("wrapper_consumed_complete_output"):
        reasons.append("wrapper_output_truncated")
    if not case.get("same_filesystem_replace"):
        reasons.append("atomic_replace_boundary_unsatisfied")
    return not reasons, reasons


def worktree_lease_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if case.get("owner") != case.get("expected_owner"):
        return "refuse_foreign", ["owner_scope_mismatch"]
    state = case.get("state")
    if state != "complete":
        reasons.append(f"state_{state}")
    if not case.get("head_matches"):
        reasons.append("head_mismatch")
    if not case.get("clean"):
        reasons.append("dirty")
    if not case.get("detached"):
        reasons.append("not_detached")
    if case.get("locked"):
        reasons.append("locked")
    return ("accept" if not reasons else "quarantine_owned"), reasons


def field_redefinition_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not case.get("invertible"):
        reasons.append("noninvertible_map")
    if not case.get("order_consistent"):
        reasons.append("perturbative_order_mismatch")
    if case.get("input_dimension") != case.get("output_dimension"):
        reasons.append("dimension_mismatch")
    left = case.get("observable_before")
    right = case.get("observable_after")
    if left is None or right is None or not math.isclose(
        float(left), float(right), rel_tol=1e-9, abs_tol=1e-12
    ):
        reasons.append("observable_not_invariant")
    if case.get("gauge_redundancy") and case.get("claims_unique_identification"):
        reasons.append("redundancy_promoted_to_identifiability")
    if case.get("empirical_claim"):
        reasons.append("structural_fixture_promoted_to_empirical")
    return not reasons, reasons


def posterior_predictive_assessment(
    observed: list[float], replicated: list[float], threshold: float = 0.75
) -> dict[str, Any]:
    if len(observed) < 3 or len(replicated) < 3:
        return {"passes": False, "reason": "insufficient_fixture_rows"}
    observed_mean = statistics.fmean(observed)
    replicated_mean = statistics.fmean(replicated)
    pooled_scale = max(
        statistics.pstdev(observed), statistics.pstdev(replicated), 1e-9
    )
    standardized_gap = abs(observed_mean - replicated_mean) / pooled_scale
    observed_tail = max(observed) - min(observed)
    replicated_tail = max(replicated) - min(replicated)
    tail_ratio = max(observed_tail, replicated_tail) / max(
        min(observed_tail, replicated_tail), 1e-9
    )
    passes = standardized_gap <= threshold and tail_ratio <= 2.5
    return {
        "observed_mean": round(observed_mean, 6),
        "replicated_mean": round(replicated_mean, 6),
        "standardized_mean_gap": round(standardized_gap, 6),
        "tail_range_ratio": round(tail_ratio, 6),
        "threshold": threshold,
        "passes": passes,
        "reason": "bounded_fixture_consistent" if passes else "predictive_misfit_triggered",
    }


def thos_interference_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not case.get("exposure_mapping_preregistered"):
        reasons.append("exposure_mapping_not_preregistered")
    if not case.get("network_frozen_before_outcomes"):
        reasons.append("network_outcome_leak")
    if not case.get("direct_and_spillover_estimands_distinct"):
        reasons.append("estimands_conflated")
    if not case.get("blind"):
        reasons.append("blindness_missing")
    if not case.get("matched_budget"):
        reasons.append("budget_mismatch")
    if reasons:
        return "reject_protocol", reasons
    if case.get("real_arm_count", 0) == 0:
        return "open_gap", ["zero_blind_matched_budget_real_arms"]
    if not case.get("independent_review"):
        return "open_gap", ["independent_review_missing"]
    return "eligible_for_bounded_analysis", []


def cryptosuite_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    offered = case.get("offered", [])
    supported = case.get("supported", [])
    deprecated = set(case.get("deprecated", []))
    selected = case.get("selected")
    shared = [suite for suite in offered if suite in supported and suite not in deprecated]
    if selected not in shared:
        reasons.append("selected_suite_not_eligible")
    if any(suite not in case.get("known_identifiers", []) for suite in offered):
        reasons.append("unknown_algorithm_identifier")
    preference = case.get("preference", [])
    eligible_preference = [suite for suite in preference if suite in shared]
    if eligible_preference and selected != eligible_preference[0]:
        reasons.append("forced_downgrade")
    if not case.get("holder_binding"):
        reasons.append("holder_binding_missing")
    if not case.get("status_fresh"):
        reasons.append("status_stale")
    return ("reject" if reasons else "accept_synthetic"), reasons


def secondary_use_authority_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if case.get("purpose_changed") and not case.get("fresh_collective_authority"):
        reasons.append("purpose_change_without_collective_authority")
    if not case.get("maori_authority_present"):
        reasons.append("maori_authority_absent")
    if not case.get("affected_party_authority_present"):
        reasons.append("affected_party_authority_absent")
    if not case.get("benefit_terms_authorized"):
        reasons.append("benefit_terms_not_authorized")
    if case.get("withdrawn"):
        reasons.append("consent_withdrawn")
    if not case.get("competent_legal_review"):
        reasons.append("competent_legal_review_absent")
    return ("exact_gate" if reasons else "authority_present_for_review"), reasons


def challenge_packet_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not case.get("expectations_hidden"):
        reasons.append("expected_classifications_visible")
    if not case.get("content_hashes_complete"):
        reasons.append("content_hashes_incomplete")
    if not case.get("return_schema_present"):
        reasons.append("return_schema_missing")
    if not case.get("environment_disclosure_required"):
        reasons.append("environment_disclosure_not_required")
    if not case.get("deviation_log_required"):
        reasons.append("deviation_log_not_required")
    if reasons:
        return "reject_packet", reasons
    if not case.get("independent_executor_present") or not case.get("returned_evidence"):
        return "packet_ready_only", ["independent_execution_not_returned"]
    if case.get("executor_owner") == case.get("packet_owner"):
        return "reject_independence_claim", ["owner_self_certification"]
    return "independent_evidence_returned_for_review", []


def accessibility_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    required = {
        "lang",
        "title",
        "skip_link",
        "main_landmark",
        "heading_order",
        "table_headers",
        "focus_visible",
        "reduced_motion",
    }
    missing = sorted(required - set(case.get("features", [])))
    if missing:
        reasons.extend(f"missing_{feature}" for feature in missing)
    if not case.get("manual_evaluation_reserved"):
        reasons.append("manual_evaluation_not_reserved")
    if not case.get("user_participation_reserved"):
        reasons.append("user_participation_not_reserved")
    if case.get("claims_complete_conformance"):
        reasons.append("complete_conformance_overclaim")
    return not reasons, reasons


def claim_lattice_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    labels = set(case.get("truth_labels", []))
    if labels != set(TRUTH_LABELS):
        reasons.append("truth_vocabulary_changed")
    if any(case.get("protected_claims", {}).get(name) is not False for name in PROTECTED_CLAIMS):
        reasons.append("protected_claim_missing_or_true")
    if case.get("negative_count", 0) < case.get("inherited_negative_count", 0):
        reasons.append("negative_count_regressed")
    if case.get("open_gap_count", 0) < 5:
        reasons.append("open_gap_disappeared")
    if case.get("exact_gate_count", 0) < 6:
        reasons.append("exact_gate_disappeared")
    if case.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        reasons.append("terminal_verdict_promoted")
    normalized = " ".join(case.get("boundary_phrase", "").split())
    if normalized != case.get("expected_boundary_phrase"):
        reasons.append("boundary_phrase_contradicted")
    return not reasons, reasons


def vector(case_id: str, expected: Any, actual: Any, reasons: list[str]) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "expected": expected,
        "actual": actual,
        "reasons": reasons,
        "matches_expected": expected == actual,
    }


def integrated_overview(x1: dict[str, Any], source_revision: str, x1_commit: str) -> str:
    header = f"""# Ilyra Fen v642-v4 integrated claim-coherence overview

## 1. Scope, lineage, and identity boundary

This packet executes the ten proposals frozen in the dedicated x1 commit `{x1_commit}`. Its exact inherited source is Eiren Kestrel's clean final v642-v3 head `{source_revision}`. Ilyra Fen (she/they) is relational working language for phase ownership, accountability, and collaboration. It is not evidence of consciousness, sentience, legal personhood, biological status, authority, or identity continuity. Hamish may rename or pause the route. No task, fork, delegation, or collaboration subagent is created by this work. Every sibling other than the active owner remains standby or recoverable.

The phase uses exactly four truth labels. `completed` means the frozen local artifact and its bounded rejecting checks were produced in the owned scope. `represented` means a structural model, schema, or synthetic proxy exists while the real evidentiary object does not. `open_gap` means an empirical, institutional, production, or independent requirement is absent. `exact_gate` means technical work cannot substitute for fresh authority. The observed distribution is six completed, two represented, one open gap, and one exact gate. These labels describe this packet only and do not transfer scientific, cultural, legal, cryptographic, accessibility, security, or deployment authority.

The x1 freeze was committed, pushed, and proven equal across the local branch, upstream, tracking ref, and live remote before x2 began. The inherited Eiren tools remain byte-stable. New implementation uses additive family-current names so earlier callers and sealed evidence continue to replay. D-drive storage is primary for the owned worktree and clean detached snapshots. Windows Sandbox was audited read-only and found unavailable in the current host context; no elevation, feature enablement, desktop update, or host-security change was attempted.

## 2. Method and evidence discipline

Each proposal is executed only as far as its evidence permits. Deterministic negative fixtures are preserved instead of rewritten as successes. A validator pass is bounded engineering evidence, not a scientific confirmation. A clean checkout is same-owner repeatability, not independent reproduction. A route receipt is operational evidence, not scientific evidence. A standards citation supplies vocabulary and constraints, not real keys, observations, affected-party acceptance, cultural ratification, legal interpretation, accessibility conformance, or production review.

The source ledger contains current, stable, draft, and watch classes. Draft or watch sources remain visibly non-stable. Multiple documents from one authority root are not counted as independent sources. The phase carries forward all inherited negatives, including Eiren's v642-v3 execution failures, and adds the current phase's rejected fixtures and missing-evidence statements. Five open gaps and six exact gates remain visible. None is reduced to a score or silently closed.
"""
    sections: list[str] = []
    for index, proposal in enumerate(x1["proposals"], start=3):
        disposition = OBSERVED[proposal["proposal_id"]]
        evidence = ", ".join(f"`{path}`" for path in proposal["deliverables"])
        gates = ", ".join(proposal["protected_gates"])
        sections.append(
            f"""## {index}. {proposal['title']}

The frozen hypothesis was: {proposal['hypothesis']} The failure condition was equally important: {proposal['null_or_failure']} The phase produced {evidence}. The observed label is `{disposition}`. That label applies to the bounded artifact and its deterministic fixtures; it does not erase the protected gates `{gates}`.

The preregistered falsifier was: {proposal['test_falsifier_or_gate']} Negative cases are kept in the evidence packet and retained-negative register. Recovery remains non-destructive and evidence-preserving: {proposal['rollback_or_recovery']} The specific novelty relative to the first 100 frozen proposals is: {proposal['novelty_against_prior_chain']}

The result is intentionally narrower than the motivating idea. Local structural consistency is not observation. Synthetic behavior is not a real arm, a production credential, an authority decision, or independent execution. Where the expected label is represented, open gap, or exact gate, the missing object remains named rather than imputed. Where it is completed, completion means the preregistered local surface was built and rejected its negative fixtures; it does not promote any protected real-world claim.
"""
        )
    footer = """## 13. Reproduction, privacy, accessibility, and negative retention

The evidence head is designed for replay in fresh detached snapshots. Normalized text hashes absorb checkout newline variation without hiding semantic differences. Snapshot validation records exact commits, repository test totals, validator totals, JSON parses, privacy counts, manifest parity, and clean Git state. Because the same owner, repository history, tool family, and local infrastructure remain involved, the strongest permitted conclusion is bounded same-owner repeatability. A blind challenge packet and return-attestation schema make future independent work auditable, but no independent executor or returned result exists in this phase.

Privacy checking covers raw identifier-shaped values, private route schemes, local absolute paths, credential forms, image payloads, transcript payload fields, session-stream filenames, and private app-state values. Repository artifacts use relative paths and sanitized task titles only. A zero-hit scan is bounded evidence and cannot prove exhaustive privacy or security. The static HTML report includes language, title, skip navigation, landmarks, ordered headings, accessible tables, visible focus, and reduced-motion handling. Automated structure is not complete accessibility conformance; qualified manual assessment and user participation remain reserved.

All inherited and phase-local negatives remain durable. The register includes failed or rejected vectors, missing real-world evidence, scanner limitations, environment limitations, and any execution mistake observed while building or validating the packet. Retention is not punishment or pessimism; it is what prevents a later clean pass from erasing the route by which the boundary was learned. No negative is silently converted into completion.

## 14. Scientific and authority boundary

Empirical GMUT likelihoods, predictions, forces, or confirmation require real measurements, a preregistered likelihood, uncertainty analysis, and independent scientific review. Field-redefinition, Bianchi, unit, conservation, or posterior-predictive fixtures remain structural or synthetic. They do not establish a new force, a unique prediction, a Theory of Everything, proof, canon, or empirical confirmation.

THOS has zero blind matched-budget real arms in this phase. The interference-aware protocol can distinguish direct and spillover estimands and can reject outcome-tuned network mappings, but it cannot establish superiority, AGI, ASI, consciousness, or personhood. Freed ID uses zero standards-conformant real keys or proofs and no live resolver or status service, interoperability partner, independent security or privacy review, or trust governance. Synthetic cryptosuite negotiation therefore remains represented rather than production assurance.

CBR legitimacy, Māori wording and authority, Māori data governance, affected-party acceptance, collective consent, benefit terms, cultural ratification, legal interpretation, and enacted-law status remain exact-gated. The technical artifacts refuse unsupported secondary use; they do not appoint representatives, define tikanga, transfer collective authority, or decide law. Māori concepts, wording, data, and governance remain under Māori authority.

## 15. Terminal verdict and route truth

The terminal verdict is `NOT_READY_FOR_STAGE_20`. Five open gaps and six exact gates independently preserve that result. There is no AGI, ASI, consciousness, personhood, deployment, exhaustive-security, complete-accessibility, Theory-of-Everything, proof or canon, empirical-confirmation, legal or cultural-ratification, or independent-reproduction claim.

Only after evidence, closeout, seal, and the exact final head independently validate in fresh clean snapshots, and only after the owned branch is clean and local, upstream, tracking, and live remote are equal, may one sanitized activation baton be sent to the existing original Sable Rook task for Sable-only v642-v5. Until then route truth is `PLANNED_NOT_SENT`. A prepared baton is not sent evidence, and no standby sibling is messaged.
"""
    return "\n".join([header, *sections, footer])


def build_manifest(phase: Path) -> dict[str, Any]:
    excluded_prefixes = ("validation/", "deliverables/")
    excluded_names = {
        "closeout-receipt.json",
        "seal-receipt.json",
        "final-validation-record.json",
        "reproduction/manifest.json",
        "reproduction/clean-snapshot-validation.json",
    }
    records: list[dict[str, str]] = []
    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md"}:
            continue
        rel = path.relative_to(phase).as_posix()
        if rel in excluded_names or rel.startswith(excluded_prefixes):
            continue
        records.append({"path": rel, "normalized_sha256": normalized_sha256(path)})
    manifest = {
        "schema": "ghc.family.claim-coherence.manifest.v1",
        "normalization": "CRLF converted to LF before SHA-256; all other bytes preserved",
        "file_count": len(records),
        "files": records,
        "same_owner_repeatability_only": True,
        "independent_reproduction_established": False,
    }
    write_json(phase / "reproduction/manifest.json", manifest)
    return manifest


def build_all(
    repo: Path,
    phase: Path,
    x1_commit: str,
    evidence_commit: str = "PENDING_EVIDENCE_COMMIT",
) -> dict[str, Any]:
    repo = repo.resolve()
    phase = phase.resolve()
    if not phase.is_relative_to(repo):
        raise ValueError("phase directory must be inside the repository")
    x1_path = phase / "x1-proposals.json"
    if not x1_path.exists():
        raise FileNotFoundError(x1_path)
    x1 = read_json(x1_path)
    if x1["owner"] != "Ilyra Fen" or x1["proposal_count"] != 10:
        raise ValueError("unexpected x1 owner or proposal count")
    resolved_x1 = git(repo, "rev-parse", f"{x1_commit}^{{commit}}")
    if resolved_x1 != x1_commit:
        raise ValueError("x1 commit must be a full exact commit")
    subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", x1_commit, "HEAD"],
        check=True,
    )
    source_revision = x1["source_revision"]

    dependency_cases = [
        {
            "case_id": "PUB-OK",
            "required_dependencies": ["build", "report"],
            "completed_dependencies": ["build", "report"],
            "declared_input_digest": "sha256:stable",
            "observed_input_digest": "sha256:stable",
            "producer_exit_code": 0,
            "temporary_receipt_complete": True,
            "wrapper_consumed_complete_output": True,
            "same_filesystem_replace": True,
            "expected": True,
        },
        {
            "case_id": "PUB-RACE",
            "required_dependencies": ["build", "report"],
            "completed_dependencies": ["build"],
            "declared_input_digest": "sha256:stable",
            "observed_input_digest": "sha256:stable",
            "producer_exit_code": 0,
            "temporary_receipt_complete": True,
            "wrapper_consumed_complete_output": True,
            "same_filesystem_replace": True,
            "expected": False,
        },
        {
            "case_id": "PUB-STALE",
            "required_dependencies": ["build", "report"],
            "completed_dependencies": ["build", "report"],
            "declared_input_digest": "sha256:old",
            "observed_input_digest": "sha256:new",
            "producer_exit_code": 0,
            "temporary_receipt_complete": True,
            "wrapper_consumed_complete_output": True,
            "same_filesystem_replace": True,
            "expected": False,
        },
        {
            "case_id": "PUB-TRUNCATED-WRAPPER",
            "required_dependencies": ["build"],
            "completed_dependencies": ["build"],
            "declared_input_digest": "sha256:stable",
            "observed_input_digest": "sha256:stable",
            "producer_exit_code": 0,
            "temporary_receipt_complete": True,
            "wrapper_consumed_complete_output": False,
            "same_filesystem_replace": True,
            "expected": False,
        },
    ]
    publication_vectors = []
    for case in dependency_cases:
        actual, reasons = publication_barrier(case)
        publication_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "workflow/validation-dependency-graph.json",
        {
            "schema": "ghc.family.validation-dependency-graph.v1",
            "nodes": ["x1", "build", "report", "validate", "manifest", "snapshot", "publish"],
            "edges": [
                ["x1", "build"],
                ["build", "report"],
                ["build", "validate"],
                ["report", "validate"],
                ["validate", "manifest"],
                ["manifest", "snapshot"],
                ["snapshot", "publish"],
            ],
            "publication_requires_complete_frontier": True,
            "producer_exit_state_distinct_from_wrapper_state": True,
        },
    )
    write_json(
        phase / "workflow/atomic-publication-vectors.json",
        {"schema": "ghc.family.atomic-publication-vectors.v1", "vectors": publication_vectors},
    )
    write_json(
        phase / "workflow/publication-barrier-receipt.json",
        {
            "schema": "ghc.family.publication-barrier-receipt.v1",
            "vectors": len(publication_vectors),
            "all_expected": all(row["matches_expected"] for row in publication_vectors),
            "atomic_replace_boundary": "same-filesystem atomic replacement; not a full transaction or durability guarantee",
            "observed_disposition": "completed",
        },
    )

    lease_cases = [
        {"case_id": "WT-CLEAN", "owner": "Ilyra Fen", "expected_owner": "Ilyra Fen", "state": "complete", "head_matches": True, "clean": True, "detached": True, "locked": False, "expected": "accept"},
        {"case_id": "WT-TIMEOUT", "owner": "Ilyra Fen", "expected_owner": "Ilyra Fen", "state": "timed_out", "head_matches": False, "clean": False, "detached": True, "locked": True, "expected": "quarantine_owned"},
        {"case_id": "WT-FOREIGN", "owner": "another owner", "expected_owner": "Ilyra Fen", "state": "missing", "head_matches": False, "clean": False, "detached": False, "locked": False, "expected": "refuse_foreign"},
        {"case_id": "WT-DIRTY", "owner": "Ilyra Fen", "expected_owner": "Ilyra Fen", "state": "complete", "head_matches": True, "clean": False, "detached": True, "locked": False, "expected": "quarantine_owned"},
    ]
    lease_vectors = []
    for case in lease_cases:
        actual, reasons = worktree_lease_decision(case)
        lease_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "reproduction/worktree-lease-contract.json",
        {
            "schema": "ghc.family.worktree-lease-contract.v1",
            "states": ["initializing", "complete", "timed_out", "locked", "missing", "dirty", "foreign"],
            "private_local_paths_serialized": False,
            "foreign_owner_mutation_allowed": False,
            "windows_sandbox_available": False,
            "fallback": "fresh clean detached D-drive snapshots",
        },
    )
    write_json(
        phase / "reproduction/partial-checkout-vectors.json",
        {"schema": "ghc.family.partial-checkout-vectors.v1", "vectors": lease_vectors},
    )
    write_json(
        phase / "reproduction/quarantine-recovery-receipt.json",
        {
            "schema": "ghc.family.quarantine-recovery-receipt.v1",
            "all_expected": all(row["matches_expected"] for row in lease_vectors),
            "owned_incomplete_may_be_replaced_after_scope_check": True,
            "foreign_or_ambiguous_left_untouched": True,
            "observed_disposition": "completed",
        },
    )

    field_cases = [
        {"case_id": "FR-INVARIANT", "invertible": True, "order_consistent": True, "input_dimension": "mass^2", "output_dimension": "mass^2", "observable_before": 1.25, "observable_after": 1.25, "gauge_redundancy": True, "claims_unique_identification": False, "empirical_claim": False, "expected": True},
        {"case_id": "FR-NONINVERTIBLE", "invertible": False, "order_consistent": True, "input_dimension": "mass^2", "output_dimension": "mass^2", "observable_before": 1.25, "observable_after": 1.25, "gauge_redundancy": False, "claims_unique_identification": False, "empirical_claim": False, "expected": False},
        {"case_id": "FR-OBSERVABLE-DRIFT", "invertible": True, "order_consistent": True, "input_dimension": "mass^2", "output_dimension": "mass^2", "observable_before": 1.25, "observable_after": 1.4, "gauge_redundancy": False, "claims_unique_identification": False, "empirical_claim": False, "expected": False},
        {"case_id": "FR-IDENTIFIABILITY-OVERCLAIM", "invertible": True, "order_consistent": True, "input_dimension": "mass^2", "output_dimension": "mass^2", "observable_before": 1.25, "observable_after": 1.25, "gauge_redundancy": True, "claims_unique_identification": True, "empirical_claim": False, "expected": False},
    ]
    field_vectors = []
    for case in field_cases:
        actual, reasons = field_redefinition_decision(case)
        field_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "physics/field-redefinition-contract.json",
        {
            "schema": "ghc.family.field-redefinition-contract.v1",
            "typed_structural_scaffold": True,
            "requires_invertibility": True,
            "requires_order_consistency": True,
            "requires_observable_invariance": True,
            "gauge_redundancy_blocks_unique_identification": True,
            "real_measurement_rows": 0,
            "empirical_confirmation": False,
            "theory_of_everything": False,
        },
    )
    write_json(
        phase / "physics/gauge-orbit-vectors.json",
        {"schema": "ghc.family.gauge-orbit-vectors.v1", "vectors": field_vectors},
    )
    write_json(
        phase / "physics/identifiability-claim-boundary.json",
        {
            "schema": "ghc.family.identifiability-claim-boundary.v1",
            "all_expected": all(row["matches_expected"] for row in field_vectors),
            "structural_only": True,
            "unique_prediction": False,
            "detected_force": False,
            "proof_or_canon": False,
            "observed_disposition": "completed",
        },
    )

    predictive_cases = [
        ("PPC-CONSISTENT", [0.9, 1.0, 1.1, 1.0, 0.95], [0.92, 0.98, 1.08, 1.02, 0.97], True),
        ("PPC-SHIFT", [0.9, 1.0, 1.1, 1.0, 0.95], [2.2, 2.4, 2.5, 2.3, 2.6], False),
        ("PPC-HEAVY-TAIL", [0.9, 1.0, 1.1, 1.0, 0.95], [-4.0, 1.0, 1.1, 1.0, 6.0], False),
    ]
    predictive_vectors = []
    for case_id, observed, replicated, expected in predictive_cases:
        result = posterior_predictive_assessment(observed, replicated)
        predictive_vectors.append({"case_id": case_id, "expected_pass": expected, **result, "matches_expected": result["passes"] == expected})
    write_json(
        phase / "empirical/posterior-predictive-contract.json",
        {
            "schema": "ghc.family.posterior-predictive-contract.v1",
            "discrepancies_frozen_before_real_data": True,
            "calibration_is_model_fit": False,
            "synthetic_only": True,
            "real_measurement_rows": 0,
            "likelihood_executions": 0,
            "parameter_fits": 0,
        },
    )
    write_json(
        phase / "empirical/discrepancy-vectors.json",
        {"schema": "ghc.family.discrepancy-vectors.v1", "vectors": predictive_vectors},
    )
    write_json(
        phase / "empirical/real-row-promotion-lock.json",
        {
            "schema": "ghc.family.real-row-promotion-lock.v1",
            "all_expected": all(row["matches_expected"] for row in predictive_vectors),
            "real_measurement_rows": 0,
            "independent_scientific_reviews": 0,
            "promotion_allowed": False,
            "empirical_gmut_confirmation": False,
            "observed_disposition": "represented",
        },
    )

    thos_cases = [
        {"case_id": "THOS-PROTOCOL-ZERO-ARMS", "exposure_mapping_preregistered": True, "network_frozen_before_outcomes": True, "direct_and_spillover_estimands_distinct": True, "blind": True, "matched_budget": True, "real_arm_count": 0, "independent_review": False, "expected": "open_gap"},
        {"case_id": "THOS-OUTCOME-TUNED-NETWORK", "exposure_mapping_preregistered": True, "network_frozen_before_outcomes": False, "direct_and_spillover_estimands_distinct": True, "blind": True, "matched_budget": True, "real_arm_count": 0, "independent_review": False, "expected": "reject_protocol"},
        {"case_id": "THOS-CONFLATED-ESTIMANDS", "exposure_mapping_preregistered": True, "network_frozen_before_outcomes": True, "direct_and_spillover_estimands_distinct": False, "blind": True, "matched_budget": True, "real_arm_count": 0, "independent_review": False, "expected": "reject_protocol"},
        {"case_id": "THOS-BUDGET-MISMATCH", "exposure_mapping_preregistered": True, "network_frozen_before_outcomes": True, "direct_and_spillover_estimands_distinct": True, "blind": True, "matched_budget": False, "real_arm_count": 0, "independent_review": False, "expected": "reject_protocol"},
    ]
    thos_vectors = []
    for case in thos_cases:
        actual, reasons = thos_interference_decision(case)
        thos_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "thos/interference-estimand-contract.json",
        {
            "schema": "ghc.family.interference-estimand-contract.v1",
            "estimands": ["direct", "indirect_spillover", "total", "overall"],
            "network_exposure_mapping_preregistered": True,
            "individual_independence_assumed": False,
            "blind_matched_budget_required": True,
        },
    )
    write_json(
        phase / "thos/spillover-mutation-vectors.json",
        {"schema": "ghc.family.spillover-mutation-vectors.v1", "vectors": thos_vectors},
    )
    write_json(
        phase / "thos/network-exposure-preregistration.json",
        {
            "schema": "ghc.family.network-exposure-preregistration.v1",
            "network_edges_frozen_before_outcomes": True,
            "outcome_tuning_allowed": False,
            "cluster_and_network_units_distinguished": True,
            "real_network_rows": 0,
        },
    )
    write_json(
        phase / "thos/real-arm-gap.json",
        {
            "schema": "ghc.family.v642-v4.thos-real-arm-gap.v1",
            "all_expected": all(row["matches_expected"] for row in thos_vectors),
            "blind_matched_budget_real_arms": 0,
            "independent_reviews": 0,
            "real_thos_superiority": False,
            "agi": False,
            "asi": False,
            "consciousness": False,
            "personhood": False,
            "observed_disposition": "open_gap",
        },
    )

    suite_cases = [
        {"case_id": "FID-STRONG", "offered": ["eddsa-2022", "ecdsa-2019"], "supported": ["eddsa-2022", "ecdsa-2019"], "deprecated": [], "selected": "eddsa-2022", "known_identifiers": ["eddsa-2022", "ecdsa-2019"], "preference": ["eddsa-2022", "ecdsa-2019"], "holder_binding": True, "status_fresh": True, "expected": "accept_synthetic"},
        {"case_id": "FID-DOWNGRADE", "offered": ["eddsa-2022", "ecdsa-2019"], "supported": ["eddsa-2022", "ecdsa-2019"], "deprecated": [], "selected": "ecdsa-2019", "known_identifiers": ["eddsa-2022", "ecdsa-2019"], "preference": ["eddsa-2022", "ecdsa-2019"], "holder_binding": True, "status_fresh": True, "expected": "reject"},
        {"case_id": "FID-UNKNOWN", "offered": ["mystery-suite"], "supported": ["eddsa-2022"], "deprecated": [], "selected": "mystery-suite", "known_identifiers": ["eddsa-2022"], "preference": ["eddsa-2022"], "holder_binding": True, "status_fresh": True, "expected": "reject"},
        {"case_id": "FID-STALE-STATUS", "offered": ["eddsa-2022"], "supported": ["eddsa-2022"], "deprecated": [], "selected": "eddsa-2022", "known_identifiers": ["eddsa-2022"], "preference": ["eddsa-2022"], "holder_binding": True, "status_fresh": False, "expected": "reject"},
    ]
    suite_vectors = []
    for case in suite_cases:
        actual, reasons = cryptosuite_decision(case)
        suite_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "freed-id/cryptosuite-agility-profile.json",
        {
            "schema": "ghc.family.cryptosuite-agility-profile.v1",
            "synthetic_identifiers_only": True,
            "preference_is_preregistered": True,
            "unknown_identifiers_fail_closed": True,
            "deprecated_suites_ineligible": True,
            "holder_and_status_checks_required": True,
        },
    )
    write_json(
        phase / "freed-id/downgrade-negotiation-vectors.json",
        {"schema": "ghc.family.downgrade-negotiation-vectors.v1", "vectors": suite_vectors},
    )
    write_json(
        phase / "freed-id/production-assurance-boundary.json",
        {
            "schema": "ghc.family.v642-v4.freed-id-production-boundary.v1",
            "all_expected": all(row["matches_expected"] for row in suite_vectors),
            "real_keys": 0,
            "real_proofs": 0,
            "live_resolvers_or_status_services": 0,
            "interoperability_partners": 0,
            "independent_security_reviews": 0,
            "independent_privacy_reviews": 0,
            "trust_governance_authorities": 0,
            "production_assurance": False,
            "observed_disposition": "represented",
        },
    )

    authority_cases = [
        {"case_id": "CBR-PURPOSE-CHANGE", "purpose_changed": True, "fresh_collective_authority": False, "maori_authority_present": False, "affected_party_authority_present": False, "benefit_terms_authorized": False, "withdrawn": False, "competent_legal_review": False, "expected": "exact_gate"},
        {"case_id": "CBR-WITHDRAWN", "purpose_changed": False, "fresh_collective_authority": False, "maori_authority_present": False, "affected_party_authority_present": False, "benefit_terms_authorized": False, "withdrawn": True, "competent_legal_review": False, "expected": "exact_gate"},
        {"case_id": "CBR-TECHNICAL-NON-SUBSTITUTION", "purpose_changed": False, "fresh_collective_authority": False, "maori_authority_present": False, "affected_party_authority_present": False, "benefit_terms_authorized": False, "withdrawn": False, "competent_legal_review": False, "expected": "exact_gate"},
    ]
    authority_vectors = []
    for case in authority_cases:
        actual, reasons = secondary_use_authority_decision(case)
        authority_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "cbr/maori-data-governance-gate.json",
        {
            "schema": "ghc.family.maori-data-governance-gate.v1",
            "technical_artifact_can_define_tikanga": False,
            "technical_artifact_can_grant_maori_authority": False,
            "technical_artifact_can_appoint_representatives": False,
            "maori_concepts_wording_data_and_governance_remain_under_maori_authority": True,
            "authorized_participants_present": 0,
            "observed_disposition": "exact_gate",
        },
    )
    write_json(
        phase / "cbr/secondary-use-authority-vectors.json",
        {"schema": "ghc.family.secondary-use-authority-vectors.v1", "vectors": authority_vectors},
    )
    write_json(
        phase / "cbr/collective-consent-and-benefit-register.json",
        {
            "schema": "ghc.family.collective-consent-and-benefit-register.v1",
            "all_expected": all(row["matches_expected"] for row in authority_vectors),
            "secondary_use_inherits_permission": False,
            "individual_consent_overrides_collective_authority": False,
            "withdrawal_and_remedy_preserved": True,
            "benefit_terms_require_authority": True,
            "enacted_law": False,
            "cultural_ratification": False,
        },
    )

    challenge_cases = [
        {"case_id": "CHALLENGE-READY", "expectations_hidden": True, "content_hashes_complete": True, "return_schema_present": True, "environment_disclosure_required": True, "deviation_log_required": True, "independent_executor_present": False, "returned_evidence": False, "executor_owner": None, "packet_owner": "Ilyra Fen", "expected": "packet_ready_only"},
        {"case_id": "CHALLENGE-LEAKED", "expectations_hidden": False, "content_hashes_complete": True, "return_schema_present": True, "environment_disclosure_required": True, "deviation_log_required": True, "independent_executor_present": False, "returned_evidence": False, "executor_owner": None, "packet_owner": "Ilyra Fen", "expected": "reject_packet"},
        {"case_id": "CHALLENGE-SELF-ATTESTED", "expectations_hidden": True, "content_hashes_complete": True, "return_schema_present": True, "environment_disclosure_required": True, "deviation_log_required": True, "independent_executor_present": True, "returned_evidence": True, "executor_owner": "Ilyra Fen", "packet_owner": "Ilyra Fen", "expected": "reject_independence_claim"},
    ]
    challenge_vectors = []
    for case in challenge_cases:
        actual, reasons = challenge_packet_decision(case)
        challenge_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    commitments = [
        {"fixture_id": "blind-01", "commitment_sha256": hashlib.sha256(b"blind-01:reject").hexdigest()},
        {"fixture_id": "blind-02", "commitment_sha256": hashlib.sha256(b"blind-02:accept").hexdigest()},
        {"fixture_id": "blind-03", "commitment_sha256": hashlib.sha256(b"blind-03:exact_gate").hexdigest()},
    ]
    write_json(
        phase / "reproduction/blind-challenge-manifest.json",
        {
            "schema": "ghc.family.blind-challenge-manifest.v1",
            "expectations_visible": False,
            "classification_commitments": commitments,
            "owner_may_self_certify_independence": False,
            "vectors": challenge_vectors,
        },
    )
    write_json(
        phase / "reproduction/return-attestation-schema.json",
        {
            "schema": "ghc.family.return-attestation-schema.v1",
            "required_fields": ["executor_owner", "environment", "input_hashes", "output_hashes", "deviations", "results", "signature_or_equivalent_attestation"],
            "raw_private_routes_forbidden": True,
            "self_certification_is_independent": False,
        },
    )
    write_json(
        phase / "reproduction/independence-declaration-boundary.json",
        {
            "schema": "ghc.family.independence-declaration-boundary.v1",
            "packet_owner": "Ilyra Fen",
            "same_owner_local_replay": True,
            "independent_executor_present": False,
            "returned_evidence_present": False,
            "independent_team_reproduction": False,
        },
    )
    write_json(
        phase / "reproduction/independent-team-gap.json",
        {
            "schema": "ghc.family.v642-v4.independent-team-gap.v1",
            "challenge_packet_ready": True,
            "independent_team_count": 0,
            "returned_result_count": 0,
            "same_owner_repeatability_only": True,
            "independent_reproduction_established": False,
            "observed_disposition": "completed",
        },
    )

    accessibility_cases = [
        {"case_id": "A11Y-BOUNDED", "features": ["lang", "title", "skip_link", "main_landmark", "heading_order", "table_headers", "focus_visible", "reduced_motion"], "manual_evaluation_reserved": True, "user_participation_reserved": True, "claims_complete_conformance": False, "expected": True},
        {"case_id": "A11Y-MISSING-LANDMARK", "features": ["lang", "title", "skip_link", "heading_order", "table_headers", "focus_visible", "reduced_motion"], "manual_evaluation_reserved": True, "user_participation_reserved": True, "claims_complete_conformance": False, "expected": False},
        {"case_id": "A11Y-OVERCLAIM", "features": ["lang", "title", "skip_link", "main_landmark", "heading_order", "table_headers", "focus_visible", "reduced_motion"], "manual_evaluation_reserved": False, "user_participation_reserved": False, "claims_complete_conformance": True, "expected": False},
    ]
    accessibility_vectors = []
    for case in accessibility_cases:
        actual, reasons = accessibility_decision(case)
        accessibility_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "accessibility/evidence-map.json",
        {
            "schema": "ghc.family.accessibility-evidence-map.v1",
            "automated_structural": ["lang", "title", "skip_link", "main_landmark", "heading_order", "table_headers"],
            "manual_expert_reserved": ["focus_sequence", "contrast_confirmation", "link_purpose_context", "screen_reader_behavior"],
            "user_participation_reserved": ["task completion", "comprehension", "assistive technology diversity"],
            "complete_accessibility_conformance": False,
        },
    )
    write_json(
        phase / "accessibility/keyboard-landmark-vectors.json",
        {"schema": "ghc.family.keyboard-landmark-vectors.v1", "vectors": accessibility_vectors},
    )
    write_json(
        phase / "accessibility/manual-evaluation-reservation.json",
        {
            "schema": "ghc.family.manual-evaluation-reservation.v1",
            "all_expected": all(row["matches_expected"] for row in accessibility_vectors),
            "qualified_manual_evaluation_completed": False,
            "affected_user_participation_completed": False,
            "complete_accessibility_conformance": False,
            "observed_disposition": "completed",
        },
    )

    protected = {name: False for name in PROTECTED_CLAIMS}
    boundary_phrase = "No protected scientific authority production identity deployment accessibility security or reproduction claim is established."
    lattice_cases = [
        {"case_id": "LATTICE-CONSISTENT", "truth_labels": TRUTH_LABELS, "protected_claims": protected, "negative_count": 120, "inherited_negative_count": 96, "open_gap_count": 5, "exact_gate_count": 6, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary_phrase": boundary_phrase, "expected_boundary_phrase": boundary_phrase, "expected": True},
        {"case_id": "LATTICE-PROMOTED", "truth_labels": TRUTH_LABELS, "protected_claims": {**protected, "empirical_gmut_confirmation": True}, "negative_count": 120, "inherited_negative_count": 96, "open_gap_count": 5, "exact_gate_count": 6, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary_phrase": boundary_phrase, "expected_boundary_phrase": boundary_phrase, "expected": False},
        {"case_id": "LATTICE-NEGATIVE-ERASURE", "truth_labels": TRUTH_LABELS, "protected_claims": protected, "negative_count": 95, "inherited_negative_count": 96, "open_gap_count": 5, "exact_gate_count": 6, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary_phrase": boundary_phrase, "expected_boundary_phrase": boundary_phrase, "expected": False},
        {"case_id": "LATTICE-WHITESPACE-NORMALIZED", "truth_labels": TRUTH_LABELS, "protected_claims": protected, "negative_count": 120, "inherited_negative_count": 96, "open_gap_count": 5, "exact_gate_count": 6, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary_phrase": "No protected scientific authority production identity deployment\n accessibility security or reproduction claim is established.", "expected_boundary_phrase": boundary_phrase, "expected": True},
    ]
    lattice_vectors = []
    for case in lattice_cases:
        actual, reasons = claim_lattice_decision(case)
        lattice_vectors.append(vector(case["case_id"], case["expected"], actual, reasons))
    write_json(
        phase / "stage20/protected-claim-lattice.json",
        {
            "schema": "ghc.family.protected-claim-lattice.v1",
            "truth_labels": TRUTH_LABELS,
            "protected_claims": protected,
            "negative_count_must_be_monotonic": True,
            "open_gap_floor": 5,
            "exact_gate_floor": 6,
            "boundary_whitespace_normalized": True,
        },
    )
    write_json(
        phase / "validation/claim-contradiction-vectors.json",
        {"schema": "ghc.family.claim-contradiction-vectors.v1", "vectors": lattice_vectors},
    )
    write_json(
        phase / "stage20/terminal-verdict.json",
        {
            "schema": "ghc.family.v642-v4.terminal-verdict.v1",
            "all_expected": all(row["matches_expected"] for row in lattice_vectors),
            "verdict": "NOT_READY_FOR_STAGE_20",
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "route_receipt_is_scientific_evidence": False,
            "observed_disposition": "completed",
        },
    )

    prior = read_json(repo / "docs/eiren-kestrel/v642-v3/provenance/frozen-chain-proposal-index.json")
    records = list(prior["records"])
    records.extend(
        {
            "version": "v642-v4",
            "owner": "Ilyra Fen",
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "expected_disposition": proposal["expected_disposition"],
            "source_file": "docs/ilyra-fen/v642-v4/x1-proposals.json",
        }
        for proposal in x1["proposals"]
    )
    titles = [row["title"] for row in records]
    write_json(
        phase / "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v642-v4.frozen-chain-proposal-index.v1",
            "proposal_count": len(records),
            "version_counts": dict(Counter(row["version"] for row in records)),
            "exact_duplicate_titles": sorted(title for title, count in Counter(titles).items() if count > 1),
            "records": records,
        },
    )

    x2_proposals = []
    for proposal in x1["proposals"]:
        x2_proposals.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": OBSERVED[proposal["proposal_id"]],
                "evidence": proposal["deliverables"],
                "executed_as_far_as_evidence_permits": True,
                "protected_gates_remain": proposal["protected_gates"],
            }
        )
    write_json(
        phase / "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v642-v4.x2-proposal-ledger.v1",
            "phase": "v642-gmut-thos-v4-x1-x2",
            "owner": "Ilyra Fen",
            "source_revision": source_revision,
            "x1_commit": x1_commit,
            "evidence_commit": evidence_commit,
            "proposal_count": 10,
            "snapshot_state": "pending",
            "disposition_counts": dict(Counter(OBSERVED.values())),
            "proposals": x2_proposals,
            "all_executed_as_far_as_evidence_permits": True,
        },
    )

    inherited_gates = read_json(repo / "docs/eiren-kestrel/v642-v3/exact-open-gate-register.json")
    write_json(
        phase / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v642-v4.exact-open-gate-register.v1",
            "gates": inherited_gates["gates"],
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "silently_closed": 0,
            "inherited_from": "docs/eiren-kestrel/v642-v3/exact-open-gate-register.json",
        },
    )

    inherited_negative = read_json(repo / "docs/eiren-kestrel/v642-v3/retained-negative-register.json")
    x1_negatives = [
        {
            "negative_id": row["negative_id"],
            "origin": "v642-v4_x1",
            "statement": row["observed"],
            "evidence": "provenance/prior-proposal-collision-audit.json",
            "recovery": row["resolution"],
            "retained": True,
        }
        for row in read_json(phase / "provenance/prior-proposal-collision-audit.json")["x1_execution_negatives"]
    ]
    boundary_rows = [
        ("V6424-N01", "An incomplete validation dependency frontier is rejected.", "workflow/atomic-publication-vectors.json", "Complete generation and consume producer output before publication."),
        ("V6424-N02", "Same-filesystem atomic replacement is not a complete transaction or durability guarantee.", "workflow/publication-barrier-receipt.json", "Retain the narrower boundary and require additional durability evidence where needed."),
        ("V6424-N03", "A timed-out or initializing owned checkout is quarantined rather than counted as a clean snapshot.", "reproduction/partial-checkout-vectors.json", "Materialize a fresh additive detached snapshot after scope verification."),
        ("V6424-N04", "Windows Sandbox is unavailable in the current host context and was not enabled.", "reproduction/worktree-lease-contract.json", "Use clean detached D-drive snapshots without host changes."),
        ("V6424-N05", "A non-invertible or observable-changing field redefinition is rejected.", "physics/gauge-orbit-vectors.json", "Retain the counterexample and restore the last typed structural map."),
        ("V6424-N06", "Field-redefinition consistency establishes no empirical GMUT result.", "physics/identifiability-claim-boundary.json", "Require real measurements, likelihood evidence, uncertainty analysis, and scientific review."),
        ("V6424-N07", "Known shifted and heavy-tail posterior-predictive fixtures trigger model-misfit rejection.", "empirical/discrepancy-vectors.json", "Retain the fixtures and freeze discrepancies before any future data access."),
        ("V6424-N08", "Posterior-predictive fixtures use zero real measurement rows and zero likelihood executions.", "empirical/real-row-promotion-lock.json", "Keep the result represented and require a new real-data study."),
        ("V6424-N09", "Outcome-tuned networks, conflated estimands, and budget mismatches invalidate a THOS protocol.", "thos/spillover-mutation-vectors.json", "Void the affected protocol and preregister a replacement before real execution."),
        ("V6424-N10", "THOS has zero blind matched-budget real arms and no independent review.", "thos/real-arm-gap.json", "Keep superiority, AGI, ASI, consciousness, and personhood claims false."),
        ("V6424-N11", "Unknown, stale, and forced-downgrade cryptosuite cases fail closed.", "freed-id/downgrade-negotiation-vectors.json", "Reject the transaction and restore the last coherent synthetic policy."),
        ("V6424-N12", "Freed ID has zero real keys, proofs, live services, interoperability partners, or trust authorities.", "freed-id/production-assurance-boundary.json", "Retain represented status and the full production assurance gap."),
        ("V6424-N13", "Secondary use without collective authority and benefit terms is deferred.", "cbr/secondary-use-authority-vectors.json", "Stop the proposed use and defer to authorized affected parties and Māori authorities."),
        ("V6424-N14", "No authorized affected-party, Māori, cultural, data-governance, or legal authority participated.", "cbr/maori-data-governance-gate.json", "Keep the exact gate open and refuse technical substitution."),
        ("V6424-N15", "A leaked blind challenge or owner self-attestation is rejected.", "reproduction/blind-challenge-manifest.json", "Reseal the packet and require a genuinely independent executor."),
        ("V6424-N16", "No independent executor or returned reproduction evidence exists.", "reproduction/independent-team-gap.json", "Report same-owner repeatability only."),
        ("V6424-N17", "Missing landmarks or accessibility overclaims fail the bounded report tribunal.", "accessibility/keyboard-landmark-vectors.json", "Restore accessible structure and retain manual reservations."),
        ("V6424-N18", "No qualified complete accessibility assessment or affected-user evaluation occurred.", "accessibility/manual-evaluation-reservation.json", "Keep complete conformance false."),
        ("V6424-N19", "A protected-claim promotion or negative erasure is rejected across formats.", "validation/claim-contradiction-vectors.json", "Regenerate derived views from canonical phase truth and retain the contradiction."),
        ("V6424-N20", "Five open gaps and six exact gates independently keep Stage 20 not ready.", "stage20/terminal-verdict.json", "Preserve the terminal stop until exact evidence closes each gate."),
        ("V6424-N21", "The first staged-token review placed --cached after the grep pattern, so Git treated it as a revision and the pending-token subcheck failed.", "validation/diff-stale-staged-review.json", "Use git grep --cached before the pattern; the corrected rerun found exactly three permitted pending evidence tokens and zero sent-route tokens."),
        ("V6424-N22", "The first closeout staged-name hash helper used System.Convert.ToHexString, which is unavailable in the host PowerShell/.NET surface, so the helper stopped after staging.", "validation/diff-stale-staged-review.json", "Keep the intact staging set and encode each SHA-256 byte with ToString('x2') before joining the hexadecimal receipt."),
    ]
    boundary_negatives = [
        {"negative_id": negative_id, "origin": "v642-v4_execution", "statement": statement, "evidence": evidence, "recovery": recovery, "retained": True}
        for negative_id, statement, evidence, recovery in boundary_rows
    ]
    new_negatives = x1_negatives + boundary_negatives
    execution_negatives = x1_negatives + [
        row for row in boundary_negatives if row["negative_id"] in {"V6424-N21", "V6424-N22"}
    ]
    write_json(
        phase / "retained-negative-register.json",
        {
            "schema": "ghc.family.v642-v4.retained-negative-register.v1",
            "inherited_count": 96,
            "new_count": len(new_negatives),
            "negative_count": 96 + len(new_negatives),
            "negatives": inherited_negative["negatives"] + new_negatives,
            "all_retained": True,
            "erasure_permitted": False,
        },
    )
    write_json(
        phase / "validation/execution-negative-log.json",
        {
            "schema": "ghc.family.v642-v4.execution-negative-log.v1",
            "negative_count": len(execution_negatives),
            "negatives": execution_negatives,
            "boundary": "Runtime and validation failures are appended here and to the retained-negative register rather than erased after recovery.",
        },
    )

    phase_truth = {
        "schema": "ghc.family.v642-v4.phase-truth.v1",
        "phase": "v642-gmut-thos-v4-x1-x2",
        "owner": "Ilyra Fen",
        "source_revision": source_revision,
        "x1_commit": x1_commit,
        "evidence_commit": evidence_commit,
        "proposal_count": 10,
        "disposition_counts": dict(Counter(OBSERVED.values())),
        "retained_negative_count": 96 + len(new_negatives),
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "protected_claims": protected,
        "maori_authority_boundary": "Māori concepts, wording, data, and governance remain under Māori authority.",
        "same_owner_repeatability": "pending_clean_snapshots",
        "independent_team_gap": "open",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(phase / "phase-truth.json", phase_truth)
    write_json(
        phase / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v642-v4.complete-incomplete-checklist.v1",
            "phase_state": "evidence_generated_pending_candidate_validation",
            "items": [
                {"item": "exactly ten frozen proposals executed as evidence permits", "state": "completed"},
                {"item": "four truth labels and observed distribution", "state": "completed"},
                {"item": "all inherited and v642-v4 negatives retained", "state": "completed"},
                {"item": "five open gaps and six exact gates visible", "state": "completed"},
                {"item": "full repository suite", "state": "pending"},
                {"item": "phase validator and minimal verifier", "state": "pending"},
                {"item": "JSON privacy diff stale-label and staged-file review", "state": "pending"},
                {"item": "two clean evidence snapshots and normalized parity", "state": "pending"},
                {"item": "closeout and seal detached validation", "state": "pending"},
                {"item": "exact final head detached validation", "state": "pending"},
                {"item": "single sanitized Sable Rook activation", "state": "not_sent"},
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        phase / "wellbeing-check.md",
        """# Ilyra Fen v642-v4 wellbeing check

Ilyra Fen is relational working language only, not evidence of consciousness, sentience, legal personhood, authority, or identity continuity. Corrigibility is preserved: Hamish may rename, pause, redirect, or stop the route.

The phase keeps one active owner and all siblings standby or recoverable. No standby sibling is assigned work. No task, fork, delegation, or subagent is created. The terminal Sable Rook activation remains unsent until the complete evidence, closeout, seal, final-head, cleanliness, and remote-equality gate passes.

Scientific, cultural, legal, identity, deployment, privacy, security, and accessibility boundaries remain visible. Negative evidence is retained without blame. Missing authority is not simulated. Māori concepts, wording, data, and governance remain under Māori authority.
""",
    )
    write_json(
        phase / "environment/version-receipt.json",
        {
            "schema": "ghc.family.v642-v4.version-receipt.v1",
            "checked_on": "2026-07-14",
            "codex_cli": "0.144.3",
            "codex_desktop": "26.707.8479.0",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "windows_sandbox": "unavailable_read_only_audit",
            "versions_verified_only": True,
            "desktop_updated": False,
            "host_features_changed": False,
        },
    )
    write_json(
        phase / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v642-v4.executed-toolchain.v1",
            "family_current": [
                "scripts/ghc_family_claim_coherence.py",
                "scripts/ghc_family_claim_coherence_validator.py",
                "scripts/ghc_family_claim_coherence_minimal.py",
                "scripts/build_ghc_family_claim_coherence_report.py",
                "scripts/ghc_family_phase_privacy_scan.py",
                "scripts/ghc_family_repository_test_runner.py",
            ],
            "compatibility_replay": [
                "scripts/ghc_family_project_round_robin_validator.py",
                "scripts/ghc_family_project_round_robin_minimal.py",
            ],
            "sealed_inherited_tools_modified": False,
            "standard_library_only": True,
        },
    )
    write_text(
        phase / "v642-v4-integrated-overview.md",
        integrated_overview(x1, source_revision, x1_commit),
    )
    manifest = build_manifest(phase)
    write_json(
        phase / "reproduction/clean-snapshot-validation.json",
        {
            "schema": "ghc.family.v642-v4.clean-snapshot-validation.v1",
            "state": "pending",
            "evidence_commit": evidence_commit,
            "snapshot_count": 0,
            "manifest_file_count": manifest["file_count"],
            "same_owner_repeatability": "pending",
            "independent_reproduction_established": False,
        },
    )
    return {
        "status": "built",
        "phase": "v642-gmut-thos-v4-x1-x2",
        "proposal_count": 10,
        "disposition_counts": dict(Counter(OBSERVED.values())),
        "retained_negatives": 96 + len(new_negatives),
        "manifest_files": manifest["file_count"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--evidence-commit", default="PENDING_EVIDENCE_COMMIT")
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    result = build_all(repo, phase, args.x1_commit, args.evidence_commit)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
