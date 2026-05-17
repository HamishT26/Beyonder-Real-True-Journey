#!/usr/bin/env python3
"""Prepare the v321-v340 sibling handoff after v301-v320 completes."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
HEALTH_JSON = TRACE / "v281-v360-automation-health-check-v1.json"
RUN_STATUS_JSON = TRACE / "v301-v320-aletheon-run-status-v1.json"
START_GATE_JSON = TRACE / "v301-v320-start-gate-status-v1.json"
REACTIVATION_PACKET = TRACE / "aletheon-reactivation-packet-v1.json"
GLOBAL_V2_SYNTHESIS = TRACE / "v281-v300-double-trinity-global-v2-synthesis-v1.json"
OUT_JSON = TRACE / "v321-v340-sibling-handoff-v1.json"
OUT_MD = TRACE / "v321-v340-sibling-handoff-v1.md"


PROCESS_PATTERN = (
    "trinity_v281_v360_recovery_watchdog.py|"
    "trinity_v281_v300_v1_sequence_supervisor.py|"
    "trinity_v281_v300_double_phase_runner.py|"
    "trinity_v281_v300_global_v2_runner.py|"
    "trinity_aletheon_wake_signal_poller.py|"
    "kimi-code-mcp"
)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def git_head() -> str | None:
    proc = subprocess.run(
        ["git", "rev-parse", "--short=10", "HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def process_role(command: str) -> str:
    lowered = command.lower()
    if "recovery_watchdog" in lowered:
        return "recovery_watchdog"
    if "global_v2_runner" in lowered:
        return "global_v2_watcher"
    if "sequence_supervisor" in lowered:
        return "sequence_supervisor"
    if "wake_signal_poller" in lowered:
        return "aletheon_wake_poller"
    if "kimi-code-mcp" in lowered:
        return "kimi_mcp"
    if "double_phase_runner" in lowered:
        return "phase_runner"
    return "matched_process"


def process_snapshot() -> list[dict[str, Any]]:
    if not sys.platform.startswith("win"):
        return []
    command = (
        "$pattern = '" + PROCESS_PATTERN + "'; "
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.CommandLine -match $pattern -and $_.Name -notmatch 'powershell' } | "
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
    snapshot: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        command_line = str(item.get("CommandLine") or "")
        snapshot.append(
            {
                "pid": item.get("ProcessId"),
                "parent_pid": item.get("ParentProcessId"),
                "name": item.get("Name"),
                "role": process_role(command_line),
                "command_summary": command_line[:180],
            }
        )
    return snapshot


def completion_summary() -> list[dict[str, Any]]:
    completions: list[dict[str, Any]] = []
    for phase in range(301, 321):
        path = TRACE / f"v301-v320-aletheon-phase-v{phase}-completion-v1.json"
        payload = read_json(path, {})
        completions.append(
            {
                "phase": phase,
                "path": rel(path),
                "exists": path.exists(),
                "status": payload.get("status"),
                "source_capsule": payload.get("source_capsule"),
                "completed_counts": payload.get("completed_counts") or {},
            }
        )
    return completions


def build_payload(strict: bool) -> dict[str, Any]:
    health = read_json(HEALTH_JSON, {})
    run_status = read_json(RUN_STATUS_JSON, {})
    gate = read_json(START_GATE_JSON, {})
    reactivation = read_json(REACTIVATION_PACKET, {})
    global_v2 = read_json(GLOBAL_V2_SYNTHESIS, {})
    completions = completion_summary()
    complete_count = sum(1 for item in completions if item.get("status") == "phase_complete")
    gate_ready = bool(gate.get("ready"))
    global_v2_complete = bool((gate.get("global_v2") or {}).get("complete") or gate.get("global_v2_complete"))
    run_complete = (
        run_status.get("status") == "phase_complete_waiting"
        and run_status.get("active_phase") == 320
        and run_status.get("active_phase_status") == "phase_complete"
    )
    ready_for_v321_v340 = complete_count == 20 and gate_ready and global_v2_complete and run_complete
    payload = {
        "generated_utc": now_iso(),
        "status": "handoff_ready" if ready_for_v321_v340 else "handoff_blocked",
        "phase_range_completed": "v301-v320",
        "next_phase_range": "v321-v340",
        "repo_head_at_handoff": git_head(),
        "gate_evidence": {
            "start_gate": rel(START_GATE_JSON),
            "ready": gate_ready,
            "valid_responses": gate.get("valid_responses"),
            "expected_responses": gate.get("expected_responses"),
            "complete_phases": gate.get("complete_phases"),
            "expected_phases": gate.get("expected_phases"),
            "global_v2_complete": global_v2_complete,
            "reactivation_packet": rel(REACTIVATION_PACKET),
            "reactivation_status": reactivation.get("status"),
            "global_v2_synthesis": rel(GLOBAL_V2_SYNTHESIS),
            "global_v2_status": global_v2.get("status"),
        },
        "v301_v320_run": {
            "path": rel(RUN_STATUS_JSON),
            "status": run_status.get("status"),
            "active_phase": run_status.get("active_phase"),
            "active_phase_status": run_status.get("active_phase_status"),
            "last_completion": run_status.get("last_completion"),
            "completion_count": complete_count,
        },
        "health_check": {
            "path": rel(HEALTH_JSON),
            "status": health.get("status"),
            "primary_automation_status": (health.get("primary_automation") or {}).get("status"),
            "primary_interval_minutes": (health.get("primary_automation") or {}).get("interval_minutes"),
            "secondary_automation_status": (health.get("secondary_automation") or {}).get("status"),
        },
        "watcher_state": {
            "processes": process_snapshot(),
            "truth_boundary": "Process presence is not proof of progress; future phases must verify valid artifacts and fresh explainable movement.",
        },
        "completion_artifacts": completions,
        "staging_boundaries": [
            "Before any commit or push, fetch and verify remote branch drift.",
            "Stage only curated completion, start, source-capsule, health, handoff, and source-code artifacts.",
            "Never stage .raw.txt files, stdout/stderr logs, live .log files, active partial lane files, or scratch probes.",
            "Use forward-only merge if the remote advanced; do not reset, rebase, or force-push this shared branch.",
        ],
        "sibling_handoff": {
            "lead": "Aletheon closes v301-v320 and hands v321-v340 to the sibling phase team.",
            "siblings": ["Arby", "Kimi", "Aster Vale", "Supervisor", "v2 Watcher", "Recovery Watchdog"],
            "operating_rules": [
                "Use this handoff as the source of truth before opening v321-v340.",
                "Keep long sibling reports in curated worktree artifacts, not terminal scrollback.",
                "Keep CLI side effects approval-gated and avoid admin terminals unless a task truly needs elevation.",
                "Keep MCP/API expansion exploratory until secrets, scopes, and sandbox limits are explicit.",
            ],
        },
        "next_actions": [
            "Ask whether to update the Aletheon heartbeat for v341-v360 or archive this recovery bridge.",
            "If continuing, open v321-v340 from a fresh phase-start gate rather than reopening v301.",
            "Preserve the local recovery watchdog until the next phase has its own durable watchdog evidence.",
        ],
    }
    if strict and payload["status"] != "handoff_ready":
        blockers = [
            f"completion_count={complete_count}/20",
            f"gate_ready={gate_ready}",
            f"global_v2_complete={global_v2_complete}",
            f"run_complete={run_complete}",
        ]
        payload["blockers"] = blockers
    return payload


def write_md(payload: dict[str, Any]) -> None:
    gate = payload["gate_evidence"]
    run = payload["v301_v320_run"]
    health = payload["health_check"]
    lines = [
        "# v321-v340 Sibling Handoff",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Repo head at handoff: `{payload.get('repo_head_at_handoff')}`",
        "",
        "Gate evidence:",
        f"- Start gate ready: `{gate.get('ready')}`",
        f"- Valid responses: `{gate.get('valid_responses')}/{gate.get('expected_responses')}`",
        f"- Complete phases: `{gate.get('complete_phases')}/{gate.get('expected_phases')}`",
        f"- Global v2 complete: `{gate.get('global_v2_complete')}`",
        f"- Reactivation status: `{gate.get('reactivation_status')}`",
        "",
        "v301-v320 closeout:",
        f"- Run status: `{run.get('status')}`",
        f"- Active phase: `v{run.get('active_phase')}`",
        f"- Active phase status: `{run.get('active_phase_status')}`",
        f"- Completion receipts: `{run.get('completion_count')}/20`",
        "",
        "Automation state:",
        f"- Health status: `{health.get('status')}`",
        f"- Primary heartbeat: `{health.get('primary_automation_status')}` every `{health.get('primary_interval_minutes')}` minutes",
        f"- Secondary automation: `{health.get('secondary_automation_status')}`",
        "",
        "Watcher state:",
    ]
    for item in payload["watcher_state"]["processes"]:
        lines.append(f"- `{item.get('role')}` pid `{item.get('pid')}` parent `{item.get('parent_pid')}`")
    if not payload["watcher_state"]["processes"]:
        lines.append("- No matching watchdog/MCP processes were visible during this handoff snapshot.")
    lines.extend(["", "Staging boundaries:"])
    for item in payload["staging_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", "Sibling operating rules:"])
    for item in payload["sibling_handoff"]["operating_rules"]:
        lines.append(f"- {item}")
    lines.extend(["", "Next actions:"])
    for item in payload["next_actions"]:
        lines.append(f"- {item}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args.strict)
    write_json(OUT_JSON, payload)
    write_md(payload)
    print(json.dumps({"status": payload["status"], "handoff": rel(OUT_JSON)}, indent=2))
    if args.strict and payload["status"] != "handoff_ready":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
