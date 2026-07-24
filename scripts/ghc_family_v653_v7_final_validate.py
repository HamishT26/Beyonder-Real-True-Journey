#!/usr/bin/env python3
"""Run Orin Thale's one coherent exact-final v653-v7 validation pass."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v653_v7_detailed_validator as detailed
import ghc_family_v653_v7_minimal_validator as minimal
from ghc_family_v653_v7_validation_common import (
    PHASE,
    REPO,
    batch_blob_bytes,
    phase_public_paths,
    read_json,
    revision_blob_map,
    scan_privacy_paths,
    sha256_bytes,
)


SOURCE = "c044464ed940093d59a59686efd4faa61853f341"
X1 = "78ece91db153275ca2857899ee125dc0673c0154"
EVIDENCE = "888df289dd58f5717919ac1ee2c8083cd93cddfe"
CLOSEOUT = "cceb53e1bc5ad0c5e9b4a01cc3eac42f3a360b8b"
FIRST_CORRECTION = "e94f2f3c048678b6d7c87c6d4037dc8b24787c4a"
SECOND_CORRECTION = "0eb92e13d6105345635e4f9cf87626b0b2462995"
EXPECTED_BRANCH = "codex/GHC-Family/orin-thale-v653-v7-full-tools"
TEST_SELECTIONS = {
    "current_orin": [
        "tests.test_ghc_family_v653_v7_core",
        "tests.test_ghc_family_v653_v7_validation",
        "tests.test_ghc_family_v653_v7_closeout",
    ],
    "recent_caelen": [
        "tests.test_ghc_family_v653_v6_core",
        "tests.test_ghc_family_v653_v6_validation",
        "tests.test_ghc_family_v653_v6_closeout",
    ],
    "inherited_sable": [
        "tests.test_ghc_family_v653_v5_core",
        "tests.test_ghc_family_v653_v5_validation",
        "tests.test_ghc_family_v653_v5_closeout",
    ],
    "successor_compatibility": [
        "tests.test_ghc_family_v653_v7_x1",
    ],
}
TEST_EXCLUSIONS = {
    (
        "tests.test_ghc_family_v653_v6_closeout."
        "V653V6CloseoutTests.test_anchor_history_and_commit_cap"
    ): (
        "Caelen lifecycle-local HEAD distance assertion; Orin validates "
        "Caelen final, Orin x1, evidence, final ancestry and commit cap separately."
    ),
    (
        "tests.test_ghc_family_v653_v5_closeout."
        "V653V4CloseoutTests.test_anchor_history_and_commit_cap"
    ): (
        "Sable lifecycle-local HEAD distance assertion; Orin validates "
        "source, x1, evidence, final ancestry and commit cap separately."
    ),
    (
        "tests.test_ghc_family_v653_v7_x1."
        "V653V7X1Tests.test_no_x2_output_files"
    ): (
        "Orin x1 tree-local absence assertion; its immutable x1 commit and "
        "manifest passed before x2, while the final tree must contain x2 output."
    ),
}


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
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
    tree = ast.parse(
        path.read_text(encoding="utf-8-sig"), filename=str(path)
    )
    return sorted(
        f"{module}.{node.name}.{child.name}"
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
        and child.name.startswith("test")
    )


def selection_result(name: str) -> dict[str, Any]:
    discovered = [
        test_id
        for module in TEST_SELECTIONS[name]
        for test_id in module_test_ids(module)
    ]
    excluded = [
        {"test_id": test_id, "reason": TEST_EXCLUSIONS[test_id]}
        for test_id in discovered
        if test_id in TEST_EXCLUSIONS
    ]
    eligible = [row for row in discovered if row not in TEST_EXCLUSIONS]
    result = run(
        [sys.executable, "-m", "unittest", "-q", *eligible],
        check=False,
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "group": name,
        "discovered": len(discovered),
        "eligible": len(eligible),
        "excluded": excluded,
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


def manifest_result(relative: str) -> dict[str, Any]:
    manifest = read_json(PHASE / relative)
    paths = [entry["path"] for entry in manifest["entries"]]
    blobs = revision_blob_map(paths, "HEAD")
    payloads = batch_blob_bytes(blobs.values())
    issues = []
    for entry in manifest["entries"]:
        observed_blob = blobs[entry["path"]]
        payload = payloads[observed_blob]
        if (
            observed_blob != entry["git_blob"]
            or len(payload) != entry["bytes"]
            or sha256_bytes(payload) != entry["sha256"]
        ):
            issues.append(entry["path"])
    return {
        "manifest": relative,
        "entry_count": len(paths),
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
    }


def exact_head_checks(head: str) -> dict[str, bool]:
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_count = int(
        git("rev-list", "--count", "--merges", f"{SOURCE}..{head}")
    )
    parent_count = len(git("show", "-s", "--format=%P", head).split())
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git(
        "rev-parse",
        "refs/remotes/origin/codex/GHC-Family/orin-thale-v653-v7-full-tools",
    )
    live_row = git(
        "ls-remote",
        "--heads",
        "origin",
        "refs/heads/codex/GHC-Family/orin-thale-v653-v7-full-tools",
    )
    live = live_row.split("\t", 1)[0] if live_row else ""
    return {
        "source_ancestral": run(
            ["git", "merge-base", "--is-ancestor", SOURCE, head],
            check=False,
        ).returncode
        == 0,
        "x1_ancestral": run(
            ["git", "merge-base", "--is-ancestor", X1, head],
            check=False,
        ).returncode
        == 0,
        "evidence_ancestral": run(
            ["git", "merge-base", "--is-ancestor", EVIDENCE, head],
            check=False,
        ).returncode
        == 0,
        "closeout_ancestral": run(
            ["git", "merge-base", "--is-ancestor", CLOSEOUT, head],
            check=False,
        ).returncode
        == 0,
        "first_correction_ancestral": run(
            ["git", "merge-base", "--is-ancestor", FIRST_CORRECTION, head],
            check=False,
        ).returncode
        == 0,
        "second_correction_ancestral": run(
            ["git", "merge-base", "--is-ancestor", SECOND_CORRECTION, head],
            check=False,
        ).returncode
        == 0,
        "six_phase_commits": phase_commits == 6,
        "within_eight_commit_cap": phase_commits <= 8,
        "zero_merges": merge_count == 0,
        "one_final_parent": parent_count == 1,
        "final_direct_child_of_second_correction": git(
            "rev-parse", f"{head}^"
        )
        == SECOND_CORRECTION,
        "expected_branch": branch == EXPECTED_BRANCH,
        "exact_head_stable": git("rev-parse", "HEAD") == head,
        "clean": git("status", "--porcelain=v1") == "",
        "local_upstream_equal": upstream == head,
        "local_tracking_equal": tracking == head,
        "local_fresh_live_equal": live == head,
        "zero_divergence": git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        == "0\t0",
        "diff_hygiene": run(
            ["git", "diff", "--check", f"{head}^", head],
            check=False,
        ).returncode
        == 0,
    }


def validate() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    if git("status", "--porcelain=v1"):
        raise RuntimeError("exact-final canonical pass requires a clean tree")
    groups = [
        selection_result(name) for name in TEST_SELECTIONS
    ]
    detailed_result = detailed.validate()
    minimal_result = minimal.validate()
    json_paths = sorted(PHASE.rglob("*.json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_failures.append(
                {
                    "path": path.relative_to(REPO).as_posix(),
                    "error": type(exc).__name__,
                }
            )
    privacy = scan_privacy_paths(phase_public_paths())
    manifests = [
        manifest_result("validation/x1-staged-manifest.json"),
        manifest_result("validation/evidence-candidate-manifest.json"),
        manifest_result("validation/final-staged-manifest.json"),
        manifest_result("validation/final-owner-manifest.json"),
    ]
    route = read_json(PHASE / "orchestration/terminal-route-state.json")
    stale = read_json(PHASE / "validation/stale-label-review.json")
    lifecycle = exact_head_checks(head)
    route_valid = (
        route["state"] == "STOP_AFTER_TRUTHFUL_CLOSEOUT"
        and not route["downstream_authorized"]
        and route["successor_title"] is None
        and not route["task_created"]
        and not route["task_forked"]
        and not route["delegation_used"]
        and not route["collaboration_subagent_spawned"]
        and not route["standby_contacted"]
        and not route["activation_sent"]
        and route["send_count"] == 0
    )
    valid = (
        all(group["valid"] for group in groups)
        and detailed_result["valid"]
        and minimal_result["valid"]
        and not json_failures
        and privacy["valid"]
        and all(row["valid"] for row in manifests)
        and all(lifecycle.values())
        and stale["valid"]
        and route_valid
    )
    return {
        "schema": "ghc.family.v653-v7.exact-final-validation.v1",
        "exact_head": head,
        "test_groups": groups,
        "eligible_test_count": sum(row["eligible"] for row in groups),
        "tests_run": sum(row["tests_run"] for row in groups),
        "detailed_checks": detailed_result["check_count"],
        "detailed_passed": detailed_result["passed_count"],
        "minimal_checks": minimal_result["check_count"],
        "minimal_passed": minimal_result["passed_count"],
        "json_parse_count": len(json_paths),
        "json_failures": json_failures,
        "privacy": privacy,
        "manifests": manifests,
        "lifecycle": lifecycle,
        "route_valid": route_valid,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren-only inherited policy",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "successful_replay_permitted": False,
        "valid": valid,
        "boundary": (
            "One coherent canonical exact-final pass only; bounded same-owner "
            "evidence, not independent reproduction or external authority."
        ),
    }


def main() -> None:
    result = validate()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
