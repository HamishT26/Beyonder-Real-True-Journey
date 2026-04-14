#!/usr/bin/env python3
"""Create the curated V42 recurring automation fallback and publish the registry."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

from trinity_v42_common import ROOT, now_iso, safe_run, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-automation-registry-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-automation-registry-v1.md"
WRAPPER = ROOT / "scripts" / "trinity_v42_scheduled_cycle.ps1"
POWERSHELL = shutil.which("powershell.exe") or "powershell.exe"
PYTHON = sys.executable


def _task_name(label: str, hhmm: str) -> str:
    return f"Codex V42 {label} {hhmm.replace(':', '')}"


def _task_action(lane: str) -> str:
    return f'{POWERSHELL} -NoProfile -ExecutionPolicy Bypass -File "{WRAPPER}" -Lane {lane}'


def _create_task(task_name: str, start_time: str, lane: str) -> dict[str, Any]:
    proc = safe_run(
        [
            "schtasks",
            "/Create",
            "/F",
            "/SC",
            "DAILY",
            "/TN",
            task_name,
            "/ST",
            start_time,
            "/TR",
            _task_action(lane),
        ],
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


def _run_first_cycle(lane: str) -> dict[str, Any]:
    proc = safe_run(
        [
            POWERSHELL,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(WRAPPER),
            "-Lane",
            lane,
        ],
        timeout=5400,
    )
    return {
        "lane": lane,
        "returncode": proc.returncode,
        "stdout_excerpt": proc.stdout[-2400:],
        "stderr_excerpt": proc.stderr[-2000:],
        "verified": proc.returncode == 0,
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Automation Registry",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Automation registry state: `{payload['automation_registry_state']}`",
        f"- Automation surface state: `{payload['automation_surface_state']}`",
        "",
        "## Admitted Automations",
        "",
    ]
    for row in payload.get("admitted_automations", []):
        lines.append(f"- `{row['name']}`: tier=`{row['tier']}`, entrypoint=`{row['entrypoint']}`, proof=`{row['proof_artifact']}`")
    if payload.get("rejected_candidates"):
        lines.extend(["", "## Deferred Candidates", ""])
        for row in payload["rejected_candidates"]:
            lines.append(f"- `{row['name']}`: `{row['reason']}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the curated V42 recurring automation fallback and registry.")
    parser.add_argument("--run-first-cycle", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    admitted = [
        {
            "name": "V42 API Health",
            "lane": "api_health",
            "times": ["03:30", "15:30"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Refresh the API/cloud/runtime health surface and capture a Kai headless summary.",
            "entrypoint": "scripts/trinity_v42_scheduled_cycle.ps1 -Lane api_health",
            "proof_artifact": "docs/trinity-live-traces/v42-api-automation-wave-v1.json",
            "rollback_note": "Delete both scheduled tasks and keep the manual proof lane only.",
        },
        {
            "name": "V42 GMUT Lab",
            "lane": "gmut_lab",
            "times": ["03:45", "15:45"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Run the bounded QCIT, transmutation, validation, kairotic, and energy-bank bundle.",
            "entrypoint": "scripts/trinity_v42_scheduled_cycle.ps1 -Lane gmut_lab",
            "proof_artifact": "docs/trinity-live-traces/v42-gmut-lab-bundle-v1.json",
            "rollback_note": "Delete both scheduled tasks and keep the manual experiment bundle only.",
        },
        {
            "name": "V42 Vesper Sync",
            "lane": "vesper_sync",
            "times": ["04:00", "16:00"],
            "classification": "runtime_script",
            "tier": "core",
            "purpose": "Ingest the latest health and lab telemetry into Bigtable and mirror it into Agent Engine when healthy.",
            "entrypoint": "scripts/trinity_v42_scheduled_cycle.ps1 -Lane vesper_sync",
            "proof_artifact": "docs/trinity-live-traces/v42-vesper-telemetry-sync-v1.json",
            "rollback_note": "Delete both scheduled tasks and keep Bigtable sync manual only.",
        },
    ]
    rejected = [
        {
            "name": "run_all_trinity_systems",
            "reason": "Too broad for unattended twice-daily recurrence and not restricted to a bounded proof surface.",
        },
        {
            "name": "trinity_background_os",
            "reason": "Needs additional runtime guardrails before unattended scheduling.",
        },
        {
            "name": "trinity_expansion_system_runner",
            "reason": "Candidate inventory remains too wide for safe recurring admission in V42.",
        },
    ]

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": "WARN",
        "automation_registry_state": "pending",
        "automation_surface_state": "windows_task_scheduler_fallback",
        "codex_native_automation_state": "tool_unavailable_in_session",
        "repo_workspace": str(ROOT),
        "python_path": PYTHON,
        "powershell_path": POWERSHELL,
        "admitted_automations": admitted,
        "rejected_candidates": rejected,
        "task_results": [],
        "manual_first_cycles": [],
        "completed_steps": [],
        "blockers": [],
    }

    if not WRAPPER.exists():
        payload["overall_status"] = "FAIL"
        payload["automation_registry_state"] = "blocked_missing_wrapper"
        payload["blockers"].append("The V42 scheduled-cycle PowerShell wrapper is missing.")
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
            cycle = _run_first_cycle(automation["lane"])
            payload["manual_first_cycles"].append(cycle)
            if cycle["verified"]:
                payload["completed_steps"].append(f"manual_first_cycle_verified::{automation['lane']}")
            else:
                all_tasks_ok = False
                payload["blockers"].append(f"manual_first_cycle_failed::{automation['lane']}")

    payload["overall_status"] = "PASS" if all_tasks_ok else "WARN"
    payload["automation_registry_state"] = "scheduler_fallback_verified" if all_tasks_ok else "scheduler_fallback_bounded_with_residuals"
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if all_tasks_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
