#!/usr/bin/env python3
"""Aggregate five-lane timing receipts into a soft timeout baseline."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def receipt_paths(args: argparse.Namespace) -> list[Path]:
    if args.receipt:
        return [Path(item) for item in args.receipt]
    return sorted(TRACE_DIR.glob(args.glob))


def duration_rows(receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for receipt in receipts:
        for lane in receipt.get("lanes", []):
            if not isinstance(lane, dict):
                continue
            duration = lane.get("duration_seconds")
            if not isinstance(duration, (int, float)):
                continue
            rows.append(
                {
                    "phase_slug": receipt.get("phase_slug"),
                    "observation_run_index_today": receipt.get("observation_run_index_today"),
                    "lane": lane.get("lane"),
                    "platform": lane.get("platform"),
                    "duration_seconds": round(float(duration), 3),
                    "completion_type": lane.get("completion_type"),
                    "timing_basis": lane.get("timing_basis"),
                }
            )
    return rows


def mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 3)


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    paths = [path for path in receipt_paths(args) if path.exists()]
    receipts = [read_json(path) for path in paths]
    rows = duration_rows(receipts)
    unique_runs = sorted({row.get("observation_run_index_today") for row in rows if row.get("observation_run_index_today") is not None})
    lane_names = sorted({str(row.get("lane")) for row in rows if row.get("lane")})
    values = [float(row["duration_seconds"]) for row in rows]
    payload: dict[str, Any] = {
        "artifact_type": "five_lane_timing_baseline",
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "READY_THREE_RUN_BASELINE" if len(unique_runs) >= args.required_runs else "PENDING_MORE_OBSERVATIONS",
        "required_runs": args.required_runs,
        "observed_run_count": len(unique_runs),
        "observed_lane_count": len(rows),
        "lane_names": lane_names,
        "average_response_seconds": mean(values),
        "soft_timeout_rule": "Use only as a practical waiting baseline; never as a substitute for a final marker or completion receipt.",
        "receipt_files": [path.name for path in paths],
        "rows": rows,
        "claim_boundary": {
            "scope": "timing baseline only",
            "completion_substitute": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(TRACE_DIR / f"{args.receipt_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.receipt_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Five-Lane Timing Baseline",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- required_runs: `{payload['required_runs']}`",
        f"- observed_run_count: `{payload['observed_run_count']}`",
        f"- observed_lane_count: `{payload['observed_lane_count']}`",
        f"- average_response_seconds: `{payload['average_response_seconds']}`",
        "- soft timeout rule: use only as a practical waiting baseline; never as a substitute for a final marker or completion receipt.",
        "",
        "## Receipts",
    ]
    for name in payload["receipt_files"]:
        lines.append(f"- `{name}`")
    lines.append("")
    lines.append("## Lane Rows")
    for row in payload["rows"]:
        lines.append(
            f"- {row['phase_slug']} run {row['observation_run_index_today']} {row['lane']}: "
            f"`{row['duration_seconds']}` seconds via `{row['timing_basis']}`."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--glob", default="v478-thos-v14-*-five-lane-timing-v1.json")
    parser.add_argument("--receipt", action="append", help="Explicit timing receipt path. Repeat for multiple receipts.")
    parser.add_argument("--required-runs", type=int, default=3)
    parser.add_argument("--receipt-prefix", default="v478-thos-five-lane-timing-baseline")
    return parser.parse_args()


def main() -> int:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "average": payload["average_response_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
