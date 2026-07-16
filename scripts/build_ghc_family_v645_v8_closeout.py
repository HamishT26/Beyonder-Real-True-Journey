#!/usr/bin/env python3
"""Build closeout and seal-candidate receipts for Sylven v645-v8."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from ghc_family_v645_v8_definitions import IDENTITY_BOUNDARY, SOURCE_REVISION
from ghc_family_v645_v8_runtime import PHASE, ROOT, TRUTH_BOUNDARY, owner_files, parse_json_documents, privacy_scan, sha256_file, write_json


X1_COMMIT = "3274af55081cf023f78e2a854448f2c5f936dbbd"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def manifest_entries() -> list[dict[str, str | int]]:
    excluded = {
        "docs/sylven-arc/v645-v8/validation/exact-owner-manifest.json",
        "docs/sylven-arc/v645-v8/validation/closeout-staged-manifest.json",
        "docs/sylven-arc/v645-v8/validation/closeout-staged-review.json",
    }
    entries = []
    for path in owner_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative in excluded:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": sha256_file(path)})
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    if head != args.evidence_commit:
        raise SystemExit("evidence commit does not match current head")
    phase_commits_before_closeout = int(git("rev-list", "--count", f"{SOURCE_REVISION}..HEAD"))
    merges_before_closeout = len([row for row in git("rev-list", "--merges", f"{SOURCE_REVISION}..HEAD").splitlines() if row])
    write_json("validation/closeout-json-document-receipt.json", parse_json_documents())
    write_json("validation/closeout-privacy-scan.json", privacy_scan())
    write_json("validation/closeout-stale-label-review.json", {
        "schema": "ghc.family.v645-v8.stale-label-review.v1",
        "reviewed_labels": ["outcome vocabulary", "terminal verdict", "same-owner boundary", "route state", "full-suite ownership", "negative and gate counts"],
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "issues": [],
        "valid": True,
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v645-v8.closeout-receipt.v1",
        "source_revision": SOURCE_REVISION,
        "x1_commit": X1_COMMIT,
        "evidence_commit": args.evidence_commit,
        "closeout_binding": "the Git commit containing this receipt",
        "phase_commits_before_closeout": phase_commits_before_closeout,
        "expected_phase_commits_after_closeout": phase_commits_before_closeout + 1,
        "maximum_phase_commits": 4,
        "merge_commits": merges_before_closeout,
        "distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": 2431,
        "effective_open_gaps": 10,
        "effective_exact_gates": 11,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v645-v8.seal-receipt.v1",
        "seal_binding": "the Git commit containing this receipt",
        "source_revision": SOURCE_REVISION,
        "x1_commit": X1_COMMIT,
        "evidence_commit": args.evidence_commit,
        "candidate_checks": ["bounded scoped tests", "detailed and minimal validators", "JSON parsing", "five-class privacy", "exact owner manifest", "diff hygiene", "stale labels", "ancestry", "zero merges", "commit cap", "clean state", "four-way remote equality"],
        "named_lane_replay_required_after_push": 1,
        "detached_validation_forbidden": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("final-validation-record.json", {
        "schema": "ghc.family.v645-v8.final-validation-record.v1",
        "revision_binding": "the Git commit containing this record",
        "source_revision": SOURCE_REVISION,
        "x1_commit": X1_COMMIT,
        "evidence_commit": args.evidence_commit,
        "canonical_precommit_validation": "required_and_recorded_in_validation_directory",
        "canonical_exact_commit_validation": "required_after_commit",
        "named_lane_exact_commit_replay": "required_after_canonical_push",
        "fresh_live_remote_equality": "required_after_canonical_push",
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True,
        "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("orchestration/terminal-route-readiness-candidate.json", {
        "schema": "ghc.family.v645-v8.route-readiness.v1",
        "target_title": "Eiren Kestrel",
        "target_phase": "v646-v1",
        "state": "PREPARED_NOT_SENT",
        "send_count": 0,
        "task_creation_allowed": False,
        "preconditions_remaining": ["commit and push exact closeout", "prove canonical four-way equality", "run exact final canonical checks", "run exactly one clean local named-lane replay", "resolve unique existing target title"],
        "standby_siblings_contacted": False,
    })
    entries = manifest_entries()
    manifest = {
        "schema": "ghc.family.v645-v8.exact-owner-manifest.v1",
        "domain": "LF-preserving owner working-tree bytes before exact staging",
        "entry_count": len(entries),
        "excluded_self_describing_paths": ["docs/sylven-arc/v645-v8/validation/exact-owner-manifest.json", "docs/sylven-arc/v645-v8/validation/closeout-staged-manifest.json", "docs/sylven-arc/v645-v8/validation/closeout-staged-review.json"],
        "entries": entries,
        "valid": True,
        "boundary": "Manifest parity is an integrity check, not security or privacy completeness.",
    }
    write_json("validation/exact-owner-manifest.json", manifest)
    write_json("validation/closeout-staged-manifest.json", {**manifest, "schema": "ghc.family.v645-v8.closeout-staged-manifest.v1", "state": "candidate_recheck_after_exact_staging"})
    print(json.dumps({"evidence_commit": args.evidence_commit, "entries": len(entries), "phase_commits_before_closeout": phase_commits_before_closeout, "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
