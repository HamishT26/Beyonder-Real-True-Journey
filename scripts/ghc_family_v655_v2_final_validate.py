#!/usr/bin/env python3
"""Run the one exact-final canonical validation for Lyren v655-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v655_v2_validate as phase_validator


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/lyren-moss/v655-v2"
BRANCH = "codex/GHC-Family/lyren-moss-v655-v2-full-tools"
SOURCE = "e1534547a8e6b053e90bbb1eed0966402ef03908"
X1_FREEZE = "848c28330b9b5d70eb5c8e716bcd9e300c512789"
X1_FINAL = X1_FREEZE
EVIDENCE = "786368c1879df9c1dfd00bae50a657d1e96c7c83"
CORRECTION = EVIDENCE
CURRENT_MODULES = [
    "tests.test_ghc_family_v655_v2_x1",
    "tests.test_ghc_family_v655_v2_core",
    "tests.test_ghc_family_v655_v2_validation",
    "tests.test_ghc_family_v655_v2_closeout",
]
INHERITED_TESTS: list[str] = []
FINAL_CODE_PATHS = [
    "scripts/build_ghc_family_v655_v2_closeout.py",
    "scripts/ghc_family_v655_v2_final_staged_review.py",
    "scripts/ghc_family_v655_v2_final_validate.py",
    "tests/test_ghc_family_v655_v2_closeout.py",
]
SCANNERS = {
    "scripts/ghc_family_v655_v2_final_staged_review.py",
    "scripts/ghc_family_v655_v2_final_validate.py",
}


def run(
    args: list[str], *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return subprocess.run(
        args,
        cwd=REPO,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def git(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def clean_state() -> dict[str, Any]:
    working = [
        row for row in git("diff", "--name-only").splitlines() if row
    ]
    index = [
        row for row in git("diff", "--cached", "--name-only").splitlines() if row
    ]
    untracked = [
        row
        for row in git("ls-files", "--others", "--exclude-standard").splitlines()
        if row
    ]
    return {
        "working_tree_paths": working,
        "index_paths": index,
        "untracked_paths": untracked,
        "valid": not working and not index and not untracked,
    }


def test_result() -> dict[str, Any]:
    result = run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-q",
            *CURRENT_MODULES,
        ],
        check=False,
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "tests_run": int(match.group(1)) if match else 0,
        "failures": len(re.findall(r"^FAIL:", output, re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, re.MULTILINE)),
        "exit_code": result.returncode,
        "valid": result.returncode == 0 and match is not None,
        "full_repository_suite_run": False,
        "bounded_inherited_test_count": len(INHERITED_TESTS),
    }


def all_phase_json() -> tuple[int, list[dict[str, str]]]:
    failures = []
    paths = sorted(PHASE.rglob("*.json"))
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(
                {
                    "path": path.relative_to(REPO).as_posix(),
                    "error": type(exc).__name__,
                }
            )
    return len(paths), failures


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_value": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private_callable_identifier)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
        "session_stream_payload": re.compile(
            r"(?:conversation[_ -]?transcript|session[_ -]?stream)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
    }
    paths = [
        path
        for path in sorted(PHASE.rglob("*"))
        if path.is_file()
        and path.suffix.lower()
        in {".py", ".json", ".md", ".txt", ".html", ".yaml", ".yml"}
    ]
    paths.extend(REPO / relative for relative in FINAL_CODE_PATHS)
    candidates = []
    for path in paths:
        relative = path.relative_to(REPO).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": relative, "class": label})
    confirmed = [row for row in candidates if row["path"] not in SCANNERS]
    return {
        "file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def verify_owner_manifest() -> dict[str, Any]:
    manifest = json.loads(
        (PHASE / "validation/final-owner-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    exclusions = set(manifest["self_exclusions"])
    actual = {
        path.relative_to(REPO).as_posix()
        for path in PHASE.rglob("*")
        if path.is_file()
    }
    manifest_paths = {row["path"] for row in manifest["entries"]}
    issues = []
    if manifest_paths != actual - exclusions:
        issues.append("path_coverage")
    for row in manifest["entries"]:
        try:
            actual_blob = git("rev-parse", f"HEAD:{row['path']}")
            content = git_bytes("show", f"HEAD:{row['path']}")
        except subprocess.CalledProcessError:
            actual_blob = "missing"
            content = b""
        if actual_blob != row["git_blob"]:
            issues.append(f"blob:{row['path']}")
        if len(content) != row["bytes"]:
            issues.append(f"bytes:{row['path']}")
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            issues.append(f"sha256:{row['path']}")
    return {
        "entry_count": manifest["entry_count"],
        "issues": issues,
        "valid": not issues,
    }


def verify_staged_manifest() -> dict[str, Any]:
    manifest = json.loads(
        (PHASE / "validation/final-staged-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    exclusions = set(manifest["self_exclusions"])
    delta = {
        row
        for row in git("diff", "--name-only", f"{CORRECTION}..HEAD").splitlines()
        if row
    }
    manifest_paths = {row["path"] for row in manifest["entries"]}
    issues = []
    if manifest_paths != delta - exclusions:
        issues.append("delta_coverage")
    for row in manifest["entries"]:
        if git("rev-parse", f"HEAD:{row['path']}") != row["git_blob"]:
            issues.append(f"blob:{row['path']}")
        content = git_bytes("show", f"HEAD:{row['path']}")
        if len(content) != row["bytes"]:
            issues.append(f"bytes:{row['path']}")
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            issues.append(f"sha256:{row['path']}")
    names_hash = hashlib.sha256(
        ("\n".join(sorted(delta)) + "\n").encode("utf-8")
    ).hexdigest()
    if names_hash != manifest["exact_staged_names_sha256"]:
        issues.append("names_hash")
    return {
        "entry_count": manifest["entry_count"],
        "issues": issues,
        "valid": not issues,
    }


def validate(expected_head: str) -> dict[str, Any]:
    clean_before = clean_state()
    head = git("rev-parse", "HEAD")
    tests = test_result()
    detailed = phase_validator.validate(
        "final", "detailed", "validation/final-owner-manifest.json"
    )
    minimal = phase_validator.validate(
        "final", "minimal", "validation/final-owner-manifest.json"
    )
    json_count, json_failures = all_phase_json()
    privacy = privacy_scan()
    owner_manifest = verify_owner_manifest()
    staged_manifest = verify_staged_manifest()
    final_review = json.loads(
        (PHASE / "validation/final-staged-review.json").read_text(
            encoding="utf-8"
        )
    )
    route = json.loads(
        (PHASE / "orchestration/terminal-route-state.json").read_text(
            encoding="utf-8"
        )
    )
    final_truth = json.loads(
        (PHASE / "truth/retained-negative-register-final.json").read_text(
            encoding="utf-8"
        )
    )
    baton = (
        PHASE / "handoffs/ilyra-fen-v655-v3-activation.md"
    ).read_text(encoding="utf-8")
    stale_tokens = (
        "PENDING_EVIDENCE_COMMIT",
        "PENDING_X1_COMMIT",
        "PENDING_FINAL_COMMIT",
        "<FINAL_COMMIT>",
        "0000000000000000000000000000000000000000",
    )
    stale_hits = []
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".yaml",
            ".yml",
        }:
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(token in text for token in stale_tokens):
                stale_hits.append(path.relative_to(REPO).as_posix())

    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_row.split("\t", 1)[0] if live_row else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    anchors = {
        name: run(
            ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
            check=False,
        ).returncode
        == 0
        for name, anchor in (
            ("source", SOURCE),
            ("x1_freeze", X1_FREEZE),
            ("evidence", EVIDENCE),
        )
    }
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    phase_merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"))
    parent_rows = git("rev-list", "--parents", f"{SOURCE}..HEAD").splitlines()
    all_single_parent = all(len(row.split()) == 2 for row in parent_rows)
    direct_chain = {
        "x1_freeze_parent_source": git("rev-parse", f"{X1_FREEZE}^") == SOURCE,
        "evidence_parent_x1": git("rev-parse", f"{EVIDENCE}^") == X1_FREEZE,
        "final_parent_evidence": git("rev-parse", "HEAD^") == EVIDENCE,
    }
    diff_hygiene = (
        run(["git", "diff-tree", "--check", "HEAD^", "HEAD"], check=False).returncode
        == 0
    )
    clean_after = clean_state()
    lifecycle = {
        "expected_head": head == expected_head,
        "branch_exact": git("branch", "--show-current") == BRANCH,
        "all_anchors_ancestral": all(anchors.values()),
        "direct_chain": all(direct_chain.values()),
        "three_phase_commits": phase_commits == 3,
        "within_eight_commit_cap": phase_commits <= 8,
        "zero_merges": phase_merges == 0,
        "all_single_parent": all_single_parent,
        "local_upstream_tracking_live_equal": head
        == upstream
        == tracking
        == live,
        "zero_divergence": divergence.replace("\t", " ") == "0 0",
        "clean_before": clean_before["valid"],
        "clean_after": clean_after["valid"],
        "diff_hygiene": diff_hygiene,
        "owner_manifest": owner_manifest["valid"],
        "staged_manifest": staged_manifest["valid"],
        "final_staged_review": final_review["valid"],
        "json": not json_failures,
        "privacy": privacy["valid"],
        "stale_labels": not stale_hits,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT"
        and route["successor_exact_title"] == "Ilyra Fen"
        and route["successor_phase"] == "v655-v3"
        and route["message_sent"] is False
        and route["hamish_successor_authorization"] is True
        and route["authorization_class"]
        == "authorized_with_terminal_conditions"
        and route["task_lookup_performed"] is False
        and route["blocker"] == "TERMINAL_GATE_PENDING",
        "final_negative_truth": (
            final_truth["effective_at_evidence"] == 12553
            and final_truth["final_operational_count"]
            == len(final_truth["final_operational"])
            and final_truth["effective_at_final_candidate"]
            == 12553 + final_truth["final_operational_count"]
            and final_truth["no_failure_erased"] is True
        ),
        "baton_word_bounds": 10_000 <= len(baton.split()) <= 100_000,
    }
    valid = (
        tests["valid"]
        and detailed["valid"]
        and minimal["valid"]
        and all(lifecycle.values())
    )
    return {
        "schema": "ghc.family.v655-v2.exact-final-validation.v1",
        "exact_final_head": head,
        "tests": tests,
        "detailed_check_count": detailed["check_count"],
        "detailed_passed_count": detailed["passed_count"],
        "minimal_check_count": minimal["check_count"],
        "minimal_passed_count": minimal["passed_count"],
        "json_parse_count": json_count,
        "json_parse_failures": json_failures,
        "privacy": privacy,
        "owner_manifest": owner_manifest,
        "final_staged_manifest": staged_manifest,
        "anchors": anchors,
        "direct_chain": direct_chain,
        "lifecycle_check_count": len(lifecycle),
        "lifecycle_checks": lifecycle,
        "phase_commit_count": phase_commits,
        "phase_merge_count": phase_merges,
        "stale_label_hits": stale_hits,
        "full_repository_suite_run": False,
        "canonical_pass_count": 1,
        "replay_after_success": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": (
            "One attributable exact-final canonical pass. Do not replay after success."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt.exists():
        raise RuntimeError("canonical receipt already exists; replay is forbidden")
    result = validate(args.expected_head)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "head": result["exact_final_head"],
                "tests": result["tests"]["tests_run"],
                "detailed": result["detailed_check_count"],
                "minimal": result["minimal_check_count"],
                "json": result["json_parse_count"],
                "privacy_files": result["privacy"]["file_count"],
                "privacy_hits": len(result["privacy"]["confirmed_hits"]),
                "owner_manifest": result["owner_manifest"]["entry_count"],
                "staged_manifest": result["final_staged_manifest"]["entry_count"],
                "lifecycle": result["lifecycle_check_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
