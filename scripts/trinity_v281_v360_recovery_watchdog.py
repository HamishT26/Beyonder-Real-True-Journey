#!/usr/bin/env python3
"""Local watchdog for the v281-v360 recovery bridge.

This script is intentionally conservative: it only launches a repair when the
first incomplete v281-v300 phase has no active runner process and no fresh file
movement. It keeps the app automation as a wake channel, while this local
watchdog protects the filesystem/process side from stale-path app failures.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v281-v300-double-trinity"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
STATUS_JSON = TRACE / "v281-v360-recovery-watchdog-status-v1.json"
STATUS_MD = TRACE / "v281-v360-recovery-watchdog-status-v1.md"
REFRESHER = ROOT / "scripts" / "trinity_v281_v300_blocked_phase_refresher.py"
GLOBAL_V2 = ROOT / "scripts" / "trinity_v281_v300_global_v2_runner.py"
PHASES = range(281, 301)
LANES = ("arby", "kimi", "aster-vale")
LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")
EXECUTOR_PATTERN = r"trinity_v281_v300_(blocked_phase_refresher|v1_sequence_supervisor|double_phase_runner)"
GLOBAL_PATTERN = r"trinity_v281_v300_global_v2_runner"


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def now_iso() -> str:
    return now().isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def response_path(lane: str, phase: int, turn: int) -> Path:
    return LANE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    invalid = ("Max number of steps reached", "To resume this session:", "Traceback (most recent call last)")
    if any(marker in text for marker in invalid):
        return False
    return sum(1 for label in LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def phase_count(phase: int) -> dict[str, Any]:
    lanes: dict[str, Any] = {}
    for lane in LANES:
        valid = 0
        invalid: list[dict[str, Any]] = []
        for turn in range(1, 11):
            path = response_path(lane, phase, turn)
            if valid_response(path):
                valid += 1
            else:
                invalid.append(
                    {
                        "turn": turn,
                        "path": rel(path),
                        "exists": path.exists(),
                        "size": path.stat().st_size if path.exists() else 0,
                    }
                )
        lanes[lane] = {"valid": valid, "expected": 10, "invalid": invalid}
    total = sum(item["valid"] for item in lanes.values())
    return {"phase": phase, "valid": total, "expected": 30, "complete": total == 30, "lanes": lanes}


def all_counts() -> list[dict[str, Any]]:
    return [phase_count(phase) for phase in PHASES]


def powershell_processes(pattern: str) -> list[dict[str, Any]]:
    command = (
        "Get-CimInstance Win32_Process | "
        f"Where-Object {{ $_.CommandLine -match '{pattern}' }} | "
        "Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Depth 4"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    items = parsed if isinstance(parsed, list) else [parsed]
    filtered: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        command_line = str(item.get("CommandLine") or "")
        # Do not count this script's transient PowerShell process-inspection calls
        # as real runners/watchers just because their command text contains the
        # search pattern.
        if "Get-CimInstance Win32_Process" in command_line and "ConvertTo-Json" in command_line:
            continue
        filtered.append(item)
    return filtered


def phase_latest_mtime(phase: int) -> dt.datetime | None:
    paths = list(LANE_DIR.glob(f"*-phase-v{phase}-response-*.txt"))
    if not paths:
        return None
    latest = max(path.stat().st_mtime for path in paths)
    return dt.datetime.fromtimestamp(latest, tz=dt.timezone.utc)


def launch_detached(cmd: list[str], label: str) -> dict[str, Any]:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    stdout = TRACE / f"{label}-{stamp}.stdout.log"
    stderr = TRACE / f"{label}-{stamp}.stderr.log"
    stdout.parent.mkdir(parents=True, exist_ok=True)
    creationflags = 0
    popen_kwargs: dict[str, Any] = {}
    if sys.platform.startswith("win"):
        creationflags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        popen_kwargs["start_new_session"] = True
    with stdout.open("w", encoding="utf-8") as out, stderr.open("w", encoding="utf-8") as err:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=out, stderr=err, creationflags=creationflags, **popen_kwargs)
    return {"pid": proc.pid, "cmd": cmd, "stdout": rel(stdout), "stderr": rel(stderr)}


def write_status(status: dict[str, Any]) -> None:
    write_json(STATUS_JSON, status)
    lines = [
        "# v281-v360 Recovery Watchdog Status",
        "",
        f"Generated UTC: `{status.get('generated_utc')}`",
        f"Updated UTC: `{status.get('updated_utc')}`",
        f"Status: `{status.get('status')}`",
        f"Valid responses: `{status.get('valid_responses')}/{status.get('expected_responses')}`",
        f"First incomplete phase: `v{status.get('first_incomplete_phase')}`",
        "",
        "Recent events:",
    ]
    for event in status.get("events", [])[-12:]:
        detail = event.get("detail", "")
        lines.append(f"- `{event.get('time')}` {event.get('status')} {detail}".rstrip())
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_once(args: argparse.Namespace, status: dict[str, Any]) -> dict[str, Any]:
    counts = all_counts()
    valid = sum(item["valid"] for item in counts)
    expected = len(list(PHASES)) * 30
    first = next((item for item in counts if not item["complete"]), None)
    executors = powershell_processes(EXECUTOR_PATTERN)
    global_watchers = powershell_processes(GLOBAL_PATTERN)
    event: dict[str, Any] = {
        "time": now_iso(),
        "status": "checked",
        "valid_responses": valid,
        "expected_responses": expected,
        "executor_count": len(executors),
        "global_watcher_count": len(global_watchers),
    }

    if args.ensure_global_watch and valid < expected and not global_watchers:
        launched = launch_detached(
            [
                sys.executable,
                str(GLOBAL_V2),
                "--watch",
                "--poll-sec",
                "180",
                "--timeout-sec",
                "172800",
                "--write-supervisor-candidate",
                "--write-reactivation-packet-on-complete",
                "--reactivation-target-phase",
                "v301-v320",
            ],
            "v281-v360-watchdog-global-v2",
        )
        event["global_watcher_launch"] = launched

    if first is None:
        event["status"] = "v281_v300_complete"
    elif executors:
        event["status"] = "active_executor_present"
        event["detail"] = f"v{first['phase']} {first['valid']}/30"
    else:
        phase = int(first["phase"])
        latest_mtime = phase_latest_mtime(phase)
        stale = latest_mtime is None or (now() - latest_mtime).total_seconds() >= args.stale_minutes * 60
        event["status"] = "incomplete_without_executor"
        event["detail"] = f"v{phase} {first['valid']}/30 stale={stale}"
        event["latest_phase_file_utc"] = latest_mtime.isoformat() if latest_mtime else None
        if args.repair and stale:
            event["status"] = "repair_launched"
            event["repair_launch"] = launch_detached(
                [
                    sys.executable,
                    str(REFRESHER),
                    "--phase",
                    str(phase),
                    "--end-phase",
                    "300",
                    "--timeout-sec",
                    "43200",
                    "--kimi-max-steps",
                    "6",
                    "--max-attempts",
                    str(args.max_attempts),
                    "--resume-sequence",
                ],
                f"v281-v360-watchdog-repair-v{phase}",
            )

    status.update(
        {
            "updated_utc": now_iso(),
            "status": event["status"],
            "valid_responses": valid,
            "expected_responses": expected,
            "first_incomplete_phase": first["phase"] if first else None,
            "phase_counts": counts,
            "executor_processes": executors,
            "global_watcher_processes": global_watchers,
        }
    )
    status.setdefault("events", []).append(event)
    write_status(status)
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--poll-sec", type=int, default=300)
    parser.add_argument("--stale-minutes", type=int, default=20)
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--ensure-global-watch", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=6)
    args = parser.parse_args()

    status: dict[str, Any] = {
        "generated_utc": now_iso(),
        "updated_utc": now_iso(),
        "status": "running" if args.watch else "single_check",
        "events": [],
        "stale_minutes": args.stale_minutes,
        "repair_enabled": args.repair,
        "ensure_global_watch": args.ensure_global_watch,
    }
    while True:
        run_once(args, status)
        if not args.watch:
            break
        time.sleep(max(30, args.poll_sec))
    print(json.dumps({"status": status["status"], "valid": status.get("valid_responses"), "expected": status.get("expected_responses"), "status_file": rel(STATUS_JSON)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
