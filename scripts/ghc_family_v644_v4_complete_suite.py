#!/usr/bin/env python3
"""Run the complete v644-v4 validation stack in one clean checkout."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_phase_privacy_scan import scan_phase
from ghc_family_repository_test_runner import run as run_repository_tests
from ghc_family_v644_v4_minimal import verify as verify_minimal
from ghc_family_v644_v4_validator import validate as validate_detailed


PHASE_REL = Path("docs/sylven-arc/v644-v4")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True, encoding="utf-8").strip()


def json_parse_floor(phase: Path) -> tuple[int, list[str]]:
    parsed = 0
    issues = []
    for path in sorted(phase.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except Exception as exc:  # pragma: no cover - defensive receipt path
            issues.append(f"{path.relative_to(phase).as_posix()}: {exc}")
    return parsed, issues


def run(
    repo: Path,
    expected_head: str,
    allow_pending_snapshot: bool = False,
) -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / PHASE_REL
    head = git(repo, "rev-parse", "HEAD")
    clean_before = git(repo, "status", "--porcelain=v1", "--untracked-files=all") == ""
    test_result = run_repository_tests(repo / "tests", "test_*.py", sys.platform == "win32")
    detailed = validate_detailed(repo, phase, allow_pending_snapshot, expected_head)
    minimal = verify_minimal(phase, allow_pending_snapshot)
    privacy = scan_phase(repo, phase, set())
    json_parsed, json_issues = json_parse_floor(phase)
    diff_worktree = subprocess.run(
        ["git", "diff", "--check"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    diff_head = subprocess.run(
        ["git", "diff", "HEAD", "--check"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    clean_after = git(repo, "status", "--porcelain=v1", "--untracked-files=all") == ""
    repository_valid = test_result.wasSuccessful()
    diff_hygiene = diff_worktree.returncode == 0 and diff_head.returncode == 0
    valid = all(
        [
            head == expected_head,
            clean_before,
            repository_valid,
            detailed["valid"],
            minimal["valid"],
            privacy["valid"],
            not json_issues,
            detailed["manifest_mismatch_count"] == 0,
            diff_hygiene,
            clean_after,
        ]
    )
    return {
        "schema": "ghc.family.v644-v4.complete-suite.v1",
        "phase": "v644-gmut-thos-v4-x1-x2",
        "valid": valid,
        "head": head,
        "expected_head": expected_head,
        "exact_head": head == expected_head,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "repository_tests": {
            "passed": test_result.testsRun - len(test_result.failures) - len(test_result.errors),
            "total": test_result.testsRun,
            "failures": len(test_result.failures),
            "errors": len(test_result.errors),
            "skipped": len(test_result.skipped),
            "valid": repository_valid,
        },
        "detailed": {
            "passed": detailed["checks_passed"],
            "total": detailed["checks_total"],
            "issues": detailed["issues"],
            "valid": detailed["valid"],
        },
        "minimal": {
            "passed": minimal["checks_passed"],
            "total": minimal["checks_total"],
            "issues": minimal["issues"],
            "valid": minimal["valid"],
        },
        "json": {"parsed": json_parsed, "issues": json_issues, "valid": not json_issues},
        "privacy": {
            "files": privacy["scanned_file_count"],
            "hits": privacy["hit_count"],
            "valid": privacy["valid"],
        },
        "manifest": {
            "entries": detailed["manifest_entries"],
            "mismatches": detailed["manifest_mismatch_count"],
            "valid": detailed["manifest_mismatch_count"] == 0,
        },
        "diff_hygiene": {
            "valid": diff_hygiene,
            "worktree_output": diff_worktree.stdout,
            "head_output": diff_head.stdout,
        },
        "allow_pending_snapshot": allow_pending_snapshot,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.repo, args.expected_head, args.allow_pending_snapshot)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else args.repo.resolve() / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "head": result["head"],
                "clean_before": result["clean_before"],
                "clean_after": result["clean_after"],
                "repository_tests": result["repository_tests"],
                "detailed": result["detailed"],
                "minimal": result["minimal"],
                "json": result["json"],
                "privacy": result["privacy"],
                "manifest": result["manifest"],
                "diff_hygiene": result["diff_hygiene"]["valid"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
