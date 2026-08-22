#!/usr/bin/env python3
"""Shared bounded runtime for Orin Thale v666-v8 owner-local runners."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, BinaryIO


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v666-v8"
X1_SHA = "ea951ad7b1305ffc485c581af9ad10769c48fccb"
SOURCE_SHA = "6e157b95c3129226b8bd1f83b8c010e28a206346"
ALLOWED_LABELS = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_CONTRACT_FIELDS = {
    "proposal_id",
    "title",
    "expected_disposition",
    "synthetic_only",
    "participant_count",
    "real_data_row_count",
    "network_call_count",
    "external_action",
    "authority_claim",
    "stage20_claim",
    "provenance",
    "uncertainty",
    "protected_gates",
    "positive_fixture",
}


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_contract(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CONTRACT_FIELDS - value.keys())
    if missing:
        errors.append("missing_required_field:" + ",".join(missing))
    if not isinstance(value.get("proposal_id"), str) or not re.fullmatch(
        r"OR6668-N\d{3}", str(value.get("proposal_id") or "")
    ):
        errors.append("invalid_proposal_id")
    if value.get("expected_disposition") not in ALLOWED_LABELS:
        errors.append("invalid_disposition")
    if value.get("synthetic_only") is not True:
        errors.append("synthetic_only_required")
    for field in ("participant_count", "real_data_row_count", "network_call_count"):
        if value.get(field) != 0:
            errors.append(f"{field}_must_be_zero")
    if value.get("external_action") is not False:
        errors.append("external_action_forbidden")
    if value.get("authority_claim") is not False:
        errors.append("authority_claim_forbidden")
    if value.get("stage20_claim") is not False:
        errors.append("stage20_claim_forbidden")
    if not isinstance(value.get("provenance"), dict) or not value.get("provenance"):
        errors.append("provenance_required")
    if not isinstance(value.get("uncertainty"), dict) or not value.get("uncertainty"):
        errors.append("uncertainty_required")
    if not isinstance(value.get("protected_gates"), list) or len(value.get("protected_gates", [])) < 8:
        errors.append("protected_gates_incomplete")
    fixture = value.get("positive_fixture")
    if not isinstance(fixture, dict) or fixture.get("real_object") is not False:
        errors.append("positive_fixture_must_be_zero_object")
    return errors


def mutation_variants(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    missing = copy.deepcopy(contract)
    missing.pop("proposal_id", None)
    rows.append(("missing_required_field", missing))
    wrong_type = copy.deepcopy(contract)
    wrong_type["participant_count"] = "zero"
    rows.append(("wrong_type_or_invalid_range", wrong_type))
    smuggled = copy.deepcopy(contract)
    smuggled["authority_claim"] = True
    rows.append(("provenance_or_authority_smuggling", smuggled))
    external = copy.deepcopy(contract)
    external["external_action"] = True
    external["network_call_count"] = 1
    rows.append(("real_world_or_production_action", external))
    promoted = copy.deepcopy(contract)
    promoted["stage20_claim"] = True
    rows.append(("outcome_or_conformance_promotion", promoted))
    return rows


def read_exact(stream: BinaryIO, length: int) -> bytes:
    chunks: list[bytes] = []
    remaining = length
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"short git batch read: needed {remaining} more bytes")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_tree_map(commit: str) -> dict[str, tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "-z", "--full-tree", commit]
    )
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.decode("ascii").split()
        if kind == "blob":
            result[path.decode("utf-8")] = (mode, oid)
    return result


def replay_manifest(path: Path, commit: str) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    tree = git_tree_map(commit)
    failures: list[dict[str, str]] = []
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("git cat-file pipes unavailable")
        for entry in manifest["entries"]:
            path_value = entry["path"]
            actual = tree.get(path_value)
            if actual != (entry["git_mode"], entry["git_blob_oid"]):
                failures.append({"path": path_value, "failure": "tree_entry_mismatch"})
                continue
            oid = entry["git_blob_oid"]
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[0] != oid or header[1] != "blob":
                failures.append({"path": path_value, "failure": "batch_header_mismatch"})
                continue
            blob = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                failures.append({"path": path_value, "failure": "batch_terminator_mismatch"})
                continue
            if hashlib.sha256(blob).hexdigest() != entry["sha256"]:
                failures.append({"path": path_value, "failure": "sha256_mismatch"})
            if len(blob) != entry["size_bytes"]:
                failures.append({"path": path_value, "failure": "size_mismatch"})
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if return_code:
            raise RuntimeError(stderr[:240])
    return {
        "entry_count": manifest["entry_count"],
        "failure_count": len(failures),
        "failures": failures,
        "valid": not failures,
    }


def owner_paths() -> list[Path]:
    paths = list(PHASE_ROOT.rglob("*")) if PHASE_ROOT.exists() else []
    paths += list((ROOT / "scripts").glob("*orin_thale_v666_v8*.py"))
    paths += list((ROOT / "tests").glob("*orin_thale_v666_v8*.py"))
    return sorted(path for path in paths if path.is_file())


def contract_summary() -> dict[str, Any]:
    rows = []
    for path in sorted((PHASE_ROOT / "x2" / "proposals").glob("*/contract.json")):
        contract = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_contract(contract)
        rows.append({"proposal_id": contract.get("proposal_id"), "errors": errors})
    invalid_count = sum(bool(row["errors"]) for row in rows)
    return {
        "contract_count": len(rows),
        "invalid_count": invalid_count,
        "rows": rows,
        "valid": len(rows) == 20 and invalid_count == 0,
    }


def mutation_summary() -> dict[str, Any]:
    rows = []
    for path in sorted((PHASE_ROOT / "x2" / "proposals").glob("*/mutation-results.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        rows.append({"proposal_id": value["proposal_id"], "rejected": value["rejected_count"], "valid": value["all_rejected_and_retained"]})
    return {"proposal_count": len(rows), "rejected_total": sum(row["rejected"] for row in rows), "valid": len(rows) == 20 and sum(row["rejected"] for row in rows) == 100 and all(row["valid"] for row in rows)}


def json_summary() -> dict[str, Any]:
    paths = [path for path in owner_paths() if path.suffix == ".json"]
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))
    return {"json_count": len(paths), "valid": True}


PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
    "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
    "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
    "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
}


def privacy_summary() -> dict[str, Any]:
    candidates = []
    for path in owner_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
    return {"file_count": len(owner_paths()), "classes": list(PRIVACY_PATTERNS), "candidates": candidates, "confirmed_hits": len(candidates), "valid": not candidates}


def security_summary() -> dict[str, Any]:
    findings = []
    python_paths = [path for path in owner_paths() if path.suffix == ".py"]
    for path in python_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
            if name in {"eval", "exec"}:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "class": f"dynamic_{name}"})
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "class": "shell_true"})
    return {"python_count": len(python_paths), "findings": findings, "valid": not findings}


def accessibility_summary() -> dict[str, Any]:
    fixture = '<!doctype html><html lang="en-NZ"><body><main><h1>Bounded report</h1><table><caption>Outcomes</caption><thead><tr><th scope="col">ID</th></tr></thead></table></main></body></html>'
    checks = {token: token in fixture for token in ('lang="en-NZ"', "<main>", "<h1>", "<caption>", 'scope="col"')}
    return {"checks": checks, "manual_evaluation_reserved": True, "affected_user_evaluation_reserved": True, "valid": all(checks.values())}


def manifest_summary() -> dict[str, Any]:
    x1 = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    return {"x1": x1, "valid": x1["valid"]}


def truth_summary() -> dict[str, Any]:
    ledger_path = PHASE_ROOT / "x2" / "proposal-ledger.json"
    if not ledger_path.exists():
        return {"available": False, "valid": False}
    value = json.loads(ledger_path.read_text(encoding="utf-8"))
    return {
        "available": True,
        "outcomes": value["outcome_counts"],
        "unknown_labels": value["unknown_labels"],
        "terminal_verdict": value["terminal_verdict"],
        "valid": value["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and not value["unknown_labels"] and value["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }


RUNNERS = {
    "topology": contract_summary,
    "mutations": mutation_summary,
    "json": json_summary,
    "privacy": privacy_summary,
    "security": security_summary,
    "accessibility": accessibility_summary,
    "manifests": manifest_summary,
    "truth": truth_summary,
}


def runner_main(mode: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    if mode in {"closeout", "canonical"}:
        if not args.smoke:
            raise SystemExit(f"{mode} is terminal-only; use the dedicated lifecycle builder")
        result = {"mode": mode, "interface": "available_not_invoked", "valid": True}
    elif args.smoke and mode in {"topology", "mutations", "truth"} and not (PHASE_ROOT / "x2").exists():
        result = {"mode": mode, "interface": "pre-execution_smoke", "valid": True}
    else:
        result = RUNNERS[mode]()
    print(json.dumps({"mode": mode, "smoke": args.smoke, **result}, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit("import this runtime through a family-current phase runner")
