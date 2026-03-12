#!/usr/bin/env python3
"""Validate the Trinity command book and execution ledger."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = {
    "command_id",
    "intent",
    "mode",
    "risk_class",
    "requires_live",
    "requires_connector",
    "preconditions",
    "command_template",
    "expected_artifacts",
    "rollback",
    "source_of_truth",
    "executor_role",
    "authority_scope",
    "council_visibility",
}
ALLOWED_RISK = {"low", "medium", "high", "critical"}
ALLOWED_EXECUTOR = {"aletheon", "planner", "builder", "reviewer", "researcher", "archivist"}
ALLOWED_VISIBILITY = {"leader_only", "pair", "council_shared", "public_readiness"}


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Trinity Command Book Validation",
            "",
            f"- generated_utc: `{payload['generated_utc']}`",
            f"- overall_status: **{payload['overall_status']}**",
            f"- command_count: `{payload['command_count']}`",
            "",
            "## Failures",
            *([f"- {item}" for item in payload["failures"]] or ["- none"]),
            "",
            "## Warnings",
            *([f"- {item}" for item in payload["warnings"]] or ["- none"]),
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity command book.")
    parser.add_argument("--command-book", default="docs/trinity-command-book-v5.json")
    parser.add_argument("--execution-ledger", default="docs/trinity-command-execution-ledger.jsonl")
    parser.add_argument("--reports-dir", default="docs/trinity-command-book-runs")
    parser.add_argument("--latest-json", default="docs/trinity-command-book-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-command-book-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    payload = json.loads(_repo_path(args.command_book).read_text(encoding="utf-8"))
    commands = payload.get("commands", [])
    if not isinstance(commands, list):
        failures.append("commands must be a list")
        commands = []
    if len(commands) != 348:
        failures.append(f"expected 348 commands, found {len(commands)}")

    seen: set[str] = set()
    for index, row in enumerate(commands):
        label = f"commands[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            failures.append(f"{label} missing fields: {missing}")
        command_id = str(row.get("command_id") or "").strip()
        if not command_id:
            failures.append(f"{label} empty command_id")
        elif command_id in seen:
            failures.append(f"duplicate command_id: {command_id}")
        else:
            seen.add(command_id)
        if str(row.get("risk_class") or "") not in ALLOWED_RISK:
            failures.append(f"{command_id or label} invalid risk_class")
        if str(row.get("executor_role") or "") not in ALLOWED_EXECUTOR:
            failures.append(f"{command_id or label} invalid executor_role")
        if str(row.get("council_visibility") or "") not in ALLOWED_VISIBILITY:
            failures.append(f"{command_id or label} invalid council_visibility")
        if not str(row.get("authority_scope") or "").strip():
            failures.append(f"{command_id or label} authority_scope must be non-empty")
        if not isinstance(row.get("requires_live"), bool):
            failures.append(f"{command_id or label} requires_live must be boolean")
        if not isinstance(row.get("preconditions"), list):
            failures.append(f"{command_id or label} preconditions must be a list")
        if not isinstance(row.get("expected_artifacts"), list) or not row.get("expected_artifacts"):
            failures.append(f"{command_id or label} expected_artifacts must be a non-empty list")
        if not str(row.get("command_template") or "").strip():
            failures.append(f"{command_id or label} empty command_template")
        if not str(row.get("rollback") or "").strip():
            failures.append(f"{command_id or label} empty rollback")
        source = str(row.get("source_of_truth") or "").strip()
        if not source:
            failures.append(f"{command_id or label} empty source_of_truth")
        else:
            try:
                if not _repo_path(source).exists():
                    failures.append(f"{command_id or label} missing source_of_truth: {source}")
            except Exception:
                failures.append(f"{command_id or label} invalid source_of_truth: {source}")
        template = str(row.get("command_template") or "").strip().split()
        if len(template) >= 2 and template[0].startswith("python") and template[1].startswith("scripts/"):
            try:
                if not _repo_path(template[1]).exists():
                    failures.append(f"{command_id or label} points to missing script: {template[1]}")
            except Exception:
                failures.append(f"{command_id or label} invalid script path in command_template: {template[1]}")

    ledger_path = _repo_path(args.execution_ledger)
    if not ledger_path.exists():
        failures.append(f"missing execution ledger: {args.execution_ledger}")
    else:
        for index, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                failures.append(f"execution_ledger[{index}] invalid json: {exc}")

    result = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "command_count": len(commands),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }
    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    (reports_dir / f"{stamp}-trinity-command-book-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (reports_dir / f"{stamp}-trinity-command-book-validation.md").write_text(_markdown(result), encoding="utf-8")
    latest_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(_markdown(result), encoding="utf-8")
    print(f"overall_status={result['overall_status']}")
    print(f"effective_success={result['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if result["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
