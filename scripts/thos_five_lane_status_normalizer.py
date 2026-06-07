#!/usr/bin/env python3
"""Normalize five-lane app and CLI receipts without reading raw lane output."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    candidate = Path(path)
    if not candidate.exists():
        return {}
    return json.loads(candidate.read_text(encoding="utf-8"))


def by_lane(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("lane")): row for row in rows if row.get("lane")}


def app_rows(app_gate: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in app_gate.get("lanes", []):
        rows.append(
            {
                "lane": row.get("lane"),
                "surface": "app",
                "status": row.get("overall_status"),
                "completion_status": row.get("completion_status"),
                "read_status": row.get("read_status"),
                "resume_status": row.get("resume_status"),
                "raw_boundary": "status_only",
            }
        )
    return rows


def cli_rows(cli_notice: dict[str, Any], quality_gate: dict[str, Any]) -> list[dict[str, Any]]:
    quality = by_lane(quality_gate.get("lanes", []))
    rows = []
    for row in cli_notice.get("lanes", []):
        lane_name = str(row.get("lane"))
        q = quality.get(lane_name, {})
        rows.append(
            {
                "lane": lane_name,
                "surface": "cli",
                "status": row.get("completion_status"),
                "completion_status": row.get("completion_status"),
                "quality_status": q.get("quality_status"),
                "word_count": q.get("word_count"),
                "final_message_bytes": row.get("final_message_bytes"),
                "final_message_hash": row.get("final_message_hash"),
                "generic_sensitive_marker_count": row.get("final_message_sensitive_marker_count"),
                "strict_sensitive_or_path_marker_count": q.get("sensitive_or_path_marker_count"),
                "missing_required_heading_count": len(q.get("missing_required_headings", [])),
                "raw_boundary": row.get("raw_output_boundary", "temp_only_not_published"),
            }
        )
    return rows


def status_for(app_gate: dict[str, Any], cli_notice: dict[str, Any], quality_gate: dict[str, Any]) -> str:
    app_lanes = app_gate.get("lanes", [])
    app_ok = str(app_gate.get("overall_status", "")).startswith("PASS") or (
        bool(app_lanes)
        and all(row.get("overall_status") == "completed" for row in app_lanes)
    )
    cli_ready = all(
        row.get("completion_status") == "FINAL_MESSAGE_READY"
        for row in cli_notice.get("lanes", [])
    ) and bool(cli_notice.get("lanes"))
    quality_ok = str(quality_gate.get("aggregate_status", "")).startswith("PASS")
    if app_ok and cli_ready and quality_ok:
        return "PASS_FIVE_LANE_READY"
    if app_ok and cli_ready:
        return "PASS_FIVE_LANE_VISIBLE_WITH_OPEN_REPAIR"
    return "OPEN_GAP_FIVE_LANE_STATUS"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Five-Lane Normalized Status Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- next_manual_check_utc: `{payload.get('next_manual_check_utc') or 'not specified'}`",
        f"- phase_advance_allowed: `{str(payload['phase_advance_allowed']).lower()}`",
        "",
        "## Lane Rows",
    ]
    for row in payload["lanes"]:
        if row["surface"] == "cli":
            lines.append(
                f"- {row['lane']} ({row['surface']}): `{row.get('completion_status')}`, "
                f"quality `{row.get('quality_status')}`, words `{row.get('word_count')}`, "
                f"missing headings `{row.get('missing_required_heading_count')}`, raw `{row.get('raw_boundary')}`."
            )
        else:
            lines.append(
                f"- {row['lane']} ({row['surface']}): `{row.get('status')}`, "
                f"completion `{row.get('completion_status')}`, raw `{row.get('raw_boundary')}`."
            )
    lines.extend(
        [
            "",
        "This board reads curated receipts only. It does not read or publish raw lane text, raw app transport, raw CLI output, image captures, credentials, session streams, or private dumps.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--cadence-json")
    parser.add_argument("--app-json", required=True)
    parser.add_argument("--cli-json", required=True)
    parser.add_argument("--quality-json", required=True)
    parser.add_argument("--next-manual-check-utc")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    cadence = read_json(args.cadence_json)
    app_gate = read_json(args.app_json)
    cli_notice = read_json(args.cli_json)
    quality_gate = read_json(args.quality_json)
    lanes = app_rows(app_gate) + cli_rows(cli_notice, quality_gate)
    overall_status = status_for(app_gate, cli_notice, quality_gate)
    payload = {
        "artifact_type": "five_lane_normalized_status_board",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": overall_status,
        "phase_advance_allowed": overall_status == "PASS_FIVE_LANE_READY",
        "next_manual_check_utc": args.next_manual_check_utc,
        "inputs": {
            "cadence_receipt": Path(args.cadence_json).name if args.cadence_json else None,
            "app_receipt": Path(args.app_json).name,
            "cli_receipt": Path(args.cli_json).name,
            "quality_receipt": Path(args.quality_json).name,
        },
        "cadence_status": cadence.get("overall_status"),
        "lanes": lanes,
        "claim_boundary": {
            "reads_curated_receipts_only": True,
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "external_account_mutation": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if overall_status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
