#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for v672-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SOURCE = "842956c8ddc8b648d14911ac6228ba1cffb7d5ad"
X1 = "1875dc20ea21a47fd411bc898ee274e632b2977f"
EVIDENCE = "f1335924c402b450c1458f15d77a759d0e23d291"
EXPECTED_BRANCH = "codex/GHC-Family/sable-rook-v672-v3-full-tools"
PHASE_PREFIX = "docs/sable-rook/v672-v3/"
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}
PRIVACY_PATTERNS = {
    "raw_uuid_identifier": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\(?:Users|GHC-Archives|Windows)\\[^\r\n\"']+"),
    "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    "private_application_route": re.compile(rb"\b(?:app|file|vscode)://[^\s\"']+"),
    "session_stream_marker": re.compile(rb"(?i)\b(?:session[_-]?stream|terminal[_-]?session)\s*[:=]\s*[\"'][^\"']+[\"']"),
}


def git(root: Path, *args: str, text: bool = False):
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        check=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return completed.stdout


def git_text(root: Path, *args: str) -> str:
    return git(root, *args, text=True).strip()


def git_blob(root: Path, revision: str, path: str) -> bytes:
    return git(root, "show", f"{revision}:{path}")


def read_json_blob(root: Path, revision: str, path: str) -> Any:
    return json.loads(git_blob(root, revision, path).decode("utf-8"))


def write_receipt(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def owner_path(path: str) -> bool:
    return (
        path.startswith(PHASE_PREFIX)
        or path == "scripts/build_ghc_family_sable_rook_v672_v3.py"
        or path.startswith("scripts/ghc_family_sable_v672_v3_")
        or path == "scripts/validate_ghc_family_sable_rook_v672_v3_final.py"
        or path.startswith("tests/test_ghc_family_sable_rook_v672_v3_")
    )


def materialize_x1(root: Path, destination: Path) -> None:
    paths = git_text(root, "ls-tree", "-r", "--name-only", X1).splitlines()
    selected = [
        path
        for path in paths
        if path.startswith("docs/sable-rook/v672-v3/x1/")
        or path == "scripts/build_ghc_family_sable_rook_v672_v3.py"
        or path == "tests/test_ghc_family_sable_rook_v672_v3_x1.py"
    ]
    for relative in selected:
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(git_blob(root, X1, relative))


def run_test_module(test_root: Path, pattern: str) -> dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(test_root), "-p", pattern, "-v"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
    )
    combined = completed.stdout + completed.stderr
    match = re.search(r"Ran (\d+) tests?", combined)
    return {
        "pattern": pattern,
        "tests": int(match.group(1)) if match else 0,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "failing_test_ids": sorted(
            set(
                line.split()[0]
                for line in combined.splitlines()
                if line.startswith(("FAIL:", "ERROR:")) and line.split()
            )
        ),
    }


def validate_manifest(root: Path, revision: str, path: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = read_json_blob(root, revision, path)
    details = []
    mismatches = []
    for row in manifest["entries"]:
        observed_oid = git_text(root, "rev-parse", f"{revision}:{row['path']}")
        observed_blob = git_blob(root, revision, row["path"])
        valid = observed_oid == row["git_blob_oid"] and hashlib.sha256(observed_blob).hexdigest() == row["sha256"]
        details.append({"check": f"manifest:{path}:{row['path']}", "valid": valid})
        if not valid:
            mismatches.append(row["path"])
    exclusions_missing = [
        exclusion
        for exclusion in manifest.get("self_exclusions", [])
        if subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{revision}:{exclusion}"],
            capture_output=True,
        ).returncode
        != 0
    ]
    return (
        {
            "path": path,
            "revision": revision,
            "entries": len(manifest["entries"]),
            "self_exclusions": len(manifest.get("self_exclusions", [])),
            "mismatches": mismatches,
            "exclusions_missing": exclusions_missing,
            "valid": not mismatches and not exclusions_missing,
        },
        details,
    )


def ast_findings(path: str, source: bytes) -> list[str]:
    try:
        tree = ast.parse(source.decode("utf-8"), filename=path)
    except (UnicodeDecodeError, SyntaxError):
        return ["parse_failure"]
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append(f"dynamic_execution:{node.lineno}")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if (node.func.value.id, node.func.attr) in {("os", "system"), ("pickle", "loads")}:
                    findings.append(f"unsafe_call:{node.lineno}")
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append(f"shell_true:{node.lineno}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--scratch-root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    scratch_root = Path(args.scratch_root).resolve()
    if output.exists():
        raise SystemExit("canonical latch spent: output already exists")
    write_receipt(
        output,
        {
            "schema": "ghc.family.sable.v672-v3.external-canonical.v1",
            "status": "RUNNING_CANONICAL_LATCH_SPENT",
            "canonical_invocations": 1,
            "canonical_successes": 0,
        },
    )
    try:
        clean_before = git_text(root, "status", "--porcelain=v1") == ""
        head = git_text(root, "rev-parse", "HEAD")
        branch = git_text(root, "rev-parse", "--abbrev-ref", "HEAD")
        upstream = git_text(root, "rev-parse", "@{u}")
        tracking = git_text(root, "rev-parse", f"refs/remotes/origin/{EXPECTED_BRANCH}")
        live_line = git_text(root, "ls-remote", "--heads", "origin", f"refs/heads/{EXPECTED_BRANCH}")
        fresh_live = live_line.split()[0] if live_line else ""
        divergence_parts = git_text(root, "rev-list", "--left-right", "--count", "HEAD...@{u}").split()
        ahead, behind = (int(divergence_parts[0]), int(divergence_parts[1]))
        parents = git_text(root, "show", "-s", "--format=%P", "HEAD").split()
        phase_commits = int(git_text(root, "rev-list", "--count", f"{SOURCE}..HEAD"))
        merge_lines = git_text(root, "rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
        source_x1_direct = git_text(root, "rev-parse", f"{X1}^") == SOURCE
        x1_evidence_direct = git_text(root, "rev-parse", f"{EVIDENCE}^") == X1
        evidence_final_direct = len(parents) == 1 and parents[0] == EVIDENCE

        with tempfile.TemporaryDirectory(prefix="sable-v672-v3-x1-", dir=scratch_root) as temp:
            temp_root = Path(temp)
            materialize_x1(root, temp_root)
            x1_tests = run_test_module(temp_root / "tests", "test_ghc_family_sable_rook_v672_v3_x1.py")
        x2_tests = run_test_module(root / "tests", "test_ghc_family_sable_rook_v672_v3_x2.py")
        final_tests = run_test_module(root / "tests", "test_ghc_family_sable_rook_v672_v3_final.py")
        test_suites = [x1_tests, x2_tests, final_tests]

        manifests = []
        detailed: list[dict[str, Any]] = []
        for revision, path in [
            (X1, "docs/sable-rook/v672-v3/x1/staged-manifest.json"),
            (EVIDENCE, "docs/sable-rook/v672-v3/validation/evidence-staged-manifest.json"),
            (head, "docs/sable-rook/v672-v3/validation/final-staged-manifest.json"),
            (head, "docs/sable-rook/v672-v3/closeout/owner-manifest.json"),
        ]:
            summary, checks = validate_manifest(root, revision, path)
            manifests.append(summary)
            detailed.extend(checks)

        tree_paths = git_text(root, "ls-tree", "-r", "--name-only", head).splitlines()
        phase_paths = [path for path in tree_paths if path.startswith(PHASE_PREFIX)]
        owner_paths = [path for path in tree_paths if owner_path(path)]
        json_paths = [path for path in phase_paths if path.endswith(".json")]
        json_issues = []
        for path in json_paths:
            try:
                json.loads(git_blob(root, head, path).decode("utf-8"))
                valid = True
            except (UnicodeDecodeError, json.JSONDecodeError):
                valid = False
                json_issues.append(path)
            detailed.append({"check": f"json:{path}", "valid": valid})

        changed_paths = git_text(root, "diff", "--name-only", f"{SOURCE}..{head}").splitlines()
        changed_text_paths = [path for path in changed_paths if Path(path).suffix.casefold() in TEXT_SUFFIXES]
        privacy_hits = []
        for path in changed_text_paths:
            blob = git_blob(root, head, path)
            file_hits = []
            for class_name, pattern in PRIVACY_PATTERNS.items():
                for match in pattern.finditer(blob):
                    file_hits.append({"path": path, "class": class_name, "offset": match.start()})
            privacy_hits.extend(file_hits)
            detailed.append({"check": f"privacy:{path}", "valid": not file_hits})

        python_paths = [path for path in changed_paths if path.endswith(".py")]
        security_findings = []
        for path in python_paths:
            findings = ast_findings(path, git_blob(root, head, path))
            security_findings.extend({"path": path, "finding": finding} for finding in findings)
            detailed.append({"check": f"python_ast:{path}", "valid": not findings})

        markdown_paths = [path for path in phase_paths if path.endswith(".md")]
        markdown_over_cap = []
        markdown_word_counts = []
        for path in markdown_paths:
            words = len(git_blob(root, head, path).decode("utf-8").split())
            markdown_word_counts.append({"path": path, "words": words})
            if words > 100000:
                markdown_over_cap.append(path)
            detailed.append({"check": f"word_cap:{path}", "valid": words <= 100000})

        seal = read_json_blob(root, head, "docs/sable-rook/v672-v3/closeout/content-seal.json")
        seal_mismatches = []
        for row in seal["targets"]:
            blob = git_blob(root, head, row["path"])
            valid = hashlib.sha256(blob).hexdigest() == row["sha256"] and len(blob) == row["bytes"]
            detailed.append({"check": f"content_seal:{row['path']}", "valid": valid})
            if not valid:
                seal_mismatches.append(row["path"])

        route = read_json_blob(root, head, "docs/sable-rook/v672-v3/handoffs/terminal-route-hold.json")
        phase_truth = read_json_blob(root, head, "docs/sable-rook/v672-v3/closeout/phase-truth.json")
        outcomes = phase_truth["outcomes"]
        allowed_labels = {"completed", "represented", "open_gap", "exact_gate"}
        minimal = [
            {"check": "expected_head", "valid": head == args.expected_head},
            {"check": "expected_branch", "valid": branch == EXPECTED_BRANCH},
            {"check": "clean_before", "valid": clean_before},
            {"check": "local_upstream_equal", "valid": head == upstream},
            {"check": "local_tracking_equal", "valid": head == tracking},
            {"check": "local_fresh_live_equal", "valid": head == fresh_live},
            {"check": "zero_ahead", "valid": ahead == 0},
            {"check": "zero_behind", "valid": behind == 0},
            {"check": "source_x1_direct", "valid": source_x1_direct},
            {"check": "x1_evidence_direct", "valid": x1_evidence_direct},
            {"check": "evidence_final_direct", "valid": evidence_final_direct},
            {"check": "phase_commit_count", "valid": phase_commits == 3},
            {"check": "zero_merges", "valid": len(merge_lines) == 0},
            {"check": "one_final_parent", "valid": len(parents) == 1},
            {"check": "owner_file_ceiling", "valid": len(owner_paths) < 2000},
            {"check": "all_manifests", "valid": all(row["valid"] for row in manifests)},
            {"check": "json_parse", "valid": not json_issues},
            {"check": "privacy", "valid": not privacy_hits},
            {"check": "bounded_ast_security", "valid": not security_findings},
            {"check": "document_cap", "valid": not markdown_over_cap},
            {"check": "content_seal", "valid": not seal_mismatches},
            {"check": "test_suites", "valid": all(row["passed"] for row in test_suites)},
            {"check": "route_hold", "valid": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0},
            {"check": "truth_labels", "valid": set(outcomes) == allowed_labels},
            {"check": "terminal_verdict", "valid": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"},
        ]
        detailed.extend(minimal)
        clean_after = git_text(root, "status", "--porcelain=v1") == ""
        minimal.append({"check": "clean_after", "valid": clean_after})
        detailed.append({"check": "clean_after", "valid": clean_after})
        valid = all(row["valid"] for row in detailed) and all(row["passed"] for row in test_suites)
        receipt = {
            "schema": "ghc.family.sable.v672-v3.external-canonical.v1",
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "canonical_invocations": 1,
            "canonical_successes": 1 if valid else 0,
            "postsuccess_replay_allowed": False,
            "phase": "v672-v3",
            "owner": "Sable Rook",
            "source_head": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "exact_final_head": head,
            "branch": branch,
            "test_suites": test_suites,
            "selected_tests": sum(row["tests"] for row in test_suites),
            "detailed_checks": {"passed": sum(row["valid"] for row in detailed), "total": len(detailed)},
            "minimal_checks": {"passed": sum(row["valid"] for row in minimal), "total": len(minimal)},
            "phase_json": {"parsed": len(json_paths) - len(json_issues), "total": len(json_paths), "issues": json_issues},
            "privacy_scan": {
                "files": len(changed_text_paths),
                "classes": len(PRIVACY_PATTERNS),
                "confirmed_hits": privacy_hits,
            },
            "bounded_python_ast_security": {"files": len(python_paths), "findings": security_findings},
            "markdown": {
                "files": len(markdown_paths),
                "largest_words": max((row["words"] for row in markdown_word_counts), default=0),
                "over_cap": markdown_over_cap,
            },
            "manifests": manifests,
            "owner_files": len(owner_paths),
            "phase_files": len(phase_paths),
            "content_seal_mismatches": seal_mismatches,
            "lifecycle": {
                "phase_commits": phase_commits,
                "merges": len(merge_lines),
                "final_parents": len(parents),
                "ahead": ahead,
                "behind": behind,
                "local_upstream_tracking_fresh_live_equal": head == upstream == tracking == fresh_live,
                "clean_before": clean_before,
                "clean_after": clean_after,
            },
            "full_repository_suite_run": False,
            "same_owner_shared_infrastructure": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_receipt(output, receipt)
        return 0 if valid else 1
    except Exception as exc:  # keep the one-shot failure receipt privacy-safe
        write_receipt(
            output,
            {
                "schema": "ghc.family.sable.v672-v3.external-canonical.v1",
                "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
                "canonical_invocations": 1,
                "canonical_successes": 0,
                "failure_type": type(exc).__name__,
                "failure_detail": "canonical validator raised before a complete sanitized receipt",
                "postsuccess_replay_allowed": False,
            },
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
