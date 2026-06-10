#!/usr/bin/env python3
"""Guard phase status checks against premature lane babysitting."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_utc(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a lane harvest is allowed by cadence policy.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--boundary", choices=["x1", "x2"], required=True)
    parser.add_argument("--started-utc", required=True)
    parser.add_argument("--now-utc")
    parser.add_argument("--threshold-minutes", type=int)
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    args = parser.parse_args()

    started = parse_utc(args.started_utc)
    now = parse_utc(args.now_utc) if args.now_utc else datetime.now(timezone.utc)
    elapsed_seconds = max(0, int((now - started).total_seconds()))
    threshold_minutes = args.threshold_minutes if args.threshold_minutes is not None else 15
    if threshold_minutes <= 0:
        raise SystemExit("--threshold-minutes must be positive")
    threshold_seconds = threshold_minutes * 60
    allowed = elapsed_seconds >= threshold_seconds
    receipt = {
        "artifact_type": "status_check_cadence_guard",
        "phase_slug": args.phase_slug,
        "boundary": args.boundary,
        "generated_utc": now.replace(microsecond=0).isoformat(),
        "started_utc": started.replace(microsecond=0).isoformat(),
        "elapsed_seconds": elapsed_seconds,
        "threshold_seconds": threshold_seconds,
        "status_check_allowed": allowed,
        "overall_status": "PASS_STATUS_CHECK_ALLOWED" if allowed else "OPEN_GAP_WAIT_FOR_CADENCE_MARK",
        "claim_boundary": {
            "does_not_harvest_lane_status": True,
            "raw_lane_text_published": False,
            "raw_transport_published": False,
        },
    }
    if args.receipt_json:
        Path(args.receipt_json).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if args.receipt_md:
        lines = [
            f"# {args.phase_slug} Status Check Cadence Guard",
            "",
            f"- Boundary: `{args.boundary}`",
            f"- Status: `{receipt['overall_status']}`",
            f"- Started UTC: `{receipt['started_utc']}`",
            f"- Generated UTC: `{receipt['generated_utc']}`",
            f"- Elapsed seconds: `{receipt['elapsed_seconds']}`",
            f"- Threshold seconds: `{receipt['threshold_seconds']}`",
            f"- Status check allowed: `{str(receipt['status_check_allowed']).lower()}`",
            "",
            "This receipt records the cadence gate only. It does not harvest lane status, publish raw lane text, or read raw transport.",
            "",
        ]
        Path(args.receipt_md).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
