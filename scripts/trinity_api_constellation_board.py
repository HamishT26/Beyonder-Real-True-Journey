#!/usr/bin/env python3
"""Emit a combined cached Trinity API constellation board."""

from __future__ import annotations

import argparse
from typing import Any

from trinity_api_common import (
    iso_now,
    normalize_status,
    read_json,
    save_json_and_markdown_run,
    severity,
)


def _build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Trinity API Constellation Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- manifest_validation_status: `{payload['manifest_validation_status']}`",
        "",
        "## Pillar rollup",
        "| pillar | status | freshness_status | source_count | next_refresh_action |",
        "|---|---|---|---|---|",
    ]
    for pillar in ("mind", "body", "heart"):
        row = payload["pillars"][pillar]
        lines.append(
            f"| {pillar} | {row['overall_status']} | {row['freshness_status']} | "
            f"{row['source_count']} | {row['next_refresh_action']} |"
        )
    lines.extend(
        [
            "",
            "## Promotion candidates",
            "| target | record_count | latest_published_at | supporting_source_ids |",
            "|---|---|---|---|",
        ]
    )
    for row in payload["promotion_candidates"]:
        lines.append(
            f"| {row['target']} | {row['record_count']} | {row['latest_published_at']} | "
            f"{', '.join(row['supporting_source_ids']) or '-'} |"
        )
    lines.extend(["", "## Manual follow-ups"])
    for item in payload["manual_follow_ups"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the combined Trinity API constellation board.")
    parser.add_argument("--manifest-validator", default="docs/trinity-api-source-manifest-validation-latest.json")
    parser.add_argument("--mind-board", default="docs/mind-theory-signal-board-latest.json")
    parser.add_argument("--body-board", default="docs/body-compute-signal-board-latest.json")
    parser.add_argument("--heart-board", default="docs/heart-governance-signal-board-latest.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-board-runs")
    parser.add_argument("--latest-json", default="docs/trinity-api-constellation-board-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-api-constellation-board-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    manifest_validator = read_json(args.manifest_validator)
    boards = {
        "mind": read_json(args.mind_board),
        "body": read_json(args.body_board),
        "heart": read_json(args.heart_board),
    }

    overall_status = normalize_status(manifest_validator.get("overall_status"))
    promotion_candidates: dict[str, dict[str, Any]] = {}
    manual_follow_ups: list[str] = []
    for pillar, board in boards.items():
        status = normalize_status(board.get("overall_status"))
        if severity(status) > severity(overall_status):
            overall_status = status
        if status != "PASS":
            manual_follow_ups.append(f"Resolve {pillar} API board drift before promoting new comparison language.")
        for row in board.get("promotion_candidates", []):
            target = str(row.get("target"))
            bucket = promotion_candidates.setdefault(
                target,
                {
                    "target": target,
                    "record_count": 0,
                    "latest_published_at": "1970-01-01",
                    "supporting_source_ids": set(),
                },
            )
            bucket["record_count"] += int(row.get("record_count", 0))
            if str(row.get("latest_published_at", "")) > str(bucket["latest_published_at"]):
                bucket["latest_published_at"] = str(row.get("latest_published_at"))
            bucket["supporting_source_ids"].update(str(value) for value in row.get("supporting_source_ids", []))

    if normalize_status(manifest_validator.get("overall_status")) != "PASS":
        manual_follow_ups.append("Fix manifest or query-pack integrity before trusting the API constellation layer.")
    if not manual_follow_ups:
        manual_follow_ups.append("Review the strongest promotion candidates before editing the curated public-source registry.")

    payload = {
        "generated_utc": iso_now(),
        "overall_status": overall_status,
        "manifest_validation_status": normalize_status(manifest_validator.get("overall_status")),
        "pillars": boards,
        "promotion_candidates": sorted(
            [
                {
                    "target": row["target"],
                    "record_count": row["record_count"],
                    "latest_published_at": row["latest_published_at"],
                    "supporting_source_ids": sorted(row["supporting_source_ids"]),
                }
                for row in promotion_candidates.values()
            ],
            key=lambda row: (row["record_count"], row["latest_published_at"], row["target"]),
            reverse=True,
        ),
        "manual_follow_ups": manual_follow_ups,
        "effective_success": overall_status == "PASS",
    }
    markdown = _build_markdown(payload)
    save_json_and_markdown_run(
        payload=payload,
        markdown=markdown,
        latest_json=args.latest_json,
        latest_md=args.latest_md,
        reports_dir=args.reports_dir,
        stem="trinity-api-constellation-board",
    )
    print(f"overall_status={overall_status}")
    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
