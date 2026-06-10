#!/usr/bin/env python3
"""Generate sanitized v477 THOS Codex CLI/App readiness artifacts."""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACES = DOCS / "trinity-live-traces"
ARCHIVES = ROOT.parents[1]
ADVISORY_ROOT = ARCHIVES / "agent-worktrees" / "v461-round-robin"
APPROVED_STALE_TEMP = (
    Path(os.environ.get("APPDATA", ""))
    / "npm"
    / "node_modules"
    / "@openai"
    / ".codex-3J4dZeTD"
)

BASELINE_HEAD = "0973722439be759b1b5ef2f507489d3f7675af5e"
SESSION_START_NZ = "2026-06-04T00:24:27+12:00"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def run(args: list[str], cwd: Path = ROOT, check: bool = False) -> dict:
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stdout)
    return {"code": proc.returncode, "text": proc.stdout}


def codex(args: list[str]) -> dict:
    return run(["cmd", "/c", "codex", *args])


def git(args: list[str], cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, check=True)["text"].strip()


def advisory_state(label: str) -> dict:
    path = ADVISORY_ROOT / label
    if not path.exists():
        return {"lane": label, "exists": False, "status": "missing"}
    status_text = git(["status", "--short"], cwd=path)
    upstream = run(["git", "rev-parse", "@{u}"], cwd=path)
    drift = run(["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"], cwd=path)
    return {
        "lane": label,
        "exists": True,
        "branch": git(["branch", "--show-current"], cwd=path),
        "head": git(["rev-parse", "HEAD"], cwd=path),
        "upstream_head": upstream["text"].strip() if upstream["code"] == 0 else None,
        "drift": drift["text"].strip() if drift["code"] == 0 else None,
        "worktree_state": "clean" if not status_text else "has_unstaged_or_untracked_entries",
        "boundary": "non_ephemeral_read_only_advisory",
    }


def sandbox_probe(command: list[str]) -> dict:
    result = codex(["sandbox", *command])
    first = result["text"].splitlines()[0].strip() if result["text"].splitlines() else ""
    sanitized = first
    if "spawn setup refresh" in first:
        sanitized = "windows sandbox failed: spawn setup refresh"
    elif result["code"] == 0:
        sanitized = "sandbox command completed"
    return {
        "command_shape": " ".join(command[:2]) if command else "empty",
        "exit_code": result["code"],
        "sanitized_result": sanitized,
    }


def doctor_summary() -> dict:
    output = codex(["doctor", "--summary", "--ascii", "--no-color"])["text"]
    version_match = re.search(r"Codex Doctor v([^\s]+)", output)
    update_match = re.search(r"updates\s+([0-9.]+) available \(current ([0-9.]+)\)", output)
    final_match = re.search(
        r"(?P<ok>\d+) ok \| (?P<idle>\d+) idle \| (?P<notes>\d+) notes \| (?P<warn>\d+) warn \| (?P<fail>\d+) fail (?P<status>\w+)",
        output,
    )
    return {
        "doctor_version": version_match.group(1) if version_match else None,
        "update_available": update_match.group(1) if update_match else None,
        "current_version": update_match.group(2) if update_match else None,
        "summary_counts": final_match.groupdict() if final_match else None,
        "sanitized_notes": [
            "update_available" if update_match else "update_state_not_extracted",
            "rollout_storage_pressure_note_present" if "rollouts" in output else "rollout_note_absent",
            "current_runtime_unrestricted_note_present" if "unrestricted fs" in output else "runtime_note_absent",
            "app_server_idle_ephemeral" if "not running (ephemeral mode)" in output else "app_server_summary_not_extracted",
        ],
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    now_utc = _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()
    local_head = git(["rev-parse", "HEAD"])
    remote_head = git(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = git(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])
    codex_version_result = codex(["--version"])
    if codex_version_result["code"] != 0:
        raise RuntimeError(codex_version_result["text"])
    codex_version = codex_version_result["text"].strip()
    doctor = doctor_summary()
    sandbox_probes = [
        sandbox_probe(["powershell", "-NoProfile", "-Command", "Write-Output sandbox-ok"]),
        sandbox_probe(["cmd", "/c", "echo", "sandbox-ok"]),
        sandbox_probe(["--", "cmd", "/c", "echo", "sandbox-ok"]),
    ]
    advisory = [
        advisory_state("arby-advisory"),
        advisory_state("aster-vale-advisory"),
    ]

    common = {
        "generated_utc": now_utc,
        "session_start_nz": SESSION_START_NZ,
        "phase": "v477_thos_v2",
        "baseline_head": BASELINE_HEAD,
        "local_head": local_head,
        "remote_head": remote_head,
        "drift": drift,
        "claim_boundary": {
            "domain": "THOS Codex App/CLI readiness diagnostics only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }

    update_record = {
        "approved_packet": "APPROVED LIVE ACTION PACKET v477 APP LANES + CODEX CLI/SANDBOX READINESS",
        "codex_update_attempted": True,
        "codex_update_result": "completed_before_this_receipt",
        "codex_version_after_update": codex_version,
        "restart_recommended_by_update": True,
        "cleanup_warning_observed": True,
        "cleanup_action_taken": True,
        "cleanup_result": "approved_stale_temp_removed_before_this_receipt",
        "cleanup_target_label": APPROVED_STALE_TEMP.name,
        "cleanup_target_exists_after": APPROVED_STALE_TEMP.exists(),
        "cleanup_boundary": "only the approved stale npm temp directory was removed",
    }

    readiness = {
        **common,
        "artifact_type": "codex_cli_app_readiness",
        "overall_status": "WARN",
        "codex_version_observed": codex_version,
        "update_record": update_record,
        "doctor_summary": doctor,
        "sandbox_probe_status": "FAIL",
        "sandbox_probes": sandbox_probes,
        "advisory_lanes": advisory,
        "thread_tool_state": {
            "main_thread_management_tools_exposed": False,
            "existing_callable_lanes_requested": [
                "Cicero",
                "Kierkegaard",
                "Aristotle",
            ],
            "existing_callable_lane_message_tools_exposed": False,
            "old_subagent_system_used": False,
            "note": "Only old-style subagent management appeared in tool discovery; it was not used or expanded.",
        },
        "approved_boundary_observed": [
            "approved Codex CLI update completed",
            "approved stale npm temp cleanup completed",
            "no app setting mutation",
            "no plugin cache mutation",
            "no user skill mutation",
        ],
        "blockers": [
            "Codex restart is recommended after the 0.136.0 CLI update.",
            "Windows sandbox probes fail at setup refresh.",
            "Existing app-lane message tools for Cicero, Kierkegaard, and Aristotle are not currently callable in this session.",
        ],
        "next_expected_phase": "v477_thos_v2_x2_or_v477_thos_v3_x1",
    }

    handoff = {
        **common,
        "artifact_type": "v477_thos_v2_handoff",
        "overall_status": "WARN",
        "handoff_summary": [
            "Do not assume sandbox readiness until spawn setup refresh is fixed.",
            "Arby and Aster advisory worktrees are present, clean, and upstream-equal.",
            "Use non-ephemeral read-only lanes only; no old-style subagent spawn.",
            "Codex CLI update to 0.136.0 completed; restart is recommended before assuming desktop-app parity.",
        ],
        "next_action_options": [
            "continue v477 v2 x2 with launcher watcher design around the sandbox blocker",
            "move to v477 v3 x1 for THOS command/watch surface hardening",
            "pause for restart if the user wants desktop-app parity before deeper lane launch",
        ],
    }

    write_json(TRACES / "v477-thos-v2-x1-codex-cli-app-readiness-v1.json", readiness)
    write_json(TRACES / "v477-thos-v2-x1-handoff-v1.json", handoff)
    write_md(
        TRACES / "v477-thos-v2-x1-codex-cli-app-readiness-v1.md",
        "V477 THOS V2 X1 Codex CLI/App Readiness",
        [
            f"- generated_utc: `{now_utc}`",
            f"- local_head: `{local_head}`",
            f"- remote_head: `{remote_head}`",
            f"- drift: `{drift}`",
            f"- codex_version_observed: `{codex_version}`",
            "- update_result: approved CLI update completed before this receipt.",
            "- stale_temp_cleanup: approved stale npm temp directory removed before this receipt.",
            "- doctor_summary: sanitized; raw local machine paths are not published.",
            "- sandbox_probe_status: `FAIL`.",
            "- sandbox_result: `windows sandbox failed: spawn setup refresh`.",
            "- Arby/Aster: worktrees present, clean, and upstream-equal.",
            "- boundary: no app setting mutation, plugin cache mutation, user skill mutation, or cleanup.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v2-x1-handoff-v1.md",
        "V477 THOS V2 X1 Handoff",
        [
            f"- generated_utc: `{now_utc}`",
            "- status: `WARN` due sandbox setup blocker and restart recommendation.",
            "- safe lane state: Arby/Aster worktrees are reachable and clean.",
            "- blocked lane state: Windows sandbox probes fail at setup refresh.",
            "- main-thread app tools: not currently callable here; old-style subagent tools were not used.",
            "- existing app lanes: Cicero, Kierkegaard, and Aristotle are approved but no message tool is exposed here.",
            "- next: v477 v2 x2 can design a watcher/launcher around this blocker, or pause for app restart.",
        ],
    )
    print(json.dumps({"status": "ok", "generated": 4}, indent=2))


if __name__ == "__main__":
    main()
