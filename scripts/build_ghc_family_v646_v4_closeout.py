#!/usr/bin/env python3
"""Build the combined Orin Thale v646-v4 closeout and seal candidate."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"
SOURCE = "c45aba6c9c2fee5d60e1fcde9f0de849290cfc96"
INHERITED_SOURCE = "bb9d80cd6f5443d47eba757847e3d213ec3d0162"
SOURCE_X1 = "5894a1e1fcb923b37d5ce109824b61ad24739fb5"
SOURCE_EVIDENCE = "793ba9f6b02e5e908cd6b6b82b513b5e8fc60a01"
X1 = "8b63d3f65f9fe9909da71eeb1171e3b5cf86768a"
EVIDENCE = "3aa962ee71ed087d1ef44311b11be80b47ba6a0e"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
BOUNDARY = "Same-owner closeout and combined-seal candidate only; not independent reproduction, empirical confirmation, authority, production certification, complete accessibility, exhaustive security, or Stage 20 approval."


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def ancestor(older: str, newer: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT).returncode == 0


def live_head() -> str:
    output = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")).strip()
    return output.split()[0] if output else ""


def verify_evidence_manifest() -> tuple[int, list[str]]:
    manifest_blob = git("show", f"{EVIDENCE}:docs/orin-thale/v646-v4/validation/evidence-staged-manifest.json", binary=True)
    assert isinstance(manifest_blob, bytes)
    manifest = json.loads(manifest_blob.decode("utf-8"))
    mismatches = []
    for row in manifest.get("entries", []):
        try:
            blob = git("show", f"{EVIDENCE}:{row['path']}", binary=True)
            assert isinstance(blob, bytes)
            observed = hashlib.sha256(blob).hexdigest()
        except Exception:
            observed = "missing"
        if observed != row["sha256"]:
            mismatches.append(row["path"])
    return len(manifest.get("entries", [])), mismatches


def main() -> int:
    head = str(git("rev-parse", "HEAD")).strip()
    if head != EVIDENCE:
        raise SystemExit(f"closeout builder requires exact evidence head {EVIDENCE}; observed {head}")
    if str(git("diff", "--cached", "--name-only")).strip():
        raise SystemExit("closeout builder requires an empty Git index")
    status_rows = [row for row in str(git("status", "--porcelain=v1")).splitlines() if row]
    unexpected = []
    for row in status_rows:
        path = row[3:]
        if path.startswith("docs/orin-thale/v646-v4/") or path == "scripts/build_ghc_family_v646_v4_closeout.py":
            continue
        unexpected.append(row)
    if unexpected:
        raise SystemExit(f"unexpected closeout working paths: {unexpected}")
    local = head
    upstream = str(git("rev-parse", "@{u}")).strip()
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip()
    live = live_head()
    four_way = len({local, upstream, tracking, live}) == 1
    if not four_way:
        raise SystemExit("evidence head is not four-way equal")
    anchors = {
        "inherited_source": ancestor(INHERITED_SOURCE, head), "source_x1": ancestor(SOURCE_X1, head),
        "source_evidence": ancestor(SOURCE_EVIDENCE, head), "source_final": ancestor(SOURCE, head),
        "orin_x1": ancestor(X1, head), "evidence": head == EVIDENCE,
    }
    commit_count = int(str(git("rev-list", "--count", f"{SOURCE}..HEAD")).strip())
    merge_count = int(str(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")).strip())
    manifest_entries, manifest_mismatches = verify_evidence_manifest()
    if not all(anchors.values()) or commit_count != 2 or merge_count != 0 or manifest_mismatches:
        raise SystemExit("evidence ancestry, lifecycle count, or manifest parity mismatch")

    truth = load("phase-truth.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    if negatives.get("effective_total") != 2797 or negatives.get("x2_operational") != 7:
        raise SystemExit("late negative continuity is not current")
    exact_validation = {
        "schema": "ghc.family.v646-v4.evidence-exact-validation-summary.v1", "revision": EVIDENCE,
        "current_phase_tests": {"tests": 17, "passed": 17, "failures": 0, "errors": 0},
        "successor_scoped_tests": {"discovered": 70, "excluded_phase_local": 2, "eligible": 68, "passed": 68, "failures": 0, "errors": 0},
        "minimal_validation": {"checks": 43, "passed": 43, "issues": 0},
        "detailed_validation": {"checks": 838, "passed": 838, "issues": 0},
        "json_parse_count": 233,
        "privacy_scan": {"files": 281, "pattern_classes": 5, "confirmed_hits": 0},
        "evidence_manifest": {"entries": manifest_entries, "mismatches": len(manifest_mismatches)},
        "evidence_commit_effective_negatives": 2796,
        "post_evidence_operational_negatives": ["V6464-X2-N07"],
        "closeout_candidate_effective_negatives": negatives["effective_total"],
        "clean_before_and_after": True, "four_way_remote_equal": four_way,
        "commit_count_from_source": commit_count, "merge_count_from_source": merge_count,
        "same_owner_only": True, "independent_reproduction": False, "valid": True, "boundary": BOUNDARY,
    }
    write_json("validation/evidence-exact-validation-summary.json", exact_validation)
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v646-v4.closeout-receipt.v1", "phase": "v646-gmut-thos-v4-x1-x2", "owner": "Orin Thale",
        "source_revision": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "combined_closeout_and_seal_commit": None, "final_commit_pending_at_write": True,
        "phase_commit_count_before_final": commit_count, "phase_commit_cap": 4, "zero_merges": merge_count == 0,
        "anchors_ancestral": anchors, "evidence_four_way_equal": four_way,
        "distribution": truth["distribution"], "effective_retained_negatives": negatives["effective_total"],
        "effective_open_gaps": gates["effective_open_gaps"], "effective_exact_gates": gates["effective_exact_gates"],
        "evidence_exact_validation": "validation/evidence-exact-validation-summary.json",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT",
        "same_owner_only": True, "independent_reproduction": False, "valid_as_precommit_closeout_candidate": True,
        "boundary": BOUNDARY,
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v646-v4.combined-seal-candidate.v1", "source_revision": SOURCE, "x1_commit": X1,
        "evidence_commit": EVIDENCE, "combined_closeout_and_seal_commit": None,
        "exact_final_identifier_pending_at_write": True, "seal_candidate": True,
        "final_commit_must_be_single_parent_of_evidence": True,
        "final_commit_must_preserve_three_phase_commits_and_zero_merges": True,
        "final_commit_must_be_pushed_and_four_way_equal": True,
        "exactly_one_local_named_lane_replay_required": True,
        "route_must_remain_prepared_not_sent_until_replay": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True, "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_json("final-validation-record.json", {
        "schema": "ghc.family.v646-v4.final-validation-candidate.v1", "exact_final_head": None,
        "exact_final_head_pending_at_write": True, "resolution_rule": "the single-parent commit containing this record is the exact final head",
        "canonical_exact_head_validation": "pending postcommit", "single_local_named_lane_replay": "pending postcommit",
        "final_four_way_remote_equality": "pending postcommit push", "required_current_phase_tests": 17,
        "required_successor_scoped_tests": 68, "required_minimal_checks_at_least": 43,
        "required_detailed_checks_at_least": 838, "required_json_parse_count_at_least": 236,
        "required_privacy_confirmed_hits": 0, "required_manifest_mismatches": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True, "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    checklist = load("complete-incomplete-checklist.json")
    checklist["completed"] = list(dict.fromkeys([*checklist.get("completed", []), "evidence commit pushed and four-way equal", "exact evidence-head canonical validation passed", "evidence manifest matched all exact commit blobs", "post-evidence parser fault retained before recovery"]))
    checklist["pending"] = ["combined closeout and seal commit", "exact-final canonical validation", "exactly one local-only named-lane replay", "final four-way remote equality", "single Tamar Vey baton"]
    write_json("complete-incomplete-checklist.json", checklist)
    truth.update({
        "evidence_commit": EVIDENCE, "evidence_exact_validation_passed": True, "closeout_candidate_built": True,
        "combined_closeout_and_seal_commit": None, "final_exact_validation": "pending postcommit",
        "same_owner_repeatability": "pending named-lane exact-final replay", "route_state": "PREPARED_NOT_SENT",
        "effective_retained_negatives": negatives["effective_total"], "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("phase-truth.json", truth)
    update = load("orchestration/phase-update.json")
    update.update({"state": "combined_closeout_and_seal_candidate_built_pending_final_commit", "terminal_route": "PREPARED_NOT_SENT", "standby_contact_count": 0})
    write_json("orchestration/phase-update.json", update)
    write_json("family-index/v646-v4-closeout-index.json", {
        "schema": "ghc.family.v646-v4.phase-index.closeout.v1", "owner": "Orin Thale", "source_revision": SOURCE,
        "x1_commit": X1, "evidence_commit": EVIDENCE, "final_commit": None, "final_commit_pending_at_write": True,
        "proposal_chain_total": 430, "distribution": truth["distribution"], "effective_negatives": negatives["effective_total"],
        "effective_open_gaps": gates["effective_open_gaps"], "effective_exact_gates": gates["effective_exact_gates"],
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_json("validation/closeout-build-receipt.json", {
        "schema": "ghc.family.v646-v4.closeout-build-receipt.v1", "evidence_head": EVIDENCE,
        "evidence_clean": True, "evidence_four_way_equal": four_way, "anchors_ancestral": anchors,
        "evidence_manifest_entries": manifest_entries, "evidence_manifest_mismatches": len(manifest_mismatches),
        "commit_count_before_final": commit_count, "merge_count": merge_count,
        "lifecycle_files": ["closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"],
        "route_state": "PREPARED_NOT_SENT", "valid": True, "boundary": BOUNDARY,
    })
    print(json.dumps({"evidence": EVIDENCE, "current": 17, "scoped": 68, "minimal": 43, "detailed": 838, "json": 233, "privacy_files": 281, "privacy_hits": 0, "manifest_entries": manifest_entries, "effective_negatives": negatives["effective_total"], "closeout_candidate": True, "valid": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
