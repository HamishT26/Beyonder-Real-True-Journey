#!/usr/bin/env python3
"""One-pass exact-final canonical validator for Lyren Moss v653-v2."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v653_v2_detailed_validator as detailed
import ghc_family_v653_v2_minimal_validator as minimal
from ghc_family_v653_v2_validation_common import (
    PHASE,
    REPO,
    phase_public_paths,
    read_json,
    revision_blob_map,
    scan_privacy_paths,
)


SOURCE = "97989717f8447ef2fa09a37a92c76617dea30874"
X1 = "90cc4cff205fef8b7fe0fb1218083e9ced14f146"
EVIDENCE = "6728c0e6d2a5b16a56f08b80e60fdbfe36818427"
TEST_MODULES = [
    "tests.test_ghc_family_v653_v2_x1",
    "tests.test_ghc_family_v653_v2_core",
    "tests.test_ghc_family_v653_v2_validation",
    "tests.test_ghc_family_v653_v2_closeout",
]


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(args, cwd=REPO, check=check, capture_output=True, text=True, encoding="utf-8", env=env)


def git(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def test_result() -> dict[str, Any]:
    result = run([sys.executable, "-m", "unittest", "-q", *TEST_MODULES], check=False)
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "tests_run": int(match.group(1)) if match else 0,
        "failures": len(re.findall(r"^FAIL:", output, flags=re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, flags=re.MULTILINE)),
        "exit_code": result.returncode,
        "valid": result.returncode == 0 and match is not None,
    }


def validate(expected_head: str) -> dict[str, Any]:
    clean_before = git("status", "--porcelain=v1") == ""
    head = git("rev-parse", "HEAD")
    tests = test_result()
    detailed_result = detailed.validate()
    minimal_result = minimal.validate()
    json_paths = sorted(PHASE.rglob("*.json"))
    parse_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_failures.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    privacy = scan_privacy_paths(phase_public_paths())

    owner_manifest = read_json(PHASE / "validation/final-owner-manifest.json")
    exclusions = set(owner_manifest["self_exclusions"])
    actual_paths = {path.relative_to(REPO).as_posix() for path in phase_public_paths()}
    manifest_paths = {row["path"] for row in owner_manifest["entries"]}
    manifest_issues = []
    if manifest_paths != actual_paths - exclusions:
        manifest_issues.append("path_coverage")
    committed_blobs = revision_blob_map(
        [row["path"] for row in owner_manifest["entries"]]
    )
    for row in owner_manifest["entries"]:
        if committed_blobs[row["path"]] != row["git_blob"]:
            manifest_issues.append(f"blob:{row['path']}")

    final_review = read_json(PHASE / "validation/final-staged-review.json")
    final_manifest = read_json(PHASE / "validation/final-staged-manifest.json")
    stale_tokens = ("PENDING_EVIDENCE_COMMIT", "PENDING_X1_COMMIT", "PENDING_FINAL_COMMIT", "<FINAL_COMMIT>")
    stale_hits = []
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".html", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8")
            if any(token in text for token in stale_tokens):
                stale_hits.append(path.relative_to(REPO).as_posix())

    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_row = git("ls-remote", "origin", f"refs/heads/{branch}")
    live = live_row.split("\t", 1)[0] if live_row else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    ancestry = {}
    for name, anchor in (("source", SOURCE), ("x1", X1), ("evidence", EVIDENCE)):
        ancestry[name] = run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], check=False).returncode == 0
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    phase_merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"))
    parents = git("rev-list", "--parents", f"{SOURCE}..HEAD").splitlines()
    all_single_parent = all(len(row.split()) == 2 for row in parents)
    final_parent = git("rev-parse", "HEAD^")
    diff_hygiene = git("diff-tree", "--check", "HEAD^", "HEAD") == ""
    clean_after = git("status", "--porcelain=v1") == ""

    lifecycle_checks = {
        "expected_head": head == expected_head,
        "head_parent_is_evidence": final_parent == EVIDENCE,
        "source_ancestral": ancestry["source"],
        "x1_ancestral": ancestry["x1"],
        "evidence_ancestral": ancestry["evidence"],
        "three_phase_commits": phase_commits == 3,
        "within_eight_commit_cap": phase_commits <= 8,
        "zero_merges": phase_merges == 0,
        "all_single_parent": all_single_parent,
        "local_upstream_tracking_live_equal": head == upstream == tracking == live,
        "zero_divergence": divergence.replace("\t", " ") == "0 0",
        "clean_before": clean_before,
        "clean_after": clean_after,
        "diff_hygiene": diff_hygiene,
        "final_staged_review": final_review["valid"],
        "final_staged_manifest": final_manifest["entry_count"] > 0,
        "owner_manifest": not manifest_issues,
        "stale_labels": not stale_hits,
        "json": not parse_failures,
        "privacy": privacy["valid"],
        "route_prepared_for_exact_successor": (
            read_json(PHASE / "orchestration/terminal-route-state.json")["state"]
            == "PREPARED_NOT_SENT"
            and read_json(PHASE / "orchestration/terminal-route-state.json")[
                "successor_title"
            ]
            == "Ilyra Fen"
            and not read_json(
                PHASE / "orchestration/terminal-route-state.json"
            )["activation_sent"]
        ),
    }
    valid = (
        tests["valid"]
        and detailed_result["valid"]
        and minimal_result["valid"]
        and all(lifecycle_checks.values())
    )
    return {
        "schema": "ghc.family.v653-v2.exact-final-validation.v1",
        "exact_final_head": head,
        "tests": tests,
        "detailed_check_count": detailed_result["check_count"],
        "detailed_passed_count": detailed_result["passed_count"],
        "minimal_check_count": minimal_result["check_count"],
        "minimal_passed_count": minimal_result["passed_count"],
        "json_parse_count": len(json_paths),
        "json_parse_failures": parse_failures,
        "privacy": privacy,
        "owner_manifest_entry_count": owner_manifest["entry_count"],
        "owner_manifest_issues": manifest_issues,
        "final_staged_manifest_entry_count": final_manifest["entry_count"],
        "stale_label_hits": stale_hits,
        "lifecycle_check_count": len(lifecycle_checks),
        "lifecycle_checks": lifecycle_checks,
        "phase_commit_count": phase_commits,
        "phase_merge_count": phase_merges,
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": "One attributable exact-final canonical pass. Do not replay after success.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.expected_head)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
