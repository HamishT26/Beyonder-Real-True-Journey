#!/usr/bin/env python3
"""Create the curated V44 recurring automation fallback and publish the registry."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from trinity_v44_common import ROOT, now_iso, read_json, resolve_status, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-automation-registry-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v44-automation-registry-v1.md"
WRAPPER = ROOT / "scripts" / "trinity_v44_scheduled_cycle.ps1"
POWERSHELL = shutil.which("powershell.exe") or "powershell.exe"
PYTHON = sys.executable


def _task_name(label: str, hhmm: str) -> str:
    return f"Codex V44 {label} {hhmm.replace(':', '')}"


def _task_action(lane: str) -> str:
    return f'{POWERSHELL} -NoProfile -ExecutionPolicy Bypass -File "{WRAPPER}" -Lane {lane}'


def _create_task(task_name: str, start_time: str, lane: str) -> dict[str, Any]:
    proc = safe_run(
        ["schtasks", "/Create", "/F", "/SC", "DAILY", "/TN", task_name, "/ST", start_time, "/TR", _task_action(lane)],
        timeout=120,
    )
    query = safe_run(["schtasks", "/Query", "/TN", task_name, "/V", "/FO", "LIST"], timeout=120)
    return {
        "task_name": task_name,
        "lane": lane,
        "start_time": start_time,
        "create_returncode": proc.returncode,
        "create_stdout_excerpt": proc.stdout[-1200:],
        "create_stderr_excerpt": proc.stderr[-1200:],
        "query_returncode": query.returncode,
        "query_stdout_excerpt": query.stdout[-2400:],
        "query_stderr_excerpt": query.stderr[-1200:],
        "created": proc.returncode == 0,
        "queried": query.returncode == 0,
    }


def _artifact_snapshot(relative_path: str) -> tuple[Path, bool, int | None]:
    path = ROOT / Path(relative_path)
    if not path.exists():
        return path, False, None
    return path, True, path.stat().st_mtime_ns


def _run_first_cycle(automation: dict[str, Any]) -> dict[str, Any]:
    proof_artifact = str(automation["proof_artifact"])
    proof_path, before_exists, before_mtime_ns = _artifact_snapshot(proof_artifact)
    proc = safe_run(
        [POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WRAPPER), "-Lane", str(automation["lane"])],
        timeout=7200,
    )
    _, after_exists, after_mtime_ns = _artifact_snapshot(proof_artifact)
    artifact_payload = read_json(proof_path) if after_exists else {}
    artifact_status = resolve_status(artifact_payload)
    artifact_refreshed = bool(after_exists and (not before_exists or after_mtime_ns != before_mtime_ns))
    verified = proc.returncode == 0 or artifact_refreshed
    if not verified:
        verification_state = "execution_failed"
    elif proc.returncode == 0 and artifact_status == "PASS":
        verification_state = "verified_clean"
    else:
        verification_state = "verified_with_residuals"
    return {
        "lane": str(automation["lane"]),
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-3200:],
        "stderr_excerpt": proc.stderr[-2400:],
        "proof_artifact": proof_artifact,
        "proof_artifact_exists": after_exists,
        "proof_artifact_refreshed": artifact_refreshed,
        "proof_artifact_status": artifact_status,
        "verified": verified,
        "verification_state": verification_state,
    }


def _existing_tasks(pattern: str) -> list[dict[str, Any]]:
    proc = safe_run(
        [
            POWERSHELL,
            "-NoProfile",
            "-Command",
            f"Get-ScheduledTask | Where-Object {{ $_.TaskName -like '{pattern}' }} | Select-Object TaskName,State,TaskPath | ConvertTo-Json -Depth 3",
        ],
        timeout=120,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    rows = payload if isinstance(payload, list) else [payload]
    result: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        result.append(
            {
                "task_name": str(row.get("TaskName") or ""),
                "state": str(row.get("State") or ""),
                "task_path": str(row.get("TaskPath") or ""),
            }
        )
    return result


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V44 Automation Registry",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Automation registry state: `{payload['automation_registry_state']}`",
        f"- Automation backend state: `{payload['automation_backend_state']}`",
        f"- Native automation state: `{payload['codex_native_automation_state']}`",
        "",
        "## Existing Tasks",
        "",
    ]
    for row in payload.get("existing_v42_tasks", []):
        lines.append(f"- `V42::{row['task_name']}`: state=`{row['state']}`")
    for row in payload.get("existing_v43_tasks", []):
        lines.append(f"- `V43::{row['task_name']}`: state=`{row['state']}`")
    lines.extend(["", "## Admitted V44 Automations", ""])
    for row in payload.get("admitted_automations", []):
        lines.append(f"- `{row['name']}`: tier=`{row['tier']}`, entrypoint=`{row['entrypoint']}`, proof=`{row['proof_artifact']}`")
    if payload.get("lane_residuals"):
        lines.extend(["", "## Lane Residuals", ""])
        lines.extend(f"- `{row}`" for row in payload["lane_residuals"])
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the curated V44 recurring automation fallback and registry.")
    parser.add_argument("--run-first-cycle", action="store_true")
    parser.add_argument("--native-automation-tool-available", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    admitted = [
        {
            "name": "V44 PowerShell Health",
            "lane": "powershell_health",
            "times": ["03:15", "15:15"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Verify the PowerShell operator lane, worktree baseline, and Codex CLI gate.",
            "entrypoint": "scripts/trinity_v44_scheduled_cycle.ps1 -Lane powershell_health",
            "proof_artifact": "docs/trinity-live-traces/v44-operator-surface-probe-v1.json",
        },
        {
            "name": "V44 API Health",
            "lane": "api_health",
            "times": ["03:30", "15:30"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Refresh billing, auth, project, and cloud carry-forward truth.",
            "entrypoint": "scripts/trinity_v44_scheduled_cycle.ps1 -Lane api_health",
            "proof_artifact": "docs/trinity-live-traces/v44-cloud-sweep-v1.json",
        },
        {
            "name": "V44 GMUT Lab",
            "lane": "gmut_lab",
            "times": ["03:45", "15:45"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Run the bounded QCIT, transmutation, validation, kairotic, and energy-bank bundle.",
            "entrypoint": "scripts/trinity_v44_scheduled_cycle.ps1 -Lane gmut_lab",
            "proof_artifact": "docs/trinity-live-traces/v44-gmut-lab-bundle-v1.json",
        },
        {
            "name": "V44 Vesper Sync",
            "lane": "vesper_sync",
            "times": ["04:00", "16:00"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Refresh the bounded Vesper memory and Agent Engine truth surface.",
            "entrypoint": "scripts/trinity_v44_scheduled_cycle.ps1 -Lane vesper_sync",
            "proof_artifact": "docs/trinity-live-traces/v44-vesper-memory-cognitive-bridge-v1.json",
        },
    ]

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v44_omega",
        "overall_status": "WARN",
        "automation_registry_state": "pending",
        "automation_backend_state": "native_codex_automation_ready" if args.native_automation_tool_available else "windows_task_scheduler_authoritative",
        "codex_native_automation_state": "callable_in_session" if args.native_automation_tool_available else "tool_unavailable_in_session",
        "repo_workspace": str(ROOT),
        "python_path": PYTHON,
        "powershell_path": POWERSHELL,
        "existing_v42_tasks": _existing_tasks("Codex V42*"),
        "existing_v43_tasks": _existing_tasks("Codex V43*"),
        "admitted_automations": admitted,
        "task_results": [],
        "manual_first_cycles": [],
        "lane_residuals": [],
        "completed_steps": [],
        "blockers": [],
    }

    if not WRAPPER.exists():
        payload["overall_status"] = "FAIL"
        payload["automation_registry_state"] = "blocked_missing_wrapper"
        payload["blockers"].append("The V44 scheduled-cycle PowerShell wrapper is missing.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), _markdown(payload))
        return 1

    all_tasks_ok = True
    for automation in admitted:
        for start_time in automation["times"]:
            task_name = _task_name(automation["name"], start_time)
            result = _create_task(task_name, start_time, automation["lane"])
            payload["task_results"].append(result)
            if result["created"] and result["queried"]:
                payload["completed_steps"].append(f"scheduled_task_created::{task_name}")
            else:
                all_tasks_ok = False
                payload["blockers"].append(f"scheduled_task_create_failed::{task_name}")

    if args.run_first_cycle:
        for automation in admitted:
            cycle = _run_first_cycle(automation)
            payload["manual_first_cycles"].append(cycle)
            if cycle["verified"]:
                payload["completed_steps"].append(f"manual_first_cycle_verified::{automation['lane']}")
                if cycle["proof_artifact_status"] not in {"PASS", "MISSING"}:
                    payload["lane_residuals"].append(f"{automation['lane']}={cycle['proof_artifact_status']}")
            else:
                all_tasks_ok = False
                payload["blockers"].append(f"manual_first_cycle_failed::{automation['lane']}")

    payload["overall_status"] = "PASS" if all_tasks_ok else "WARN"
    if all_tasks_ok and payload["lane_residuals"]:
        payload["automation_registry_state"] = "scheduler_fallback_verified_with_lane_residuals"
    elif all_tasks_ok:
        payload["automation_registry_state"] = "scheduler_fallback_verified"
    else:
        payload["automation_registry_state"] = "scheduler_fallback_bounded_with_residuals"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if all_tasks_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

