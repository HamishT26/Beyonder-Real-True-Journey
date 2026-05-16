#!/usr/bin/env python3
"""Summarize the v281-v360 automation and runner health without starting phases."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
OUT_JSON = TRACE / "v281-v360-automation-health-check-v1.json"
OUT_MD = TRACE / "v281-v360-automation-health-check-v1.md"
START_GATE_SCRIPT = ROOT / "scripts" / "trinity_v301_v320_start_gate.py"
START_GATE = TRACE / "v301-v320-start-gate-status-v1.json"
PHASE_296_STATUS = TRACE / "v281-v300-double-trinity-phase-v296-runner-status-v1-sequence.json"
SUPERVISOR_STATUS = TRACE / "v281-v300-double-trinity-v1-sequence-supervisor-status-v1.json"
AUTOMATION_DIR = Path.home() / ".codex" / "automations" / "grand-v281-to-v360-beta-alpha-omega-trinity-hybrid-os"
AUTOMATION_TOML = AUTOMATION_DIR / "automation.toml"
AUTOMATION_MEMORY = AUTOMATION_DIR / "memory.md"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def refresh_gate() -> None:
    subprocess.run(
        [sys.executable, str(START_GATE_SCRIPT)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )


def process_snapshot() -> list[dict[str, Any]]:
    if not sys.platform.startswith("win"):
        return []
    pattern = (
        "trinity_v281_v300_v1_sequence_supervisor.py|"
        "trinity_v281_v300_double_phase_runner.py|"
        "trinity_v281_v300_global_v2_runner.py|"
        "trinity_aletheon_wake_signal_poller.py|"
        "kimi --work-dir|codex exec"
    )
    command = (
        "Get-CimInstance Win32_Process | "
        f"Where-Object {{ $_.Name -match 'python|kimi|codex' -and ($_.CommandLine -match '{pattern}') }} | "
        "Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Depth 3"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = [data]
    return [
        {
            "pid": item.get("ProcessId"),
            "parent_pid": item.get("ParentProcessId"),
            "name": item.get("Name"),
            "command": item.get("CommandLine"),
        }
        for item in data
        if isinstance(item, dict)
    ]


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.refresh_gate:
        refresh_gate()
    automation = read_toml(AUTOMATION_TOML)
    gate = read_json(START_GATE, {})
    phase_296 = read_json(PHASE_296_STATUS, {})
    supervisor = read_json(SUPERVISOR_STATUS, {})
    processes = process_snapshot()
    cwds = automation.get("cwds") or []
    root_text = str(ROOT)
    cwd_mentions_root = any(str(cwd).lower() == root_text.lower() for cwd in cwds)
    paused = automation.get("status") == "PAUSED"
    ready = bool(gate.get("ready"))
    valid = gate.get("valid_responses")
    expected = gate.get("expected_responses")
    global_v2_complete = gate.get("global_v2_complete")
    if global_v2_complete is None:
        blockers = gate.get("blockers") or []
        global_v2_complete = not any("global v2" in str(item).lower() for item in blockers)
    findings: list[str] = []
    if paused:
        findings.append("Automation config status is PAUSED; activate through the Codex app UI rather than editing TOML directly.")
    if not cwd_mentions_root:
        findings.append("Automation cwd is not the D: worktree; keep the prompt's explicit D: worktree instruction, and choose the D: project/worktree in the UI if available.")
    if not ready:
        findings.append("v301-v320 is not ready; automation should report standby only.")
    if processes:
        findings.append("Local supervisor/watcher processes are present.")
    else:
        findings.append("No local runner processes matched the health pattern; inspect before assuming background progress.")
    return {
        "generated_utc": now_iso(),
        "status": "ready_to_start_v301" if ready else "standby",
        "automation": {
            "path": str(AUTOMATION_TOML),
            "exists": AUTOMATION_TOML.exists(),
            "memory_path": str(AUTOMATION_MEMORY),
            "memory_exists": AUTOMATION_MEMORY.exists(),
            "name": automation.get("name"),
            "kind": automation.get("kind"),
            "status": automation.get("status"),
            "rrule": automation.get("rrule"),
            "model": automation.get("model"),
            "reasoning_effort": automation.get("reasoning_effort"),
            "execution_environment": automation.get("execution_environment"),
            "cwds": cwds,
            "cwd_mentions_target_worktree": cwd_mentions_root,
        },
        "gate": {
            "path": rel(START_GATE),
            "ready": gate.get("ready"),
            "status": gate.get("status"),
            "valid_responses": valid,
            "expected_responses": expected,
            "complete_phases": gate.get("complete_phases"),
            "expected_phases": gate.get("expected_phases"),
            "first_incomplete_phase": gate.get("first_incomplete_phase"),
            "global_v2_complete": global_v2_complete,
        },
        "phase_296": {
            "path": rel(PHASE_296_STATUS),
            "status": phase_296.get("status"),
            "completed_for_phase": phase_296.get("completed_for_phase"),
            "active_lane": phase_296.get("active_lane"),
            "active_turn": phase_296.get("active_turn"),
        },
        "supervisor": {
            "path": rel(SUPERVISOR_STATUS),
            "status": supervisor.get("status"),
            "latest_phase": supervisor.get("latest_phase"),
        },
        "processes": processes,
        "findings": findings,
        "recommended_action": (
            "If the app UI shows PAUSED, unpause it. Do not start v301-v320 until gate.ready is true. "
            "If the UI lets you pick the D: worktree as the project, prefer that; otherwise keep the explicit D: path in the prompt."
        ),
    }


def write_md(payload: dict[str, Any]) -> None:
    gate = payload["gate"]
    automation = payload["automation"]
    lines = [
        "# v281-v360 Automation Health Check",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Automation:",
        f"- Status: `{automation.get('status')}`",
        f"- Schedule: `{automation.get('rrule')}`",
        f"- Model: `{automation.get('model')}` / `{automation.get('reasoning_effort')}`",
        f"- CWD includes target worktree: `{automation.get('cwd_mentions_target_worktree')}`",
        "",
        "Gate:",
        f"- Ready: `{gate.get('ready')}`",
        f"- Responses: `{gate.get('valid_responses')}/{gate.get('expected_responses')}`",
        f"- Complete phases: `{gate.get('complete_phases')}/{gate.get('expected_phases')}`",
        f"- First incomplete phase: `v{gate.get('first_incomplete_phase')}`",
        f"- Global v2 complete: `{gate.get('global_v2_complete')}`",
        "",
        "Findings:",
    ]
    for finding in payload["findings"]:
        lines.append(f"- {finding}")
    lines.extend(["", "Recommended action:", f"- {payload['recommended_action']}"])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-gate", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args)
    write_json(OUT_JSON, payload)
    write_md(payload)
    print(json.dumps({"status": payload["status"], "health": rel(OUT_JSON)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
