#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Orin v668-v7."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/orin-thale/v668-v7/"
BRANCH = "codex/GHC-Family/orin-thale-v668-v7-full-tools"
SOURCE = "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"
X1 = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
EVIDENCE = "64e5b3f995061e3f7c547a0759e2a5a111dfdbbc"
OWNER_MANIFEST = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
X1_MANIFEST = f"{PHASE_PREFIX}x1/x1-manifest.json"
X2_MANIFEST = f"{PHASE_PREFIX}x2/evidence/evidence-content-manifest.json"
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".py", ".yaml", ".yml"}


def run_git(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check, timeout=timeout)


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8").strip()


def commit_bytes(commit: str, path: str) -> bytes:
    return run_git("cat-file", "blob", f"{commit}:{path}").stdout


def commit_json(commit: str, path: str) -> Any:
    return json.loads(commit_bytes(commit, path))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = commit_json(commit, path)
    mismatches = []
    for row in manifest["entries"]:
        data = commit_bytes(commit, row["path"])
        observed = {
            "git_blob_oid": git_text("rev-parse", f"{commit}:{row['path']}"),
            "sha256": sha256(data),
            "bytes": len(data),
        }
        expected = {key: row[key] for key in observed}
        if observed != expected:
            mismatches.append(row["path"])
    return {
        "path": path,
        "entries": len(manifest["entries"]),
        "self_exclusions": len(manifest.get("self_exclusions", [])),
        "coverage_count": manifest.get("coverage_count", len(manifest["entries"]) + len(manifest.get("self_exclusions", []))),
        "mismatch_count": len(mismatches),
        "mismatch_sample": mismatches[:10],
    }


def owner_paths(expected_head: str) -> list[str]:
    manifest = commit_json(expected_head, OWNER_MANIFEST)
    return sorted({row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"]))


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "credential_assignment": re.compile(
            rb"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{12,}"
        ),
        "delegation_markup": re.compile(rb"(?i)<codex_delegation>|source_thread_id\s*[:=]"),
        "private_local_path": re.compile(rb"(?i)\b[A-Z]:\\Users\\[^\s\"']+"),
        "private_uri": re.compile(rb"(?i)\b(?:codex|file|app)://[^\s\"']+"),
        "raw_uuid": re.compile(rb"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    }


def scanner_definition_lines(path: str, text: str) -> set[int]:
    allowed: set[int] = set()
    if path == "scripts/build_ghc_family_orin_thale_v668_v7_x1.py":
        for number, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("forbidden = ("):
                allowed.add(number)
    if path in {
        "tests/test_ghc_family_orin_thale_v668_v7_x2.py",
        "tests/test_ghc_family_orin_thale_v668_v7_final.py",
    }:
        for number, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("re.compile("):
                allowed.add(number)
    if path == "scripts/ghc_family_orin_thale_v668_v7_canonical.py":
        tree = ast.parse(text, filename=path)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == "privacy_patterns":
                allowed.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    return allowed


def scan_owner(expected_head: str, paths: list[str]) -> dict[str, Any]:
    patterns = privacy_patterns()
    raw = []
    definitions = []
    confirmed = []
    stale = []
    security = []
    strict_json = 0
    markdown = 0
    html_count = 0
    yaml_count = 0
    python_count = 0
    oversized = []
    maximum_words = 0
    stale_patterns = {
        "stale_orin": re.compile(r"(?i)\bOrin(?:\s+Thale)?\s+v(?!668-v7\b)\d{3}-v[1-8]\b"),
        "stale_liora": re.compile(r"(?i)\bLiora(?:\s+Venn)?\s+v(?!668-v8\b)\d{3}-v[1-8]\b"),
    }
    for path in paths:
        suffix = pathlib.PurePosixPath(path).suffix.lower()
        if suffix not in TEXT_SUFFIXES:
            continue
        data = commit_bytes(expected_head, path)
        text = data.decode("utf-8")
        if suffix == ".json":
            json.loads(text)
            strict_json += 1
        elif suffix == ".md":
            markdown += 1
        elif suffix == ".html":
            html_count += 1
        elif suffix in {".yaml", ".yml"}:
            yaml_count += 1
        elif suffix == ".py":
            python_count += 1
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "line": node.lineno, "kind": node.func.id})
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            security.append({"path": path, "line": node.lineno, "kind": "explicit_shell_true"})
        words = len(re.findall(r"\b\w+[\w'-]*\b", text))
        maximum_words = max(maximum_words, words)
        if suffix in {".json", ".md", ".txt", ".html", ".yaml", ".yml"} and words > 6000:
            oversized.append({"path": path, "words": words})
        allowed_definition_lines = scanner_definition_lines(path, text)
        for line_number, line in enumerate(text.splitlines(), 1):
            encoded = line.encode("utf-8")
            for class_id, pattern in patterns.items():
                if pattern.search(encoded):
                    candidate = {"path": path, "line": line_number, "class": class_id}
                    raw.append(candidate)
                    if line_number in allowed_definition_lines:
                        definitions.append(candidate)
                    else:
                        confirmed.append(candidate)
            for class_id, pattern in stale_patterns.items():
                match = pattern.search(line)
                if match:
                    stale.append({"path": path, "line": line_number, "class": class_id, "label": match.group(0)})
    return {
        "files": len(paths),
        "strict_json_parses": strict_json,
        "markdown_checks": markdown,
        "html_checks": html_count,
        "yaml_checks": yaml_count,
        "python_ast_checks": python_count,
        "raw_privacy_candidates": len(raw),
        "scanner_definition_candidates": len(definitions),
        "confirmed_privacy_hits": len(confirmed),
        "privacy_candidate_sample": raw[:10],
        "security_findings": len(security),
        "security_sample": security[:10],
        "stale_labels": len(stale),
        "stale_sample": stale[:10],
        "oversized_documents": len(oversized),
        "oversized_sample": oversized[:10],
        "maximum_document_words": maximum_words,
    }


def run_tests() -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_orin_thale_v668_v7_x1",
        "tests.test_ghc_family_orin_thale_v668_v7_x2",
        "tests.test_ghc_family_orin_thale_v668_v7_final",
    ]
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", *modules],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    combined = result.stdout + "\n" + result.stderr
    ran = re.search(r"Ran (\d+) tests", combined)
    terminal = "OK" if re.search(r"\nOK\s*$", combined) else "FAILED"
    return {
        "modules": modules,
        "return_code": result.returncode,
        "tests_run": int(ran.group(1)) if ran else None,
        "terminal": terminal,
        "expected_tests": 51,
    }


def validate(expected_head: str) -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_lines = run_git("ls-remote", "--heads", "origin", BRANCH).stdout.decode("utf-8").splitlines()
    live = live_lines[0].split()[0] if len(live_lines) == 1 else None
    parents = [value for value in git_text("show", "-s", "--format=%P", expected_head).split() if value]
    phase_commits = int(git_text("rev-list", "--count", f"{SOURCE}..{expected_head}"))
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{expected_head}").splitlines() if line]
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    porcelain = run_git("status", "--porcelain=v1").stdout
    manifests = {
        "x1": replay_manifest(X1, X1_MANIFEST),
        "x2": replay_manifest(EVIDENCE, X2_MANIFEST),
        "final_owner": replay_manifest(expected_head, OWNER_MANIFEST),
        "final_delta": replay_manifest(expected_head, DELTA_MANIFEST),
    }
    paths = owner_paths(expected_head)
    scan = scan_owner(expected_head, paths)
    route = commit_json(expected_head, f"{PHASE_PREFIX}route/terminal-route-state.json")
    truth = commit_json(expected_head, f"{PHASE_PREFIX}closeout/phase-truth.json")
    tests = run_tests()
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    checks = {
        "exact_branch": branch == BRANCH,
        "exact_head": local == expected_head,
        "local_upstream_tracking_live_equal": local == upstream == tracking == live,
        "typed_zero_divergence": divergence == ["0", "0"],
        "clean_before_and_after": not porcelain,
        "final_single_parent": len(parents) == 1 and parents[0] == EVIDENCE,
        "source_x1_evidence_ancestry": git_text("rev-parse", f"{X1}^") == SOURCE and git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": not merges,
        "all_manifest_replays": all(row["mismatch_count"] == 0 for row in manifests.values()),
        "owner_manifest_coverage": manifests["final_owner"]["coverage_count"] == manifests["final_owner"]["entries"] + 3,
        "delta_manifest_coverage": manifests["final_delta"]["coverage_count"] == manifests["final_delta"]["entries"] + 3,
        "strict_json": scan["strict_json_parses"] > 0,
        "document_ceiling": scan["oversized_documents"] == 0,
        "zero_confirmed_privacy_hits": scan["confirmed_privacy_hits"] == 0,
        "zero_bounded_security_findings": scan["security_findings"] == 0,
        "zero_stale_labels": scan["stale_labels"] == 0,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and route["successor_title"] == "Liora Venn" and route["successor_phase"] == "v668-v8",
        "truth_labels_and_verdict": truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2} and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "owner_scoped_tests": tests["return_code"] == 0 and tests["terminal"] == "OK" and tests["tests_run"] == tests["expected_tests"],
        "materialized_file_ceiling": materialized < 2000,
        "full_repository_suite_not_run": True,
    }
    return {
        "schema": "ghc.family.orin-thale.v668-v7.exact-final-canonical.v1",
        "status": "PASS_EXACT_FINAL_OWNER_CANONICAL_ONCE" if all(checks.values()) else "FAIL_EXACT_FINAL_OWNER_CANONICAL_ZERO_SUCCESS_CREDIT",
        "phase": "v668-v7",
        "owner": "Orin Thale",
        "expected_head": expected_head,
        "checks": checks,
        "check_count": len(checks),
        "passed_checks": sum(checks.values()),
        "manifests": manifests,
        "scan": scan,
        "tests": tests,
        "history": {"phase_commits": phase_commits, "merges": len(merges), "final_parents": parents},
        "remote": {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence, "clean": not porcelain},
        "materialized_files": materialized,
        "full_repository_suite": "not_run_non_Eiren_owner_scope",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Bounded same-owner software validation under shared infrastructure only; not external audit, independent reproduction, empirical confirmation, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal or cultural authority, Maori-authority review, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.expected_head)
    except Exception as error:  # fail closed while keeping private path details out of the receipt
        result = {
            "schema": "ghc.family.orin-thale.v668-v7.exact-final-canonical.v1",
            "status": "ERROR_EXACT_FINAL_OWNER_CANONICAL_ZERO_SUCCESS_CREDIT",
            "phase": "v668-v7",
            "owner": "Orin Thale",
            "expected_head": args.expected_head,
            "error_class": type(error).__name__,
            "error": "canonical validation raised before complete result; inspect the attributable process locally",
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": result["status"],
        "receipt_sha256": sha256(payload.encode("utf-8")),
        "passed_checks": result.get("passed_checks"),
        "check_count": result.get("check_count"),
        "tests_run": (result.get("tests") or {}).get("tests_run"),
        "strict_json_parses": (result.get("scan") or {}).get("strict_json_parses"),
        "owner_files": (result.get("scan") or {}).get("files"),
        "confirmed_privacy_hits": (result.get("scan") or {}).get("confirmed_privacy_hits"),
    }, sort_keys=True))
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
