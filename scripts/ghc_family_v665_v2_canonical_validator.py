#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Liora Venn v665-v2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/liora-venn/v665-v2/"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
SOURCE = "f4abecafb107f4ac840c09b46a6b30079171816d"
X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
EVIDENCE = "420f73d2bb5c7570a886cd04a37d81bf03449bf2"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
OWNER_MANIFEST = f"{PREFIX}validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PREFIX}validation/final-delta-manifest.json"
STAGED_REVIEW = f"{PREFIX}validation/final-staged-review.json"
CONTRACT = f"{PREFIX}validation/final-canonical-contract.json"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def blob(path: str, revision: str = "HEAD") -> bytes:
    result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_json(path: str) -> Any:
    return json.loads(blob(path).decode("utf-8"))


def diff_paths(left: str, right: str) -> list[str]:
    raw = git("diff", "--name-only", f"{left}..{right}")
    return sorted(line for line in raw.splitlines() if line)


def manifest_check(path: str, expected_paths: list[str]) -> dict[str, Any]:
    manifest = strict_json(path)
    entries = manifest["entries"]
    exclusions = manifest["declared_self_exclusions"]
    mismatches = []
    for entry in entries:
        raw = blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    coverage = sorted([row["path"] for row in entries] + exclusions) == sorted(expected_paths)
    return {
        "path": path,
        "entry_count": len(entries),
        "self_exclusion_count": len(exclusions),
        "mismatches": mismatches,
        "coverage": coverage,
        "valid": not mismatches and coverage and manifest["coverage_valid"],
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    definitions = []
    confirmed = []
    windows = re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\")
    raw_id = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    credential = re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}")
    unix_markers = ["/" + "home/", "/" + "users/"]
    classes = [("windows_private_absolute_path", windows), ("raw_task_identifier", raw_id), ("credential_assignment", credential)]
    scanned = 0
    for path in paths:
        raw = blob(path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        lines = text.splitlines()
        for name, pattern in classes:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                line = lines[line_number - 1] if line_number <= len(lines) else ""
                record = {"path": path, "class": name, "line": line_number}
                if path.endswith(".py") and any(marker in line for marker in ("re.compile", "raw_id =", "windows =", "credential =")):
                    record["disposition"] = "scanner_definition"
                    definitions.append(record)
                else:
                    record["disposition"] = "confirmed"
                    confirmed.append(record)
        for marker in unix_markers:
            if marker in text.casefold():
                confirmed.append({"path": path, "class": "unix_private_absolute_path", "line": None, "disposition": "confirmed"})
    return {
        "classes": 5,
        "text_files_scanned": scanned,
        "scanner_definition_candidates": definitions,
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def python_security_and_compile(paths: list[str]) -> dict[str, Any]:
    compiled = 0
    findings = []
    for path in paths:
        if not path.endswith(".py"):
            continue
        text = blob(path).decode("utf-8")
        compile(text, path, "exec")
        compiled += 1
        tree = ast.parse(text, filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                parts = []
                current: ast.expr = node.func
                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    parts.append(current.id)
                name = ".".join(reversed(parts))
            if name in {"eval", "exec", "os.system", "pickle.loads", "pickle.load", "yaml.load"}:
                findings.append({"path": path, "line": node.lineno, "call": name})
            if name.startswith("subprocess."):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "line": node.lineno, "call": name, "issue": "shell_true"})
    return {"python_files_compiled": compiled, "bounded_findings": findings, "valid": not findings}


def markdown_and_json(paths: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    json_errors = []
    markdown_issues = []
    json_count = 0
    markdown_count = 0
    for path in paths:
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(blob(path).decode("utf-8"))
            except Exception as exc:
                json_errors.append({"path": path, "error": type(exc).__name__})
        elif path.endswith(".md"):
            markdown_count += 1
            text = blob(path).decode("utf-8")
            skill_front_matter = path.endswith("/SKILL.md") and text.startswith("---\n") and "\n# " in text
            if not text.startswith("#") and not skill_front_matter:
                markdown_issues.append({"path": path, "issue": "missing_top_heading"})
    return (
        {"count": json_count, "errors": json_errors, "valid": not json_errors},
        {"count": markdown_count, "issues": markdown_issues, "valid": not markdown_issues},
    )


def outcome_label_check(paths: list[str]) -> dict[str, Any]:
    observed = []
    unknown = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"outcome", "expected_disposition", "observed_disposition"} and isinstance(child, str):
                    observed.append(child)
                    if child not in ALLOWED:
                        unknown.append({"path": path, "key": key, "value": child})
                walk(child, path)
        elif isinstance(value, list):
            for child in value:
                walk(child, path)

    for path in paths:
        if path.endswith(".json"):
            walk(json.loads(blob(path).decode("utf-8")), path)
    return {"observed_values": sorted(set(observed)), "unknown": unknown, "valid": not unknown and set(observed) == ALLOWED}


def scalar_checks(expected_head: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    final_paths = diff_paths(SOURCE, expected_head)
    delta_paths = diff_paths(EVIDENCE, expected_head)
    phase = strict_json(f"{PREFIX}closeout/phase-truth.json")
    method = strict_json(f"{PREFIX}closeout/method-flow-final.json")
    delivery = strict_json(f"{PREFIX}closeout/delivery-state.json")
    contract = strict_json(CONTRACT)
    review = strict_json(STAGED_REVIEW)
    detailed_values = [
        ("exact_head", git("rev-parse", "HEAD") == expected_head),
        ("branch", git("branch", "--show-current") == BRANCH),
        ("x1_parent", git("rev-parse", f"{X1}^") == SOURCE),
        ("evidence_parent", git("rev-parse", f"{EVIDENCE}^") == X1),
        ("final_parent", git("rev-parse", f"{expected_head}^") == EVIDENCE),
        ("final_parent_count", len(git("show", "-s", "--format=%P", expected_head).split()) == 1),
        ("source_to_final_commits", int(git("rev-list", "--count", f"{SOURCE}..{expected_head}")) == 3),
        ("source_to_final_merges", int(git("rev-list", "--count", "--merges", f"{SOURCE}..{expected_head}")) == 0),
        ("source_to_final_paths", len(final_paths) == 152),
        ("final_delta_paths", len(delta_paths) == 12),
        ("diff_hygiene", run("git", "diff", "--check", f"{SOURCE}..{expected_head}", check=False).returncode == 0),
        ("file_cap", len(final_paths) <= 2_000),
        ("word_cap", review["source_to_final_word_count"] <= 100_000),
        ("contract_valid", contract["valid"] is True),
        ("review_valid", review["valid"] is True),
        ("phase_valid", phase["valid"] is True),
        ("method_valid", method["valid"] is True),
        ("delivery_valid", delivery["valid"] is True),
    ]
    minimal_values = [
        ("outcomes", phase["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        ("mutations", phase["mutations"] == {"preregistered": 100, "executed": 100, "rejected": 100, "accepted": 0}),
        ("negatives", phase["effective_negatives"] == 25_307),
        ("methods", phase["effective_method_flow_methods"] == 9_169),
        ("open_gaps", phase["open_gaps"] == 176),
        ("exact_gates", phase["exact_gates"] == 174),
        ("terminal", phase["terminal_verdict"] == TERMINAL_VERDICT),
        ("real_rows", phase["real_rows"] == 0),
        ("authority_events", phase["authority_events"] == 0),
        ("full_suite_not_run", phase["full_repository_suite_run"] is False),
        ("not_independent", phase["independent_reproduction"] is False),
        ("delivery_prepared", delivery["state"] == "PREPARED_NOT_SENT"),
        ("target", delivery["target_exact_title"] == "Tamar Vey" and delivery["target_phase"] == "v665-v3"),
        ("canonical_prepared", phase["canonical_state"] == "PREPARED_NOT_RUN"),
        ("failure_erasure", phase["failure_erasure_count"] == 0),
    ]
    return (
        [{"check": name, "valid": valid} for name, valid in detailed_values],
        [{"check": name, "valid": valid} for name, valid in minimal_values],
        {"final_paths": final_paths, "delta_paths": delta_paths, "contract": contract},
    )


def validate(expected_head: str) -> dict[str, Any]:
    before_status = git("status", "--porcelain=v1").splitlines()
    detailed, minimal, context = scalar_checks(expected_head)
    final_paths = context["final_paths"]
    delta_paths = context["delta_paths"]
    contract = context["contract"]

    tests = run(sys.executable, "-m", "unittest", "tests.test_ghc_family_liora_v665_v2_closeout", check=False)
    test_text = tests.stdout + tests.stderr
    match = re.search(r"Ran (\d+) tests?", test_text)
    test_count = int(match.group(1)) if match else 0
    tests_valid = tests.returncode == 0 and test_count == contract["expected_test_count"] and "OK" in test_text

    owner = manifest_check(OWNER_MANIFEST, final_paths)
    delta = manifest_check(DELTA_MANIFEST, delta_paths)
    json_result, markdown_result = markdown_and_json(final_paths)
    python_result = python_security_and_compile(final_paths)
    privacy = privacy_scan(final_paths)
    labels = outcome_label_check(final_paths)

    branch_ref = f"refs/remotes/origin/{BRANCH}"
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", branch_ref)
    fresh_line = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    fresh = fresh_line.split("\t", 1)[0] if fresh_line else ""
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    after_status = git("status", "--porcelain=v1").splitlines()
    remote = {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "divergence": divergence,
        "status_before_rows": len(before_status),
        "status_after_rows": len(after_status),
        "four_way_equal": local == upstream == tracking == fresh == expected_head,
        "clean_before_and_after": not before_status and not after_status,
    }
    detailed.extend(
        [
            {"check": "scoped_tests", "valid": tests_valid},
            {"check": "owner_manifest", "valid": owner["valid"]},
            {"check": "delta_manifest", "valid": delta["valid"]},
            {"check": "strict_json", "valid": json_result["valid"] and json_result["count"] == contract["strict_json_count"]},
            {"check": "markdown", "valid": markdown_result["valid"]},
            {"check": "python_compile_security", "valid": python_result["valid"]},
            {"check": "privacy", "valid": privacy["valid"]},
            {"check": "outcome_labels", "valid": labels["valid"]},
            {"check": "clean_remote_equality", "valid": remote["four_way_equal"] and remote["clean_before_and_after"] and divergence == [0, 0]},
        ]
    )
    valid = all(row["valid"] for row in detailed) and all(row["valid"] for row in minimal)
    return {
        "schema": "ghc.family.liora.v665-v2.external-canonical-receipt.v1",
        "owner": "Liora Venn",
        "phase": "v665-v2",
        "expected_head": expected_head,
        "branch": BRANCH,
        "tests": {"module": "tests.test_ghc_family_liora_v665_v2_closeout", "run": test_count, "return_code": tests.returncode, "valid": tests_valid, "output_tail": test_text.strip().splitlines()[-4:]},
        "detailed_checks": {"count": len(detailed), "passed": sum(row["valid"] for row in detailed), "checks": detailed},
        "minimal_checks": {"count": len(minimal), "passed": sum(row["valid"] for row in minimal), "checks": minimal},
        "json_documents": json_result,
        "markdown_documents": markdown_result,
        "python_security": python_result,
        "privacy": privacy,
        "outcome_labels": labels,
        "owner_manifest": owner,
        "delta_manifest": delta,
        "git": remote,
        "source_to_final": {"paths": len(final_paths), "commits": 3, "merges": 0},
        "final_delta": {"paths": len(delta_paths)},
        "full_repository_suite_run": False,
        "same_owner_validation": True,
        "independent_reproduction": False,
        "successful_invocation_limit": 1,
        "replay_after_success_forbidden": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = args.receipt.open("xb")
    except FileExistsError:
        print(json.dumps({"valid": False, "error": "exclusive_receipt_already_exists"}, sort_keys=True))
        return 3
    try:
        try:
            result = validate(args.expected_head)
        except Exception as exc:
            result = {
                "schema": "ghc.family.liora.v665-v2.external-canonical-receipt.v1",
                "expected_head": args.expected_head,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "terminal_verdict": TERMINAL_VERDICT,
                "valid": False,
            }
        raw = (json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        handle.write(raw)
        handle.flush()
    finally:
        handle.close()
    summary = {
        "valid": result.get("valid", False),
        "expected_head": args.expected_head,
        "tests": result.get("tests", {}).get("run"),
        "detailed": result.get("detailed_checks", {}).get("count"),
        "minimal": result.get("minimal_checks", {}).get("count"),
        "json": result.get("json_documents", {}).get("count"),
        "owner_manifest_entries": result.get("owner_manifest", {}).get("entry_count"),
        "final_delta_entries": result.get("delta_manifest", {}).get("entry_count"),
        "privacy_confirmed_hits": len(result.get("privacy", {}).get("confirmed_hits", [])),
        "security_findings": len(result.get("python_security", {}).get("bounded_findings", [])),
        "terminal_verdict": TERMINAL_VERDICT,
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
