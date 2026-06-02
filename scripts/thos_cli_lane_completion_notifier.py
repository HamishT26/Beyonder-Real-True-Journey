#!/usr/bin/env python3
"""Watch Codex CLI advisory lane outputs and write curated completion notices."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LANES = ["Arby", "Aster Vale"]
ARTIFACT_ROOT = Path(__file__).resolve().parents[1] / "docs" / "trinity-live-traces"
SENSITIVE_PATTERNS = [
    "BEGIN " + "RSA",
    "BEGIN " + "OPENSSH",
    "api" + r"[_-]?" + "key",
    "sec" + "ret",
    "pass" + "word",
    "to" + "ken",
]
SENSITIVE_RE = re.compile("|".join(SENSITIVE_PATTERNS), re.IGNORECASE)
TRANSPORT_RE = re.compile(r"exec\n|succeeded in|ERROR|WARN", re.IGNORECASE)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def byte_count(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def lane_snapshot(output_dir: Path, lane: str) -> dict[str, Any]:
    final_path = output_dir / f"{lane}-last-message.txt"
    stdout_path = output_dir / f"{lane}-stdout.txt"
    stderr_path = output_dir / f"{lane}-stderr.txt"
    final_text = read_optional(final_path)
    stderr_text = read_optional(stderr_path)
    return {
        "completion_status": "FINAL_MESSAGE_READY" if final_text else "WAITING_FOR_FINAL_MESSAGE",
        "final_message_bytes": byte_count(final_path),
        "final_message_hash": sha256_text(final_text) if final_text else None,
        "final_message_sensitive_marker_count": len(SENSITIVE_RE.findall(final_text)),
        "lane": lane,
        "raw_output_boundary": "temp_only_not_published",
        "stderr_bytes": byte_count(stderr_path),
        "stderr_sensitive_marker_count_unpublished": len(SENSITIVE_RE.findall(stderr_text)),
        "stderr_transport_marker_count_unpublished": len(TRANSPORT_RE.findall(stderr_text)),
        "stdout_bytes": byte_count(stdout_path),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Lane Completion Notice",
        "",
        f"Generated UTC: `{payload['generated_at_utc']}`",
        f"Status: `{payload['aggregate_status']}`",
        "",
        "Lane snapshots:",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane['completion_status']}`, final bytes `{lane['final_message_bytes']}`, raw output `{lane['raw_output_boundary']}`"
        )
    lines.extend(
        [
            "",
            "This notice records completion markers only. It does not publish raw lane transport.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_notice(output_dir: Path, lanes: list[str], phase_slug: str, started_at: str) -> dict[str, Any]:
    snapshots = [lane_snapshot(output_dir, lane) for lane in lanes]
    all_ready = all(item["completion_status"] == "FINAL_MESSAGE_READY" for item in snapshots)
    sensitive_in_final = sum(item["final_message_sensitive_marker_count"] for item in snapshots)
    return {
        "aggregate_status": (
            "FINAL_MESSAGES_READY"
            if all_ready and sensitive_in_final == 0
            else "OPEN_GAP_FINAL_MESSAGE_PENDING"
            if not all_ready
            else "FAIL_BLOCKER_FINAL_MESSAGE_MARKER"
        ),
        "generated_at_utc": utc_now(),
        "lanes": snapshots,
        "mutation_performed": False,
        "output_dir": "<local_temp_redacted>",
        "phase_slug": phase_slug,
        "started_at_utc": started_at,
    }


def watch(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output_dir)
    lanes = args.lane or DEFAULT_LANES
    started_at = utc_now()
    deadline = time.monotonic() + args.timeout_seconds
    notice = build_notice(output_dir, lanes, args.phase_slug, started_at)
    while time.monotonic() <= deadline:
        notice = build_notice(output_dir, lanes, args.phase_slug, started_at)
        if notice["aggregate_status"] == "FINAL_MESSAGES_READY":
            return notice
        if args.once:
            return notice
        time.sleep(args.poll_seconds)
    notice = build_notice(output_dir, lanes, args.phase_slug, started_at)
    if notice["aggregate_status"] != "FINAL_MESSAGES_READY":
        notice["aggregate_status"] = "OPEN_GAP_WATCH_TIMEOUT"
    return notice


def main() -> int:
    parser = argparse.ArgumentParser(description="Write curated completion notices for CLI advisory lanes.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--phase-slug", default="v472-thos-v5-x2")
    parser.add_argument("--lane", action="append", help="Lane name. Repeat for multiple lanes.")
    parser.add_argument("--poll-seconds", type=float, default=30.0)
    parser.add_argument("--timeout-seconds", type=float, default=3600.0)
    parser.add_argument("--once", action="store_true", help="Inspect once and write a notice immediately.")
    parser.add_argument("--receipt-json", default=str(ARTIFACT_ROOT / "v472-thos-v5-x2-cli-lane-completion-notice-v1.json"))
    parser.add_argument("--receipt-md", default=str(ARTIFACT_ROOT / "v472-thos-v5-x2-cli-lane-completion-notice-v1.md"))
    args = parser.parse_args()

    notice = watch(args)
    write_json(Path(args.receipt_json), notice)
    write_md(Path(args.receipt_md), notice)
    print(json.dumps(notice, indent=2, sort_keys=True))
    return 0 if notice["aggregate_status"] == "FINAL_MESSAGES_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
