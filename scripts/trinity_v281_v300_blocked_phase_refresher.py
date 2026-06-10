#!/usr/bin/env python3
"""Repair blocked v281-v300 phase runners without overwriting valid lane replies."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v281-v300-double-trinity"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
SEQUENCE_STATUS = TRACE / f"{LANE}-v1-sequence-supervisor-status-v1.json"
REFRESH_STATUS = TRACE / f"{LANE}-blocked-phase-refresh-status-v1.json"
REFRESH_MD = TRACE / f"{LANE}-blocked-phase-refresh-status-v1.md"
RUNNER = ROOT / "scripts" / "trinity_v281_v300_double_phase_runner.py"
SEQUENCE = ROOT / "scripts" / "trinity_v281_v300_v1_sequence_supervisor.py"
LANES = ("arby", "kimi", "aster-vale")
RUNNER_LANE = {"arby": "arby", "kimi": "kimi", "aster-vale": "aster_vale"}
LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def phase_counts(phase: int) -> dict[str, Any]:
    lanes: dict[str, Any] = {}
    for lane in LANES:
        invalid = []
        valid = 0
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


def latest_blocked_phase() -> int:
    status = read_json(SEQUENCE_STATUS, {})
    latest = status.get("latest_phase")
    if isinstance(latest, int):
        return latest
    events = [event for event in status.get("events", []) if isinstance(event.get("phase"), int)]
    return int(events[-1]["phase"]) if events else 281


def run_command(cmd: list[str], timeout: int) -> dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-1600:],
        "stderr_tail": (proc.stderr or "")[-1600:],
    }


def write_status(status: dict[str, Any]) -> None:
    write_json(REFRESH_STATUS, status)
    lines = [
        "# v281-v300 Blocked Phase Refresh Status",
        "",
        f"Generated UTC: `{status.get('generated_utc')}`",
        f"Updated UTC: `{status.get('updated_utc')}`",
        f"Status: `{status.get('status')}`",
        f"Phase: `v{status.get('phase')}`",
        f"Completion: `{status.get('valid')}/{status.get('expected')}`",
        "",
        "Recent events:",
    ]
    for event in status.get("events", [])[-12:]:
        lines.append(f"- `{event.get('time')}` {event.get('status')} {event.get('detail', '')}".rstrip())
    REFRESH_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def repair_phase(phase: int, timeout_sec: int, kimi_max_steps: int, max_attempts: int) -> dict[str, Any]:
    status: dict[str, Any] = {
        "generated_utc": now_iso(),
        "updated_utc": now_iso(),
        "phase_range": "v281-v300",
        "phase": phase,
        "status": "running",
        "events": [],
    }
    for attempt in range(1, max_attempts + 1):
        before = phase_counts(phase)
        status.update({"valid": before["valid"], "expected": before["expected"], "phase_counts": before, "updated_utc": now_iso()})
        if before["complete"]:
            status["status"] = "phase_already_complete"
            write_status(status)
            return status
        lanes_to_repair = [lane for lane, item in before["lanes"].items() if item["valid"] < item["expected"]]
        status["events"].append(
            {
                "time": now_iso(),
                "status": "repair_attempt",
                "detail": f"attempt={attempt} lanes={','.join(lanes_to_repair)} valid={before['valid']}/30",
            }
        )
        write_status(status)
        for lane in lanes_to_repair:
            cmd = [
                sys.executable,
                str(RUNNER),
                "--phase",
                str(phase),
                "--timeout-sec",
                str(timeout_sec),
                "--status-id",
                f"blocked-refresh-v{phase}-{lane}-attempt-{attempt}",
                "--max-turns-per-lane",
                "10",
                "--only-lane",
                RUNNER_LANE[lane],
                "--kimi-max-steps",
                str(kimi_max_steps),
            ]
            result = run_command(cmd, timeout=timeout_sec * 2 + 600)
            status["events"].append(
                {
                    "time": now_iso(),
                    "status": "lane_refresh_finished",
                    "detail": f"lane={lane} attempt={attempt} returncode={result['returncode']}",
                    **result,
                }
            )
            status["updated_utc"] = now_iso()
            write_status(status)
        after = phase_counts(phase)
        status.update({"valid": after["valid"], "expected": after["expected"], "phase_counts": after, "updated_utc": now_iso()})
        if after["complete"]:
            status["status"] = "phase_repaired"
            write_status(status)
            return status
    status["status"] = "blocked_after_refresh_attempts"
    write_status(status)
    return status


def resume_sequence(start_phase: int, end_phase: int, timeout_sec: int, kimi_max_steps: int, refresh_max_attempts: int) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(SEQUENCE),
        "--start-phase",
        str(start_phase),
        "--end-phase",
        str(end_phase),
        "--timeout-sec",
        str(timeout_sec),
        "--kimi-max-steps",
        str(kimi_max_steps),
        "--sleep-between-phases-sec",
        "5",
        "--prepare-global-v2",
        "--auto-refresh-blocked",
        "--refresh-max-attempts",
        str(refresh_max_attempts),
    ]
    return run_command(cmd, timeout=timeout_sec * 3 + 600)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=0)
    parser.add_argument("--end-phase", type=int, default=300)
    parser.add_argument("--timeout-sec", type=int, default=36000)
    parser.add_argument("--kimi-max-steps", type=int, default=6)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--resume-sequence", action="store_true")
    args = parser.parse_args()

    phase = args.phase or latest_blocked_phase()
    status = repair_phase(phase, args.timeout_sec, args.kimi_max_steps, args.max_attempts)
    if status["status"] == "phase_repaired" and args.resume_sequence and phase < args.end_phase:
        result = resume_sequence(phase + 1, args.end_phase, args.timeout_sec, args.kimi_max_steps, args.max_attempts)
        status["events"].append(
            {
                "time": now_iso(),
                "status": "sequence_resume_launched",
                "detail": f"start_phase={phase + 1} end_phase={args.end_phase} returncode={result['returncode']}",
                **result,
            }
        )
        status["updated_utc"] = now_iso()
        status["sequence_resume"] = result
        write_status(status)
    print(json.dumps({"status": status["status"], "phase": phase, "valid": status.get("valid"), "expected": status.get("expected"), "status_file": rel(REFRESH_STATUS)}, indent=2))
    return 0 if status["status"] in {"phase_repaired", "phase_already_complete"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
