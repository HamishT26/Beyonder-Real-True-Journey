#!/usr/bin/env python3
"""Validate Aurelis memory continuity artifacts for consistency."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "docs" / "aurelis-memory-log.jsonl"
MD_LOG = ROOT / "docs" / "aurelis-memory-log.md"
SUMMARY = ROOT / "docs" / "aurelis-memory-latest-summary.md"
NEXT_STEPS = ROOT / "docs" / "aurelis-next-steps.md"
REPORT = ROOT / "docs" / "aurelis-memory-integrity-report.md"

REQUIRED_FIELDS = [
    "timestamp_utc",
    "nzdt_context",
    "role",
    "user_message",
    "assistant_reflection",
    "progress_snapshot",
    "next_step",
]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def strict_required_fields_check(rows: list[dict]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows to validate"
    missing = 0
    for row in rows:
        for field in REQUIRED_FIELDS:
            if field not in row or row.get(field) in (None, ""):
                missing += 1
    return missing == 0, f"missing_or_empty_fields={missing}"


def strict_timestamp_order_check(rows: list[dict]) -> tuple[bool, str]:
    if len(rows) < 2:
        return True, "rows<2"
    parsed: list[datetime] = []
    parse_errors = 0
    for row in rows:
        ts = row.get("timestamp_utc", "")
        try:
            parsed.append(datetime.fromisoformat(ts))
        except Exception:  # noqa: BLE001
            parse_errors += 1
    if parse_errors > 0:
        return False, f"timestamp_parse_errors={parse_errors}"

    violations = 0
    for i in range(len(parsed) - 1):
        if parsed[i] > parsed[i + 1]:
            violations += 1
    return violations == 0, f"ordering_violations={violations}"


def main() -> None:
    p = argparse.ArgumentParser(description="Validate Aurelis continuity artifacts")
    p.add_argument("--strict", action="store_true", help="Enable required-field and timestamp-order checks")
    args = p.parse_args()

    checks: list[tuple[str, bool, str]] = []

    rows = read_jsonl(JSONL)
    checks.append(("jsonl_exists_and_nonempty", len(rows) > 0, f"rows={len(rows)}"))

    md_text = MD_LOG.read_text() if MD_LOG.exists() else ""
    md_entries = len(re.findall(r"^## ", md_text, flags=re.MULTILINE))
    checks.append(("markdown_entry_count_matches_jsonl", md_entries == len(rows), f"md_entries={md_entries}, jsonl_rows={len(rows)}"))

    summary_text = SUMMARY.read_text() if SUMMARY.exists() else ""
    m = re.search(r"Entries summarized: \*\*(\d+)\*\*", summary_text)
    summarized = int(m.group(1)) if m else -1
    expected_summary = min(5, len(rows)) if len(rows) > 0 else 0
    checks.append(("summary_entry_count_expected", summarized == expected_summary, f"summary={summarized}, expected={expected_summary}"))

    latest_ts = rows[-1].get("timestamp_utc", "") if rows else ""
    next_text = NEXT_STEPS.read_text() if NEXT_STEPS.exists() else ""
    checks.append(("next_steps_references_latest_timestamp", latest_ts in next_text, f"latest_ts={latest_ts}"))

    if args.strict:
        ok_fields, detail_fields = strict_required_fields_check(rows)
        checks.append(("strict_required_fields_present", ok_fields, detail_fields))

        ok_order, detail_order = strict_timestamp_order_check(rows)
        checks.append(("strict_timestamp_monotonic_non_decreasing", ok_order, detail_order))

    ok_count = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)

    lines = [
        "# Aurelis Memory Integrity Report",
        "",
        f"Checks passed: **{ok_count}/{total}**",
        "",
        f"Mode: **{'strict' if args.strict else 'standard'}**",
        "",
        "## Check results",
    ]
    for name, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        lines.append(f"- {name}: **{mark}** ({detail})")

    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT}")

    if ok_count != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
