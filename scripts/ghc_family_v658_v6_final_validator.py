#!/usr/bin/env python3
"""Run the single exact-final canonical validation for Neris v658-v6."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v6_phase_data as d  # noqa: E402
from ghc_family_v658_v6_minimal import validate_minimal  # noqa: E402
from ghc_family_v658_v6_validator import validate_phase  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1 = "1591612c83feb7f47fb0b044525bf4b37f71bfb7"
EVIDENCE = "35ee24d2e708451e3862cbb81bc9103a691bd497"
BRANCH = d.BRANCH


def git(*args: str, binary: bool = False) -> Any:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=not binary, encoding=None if binary else "utf-8")
    return result.stdout if binary else result.stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def manifest_replay(relative: str, revision: str) -> tuple[int, list[str]]:
    payload = load(relative)
    mismatches = []
    for row in payload["entries"]:
        try:
            blob = git("rev-parse", f"{revision}:{row['path']}")
        except subprocess.CalledProcessError:
            mismatches.append(row["path"])
            continue
        if blob != row["git_blob"]:
            mismatches.append(row["path"])
    return len(payload["entries"]), mismatches


def run_tests() -> dict[str, Any]:
    names = ["tests.test_ghc_family_v658_v6_x1", "tests.test_ghc_family_v658_v6", "tests.test_ghc_family_v658_v6_closeout"]
    suite = unittest.TestLoader().loadTestsFromNames(names)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "modules": names,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "diagnostic_tail": stream.getvalue().splitlines()[-8:],
    }


def privacy_scan(paths: list[str], revision: str) -> dict[str, Any]:
    patterns = {
        "raw_task_thread_session_identifier": re.compile(r"(?i)\b(?:thread|task|session)[_-]?(?:id|identifier)\s*[:=]\s*[0-9a-f-]{20,}"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "credential_or_secret": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,;]{12,}"),
        "private_absolute_path": re.compile(r"(?i)\b[a-z]:\\(?:users|ghc-archives)\\[^\s\"']+"),
        "private_callable_identifier": re.compile(r"(?i)\bmcp__[A-Za-z0-9_]{8,}"),
    }
    hits = []
    for path in paths:
        raw = git("show", f"{revision}:{path}", binary=True)
        text = raw.decode("utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": label})
    return {"file_count": len(paths), "pattern_class_count": len(patterns), "hit_count": len(hits), "hits": hits, "valid": not hits}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    expected = args.expected_head
    clean_before = git("status", "--porcelain=v1") == ""
    head = git("rev-parse", "HEAD")
    parent = git("rev-parse", "HEAD^")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", f"{head}...{upstream}")
    ancestry = {}
    for name, anchor in {"source": SOURCE, "x1": X1, "evidence": EVIDENCE}.items():
        result = subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=ROOT)
        ancestry[name] = result.returncode == 0
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_count = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parent_rows = [line.split() for line in git("rev-list", "--parents", f"{SOURCE}..{head}").splitlines() if line]
    all_single_parent = all(len(row) == 2 for row in parent_rows)

    tests = run_tests()
    detailed = validate_phase()
    minimal = validate_minimal()
    json_files = sorted(PHASE.rglob("*.json"))
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - terminal diagnostic
            json_errors.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})

    owner_paths = sorted(line for line in git("diff", "--name-only", SOURCE, head).splitlines() if line)
    privacy = privacy_scan(owner_paths, head)
    manifest_specs = [
        ("reproduction/x1-content-seal.json", X1),
        ("validation/evidence-commit-local-manifest.json", EVIDENCE),
        ("validation/final-delta-manifest.json", head),
        ("final/final-owner-manifest.json", head),
    ]
    manifest_rows = []
    for relative, revision in manifest_specs:
        count, mismatches = manifest_replay(relative, revision)
        manifest_rows.append({"path": relative, "revision": revision, "entry_count": count, "mismatch_count": len(mismatches), "mismatches": mismatches})
    final_delta = load("validation/final-delta-manifest.json")
    actual_delta = set(line for line in git("diff", "--name-only", EVIDENCE, head).splitlines() if line)
    declared_delta = {row["path"] for row in final_delta["entries"]}
    delta_exclusions = {f"{d.PHASE_ROOT}/{path}" for path in final_delta["self_exclusions"]}
    delta_coverage_valid = actual_delta == declared_delta | delta_exclusions
    owner_manifest = load("final/final-owner-manifest.json")
    declared_owner = {row["path"] for row in owner_manifest["entries"]}
    owner_exclusions = {f"{d.PHASE_ROOT}/{path}" for path in owner_manifest["self_exclusions"]}
    owner_coverage_valid = set(owner_paths) == declared_owner | owner_exclusions

    checks = {
        "expected_head": head == expected,
        "clean_before": clean_before,
        "parent_is_evidence": parent == EVIDENCE,
        "local_equals_upstream": head == upstream,
        "local_equals_tracking": head == tracking,
        "local_equals_live": head == live,
        "zero_divergence": divergence.replace("\t", " ").strip() == "0 0",
        "all_anchors_ancestral": all(ancestry.values()),
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merge_count == 0,
        "all_single_parent": all_single_parent,
        "tests": tests["successful"],
        "detailed": detailed["valid"],
        "minimal": minimal["valid"],
        "json": not json_errors,
        "privacy": privacy["valid"],
        "manifests": all(row["mismatch_count"] == 0 for row in manifest_rows),
        "delta_coverage": delta_coverage_valid,
        "owner_coverage": owner_coverage_valid,
        "diff_hygiene": subprocess.run(["git", "diff", "--check", f"{SOURCE}..{head}"], cwd=ROOT, capture_output=True).returncode == 0,
        "commit_cap": phase_commits <= 8,
        "terminal_verdict": load("truth/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": load("orchestration/route-state-final-candidate.json")["state"] == "PREPARED_NOT_SENT" and load("orchestration/route-state-final-candidate.json")["message_sent"] is False,
    }
    valid_before_write = all(checks.values())
    receipt = {
        "schema": "ghc.family.v658-v6.external-canonical-validation.v1",
        "valid": valid_before_write,
        "exact_final": head,
        "expected_final": expected,
        "source_final": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_parent": parent,
        "branch": BRANCH,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": live,
        "divergence": divergence,
        "ancestry": ancestry,
        "phase_commit_count": phase_commits,
        "merge_count": merge_count,
        "all_single_parent": all_single_parent,
        "tests": tests,
        "detailed_check_count": detailed["check_count"],
        "detailed_error_count": detailed["error_count"],
        "minimal_check_count": minimal["check_count"],
        "minimal_error_count": minimal["error_count"],
        "json_parse_count": len(json_files),
        "json_errors": json_errors,
        "privacy": privacy,
        "manifests": manifest_rows,
        "manifest_replay_count": sum(row["entry_count"] for row in manifest_rows),
        "delta_coverage_valid": delta_coverage_valid,
        "owner_coverage_valid": owner_coverage_valid,
        "checks": checks,
        "same_owner_only": True,
        "independent_reproduction": False,
        "canonical_success_count": 1 if valid_before_write else 0,
        "post_success_replay_count": 0,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Bounded same-owner canonical validation under shared infrastructure only; not external audit, empirical confirmation, professional certification, production readiness, complete privacy or accessibility, independent reproduction, Theory-of-Everything proof, or Stage 20 authority.",
    }
    output = Path(args.json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    clean_after = git("status", "--porcelain=v1") == ""
    receipt_sha = hashlib.sha256(output.read_bytes()).hexdigest()
    summary = {"valid": valid_before_write and clean_after, "exact_final": head, "tests": tests["tests_run"], "detailed": detailed["check_count"], "minimal": minimal["check_count"], "json": len(json_files), "privacy_files": privacy["file_count"], "privacy_hits": privacy["hit_count"], "manifest_replays": receipt["manifest_replay_count"], "clean_before": clean_before, "clean_after": clean_after, "receipt_sha256": receipt_sha}
    print(json.dumps(summary, sort_keys=True))
    if not summary["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
