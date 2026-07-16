#!/usr/bin/env python3
"""Build the combined Tamar v646-v5 closeout and seal candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
SOURCE = "d970dbc12cd0ded0d6790454491fa45d3012aa86"
X1 = "3f6b5302e18c7828d19ffb621da153f6ae173de0"
EVIDENCE = "575b8fb6c443d10be5551d57621a7cee17de751e"
BOUNDARY = "Same-owner bounded repository validation only; no empirical, participant, professional, legal, cultural, Māori-authority, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, proof-or-canon, consciousness, personhood, Theory-of-Everything, or Stage 20 claim."


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at exact evidence commit")
    if git("status", "--porcelain=v1"):
        expected = {"scripts/build_ghc_family_v646_v5_closeout.py"}
        observed = {line[3:].replace("\\", "/") for line in git("status", "--porcelain=v1").splitlines()}
        if observed != expected:
            raise RuntimeError(f"unexpected pre-closeout paths: {sorted(observed)}")
    for anchor in (SOURCE, X1):
        if subprocess.run(["git", "merge-base", "--is-ancestor", anchor, EVIDENCE], cwd=ROOT).returncode:
            raise RuntimeError(f"missing anchor ancestry: {anchor}")
    phase_commits_before = int(git("rev-list", "--count", f"{SOURCE}..{EVIDENCE}"))
    merges_before = int(git("rev-list", "--min-parents=2", "--count", f"{SOURCE}..{EVIDENCE}"))
    if (phase_commits_before, merges_before) != (2, 0):
        raise RuntimeError("evidence history violates the phase commit plan")

    current = load("validation/current-phase-tests.json")
    scoped = load("validation/successor-scoped-tests.json")
    detailed = load("validation/detailed-validation.json")
    minimal = load("validation/minimal-validation.json")
    privacy = load("validation/json-privacy-validation.json")
    manifest = load("validation/evidence-staged-manifest.json")
    truth = load("phase-truth.json")
    runner = load("prototypes/runner-build-use-receipt.json")
    method = load("method-flow/method-flow-state.json")
    evidence_valid = all((
        current["valid"], scoped["valid"], detailed["valid"], minimal["valid"], privacy["valid"],
        current["tests_run"] == current["passed"] == 40,
        scoped["tests_run"] == scoped["passed"] == 108,
        scoped["excluded_count"] == 2,
        detailed["check_count"] == detailed["passed"] == 576,
        minimal["check_count"] == minimal["passed"] == 22,
        privacy["privacy_confirmed_hit_count"] == 0,
        manifest["entry_count"] == 228,
        runner["runner_count"] == runner["passed_count"] == 10,
        truth["effective_negatives"] == 2884,
    ))
    if not evidence_valid:
        raise RuntimeError("committed evidence receipts are not valid")

    owner_files = len(git("diff", "--name-only", SOURCE, EVIDENCE).splitlines())
    evidence_summary = {
        "schema": "ghc.family.v646-v5.evidence-exact-validation.v1", "exact_evidence_commit": EVIDENCE,
        "source": SOURCE, "x1": X1, "source_and_x1_ancestral": True, "phase_commits_before_final": phase_commits_before,
        "merge_commits": merges_before, "current_tests": current["tests_run"], "current_passed": current["passed"],
        "scoped_tests": scoped["tests_run"], "scoped_passed": scoped["passed"], "scoped_exclusions": scoped["excluded_count"],
        "detailed_checks": detailed["check_count"], "detailed_passed": detailed["passed"],
        "minimal_checks": minimal["check_count"], "minimal_passed": minimal["passed"],
        "phase_json_parses": privacy["json_parse_count"], "phase_files_scanned": privacy["files_scanned"],
        "privacy_confirmed_hits": privacy["privacy_confirmed_hit_count"], "evidence_manifest_entries": manifest["entry_count"],
        "runner_passes": runner["passed_count"], "method_flow_methods": method["counts"]["methods"],
        "method_flow_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "method_flow_passing_witnesses": method["counts"]["witness_results"]["pass"],
        "full_repository_suite_run": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True, "boundary": BOUNDARY,
    }
    write_json("validation/evidence-exact-validation-summary.json", evidence_summary)
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v646-v5.closeout-receipt.v1", "phase": "v646-gmut-thos-v5-x1-x2", "owner": "Tamar Vey",
        "source_revision": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE, "anchors_ancestral": True,
        "evidence_exact_validation": True, "evidence_four_way_equal": True, "zero_merges": True,
        "phase_commit_count_before_final": phase_commits_before, "phase_commit_cap": 4,
        "combined_closeout_and_seal_commit": True, "final_commit_pending_at_write": True,
        "distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": 2884, "effective_open_gaps": 14, "effective_exact_gates": 15,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_only": True, "independent_reproduction": False, "valid_as_precommit_closeout_candidate": True, "boundary": BOUNDARY,
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v646-v5.seal-receipt.v1", "source_revision": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "seal_candidate": True, "combined_closeout_and_seal_commit": True, "exact_final_identifier_pending_at_write": True,
        "final_commit_must_be_single_parent_of_evidence": True, "final_commit_must_preserve_three_phase_commits_and_zero_merges": True,
        "final_commit_must_be_pushed_and_four_way_equal": True, "exactly_one_local_named_lane_replay_required": True,
        "route_must_remain_prepared_not_sent_until_replay": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY,
    })
    write_json("final-validation-record.json", {
        "schema": "ghc.family.v646-v5.final-validation-record.v1", "exact_final_head": None,
        "exact_final_head_pending_at_write": True, "resolution_rule": "The exact final head is the single commit containing this record; resolve and validate it after commit without rewriting history.",
        "canonical_exact_head_validation": "required_after_commit", "single_local_named_lane_replay": "required_exactly_once_after_canonical_validation",
        "final_four_way_remote_equality": "required_before_route", "required_current_phase_tests": 40,
        "required_successor_scoped_tests": 108, "required_detailed_checks_at_least": 576,
        "required_minimal_checks_at_least": 22, "required_json_parse_count_at_least": privacy["json_parse_count"],
        "required_privacy_confirmed_hits": 0, "required_manifest_mismatches": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY,
    })
    write_json("environment/final-rotation-receipt.json", {
        "schema": "ghc.family.v646-v5.final-rotation.v1", "owner_generated_paths_through_evidence": owner_files,
        "closeout_files_pending": 9, "threshold": 15000, "threshold_scope": "new_tamar_generated_addition",
        "rotate": owner_files + 9 >= 15000, "inherited_baseline_triggers_rotation": False,
    })
    write_json("family-index/v646-v5-closeout-index.json", {
        "schema": "ghc.family.v646-v5.closeout-index.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "closeout": "closeout-receipt.json", "seal": "seal-receipt.json", "final_validation": "final-validation-record.json",
        "evidence_validation": "validation/evidence-exact-validation-summary.json", "final_stage_review": "validation/final-staged-review.json",
        "final_manifest": "validation/final-staged-manifest.json", "route_state": "PREPARED_NOT_SENT", "boundary": BOUNDARY,
    })
    checklist = load("complete-incomplete-checklist.json")
    checklist["complete"].extend(["evidence commit pushed and four-way equal", "combined closeout and seal candidate built within commit cap"])
    checklist["pre_route_required"] = ["exact-final canonical validation", "exactly one clean local-only named-lane replay", "final four-way remote equality", "unique existing Sylven Arc task resolution", "one acknowledged sanitized baton"]
    write_json("complete-incomplete-checklist.json", checklist)
    phase_truth = load("phase-truth.json")
    phase_truth.update({"x1_commit": X1, "evidence_commit": EVIDENCE, "combined_final_commit_semantics": "commit_containing_closeout_seal_and_final_validation_records", "planned_phase_commit_count": 3, "phase_commit_cap": 4, "route_state": "PREPARED_NOT_SENT"})
    write_json("phase-truth.json", phase_truth)
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.phase-update.v1", "phase": "v646-gmut-thos-v5-x1-x2", "owner": "Tamar Vey",
        "state": "combined_closeout_and_seal_candidate_pending_exact_final_validation", "active": ["Tamar Vey"],
        "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": True,
        "core_outcomes_executed": 10, "evidence_commit": EVIDENCE, "terminal_route": "PREPARED_NOT_SENT",
    })
    write_json("validation/closeout-build-receipt.json", {
        "schema": "ghc.family.v646-v5.closeout-build.v1", "head_before_final": EVIDENCE,
        "evidence_valid": evidence_valid, "phase_commits_before_final": phase_commits_before, "merge_commits": merges_before,
        "final_commit_pending": True, "combined_closeout_and_seal": True, "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "result": "pass", "boundary": BOUNDARY,
    })
    print(json.dumps({"evidence": EVIDENCE, "current_tests": 40, "scoped_tests": 108, "detailed": 576, "minimal": 22, "privacy_hits": 0, "manifest": 228, "phase_commits_before_final": 2, "result": "pass"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
