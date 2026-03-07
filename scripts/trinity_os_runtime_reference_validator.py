#!/usr/bin/env python3
"""Validate the OS runtime reference registry."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = {"source_id", "os_family", "layer", "publisher", "url", "published_at", "pattern", "trinity_target"}
ALLOWED_TARGETS = {"mind", "body", "heart", "trinity"}


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
        "# Trinity OS Runtime Reference Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- source_count: `{payload['source_count']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity OS runtime reference registry.")
    parser.add_argument("--registry", default="docs/trinity-os-runtime-reference-registry-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-os-runtime-reference-runs")
    parser.add_argument("--latest-json", default="docs/trinity-os-runtime-reference-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-os-runtime-reference-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    payload = json.loads(_repo_path(args.registry).read_text(encoding="utf-8"))
    sources = payload.get("sources", [])
    if not isinstance(sources, list):
        failures.append("registry.sources must be a list")
        sources = []

    seen_ids: set[str] = set()
    for index, row in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(row.keys())
        if missing:
            failures.append(f"{label} missing fields {sorted(missing)}")
        source_id = str(row.get("source_id") or "").strip()
        if not source_id:
            failures.append(f"{label} empty source_id")
        elif source_id in seen_ids:
            failures.append(f"duplicate source_id: {source_id}")
        else:
            seen_ids.add(source_id)
        if str(row.get("trinity_target") or "") not in ALLOWED_TARGETS:
            failures.append(f"{source_id or label} invalid trinity_target: {row.get('trinity_target')}")
        if not str(row.get("url") or "").startswith("https://"):
            failures.append(f"{source_id or label} url must be https")

    result = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "source_count": len(sources),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-os-runtime-reference-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-os-runtime-reference-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    markdown = _markdown(result)
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={result['overall_status']}")
    print(f"effective_success={result['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if result["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
