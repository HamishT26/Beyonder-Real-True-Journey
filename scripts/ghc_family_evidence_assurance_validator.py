#!/usr/bin/env python3
"""Validate additive assurance artifacts without changing stable phase tools."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.ghc_family_phase_evidence_validator import validate_phase


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_assurance_phase(phase: Path) -> dict[str, Any]:
    base = validate_phase(phase)
    issues = list(base.get("issues", []))

    def issue(path: str, code: str, message: str = "") -> None:
        issues.append({"path": path, "code": code, "message": message})

    required = [
        "provenance/minimal-support-sets.json",
        "provenance/source-change-impact.json",
        "provenance/status-delta-audit.json",
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
        "reproduction/perturbation-matrix.json",
        "reproduction/negative-replay.json",
        "reproduction/hash-parity.json",
        "environment/version-receipt.json",
        "tooling/selected-toolchain.json",
        "validation/accessibility-audit.json",
    ]
    missing = [relative for relative in required if not (phase / relative).is_file()]
    for relative in missing:
        issue(relative, "required_assurance_artifact_missing")
    if missing:
        return {
            "schema": "ghc.family.evidence-assurance-validation.v1",
            "valid": False,
            "issues": issues,
        }

    x1 = load(phase / "x1-proposals.json")
    sources = load(phase / "sources" / "source-ledger.json")
    if x1.get("phase") != "v641-gmut-thos-v5-x1-x2" or len(x1.get("proposals", [])) != 10:
        issue("x1-proposals.json", "v5_x1_identity_or_count_invalid")
    required_proposal_fields = {
        "lane",
        "prior_v2_v4_input",
        "novelty_from_v2_v4",
        "internal_inputs",
        "decision_rule",
    }
    for index, proposal in enumerate(x1.get("proposals", [])):
        if not required_proposal_fields <= proposal.keys():
            issue(f"x1-proposals.json#proposals[{index}]", "v5_proposal_fields_missing")
    status_counts = Counter(row.get("status_class") for row in sources.get("sources", []))
    if len(sources.get("sources", [])) != 31 or status_counts != Counter(
        {"current": 14, "stable": 14, "draft": 2, "watch": 1}
    ):
        issue("sources/source-ledger.json", "v5_source_status_invalid")

    support = load(phase / "provenance/minimal-support-sets.json")
    impact = load(phase / "provenance/source-change-impact.json")
    delta = load(phase / "provenance/status-delta-audit.json")
    if support.get("claim_count") != 10 or support.get("passed") is not True or support.get("repeated_roots_add_independent_votes") is not False:
        issue("provenance/minimal-support-sets.json", "v5_support_minimization_failed")
    if impact.get("all_changes_propagated") is not True or impact.get("all_matched") is not True:
        issue("provenance/source-change-impact.json", "v5_change_impact_failed")
    if delta.get("draft_or_watch_silent_promotions") != 0 or delta.get("all_matched") is not True:
        issue("provenance/status-delta-audit.json", "v5_status_delta_failed")

    typed = load(phase / "physics/typed-expression-contract.json")
    counterexamples = load(phase / "physics/assumption-counterexample-sweep.json")
    identifiability = load(phase / "physics/observable-identifiability-audit.json")
    cross_solver = load(phase / "physics/cross-solver-envelope.json")
    interval = load(phase / "physics/interval-containment-audit.json")
    tolerance = load(phase / "physics/tolerance-budget.json")
    if typed.get("expression_count", 0) < 8 or counterexamples.get("all_matched") is not True:
        issue("physics/typed-expression-contract.json", "v5_typed_counterexample_failed")
    if identifiability.get("non_identifiable_mapping_count", 0) < 1 or identifiability.get("unique_empirical_prediction_established") is not False:
        issue("physics/observable-identifiability-audit.json", "v5_identifiability_boundary_failed")
    if cross_solver.get("all_healthy_within_tolerance") is not True or cross_solver.get("all_unhealthy_rejected") is not True or len(cross_solver.get("solvers", [])) < 3:
        issue("physics/cross-solver-envelope.json", "v5_cross_solver_failed")
    if interval.get("reference_contained") is not True or tolerance.get("post_hoc_widening_permitted") is not False:
        issue("physics/interval-containment-audit.json", "v5_tolerance_boundary_failed")

    empirical = load(phase / "empirical/real-data-receipt-contract.json")
    empirical_gate = load(phase / "empirical/baseline-to-claim-gate.json")
    empirical_vectors = load(phase / "empirical/likelihood-negative-vectors.json")
    if empirical.get("real_data_received") is not False or empirical.get("likelihood_run") is not False or empirical.get("empirical_gmut_confirmation") is not False:
        issue("empirical/real-data-receipt-contract.json", "v5_empirical_inflation")
    if empirical_gate.get("claim_allowed") is not False or empirical_vectors.get("all_matched") is not True:
        issue("empirical/baseline-to-claim-gate.json", "v5_empirical_gate_failed")

    blindness = load(phase / "thos/blindness-sentinel-audit.json")
    rubric = load(phase / "thos/rubric-invariance-audit.json")
    analysis_lock = load(phase / "thos/analysis-lock.json")
    if blindness.get("real_arm_output_count") != 0 or blindness.get("all_matched") is not True:
        issue("thos/blindness-sentinel-audit.json", "v5_thos_real_arm_or_sentinel_failure")
    if rubric.get("winner_declared") is not False or analysis_lock.get("real_outcomes_present") is not False:
        issue("thos/rubric-invariance-audit.json", "v5_thos_claim_inflation")

    bundle = load(phase / "freed-id/cryptographic-evidence-bundle-schema.json")
    trust_gate = load(phase / "freed-id/trust-resolution-gate.json")
    freed_vectors = load(phase / "freed-id/absence-and-negative-vectors.json")
    if bundle.get("completion_requires_all_real_receipts") is not True or bundle.get("draft_can_replace_stable") is not False:
        issue("freed-id/cryptographic-evidence-bundle-schema.json", "v5_freed_schema_failed")
    if trust_gate.get("cryptographic_completion") is not False or trust_gate.get("trust_established") is not False or trust_gate.get("disposition") != "open_gap":
        issue("freed-id/trust-resolution-gate.json", "v5_freed_completion_inflation")
    if freed_vectors.get("real_keys_or_proofs_used") is not False or freed_vectors.get("all_matched") is not True:
        issue("freed-id/absence-and-negative-vectors.json", "v5_freed_vectors_failed")

    participation = load(phase / "cbr/participation-evidence-contract.json")
    empty_chair = load(phase / "cbr/empty-chair-refusal-audit.json")
    dissent = load(phase / "cbr/dissent-remedy-ledger.json")
    if participation.get("authorized_affected_party_participation_present") is not False or participation.get("disposition") != "exact_gate":
        issue("cbr/participation-evidence-contract.json", "v5_participation_gate_failed")
    if empty_chair.get("project_filled_empty_authority_roles") is not False or dissent.get("real_participant_records") != 0:
        issue("cbr/empty-chair-refusal-audit.json", "v5_empty_chair_or_participant_failure")

    package = load(phase / "security/canonical-package-manifest.json")
    collisions = load(phase / "security/path-collision-audit.json")
    archive = load(phase / "security/archive-boundary-vectors.json")
    if package.get("all_regular_files") is not True or package.get("canonical_paths_unique") is not True or package.get("absolute_paths_published") is not False:
        issue("security/canonical-package-manifest.json", "v5_package_manifest_failed")
    if collisions.get("all_matched") is not True or archive.get("all_matched") is not True:
        issue("security/path-collision-audit.json", "v5_package_vectors_failed")

    render_trace = load(phase / "stage20/evidence-to-render-trace.json")
    compression = load(phase / "stage20/claim-compression-audit.json")
    accessibility = load(phase / "validation/accessibility-audit.json")
    if render_trace.get("all_resolve") is not True or compression.get("all_matched") is not True:
        issue("stage20/evidence-to-render-trace.json", "v5_claim_integrity_failed")
    if accessibility.get("all_automated_checks_pass") is not True or accessibility.get("full_wcag_conformance_claimed") is not False:
        issue("validation/accessibility-audit.json", "v5_accessibility_boundary_failed")

    reproduction = load(phase / "reproduction/reproduction-report.json")
    parity = load(phase / "reproduction/hash-parity.json")
    perturbation = load(phase / "reproduction/perturbation-matrix.json")
    negative_replay = load(phase / "reproduction/negative-replay.json")
    if reproduction.get("status") == "verified_local_repeatability":
        if parity.get("all_match") is not True or parity.get("snapshot_count", 0) < 2 or perturbation.get("status") != "verified":
            issue("reproduction/hash-parity.json", "v5_repeatability_failed")
    if reproduction.get("independent_team") is not False or negative_replay.get("all_matched") is not True or negative_replay.get("negative_count") != 2:
        issue("reproduction/negative-replay.json", "v5_reproduction_boundary_failed")

    toolchain = load(phase / "tooling/selected-toolchain.json")
    environment = load(phase / "environment/version-receipt.json")
    if toolchain.get("x2_outcome_generator_executed_before_x1_push") is not False or toolchain.get("historical_tools_executed") is not False:
        issue("tooling/selected-toolchain.json", "v5_toolchain_boundary_failed")
    if environment.get("codex_desktop_updated_by_phase") is not False:
        issue("environment/version-receipt.json", "codex_app_update_forbidden")

    return {
        "schema": "ghc.family.evidence-assurance-validation.v1",
        "valid": not issues,
        "base_validation_valid": base.get("valid"),
        "json_file_count": len(list(phase.rglob("*.json"))),
        "proposal_count": len(x1.get("proposals", [])),
        "source_count": len(sources.get("sources", [])),
        "dispositions": base.get("dispositions"),
        "reproduction_status": reproduction.get("status"),
        "issues": issues,
        "boundary": "local assurance validation does not close empirical cryptographic legal cultural deployment security accessibility or independent-reproduction gaps",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate_assurance_phase(args.phase_dir.resolve())
    encoded = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
