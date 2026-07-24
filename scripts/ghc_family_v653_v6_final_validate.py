#!/usr/bin/env python3
"""One-pass exact-final canonical validator for Caelen Ash v653-v6."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v653_v6_detailed_validator as detailed
import ghc_family_v653_v6_minimal_validator as minimal
from ghc_family_v653_v6_validation_common import (
    PHASE,
    REPO,
    batch_blob_bytes,
    phase_public_paths,
    read_json,
    revision_blob_map,
    scan_privacy_paths,
)


SOURCE = "8cfda9ac9ac86d186346b473795e7bfb045effa0"
X1 = "5be148f1171a449550ce73dd524cb866db7632e3"
EVIDENCE = "17dc9cc858ec2366d25b4b85b8bf85f3f792c8db"
TEST_SELECTIONS = {
    "current_caelen": [
        "tests.test_ghc_family_v653_v6_core",
        "tests.test_ghc_family_v653_v6_validation",
        "tests.test_ghc_family_v653_v6_closeout",
    ],
    "recent_sable": [
        "tests.test_ghc_family_v653_v5_core",
        "tests.test_ghc_family_v653_v5_validation",
        "tests.test_ghc_family_v653_v5_closeout",
    ],
    "inherited_auren": [
        "tests.test_ghc_family_v653_v4_core",
        "tests.test_ghc_family_v653_v4_validation",
        "tests.test_ghc_family_v653_v4_closeout",
    ],
    "successor_orin": [
        "tests.test_ghc_family_v652_v2",
        "tests.test_ghc_family_v652_v2_closeout",
    ],
}
TEST_EXCLUSIONS = {
    (
        "tests.test_ghc_family_v653_v5_closeout."
        "V653V4CloseoutTests.test_anchor_history_and_commit_cap"
    ): (
        "Sable lifecycle-local HEAD distance assertion; Caelen validates "
        "source, x1, evidence, final ancestry and commit cap separately."
    ),
    (
        "tests.test_ghc_family_v653_v4_closeout."
        "V653V4CloseoutTests.test_anchor_history_and_commit_cap"
    ): (
        "Auren lifecycle-local HEAD distance assertion; Caelen validates "
        "source, x1, evidence, final ancestry and commit cap separately."
    ),
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


def module_test_ids(module: str) -> list[str]:
    path = REPO / (module.replace(".", "/") + ".py")
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return sorted(
        f"{module}.{node.name}.{child.name}"
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
        and child.name.startswith("test")
    )


def selection_result(name: str) -> dict[str, Any]:
    modules = TEST_SELECTIONS[name]
    discovered = [
        test_id
        for module in modules
        for test_id in module_test_ids(module)
    ]
    exclusions = [
        {"test_id": test_id, "reason": reason}
        for test_id, reason in TEST_EXCLUSIONS.items()
        if test_id in discovered
    ]
    excluded_ids = {row["test_id"] for row in exclusions}
    eligible = [test_id for test_id in discovered if test_id not in excluded_ids]
    result = run(
        [sys.executable, "-m", "unittest", "-q", *eligible],
        check=False,
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "selection": name,
        "modules": modules,
        "discovered_count": len(discovered),
        "eligible_count": len(eligible),
        "explicit_lifecycle_exclusions": exclusions,
        "tests_run": int(match.group(1)) if match else 0,
        "failures": len(re.findall(r"^FAIL:", output, flags=re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, flags=re.MULTILINE)),
        "exit_code": result.returncode,
        "valid": (
            result.returncode == 0
            and match is not None
            and int(match.group(1)) == len(eligible)
        ),
    }


def test_result() -> dict[str, Any]:
    selections = {
        name: selection_result(name) for name in TEST_SELECTIONS
    }
    return {
        "selection_count": len(selections),
        "tests_run": sum(row["tests_run"] for row in selections.values()),
        "failures": sum(row["failures"] for row in selections.values()),
        "errors": sum(row["errors"] for row in selections.values()),
        "valid": all(row["valid"] for row in selections.values()),
        "selections": selections,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren-only inherited policy",
    }


def manifest_issues(
    manifest: dict[str, Any], actual_paths: set[str], *, head: str
) -> list[str]:
    exclusions = set(manifest["self_exclusions"])
    entry_paths = {row["path"] for row in manifest["entries"]}
    issues: list[str] = []
    if entry_paths != actual_paths - exclusions:
        issues.append("path_coverage")
    committed_blobs = revision_blob_map([row["path"] for row in manifest["entries"]])
    payloads = batch_blob_bytes(committed_blobs.values())
    for row in manifest["entries"]:
        path = row["path"]
        if committed_blobs[path] != row["git_blob"]:
            issues.append(f"blob:{path}")
        if "sha256" in row:
            digest = hashlib.sha256(payloads[committed_blobs[path]]).hexdigest()
            if digest != row["sha256"]:
                issues.append(f"sha256:{path}")
    return issues


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
            parse_failures.append(
                {
                    "path": path.relative_to(REPO).as_posix(),
                    "error": type(exc).__name__,
                }
            )
    privacy = scan_privacy_paths(phase_public_paths())

    owner_manifest = read_json(PHASE / "validation/final-owner-manifest.json")
    actual_paths = {
        path.relative_to(REPO).as_posix() for path in phase_public_paths()
    }
    owner_issues = manifest_issues(owner_manifest, actual_paths, head=head)

    final_review = read_json(PHASE / "validation/final-staged-review.json")
    final_manifest = read_json(PHASE / "validation/final-staged-manifest.json")
    final_delta_paths = {
        path
        for path in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).splitlines()
        if path
    }
    final_manifest_issues = manifest_issues(
        final_manifest, final_delta_paths, head=head
    )
    delta_name_hash = hashlib.sha256(
        ("\n".join(sorted(final_delta_paths)) + "\n").encode("utf-8")
    ).hexdigest()
    if delta_name_hash != final_manifest["exact_staged_names_sha256"]:
        final_manifest_issues.append("exact_staged_names_sha256")

    stale_tokens = (
        "PENDING_EVIDENCE_COMMIT",
        "PENDING_X1_COMMIT",
        "PENDING_FINAL_COMMIT",
        "<FINAL_COMMIT>",
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
        ancestry[name] = (
            run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                check=False,
            ).returncode
            == 0
        )
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    phase_merges = int(
        git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD")
    )
    parents = git("rev-list", "--parents", f"{SOURCE}..HEAD").splitlines()
    all_single_parent = all(len(row.split()) == 2 for row in parents)
    final_parent = git("rev-parse", "HEAD^")
    diff_hygiene = git("diff-tree", "--check", "HEAD^", "HEAD") == ""
    clean_after = git("status", "--porcelain=v1") == ""
    route = read_json(PHASE / "orchestration/terminal-route-state.json")
    negatives = read_json(PHASE / "retained-negative-register-final.json")
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    truth = read_json(PHASE / "phase-truth.json")

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
        "local_upstream_tracking_live_equal": head
        == upstream
        == tracking
        == live,
        "zero_divergence": divergence.replace("\t", " ") == "0 0",
        "clean_before": clean_before,
        "clean_after": clean_after,
        "diff_hygiene": diff_hygiene,
        "final_staged_review": final_review["valid"],
        "final_staged_manifest": not final_manifest_issues,
        "owner_manifest": not owner_issues,
        "stale_labels": not stale_hits,
        "json": not parse_failures,
        "privacy": privacy["valid"],
        "negative_accounting": negatives["effective_total"] == 10279
        and negatives["none_erased"],
        "gate_accounting": gates["effective_open_gaps"] == 75
        and gates["effective_exact_gates"] == 76
        and gates["none_silently_closed"],
        "outcome_truth": truth["outcomes"]
        == {
            "completed": 23,
            "represented": 5,
            "open_gap": 1,
            "exact_gate": 1,
        },
        "route_prepared_for_authorized_orin_activation": route["state"]
        == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
        and route["successor_authorized"]
        and route["successor_title"] == "Orin Thale"
        and route["successor_phase"] == "v653-v7"
        and not route["post_gate_unique_resolution_completed"]
        and not route["post_gate_task_reread"]
        and not route["activation_sent"]
        and route["send_count"] == 0
        and route["create_or_fork_count"] == 0
        and not route["task_created"]
        and not route["task_forked"]
        and not route["delegation_used"]
        and not route["collaboration_subagent_spawned"]
        and route["current_task_created_by_sable_rook"]
        and route["current_task_creation_tool_acknowledged_exactly_one_creation"],
    }
    valid = (
        tests["valid"]
        and detailed_result["valid"]
        and minimal_result["valid"]
        and all(lifecycle_checks.values())
    )
    return {
        "schema": "ghc.family.v653-v6.exact-final-validation.v1",
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
        "owner_manifest_issues": owner_issues,
        "final_staged_manifest_entry_count": final_manifest["entry_count"],
        "final_staged_manifest_issues": final_manifest_issues,
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
        "boundary": (
            "One attributable exact-final canonical pass. Do not replay after "
            "success."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", choices=sorted(TEST_SELECTIONS))
    parser.add_argument("--expected-head")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.selection:
        result = selection_result(args.selection)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        if not result["valid"]:
            raise SystemExit(1)
        return
    if not args.expected_head or args.receipt is None:
        parser.error("--expected-head and --receipt are required")
    result = validate(args.expected_head)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
