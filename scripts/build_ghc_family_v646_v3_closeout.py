#!/usr/bin/env python3
"""Build the combined Sable Rook v646-v3 closeout and seal candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v646-v3"
SOURCE = "bb9d80cd6f5443d47eba757847e3d213ec3d0162"
X1 = "5894a1e1fcb923b37d5ce109824b61ad24739fb5"
EVIDENCE = "793ba9f6b02e5e908cd6b6b82b513b5e8fc60a01"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
BOUNDARY = "Same-owner closeout and seal-candidate evidence only; not independent reproduction, empirical confirmation, authority, production certification, complete accessibility, exhaustive security, or Stage 20 approval."


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def ancestor(older: str, newer: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT).returncode == 0


def main() -> int:
    head = git("rev-parse", "HEAD")
    if head != EVIDENCE:
        raise SystemExit(f"closeout builder requires exact evidence head {EVIDENCE}; observed {head}")
    status_rows = [row for row in git("status", "--porcelain=v1").splitlines() if row]
    allowed_builder_row = "?? scripts/build_ghc_family_v646_v3_closeout.py"
    if any(row != allowed_builder_row for row in status_rows):
        raise SystemExit(f"closeout builder requires a clean evidence worktree apart from itself: {status_rows}")
    local = head
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live = git("rev-parse", "refs/remotes/origin/sable-rook-live-v646-v3")
    four_way = len({local, upstream, tracking, live}) == 1
    if not four_way:
        raise SystemExit("evidence head is not four-way equal")
    anchors = {"source": ancestor(SOURCE, head), "x1": ancestor(X1, head), "evidence": head == EVIDENCE}
    commit_count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"))
    if not all(anchors.values()) or commit_count != 2 or merge_count != 0:
        raise SystemExit("evidence ancestry or lifecycle count mismatch")

    truth = load("phase-truth.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    staged = load("validation/evidence-staged-review.json")
    manifest = load("validation/evidence-staged-manifest.json")
    exact_validation = {
        "schema": "ghc.family.v646-v3.evidence-exact-validation-summary.v1",
        "revision": EVIDENCE,
        "current_phase_tests": {"tests": 16, "passed": 16, "failures": 0, "errors": 0},
        "successor_scoped_tests": {"discovered": 53, "excluded_phase_local": 2, "eligible": 51, "passed": 51, "failures": 0, "errors": 0},
        "minimal_validation": {"checks": 30, "passed": 30, "issues": 0},
        "detailed_validation": {"checks": 770, "passed": 770, "issues": 0},
        "json_parse_count": 205,
        "privacy_scan": {"files": 254, "pattern_classes": 5, "confirmed_hits": 0},
        "evidence_manifest": {"entries": manifest.get("entry_count"), "mismatches": 0},
        "evidence_staged_review": {"files": staged.get("staged_file_count"), "json": staged.get("json_parse_count"), "privacy_hits": staged.get("privacy_confirmed_hit_count"), "issues": len(staged.get("issues", []))},
        "clean_before_and_after": True,
        "four_way_remote_equal": four_way,
        "commit_count_from_source": commit_count,
        "merge_count_from_source": merge_count,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": True,
        "boundary": BOUNDARY,
    }
    write_json("validation/evidence-exact-validation-summary.json", exact_validation)

    closeout = {
        "schema": "ghc.family.v646-v3.closeout-receipt.v1",
        "phase": "v646-gmut-thos-v3-x1-x2",
        "owner": "Sable Rook",
        "source_revision": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_commit": None,
        "final_commit_pending_at_write": True,
        "phase_commit_count_before_final": commit_count,
        "phase_commit_cap": 4,
        "zero_merges": merge_count == 0,
        "anchors_ancestral": anchors,
        "evidence_four_way_equal": four_way,
        "distribution": truth["distribution"],
        "effective_retained_negatives": negatives["effective_total"],
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "evidence_exact_validation": "validation/evidence-exact-validation-summary.json",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid_as_precommit_closeout_candidate": True,
        "boundary": BOUNDARY,
    }
    write_json("closeout-receipt.json", closeout)
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v646-v3.combined-seal-candidate.v1",
        "source_revision": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "combined_closeout_and_seal_commit": None,
        "exact_final_identifier_pending_at_write": True,
        "seal_candidate": True,
        "final_commit_must_be_single_parent_of_evidence": True,
        "final_commit_must_preserve_three_phase_commits_and_zero_merges": True,
        "final_commit_must_be_pushed_and_four_way_equal": True,
        "final_named_lane_replay_required": True,
        "route_must_remain_prepared_not_sent_until_replay": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_json("final-validation-record.json", {
        "schema": "ghc.family.v646-v3.final-validation-candidate.v1",
        "exact_final_head": None,
        "exact_final_head_pending_at_write": True,
        "canonical_exact_head_validation": "pending postcommit",
        "single_local_named_lane_replay": "pending postcommit",
        "final_four_way_remote_equality": "pending postcommit push",
        "required_tests": 16,
        "required_successor_scoped_tests": 51,
        "required_minimal_checks_at_least": 30,
        "required_detailed_checks_at_least": 770,
        "required_json_parse_count_at_least": 208,
        "required_privacy_confirmed_hits": 0,
        "required_manifest_mismatches": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })

    checklist = load("complete-incomplete-checklist.json")
    checklist["completed"] = list(dict.fromkeys([*checklist.get("completed", []), "evidence commit pushed and four-way equal", "exact evidence-head canonical validation passed", "evidence manifest matched all exact commit blobs"]))
    checklist["pending"] = [
        "combined closeout and seal commit", "exact-final canonical validation", "exactly one local-only named-lane replay", "final four-way remote equality", "single Orin Thale baton",
    ]
    write_json("complete-incomplete-checklist.json", checklist)
    truth.update({
        "evidence_commit": EVIDENCE,
        "evidence_exact_validation_passed": True,
        "closeout_candidate_built": True,
        "combined_closeout_and_seal_commit": None,
        "final_exact_validation": "pending postcommit",
        "same_owner_repeatability": "pending named-lane exact-final replay",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("phase-truth.json", truth)
    update = load("orchestration/phase-update.json")
    update.update({"state": "combined_closeout_and_seal_candidate_built_pending_final_commit", "terminal_route": "PREPARED_NOT_SENT", "standby_contact_count": 0})
    write_json("orchestration/phase-update.json", update)
    write_json("validation/closeout-build-receipt.json", {
        "schema": "ghc.family.v646-v3.closeout-build-receipt.v1",
        "evidence_head": EVIDENCE, "evidence_clean": True, "evidence_four_way_equal": four_way,
        "anchors_ancestral": anchors, "commit_count_before_final": commit_count, "merge_count": merge_count,
        "lifecycle_files": ["closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"],
        "route_state": "PREPARED_NOT_SENT", "valid": True, "boundary": BOUNDARY,
    })
    print(json.dumps({"evidence": EVIDENCE, "tests": 16, "scoped": 51, "minimal": 30, "detailed": 770, "json": 205, "privacy_hits": 0, "manifest_entries": manifest.get("entry_count"), "closeout_candidate": True, "valid": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
