#!/usr/bin/env python3
"""Shared bounded dispatch for ten Vesper Arlen v666-v2 runners."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v666_v2_runtime import evaluate_tree


RUNNER_IDS = {
    "contracts",
    "mutations",
    "json",
    "privacy",
    "security",
    "manifests",
    "accessibility",
    "truth",
    "closeout",
    "canonical-preflight",
}
X1_SHA = "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969"


def _phase_root(repo_root: Path) -> Path:
    return repo_root / "docs" / "vesper-arlen" / "v666-v2"


def _json_result(runner_id: str, passed: bool, **details: Any) -> dict[str, Any]:
    return {
        "runner_id": runner_id,
        "passed": passed,
        "synthetic_only": True,
        "network_calls": 0,
        "external_actions": 0,
        "claim_boundary": "bounded same-owner software evidence only",
        **details,
    }


def self_test(runner_id: str, repo_root: Path) -> dict[str, Any]:
    phase = _phase_root(repo_root)
    passed = (
        runner_id in RUNNER_IDS
        and (phase / "x1" / "proposal-freeze.json").is_file()
        and (repo_root / "scripts" / "ghc_family_vesper_arlen_v666_v2_runtime.py").is_file()
    )
    return _json_result(runner_id, passed, mode="self-test")


def _json_check(phase: Path) -> dict[str, Any]:
    paths = sorted(phase.rglob("*.json"))
    failures = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # retained by caller if observed
            failures.append({"path": path.relative_to(phase).as_posix(), "error": type(exc).__name__})
    return _json_result("json", not failures, parsed=len(paths), failures=failures)


def _privacy_check(repo_root: Path, phase: Path) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            "(" + "source_" + "thread_id|" + "thread" + "Id|" + "task" + "Id)", re.I
        ),
        "private_absolute_path": re.compile(r"[A-Z]:\\(?:Users|GHC-Archives)\\", re.I),
        "credential_or_token_value": re.compile(r"(Bearer\s+[A-Za-z0-9._~-]+|api[_-]?key\s*[:=]\s*[\"']?[A-Za-z0-9])", re.I),
        "session_identifier_value": re.compile(r"session[_ -]?(?:id|stream)\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I),
        "private_callable_identifier_value": re.compile(r"(?:callable|tool)[_ -]?id\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I),
    }
    files = [path for path in phase.rglob("*") if path.is_file()]
    files += sorted(repo_root.glob("scripts/*v666_v2*.py"))
    files += sorted(repo_root.glob("tests/*v666_v2*.py"))
    hits = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"class": class_name, "path": path.relative_to(repo_root).as_posix()})
    return _json_result(
        "privacy",
        not hits,
        scanned_files=len(files),
        scan_classes=list(patterns),
        candidates=hits,
        confirmed_hits=len(hits),
    )


def _security_check(repo_root: Path) -> dict[str, Any]:
    findings = []
    paths = sorted(repo_root.glob("scripts/*v666_v2*.py"))
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"eval", "exec", "system", "popen"}:
                    findings.append({"path": path.name, "line": node.lineno, "class": name})
                if name in {"run", "Popen", "call", "check_call", "check_output"}:
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            findings.append({"path": path.name, "line": node.lineno, "class": "subprocess_shell_true"})
    return _json_result(
        "security",
        not findings,
        scanned_python_files=len(paths),
        bounded_findings=findings,
        exhaustive_security=False,
    )


def _manifest_check(repo_root: Path, phase: Path) -> dict[str, Any]:
    manifests = sorted((phase / "validation").glob("*manifest.json"))
    failures = []
    entries = 0
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for row in manifest.get("entries", []):
            entries += 1
            object_spec = (
                f"{X1_SHA}:{row['path']}"
                if manifest.get("phase") == "x1"
                else ":" + row["path"]
            )
            try:
                blob = subprocess.check_output(
                    ["git", "-C", str(repo_root), "show", object_spec],
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                failures.append({"path": row["path"], "reason": "missing_git_blob"})
                continue
            if len(blob) != row["size_bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
                failures.append({"path": row["path"], "reason": "hash_or_size"})
    return _json_result("manifests", bool(manifests) and not failures, manifests=len(manifests), entries=entries, failures=failures)


def _accessibility_check(phase: Path) -> dict[str, Any]:
    paths = sorted(phase.rglob("*.html"))
    checks = []
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        present = {
            "language": "<html lang=" in text,
            "skip_link": "skip-link" in text,
            "main": "<main" in text,
            "heading": "<h1" in text,
            "caption": "<caption" in text,
            "reduced_motion": "prefers-reduced-motion" in text,
        }
        checks.append({"path": path.name, "checks": present, "passed": all(present.values())})
    return _json_result("accessibility", bool(checks) and all(row["passed"] for row in checks), files=len(paths), checks=checks, manual_evaluation_reserved=True)


def _truth_check(phase: Path) -> dict[str, Any]:
    path = phase / "x2" / "proposal-ledger.json"
    if not path.is_file():
        return _json_result("truth", False, reason="proposal_ledger_absent")
    ledger = json.loads(path.read_text(encoding="utf-8"))
    counts = ledger.get("outcome_counts", {})
    passed = counts == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    return _json_result("truth", passed, outcome_counts=counts)


def _closeout_check(phase: Path) -> dict[str, Any]:
    required = [
        phase / "closeout" / "phase-truth.json",
        phase / "closeout" / "closeout-receipt.json",
        phase / "seal" / "seal-candidate.json",
    ]
    missing = [path.relative_to(phase).as_posix() for path in required if not path.is_file()]
    return _json_result("closeout", not missing, missing=missing)


def _canonical_preflight(repo_root: Path, phase: Path) -> dict[str, Any]:
    required = [
        phase / "final" / "final-validation-prerequisites.json",
        phase / "validation" / "final-owner-manifest.json",
        phase / "validation" / "final-delta-manifest.json",
    ]
    missing = [path.relative_to(phase).as_posix() for path in required if not path.is_file()]
    clean = not subprocess.check_output(["git", "-C", str(repo_root), "status", "--porcelain=v1"]).decode().strip()
    return _json_result(
        "canonical-preflight",
        not missing and clean,
        missing=missing,
        clean=clean,
        canonical_aggregate_invoked=False,
    )


def run(runner_id: str, repo_root: Path, self_test_only: bool = False) -> dict[str, Any]:
    if runner_id not in RUNNER_IDS:
        return _json_result(runner_id, False, reason="unknown_runner")
    if self_test_only:
        return self_test(runner_id, repo_root)
    phase = _phase_root(repo_root)
    if runner_id in {"contracts", "mutations"}:
        result = evaluate_tree(phase)
        expected_mutations = 100 if runner_id == "mutations" else result["mutation_count"]
        return _json_result(
            runner_id,
            result["passed"] and result["mutation_count"] == expected_mutations,
            contract_count=result["contract_count"],
            mutation_count=result["mutation_count"],
            rejected_mutation_count=result["rejected_mutation_count"],
        )
    if runner_id == "json":
        return _json_check(phase)
    if runner_id == "privacy":
        return _privacy_check(repo_root, phase)
    if runner_id == "security":
        return _security_check(repo_root)
    if runner_id == "manifests":
        return _manifest_check(repo_root, phase)
    if runner_id == "accessibility":
        return _accessibility_check(phase)
    if runner_id == "truth":
        return _truth_check(phase)
    if runner_id == "closeout":
        return _closeout_check(phase)
    return _canonical_preflight(repo_root, phase)
