#!/usr/bin/env python3
r"""Check Codex Desktop resume-path mismatches without editing session logs.

The Codex app can sometimes report a stale resume path when the requested
session path uses the normal Win32 form (C:\...) and the active session path
uses the extended-length form (\\?\C:\...). Those can point to the same JSONL.
This script records that as an app resume-path vitality issue, not a repo
failure, and never modifies the session JSONL.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
OUT_JSON = TRACE / "v281-v360-resume-path-vitality-check-v1.json"
OUT_MD = TRACE / "v281-v360-resume-path-vitality-check-v1.md"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_windows_path(value: str) -> str:
    text = value.strip().strip("`\"'")
    text = text.replace("/", "\\")
    if text.startswith("\\\\?\\UNC\\"):
        text = "\\\\" + text[len("\\\\?\\UNC\\") :]
    elif text.startswith("\\\\?\\"):
        text = text[len("\\\\?\\") :]
    return text.lower()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# v281-v360 Resume Path Vitality Check",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Automation ID: `{payload['automation_id']}`",
        f"Thread ID: `{payload['thread_id']}`",
        "",
        "Requested path:",
        f"- `{payload['requested_path']}`",
        "",
        "Active path:",
        f"- `{payload['active_path']}`",
        "",
        "Interpretation:",
        f"- {payload['interpretation']}",
        "",
        "Operator action:",
    ]
    for item in payload["operator_actions"]:
        lines.append(f"- {item}")
    lines.extend(["", "Truth boundaries:"])
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    requested_norm = normalize_windows_path(args.requested_path)
    active_norm = normalize_windows_path(args.active_path)
    same_session = requested_norm == active_norm
    status = "same_session_path_normalized" if same_session else "different_session_paths"
    return {
        "generated_utc": now_iso(),
        "automation_id": args.automation_id,
        "thread_id": args.thread_id,
        "status": status,
        "requested_path": args.requested_path,
        "active_path": args.active_path,
        "requested_normalized": requested_norm,
        "active_normalized": active_norm,
        "same_session_after_normalization": same_session,
        "interpretation": (
            "The paths normalize to the same session JSONL. Treat this as Codex Desktop resume-path vitality, not a repo failure."
            if same_session
            else "The paths do not normalize to the same session JSONL. Verify the active thread before resuming automation."
        ),
        "operator_actions": [
            "Do not edit the session JSONL by hand.",
            "Keep the local watchdog as the filesystem/process safety net while app wake is paused.",
            "If the stale-path error repeats after reopening the automation, restart Codex Desktop and reopen the Aletheon thread.",
            "Keep the laptop fully awake during unattended automation; partial lid closure can suspend or throttle the app wake path.",
        ],
        "truth_boundaries": [
            "This check records path equivalence only; it does not repair Codex Desktop internals.",
            "Repository artifacts remain valid when the stale path normalizes to the same JSONL.",
            "The chat-attached heartbeat is the app wake layer; local scripts remain the filesystem/process watchdog layer.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requested-path", required=True)
    parser.add_argument("--active-path", required=True)
    parser.add_argument("--automation-id", default="aletheon")
    parser.add_argument("--thread-id", default="unknown")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args)
    if args.write_report:
        write_json(OUT_JSON, payload)
        write_md(OUT_MD, payload)
    print(json.dumps({"status": payload["status"], "report": str(OUT_JSON) if args.write_report else None}, indent=2))
    return 0 if payload["same_session_after_normalization"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
