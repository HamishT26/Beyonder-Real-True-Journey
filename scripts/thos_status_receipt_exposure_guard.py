#!/usr/bin/env python3
"""Scan curated THOS status receipts for publish-blocking exposure patterns."""

from __future__ import annotations

import argparse
import glob
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Rule:
    rule_id: str
    pattern: re.Pattern[str]
    description: str


RULES = [
    Rule("drive_path", re.compile(r"[A-Z]:\\"), "Windows drive path"),
    Rule("api_key_shape", re.compile(r"sk-[A-Za-z0-9]{20,}"), "API key shaped token"),
    Rule("private_key_block", re.compile(r"BEGIN (?:OPENAI|RSA PRIVATE KEY|PRIVATE KEY)"), "private key block"),
    Rule("github_pat_shape", re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub personal access token shape"),
    Rule("session_jsonl", re.compile(r"session\.jsonl", re.IGNORECASE), "session transcript file reference"),
    Rule("raw_session_stream", re.compile(r"raw\s+session\s+stream", re.IGNORECASE), "unfiltered session stream phrase"),
    Rule("dated_image_capture", re.compile(r"Screenshot [0-9]{4}-[0-9]{2}-[0-9]{2}"), "dated image-capture filename"),
    Rule("unredacted_app_thread_id", re.compile(r"019[de][0-9a-f-]{20,}"), "unredacted app thread id"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def expand_inputs(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(match) for match in glob.glob(pattern)]
        if matches:
            paths.extend(matches)
        else:
            paths.append(Path(pattern))
    unique = {path.as_posix(): path for path in paths if path.exists() and path.is_file()}
    return [unique[key] for key in sorted(unique)]


def scan_file(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits: list[dict[str, Any]] = []
    for rule in RULES:
        count = len(rule.pattern.findall(text))
        if count:
            hits.append(
                {
                    "file": path.name,
                    "rule_id": rule.rule_id,
                    "description": rule.description,
                    "count": count,
                }
            )
    return hits


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Status Receipt Exposure Guard",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- files_scanned: `{payload['files_scanned']}`",
        f"- findings_count: `{payload['findings_count']}`",
        "",
        "## Findings",
    ]
    if payload["findings"]:
        for row in payload["findings"]:
            lines.append(f"- `{row['file']}`: `{row['rule_id']}` count `{row['count']}`.")
    else:
        lines.append("- No publish-blocking exposure patterns found.")
    lines.extend(
        [
            "",
            "This guard records filenames, rule identifiers, and counts only. It does not publish matched text.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--input", action="append", required=True, help="File path or glob. Repeatable.")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    files = expand_inputs(args.input)
    findings: list[dict[str, Any]] = []
    for path in files:
        findings.extend(scan_file(path))
    payload = {
        "artifact_type": "status_receipt_exposure_guard",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_EXPOSURE_GUARD" if not findings else "OPEN_GAP_EXPOSURE_GUARD_FINDINGS",
        "files_scanned": len(files),
        "findings_count": len(findings),
        "findings": findings,
        "claim_boundary": {
            "matched_text_published": False,
            "raw_lane_text_published": False,
            "raw_transport_published": False,
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "findings_count": len(findings)}, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
