#!/usr/bin/env python3
"""Corrected exclusive exact-final canonical validator for Sable Rook v664-v7."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_terminal_correction as correction  # noqa: E402
import ghc_family_v664_v7_canonical_validator as v1  # noqa: E402


SOURCE = correction.SOURCE
X1 = correction.X1
EVIDENCE = correction.EVIDENCE
BASE_FINAL = correction.BASE_FINAL
BRANCH = correction.BRANCH
PREFIX = correction.PREFIX
VERDICT = correction.VERDICT
TEST_MODULES = [
    "tests.test_ghc_family_sable_v664_v7_x1",
    "tests.test_ghc_family_sable_v664_v7_x2",
    "tests.test_ghc_family_sable_v664_v7_closeout",
    "tests.test_ghc_family_sable_v664_v7_terminal_correction",
]


class CorrectedCanonicalError(RuntimeError):
    """Raised when the corrected canonical contract cannot run."""


def read_json(commit: str, path: str) -> dict[str, Any]:
    value = v1.strict_json(v1.git_blob(commit, path), path)
    if not isinstance(value, dict):
        raise CorrectedCanonicalError(f"JSON root is not an object: {path}")
    return value


def replay_owner_manifest(final: str) -> dict[str, Any]:
    path = correction.CORRECTION_OWNER_MANIFEST
    manifest = read_json(final, path)
    expected = v1.git_paths("diff", "--name-only", "-z", f"{SOURCE}..{final}")
    covered = sorted([row["path"] for row in manifest["entries"]] + manifest["declared_self_exclusions"])
    mismatches: list[str] = []
    if covered != expected:
        mismatches.append("path_coverage")
    for row in manifest["entries"]:
        raw = v1.git_blob(final, row["path"])
        oid = v1.git_text("rev-parse", f"{final}:{row['path']}")
        if oid != row["git_blob"] or v1.sha256(raw) != row["sha256"] or len(raw) != row["size"]:
            mismatches.append(row["path"])
    return {
        "manifest": path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "expected_path_count": len(expected),
        "mismatches": mismatches,
        "valid": manifest.get("coverage_valid") is True and not mismatches,
    }


def validate(expected_final: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    clean_before = not v1.git_text("status", "--porcelain=v1")
    head = v1.git_text("rev-parse", "HEAD")
    branch = v1.git_text("branch", "--show-current")
    record("exact_head", head == expected_final, head)
    record("expected_branch", branch == BRANCH, branch)
    record("clean_before", clean_before, clean_before)

    final_parent = v1.git_text("rev-parse", f"{head}^")
    base_parent = v1.git_text("rev-parse", f"{BASE_FINAL}^")
    evidence_parent = v1.git_text("rev-parse", f"{EVIDENCE}^")
    x1_parent = v1.git_text("rev-parse", f"{X1}^")
    record("correction_direct_base_parent", final_parent == BASE_FINAL, final_parent)
    record("base_direct_evidence_parent", base_parent == EVIDENCE, base_parent)
    record("evidence_direct_x1_parent", evidence_parent == X1, evidence_parent)
    record("x1_direct_source_parent", x1_parent == SOURCE, x1_parent)

    phase_commits = int(v1.git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = v1.git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines()
    commits = [row for row in v1.git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if row]
    parent_counts = [len(v1.git_text("show", "-s", "--format=%P", commit).split()) for commit in commits]
    record("four_phase_commits", phase_commits == 4, phase_commits)
    record("zero_merges", not merges, len(merges))
    record("single_parent_phase_history", all(count == 1 for count in parent_counts), parent_counts)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(SCRIPTS), env.get("PYTHONPATH", "")])
    tests = v1.run([sys.executable, "-m", "unittest", *TEST_MODULES], env=env)
    test_output = (tests.stdout + tests.stderr).decode("utf-8", "replace")
    match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(match.group(1)) if match else 0
    record("scoped_tests", tests.returncode == 0 and test_count > 0, {"count": test_count, "returncode": tests.returncode})

    x1_manifest = v1.replay_sha_manifest(X1, SOURCE, f"{PREFIX}x1/x1-content-manifest.json")
    evidence_manifest = v1.replay_sha_manifest(EVIDENCE, X1, f"{PREFIX}validation/evidence-manifest.json")
    base_owner = v1.replay_owner_manifest(BASE_FINAL)
    base_delta = v1.replay_git_blob_manifest(
        BASE_FINAL,
        EVIDENCE,
        f"{PREFIX}validation/final-delta-manifest.json",
    )
    owner_manifest = replay_owner_manifest(head)
    correction_delta = v1.replay_git_blob_manifest(
        head,
        BASE_FINAL,
        correction.CORRECTION_DELTA_MANIFEST,
    )
    for name, value in (
        ("x1_manifest", x1_manifest),
        ("evidence_manifest", evidence_manifest),
        ("base_owner_manifest", base_owner),
        ("base_final_delta_manifest", base_delta),
        ("correction_owner_manifest", owner_manifest),
        ("correction_delta_manifest", correction_delta),
    ):
        record(name, value["valid"], value)

    owner_paths = v1.git_paths("diff", "--name-only", "-z", f"{SOURCE}..{head}")
    json_count = 0
    markdown_count = 0
    python_count = 0
    candidates: list[dict[str, str]] = []
    word_issues: list[dict[str, Any]] = []
    for path in owner_paths:
        raw = v1.git_blob(head, path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            v1.strict_json(raw, path)
            json_count += 1
        if suffix == ".py":
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if suffix == ".md":
            words = len(raw.decode("utf-8").split())
            markdown_count += 1
            if words > 100_000:
                word_issues.append({"path": path, "words": words})
        if suffix in correction.closeout.TEXT_SUFFIXES:
            candidates.extend(correction.corrected_scan(path, raw))
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_issue"]
    exact_adjudications = [
        row
        for row in candidates
        if row.get("adjudication")
        and row["excerpt_sha256"] in correction.SCANNER_DEFINITION_DIGESTS
        and row["path"] == correction.closeout.evidence.EVIDENCE_BUILDER
    ]
    record("strict_json", json_count > 0, json_count)
    record("python_compile", python_count > 0, python_count)
    record("document_word_caps", not word_issues, word_issues)
    record("owner_file_guard", len(owner_paths) < 2000, len(owner_paths))
    record(
        "five_class_privacy",
        not confirmed and len(exact_adjudications) == 2,
        {
            "scanned_text_files": sum(Path(path).suffix.lower() in correction.closeout.TEXT_SUFFIXES for path in owner_paths),
            "candidate_count": len(candidates),
            "scanner_definitions": sum(row["disposition"] == "scanner_definition" for row in candidates),
            "exact_carried_adjudications": len(exact_adjudications),
            "confirmed_hits": len(confirmed),
        },
    )

    diff = v1.git("diff", "--check", f"{SOURCE}..{head}", check=False)
    record("diff_hygiene", diff.returncode == 0, diff.returncode)
    route = read_json(head, f"{PREFIX}orchestration/terminal-route-state-correction.json")
    record(
        "route_prepared_not_sent",
        route.get("state") == "PREPARED_NOT_SENT" and route.get("send_count") == 0 and route.get("successor_title") is None,
        {"state": route.get("state"), "send_count": route.get("send_count")},
    )
    truth = read_json(head, f"{PREFIX}correction/phase-truth.json")
    record("terminal_verdict", truth.get("terminal_verdict") == VERDICT, truth.get("terminal_verdict"))
    failed_receipt = read_json(head, f"{PREFIX}correction/canonical-failure-receipt.json")
    record(
        "failed_canonical_preserved",
        failed_receipt.get("valid") is False
        and failed_receipt.get("completion_credit") == 0
        and failed_receipt.get("external_receipt_sha256") == correction.FAILED_CANONICAL_SHA256,
        failed_receipt.get("external_receipt_sha256"),
    )

    upstream = v1.git_text("rev-parse", "@{u}")
    tracking = v1.git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = v1.git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    divergence = v1.git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    ahead = int(divergence[0])
    behind = int(divergence[1])
    record("local_upstream_equality", head == upstream, upstream)
    record("local_tracking_equality", head == tracking, tracking)
    record("fresh_live_equality", head == live, live)
    record("typed_zero_divergence", ahead == 0 and behind == 0, {"ahead": ahead, "behind": behind})
    clean_after = not v1.git_text("status", "--porcelain=v1")
    record("clean_after", clean_after, clean_after)

    valid = all(row["passed"] for row in checks)
    return {
        "schema": "ghc.family.sable.v664-v7.external-exclusive-canonical-receipt.v2",
        "owner": "Sable Rook",
        "phase": "v664-v7",
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "base_failed_final": BASE_FINAL,
        "failed_canonical_receipt_sha256": correction.FAILED_CANONICAL_SHA256,
        "final": head,
        "invocation_policy": "one successful exact-final canonical invocation; no replay after success",
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "test_count": test_count,
        "strict_json_count": json_count,
        "markdown_count": markdown_count,
        "python_compile_count": python_count,
        "owner_path_count": len(owner_paths),
        "privacy_candidate_count": len(candidates),
        "exact_carried_scanner_adjudications": len(exact_adjudications),
        "confirmed_privacy_hits": len(confirmed),
        "manifest_replays": [x1_manifest, evidence_manifest, base_owner, base_delta, owner_manifest, correction_delta],
        "check_count": len(checks),
        "passed_check_count": sum(row["passed"] for row in checks),
        "checks": checks,
        "terminal_verdict": VERDICT,
        "valid": valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_final):
        raise CorrectedCanonicalError("expected final must be a full lowercase commit identifier")
    output = Path(args.output)
    if not output.is_absolute():
        raise CorrectedCanonicalError("external receipt path must be absolute")
    if output.exists():
        raise CorrectedCanonicalError("external receipt already exists; replay refused")
    result = validate(args.expected_final)
    v1.write_exclusive(output, result)
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "final": result["final"],
                "tests": result["test_count"],
                "checks": result["check_count"],
                "json": result["strict_json_count"],
                "owner_paths": result["owner_path_count"],
                "exact_scanner_adjudications": result["exact_carried_scanner_adjudications"],
                "confirmed_privacy_hits": result["confirmed_privacy_hits"],
                "terminal_verdict": result["terminal_verdict"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
