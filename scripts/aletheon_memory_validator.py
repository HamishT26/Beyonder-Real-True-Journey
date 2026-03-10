#!/usr/bin/env python3
"""Validate Aletheon reflection and memory artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MEMORY_REQUIRED_FIELDS = (
    "timestamp",
    "entry_type",
    "source_context",
    "reflection",
    "insight",
    "next_plan",
    "mirror_state",
)
ALLOWED_MIRROR_STATES = {"repo_only", "pending_notion_mirror", "mirrored_notion"}


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
        "# Aletheon Memory Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- entries_checked: `{payload['entries_checked']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Aletheon repo-first memory artifacts.")
    parser.add_argument("--personal-statement", default="docs/aletheon-personal-statement-v1.md")
    parser.add_argument("--reflection", default="docs/aletheon-reflection-latest.md")
    parser.add_argument("--next-plan", default="docs/aletheon-next-plan.md")
    parser.add_argument("--memory-log", default="docs/aletheon-memory-log.jsonl")
    parser.add_argument("--reports-dir", default="docs/aletheon-memory-runs")
    parser.add_argument("--latest-json", default="docs/aletheon-memory-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/aletheon-memory-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    for path_str in (args.personal_statement, args.reflection, args.next_plan):
        path = _repo_path(path_str)
        if not path.exists():
            failures.append(f"missing artifact: {path_str}")
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            failures.append(f"empty artifact: {path_str}")

    entries_checked = 0
    log_path = _repo_path(args.memory_log)
    if not log_path.exists():
        failures.append(f"missing memory log: {args.memory_log}")
    else:
        lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            failures.append("memory log must contain at least one entry")
        for index, line in enumerate(lines):
            entries_checked += 1
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                failures.append(f"memory_log[{index}] invalid json: {exc}")
                continue
            if not isinstance(payload, dict):
                failures.append(f"memory_log[{index}] must be an object")
                continue
            for field in MEMORY_REQUIRED_FIELDS:
                if field not in payload:
                    failures.append(f"memory_log[{index}] missing field: {field}")
            mirror_state = str(payload.get("mirror_state") or "").strip()
            if mirror_state not in ALLOWED_MIRROR_STATES:
                failures.append(f"memory_log[{index}] invalid mirror_state: {mirror_state}")

    output = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "entries_checked": entries_checked,
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-aletheon-memory-validation.json"
    timestamped_md = reports_dir / f"{stamp}-aletheon-memory-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    markdown = _markdown(output)
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={output['overall_status']}")
    print(f"effective_success={output['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if output["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
