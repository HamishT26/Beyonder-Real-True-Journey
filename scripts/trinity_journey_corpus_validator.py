#!/usr/bin/env python3
"""Validate the v5 Beyonder journey corpus index."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = (
    "version",
    "agent_name",
    "source_file",
    "source_text",
    "analysis_status",
    "continuity_role",
    "evidence_state",
    "modules",
    "next_reconciliation_target",
)
REQUIRED_VERSIONS = {
    "v13",
    "v15",
    "v16",
    "v24",
    "v29",
    "v31",
    "v32",
    "v33",
    "v34",
    "v35",
    "v36",
    "v37",
    "v38",
}
ALLOWED_EVIDENCE_STATES = {"confirmed_evidence", "inference", "open_gap"}


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
        "# Trinity Journey Corpus Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- versions_checked: `{payload['versions_checked']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate docs/beyonder-journey-corpus-v13-v38.json")
    parser.add_argument("--corpus", default="docs/beyonder-journey-corpus-v13-v38.json")
    parser.add_argument("--reports-dir", default="docs/trinity-journey-corpus-runs")
    parser.add_argument("--latest-json", default="docs/trinity-journey-corpus-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-journey-corpus-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    corpus_path = _repo_path(args.corpus)
    if not corpus_path.exists():
        failures.append(f"missing corpus: {args.corpus}")
        payload: dict[str, Any] = {}
    else:
        try:
            payload = json.loads(corpus_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid json: {exc}")
            payload = {}

    versions = payload.get("versions", []) if isinstance(payload, dict) else []
    if not isinstance(versions, list):
        failures.append("corpus.versions must be a list")
        versions = []

    seen_versions: set[str] = set()
    for index, entry in enumerate(versions):
        label = f"versions[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{label} must be an object")
            continue
        for field in REQUIRED_FIELDS:
            if field not in entry:
                failures.append(f"{label} missing field: {field}")
        version = str(entry.get("version") or "").strip()
        if not version:
            failures.append(f"{label} empty version")
        elif version in seen_versions:
            failures.append(f"duplicate version entry: {version}")
        else:
            seen_versions.add(version)
        evidence_state = str(entry.get("evidence_state") or "").strip()
        if evidence_state not in ALLOWED_EVIDENCE_STATES:
            failures.append(f"{version or label} invalid evidence_state: {evidence_state}")
        modules = entry.get("modules")
        if not isinstance(modules, list) or not modules:
            failures.append(f"{version or label} modules must be a non-empty list")
        source_present = entry.get("source_present")
        text_present = entry.get("text_present")
        if not isinstance(source_present, bool) or not source_present:
            failures.append(f"{version or label} source_present must be true")
        if not isinstance(text_present, bool) or not text_present:
            failures.append(f"{version or label} text_present must be true")

    missing_versions = sorted(REQUIRED_VERSIONS - seen_versions)
    if missing_versions:
        failures.append(f"missing required versions: {missing_versions}")
    if "v29" in seen_versions:
        v29_entry = next((row for row in versions if isinstance(row, dict) and row.get("version") == "v29"), None)
        if not isinstance(v29_entry, dict):
            failures.append("v29 entry missing after initial detection")
        else:
            if str(v29_entry.get("evidence_state") or "") != "confirmed_evidence":
                failures.append("v29 must be tagged confirmed_evidence")
            modules = [str(item) for item in v29_entry.get("modules", []) if str(item).strip()]
            if len(modules) < 2:
                failures.append("v29 must carry grounded module references")

    output = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "versions_checked": len(versions),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-journey-corpus-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-journey-corpus-validation.md"
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
