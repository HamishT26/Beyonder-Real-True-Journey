#!/usr/bin/env python3
"""Summarize generic CLI marker-review warnings against strict quality results."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def by_lane(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("lane")): row for row in rows if row.get("lane")}


def lane_rows(notifier: dict[str, Any], quality: dict[str, Any]) -> list[dict[str, Any]]:
    quality_by_lane = by_lane(quality.get("lanes", []))
    rows: list[dict[str, Any]] = []
    for item in notifier.get("lanes", []):
        lane = str(item.get("lane"))
        q = quality_by_lane.get(lane, {})
        generic_count = int(item.get("final_message_sensitive_marker_count") or 0)
        strict_count = int(q.get("sensitive_or_path_marker_count") or 0)
        quality_status = str(q.get("quality_status"))
        if generic_count > 0 and strict_count == 0 and quality_status == "PASS_ELABORATION_GATE":
            decision = "PASS_FALSE_POSITIVE_GENERIC_MARKER_REVIEW"
        elif strict_count > 0:
            decision = "OPEN_GAP_STRICT_MARKER_FAILURE"
        elif generic_count > 0:
            decision = "OPEN_GAP_GENERIC_MARKER_REVIEW_WITHOUT_QUALITY_PASS"
        else:
            decision = "PASS_NO_MARKERS"
        rows.append(
            {
                "lane": lane,
                "generic_marker_count": generic_count,
                "strict_sensitive_or_path_marker_count": strict_count,
                "quality_status": quality_status,
                "decision": decision,
                "raw_output_boundary": item.get("raw_output_boundary", "temp_only_not_published"),
            }
        )
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Marker Review Ledger",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['overall_status']}`",
        "",
        "Lane marker review:",
    ]
    for row in payload["lanes"]:
        lines.append(
            f"- {row['lane']}: `{row['decision']}`, generic `{row['generic_marker_count']}`, "
            f"strict `{row['strict_sensitive_or_path_marker_count']}`, quality `{row['quality_status']}`"
        )
    lines.extend(
        [
            "",
            "This ledger reads curated notifier and quality receipts only. It does not read or publish raw lane text.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--notifier-json", required=True)
    parser.add_argument("--quality-json", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    notifier = read_json(Path(args.notifier_json))
    quality = read_json(Path(args.quality_json))
    rows = lane_rows(notifier, quality)
    open_gaps = [row for row in rows if str(row["decision"]).startswith("OPEN_GAP")]
    payload: dict[str, Any] = {
        "artifact_type": "cli_marker_review_ledger",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_MARKER_REVIEW_LEDGER" if not open_gaps else "OPEN_GAP_MARKER_REVIEW",
        "notifier_receipt": Path(args.notifier_json).name,
        "quality_receipt": Path(args.quality_json).name,
        "lanes": rows,
        "raw_lane_text_published": False,
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not open_gaps else 1


if __name__ == "__main__":
    raise SystemExit(main())
