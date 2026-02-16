#!/usr/bin/env python3
"""
Build an end-of-day handoff snapshot across Mind/Body/Heart tracks.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _read_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"status": "MISSING", "path": str(path)}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "ERROR", "path": str(path), "detail": f"invalid_json: {exc}"}
    if isinstance(payload, dict):
        return payload
    return {"status": "ERROR", "path": str(path), "detail": "payload_not_object"}


def _status_from(payload: Dict[str, object], default: str = "UNKNOWN") -> str:
    for key in ("overall_status", "status"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().upper()
    if payload.get("effective_success") is True:
        return "PASS"
    if payload.get("effective_success") is False:
        return "FAIL"
    return default


def _collect(root: Path) -> Dict[str, object]:
    targets = {
        "suite": root / "docs/system-suite-status.json",
        "body_benchmark": root / "docs/body-track-benchmark-latest.json",
        "body_trend_guard": root / "docs/body-track-trend-guard-latest.json",
        "body_calibration": root / "docs/body-track-calibration-latest.json",
        "heart_gov002_standard": root / "docs/heart-track-min-disclosure-latest.json",
        "heart_gov002_live": root / "docs/heart-track-min-disclosure-live-latest.json",
        "heart_gov002_adversarial": root / "docs/heart-track-min-disclosure-adversarial-latest.json",
        "heart_gov003": root / "docs/heart-track-auditability-latest.json",
        "heart_gov004_standard": root / "docs/heart-track-dispute-recourse-latest.json",
        "heart_gov004_adversarial": root / "docs/heart-track-dispute-recourse-adversarial-latest.json",
        "heart_gov005": root / "docs/heart-track-governance-latest.json",
        "mind_comparator": root / "docs/mind-track-gmut-comparator-latest.json",
        "mind_anchor_exclusion": root / "docs/mind-track-gmut-anchor-exclusion-latest.json",
    }
    snapshots: Dict[str, Dict[str, object]] = {}
    for key, path in targets.items():
        raw = _read_json(path)
        snapshots[key] = {
            "path": str(path.relative_to(root)),
            "status": _status_from(raw),
            "payload": raw,
        }

    core_statuses: List[str] = [str(item["status"]) for item in snapshots.values()]
    if any(status in {"FAIL", "ERROR"} for status in core_statuses):
        session_status = "ATTENTION"
    elif any(status in {"WARN", "MISSING", "UNKNOWN"} for status in core_statuses):
        session_status = "STABLE_WITH_GAPS"
    else:
        session_status = "PASS"

    return {
        "session_status": session_status,
        "snapshots": snapshots,
    }


def _markdown(payload: Dict[str, object]) -> str:
    snapshots = payload["snapshots"]
    rows = []
    for key in (
        "suite",
        "body_benchmark",
        "body_trend_guard",
        "body_calibration",
        "heart_gov002_standard",
        "heart_gov002_live",
        "heart_gov002_adversarial",
        "heart_gov003",
        "heart_gov004_standard",
        "heart_gov004_adversarial",
        "heart_gov005",
        "mind_comparator",
        "mind_anchor_exclusion",
    ):
        item = snapshots[key]
        rows.append(f"| {key} | {item['status']} | `{item['path']}` |")

    return "\n".join(
        [
            "# Nightly Handoff Snapshot",
            "",
            f"- generated_utc: `{payload['generated_utc']}`",
            f"- session_label: `{payload['session_label']}`",
            f"- session_status: **{payload['session_status']}**",
            "",
            "## Track artifact statuses",
            "| artifact | status | path |",
            "|---|---|---|",
            *rows,
            "",
            "## Next-launch focus",
            "1. Heart: progress GOV-004 from callback-level checks to DID-method signature verification.",
            "2. Body: test selective policy updates and publish before/after false-alert deltas.",
            "3. Mind: attach source-side extraction artifacts and uncertainty equations per trace ID.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate nightly handoff snapshot artifact.")
    parser.add_argument("--session-label", default="nz-monday-night-closeout")
    parser.add_argument("--reports-dir", default="docs/nightly-handoffs")
    parser.add_argument("--latest-json", default="docs/nightly-handoff-latest.json")
    parser.add_argument("--latest-md", default="docs/nightly-handoff-latest.md")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    collected = _collect(root)
    payload: Dict[str, object] = {
        "generated_utc": generated_utc,
        "session_label": args.session_label,
        "session_status": collected["session_status"],
        "snapshots": collected["snapshots"],
    }
    markdown = _markdown(payload)

    reports_dir = root / args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = root / args.latest_json
    latest_md = root / args.latest_md
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json = reports_dir / f"{stamp}-nightly-handoff.json"
    timestamped_md = reports_dir / f"{stamp}-nightly-handoff.md"
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"session_status={payload['session_status']}")
    print(f"timestamped_json={timestamped_json.relative_to(root)}")
    print(f"timestamped_md={timestamped_md.relative_to(root)}")
    print(f"latest_json={latest_json.relative_to(root)}")
    print(f"latest_md={latest_md.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
