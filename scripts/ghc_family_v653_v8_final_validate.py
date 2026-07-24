#!/usr/bin/env python3
"""Run Liora Venn's one coherent exact-final v653-v8 validation pass."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v653_v8_detailed_validator as detailed
import ghc_family_v653_v8_minimal_validator as minimal
from ghc_family_v653_v8_validation_common import (
    PHASE,
    REPO,
    batch_blob_bytes,
    phase_public_paths,
    read_json,
    revision_blob_map,
    scan_privacy_paths,
    sha256_bytes,
)


SOURCE = "144a4d51195d777ea2b8068bb4cf7ed82fff21be"
X1 = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"
EVIDENCE = "67e51031ed4be4bb64962635e79c459b8a01e7d4"
EXPECTED_BRANCH = "codex/GHC-Family/liora-venn-v653-v8-full-tools"
TEST_SELECTIONS = {
    "current_liora": [
        "tests.test_ghc_family_v653_v8_core",
        "tests.test_ghc_family_v653_v8_validation",
        "tests.test_ghc_family_v653_v8_closeout",
    ],
    "recent_orin": [
        "tests.test_ghc_family_v653_v7_core",
        "tests.test_ghc_family_v653_v7_validation",
        "tests.test_ghc_family_v653_v7_closeout",
    ],
    "inherited_sable": [
        "tests.test_ghc_family_v653_v5_core",
        "tests.test_ghc_family_v653_v5_validation",
        "tests.test_ghc_family_v653_v5_closeout",
    ],
    "successor_compatibility": [
        "tests.test_ghc_family_v653_v8_x1",
    ],
}
TEST_EXCLUSIONS = {
    (
        "tests.test_ghc_family_v653_v5_closeout."
        "V653V4CloseoutTests.test_anchor_history_and_commit_cap"
    ): (
        "Sable lifecycle-local HEAD distance assertion; Liora validates source, "
        "x1, evidence, final ancestry and commit cap separately."
    ),
    (
        "tests.test_ghc_family_v653_v8_x1."
        "V653V8X1Tests.test_no_x2_output_files"
    ): (
        "Liora x1 tree-local absence assertion; its immutable x1 commit and "
        "manifest passed before x2, while the final tree must contain x2 output."
    ),
}


def run(
    args: list[str],
    *,
    check: bool = True,
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
        "failures": len(
            re.findall(r"^FAIL:", output, flags=re.MULTILINE)
        ),
        "errors": len(
            re.findall(r"^ERROR:", output, flags=re.MULTILINE)
        ),
        "exit_code": result.returncode,
        "valid": (
            result.returncode == 0
            and match is not None
            and int(match.group(1)) == len(eligible)
        ),
        "output_tail": "\n".join(output.strip().splitlines()[-8:]),
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
        "refs/remotes/origin/codex/GHC-Family/liora-venn-v653-v8-full-tools",
    )
    live_row = git(
        "ls-remote",
        "--heads",
        "origin",
        "refs/heads/codex/GHC-Family/liora-venn-v653-v8-full-tools",
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
        "three_phase_commits": phase_commits == 3,
        "within_eight_commit_cap": phase_commits <= 8,
        "zero_merges": merge_count == 0,
        "one_final_parent": parent_count == 1,
        "final_direct_child_of_evidence": git("rev-parse", f"{head}^")
        == EVIDENCE,
        "expected_branch": branch == EXPECTED_BRANCH,
        "exact_head_stable": git("rev-parse", "HEAD") == head,
        "clean": git("status", "--porcelain=v1") == "",
        "local_upstream_equal": upstream == head,
        "local_tracking_equal": tracking == head,
        "local_fresh_live_equal": live == head,
        "zero_divergence": git(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        )
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
    delivery = read_json(PHASE / "handoff/delivery-state.json")
    stale = read_json(PHASE / "validation/stale-label-review.json")
    final_truth = read_json(PHASE / "final/phase-truth.json")
    build_receipt = read_json(PHASE / "validation/final-build-receipt.json")
    lifecycle = exact_head_checks(head)
    route_valid = (
        route["state"] == "PREPARED_NOT_SENT"
        and not route["terminal_gate_satisfied"]
        and route["successor_title"] == "Tamar Vey"
        and route["successor_phase"] == "v654-v1"
        and not route["task_created"]
        and not route["task_forked"]
        and not route["delegation_used"]
        and not route["collaboration_subagent_spawned"]
        and not route["standby_contacted"]
        and not route["activation_sent"]
        and route["send_count"] == 0
        and delivery["state"] == "PREPARED_NOT_SENT"
        and not delivery["sent"]
        and delivery["send_count"] == 0
        and delivery["target_title"] == "Tamar Vey"
    )
    truth_valid = (
        final_truth["outcomes"]
        == {
            "completed": 23,
            "represented": 5,
            "open_gap": 1,
            "exact_gate": 1,
        }
        and final_truth["effective_negatives"] == 10609
        and final_truth["effective_open_gaps"] == 77
        and final_truth["effective_exact_gates"] == 78
        and final_truth["real_data_rows"] == 0
        and not final_truth["independent_reproduction"]
        and final_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        and not final_truth["complete_repository_suite_run"]
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
        and build_receipt["valid"]
        and truth_valid
        and route_valid
    )
    return {
        "schema": "ghc.family.v653-v8.exact-final-validation.v1",
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
        "truth_valid": truth_valid,
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = validate()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
