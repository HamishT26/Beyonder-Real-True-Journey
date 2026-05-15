#!/usr/bin/env python3
"""Run v281-v300 lane v1 phases, deferring the global v2 session until all v1 phases are done."""

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
STATUS = TRACE / f"{LANE}-v1-sequence-supervisor-status-v1.json"
STATUS_MD = TRACE / f"{LANE}-v1-sequence-supervisor-v1.md"
STOP_FILE = TRACE / f"{LANE}.stop"
PREP = ROOT / "scripts" / "trinity_v281_v300_double_phase_prep.py"
RUNNER = ROOT / "scripts" / "trinity_v281_v300_double_phase_runner.py"
GLOBAL_V2 = ROOT / "scripts" / "trinity_v281_v300_global_v2_prep.py"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
LANES = ("arby", "kimi", "aster-vale")


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


def run_checked(cmd: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def response_path(lane: str, phase: int, turn: int) -> Path:
    return LANE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def is_valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if "Max number of steps reached" in text or "To resume this session:" in text:
        return False
    labels = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")
    return sum(1 for label in labels if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def valid_phase_count(phase: int) -> int:
    count = 0
    for lane in LANES:
        for turn in range(1, 11):
            if is_valid_response(response_path(lane, phase, turn)):
                count += 1
    return count


def wait_for_phase(phase: int, timeout_sec: int, poll_sec: int, status: dict[str, Any]) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        count = valid_phase_count(phase)
        status["events"].append({"time": now_iso(), "phase": phase, "status": "wait_gate_poll", "valid_responses": count})
        status["updated_utc"] = now_iso()
        write_json(STATUS, status)
        write_md(status)
        if count >= 30:
            return True
        if STOP_FILE.exists():
            status["events"].append({"time": now_iso(), "phase": phase, "status": "wait_gate_stop_file"})
            return False
        time.sleep(max(1, poll_sec))
    return False


def write_md(status: dict[str, Any]) -> None:
    lines = [
        "# v281-v300 v1 Sequence Supervisor",
        "",
        f"Generated UTC: `{status.get('generated_utc')}`",
        f"Updated UTC: `{status.get('updated_utc')}`",
        f"Status: `{status.get('status')}`",
        f"Latest phase: `{status.get('latest_phase')}`",
        "",
        "Workflow:",
        "- Prepare each phase v1 prompt pack.",
        "- Run 10 Arby, 10 Kimi, and 10 Aster Vale sessions.",
        "- Do not run per-phase v2 as authority.",
        "- Prepare the global v2 session after all v1 phases are done.",
        "",
        "Recent events:",
    ]
    for event in status.get("events", [])[-16:]:
        lines.append(f"- `{event.get('time')}` v{event.get('phase')}: {event.get('status')}")
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def phase_prompt(phase: int) -> Path:
    return TRACE / f"{LANE}-phase-v{phase}-v1-prompts-v1.json"


def ensure_phase_prompt(phase: int, dependency: str, status: dict[str, Any]) -> bool:
    if phase_prompt(phase).exists():
        return True
    cmd = [
        sys.executable,
        str(PREP),
        "--source-phase",
        "v281-v300",
        "--source-dependency",
        dependency,
        "--phase",
        str(phase),
    ]
    proc = run_checked(cmd, timeout=600)
    status["events"].append(
        {
            "time": now_iso(),
            "phase": phase,
            "status": "prep_finished",
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    )
    return proc.returncode == 0 and phase_prompt(phase).exists()


def run_phase(phase: int, timeout_sec: int, kimi_max_steps: int, status: dict[str, Any]) -> bool:
    cmd = [
        sys.executable,
        str(RUNNER),
        "--phase",
        str(phase),
        "--timeout-sec",
        str(timeout_sec),
        "--status-id",
        "v1-sequence",
        "--max-turns-per-lane",
        "10",
        "--kimi-max-steps",
        str(kimi_max_steps),
    ]
    proc = run_checked(cmd, timeout=timeout_sec * 3 + 600)
    ok = proc.returncode == 0
    status["events"].append(
        {
            "time": now_iso(),
            "phase": phase,
            "status": "runner_finished" if ok else "runner_blocked",
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    )
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-phase", type=int, default=282)
    parser.add_argument("--end-phase", type=int, default=300)
    parser.add_argument("--timeout-sec", type=int, default=43200)
    parser.add_argument("--kimi-max-steps", type=int, default=6)
    parser.add_argument("--sleep-between-phases-sec", type=int, default=5)
    parser.add_argument("--prepare-global-v2", action="store_true")
    parser.add_argument("--wait-for-phase", type=int, default=0)
    parser.add_argument("--wait-timeout-sec", type=int, default=43200)
    parser.add_argument("--wait-poll-sec", type=int, default=180)
    args = parser.parse_args()

    status = read_json(
        STATUS,
        {
            "generated_utc": now_iso(),
            "phase_range": "v281-v300",
            "status_file": rel(STATUS),
            "events": [],
        },
    )
    status.update(
        {
            "updated_utc": now_iso(),
            "status": "running",
            "start_phase": args.start_phase,
            "end_phase": args.end_phase,
            "timeout_sec": args.timeout_sec,
            "stop_file": rel(STOP_FILE),
        }
    )
    if args.wait_for_phase:
        status["status"] = "waiting_for_prior_phase"
        status["latest_phase"] = args.wait_for_phase
        if not wait_for_phase(args.wait_for_phase, args.wait_timeout_sec, args.wait_poll_sec, status):
            status["status"] = "blocked_waiting_for_prior_phase"
            status["updated_utc"] = now_iso()
            write_json(STATUS, status)
            write_md(status)
            print(json.dumps({"status": status["status"], "latest_phase": args.wait_for_phase, "status_file": rel(STATUS)}, indent=2))
            return 1
        status["events"].append({"time": now_iso(), "phase": args.wait_for_phase, "status": "wait_gate_passed"})
        status["status"] = "running"
        write_json(STATUS, status)
        write_md(status)
    dependency = "docs/trinity-live-traces/v281-v300-double-trinity-global-v2-session-plan-v1.json"
    for phase in range(args.start_phase, args.end_phase + 1):
        status["latest_phase"] = phase
        if STOP_FILE.exists():
            status["status"] = "stopped_by_stop_file"
            status["events"].append({"time": now_iso(), "phase": phase, "status": "stop_file_detected"})
            break
        if not ensure_phase_prompt(phase, dependency, status):
            status["status"] = "blocked_prompt_prep"
            break
        write_json(STATUS, status)
        write_md(status)
        if not run_phase(phase, args.timeout_sec, args.kimi_max_steps, status):
            status["status"] = "blocked_phase_runner"
            break
        dependency = rel(phase_prompt(phase))
        status[f"phase_v{phase}_status"] = "v1_complete"
        status["updated_utc"] = now_iso()
        write_json(STATUS, status)
        write_md(status)
        time.sleep(max(0, args.sleep_between_phases_sec))
    else:
        status["status"] = "v1_sequence_complete"
        if args.prepare_global_v2:
            proc = run_checked([sys.executable, str(GLOBAL_V2), "--write-supervisor-candidate"], timeout=600)
            status["events"].append(
                {
                    "time": now_iso(),
                    "phase": args.end_phase,
                    "status": "global_v2_prepared",
                    "returncode": proc.returncode,
                    "stdout_tail": (proc.stdout or "")[-1000:],
                    "stderr_tail": (proc.stderr or "")[-1000:],
                }
            )
    status["updated_utc"] = now_iso()
    write_json(STATUS, status)
    write_md(status)
    print(json.dumps({"status": status["status"], "latest_phase": status.get("latest_phase"), "status_file": rel(STATUS)}, indent=2))
    return 0 if status["status"] == "v1_sequence_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
