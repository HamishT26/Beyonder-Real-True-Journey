#!/usr/bin/env python3
"""Exclusive exact-final canonical validator for Sable Rook v664-v7."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_closeout as closeout  # noqa: E402


SOURCE = closeout.SOURCE
X1 = closeout.X1
EVIDENCE = closeout.EVIDENCE
BRANCH = closeout.BRANCH
PREFIX = closeout.PREFIX
VERDICT = closeout.VERDICT
TEST_MODULES = [
    "tests.test_ghc_family_sable_v664_v7_x1",
    "tests.test_ghc_family_sable_v664_v7_x2",
    "tests.test_ghc_family_sable_v664_v7_closeout",
]


class CanonicalError(RuntimeError):
    """Raised when the canonical validation contract cannot run."""


def run(
    args: list[str],
    *,
    check: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    if check and result.returncode:
        raise CanonicalError(
            (result.stdout + result.stderr).decode("utf-8", "replace").strip()
            or f"command failed: {args}"
        )
    return result


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", *args], check=check)


def git_text(*args: str, check: bool = True) -> str:
    return git(*args, check=check).stdout.decode("utf-8", "strict").strip()


def git_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").stdout


def git_paths(*args: str) -> list[str]:
    raw = git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def strict_json(raw: bytes, label: str) -> Any:
    return closeout.strict_json(raw, label)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_commit_json(commit: str, path: str) -> dict[str, Any]:
    value = strict_json(git_blob(commit, path), path)
    if not isinstance(value, dict):
        raise CanonicalError(f"JSON root is not an object: {path}")
    return value


def replay_sha_manifest(
    commit: str,
    base: str,
    manifest_path: str,
) -> dict[str, Any]:
    manifest = read_commit_json(commit, manifest_path)
    expected_paths = git_paths("diff", "--name-only", "-z", f"{base}..{commit}")
    covered = sorted([row["path"] for row in manifest["entries"]] + manifest["declared_self_exclusions"])
    mismatches: list[str] = []
    if covered != expected_paths:
        mismatches.append("path_coverage")
    for row in manifest["entries"]:
        raw = git_blob(commit, row["path"])
        if sha256(raw) != row["sha256"] or len(raw) != row["size"]:
            mismatches.append(row["path"])
    return {
        "manifest": manifest_path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "expected_path_count": len(expected_paths),
        "mismatches": mismatches,
        "valid": manifest.get("coverage_valid") is True and not mismatches,
    }


def replay_git_blob_manifest(
    commit: str,
    base: str,
    manifest_path: str,
) -> dict[str, Any]:
    manifest = read_commit_json(commit, manifest_path)
    expected_paths = git_paths("diff", "--name-only", "-z", f"{base}..{commit}")
    covered = sorted([row["path"] for row in manifest["entries"]] + manifest["declared_self_exclusions"])
    mismatches: list[str] = []
    if covered != expected_paths:
        mismatches.append("path_coverage")
    for row in manifest["entries"]:
        raw = git_blob(commit, row["path"])
        oid = git_text("rev-parse", f"{commit}:{row['path']}")
        if oid != row["git_blob"] or sha256(raw) != row["sha256"] or len(raw) != row["size"]:
            mismatches.append(row["path"])
    return {
        "manifest": manifest_path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "expected_path_count": len(expected_paths),
        "mismatches": mismatches,
        "valid": manifest.get("coverage_valid") is True and not mismatches,
    }


def replay_owner_manifest(final: str) -> dict[str, Any]:
    path = f"{PREFIX}validation/final-owner-manifest.json"
    manifest = read_commit_json(final, path)
    expected_paths = git_paths("diff", "--name-only", "-z", f"{SOURCE}..{final}")
    covered = sorted([row["path"] for row in manifest["entries"]] + manifest["declared_self_exclusions"])
    mismatches: list[str] = []
    if covered != expected_paths:
        mismatches.append("path_coverage")
    for row in manifest["entries"]:
        raw = git_blob(final, row["path"])
        oid = git_text("rev-parse", f"{final}:{row['path']}")
        if oid != row["git_blob"] or sha256(raw) != row["sha256"] or len(raw) != row["size"]:
            mismatches.append(row["path"])
    return {
        "manifest": path,
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "expected_path_count": len(expected_paths),
        "mismatches": mismatches,
        "valid": manifest.get("coverage_valid") is True and not mismatches,
    }


def write_exclusive(path: Path, payload: dict[str, Any]) -> None:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=2,
    ).encode("utf-8") + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def validate(expected_final: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    clean_before = not git_text("status", "--porcelain=v1")
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    record("exact_head", head == expected_final, head)
    record("expected_branch", branch == BRANCH, branch)
    record("clean_before", clean_before, clean_before)

    parent = git_text("rev-parse", f"{head}^")
    evidence_parent = git_text("rev-parse", f"{EVIDENCE}^")
    x1_parent = git_text("rev-parse", f"{X1}^")
    record("final_direct_evidence_parent", parent == EVIDENCE, parent)
    record("evidence_direct_x1_parent", evidence_parent == X1, evidence_parent)
    record("x1_direct_source_parent", x1_parent == SOURCE, x1_parent)

    phase_commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = git_paths("rev-list", "--merges", "-z", f"{SOURCE}..{head}")
    commits = [row for row in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if row]
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).split()) for commit in commits]
    record("three_phase_commits", phase_commits == 3, phase_commits)
    record("zero_merges", not merges, len(merges))
    record("single_parent_phase_history", all(count == 1 for count in parent_counts), parent_counts)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(SCRIPTS), env.get("PYTHONPATH", "")])
    tests = run([sys.executable, "-m", "unittest", *TEST_MODULES], env=env)
    test_output = (tests.stdout + tests.stderr).decode("utf-8", "replace")
    match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(match.group(1)) if match else 0
    record("scoped_tests", tests.returncode == 0 and test_count > 0, {"count": test_count, "returncode": tests.returncode})

    x1_manifest = replay_sha_manifest(X1, SOURCE, f"{PREFIX}x1/x1-content-manifest.json")
    evidence_manifest = replay_sha_manifest(EVIDENCE, X1, f"{PREFIX}validation/evidence-manifest.json")
    owner_manifest = replay_owner_manifest(head)
    delta_manifest = replay_git_blob_manifest(head, EVIDENCE, f"{PREFIX}validation/final-delta-manifest.json")
    for name, value in (
        ("x1_manifest", x1_manifest),
        ("evidence_manifest", evidence_manifest),
        ("owner_manifest", owner_manifest),
        ("final_delta_manifest", delta_manifest),
    ):
        record(name, value["valid"], value)

    owner_paths = git_paths("diff", "--name-only", "-z", f"{SOURCE}..{head}")
    json_count = 0
    markdown_count = 0
    python_count = 0
    privacy_candidates: list[dict[str, str]] = []
    document_word_issues: list[dict[str, Any]] = []
    for path in owner_paths:
        raw = git_blob(head, path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            strict_json(raw, path)
            json_count += 1
        if suffix == ".py":
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if suffix == ".md":
            words = len(raw.decode("utf-8").split())
            markdown_count += 1
            if words > 100_000:
                document_word_issues.append({"path": path, "words": words})
        if suffix in closeout.TEXT_SUFFIXES:
            privacy_candidates.extend(closeout.scan(path, raw))
    confirmed = [row for row in privacy_candidates if row["disposition"] == "confirmed_issue"]
    record("strict_json", json_count > 0, json_count)
    record("python_compile", python_count > 0, python_count)
    record("document_word_caps", not document_word_issues, document_word_issues)
    record("owner_file_guard", len(owner_paths) < 2000, len(owner_paths))
    record(
        "five_class_privacy",
        not confirmed,
        {
            "scanned_text_files": sum(Path(path).suffix.lower() in closeout.TEXT_SUFFIXES for path in owner_paths),
            "candidate_count": len(privacy_candidates),
            "scanner_definitions": sum(row["disposition"] == "scanner_definition" for row in privacy_candidates),
            "confirmed_hits": len(confirmed),
        },
    )

    diff_hygiene = git("diff", "--check", f"{SOURCE}..{head}", check=False)
    record("diff_hygiene", diff_hygiene.returncode == 0, diff_hygiene.returncode)
    route = read_commit_json(head, f"{PREFIX}orchestration/terminal-route-state-final.json")
    record(
        "route_prepared_not_sent",
        route.get("state") == "PREPARED_NOT_SENT" and route.get("send_count") == 0 and route.get("successor_title") is None,
        {"state": route.get("state"), "send_count": route.get("send_count")},
    )
    truth = read_commit_json(head, f"{PREFIX}closeout/phase-truth.json")
    record("terminal_verdict", truth.get("terminal_verdict") == VERDICT, truth.get("terminal_verdict"))

    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    ahead_behind = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    ahead = int(ahead_behind[0])
    behind = int(ahead_behind[1])
    record("local_upstream_equality", head == upstream, upstream)
    record("local_tracking_equality", head == tracking, tracking)
    record("fresh_live_equality", head == live, live)
    record("typed_zero_divergence", ahead == 0 and behind == 0, {"ahead": ahead, "behind": behind})
    clean_after = not git_text("status", "--porcelain=v1")
    record("clean_after", clean_after, clean_after)

    passed = all(row["passed"] for row in checks)
    return {
        "schema": "ghc.family.sable.v664-v7.external-exclusive-canonical-receipt.v1",
        "owner": "Sable Rook",
        "phase": "v664-v7",
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": head,
        "invocation_policy": "one attributable exact-final canonical invocation; no replay after success",
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "test_count": test_count,
        "strict_json_count": json_count,
        "markdown_count": markdown_count,
        "python_compile_count": python_count,
        "owner_path_count": len(owner_paths),
        "privacy_candidate_count": len(privacy_candidates),
        "confirmed_privacy_hits": len(confirmed),
        "manifest_replays": [x1_manifest, evidence_manifest, owner_manifest, delta_manifest],
        "check_count": len(checks),
        "passed_check_count": sum(row["passed"] for row in checks),
        "checks": checks,
        "terminal_verdict": VERDICT,
        "valid": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_final):
        raise CanonicalError("expected final must be a full lowercase commit identifier")
    output = Path(args.output)
    if not output.is_absolute():
        raise CanonicalError("external receipt path must be absolute")
    if output.exists():
        raise CanonicalError("external receipt already exists; canonical replay refused")
    result = validate(args.expected_final)
    write_exclusive(output, result)
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "final": result["final"],
                "tests": result["test_count"],
                "checks": result["check_count"],
                "json": result["strict_json_count"],
                "owner_paths": result["owner_path_count"],
                "confirmed_privacy_hits": result["confirmed_privacy_hits"],
                "terminal_verdict": result["terminal_verdict"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
