#!/usr/bin/env python3
"""Shared implementation for the ten Lyren v666-v3 family-named runners."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v666_v3_runtime import (
    ALLOWED_OUTCOMES,
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    load_json,
    proposal_directories,
    replay_manifest,
    validate_contract,
)


def contracts() -> dict[str, Any]:
    failures = []
    paths = [path / "contract.json" for path in proposal_directories()]
    for path in paths:
        valid, errors = validate_contract(load_json(path))
        if not valid:
            failures.append({"path": path.relative_to(ROOT).as_posix(), "errors": errors})
    return {"runner": "contracts", "contract_count": len(paths), "failure_count": len(failures), "failures": failures, "valid": len(paths) == 20 and not failures}


def mutations() -> dict[str, Any]:
    rows = []
    for directory in proposal_directories():
        rows.extend(load_json(directory / "mutation-results.json")["mutations"])
    failures = [row["mutation_id"] for row in rows if not row["rejected"] or row["accepted"] or row["aggregate_credit"] != 0]
    return {"runner": "mutations", "mutation_count": len(rows), "rejected_count": sum(row["rejected"] for row in rows), "failure_count": len(failures), "failures": failures, "valid": len(rows) == 100 and not failures}


def json_runner() -> dict[str, Any]:
    failures, count = [], 0
    for path in sorted(PHASE_ROOT.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            count += 1
        except Exception as exc:  # exact failure retained by caller if reached
            failures.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    return {"runner": "json", "parsed_count": count, "failure_count": len(failures), "failures": failures, "valid": not failures}


def privacy() -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    candidates, scanned = [], 0
    for path in sorted(PHASE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
    return {"runner": "privacy", "classes": list(patterns), "file_count": scanned, "candidate_count": len(candidates), "confirmed_hit_count": len(candidates), "candidates": candidates, "valid": not candidates, "claim_boundary": "bounded five-class owner-file scan only; not privacy-complete"}


def security() -> dict[str, Any]:
    forbidden = ("eval", "exec", "compile", "os.system", "pickle.loads", "yaml.load")
    findings, scanned = [], 0
    for path in sorted((ROOT / "scripts").glob("*lyren_moss_v666_v3*.py")) + sorted((ROOT / "tests").glob("*lyren_moss_v666_v3*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        scanned += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    name = f"{node.func.value.id}.{node.func.attr}"
                if name in forbidden:
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "call": name})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "call": "shell=True"})
    return {"runner": "security", "python_file_count": scanned, "finding_count": len(findings), "findings": findings, "valid": not findings, "claim_boundary": "bounded changed-Python syntax scan only; not exhaustive security"}


def manifests() -> dict[str, Any]:
    result = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    return {"runner": "manifests", "manifests_replayed": 1, **result}


def accessibility() -> dict[str, Any]:
    path = PHASE_ROOT / "reports" / "static-report.html"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    checks = {
        "html_lang": bool(re.search(r"<html[^>]+lang=", text, re.I)),
        "main_landmark": "<main" in text.casefold(),
        "single_h1": len(re.findall(r"<h1\b", text, re.I)) == 1,
        "table_caption": "<caption" in text.casefold(),
        "scoped_headers": "scope=\"col\"" in text.casefold(),
        "status_region": "aria-live=\"polite\"" in text.casefold(),
        "no_color_only_legend": "text state" in text.casefold(),
    }
    return {"runner": "accessibility", "checks": checks, "passed": sum(checks.values()), "total": len(checks), "valid": all(checks.values()), "claim_boundary": "structural checks only; manual, assistive-technology, cognitive, Māori-language, and affected-user review reserved"}


def truth() -> dict[str, Any]:
    ledger = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    outcomes = [row["outcome"] for row in ledger["proposals"]]
    counts = {label: outcomes.count(label) for label in sorted(ALLOWED_OUTCOMES)}
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    unknown = sorted(set(outcomes) - ALLOWED_OUTCOMES)
    return {"runner": "truth", "outcome_counts": counts, "unknown_labels": unknown, "terminal_verdict": ledger["terminal_verdict"], "valid": counts == expected and not unknown and ledger["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"}


def closeout() -> dict[str, Any]:
    required = ["closeout/phase-truth.json", "closeout/retained-negative-register.json", "closeout/exact-open-gate-register.json", "seal/seal-candidate.json", "final/final-validation-prerequisites.json"]
    missing = [path for path in required if not (PHASE_ROOT / path).exists()]
    return {"runner": "closeout", "required_count": len(required), "missing": missing, "valid": not missing, "terminal_only": True}


RUNNERS = {
    "contracts": contracts,
    "mutations": mutations,
    "json": json_runner,
    "privacy": privacy,
    "security": security,
    "manifests": manifests,
    "accessibility": accessibility,
    "truth": truth,
    "closeout": closeout,
}


def cli(name: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--probe"]:
        print(json.dumps({"runner": name, "interface": "available", "work_invoked": False, "valid": True}, sort_keys=True))
        return
    if sys.argv[1:]:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [--probe]")
    result = RUNNERS[name]()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)
