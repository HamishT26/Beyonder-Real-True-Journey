#!/usr/bin/env python3
"""Run Tamar v657-v8's single exact-final canonical aggregate."""

from __future__ import annotations

import argparse
import importlib
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

import build_ghc_family_v657_v8_closeout_receipts as closeout_receipts
import build_ghc_family_v657_v8_evidence_receipts as evidence_receipts
import ghc_family_v657_v8_closeout_config as c
import ghc_family_v657_v8_detailed_validator as detailed
import ghc_family_v657_v8_minimal_validator as minimal
import ghc_family_v657_v8_phase_data as d
import ghc_family_v657_v8_scoped_test_runner as scoped


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def replay_manifest(relative: str, commit: str) -> dict[str, Any]:
    payload = json.loads(git("show", f"{commit}:{d.PHASE_ROOT}/{relative}"))
    mismatches = []
    for entry in payload["entries"]:
        observed = git("rev-parse", f"{commit}:{entry['path']}")
        if observed != entry["git_blob"]:
            mismatches.append({"path": entry["path"], "expected": entry["git_blob"], "observed": observed})
    return {
        "manifest": relative,
        "entry_count": payload["entry_count"],
        "declared_exclusion_count": payload.get("declared_exclusion_count", 0),
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def closeout_tests() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    module = importlib.import_module("tests.test_ghc_family_v657_v8_closeout")
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    expected = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "valid": result.wasSuccessful() and result.testsRun == expected and not result.skipped,
        "tests_run": result.testsRun,
        "expected_tests": expected,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failed_test_ids": [case.id() for case, _ in result.failures],
        "error_test_ids": [case.id() for case, _ in result.errors],
        "runner_output": stream.getvalue(),
    }


def validate(output: Path) -> dict[str, Any]:
    output = output.resolve()
    if output.exists():
        raise RuntimeError("canonical output already exists; post-success replay is forbidden")
    if output.is_relative_to(ROOT.resolve()):
        raise RuntimeError("canonical receipt must be external to the repository")

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{c.BRANCH}")
    live = git("ls-remote", "--heads", "origin", c.BRANCH).split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    status_before = git("status", "--porcelain=v1")
    final_parent = git("rev-parse", "HEAD^")
    phase_commits = int(git("rev-list", "--count", f"{c.SOURCE_COMMIT}..HEAD"))
    merge_commits = int(git("rev-list", "--count", "--merges", f"{c.SOURCE_COMMIT}..HEAD"))
    ordered = git("rev-list", "--reverse", f"{c.SOURCE_COMMIT}..HEAD").splitlines()
    parent_counts = [len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in ordered]
    ancestry = {}
    for label, commit in {
        "source": c.SOURCE_COMMIT,
        "x1": c.X1_COMMIT,
        "evidence": c.EVIDENCE_COMMIT,
    }.items():
        ancestry[label] = run("git", "merge-base", "--is-ancestor", commit, head, check=False).returncode == 0
    diff_hygiene = run("git", "diff", "--check", c.SOURCE_COMMIT, head, check=False).returncode

    x1_manifest = replay_manifest("validation/x1-content-manifest.json", c.X1_COMMIT)
    evidence_manifest = replay_manifest("validation/evidence-content-manifest.json", c.EVIDENCE_COMMIT)
    closeout_manifest = replay_manifest("validation/closeout-content-manifest.json", head)
    staged_review = load("validation/closeout-staged-review.json")

    scoped_result = scoped.run_scope()
    closeout_result = closeout_tests()
    detailed_result = detailed.validate()
    minimal_result = minimal.validate()

    json_paths = sorted(PHASE.rglob("*.json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_failures.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})

    privacy_hits = []
    owner_paths = closeout_receipts.owner_paths()
    for path in owner_paths:
        privacy_hits.extend(
            evidence_receipts.scan_text(
                path.relative_to(ROOT).as_posix(), path.read_text(encoding="utf-8")
            )
        )

    route = load("orchestration/route-state-final-candidate.json")
    truth = load("truth/phase-truth.json")
    checks = {
        "exact_branch": branch == c.BRANCH,
        "clean_before": not status_before,
        "four_way_equality": len({head, upstream, tracking, live}) == 1,
        "zero_divergence": divergence.split() == ["0", "0"],
        "final_parent_is_evidence": final_parent == c.EVIDENCE_COMMIT,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merge_commits == 0,
        "one_parent_each": parent_counts == [1, 1, 1],
        "complete_ancestry": all(ancestry.values()),
        "diff_hygiene": diff_hygiene == 0,
        "x1_manifest": x1_manifest["valid"],
        "evidence_manifest": evidence_manifest["valid"],
        "closeout_manifest": closeout_manifest["valid"],
        "closeout_staged_review": staged_review["valid"],
        "scoped_tests": scoped_result["valid"],
        "closeout_tests": closeout_result["valid"],
        "detailed": detailed_result["valid"],
        "minimal": minimal_result["valid"],
        "json_parse": not json_failures,
        "privacy": not privacy_hits,
        "truth_distribution": truth["outcome_counts"] == d.EXPECTED_DISTRIBUTION,
        "zero_real_rows": truth["real_rows"] == 0,
        "not_stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": truth["independent_reproduction"] is False,
        "no_successor_authorized": route["state"] == "NO_SUCCESSOR_AUTHORIZED_REQUIRES_FRESH_LIVE_ROUTE",
        "no_message_sent": route["message_sent"] is False and route["next_exact_title"] is None,
        "full_repository_suite_not_run": True,
    }
    payload = {
        "schema": "ghc.family.v657-v8.exact-final-canonical-validation.v1",
        "valid": all(checks.values()),
        "canonical_pass_number": 1,
        "canonical_invocation_count": 1,
        "post_success_replay_forbidden": True,
        "exact_final": head,
        "branch": branch,
        "source_commit": c.SOURCE_COMMIT,
        "x1_commit": c.X1_COMMIT,
        "evidence_commit": c.EVIDENCE_COMMIT,
        "four_way": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live},
        "divergence": divergence,
        "history": {
            "phase_commit_count": phase_commits,
            "merge_count": merge_commits,
            "parent_counts": parent_counts,
            "final_parent": final_parent,
            "ancestry": ancestry,
        },
        "checks": checks,
        "check_count": len(checks),
        "scoped_tests": scoped_result,
        "closeout_tests": closeout_result,
        "tests_run": scoped_result["tests_run"] + closeout_result["tests_run"],
        "tests_expected": scoped_result["expected_tests"] + closeout_result["expected_tests"],
        "detailed": detailed_result,
        "minimal": minimal_result,
        "json_parse_count": len(json_paths),
        "json_failures": json_failures,
        "privacy_file_count": len(owner_paths),
        "privacy_pattern_class_count": len(evidence_receipts.PRIVACY_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "manifests": {"x1": x1_manifest, "evidence": evidence_manifest, "closeout": closeout_manifest},
        "manifest_entry_total": x1_manifest["entry_count"] + evidence_manifest["entry_count"] + closeout_manifest["entry_count"],
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "route_state": route["state"],
        "message_sent": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    status_after = git("status", "--porcelain=v1")
    if status_after:
        raise RuntimeError("repository became dirty during external canonical validation")
    print(
        json.dumps(
            {
                "valid": payload["valid"],
                "exact_final": head,
                "tests": f"{payload['tests_run']}/{payload['tests_expected']}",
                "detailed": f"{detailed_result['check_count']}/{detailed_result['check_count']}",
                "minimal": f"{minimal_result['check_count']}/{minimal_result['check_count']}",
                "json": len(json_paths),
                "privacy_files": len(owner_paths),
                "manifest_entries": payload["manifest_entry_total"],
                "terminal_checks": f"{sum(checks.values())}/{len(checks)}",
            },
            sort_keys=True,
        )
    )
    if not payload["valid"]:
        raise SystemExit(1)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    validate(ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output))


if __name__ == "__main__":
    main()
