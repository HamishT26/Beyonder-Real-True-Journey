#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Tamar v678-v4."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


SOURCE = "471db44e52f9ab776b6abf05896d405022524b18"
X1 = "29a886dc5838093ed092ffc20c3d86af3b24e47c"
EVIDENCE = "18ffd0764b6df5f64360c286eabcdb361e4c29c3"
BRANCH = "codex/GHC-Family/tamar-vey-v678-v4-full-tools"
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
PHASE_PREFIX = "docs/tamar-vey/v678-v4/"
TEST_SELECTIONS = (
    (
        "tests.test_ghc_family_tamar_vey_v678_v4_x1",
        ("tests.test_ghc_family_tamar_vey_v678_v4_x1.TamarVeyV678V4X1Tests.test_x1_only_lifecycle",),
    ),
    ("tests.test_ghc_family_tamar_vey_v678_v4_x2", ()),
    ("tests.test_ghc_family_tamar_vey_v678_v4_final", ()),
)
MANIFESTS = (
    ("docs/tamar-vey/v678-v4/validation/x1-index-manifest.json", X1, "commit_delta"),
    ("docs/tamar-vey/v678-v4/validation/evidence-index-manifest.json", EVIDENCE, "commit_delta"),
    ("docs/tamar-vey/v678-v4/validation/final-delta-manifest.json", "HEAD", "commit_delta"),
    ("docs/tamar-vey/v678-v4/validation/final-owner-manifest.json", "HEAD", "owner_total"),
)


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=False)
    if check and result.returncode:
        raise RuntimeError(f"command failed: {args[0]}: {result.stdout} {result.stderr}")
    return result


def git(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def blob(path: str, anchor: str = "HEAD") -> bytes:
    return subprocess.check_output(["git", "show", f"{anchor}:{path}"], cwd=REPO)


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def batch_blobs(anchor: str, paths: list[str]) -> dict[str, bytes]:
    requests = b"".join(f"{anchor}:{path}\n".encode("utf-8") for path in paths)
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=requests,
        capture_output=True,
        check=True,
    )
    stream = io.BytesIO(result.stdout)
    objects: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().rstrip(b"\n").rsplit(b" ", 2)
        if len(header) != 3 or header[1] != b"blob":
            raise RuntimeError(f"unexpected batch header for {path}: {header!r}")
        size = int(header[2])
        value = stream.read(size)
        if len(value) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated batch object for {path}")
        objects[path] = value
    if stream.read():
        raise RuntimeError("unexpected trailing batch bytes")
    return objects


def owner_path(path: str) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path.startswith("scripts/build_ghc_family_tamar_vey_v678_v4_")
        or path.startswith("scripts/ghc_family_tamar_v678_v4_")
        or path == "scripts/ghc_family_tamar_vey_v678_v4_final_validator.py"
        or path.startswith("tests/test_ghc_family_tamar_vey_v678_v4_")
    )


def validate_manifest(path: str, anchor: str, scope: str) -> dict[str, Any]:
    resolved_anchor = git("rev-parse", anchor)
    data = json.loads(blob(path, anchor).decode("utf-8"))
    manifest_blobs = batch_blobs(resolved_anchor, [entry["path"] for entry in data["entries"]])
    for entry in data["entries"]:
        value = normalized(manifest_blobs[entry["path"]])
        if len(value) != entry["bytes"] or hashlib.sha256(value).hexdigest() != entry["sha256"]:
            raise RuntimeError(f"manifest mismatch: {path}: {entry['path']}")
    exclusions = set(data["declared_self_exclusions"])
    for excluded in exclusions:
        run(["git", "cat-file", "-e", f"{resolved_anchor}:{excluded}"])
    actual = {entry["path"] for entry in data["entries"]} | exclusions
    if scope == "commit_delta":
        expected = {
            item
            for item in git("diff-tree", "--no-commit-id", "--name-only", "-r", resolved_anchor).splitlines()
            if owner_path(item)
        }
    elif scope == "owner_total":
        expected = {
            item
            for item in git("diff", "--name-only", f"{SOURCE}..{resolved_anchor}").splitlines()
            if owner_path(item)
        }
    else:
        raise RuntimeError(f"unknown manifest scope: {scope}")
    if actual != expected:
        raise RuntimeError(
            f"manifest path-set mismatch: {path}: missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )
    if "owner_path_count" in data and data["owner_path_count"] != len(expected):
        raise RuntimeError(f"owner path-count mismatch: {path}")
    return {
        "anchor": resolved_anchor,
        "scope": scope,
        "entries": len(data["entries"]),
        "self_exclusions": len(exclusions),
        "covered_paths": len(actual),
    }


def flatten(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    tests: list[unittest.TestCase] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            tests.extend(flatten(item))
        else:
            tests.append(item)
    return tests


def run_test_selection(module: str, excluded: tuple[str, ...]) -> dict[str, Any]:
    importlib.import_module(module)
    discovered = flatten(unittest.defaultTestLoader.loadTestsFromName(module))
    selected = [test for test in discovered if test.id() not in excluded]
    if len(discovered) != len(selected) + len(excluded):
        raise RuntimeError(f"test exclusion arithmetic mismatch: {module}")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.TestSuite(selected))
    if not result.wasSuccessful():
        raise RuntimeError(f"selected tests failed: {module}: {stream.getvalue()}")
    return {
        "module": module,
        "discovered": len(discovered),
        "eligible": len(selected),
        "excluded": list(excluded),
        "state": "passed",
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
    checks: list[str] = []
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("branch mismatch")
    checks.append("exact_branch")
    if git("rev-parse", "HEAD^") != EVIDENCE or git("rev-parse", f"{EVIDENCE}^") != X1 or git("rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("direct ancestry mismatch")
    checks.extend(["final_parent", "evidence_parent", "x1_parent"])
    if int(git("rev-list", "--count", f"{SOURCE}..HEAD")) != 3:
        raise RuntimeError("commit ceiling mismatch")
    if git("rev-list", "--merges", f"{SOURCE}..HEAD"):
        raise RuntimeError("merge detected")
    checks.extend(["three_commits", "zero_merges"])
    if git("ls-tree", "-r", "--name-only", X1, "--", f"{PHASE_PREFIX}x2", f"{PHASE_PREFIX}final"):
        raise RuntimeError("immutable x1 contains later lifecycle paths")
    checks.append("immutable_x1_lifecycle_absence")
    if git("status", "--porcelain=v1"):
        raise RuntimeError("worktree not clean")
    checks.append("clean_before")

    test_results = []
    total_tests = 0
    for module, excluded in TEST_SELECTIONS:
        result = run_test_selection(module, excluded)
        total_tests += result["eligible"]
        test_results.append(result)

    manifests = {
        path: validate_manifest(path, anchor, scope)
        for path, anchor, scope in MANIFESTS
    }
    manifest_entries = sum(value["entries"] for value in manifests.values())
    owner_paths = sorted(path for path in git("ls-tree", "-r", "--name-only", "HEAD").splitlines() if owner_path(path))
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner file ceiling exceeded")
    checks.append("owner_file_ceiling")
    json_parses = 0
    markdown_checks = 0
    python_parses = 0
    privacy_candidates = []
    confirmed = []
    security = []
    patterns = scanner_patterns()
    stale_phrases = (
        b"wrong Orin branch",
        b"OrinThaleV678V2",
        b"ghc_family_build_provenance_",
        b"sixty Orin contracts",
        b"three Orin commits",
        b"not changed by Orin",
        b'"conditional_successor_title": "Tamar Vey"',
        b"audiovisual-preservation",
        b"integrated-pest-management",
        b"ghc_family_tamar_v678_v3_",
    )
    stale_labels = []
    owner_blobs = batch_blobs(head, owner_paths)
    for path in owner_paths:
        data = owner_blobs[path]
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_parses += 1
        if path.endswith((".md", ".html")):
            text = data.decode("utf-8")
            if any(line.endswith((" ", "\t")) for line in text.splitlines()):
                raise RuntimeError(f"markdown or html whitespace issue: {path}")
            if len(text.split()) > 100000:
                raise RuntimeError(f"document word ceiling exceeded: {path}")
            markdown_checks += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path); python_parses += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                    security.append({"path": path, "finding": "shell_true"})
        definition_ranges = []
        for marker in (b"def privacy_patterns()", b"def patterns()", b"def scanner_patterns()"):
            start = data.find(marker)
            if start >= 0:
                end = data.find(b"\ndef ", start + len(marker))
                if end < 0:
                    end = len(data)
                definition_ranges.append((start, end))
        stale_definition_start = data.find(b"stale_phrases = (")
        stale_definition_end = data.find(b"stale_labels = []", stale_definition_start)
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                if any(start <= match.start() < end for start, end in definition_ranges):
                    privacy_candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append({"path": path, "class": class_name})
        for phrase in stale_phrases:
            cursor = 0
            while True:
                match = data.find(phrase, cursor)
                if match < 0:
                    break
                scanner_definition_only = (
                    path == "scripts/ghc_family_tamar_vey_v678_v4_final_validator.py"
                    and stale_definition_start >= 0
                    and stale_definition_end > stale_definition_start
                    and stale_definition_start <= match < stale_definition_end
                )
                if not scanner_definition_only:
                    stale_labels.append({"path": path, "phrase": phrase.decode("utf-8")})
                cursor = match + len(phrase)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security:
        raise RuntimeError(f"bounded security findings: {security}")
    if stale_labels:
        raise RuntimeError(f"semantic stale labels: {stale_labels}")
    diff_hygiene = run(["git", "diff", "--check", "HEAD^", "HEAD"], check=False)
    if diff_hygiene.returncode:
        raise RuntimeError(f"diff hygiene failed: {diff_hygiene.stdout} {diff_hygiene.stderr}")
    phase_truth = json.loads(blob(f"{PHASE_PREFIX}final/phase-truth.json").decode("utf-8"))
    route_plan = json.loads(blob(f"{PHASE_PREFIX}final/route-plan.json").decode("utf-8"))
    if phase_truth["route_state"] != "PREPARED_NOT_SENT" or route_plan["state"] != "PREPARED_NOT_SENT" or route_plan["message_sent"]:
        raise RuntimeError("route hold mismatch")
    checks.extend([
        "unit_tests", "manifest_replay", "strict_json", "document_hygiene", "document_word_ceiling",
        "python_ast", "privacy_scan", "bounded_security", "semantic_stale_labels", "diff_hygiene", "route_held",
    ])

    local = head
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    if not live_row:
        raise RuntimeError("fresh live remote row missing")
    live = live_row.split("\t", 1)[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    if not (local == upstream == tracking == live and divergence == ["0", "0"]):
        raise RuntimeError("four-way equality failed")
    checks.extend(["local_upstream", "tracking", "fresh_live", "zero_divergence"])
    if git("status", "--porcelain=v1"):
        raise RuntimeError("worktree changed during canonical")
    checks.append("clean_after")
    minimal = [
        "source_anchor", "x1_anchor", "evidence_anchor", "final_parent", "zero_merges",
        "commit_ceiling", "clean_before", "tests", "json", "privacy", "security",
        "manifests", "remote_equality", "clean_after", "route_held",
    ]
    return {
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Tamar Vey",
        "phase": "v678-v4",
        "exact_final_head": head,
        "branch": BRANCH,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "prior_failed_canonical": None,
        "total_canonical_attempts_across_distinct_heads": 1,
        "total_canonical_successes": 1,
        "replayed": False,
        "test_results": test_results,
        "selected_tests": total_tests,
        "detailed_checks": len(checks),
        "detailed_check_names": checks,
        "minimal_checks": len(minimal),
        "minimal_check_names": minimal,
        "json_parses": json_parses,
        "markdown_html_checks": markdown_checks,
        "python_ast_parses": python_parses,
        "manifest_results": manifests,
        "manifest_entries": manifest_entries,
        "owner_paths": len(owner_paths),
        "privacy_classes": list(patterns),
        "privacy_candidates": privacy_candidates,
        "confirmed_privacy_hits": 0,
        "bounded_security_findings": 0,
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
    latch = args.receipt_root / f"tamar-vey-v678-v4-{head}.latch.json"
    receipt = args.receipt_root / f"tamar-vey-v678-v4-{head}.json"
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
        print(json.dumps({"status": payload["status"], "exact_final_head": head, "payload_sha256": wrapper["payload_sha256"], "receipt_filename": receipt.name}, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        failure = args.receipt_root / f"tamar-vey-v678-v4-{head}.failed.json"
        failure.write_text(json.dumps({"status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "head": head, "error_type": type(exc).__name__, "error": str(exc)}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
