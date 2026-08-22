#!/usr/bin/env python3
"""Family-current runner profiles for Ilyra Fen v666-v4."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from ghc_family_ilyra_fen_v666_v4_runtime import (
    ALLOWED_LABELS,
    PHASE_ROOT,
    X1_SHA,
    changed_python_files,
    emit,
    load_json,
    proposal_directories,
    replay_manifest,
    scan_privacy,
    scan_python_security,
    text_files,
    validate_contract,
)


def contracts() -> dict[str, Any]:
    rows = []
    for directory in proposal_directories():
        contract = load_json(directory / "contract.json")
        valid, errors = validate_contract(contract)
        rows.append({"proposal_id": contract["proposal_id"], "valid": valid, "errors": errors})
    return {"profile": "contracts", "count": len(rows), "valid_count": sum(row["valid"] for row in rows), "rows": rows, "valid": len(rows) == 20 and all(row["valid"] for row in rows)}


def mutations() -> dict[str, Any]:
    rows = [load_json(directory / "mutation-results.json") for directory in proposal_directories()]
    total = sum(row["mutation_count"] for row in rows)
    rejected = sum(row["rejected_count"] for row in rows)
    return {"profile": "mutations", "proposal_count": len(rows), "mutation_count": total, "rejected_count": rejected, "valid": len(rows) == 20 and total == 100 and rejected == 100 and all(row["all_rejected"] for row in rows)}


def json_profile() -> dict[str, Any]:
    failures = []
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append({"path": path.relative_to(PHASE_ROOT).as_posix(), "error": type(exc).__name__})
    return {"profile": "json", "parsed": len(paths), "failure_count": len(failures), "failures": failures, "valid": not failures}


def privacy() -> dict[str, Any]:
    return {"profile": "privacy", **scan_privacy(text_files())}


def security() -> dict[str, Any]:
    return {"profile": "security", **scan_python_security(changed_python_files())}


def manifests() -> dict[str, Any]:
    x1 = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    evidence_path = PHASE_ROOT / "validation" / "evidence-content-manifest.json"
    return {"profile": "manifests", "x1": x1, "evidence_state": "present_pending_commit_replay" if evidence_path.exists() else "not_yet_built", "valid": x1["valid"]}


def accessibility() -> dict[str, Any]:
    path = PHASE_ROOT / "reports" / "static-report.html"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    checks = {
        "lang": 'lang="en-NZ"' in text,
        "title": "<title>" in text,
        "main": "<main" in text,
        "caption": "<caption>" in text,
        "scoped_headers": 'scope="col"' in text and 'scope="row"' in text,
        "text_state": "NOT_READY_FOR_STAGE_20" in text,
        "manual_reserved": "manual" in text.casefold() and "affected-user" in text.casefold(),
        "print_fallback": "@media print" in text,
    }
    return {"profile": "accessibility", "checks": checks, "valid": all(checks.values()), "claim_boundary": "structural HTML checks only; not complete accessibility conformance"}


def truth() -> dict[str, Any]:
    ledger = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    labels = {row["outcome"] for row in ledger["proposals"]}
    valid = ledger["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and labels == set(ALLOWED_LABELS) and ledger["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    return {"profile": "truth", "counts": ledger["outcome_counts"], "labels": sorted(labels), "valid": valid}


def closeout(probe: bool) -> dict[str, Any]:
    if probe:
        return {"profile": "closeout", "terminal_work_invoked": False, "state": "interface_probe_only", "valid": True}
    path = PHASE_ROOT / "closeout" / "closeout-receipt.json"
    value = load_json(path) if path.exists() else {}
    return {"profile": "closeout", "terminal_work_invoked": True, "state": value.get("status", "missing"), "valid": bool(value.get("valid"))}


def canonical(probe: bool, execute: bool) -> dict[str, Any]:
    if probe:
        return {"profile": "canonical", "aggregate_invoked": False, "state": "interface_probe_only", "valid": True}
    if not execute:
        return {"profile": "canonical", "aggregate_invoked": False, "state": "execute_flag_required", "valid": False}
    protocol = load_json(PHASE_ROOT / "validation" / "canonical-validation-protocol.json")
    return {"profile": "canonical", "aggregate_invoked": True, "protocol_one_shot": protocol.get("one_success_no_replay"), "valid": bool(protocol.get("one_success_no_replay"))}


PROFILES = {
    "contracts": lambda _probe, _execute: contracts(),
    "mutations": lambda _probe, _execute: mutations(),
    "json": lambda _probe, _execute: json_profile(),
    "privacy": lambda _probe, _execute: privacy(),
    "security": lambda _probe, _execute: security(),
    "manifests": lambda _probe, _execute: manifests(),
    "accessibility": lambda _probe, _execute: accessibility(),
    "truth": lambda _probe, _execute: truth(),
    "closeout": lambda probe, _execute: closeout(probe),
    "canonical": lambda probe, execute: canonical(probe, execute),
}


def run(profile: str, *, probe: bool = False, execute: bool = False) -> dict[str, Any]:
    if profile not in PROFILES:
        return {"profile": profile, "valid": False, "error": "unknown_profile"}
    return PROFILES[profile](probe, execute)


def cli(profile: str) -> None:
    args = set(sys.argv[1:])
    if args - {"--probe", "--execute"}:
        raise SystemExit("supported flags: --probe or --execute")
    result = run(profile, probe="--probe" in args, execute="--execute" in args)
    emit(result)
    raise SystemExit(0 if result.get("valid") else 1)
