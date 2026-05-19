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
V301_RUN_STATUS = TRACE / "v301-v320-aletheon-run-status-v1.json"
V321_HANDOFF = TRACE / "v321-v340-sibling-handoff-v1.json"
V321_RUN_STATUS = TRACE / "v321-v340-sibling-run-status-v1.json"
V341_HANDOFF = TRACE / "v341-v360-final-handoff-v1.json"
V341_RUN_STATUS = TRACE / "v341-v360-sibling-run-status-v1.json"
PHASE_296_STATUS = TRACE / "v281-v300-double-trinity-phase-v296-runner-status-v1-sequence.json"
SUPERVISOR_STATUS = TRACE / "v281-v300-double-trinity-v1-sequence-supervisor-status-v1.json"
AUTOMATION_BASE = Path.home() / ".codex" / "automations"
PRIMARY_AUTOMATION_ID = "aletheon"
SECONDARY_AUTOMATION_ID = "grand-v281-to-v360-beta-alpha-omega-trinity-hybrid-os"
TARGET_CHAT_HEARTBEAT_MINUTES = 30


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
        "trinity_v281_v360_recovery_watchdog.py|"
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


def parse_interval_minutes(rrule: str | None) -> int | None:
    if not rrule:
        return None
    parts: dict[str, str] = {}
    for item in rrule.replace("RRULE:", "").split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            parts[key] = value
    try:
        interval = int(parts.get("INTERVAL", "1"))
    except ValueError:
        return None
    freq = parts.get("FREQ")
    if freq == "MINUTELY":
        return interval
    if freq == "HOURLY":
        return interval * 60
    return None


def automation_record(automation_id: str) -> dict[str, Any]:
    directory = AUTOMATION_BASE / automation_id
    toml_path = directory / "automation.toml"
    memory_path = directory / "memory.md"
    config = read_toml(toml_path)
    cwds = config.get("cwds") or []
    root_text = str(ROOT)
    cwd_mentions_root = any(str(cwd).lower() == root_text.lower() for cwd in cwds)
    return {
        "id": automation_id,
        "path": str(toml_path),
        "exists": toml_path.exists(),
        "memory_path": str(memory_path),
        "memory_exists": memory_path.exists(),
        "name": config.get("name"),
        "kind": config.get("kind"),
        "status": config.get("status"),
        "rrule": config.get("rrule"),
        "interval_minutes": parse_interval_minutes(config.get("rrule")),
        "target_thread_id": config.get("target_thread_id"),
        "model": config.get("model"),
        "reasoning_effort": config.get("reasoning_effort"),
        "execution_environment": config.get("execution_environment"),
        "cwds": cwds,
        "cwd_mentions_target_worktree": cwd_mentions_root,
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.refresh_gate:
        refresh_gate()
    primary = automation_record(PRIMARY_AUTOMATION_ID)
    secondary = automation_record(SECONDARY_AUTOMATION_ID)
    gate = read_json(START_GATE, {})
    v301_run = read_json(V301_RUN_STATUS, {})
    v321_run = read_json(V321_RUN_STATUS, {})
    v341_handoff = read_json(V341_HANDOFF, {})
    v341_run = read_json(V341_RUN_STATUS, {})
    phase_296 = read_json(PHASE_296_STATUS, {})
    supervisor = read_json(SUPERVISOR_STATUS, {})
    processes = process_snapshot()
    ready = bool(gate.get("ready"))
    v301_running = (
        v301_run.get("status") == "running"
        and str(v301_run.get("phase_range", "")).lower() == "v301-v320"
        and int(v301_run.get("active_phase") or 0) >= 301
    )
    v301_complete = (
        v301_run.get("status") == "phase_complete_waiting"
        and str(v301_run.get("phase_range", "")).lower() == "v301-v320"
        and int(v301_run.get("active_phase") or 0) >= 320
        and v301_run.get("active_phase_status") == "phase_complete"
    )
    v321_handoff_ready = V321_HANDOFF.exists()
    v321_running = (
        v321_run.get("status") == "running"
        and str(v321_run.get("phase_range", "")).lower() == "v321-v340"
        and int(v321_run.get("active_phase") or 0) >= 321
    )
    v321_paused = (
        v321_run.get("status") == "paused"
        and str(v321_run.get("phase_range", "")).lower() == "v321-v340"
        and int(v321_run.get("active_phase") or 0) >= 321
    )
    v321_complete = (
        v321_run.get("status") == "phase_complete_waiting"
        and str(v321_run.get("phase_range", "")).lower() == "v321-v340"
        and int(v321_run.get("active_phase") or 0) >= 340
        and v321_run.get("active_phase_status") == "phase_complete"
    )
    v341_handoff_ready = (
        V341_HANDOFF.exists()
        and v341_handoff.get("handoff_state") == "ready_for_operator_automation_update"
    )
    v341_active_phase = int(v341_run.get("active_phase") or 0)
    v341_running = (
        v341_run.get("status") == "running"
        and str(v341_run.get("phase_range", "")).lower() == "v341-v360"
        and 341 <= v341_active_phase <= 360
    )
    v341_waiting = (
        v341_run.get("status") == "phase_complete_waiting"
        and str(v341_run.get("phase_range", "")).lower() == "v341-v360"
        and 341 <= v341_active_phase <= 360
        and v341_run.get("active_phase_status") == "phase_complete"
    )
    v341_complete = (
        v341_run.get("status") == "v281_v360_complete"
        and str(v341_run.get("phase_range", "")).lower() == "v341-v360"
        and v341_active_phase >= 360
        and v341_run.get("active_phase_status") == "phase_complete"
    )
    valid = gate.get("valid_responses")
    expected = gate.get("expected_responses")
    global_v2_complete = gate.get("global_v2_complete")
    if global_v2_complete is None:
        blockers = gate.get("blockers") or []
        global_v2_complete = not any("global v2" in str(item).lower() for item in blockers)
    findings: list[str] = []
    if primary.get("exists") and primary.get("kind") == "heartbeat" and primary.get("target_thread_id"):
        findings.append("Primary Aletheon chat heartbeat exists and targets this Codex thread.")
    else:
        findings.append("Primary Aletheon chat heartbeat is missing or incomplete; keep using the older worktree automation only as fallback.")
    if primary.get("status") == "PAUSED":
        findings.append("Primary Aletheon chat heartbeat is PAUSED; activate through the Codex app UI rather than editing TOML directly.")
    if primary.get("interval_minutes") != TARGET_CHAT_HEARTBEAT_MINUTES:
        findings.append(
            f"Primary chat heartbeat interval is {primary.get('interval_minutes')} minutes; set it to "
            f"{TARGET_CHAT_HEARTBEAT_MINUTES} minutes for the energy-preserving recovery loop."
        )
    if secondary.get("exists") and secondary.get("status") != "PAUSED":
        findings.append("Secondary worktree automation is active; consider pausing it to avoid duplicate wakeups while Aletheon chat heartbeat is primary.")
    if secondary.get("exists") and not secondary.get("cwd_mentions_target_worktree"):
        findings.append("Secondary worktree automation cwd is not the D: worktree; leave it as fallback unless the UI can target the D: worktree directly.")
    if v341_complete:
        findings.append("v341-v360 is complete at v360; ask whether to archive this heartbeat or update it for the next packet.")
    elif v341_running:
        findings.append(
            f"v341-v360 is running at v{v341_run.get('active_phase')}; complete exactly the active phase and do not start a duplicate."
        )
    elif v341_waiting:
        findings.append(
            f"v341-v360 is waiting after v{v341_run.get('active_phase')} completion; open only the next bounded phase if it is within v341-v360."
        )
    elif v321_complete and v341_handoff_ready:
        findings.append("v321-v340 is complete at v340 and the v341-v360 final handoff is ready.")
    elif v321_complete:
        findings.append("v321-v340 is complete at v340; prepare v341-v360 launch only from the final handoff.")
    elif v321_paused:
        findings.append(
            f"v321-v340 is paused at v{v321_run.get('active_phase')}; do not complete the active phase until the operator resumes."
        )
    elif v321_running:
        findings.append(
            f"v321-v340 is already running at v{v321_run.get('active_phase')}; do not reopen v321."
        )
    elif v301_complete:
        findings.append("v301-v320 is complete at v320; do not reopen v301.")
        if v321_handoff_ready:
            findings.append("v321-v340 sibling handoff exists and can be used for the next phase.")
        else:
            findings.append("v321-v340 sibling handoff is still missing; prepare it before changing the heartbeat.")
    elif v301_running:
        findings.append(
            f"v301-v320 is already running at v{v301_run.get('active_phase')}; do not reopen v301."
        )
    elif ready:
        findings.append("v301-v320 start gate is ready; begin from the Aletheon run status and reactivation packet.")
    else:
        findings.append("v301-v320 is not ready; automation should report standby only.")
    if processes:
        findings.append("Local supervisor/watcher processes are present.")
    else:
        findings.append("No local runner processes matched the health pattern; inspect before assuming background progress.")
    if v341_complete:
        status = "v281_v360_complete"
    elif v341_running:
        status = "v341_v360_running"
    elif v341_waiting:
        status = "v341_v360_phase_complete_waiting"
    elif v321_complete and v341_handoff_ready:
        status = "v321_v340_complete_v341_handoff_ready"
    elif v321_complete:
        status = "v321_v340_complete_waiting_v341"
    elif v321_paused:
        status = "v321_v340_paused"
    elif v321_running:
        status = "v321_v340_running"
    elif v301_complete and v321_handoff_ready:
        status = "v301_v320_complete_handoff_ready"
    elif v301_complete:
        status = "v301_v320_complete_waiting_handoff"
    elif v301_running:
        status = "v301_v320_running"
    elif ready:
        status = "ready_to_start_v301"
    else:
        status = "standby"
    if v341_complete:
        recommended_action = (
            "v341-v360 is complete. Ask Hamish whether to archive the Aletheon heartbeat or update it for the next bounded packet."
        )
    elif v341_running:
        recommended_action = (
            f"Continue v{v341_run.get('active_phase')} from docs/trinity-live-traces/"
            "v341-v360-sibling-run-status-v1.md. Complete exactly the active phase, write v1/v2 reports "
            "and source capsule, then open the next phase only if it is within v341-v360."
        )
    elif v341_waiting:
        next_phase = v341_active_phase + 1
        recommended_action = (
            f"v{v341_active_phase} is complete. Open v{next_phase} only if it is still within v341-v360, "
            "otherwise write the v281-v360 closeout declaration."
        )
    elif v321_complete and v341_handoff_ready:
        recommended_action = (
            "v321-v340 is complete and the v341-v360 handoff is ready. If no v341-v360 run is active, "
            "create or use the bounded successor scripts and open v341."
        )
    elif v321_complete:
        recommended_action = (
            "v321-v340 is complete. Prepare the v341-v360 Aletheon-led launch and final closeout handoff."
        )
    elif v321_paused:
        recommended_action = (
            f"Hold v{v321_run.get('active_phase')} until the operator explicitly resumes. On resume, read "
            "docs/trinity-live-traces/v321-v340-sibling-run-status-v1.json and complete exactly the active phase."
        )
    elif v321_running:
        recommended_action = (
            f"Continue v{v321_run.get('active_phase')} from docs/trinity-live-traces/"
            "v321-v340-sibling-run-status-v1.md. Complete the active sibling phase, write v1/v2 reports, "
            "and only then open the next sibling phase."
        )
    elif v301_complete and v321_handoff_ready:
        recommended_action = (
            "v301-v320 is complete and the v321-v340 sibling handoff exists. Ask whether to update the "
            "Aletheon heartbeat for v341-v360 or archive the current recovery bridge."
        )
    elif v301_complete:
        recommended_action = (
            "v301-v320 is complete. Prepare docs/trinity-live-traces/v321-v340-sibling-handoff-v1.md "
            "before changing or archiving the Aletheon heartbeat."
        )
    elif v301_running:
        recommended_action = (
            f"Continue v{v301_run.get('active_phase')} from docs/trinity-live-traces/"
            "v301-v320-aletheon-run-status-v1.md. Do not rerun the v301 start gate; complete the active phase, "
            "write its completion receipt, and only then open the next phase."
        )
    elif ready:
        recommended_action = (
            "Gate is ready. Use the Aletheon chat heartbeat as primary, unpause it if needed, and begin v301 from "
            "docs/trinity-live-traces/v301-v320-aletheon-run-status-v1.md. Keep the old worktree automation paused or fallback-only."
        )
    else:
        recommended_action = (
            "Use the Aletheon chat heartbeat as primary. Set interval to 30 minutes, unpause it, and optionally Run now once. "
            "The expected result is standby until gate.ready is true. Keep the old worktree automation paused or fallback-only."
        )
    return {
        "generated_utc": now_iso(),
        "status": status,
        "primary_automation": primary,
        "secondary_automation": secondary,
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
        "v301_v320_run": {
            "path": rel(V301_RUN_STATUS),
            "status": v301_run.get("status"),
            "active_phase": v301_run.get("active_phase"),
            "active_phase_status": v301_run.get("active_phase_status"),
            "last_completion": v301_run.get("last_completion"),
            "next_action": v301_run.get("next_action"),
        },
        "v321_v340_handoff": {
            "path": rel(V321_HANDOFF),
            "exists": v321_handoff_ready,
        },
        "v321_v340_run": {
            "path": rel(V321_RUN_STATUS),
            "status": v321_run.get("status"),
            "active_phase": v321_run.get("active_phase"),
            "active_phase_status": v321_run.get("active_phase_status"),
            "last_completion": v321_run.get("last_completion"),
            "next_action": v321_run.get("next_action"),
        },
        "v341_v360_handoff": {
            "path": rel(V341_HANDOFF),
            "exists": V341_HANDOFF.exists(),
            "handoff_state": v341_handoff.get("handoff_state"),
        },
        "v341_v360_run": {
            "path": rel(V341_RUN_STATUS),
            "status": v341_run.get("status"),
            "active_phase": v341_run.get("active_phase"),
            "active_phase_status": v341_run.get("active_phase_status"),
            "last_completion": v341_run.get("last_completion"),
            "closeout_declaration": v341_run.get("closeout_declaration"),
            "next_action": v341_run.get("next_action"),
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
        "recommended_action": recommended_action,
    }


def write_md(payload: dict[str, Any]) -> None:
    gate = payload["gate"]
    v301_run = payload["v301_v320_run"]
    handoff = payload["v321_v340_handoff"]
    v321_run = payload["v321_v340_run"]
    v341_handoff = payload["v341_v360_handoff"]
    v341_run = payload["v341_v360_run"]
    primary = payload["primary_automation"]
    secondary = payload["secondary_automation"]
    lines = [
        "# v281-v360 Automation Health Check",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Primary automation:",
        f"- ID: `{primary.get('id')}`",
        f"- Kind: `{primary.get('kind')}`",
        f"- Status: `{primary.get('status')}`",
        f"- Schedule: `{primary.get('rrule')}`",
        f"- Interval minutes: `{primary.get('interval_minutes')}`",
        f"- Target thread: `{primary.get('target_thread_id')}`",
        "",
        "Secondary automation:",
        f"- ID: `{secondary.get('id')}`",
        f"- Kind: `{secondary.get('kind')}`",
        f"- Status: `{secondary.get('status')}`",
        f"- Schedule: `{secondary.get('rrule')}`",
        f"- CWD includes target worktree: `{secondary.get('cwd_mentions_target_worktree')}`",
        "",
        "Gate:",
        f"- Ready: `{gate.get('ready')}`",
        f"- Responses: `{gate.get('valid_responses')}/{gate.get('expected_responses')}`",
        f"- Complete phases: `{gate.get('complete_phases')}/{gate.get('expected_phases')}`",
        f"- First incomplete phase: `v{gate.get('first_incomplete_phase')}`",
        f"- Global v2 complete: `{gate.get('global_v2_complete')}`",
        "",
        "v301-v320 run:",
        f"- Status: `{v301_run.get('status')}`",
        f"- Active phase: `v{v301_run.get('active_phase')}`",
        f"- Active phase status: `{v301_run.get('active_phase_status')}`",
        f"- Next action: `{v301_run.get('next_action')}`",
        "",
        "v321-v340 handoff:",
        f"- Exists: `{handoff.get('exists')}`",
        f"- Path: `{handoff.get('path')}`",
        "",
        "v321-v340 run:",
        f"- Status: `{v321_run.get('status')}`",
        f"- Active phase: `v{v321_run.get('active_phase')}`",
        f"- Active phase status: `{v321_run.get('active_phase_status')}`",
        f"- Next action: `{v321_run.get('next_action')}`",
        "",
        "v341-v360 handoff:",
        f"- Exists: `{v341_handoff.get('exists')}`",
        f"- Handoff state: `{v341_handoff.get('handoff_state')}`",
        f"- Path: `{v341_handoff.get('path')}`",
        "",
        "v341-v360 run:",
        f"- Status: `{v341_run.get('status')}`",
        f"- Active phase: `v{v341_run.get('active_phase')}`",
        f"- Active phase status: `{v341_run.get('active_phase_status')}`",
        f"- Closeout declaration: `{v341_run.get('closeout_declaration')}`",
        f"- Next action: `{v341_run.get('next_action')}`",
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
