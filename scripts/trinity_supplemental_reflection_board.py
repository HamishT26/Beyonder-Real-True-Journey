#!/usr/bin/env python3
"""Emit a non-gating supplemental reflection board."""

from __future__ import annotations

import argparse
from typing import Any
from urllib.parse import urlparse

from trinity_api_common import iso_now, read_json, save_json_and_markdown_run

REQUIRED_FIELDS = {
    "tradition",
    "title",
    "publisher",
    "url",
    "curation_status",
    "reflection_summary",
    "non_gating_reason",
}


def _build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Trinity Supplemental Reflection Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- entry_count: `{payload['entry_count']}`",
        "",
        "## Traditions",
        "| tradition | title | publisher | curation_status |",
        "|---|---|---|---|",
    ]
    for entry in payload["entries"]:
        lines.append(
            f"| {entry['tradition']} | {entry['title']} | {entry['publisher']} | {entry['curation_status']} |"
        )
    lines.extend(["", "## Checks", "| check | status | detail |", "|---|---|---|"])
    for check in payload["checks"]:
        lines.append(f"| {check['name']} | {check['status']} | {check['detail']} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the non-gating Trinity supplemental reflection board.")
    parser.add_argument("--registry", default="docs/trinity-supplemental-reflection-registry-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-supplemental-reflection-runs")
    parser.add_argument("--latest-json", default="docs/trinity-supplemental-reflection-board-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-supplemental-reflection-board-latest.md")
    args = parser.parse_args()

    registry = read_json(args.registry)
    entries = registry.get("entries", [])
    failures: list[str] = []
    if not isinstance(entries, list) or not entries:
        failures.append("entries must be a non-empty list")
        entries = []
    for index, entry in enumerate(entries, start=1):
        missing = sorted(REQUIRED_FIELDS - set(entry))
        if missing:
            failures.append(f"entry[{index}] missing fields: {', '.join(missing)}")
            continue
        parsed = urlparse(str(entry["url"]))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            failures.append(f"entry[{index}] invalid url: {entry['url']}")
    payload = {
        "generated_utc": iso_now(),
        "overall_status": "FAIL" if failures else "PASS",
        "entry_count": len(entries),
        "entries": entries,
        "checks": [
            {
                "name": "registry_schema",
                "status": "FAIL" if failures else "PASS",
                "detail": "; ".join(failures) if failures else "ok",
            }
        ],
        "effective_success": not failures,
        "non_gating_notice": "This board is reflective only and does not affect the standard Trinity suite.",
    }
    markdown = _build_markdown(payload)
    save_json_and_markdown_run(
        payload=payload,
        markdown=markdown,
        latest_json=args.latest_json,
        latest_md=args.latest_md,
        reports_dir=args.reports_dir,
        stem="trinity-supplemental-reflection-board",
    )
    print(f"overall_status={payload['overall_status']}")
    print(f"entry_count={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
