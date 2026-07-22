#!/usr/bin/env python3
"""One-pass exact-head canonical validator for Vesper Arlen v651-v7."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = "docs/vesper-arlen/v651-v7"
SOURCE = "2500d063583194b30f01da429196522baaac7300"
X1 = "d55689f393292cea76f8d568d69da27c8f7b3bd6"
EVIDENCE = "78f4014c7d10d59d05f95e872ece4d52027a7a7b"
SEAL = "12a767989aba8dc1a4c2f506561a95b1181d23a6"
BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-terminal-recovery"
OWNER_GLOBALS = {
    "scripts/build_ghc_family_v651_v7_preregistration.py",
    "scripts/build_ghc_family_v651_v7_evidence.py",
    "scripts/build_ghc_family_v651_v7_tools.py",
    "scripts/build_ghc_family_v651_v7_closeout.py",
    "scripts/build_ghc_family_v651_v7_terminal_correction.py",
    "scripts/ghc_family_v651_v7_runtime.py",
    "scripts/ghc_family_v651_v7_detailed_validator.py",
    "scripts/ghc_family_v651_v7_minimal_validator.py",
    "scripts/ghc_family_v651_v7_final_validator.py",
    "scripts/ghc_family_concurrency_reclamation.py",
    "scripts/ghc_family_conditional_update.py",
    "scripts/ghc_family_identity_accessibility_proxy.py",
    "scripts/ghc_family_integrity_range.py",
    "scripts/ghc_family_numerical_boundary.py",
    "scripts/ghc_family_schema_cache_concurrency.py",
    "scripts/ghc_family_stage20_authority_refusal.py",
    "scripts/ghc_family_storage_reclamation.py",
    "scripts/ghc_family_time_rate_fairness.py",
    "scripts/ghc_family_transaction_checkpoint.py",
    "tests/test_ghc_family_v651_v7_x1.py",
    "tests/test_ghc_family_v651_v7_x2.py",
    "tests/test_ghc_family_v651_v7_closeout.py",
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=REPO,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)


def load_at(commit: str, path: str) -> dict[str, Any]:
    return json.loads(blob(commit, path).decode("utf-8"))


def tree_map(commit: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    output = git("ls-tree", "-r", commit)
    for row in output.splitlines():
        meta, path = row.split("\t", 1)
        _mode, _kind, oid = meta.split()
        mapping[path] = oid
    return mapping


def verify_manifest(commit: str, relative: str) -> dict[str, Any]:
    payload = load_at(commit, relative)
    tree = tree_map(commit)
    mismatches: list[str] = []
    for row in payload["entries"]:
        path = row["path"]
        oid = tree.get(path)
        if oid != row["git_blob"]:
            mismatches.append(path)
            continue
        content = blob(commit, path)
        if len(content) != row["bytes"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
            mismatches.append(path)
    missing_exclusions = [path for path in payload["self_exclusions"] if path not in tree]
    return {
        "entry_count": payload["entry_count"],
        "self_exclusion_count": len(payload["self_exclusions"]),
        "mismatches": mismatches,
        "missing_exclusions": missing_exclusions,
        "valid": not mismatches and not missing_exclusions,
        "payload": payload,
    }


def run_tests() -> dict[str, Any]:
    names = [
        "tests.test_ghc_family_v651_v7_x1",
        "tests.test_ghc_family_v651_v7_x2",
        "tests.test_ghc_family_v651_v7_closeout",
    ]
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
    }


def validate(expected_head: str) -> dict[str, Any]:
    run("git", "fetch", "origin", BRANCH, "--quiet")
    status_before = git("status", "--porcelain=v1").splitlines()
    head = git("rev-parse", "HEAD")
    local = head
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_rows = git("ls-remote", "origin", f"refs/heads/{BRANCH}").split()
    live = live_rows[0] if live_rows else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    sys.path.insert(0, str(REPO))
    tests = run_tests()
    from scripts.ghc_family_v651_v7_detailed_validator import validate as detailed_validate
    from scripts.ghc_family_v651_v7_minimal_validator import validate as minimal_validate

    detailed = detailed_validate()
    minimal = minimal_validate()
    x1_manifest = verify_manifest(X1, f"{ROOT}/validation/x1-staged-manifest.json")
    evidence_manifest = verify_manifest(
        EVIDENCE, f"{ROOT}/validation/evidence-staged-manifest.json"
    )
    final_manifest = verify_manifest(
        SEAL, f"{ROOT}/validation/final-staged-manifest.json"
    )
    owner_manifest = verify_manifest(SEAL, f"{ROOT}/validation/owner-manifest.json")
    correction_manifest = verify_manifest(
        head, f"{ROOT}/validation/correction-staged-manifest.json"
    )
    corrected_owner_manifest = verify_manifest(
        head, f"{ROOT}/validation/corrected-owner-manifest.json"
    )
    tree = tree_map(head)
    phase_paths = sorted(path for path in tree if path.startswith(f"{ROOT}/"))
    owner_expected = sorted(
        path for path in tree if path.startswith(f"{ROOT}/") or path in OWNER_GLOBALS
    )
    owner_payload = corrected_owner_manifest["payload"]
    owner_union = sorted(
        [row["path"] for row in owner_payload["entries"]]
        + owner_payload["self_exclusions"]
    )
    final_payload = final_manifest["payload"]
    final_union = sorted(
        [row["path"] for row in final_payload["entries"]]
        + final_payload["self_exclusions"]
    )
    final_changed = sorted(
        line
        for line in git("diff", "--name-only", EVIDENCE, SEAL).splitlines()
        if line
    )
    correction_payload = correction_manifest["payload"]
    correction_union = sorted(
        [row["path"] for row in correction_payload["entries"]]
        + correction_payload["self_exclusions"]
    )
    correction_changed = sorted(
        line
        for line in git("diff", "--name-only", SEAL, head).splitlines()
        if line
    )
    evidence_payload = evidence_manifest["payload"]
    evidence_union = sorted(
        [row["path"] for row in evidence_payload["entries"]]
        + evidence_payload["self_exclusions"]
    )
    evidence_changed = sorted(
        line
        for line in git("diff", "--name-only", X1, EVIDENCE).splitlines()
        if line
    )
    json_paths = [path for path in phase_paths if path.endswith(".json")]
    json_failures: list[str] = []
    for path in json_paths:
        try:
            json.loads(blob(head, path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            json_failures.append(path)
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:codex|thread|task|app|plugin)://"),
        "delegation_markup": re.compile(r"(?i)<codex_delegation"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{8,}"),
    }
    scanner_definitions = {
        "scripts/build_ghc_family_v651_v7_preregistration.py",
        "scripts/build_ghc_family_v651_v7_evidence.py",
        "scripts/build_ghc_family_v651_v7_closeout.py",
        "scripts/build_ghc_family_v651_v7_terminal_correction.py",
        "scripts/ghc_family_v651_v7_final_validator.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in owner_expected:
        text = blob(head, path).decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path in scanner_definitions else "confirmed_payload_hit"
                row = {"path": path, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    oversized: list[dict[str, Any]] = []
    for path in owner_expected:
        if Path(path).suffix.casefold() not in {".md", ".txt", ".html", ".json"}:
            continue
        words = len(blob(head, path).decode("utf-8", errors="replace").split())
        if words > 100000:
            oversized.append({"path": path, "words": words})
    baton_path = f"{ROOT}/handoffs/authorized-successor-v651-v8-pending-confirmation.md"
    overview_path = f"{ROOT}/overview/final-integrated-overview.md"
    baton_words = len(blob(head, baton_path).decode("utf-8").split())
    overview_words = len(blob(head, overview_path).decode("utf-8").split())
    route = load_at(head, f"{ROOT}/route/terminal-route.json")
    truth = load_at(head, f"{ROOT}/truth/corrected-final-phase-truth.json")
    source_ancestry = all(
        run("git", "merge-base", "--is-ancestor", anchor, head, check=False).returncode == 0
        for anchor in (SOURCE, X1, EVIDENCE, SEAL)
    )
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_count = len(git("rev-list", "--merges", f"{SOURCE}..{head}").splitlines())
    new_commits = [
        row for row in git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if row
    ]
    parent_counts = [
        len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1
        for commit in new_commits
    ]
    final_parent = git("rev-parse", f"{head}^")
    diff_hygiene = run("git", "diff", "--check", SOURCE, head, check=False)
    status_after = git("status", "--porcelain=v1").splitlines()
    checks = {
        "exact_head": head == expected_head,
        "tests": tests["successful"],
        "test_count": tests["tests_run"] == 69,
        "detailed": detailed["valid"],
        "minimal": minimal["valid"],
        "json": not json_failures,
        "privacy": not confirmed,
        "x1_manifest": x1_manifest["valid"],
        "evidence_manifest": evidence_manifest["valid"],
        "final_manifest": final_manifest["valid"],
        "owner_manifest": owner_manifest["valid"],
        "correction_manifest": correction_manifest["valid"],
        "corrected_owner_manifest": corrected_owner_manifest["valid"],
        "evidence_path_parity": evidence_union == evidence_changed,
        "final_path_parity": final_union == final_changed,
        "correction_path_parity": correction_union == correction_changed,
        "owner_path_parity": owner_union == owner_expected,
        "owner_threshold": len(owner_expected) < 2000,
        "document_cap": not oversized,
        "baton_contract": 10000 <= baton_words <= 100000,
        "overview_contract": 3000 <= overview_words <= 100000,
        "source_ancestry": source_ancestry,
        "phase_commit_cap": phase_commits == 4 and phase_commits <= 6,
        "zero_merges": merge_count == 0,
        "single_parent_history": all(count == 1 for count in parent_counts),
        "final_parent": final_parent == SEAL,
        "diff_hygiene": diff_hygiene.returncode == 0,
        "clean_before": not status_before,
        "clean_after": not status_after,
        "four_way_equality": len({local, upstream, tracking, live}) == 1,
        "zero_divergence": divergence == ["0", "0"],
        "route_not_overclaimed": (
            route["status"] == "PREPARED_NOT_SENT"
            and route["task_messages_sent"] == 0
            and not route["candidate_is_live_authority"]
            and not route["exact_successor_confirmed"]
        ),
        "future_cli_unlaunched": (
            route["future_cli_placeholders"] == 8
            and route["future_cli_names_chosen"] == 0
            and route["future_cli_launches"] == 0
        ),
        "truth_boundary": (
            truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
            and truth["effective_negatives"] == 7458
            and truth["effective_open_gaps"] == 59
            and truth["effective_exact_gates"] == 60
            and not truth["independent_reproduction"]
        ),
    }
    return {
        "schema": "ghc.family.v651-v7.canonical-final-validation.v2",
        "owner": "Vesper Arlen",
        "phase": "v651-gmut-thos-v7-x1-x2",
        "head": head,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "seal": SEAL,
        "tests": tests,
        "detailed": {"passed": detailed["passed_count"], "total": detailed["check_count"]},
        "minimal": {"passed": minimal["passed_count"], "total": minimal["check_count"]},
        "json": {"parsed": len(json_paths) - len(json_failures), "total": len(json_paths), "failures": json_failures},
        "privacy": {
            "scanned_files": len(owner_expected),
            "pattern_classes": sorted(patterns),
            "candidate_count": len(candidates),
            "candidates": candidates,
            "confirmed_hit_count": len(confirmed),
            "confirmed_hits": confirmed,
            "complete_privacy_assurance": False,
        },
        "manifests": {
            "x1_entries": x1_manifest["entry_count"],
            "evidence_entries": evidence_manifest["entry_count"],
            "final_entries": final_manifest["entry_count"],
            "owner_entries": owner_manifest["entry_count"],
            "correction_entries": correction_manifest["entry_count"],
            "corrected_owner_entries": corrected_owner_manifest["entry_count"],
        },
        "owner_files": len(owner_expected),
        "baton_words": baton_words,
        "overview_words": overview_words,
        "phase_commits": phase_commits,
        "merge_count": merge_count,
        "parent_counts": parent_counts,
        "remote": {
            "local": local,
            "upstream": upstream,
            "tracking": tracking,
            "live": live,
            "ahead": int(divergence[0]),
            "behind": int(divergence[1]),
        },
        "checks": checks,
        "valid": all(checks.values()),
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "terminal_route": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One successful canonical scoped validation under shared same-owner infrastructure; not independent reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, legal review, cultural ratification, professional validation, or Stage 20 authority.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    result = validate(args.expected_head)
    receipt = Path(args.receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "head": result["head"],
                "tests": result["tests"]["tests_run"],
                "detailed": result["detailed"],
                "minimal": result["minimal"],
                "json": result["json"],
                "privacy": {
                    "scanned_files": result["privacy"]["scanned_files"],
                    "confirmed_hit_count": result["privacy"]["confirmed_hit_count"],
                },
                "manifests": result["manifests"],
                "owner_files": result["owner_files"],
                "phase_commits": result["phase_commits"],
                "valid": result["valid"],
                "route": result["terminal_route"],
                "verdict": result["terminal_verdict"],
            },
            sort_keys=True,
        )
    )
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
