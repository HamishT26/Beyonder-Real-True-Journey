#!/usr/bin/env python3
"""Validate the bounded Freed ID compliance bridge surfaces used in the V20 heart wave."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_JSON_PATHS = [
    "docs/v17-standards-bridge-validation-latest.json",
    "docs/heart-track-min-disclosure-latest.json",
    "docs/heart-track-min-disclosure-live-latest.json",
    "docs/heart-track-min-disclosure-adversarial-latest.json",
    "docs/heart-track-dispute-recourse-latest.json",
    "docs/heart-track-dispute-recourse-adversarial-latest.json",
]
REQUIRED_PRESENCE_PATHS = [
    "docs/freedid-compliance-bridge-v15-catalog-entry-v1.json",
    "docs/trinity-shadow-clone-policy-v1.json",
]


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _normalize_status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in {"PASS", "WARN", "FAIL", "TIMEOUT"}:
        return text
    if text in {"OK", "SUCCESS"}:
        return "PASS"
    return "FAIL"


def _payload_status(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("effective_success"), bool):
        return "PASS" if payload["effective_success"] else "FAIL"
    for key in ("overall_status", "status", "comparator_status"):
        if key in payload:
            return _normalize_status(payload.get(key))
    return "FAIL"


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Freed ID Compliance Bridge Check",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- evidence_count: `{payload['evidence_count']}`",
        "",
        "## Checks",
    ]
    lines.extend([f"- {item}" for item in payload["checks"]] or ["- none"])
    lines.extend(["", "## Failures"])
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the bounded Freed ID compliance bridge surfaces.")
    parser.add_argument("--latest-json", default="docs/heart-track-freedid-compliance-bridge-check-latest.json")
    parser.add_argument("--latest-md", default="docs/heart-track-freedid-compliance-bridge-check-latest.md")
    parser.add_argument("--reports-dir", default="docs/freedid-compliance-bridge-runs")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    checks: list[str] = []

    for path_str in REQUIRED_PRESENCE_PATHS:
        path = _repo_path(path_str)
        if path.exists():
            checks.append(f"present: {path_str}")
        else:
            failures.append(f"missing required artifact: {path_str}")

    for path_str in REQUIRED_JSON_PATHS:
        path = _repo_path(path_str)
        if not path.exists():
            failures.append(f"missing required json artifact: {path_str}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid json: {path_str} ({exc})")
            continue
        if not isinstance(payload, dict):
            failures.append(f"expected json object: {path_str}")
            continue
        status = _payload_status(payload)
        if status == "FAIL":
            failures.append(f"{path_str} reported FAIL")
        elif status == "WARN":
            warnings.append(f"{path_str} reported WARN")
        else:
            checks.append(f"pass_like: {path_str} ({status})")

    payload = {
        "generated_utc": _now_iso(),
        "overall_status": _status(failures, warnings),
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
        "evidence_count": len(REQUIRED_JSON_PATHS) + len(REQUIRED_PRESENCE_PATHS),
        "checks": checks,
        "failures": failures,
        "warnings": warnings,
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-freedid-compliance-bridge-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-compliance-bridge-check.md"

    json_text = json.dumps(payload, indent=2) + "\n"
    markdown = _markdown(payload)
    for path in (latest_json, timestamped_json):
        path.write_text(json_text, encoding="utf-8")
    for path in (latest_md, timestamped_md):
        path.write_text(markdown, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
