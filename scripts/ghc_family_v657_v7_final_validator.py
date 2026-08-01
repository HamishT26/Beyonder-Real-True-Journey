#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Liora Venn v657-v7."""

from __future__ import annotations

import argparse
import importlib
import io
import json
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_ghc_family_v657_v7_evidence_receipts as e
import ghc_family_v657_v7_closeout_config as c
import ghc_family_v657_v7_detailed_validator as detailed
import ghc_family_v657_v7_minimal_validator as minimal
import ghc_family_v657_v7_phase_data as d
import ghc_family_v657_v7_scoped_test_runner as scoped


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
BRANCH = c.BRANCH


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


def tree_map(commit: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for line in git("ls-tree", "-r", commit).splitlines():
        metadata, path = line.split("\t", 1)
        _, kind, oid = metadata.split()
        if kind == "blob":
            mapping[path] = oid
    return mapping


def replay_manifest(relative: str, commit: str, tree: dict[str, str]) -> dict[str, Any]:
    manifest = load(relative)
    mismatches = []
    for entry in manifest["entries"]:
        observed = tree.get(entry["path"])
        if observed != entry["git_blob"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed,
                }
            )
    return {
        "path": f"{d.PHASE_ROOT}/{relative}",
        "commit": commit,
        "entry_count": manifest["entry_count"],
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path for path in (ROOT / "scripts").glob("*v657_v7*.py") if path.is_file()
    )
    paths.extend(ROOT / relative for relative in e.wrapper_paths())
    paths.extend(
        path
        for path in (ROOT / "tests").glob("test_ghc_family_v657_v7*.py")
        if path.is_file()
    )
    return sorted({path.resolve() for path in paths})


def lifecycle_tests() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    module = importlib.import_module("tests.test_ghc_family_v657_v7_closeout")
    suite = unittest.TestLoader().loadTestsFromModule(module)
    expected = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "tests_run": result.testsRun,
        "expected_tests": expected,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failed_test_ids": [case.id() for case, _ in result.failures],
        "error_test_ids": [case.id() for case, _ in result.errors],
        "valid": result.wasSuccessful()
        and result.testsRun == expected
        and not result.skipped,
        "runner_output": stream.getvalue(),
    }


def validate(output: Path) -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    before_status = git("status", "--porcelain=v1", "--untracked-files=normal")
    branch = git("symbolic-ref", "--short", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_lines = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_lines[0].split()[0] if len(live_lines) == 1 else None
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")

    scoped_tests = scoped.run_scope()
    closeout_tests = lifecycle_tests()
    tests = {
        "scoped": scoped_tests,
        "closeout": closeout_tests,
        "tests_run": scoped_tests["tests_run"] + closeout_tests["tests_run"],
        "expected_tests": scoped_tests["expected_tests"]
        + closeout_tests["expected_tests"],
        "failures": scoped_tests["failures"] + closeout_tests["failures"],
        "errors": scoped_tests["errors"] + closeout_tests["errors"],
        "skipped": scoped_tests["skipped"] + closeout_tests["skipped"],
        "valid": scoped_tests["valid"] and closeout_tests["valid"],
    }
    detailed_result = detailed.validate()
    minimal_result = minimal.validate()

    json_paths = sorted(PHASE.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "error": type(exc).__name__,
                }
            )

    paths = owner_paths()
    privacy_hits = []
    for path in paths:
        privacy_hits.extend(
            e.scan_text(path.relative_to(ROOT).as_posix(), path.read_text(encoding="utf-8"))
        )

    documents = [
        path
        for path in PHASE.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    document_words = {
        path.relative_to(PHASE).as_posix(): len(path.read_text(encoding="utf-8").split())
        for path in documents
    }

    trees = {
        c.X1_COMMIT: tree_map(c.X1_COMMIT),
        c.EVIDENCE_COMMIT: tree_map(c.EVIDENCE_COMMIT),
        head: tree_map(head),
    }
    manifests = [
        replay_manifest(
            "validation/x1-content-manifest.json", c.X1_COMMIT, trees[c.X1_COMMIT]
        ),
        replay_manifest(
            "validation/evidence-content-manifest.json",
            c.EVIDENCE_COMMIT,
            trees[c.EVIDENCE_COMMIT],
        ),
        replay_manifest(
            "validation/closeout-content-manifest.json", head, trees[head]
        ),
    ]
    manifest_entries = sum(row["entry_count"] for row in manifests)

    phase_commits = [
        row
        for row in git("rev-list", "--reverse", f"{c.SOURCE_COMMIT}..{head}").splitlines()
        if row
    ]
    parent_counts = {
        commit: len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1
        for commit in phase_commits
    }
    merge_count = int(
        git("rev-list", "--count", "--merges", f"{c.SOURCE_COMMIT}..{head}")
    )
    ancestry = {
        name: run("git", "merge-base", "--is-ancestor", commit, head, check=False).returncode
        == 0
        for name, commit in {
            "source": c.SOURCE_COMMIT,
            "first_x1": c.FIRST_X1_COMMIT,
            "x1": c.X1_COMMIT,
            "evidence": c.EVIDENCE_COMMIT,
        }.items()
    }
    diff_hygiene = run("git", "diff", "--check", c.EVIDENCE_COMMIT, head, check=False)
    final_review = load("validation/closeout-staged-review.json")
    closeout_privacy = load("validation/closeout-privacy-scan.json")
    truth = load("truth/phase-truth-final-candidate.json")
    flow = load("method-flow/method-flow-state-final.json")
    route = load("orchestration/terminal-route-state.json")

    stale_tokens = [
        "".join(("PENDING", "_EVIDENCE", "_COMMIT")),
        "".join(("PENDING", "_CLOSEOUT", "_COMMIT")),
        "".join(("FINAL", "_COMMIT", "_PLACEHOLDER")),
    ]
    affirmative_sent_lines = {
        "".join(("SENT_BY_", "LIORA_VENN", " = true")),
        "".join(("SENT_BY_", "TAMAR_VEY", " = true")),
    }
    stale_hits = []
    for path in PHASE.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in stale_tokens:
            if token in text:
                stale_hits.append(
                    {"path": path.relative_to(ROOT).as_posix(), "token": token}
                )
        if any(line.strip() in affirmative_sent_lines for line in text.splitlines()):
            stale_hits.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "token": "affirmative_sent_declaration",
                }
            )

    terminal_checks = {
        "head_direct_child_of_evidence": git("rev-parse", f"{head}^")
        == c.EVIDENCE_COMMIT,
        "source_to_final_commit_count_is_three": len(phase_commits) == 3,
        "first_x1_equals_x1_for_single_freeze": c.FIRST_X1_COMMIT
        == c.X1_COMMIT,
        "commit_cap_within_eight": len(phase_commits) <= 8,
        "all_phase_commits_single_parent": all(
            count == 1 for count in parent_counts.values()
        ),
        "zero_merges": merge_count == 0,
        "all_anchors_ancestral": all(ancestry.values()),
        "branch_exact": branch == BRANCH,
        "local_upstream_tracking_live_equal": len({head, upstream, tracking, live})
        == 1,
        "zero_divergence": divergence.split() == ["0", "0"],
        "clean_before": before_status == "",
        "tests_valid": tests["valid"],
        "detailed_valid": detailed_result["valid"],
        "minimal_valid": minimal_result["valid"],
        "json_valid": not json_issues,
        "privacy_zero_hits": not privacy_hits,
        "closeout_privacy_zero_hits": closeout_privacy["valid"]
        and closeout_privacy["hit_count"] == 0,
        "owner_file_cap": len(paths) < 2000,
        "document_word_cap": max(document_words.values()) <= 100000,
        "all_manifests_valid": all(row["valid"] for row in manifests),
        "closeout_staged_review_valid": final_review["valid"],
        "diff_hygiene": diff_hygiene.returncode == 0,
        "stale_label_review": not stale_hits,
        "truth_distribution": truth["outcome_counts"]
        == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "negative_total": truth["effective_negatives"]
        == c.EVIDENCE_EFFECTIVE_NEGATIVES + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES),
        "method_flow_total_and_parity": flow["counts"]["effective_methods"]
        == c.EVIDENCE_EFFECTIVE_METHODS + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES)
        and flow["counts"]["effective_witness_results"]
        == {
            "fail": c.EVIDENCE_EFFECTIVE_METHODS
            + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES),
            "pass": c.EVIDENCE_EFFECTIVE_METHODS
            + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES),
        },
        "open_gap_total": truth["effective_open_gaps"] == c.OPEN_GAPS,
        "exact_gate_total": truth["effective_exact_gates"] == c.EXACT_GATES,
        "terminal_verdict": truth["terminal_verdict"]
        == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": truth["independent_reproduction"] is False,
        "route_held_unresolved_not_sent": route["state"]
        == "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE"
        and route["message_sent"] is False,
        "route_exact_target_held_until_terminal_gate": route["next_exact_title"]
        == "Tamar Vey"
        and route["next_phase"] == "v657-v8",
        "tavian_standby": route["tavian_sol_state"] == "ON_STANDBY",
    }
    after_status = git("status", "--porcelain=v1", "--untracked-files=normal")
    terminal_checks["clean_after"] = after_status == ""
    valid = all(terminal_checks.values())
    payload = {
        "schema": "ghc.family.v657-v7.exact-final-canonical-validation.v1",
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "exact_final_head": head,
        "source_commit": c.SOURCE_COMMIT,
        "first_x1_commit": c.FIRST_X1_COMMIT,
        "x1_commit": c.X1_COMMIT,
        "evidence_commit": c.EVIDENCE_COMMIT,
        "branch": branch,
        "local_head": head,
        "upstream_head": upstream,
        "tracking_head": tracking,
        "fresh_live_head": live,
        "divergence": divergence,
        "phase_commits": phase_commits,
        "phase_commit_count": len(phase_commits),
        "parent_counts": parent_counts,
        "merge_count": merge_count,
        "ancestry": ancestry,
        "tests": tests,
        "detailed_check_count": detailed_result["check_count"],
        "detailed_issues": detailed_result["issues"],
        "minimal_check_count": minimal_result["check_count"],
        "json_parse_count": len(json_paths),
        "json_issues": json_issues,
        "privacy_file_count": len(paths),
        "privacy_pattern_class_count": len(e.PRIVACY_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "owner_file_count": len(paths),
        "document_count": len(documents),
        "maximum_document_words": max(document_words.values()),
        "manifest_replays": manifests,
        "manifest_entry_count": manifest_entries,
        "stale_label_hits": stale_hits,
        "diff_hygiene_returncode": diff_hygiene.returncode,
        "terminal_checks": terminal_checks,
        "terminal_check_count": len(terminal_checks),
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state_at_validation": "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE",
        "canonical_pass_number": 1,
        "replay_after_success_permitted": False,
        "full_repository_suite_run": False,
        "boundary": "One exact-final same-owner canonical aggregate under shared infrastructure; not independent reproduction or external authority.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        raise SystemExit("canonical receipt output must be an absolute external path")
    payload = validate(output)
    summary = {
        "valid": payload["valid"],
        "exact_final_head": payload["exact_final_head"],
        "tests_run": payload["tests"]["tests_run"],
        "detailed_checks": payload["detailed_check_count"],
        "minimal_checks": payload["minimal_check_count"],
        "json_parses": payload["json_parse_count"],
        "privacy_files": payload["privacy_file_count"],
        "privacy_hits": len(payload["privacy_confirmed_hits"]),
        "manifest_entries": payload["manifest_entry_count"],
        "terminal_checks": payload["terminal_check_count"],
    }
    print(json.dumps(summary, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
