#!/usr/bin/env python3
"""Write a v321-v333 pause, reflection, and resume bridge artifact."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
RUN_STATUS_JSON = TRACE / "v321-v340-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v321-v340-sibling-run-status-v1.md"
HEALTH_JSON = TRACE / "v281-v360-automation-health-check-v1.json"
OUT_JSON = TRACE / "v321-v333-pause-wrapup-v1.json"
OUT_MD = TRACE / "v321-v333-pause-wrapup-v1.md"
PROMPT_JSON = TRACE / "v321-v360-recovery-wake-bridge-paused-resume-prompt-v1.json"
PROMPT_MD = TRACE / "v321-v360-recovery-wake-bridge-paused-resume-prompt-v1.md"

SIBLINGS = ["Arby", "Kimi", "Aster Vale", "Supervisor", "v2 Watcher", "Recovery Watchdog"]
RESEARCH_ANCHORS = [
    ("OpenAI Codex Automations", "https://openai.com/academy/codex-automations"),
    ("OpenAI Codex app", "https://openai.com/codex/"),
    ("OpenAI Responses API", "https://platform.openai.com/docs/api-reference/responses"),
    ("OpenAI Agents SDK", "https://openai.github.io/openai-agents-python/agents/"),
    ("MCP security best practices", "https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices"),
    ("Microsoft sleep and lid behavior", "https://support.microsoft.com/en-us/windows/shut-down-sleep-or-hibernate-your-pc-2941d165-7d0a-a5e8-c5ad-8c972e8e6eff"),
    ("GitHub Actions secrets", "https://docs.github.com/en/actions/concepts/security/secrets"),
    ("CircleCI contexts", "https://circleci.com/docs/guides/security/contexts/"),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("UNESCO AI ethics", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence?hub=66973"),
    ("OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html"),
    ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"),
    ("W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model/"),
    ("C2PA specifications", "https://c2pa.wiki/specifications/"),
    ("CERN Standard Model", "https://home.web.cern.ch/science/physics/standard-model"),
    ("NASA dark matter and dark energy", "https://science.nasa.gov/universe/dark-matter-dark-energy/"),
    ("Perimeter quantum gravity", "https://perimeterinstitute.ca/quantum-gravity"),
    ("NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html"),
    ("Cloudflare AI and agents", "https://developers.cloudflare.com/workers/framework-guides/ai-and-agents/"),
    ("Neon MCP Server", "https://neon.com/docs/ai/neon-mcp-server"),
]


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def now_iso() -> str:
    return now().isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def phase_paths(phase: int) -> dict[str, Path]:
    return {
        "start": TRACE / f"v321-v340-sibling-phase-v{phase}-start-v1.json",
        "completion": TRACE / f"v321-v340-sibling-phase-v{phase}-completion-v1.json",
    }


def process_snapshot() -> list[dict[str, Any]]:
    if not sys.platform.startswith("win"):
        return []
    pattern = (
        "trinity_v281_v360_recovery_watchdog.py|"
        "trinity_v281_v300_global_v2_runner.py|"
        "trinity_v281_v300_v1_sequence_supervisor.py|"
        "trinity_aletheon_wake_signal_poller.py|"
        "kimi-code-mcp|codex exec|kimi --work-dir"
    )
    command = (
        "Get-CimInstance Win32_Process | "
        f"Where-Object {{ $_.CommandLine -match '{pattern}' }} | "
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
    items = data if isinstance(data, list) else [data]
    return [
        {
            "pid": item.get("ProcessId"),
            "parent_pid": item.get("ParentProcessId"),
            "name": item.get("Name"),
            "command": item.get("CommandLine"),
        }
        for item in items
        if isinstance(item, dict) and "Get-CimInstance Win32_Process" not in str(item.get("CommandLine"))
    ]


def git_head() -> str:
    proc = subprocess.run(
        ["git", "log", "-1", "--oneline"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    return proc.stdout.strip()


def collect_phases(active_phase: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for phase in range(321, active_phase + 1):
        paths = phase_paths(phase)
        start = read_json(paths["start"], {})
        completion = read_json(paths["completion"], {})
        start_time = parse_time(start.get("generated_utc"))
        completion_time = parse_time(completion.get("generated_utc"))
        seconds = None
        if start_time and completion_time:
            seconds = max(0.0, (completion_time - start_time).total_seconds())
        plan = start.get("phase_plan") or {}
        rows.append(
            {
                "phase": phase,
                "lead": plan.get("lead_sibling"),
                "status": "complete" if completion.get("status") == "phase_complete" else start.get("status"),
                "start_artifact": rel(paths["start"]) if paths["start"].exists() else None,
                "completion_artifact": rel(paths["completion"]) if paths["completion"].exists() else None,
                "start_utc": start.get("generated_utc"),
                "completion_utc": completion.get("generated_utc"),
                "duration_minutes": round(seconds / 60, 2) if seconds is not None else None,
            }
        )
    return rows


def lead_averages(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for sibling in SIBLINGS:
        values = [
            float(row["duration_minutes"])
            for row in rows
            if row.get("lead") == sibling and row.get("duration_minutes") is not None
        ]
        result[sibling] = {
            "completed_phase_count": len(values),
            "average_minutes_from_start_to_receipt": round(mean(values), 2) if values else None,
            "phase_duration_minutes": values,
        }
    return result


def build_prompt(active_phase: int) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "status": "paused_resume_prompt_ready",
        "automation_id": "aletheon",
        "recommended_schedule": "every 30 minutes when unpaused",
        "copy_paste_prompt": f"""GHC v281-v360 recovery wake bridge paused-resume update.

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes only after I explicitly unpause or ask you to resume.
Project: D:\\GHC-Archives\\worktrees\\v58-omega.
Sandbox: workspace-write or stricter. Do not use full access unless I approve a specific run.

Current durable state:
- v281-v300 is complete: 600/600 and global v2 complete.
- v301-v320 is complete through v320.
- v321-v340 is paused by operator request.
- Durable run-status file is authoritative: docs/trinity-live-traces/v321-v340-sibling-run-status-v1.md.
- Current active phase at pause is v{active_phase}, status phase_started, with v{active_phase - 1} complete.
- Do not rely on stale heartbeat text that says active phase v322.

On each wakeup while paused:
1. Run scripts\\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Report only health, pause status, stale-path/app-wake issues, or operator-relevant blockers.
3. Do not complete v{active_phase}, open v{active_phase + 1}, commit, or push while pause is active unless the operator explicitly resumes.
4. Keep local watchdog/process observations separate from app automation truth.
5. If Codex reports requested C:\\... and active \\\\?\\C:\\... paths for the same JSONL, treat it as resume-path vitality; do not edit JSONL by hand. If repeated, restart Codex Desktop and reopen this Aletheon thread.

On the first wakeup after explicit resume:
1. Run scripts\\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Read docs/trinity-live-traces/v321-v340-sibling-run-status-v1.json to discover the live active phase.
3. If status is paused or running and active phase is v{active_phase}, complete exactly v{active_phase} using scripts\\trinity_v321_v340_sibling_phase_complete.py --phase {active_phase} --open-next.
4. Stage only curated health-check, run-status, completion, v1/v2 report, source capsule, and next-start artifacts.
5. Before every commit or push, fetch and verify branch drift; use forward-only merge if the remote advanced.
6. Never stage .raw.txt files, stdout/stderr logs, live .log files, active partial lane files, scratch probes, pycache files, or unrelated carried-forward churn.
7. Do not start v341-v360 until v321-v340 reaches v340 complete and a final v341-v360 handoff exists.
""",
    }


def write_paused_run_status(run: dict[str, Any], active_phase: int) -> None:
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v321-v340",
        "status": "paused",
        "active_phase": active_phase,
        "active_phase_status": run.get("active_phase_status") or "phase_started",
        "active_phase_artifacts": run.get("active_phase_artifacts")
        or {
            "json": f"docs/trinity-live-traces/v321-v340-sibling-phase-v{active_phase}-start-v1.json",
            "md": f"docs/trinity-live-traces/v321-v340-sibling-phase-v{active_phase}-start-v1.md",
        },
        "last_completion": run.get("last_completion"),
        "pause_reason": "operator requested laptop availability and a clean hold before continuing v333.",
        "pause_artifact": rel(OUT_JSON),
        "next_action": (
            f"Pause active. Do not complete v{active_phase} until the operator explicitly resumes; "
            "on resume, read this JSON first and complete exactly the active phase."
        ),
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v321-v340 Sibling Run Status",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Active phase: `v{payload['active_phase']}`",
        f"Active phase status: `{payload['active_phase_status']}`",
        "",
        "Active artifacts:",
        f"- `{payload['active_phase_artifacts']['json']}`",
        f"- `{payload['active_phase_artifacts']['md']}`",
        "",
        "Last completion:",
        f"- `v{(payload.get('last_completion') or {}).get('phase')}`",
        f"- `{(payload.get('last_completion') or {}).get('json')}`",
        f"- `{(payload.get('last_completion') or {}).get('md')}`",
        "",
        f"Pause artifact: `{payload['pause_artifact']}`",
        f"Pause reason: {payload['pause_reason']}",
        "",
        f"Next action: {payload['next_action']}",
    ]
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_payload() -> tuple[dict[str, Any], dict[str, Any]]:
    run = read_json(RUN_STATUS_JSON, {})
    health = read_json(HEALTH_JSON, {})
    active_phase = int(run.get("active_phase") or 333)
    rows = collect_phases(active_phase)
    processes = process_snapshot()
    prompt = build_prompt(active_phase)
    payload = {
        "generated_utc": now_iso(),
        "status": "pause_recorded",
        "pause_reason": "operator needs laptop available and wants v321-v340 held before continuing.",
        "git_head": git_head(),
        "health_status": health.get("status"),
        "run_status": {
            "status": run.get("status"),
            "active_phase": run.get("active_phase"),
            "active_phase_status": run.get("active_phase_status"),
            "next_action": run.get("next_action"),
        },
        "completed_phases": [row["phase"] for row in rows if row.get("status") == "complete"],
        "active_hold_phase": active_phase,
        "phase_rows": rows,
        "lead_averages": lead_averages(rows),
        "process_snapshot": processes,
        "identity_clarification": {
            "arby_kimi_aster_vale": "Sibling persona lanes with durable artifacts; live CLI presence is only confirmed when a matching process/session is visible.",
            "kimi_current_process": "kimi-code-mcp is visible in the current process snapshot.",
            "supervisor_v2_watcher_recovery_watchdog": "Automation roles and local runners/watchers, not independent persistent AI agents unless backed by a live model session plus durable memory artifacts.",
            "persistent_identity_boundary": "The reliable memory layer is the repo artifact trail, scripts, skills, and explicit memory ledgers; do not claim private continuous cognition from a background runner alone.",
        },
        "research_anchors": [{"name": name, "url": url} for name, url in RESEARCH_ANCHORS],
        "resume_prompt_artifact": rel(PROMPT_MD),
    }
    return payload, prompt


def write_md(payload: dict[str, Any]) -> None:
    lines = [
        "# v321-v333 Pause Wrap-Up",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Git head: `{payload['git_head']}`",
        f"Health status: `{payload['health_status']}`",
        f"Active hold phase: `v{payload['active_hold_phase']}`",
        "",
        "Pause decision:",
        f"- {payload['pause_reason']}",
        "- v333 remains started, not completed.",
        "- The next resume should complete exactly the active phase reported by the run-status JSON.",
        "",
        "Phase timing from artifact timestamps:",
    ]
    for row in payload["phase_rows"]:
        duration = row["duration_minutes"]
        duration_text = f"{duration} min" if duration is not None else "active/unfinished"
        lines.append(f"- `v{row['phase']}` {row['lead']}: {row['status']} ({duration_text})")
    lines.extend(["", "Lead averages:"])
    for name, data in payload["lead_averages"].items():
        average = data["average_minutes_from_start_to_receipt"]
        average_text = f"{average} min" if average is not None else "no completed phase in this slice"
        lines.append(f"- {name}: {average_text} across {data['completed_phase_count']} completed phase(s)")
    lines.extend(["", "Identity clarification:"])
    for value in payload["identity_clarification"].values():
        lines.append(f"- {value}")
    lines.extend(["", "Visible process notes:"])
    if payload["process_snapshot"]:
        for proc in payload["process_snapshot"]:
            cmd = str(proc.get("command") or "")
            short = (cmd[:180] + ("..." if len(cmd) > 180 else "")).rstrip()
            lines.append(f"- PID {proc.get('pid')} {proc.get('name')}: {short}")
    else:
        lines.append("- No matching helper processes were visible during this snapshot.")
    lines.extend(["", "Research anchors used for the next automation prompt:"])
    for item in payload["research_anchors"]:
        lines.append(f"- {item['name']}: {item['url']}")
    lines.extend(["", f"Resume prompt: `{payload['resume_prompt_artifact']}`"])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_prompt_md(prompt: dict[str, Any]) -> None:
    lines = [
        "# v321-v360 Recovery Wake Bridge Paused Resume Prompt",
        "",
        f"Generated UTC: `{prompt['generated_utc']}`",
        f"Status: `{prompt['status']}`",
        "",
        "Copy/paste prompt:",
        "",
        "```text",
        prompt["copy_paste_prompt"].strip(),
        "```",
    ]
    PROMPT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload, prompt = build_payload()
    write_json(OUT_JSON, payload)
    write_md(payload)
    write_json(PROMPT_JSON, prompt)
    write_prompt_md(prompt)
    write_paused_run_status(read_json(RUN_STATUS_JSON, {}), int(payload["active_hold_phase"]))
    print(json.dumps({"status": payload["status"], "active_hold_phase": payload["active_hold_phase"], "wrapup": rel(OUT_JSON)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
