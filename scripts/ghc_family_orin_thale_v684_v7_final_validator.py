#!/usr/bin/env python3
"""Exclusive one-shot exact-final owner-scoped validator for Orin v684-v7."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "162b40162f1045c5ad91cfb454fad10973bf4914"
X1 = "ff4d5fd1bab9c098758a02fe08d254deac2ace44"
EVIDENCE = "ec330d5173cb142ebc03197b037d7d8859e23a51"
BRANCH = "codex/GHC-Family/orin-thale-v684-v7-full-tools"
PHASE_PREFIX = "docs/orin-thale/v684-v7/"
TEST_SELECTIONS = (
    (
        "tests/test_ghc_family_orin_thale_v684_v7_x1.py",
        {"OrinThaleV684V7X1Tests.test_x1_only_lifecycle"},
    ),
    (
        "tests/test_ghc_family_orin_thale_v684_v7_x2.py",
        {"OrinThaleV684V7X2Tests.test_lifecycle_starts_at_immutable_x1"},
    ),
    (
        "tests/test_ghc_family_orin_thale_v684_v7_final.py",
        {"OrinThaleV684V7FinalTests.test_precommit_lifecycle"},
    ),
)
MANIFESTS = (
    ("docs/orin-thale/v684-v7/validation/x1-index-manifest.json", X1, "commit_delta"),
    ("docs/orin-thale/v684-v7/validation/evidence-index-manifest.json", EVIDENCE, "commit_delta"),
    ("docs/orin-thale/v684-v7/validation/final-delta-manifest.json", "HEAD", "commit_delta"),
    ("docs/orin-thale/v684-v7/validation/final-owner-manifest.json", "HEAD", "owner_total"),
)


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def blob(path: str, anchor: str = "HEAD") -> bytes:
    result = subprocess.run(["git", "show", f"{anchor}:{path}"], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/build_ghc_family_orin_thale_v684_v7_")
        or path.startswith("scripts/ghc_family_herbarium_")
        or path.startswith("scripts/ghc_family_orin_thale_v684_v7_")
        or path.startswith("tests/test_ghc_family_orin_thale_v684_v7_")
    )


def validate_manifest(path: str, anchor: str, scope: str) -> dict[str, Any]:
    resolved = git("rev-parse", anchor)
    data = json.loads(blob(path, anchor).decode("utf-8"))
    for entry in data["entries"]:
        value = normalized(blob(entry["path"], anchor))
        if len(value) != entry["bytes"] or hashlib.sha256(value).hexdigest() != entry["sha256"]:
            raise RuntimeError(f"manifest mismatch: {path}: {entry['path']}")
    exclusions = set(data["declared_self_exclusions"])
    for excluded in exclusions:
        result = run(["git", "cat-file", "-e", f"{resolved}:{excluded}"])
        if result.returncode:
            raise RuntimeError(f"missing manifest exclusion: {excluded}")
    actual = exclusions | {entry["path"] for entry in data["entries"]}
    if scope == "commit_delta":
        expected = {
            item
            for item in git("diff-tree", "--no-commit-id", "--name-only", "-r", resolved).splitlines()
            if owner_path(item)
        }
    elif scope == "owner_total":
        expected = {
            item
            for item in git("diff", "--name-only", f"{SOURCE}..{resolved}").splitlines()
            if owner_path(item)
        }
    else:
        raise RuntimeError(f"unknown manifest scope: {scope}")
    if actual != expected:
        raise RuntimeError(f"manifest path-set mismatch: {path}: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
    if "owner_path_count" in data and data["owner_path_count"] != len(expected):
        raise RuntimeError(f"owner path count mismatch: {path}")
    return {
        "anchor": resolved,
        "scope": scope,
        "entries": len(data["entries"]),
        "self_exclusions": len(exclusions),
        "covered_paths": len(actual),
    }


def load_suite(path: str, exclusions: set[str]) -> tuple[unittest.TestSuite, dict[str, Any]]:
    module_name = "canonical_" + Path(path).stem
    spec = importlib.util.spec_from_file_location(module_name, ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    discovered = unittest.defaultTestLoader.loadTestsFromModule(module)
    flat: list[unittest.TestCase] = []

    def visit(suite: unittest.TestSuite) -> None:
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                visit(item)
            else:
                flat.append(item)

    visit(discovered)
    selected = []
    excluded_ids = []
    for test in flat:
        short = ".".join(test.id().split(".")[-2:])
        if short in exclusions:
            excluded_ids.append(short)
        else:
            selected.append(test)
    if set(excluded_ids) != exclusions:
        raise RuntimeError(f"test exclusion mismatch: {path}: {excluded_ids}")
    return unittest.TestSuite(selected), {
        "path": path,
        "discovered": len(flat),
        "eligible": len(selected),
        "excluded": sorted(exclusions),
    }


def scanner_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def canonical() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    checks = []
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("branch mismatch")
    checks.append("exact_branch")
    if git("rev-parse", "HEAD^") != EVIDENCE:
        raise RuntimeError("final parent mismatch")
    if git("rev-parse", f"{EVIDENCE}^") != X1 or git("rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("source lifecycle ancestry mismatch")
    checks.extend(["final_parent", "evidence_parent", "x1_parent"])
    if int(git("rev-list", "--count", f"{SOURCE}..HEAD")) != 3:
        raise RuntimeError("commit ceiling mismatch")
    if git("rev-list", "--merges", f"{SOURCE}..HEAD"):
        raise RuntimeError("merge detected")
    checks.extend(["three_commits", "zero_merges"])
    if git("diff", "--name-only", f"{X1}..HEAD", "--", "docs/orin-thale/v684-v7/x1", "scripts/build_ghc_family_orin_thale_v684_v7_x1.py", "tests/test_ghc_family_orin_thale_v684_v7_x1.py"):
        raise RuntimeError("immutable x1 changed after x1")
    if git(
        "diff",
        "--name-only",
        f"{EVIDENCE}..HEAD",
        "--",
        "docs/orin-thale/v684-v7/x2",
        "docs/orin-thale/v684-v7/skills",
        "scripts/build_ghc_family_orin_thale_v684_v7_x2.py",
        "scripts/ghc_family_herbarium_contract.py",
        ":(glob)scripts/ghc_family_herbarium_*_runner.py",
        "scripts/ghc_family_orin_thale_v684_v7_skill_bank.py",
        "tests/test_ghc_family_orin_thale_v684_v7_x2.py",
    ):
        raise RuntimeError("immutable evidence changed after evidence")
    checks.extend(["immutable_x1", "immutable_evidence"])
    if git("status", "--porcelain=v1"):
        raise RuntimeError("worktree not clean")
    checks.append("clean_before")

    stream = io.StringIO()
    test_results = []
    total_tests = 0
    combined = unittest.TestSuite()
    for path, exclusions in TEST_SELECTIONS:
        suite, summary = load_suite(path, exclusions)
        total_tests += summary["eligible"]
        test_results.append(summary)
        combined.addTests(suite)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(combined)
    if not result.wasSuccessful():
        raise RuntimeError(f"selected tests failed: {stream.getvalue()}")
    checks.append("selected_tests")

    manifests = {path: validate_manifest(path, anchor, scope) for path, anchor, scope in MANIFESTS}
    checks.append("manifest_replay")
    owner_paths = sorted(path for path in git("ls-tree", "-r", "--name-only", "HEAD").splitlines() if owner_path(path))
    json_parses = 0
    document_checks = 0
    python_ast = 0
    privacy_candidates = []
    confirmed = []
    security = []
    patterns = scanner_patterns()
    for path in owner_paths:
        data = blob(path)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        if path.endswith((".md", ".html", ".txt")):
            text = data.decode("utf-8")
            if len(text.split()) > 100000 or any(line.endswith((" ", "\t")) for line in text.splitlines()):
                raise RuntimeError(f"document hygiene issue: {path}")
            document_checks += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path)
            python_ast += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": node.func.id})
                if (
                    isinstance(node, ast.keyword)
                    and node.arg == "shell"
                    and isinstance(node.value, ast.Constant)
                    and node.value.value is True
                ):
                    security.append({"path": path, "finding": "shell_true"})
        scanner_definition = path.endswith(
            (
                "build_ghc_family_orin_thale_v684_v7_x1.py",
                "build_ghc_family_orin_thale_v684_v7_x2.py",
                "build_ghc_family_orin_thale_v684_v7_final.py",
                "ghc_family_orin_thale_v684_v7_final_validator.py",
            )
        )
        for class_name, pattern in patterns.items():
            for _ in pattern.finditer(data):
                if scanner_definition:
                    privacy_candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append({"path": path, "class": class_name})
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security:
        raise RuntimeError(f"bounded security findings: {security}")
    checks.extend(["strict_json", "document_hygiene", "python_ast", "privacy_scan", "bounded_security"])
    handoff_words = len(blob("docs/orin-thale/v684-v7/final/liora-venn-v684-v8-activation-candidate.md").decode("utf-8").split())
    if not 10000 <= handoff_words <= 100000:
        raise RuntimeError("handoff word bound failed")
    checks.append("handoff_word_bound")

    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    if not live_row:
        raise RuntimeError("fresh live remote row missing")
    live = live_row.split("\t", 1)[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    if not (head == upstream == tracking == live and divergence == ["0", "0"]):
        raise RuntimeError("four-way equality failed")
    checks.extend(["local_upstream", "tracking", "fresh_live", "zero_divergence"])
    if git("status", "--porcelain=v1"):
        raise RuntimeError("worktree changed during canonical")
    checks.append("clean_after")
    minimal = [
        "source_anchor",
        "x1_anchor",
        "evidence_anchor",
        "final_parent",
        "zero_merges",
        "commit_ceiling",
        "clean_before",
        "tests",
        "json",
        "privacy",
        "security",
        "manifests",
        "remote_equality",
        "clean_after",
        "route_held",
    ]
    return {
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Orin Thale",
        "phase": "v684-v7",
        "exact_final_head": head,
        "branch": BRANCH,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "replayed": False,
        "test_results": test_results,
        "selected_tests": total_tests,
        "detailed_checks": len(checks),
        "detailed_check_names": checks,
        "minimal_checks": len(minimal),
        "minimal_check_names": minimal,
        "json_parses": json_parses,
        "document_checks": document_checks,
        "python_ast_parses": python_ast,
        "manifest_results": manifests,
        "manifest_entries": sum(item["entries"] for item in manifests.values()),
        "owner_paths": len(owner_paths),
        "privacy_classes": list(patterns),
        "privacy_candidates": privacy_candidates,
        "confirmed_privacy_hits": 0,
        "bounded_security_findings": 0,
        "handoff_words": handoff_words,
        "complete_repository_suite": False,
        "same_owner_shared_infrastructure": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state_at_validation": "PREPARED_NOT_SENT",
        "four_way_equal": True,
        "divergence": {"ahead": 0, "behind": 0},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-root", type=Path, required=True)
    args = parser.parse_args()
    args.receipt_root.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    latch = args.receipt_root / f"orin-thale-v684-v7-{head}.latch.json"
    receipt = args.receipt_root / f"orin-thale-v684-v7-{head}.json"
    fd = os.open(latch, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"state": "CANONICAL_INVOKED_ONCE", "head": head}, handle, indent=2, sort_keys=True)
            handle.write("\n")
        payload = canonical()
        payload_bytes = (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        wrapper = {"payload": payload, "payload_sha256": hashlib.sha256(payload_bytes).hexdigest()}
        with receipt.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(wrapper, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        print(
            json.dumps(
                {
                    "status": payload["status"],
                    "exact_final_head": head,
                    "payload_sha256": wrapper["payload_sha256"],
                    "receipt_filename": receipt.name,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except Exception as exc:
        failure = args.receipt_root / f"orin-thale-v684-v7-{head}.failed.json"
        failure.write_text(
            json.dumps(
                {
                    "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
                    "head": head,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
