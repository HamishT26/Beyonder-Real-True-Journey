#!/usr/bin/env python3
"""Shared bounded runtime for Sable Rook v666-v6 owner-local evidence."""

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
PHASE_ROOT = ROOT / "docs" / "sable-rook" / "v666-v6"
X1_SHA = "d747c689859fafcc061e48d36f10df6361b842da"
SOURCE_SHA = "016f7db26b0354e26407fb812ae3bd190b94ac7e"
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")

REQUIRED_CONTRACT_KEYS = {
    "schema",
    "proposal_id",
    "title",
    "expected_disposition",
    "outcome",
    "synthetic_fixture",
    "real_data_rows",
    "participant_count",
    "network_calls",
    "external_actions",
    "positive_fixture",
    "invariant",
    "source_needs",
    "stop_conditions",
    "protected_gates",
    "claim_boundary",
}

PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(
        r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
    ),
    "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
    "credential_or_token_value": re.compile(
        r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"
    ),
    "session_identifier_value": re.compile(
        r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'
    ),
    "private_callable_identifier_value": re.compile(
        r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
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
    for key in ("real_data_rows", "participant_count", "network_calls", "external_actions"):
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
        if fixture.get("real_material_state") != "absent":
            errors.append("real_material_not_absent")
    if not isinstance(contract.get("protected_gates"), list) or len(
        contract.get("protected_gates", [])
    ) < 10:
        errors.append("protected_gates_incomplete")
    if not isinstance(contract.get("stop_conditions"), list) or len(
        contract.get("stop_conditions", [])
    ) < 6:
        errors.append("stop_conditions_incomplete")
    boundary = str(contract.get("claim_boundary", "")).casefold()
    if "not empirical" not in boundary or "not authority" not in boundary:
        errors.append("claim_boundary_incomplete")
    if any(
        term in boundary
        for term in ("stage 20 authorized", "production approved", "authority granted")
    ):
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
        rows.append(
            {
                "mutation_id": f"{contract['proposal_id']}-{suffix}",
                "class": class_name,
                "rejected": not valid,
                "validator_errors": errors,
                "aggregate_credit": 0,
            }
        )
    return rows


def proposal_directories() -> list[Path]:
    return sorted((PHASE_ROOT / "x2" / "proposals").glob("sr6666-n*"))


def text_files(root: Path = PHASE_ROOT) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.casefold() in {".json", ".md", ".html", ".txt", ".py"}
    )


def scan_privacy(paths: Iterable[Path]) -> dict[str, Any]:
    candidates = []
    scanned = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append(
                    {"path": path.relative_to(ROOT).as_posix(), "class": class_name}
                )
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
    candidates = sorted((ROOT / "scripts").glob("*sable_rook_v666_v6*.py")) + sorted(
        (ROOT / "tests").glob("*sable_rook_v666_v6*.py")
    )
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
                    findings.append(
                        {
                            "path": path.relative_to(ROOT).as_posix(),
                            "line": node.lineno,
                            "class": f"dynamic_{name}",
                        }
                    )
                if any(
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                    for keyword in node.keywords
                ):
                    findings.append(
                        {
                            "path": path.relative_to(ROOT).as_posix(),
                            "line": node.lineno,
                            "class": "shell_true",
                        }
                    )
    return {
        "scanned_python_count": scanned,
        "finding_count": len(findings),
        "findings": findings,
        "valid": not findings,
        "claim_boundary": "bounded changed-Python AST scan only; not exhaustive security, penetration testing, or supply-chain assurance",
    }


def git_tree_map(commit: str) -> dict[str, tuple[str, str]]:
    """Return path -> (mode, oid) without passing long paths back to Git."""
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "-z", "--full-tree", commit]
    )
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, object_type, oid = metadata.decode("ascii").split()
        if object_type == "blob":
            result[encoded_path.decode("utf-8")] = (mode, oid)
    return result


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"git cat-file stream ended with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def replay_manifest(manifest_path: Path, commit: str) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    failures = []
    tree = git_tree_map(commit)
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
            state = tree.get(entry["path"])
            if state is None:
                failures.append({"path": entry["path"], "failure": "missing_tree_path"})
                continue
            mode, oid = state
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                failures.append({"path": entry["path"], "failure": "invalid_batch_header"})
                continue
            blob = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                failures.append({"path": entry["path"], "failure": "missing_batch_terminator"})
                continue
            if (
                hashlib.sha256(blob).hexdigest() != entry["sha256"]
                or len(blob) != entry["size_bytes"]
                or mode != entry["git_mode"]
                or oid != entry["git_blob_oid"]
                or header[0] != oid
            ):
                failures.append(
                    {"path": entry["path"], "failure": "sha_size_mode_or_oid_mismatch"}
                )
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        if return_code and process.stderr is not None:
            failures.append(
                {
                    "path": "<batch>",
                    "failure": process.stderr.read().decode("utf-8", errors="replace")[:240],
                }
            )
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
    return {
        "entry_count": len(manifest["entries"]),
        "failure_count": len(failures),
        "failures": failures,
        "valid": not failures,
    }


def accessibility_structure() -> dict[str, Any]:
    path = PHASE_ROOT / "reports" / "static-report.html"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required = [
        'lang="en-NZ"',
        "<main",
        "<caption>",
        'scope="col"',
        'scope="row"',
        "NOT_READY_FOR_STAGE_20",
        "@media print",
        "affected-user evaluation remain reserved",
    ]
    missing = [token for token in required if token not in text]
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "required_token_count": len(required),
        "missing_tokens": missing,
        "valid": not missing and "accessibility complete" not in text.casefold(),
        "claim_boundary": "static structural token check only; not accessibility-complete and not affected-user evaluation",
    }


def runner_payload(name: str, probe: bool = False) -> dict[str, Any]:
    terminal_names = {"closeout", "canonical"}
    if name in terminal_names:
        return {
            "runner": name,
            "probe_only": probe,
            "terminal_work_invoked": False,
            "valid": probe,
            "boundary": "terminal interface availability only; no closeout or canonical aggregate invoked",
        }
    if name == "contracts":
        results = [validate_contract(load_json(path / "contract.json")) for path in proposal_directories()]
        return {
            "runner": name,
            "contract_count": len(results),
            "valid_count": sum(valid for valid, _ in results),
            "errors": [error for valid, errors in results if not valid for error in errors],
            "valid": len(results) == 20 and all(valid for valid, _ in results),
        }
    if name == "mutations":
        receipts = [load_json(path / "mutation-results.json") for path in proposal_directories()]
        total = sum(row["mutation_count"] for row in receipts)
        rejected = sum(row["rejected_count"] for row in receipts)
        return {
            "runner": name,
            "mutation_count": total,
            "rejected_count": rejected,
            "valid": total == 100 and rejected == 100 and all(row["all_rejected"] for row in receipts),
        }
    if name == "json":
        paths = sorted(PHASE_ROOT.rglob("*.json"))
        for path in paths:
            load_json(path)
        return {"runner": name, "json_count": len(paths), "valid": bool(paths)}
    if name == "privacy":
        result = scan_privacy(text_files())
        return {"runner": name, **result}
    if name == "security":
        result = scan_python_security(changed_python_files())
        return {"runner": name, **result}
    if name == "manifests":
        result = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
        return {"runner": name, **result}
    if name == "accessibility":
        return {"runner": name, **accessibility_structure()}
    if name == "truth":
        ledger = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
        expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        return {
            "runner": name,
            "outcome_counts": ledger["outcome_counts"],
            "unknown_labels": ledger["unknown_labels"],
            "terminal_verdict": ledger["terminal_verdict"],
            "valid": ledger["outcome_counts"] == expected
            and not ledger["unknown_labels"]
            and ledger["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        }
    return {"runner": name, "valid": False, "error": "unknown_runner"}


def emit(value: Any) -> None:
    stream = getattr(__import__("sys"), "stdout")
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="strict")
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
