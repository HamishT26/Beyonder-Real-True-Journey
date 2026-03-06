#!/usr/bin/env python3
"""Validate latest outputs for all Trinity expansion systems."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_PILLARS = {"mind", "body", "heart"}
ALLOWED_STATUS = {"PASS", "WARN", "FAIL", "TIMEOUT"}
ALLOWED_CHECK_STATUS = {"PASS", "WARN", "FAIL"}


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
        "# Trinity Expansion Result Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- systems_checked: `{payload['systems_checked']}`",
        "",
        "## Failures",
    ]
    if payload["failures"]:
        lines.extend([f"- {item}" for item in payload["failures"]])
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings"])
    if payload["warnings"]:
        lines.extend([f"- {item}" for item in payload["warnings"]])
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Trinity expansion latest artifacts.")
    parser.add_argument("--manifest", default="docs/trinity-expansion-system-manifest-v1.json")
    parser.add_argument("--schema", default="docs/trinity-expansion-result-schema-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-expansion-result-runs")
    parser.add_argument("--latest-json", default="docs/trinity-expansion-result-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-expansion-result-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    manifest = json.loads(_repo_path(args.manifest).read_text(encoding="utf-8"))
    schema = json.loads(_repo_path(args.schema).read_text(encoding="utf-8"))
    required_fields = schema.get("required_fields", [])
    if not isinstance(required_fields, list):
        required_fields = []
    check_required = schema.get("check_required_fields", [])
    if not isinstance(check_required, list):
        check_required = []

    systems = manifest.get("systems", [])
    if not isinstance(systems, list):
        systems = []
        failures.append("manifest.systems must be a list")

    checked = 0
    for entry in systems:
        if not isinstance(entry, dict):
            failures.append("manifest contains non-object system entry")
            continue
        system_id = str(entry.get("system_id") or "unknown")
        outputs = entry.get("outputs", [])
        if not isinstance(outputs, list) or not outputs:
            failures.append(f"{system_id}: missing outputs list in manifest")
            continue
        latest_path = str(outputs[0])
        checked += 1
        try:
            target = _repo_path(latest_path)
        except Exception:
            failures.append(f"{system_id}: invalid output path {latest_path}")
            continue
        if not target.exists():
            failures.append(f"{system_id}: missing output {latest_path}")
            continue
        try:
            payload = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{system_id}: invalid json ({exc})")
            continue
        if not isinstance(payload, dict):
            failures.append(f"{system_id}: payload must be an object")
            continue

        missing_fields = [field for field in required_fields if field not in payload]
        if missing_fields:
            failures.append(f"{system_id}: missing required fields {missing_fields}")

        pillar = str(payload.get("pillar") or "")
        if pillar not in ALLOWED_PILLARS:
            failures.append(f"{system_id}: invalid pillar {pillar}")

        overall_status = str(payload.get("overall_status") or "")
        if overall_status not in ALLOWED_STATUS:
            failures.append(f"{system_id}: invalid overall_status {overall_status}")

        checks = payload.get("checks", [])
        if not isinstance(checks, list):
            failures.append(f"{system_id}: checks must be a list")
            checks = []
        for idx, item in enumerate(checks):
            if not isinstance(item, dict):
                failures.append(f"{system_id}: check[{idx}] must be an object")
                continue
            for field in check_required:
                if field not in item:
                    failures.append(f"{system_id}: check[{idx}] missing field {field}")
            status_value = str(item.get("status") or "")
            if status_value and status_value not in ALLOWED_CHECK_STATUS:
                failures.append(f"{system_id}: check[{idx}] invalid status {status_value}")

        metrics = payload.get("metrics")
        if not isinstance(metrics, dict):
            failures.append(f"{system_id}: metrics must be an object")

        targets = payload.get("repo_targets_touched")
        if not isinstance(targets, list):
            failures.append(f"{system_id}: repo_targets_touched must be a list")

        effective_success = payload.get("effective_success")
        if not isinstance(effective_success, bool):
            failures.append(f"{system_id}: effective_success must be boolean")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "systems_checked": checked,
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-expansion-result-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-expansion-result-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md = _markdown(payload)
    timestamped_md.write_text(md, encoding="utf-8")
    latest_md.write_text(md, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    if payload["effective_success"]:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
