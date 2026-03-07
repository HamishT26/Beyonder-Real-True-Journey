#!/usr/bin/env python3
"""Validate the Trinity materialization ledger."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


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
    lines = [
        "# Trinity Materialization Ledger Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- rows_checked: `{payload['rows_checked']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity materialization ledger.")
    parser.add_argument("--ledger", default="docs/trinity-materialization-ledger.jsonl")
    parser.add_argument("--schema", default="docs/trinity-materialization-ledger-schema-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-materialization-ledger-runs")
    parser.add_argument("--latest-json", default="docs/trinity-materialization-ledger-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-materialization-ledger-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    schema = json.loads(_repo_path(args.schema).read_text(encoding="utf-8"))
    required_fields = schema.get("required_fields", [])
    if not isinstance(required_fields, list):
        required_fields = []
    allowed_results = set(schema.get("allowed_results", [])) if isinstance(schema.get("allowed_results"), list) else set()

    ledger_path = _repo_path(args.ledger)
    if not ledger_path.exists():
        failures.append(f"missing ledger: {args.ledger}")
        rows: list[dict[str, Any]] = []
    else:
        rows = []
        for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                failures.append(f"line {line_number}: invalid json ({exc})")
                continue
            if not isinstance(payload, dict):
                failures.append(f"line {line_number}: expected object entry")
                continue
            rows.append(payload)

    for index, row in enumerate(rows):
        label = f"rows[{index}]"
        missing = [field for field in required_fields if field not in row]
        if missing:
            failures.append(f"{label}: missing required fields {missing}")
        result = str(row.get("result") or "").strip()
        if result and allowed_results and result not in allowed_results:
            failures.append(f"{label}: invalid result {result}")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "rows_checked": len(rows),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-materialization-ledger-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-materialization-ledger-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown = _markdown(payload)
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
