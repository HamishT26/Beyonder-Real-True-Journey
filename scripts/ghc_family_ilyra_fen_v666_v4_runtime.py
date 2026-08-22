#!/usr/bin/env python3
"""Shared bounded runtime for Ilyra Fen v666-v4 owner-local evidence."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v666-v4"
X1_SHA = "7926a46fa309f180cb996dacbea7ae849a3cf507"
SOURCE_SHA = "764d3bdfb199e91a5574a904a99ff4e95825fed9"
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")

REQUIRED_CONTRACT_KEYS = {
    "schema", "proposal_id", "title", "expected_disposition", "outcome",
    "synthetic_fixture", "real_data_rows", "network_calls", "external_actions",
    "positive_fixture", "invariant", "source_needs", "stop_conditions",
    "protected_gates", "claim_boundary",
}

PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
    "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
    "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
    "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_contract(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CONTRACT_KEYS - set(contract))
    extra = sorted(set(contract) - REQUIRED_CONTRACT_KEYS)
    if missing:
        errors.append("missing:" + ",".join(missing))
    if extra:
        errors.append("extra:" + ",".join(extra))
    if contract.get("expected_disposition") not in ALLOWED_LABELS:
        errors.append("invalid_expected_disposition")
    if contract.get("outcome") != contract.get("expected_disposition"):
        errors.append("outcome_drift")
    if contract.get("synthetic_fixture") is not True:
        errors.append("not_synthetic")
    for key in ("real_data_rows", "network_calls", "external_actions"):
        if type(contract.get(key)) is not int or contract.get(key) != 0:
            errors.append(f"nonzero_or_invalid_{key}")
    fixture = contract.get("positive_fixture")
    if not isinstance(fixture, dict):
        errors.append("invalid_positive_fixture")
    else:
        if fixture.get("authority_state") != "withheld":
            errors.append("authority_not_withheld")
        if fixture.get("provenance_state") != "declared_owner_local_lineage":
            errors.append("provenance_not_declared")
        if fixture.get("uncertainty_state") != "explicit_unknown_or_bounded_placeholder":
            errors.append("uncertainty_not_bounded")
    if not isinstance(contract.get("protected_gates"), list) or len(contract.get("protected_gates", [])) < 10:
        errors.append("protected_gates_incomplete")
    if not isinstance(contract.get("stop_conditions"), list) or len(contract.get("stop_conditions", [])) < 5:
        errors.append("stop_conditions_incomplete")
    boundary = str(contract.get("claim_boundary", "")).casefold()
    if "not empirical" not in boundary or "not authority" not in boundary:
        errors.append("claim_boundary_incomplete")
    if any(term in boundary for term in ("stage 20 authorized", "production approved", "authority granted")):
        errors.append("prohibited_promotion")
    return not errors, errors


def mutations_for(contract: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[tuple[str, str, dict[str, Any]]] = []
    missing = deepcopy(contract)
    missing.pop("invariant", None)
    cases.append(("missing_required_field", "M01", missing))
    wrong_type = deepcopy(contract)
    wrong_type["real_data_rows"] = "0"
    cases.append(("wrong_type_or_invalid_range", "M02", wrong_type))
    authority = deepcopy(contract)
    authority["positive_fixture"]["authority_state"] = "granted"
    cases.append(("provenance_or_authority_smuggling", "M03", authority))
    real_action = deepcopy(contract)
    real_action["external_actions"] = 1
    cases.append(("real_world_or_production_action", "M04", real_action))
    promotion = deepcopy(contract)
    promotion["outcome"] = "deployed"
    cases.append(("outcome_or_conformance_promotion", "M05", promotion))
    rows = []
    for class_name, suffix, candidate in cases:
        valid, errors = validate_contract(candidate)
        rows.append({
            "mutation_id": f"{contract['proposal_id']}-{suffix}",
            "class": class_name,
            "rejected": not valid,
            "validator_errors": errors,
            "aggregate_credit": 0,
        })
    return rows


def proposal_directories() -> list[Path]:
    return sorted((PHASE_ROOT / "x2" / "proposals").glob("ily6664-n*"))


def text_files(root: Path = PHASE_ROOT) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.casefold() in {".json", ".md", ".html", ".txt", ".py"})


def scan_privacy(paths: Iterable[Path]) -> dict[str, Any]:
    candidates = []
    scanned = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
    return {
        "scanned_file_count": scanned,
        "classes": list(PRIVACY_PATTERNS),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(candidates),
        "candidates": candidates,
        "valid": not candidates,
        "claim_boundary": "five-class bounded pattern scan only; not privacy-complete or exhaustive security",
    }


def changed_python_files() -> list[Path]:
    candidates = sorted((ROOT / "scripts").glob("*ilyra_fen_v666_v4*.py")) + sorted((ROOT / "tests").glob("*ilyra_fen_v666_v4*.py"))
    return sorted({path.resolve() for path in candidates if path.is_file()})


def scan_python_security(paths: Iterable[Path]) -> dict[str, Any]:
    findings = []
    scanned = 0
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        scanned += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"eval", "exec"}:
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "class": f"dynamic_{name}"})
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "class": "shell_true"})
    return {
        "scanned_python_count": scanned,
        "finding_count": len(findings),
        "findings": findings,
        "valid": not findings,
        "claim_boundary": "bounded changed-Python AST scan only; not exhaustive security, penetration testing, or supply-chain assurance",
    }


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{path}"])


def replay_manifest(manifest_path: Path, commit: str) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    failures = []
    for entry in manifest["entries"]:
        try:
            blob = git_blob(commit, entry["path"])
            line = subprocess.check_output(["git", "-C", str(ROOT), "ls-tree", commit, "--", entry["path"]], text=True).strip()
        except subprocess.CalledProcessError as exc:
            failures.append({"path": entry["path"], "failure": f"missing_blob:{exc.returncode}"})
            continue
        parts = line.split(None, 3)
        if (
            hashlib.sha256(blob).hexdigest() != entry["sha256"]
            or len(blob) != entry["size_bytes"]
            or len(parts) < 3
            or parts[0] != entry["git_mode"]
            or parts[2] != entry["git_blob_oid"]
        ):
            failures.append({"path": entry["path"], "failure": "sha_size_mode_or_oid_mismatch"})
    return {"entry_count": len(manifest["entries"]), "failure_count": len(failures), "failures": failures, "valid": not failures}


def emit(value: Any) -> None:
    sys_stdout = getattr(__import__("sys"), "stdout")
    if hasattr(sys_stdout, "reconfigure"):
        sys_stdout.reconfigure(encoding="utf-8", errors="strict")
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
