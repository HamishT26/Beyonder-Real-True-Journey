#!/usr/bin/env python3
"""Exclusive exact-final owner-scoped canonical completion for Sylven v667-v4."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"
SOURCE = "9625026b09860c8964dd818e8d1f81ee6e2eed57"
X1 = "0eb52121251e3e8ee6da0c3c472626640cde96a3"
EVIDENCE = "4de3cc042a3cb15c626e744fbf9977cc7e6ca437"
BRANCH = "codex/GHC-Family/sylven-arc-v667-v4-full-tools"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    )


def output(*args: str) -> str:
    return run(*args).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def load_test_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load test module {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_tests(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


def owner_tests() -> dict[str, Any]:
    loader = unittest.TestLoader()
    paths = [
        (ROOT / "tests" / "test_ghc_family_sylven_arc_v667_v4_x1.py", "sa6674_x1"),
        (ROOT / "tests" / "test_ghc_family_sylven_arc_v667_v4_x2.py", "sa6674_x2"),
        (ROOT / "tests" / "test_ghc_family_sylven_arc_v667_v4_closeout.py", "sa6674_closeout"),
    ]
    selected = unittest.TestSuite()
    excluded = []
    for path, name in paths:
        module = load_test_module(path, name)
        suite = loader.loadTestsFromModule(module)
        for test in iter_tests(suite):
            if test.id().endswith("TestSylvenArcV667V4X1.test_no_x2_directory_or_outcome_artifact_exists"):
                excluded.append(test.id())
            else:
                selected.addTest(test)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(selected)
    if not result.wasSuccessful():
        raise AssertionError(stream.getvalue()[-4000:])
    x1_paths = output("git", "ls-tree", "-r", "--name-only", X1, "docs/sylven-arc/v667-v4").splitlines()
    x1_lifecycle_pass = not any(path.startswith("docs/sylven-arc/v667-v4/x2/") for path in x1_paths)
    if not x1_lifecycle_pass:
        raise AssertionError("immutable x1 tree contains an x2 path")
    return {
        "selected_tests_passed": result.testsRun,
        "declared_lifecycle_exclusions": excluded,
        "immutable_x1_git_tree_check_passed": x1_lifecycle_pass,
        "composite_test_count": result.testsRun + 1,
        "failures": len(result.failures),
        "errors": len(result.errors),
    }


def manifest_replay(relative: str) -> dict[str, Any]:
    manifest = load(relative)
    mismatches = []
    for row in manifest["entries"]:
        blob = subprocess.check_output(["git", "show", f"HEAD:{row['path']}"], cwd=ROOT)
        digest = hashlib.sha256(blob).hexdigest()
        if len(blob) != row["bytes"] or digest != row["sha256"]:
            mismatches.append(row["path"])
    return {
        "path": relative,
        "entries": len(manifest["entries"]),
        "self_exclusions": len(manifest["self_exclusions"]),
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    handle, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()

    head_before = output("git", "rev-parse", "HEAD")
    if head_before != args.expected_head:
        raise SystemExit("exact head mismatch before canonical completion")
    if output("git", "status", "--porcelain=v1"):
        raise SystemExit("canonical completion requires a clean worktree")

    fetch = run("git", "fetch", "origin", BRANCH)
    local = output("git", "rev-parse", "HEAD")
    upstream = output("git", "rev-parse", "@{u}")
    tracking = output("git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = output("git", "rev-parse", "FETCH_HEAD")
    divergence = output("git", "rev-list", "--left-right", "--count", "HEAD...@{u}").split()

    tests = owner_tests()
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    markdown_paths = sorted(PHASE_ROOT.rglob("*.md"))
    for path in markdown_paths:
        text = path.read_text(encoding="utf-8")
        if not text.strip() or "\x00" in text:
            raise AssertionError(f"invalid Markdown text: {path.name}")

    owner_paths = [path for path in output("git", "diff", "--name-only", SOURCE, "HEAD").splitlines() if path]
    prefixes = (
        "docs/sylven-arc/v667-v4/",
        "scripts/build_ghc_family_sylven_arc_v667_v4_",
        "scripts/ghc_family_sylven_arc_v667_v4_",
        "tests/test_ghc_family_sylven_arc_v667_v4_",
        "scripts/ghc_family_freed_id_flashcards.py",
    )
    out_of_scope = [path for path in owner_paths if not path.startswith(prefixes)]

    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\\\[^\r\n\"']+"),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']"),
        "private_callable_identifier": re.compile(rb"(?i)\b(source_thread_id|clientThreadId|resume_value|session_stream|private_callable)\b"),
        "transcript_or_private_app_state": re.compile(rb"(?i)\b(raw_transcript|private_app_state|terminal_session_stream|screenshot_payload)\b"),
    }
    scanner_paths = {
        "scripts/build_ghc_family_sylven_arc_v667_v4_closeout.py",
        "scripts/ghc_family_sylven_arc_v667_v4_canonical.py",
        "scripts/ghc_family_freed_id_flashcards.py",
        "tests/test_ghc_family_sylven_arc_v667_v4_closeout.py",
    }
    privacy_candidates: dict[str, list[str]] = {name: [] for name in patterns}
    scanner_candidates: dict[str, list[str]] = {name: [] for name in patterns}
    python_paths = []
    security_findings = []
    dangerous = {
        "eval": re.compile(rb"\beval\s*\("), "exec": re.compile(rb"\bexec\s*\("),
        "shell_true": re.compile(rb"shell\s*=\s*True"), "os_system": re.compile(rb"os\.system\s*\("),
        "pickle_loads": re.compile(rb"pickle\.loads\s*\("), "yaml_unsafe_load": re.compile(rb"yaml\.load\s*\("),
    }
    for path in owner_paths:
        blob = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
        if b"\x00" not in blob:
            for name, pattern in patterns.items():
                if pattern.search(blob):
                    (scanner_candidates if path in scanner_paths else privacy_candidates)[name].append(path)
        if path.endswith(".py"):
            python_paths.append(path)
            compile(blob.decode("utf-8"), path, "exec")
            if path not in scanner_paths:
                for name, pattern in dangerous.items():
                    if pattern.search(blob):
                        security_findings.append({"path": path, "class": name})

    manifests = [
        manifest_replay("validation/x1-content-manifest.json"),
        manifest_replay("validation/evidence-content-manifest.json"),
        manifest_replay("validation/final-delta-manifest.json"),
        manifest_replay("validation/final-owner-manifest.json"),
    ]
    history_rows = [line.split() for line in output("git", "rev-list", "--parents", f"{SOURCE}..HEAD").splitlines()]
    detailed = {
        "exact_head": local == args.expected_head,
        "source_ancestral": run("git", "merge-base", "--is-ancestor", SOURCE, "HEAD", check=False).returncode == 0,
        "x1_ancestral": run("git", "merge-base", "--is-ancestor", X1, "HEAD", check=False).returncode == 0,
        "evidence_ancestral": run("git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD", check=False).returncode == 0,
        "x1_direct_parent": output("git", "rev-parse", f"{X1}^") == SOURCE,
        "evidence_direct_parent": output("git", "rev-parse", f"{EVIDENCE}^") == X1,
        "final_direct_parent": output("git", "rev-parse", "HEAD^") == EVIDENCE,
        "three_phase_commits": int(output("git", "rev-list", "--count", f"{SOURCE}..HEAD")) == 3,
        "zero_merges": int(output("git", "rev-list", "--count", "--min-parents=2", f"{SOURCE}..HEAD")) == 0,
        "one_parent_each": len(history_rows) == 3 and all(len(row) == 2 for row in history_rows),
        "four_way_equal": len({local, upstream, tracking, fresh}) == 1,
        "zero_divergence": divergence == ["0", "0"],
        "clean": not output("git", "status", "--porcelain=v1"),
        "diff_hygiene": run("git", "diff", "--check", f"{SOURCE}..HEAD", check=False).returncode == 0,
        "owner_scope": not out_of_scope,
        "file_ceiling": len(owner_paths) < 2000,
        "json_parse": len(json_paths) > 0,
        "markdown_decode": len(markdown_paths) > 0,
        "privacy": not any(privacy_candidates.values()),
        "security": not security_findings,
        "manifest_parity": all(row["valid"] for row in manifests),
        "truth_terminal": load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_unsent": load("closeout/route-receipt.json")["status"] == "PREPARED_NOT_SENT",
        "full_suite_not_run": not load("closeout/phase-truth.json")["full_repository_suite_run"],
    }
    if not all(detailed.values()):
        raise AssertionError({name: value for name, value in detailed.items() if not value})

    minimal = {
        "head": detailed["exact_head"], "clean": detailed["clean"], "remote_equal": detailed["four_way_equal"],
        "divergence": detailed["zero_divergence"], "history": detailed["three_phase_commits"] and detailed["zero_merges"],
        "parent": detailed["final_direct_parent"], "tests": tests["failures"] == 0 and tests["errors"] == 0,
        "json": detailed["json_parse"], "privacy": detailed["privacy"], "security": detailed["security"],
        "manifests": detailed["manifest_parity"], "scope": detailed["owner_scope"], "caps": detailed["file_ceiling"],
        "route_hold": detailed["route_unsent"], "verdict": detailed["truth_terminal"],
    }
    if not all(minimal.values()):
        raise AssertionError({name: value for name, value in minimal.items() if not value})

    head_after = output("git", "rev-parse", "HEAD")
    clean_after = not output("git", "status", "--porcelain=v1")
    if head_after != args.expected_head or not clean_after:
        raise AssertionError("head or clean state changed during canonical completion")

    receipt = {
        "schema": "ghc-family-exclusive-exact-final-canonical-receipt-v5",
        "owner": "Sylven Arc",
        "phase": "v667-v4",
        "status": "VALID_EXCLUSIVE_OWNER_SCOPED_CANONICAL_COMPLETION",
        "exact_final": args.expected_head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "branch": BRANCH,
        "tests": tests,
        "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal_checks": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "phase_json_parses": len(json_paths),
        "phase_markdown_decodes": len(markdown_paths),
        "owner_files_scanned": len(owner_paths),
        "five_class_confirmed_privacy_hits": sum(len(rows) for rows in privacy_candidates.values()),
        "scanner_definition_candidates": sum(len(rows) for rows in scanner_candidates.values()),
        "python_files_compiled": len(python_paths),
        "bounded_security_findings": security_findings,
        "manifests": manifests,
        "manifest_entry_total": sum(row["entries"] for row in manifests),
        "manifest_self_exclusion_total": sum(row["self_exclusions"] for row in manifests),
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh,
        "divergence": divergence,
        "head_stable": head_before == head_after == args.expected_head,
        "clean_before_and_after": clean_after,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "post_success_replay_forbidden": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical_payload = json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt["canonical_payload_sha256"] = hashlib.sha256(canonical_payload).hexdigest()
    atomic_json(args.receipt, receipt)
    print(json.dumps({
        "status": receipt["status"], "exact_final": args.expected_head,
        "tests": tests["composite_test_count"], "detailed": len(detailed), "minimal": len(minimal),
        "json": len(json_paths), "owner_files": len(owner_paths), "manifest_entries": receipt["manifest_entry_total"],
        "privacy_hits": receipt["five_class_confirmed_privacy_hits"], "security_findings": len(security_findings),
    }, ensure_ascii=True))


if __name__ == "__main__":
    main()
