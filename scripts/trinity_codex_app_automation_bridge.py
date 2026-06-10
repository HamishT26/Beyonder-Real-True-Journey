#!/usr/bin/env python3
"""Write the Codex app automation bridge prompt and local wake fallback."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
OUT_JSON = TRACE / "codex-app-automation-bridge-v1.json"
OUT_MD = TRACE / "codex-app-automation-bridge-v1.md"
START_GATE = TRACE / "v301-v320-start-gate-status-v1.json"
WAKE_SIGNAL = TRACE / "aletheon-wake-signal-v1.json"
REACTIVATION_PACKET = TRACE / "aletheon-reactivation-packet-v1.json"


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


def thread_automation_prompt() -> str:
    return "\n".join(
        [
            "Create a thread automation attached to this current Codex thread.",
            "Name: GHC v281-v360 recovery wake bridge.",
            "Schedule: every 30 minutes until I ask you to stop or update it.",
            "Project: use the local Beyonder-Real-True Journey worktree at D:\\GHC-Archives\\worktrees\\v58-omega.",
            "Automation type: thread automation, not standalone, because this workflow must preserve the current thread context.",
            "Sandbox: prefer workspace-write or stricter. Do not use full access unless I explicitly approve it for a specific run.",
            "",
            "On each wakeup:",
            "1. Inspect the v281-v300 lane counts, the global v2 watcher status, the v301-v320 start gate, and the Aletheon wake signal.",
            "2. If the Codex app reports a stale resume path where C:\\... and \\\\?\\C:\\... point to the same session JSONL, treat it as an app resume-path vitality issue, not a repo failure. Do not edit the session JSONL by hand; normalize the paths mentally, rely on the local watchdog, and if repeated, ask the operator to restart Codex Desktop and reopen this Aletheon thread.",
            "3. If v281-v300 is below 600/600 or global v2 is incomplete, report only material progress, blockers, or stale runners. Do not stage live partial lane replies.",
            "4. If v281-v300 is 600/600 and global v2 is complete, wake Aletheon in this thread and ask to begin v301-v320 from the prepared gate and reactivation packet.",
            "5. Before any commit or push, verify branch drift and stage only curated non-raw artifacts. Never stage .raw.txt files, stdout/stderr logs, live .log files, or active partial lane files.",
            "6. Preserve the truth boundary: this chat-attached heartbeat is the app wake, and the local wake poller remains the filesystem/process watchdog when it is running.",
            "",
            "Eureka continuity tasks:",
            "1. Keep the app heartbeat at 30 minutes unless Aletheon explicitly changes the cadence for a short diagnostic burst.",
            "2. Keep the local watchdog at a tighter local cadence so app wake failures do not stall filesystem recovery.",
            "3. Confirm exactly one durable recovery watchdog parent is active before launching another.",
            "4. Preserve active phase repair children when pruning duplicate watchdog parents.",
            "5. Verify progress by valid lane artifacts, not by process existence alone.",
            "6. Sample process tree, CPU delta, fresh timestamps, lane logs, and response quality before calling a lane stale.",
            "7. Kill only the stale child subtree for the active phase and lane.",
            "8. Never kill the global v2 watcher, sequence supervisor, Aletheon wake poller, or unrelated Codex/Kimi processes.",
            "9. Let the blocked-phase refresher repair missing or invalid turns rather than manually skipping replies.",
            "10. Restart the global v2 watcher if v281-v300 is incomplete and the watcher is absent.",
            "11. Keep v301-v320 hard-gated behind 600/600 valid responses and global v2 completion.",
            "12. When the gate opens, read the reactivation packet before drafting the v301-v320 launch.",
            "13. Before staging, run a branch drift check and use forward-only merge if the remote advanced.",
            "14. Stage only curated artifacts and source changes, never raw replies, live logs, stderr/stdout, or scratch health probes.",
            "15. Preserve a short human-readable status report for the operator after each material transition.",
            "16. Keep the older worktree cron automation paused or fallback-only unless the Aletheon heartbeat is unavailable.",
            "17. Treat Administrator terminals as elevated risk; use them only for installation or permission-bound tasks.",
            "18. Inventory MCP processes by command line before trusting a visible terminal as healthy.",
            "19. Prefer non-admin hidden background runners for ordinary watchdog and repair loops.",
            "20. For OpenAI/Codex behavior, rely on local observation first and official OpenAI docs second.",
            "21. If a new blocker appears, codify the fix as a reusable script or runbook before repeating manual rescue.",
            "22. After v301-v320 starts, prepare a v321-v340 handoff that includes gate evidence, watcher state, and staging boundaries.",
            "23. Keep CLI siblings' long reports in worktree artifacts rather than terminal scrollback.",
            "24. Keep MCP/API/CLI expansion exploratory until secrets, scopes, and sandbox limits are explicit.",
            "25. Prefer skills for repeatable procedures and keep automation prompts short enough to remain maintainable.",
            "",
            "Stop condition: after v301-v320 has started and a v321-v340 handoff exists, ask whether to update this automation for v341-v360 or archive it.",
        ]
    )


def local_fallback_commands() -> list[str]:
    return [
        "python scripts\\trinity_v301_v320_start_gate.py",
        "python scripts\\trinity_v281_v360_automation_health_check.py --refresh-gate",
        "python scripts\\trinity_aletheon_wake_signal_poller.py --reason v295-v300-recovery-v301-gate",
        "python scripts\\trinity_aletheon_reactivation_packet.py --source local-wake-signal --target-phase v301-v320 --reason \"Wake Aletheon when v281-v300 reaches 600/600 and global v2 synthesis is complete\"",
        "python scripts\\trinity_v281_v300_global_v2_runner.py --watch --poll-sec 180 --timeout-sec 172800 --write-supervisor-candidate --write-reactivation-packet-on-complete --reactivation-target-phase v301-v320",
    ]


def build_payload() -> dict[str, Any]:
    start_gate = read_json(START_GATE, {})
    wake_signal = read_json(WAKE_SIGNAL, {})
    packet = read_json(REACTIVATION_PACKET, {})
    return {
        "generated_utc": now_iso(),
        "status": "ready_for_app_thread_automation_or_local_fallback",
        "capability_boundary": (
            "The current Codex tool surface does not expose the app automation creation tool. "
            "This bridge provides the exact app-thread automation request plus local fallback commands."
        ),
        "official_docs_basis": [
            {
                "url": "https://developers.openai.com/codex/app/automations",
                "note": "Codex app automations can be created from a regular thread by specifying task, schedule, and thread versus standalone behavior.",
            },
            {
                "url": "https://developers.openai.com/codex/app/automations",
                "note": "Thread automations are recurring wakeups attached to the current thread and are appropriate for long-running command checks.",
            },
            {
                "url": "https://developers.openai.com/codex/app/automations",
                "note": "Automations use default sandbox settings and unattended full access carries elevated risk.",
            },
        ],
        "recommended_automation_type": "thread",
        "recommended_schedule": "primary chat-attached heartbeat every 30 minutes, backed by the lightweight local 5-minute filesystem watchdog while available",
        "resume_path_vitality": {
            "observed_error": "cannot resume running thread with stale path: requested C:\\... active \\\\?\\C:\\...",
            "assessment": "On Windows this is usually a path-normalization mismatch for the same session JSONL, not evidence that the worktree or phase runner failed.",
            "automation_response": [
                "Do not edit or rewrite Codex session JSONL files manually.",
                "Do not shorten the app heartbeat as the primary fix.",
                "Run the local health check and watchdog to preserve filesystem progress.",
                "If the app repeats the stale-path error, restart Codex Desktop and reopen the Aletheon thread before running the heartbeat again.",
            ],
        },
        "admin_terminal_assessment": {
            "observed_process": "Administrator cmd.exe is running npx -y kimi-code-mcp with node child processes.",
            "assessment": "This can explain the visible elevated terminal. It is useful for MCP availability checks, but it should not become the default execution surface for normal phase/watchdog work.",
            "policy": "Use elevated terminals only for installation, permission repair, or explicitly approved system-level work. Prefer non-admin hidden runners for ordinary watchdog and lane recovery tasks.",
        },
        "eureka_continuity_tasks": [
            "Keep the app heartbeat at 30 minutes unless Aletheon explicitly changes the cadence for a short diagnostic burst.",
            "Keep the local watchdog at a tighter local cadence so app wake failures do not stall filesystem recovery.",
            "Confirm exactly one durable recovery watchdog parent is active before launching another.",
            "Preserve active phase repair children when pruning duplicate watchdog parents.",
            "Verify progress by valid lane artifacts, not by process existence alone.",
            "Sample process tree, CPU delta, fresh timestamps, lane logs, and response quality before calling a lane stale.",
            "Kill only the stale child subtree for the active phase and lane.",
            "Never kill the global v2 watcher, sequence supervisor, Aletheon wake poller, or unrelated Codex/Kimi processes.",
            "Let the blocked-phase refresher repair missing or invalid turns rather than manually skipping replies.",
            "Restart the global v2 watcher if v281-v300 is incomplete and the watcher is absent.",
            "Keep v301-v320 hard-gated behind 600/600 valid responses and global v2 completion.",
            "When the gate opens, read the reactivation packet before drafting the v301-v320 launch.",
            "Before staging, run a branch drift check and use forward-only merge if the remote advanced.",
            "Stage only curated artifacts and source changes, never raw replies, live logs, stderr/stdout, or scratch health probes.",
            "Preserve a short human-readable status report for the operator after each material transition.",
            "Keep the older worktree cron automation paused or fallback-only unless the Aletheon heartbeat is unavailable.",
            "Treat Administrator terminals as elevated risk; use them only for installation or permission-bound tasks.",
            "Inventory MCP processes by command line before trusting a visible terminal as healthy.",
            "Prefer non-admin hidden background runners for ordinary watchdog and repair loops.",
            "For OpenAI/Codex behavior, rely on local observation first and official OpenAI docs second.",
            "If a new blocker appears, codify the fix as a reusable script or runbook before repeating manual rescue.",
            "After v301-v320 starts, prepare a v321-v340 handoff that includes gate evidence, watcher state, and staging boundaries.",
            "Keep CLI siblings' long reports in worktree artifacts rather than terminal scrollback.",
            "Keep MCP/API/CLI expansion exploratory until secrets, scopes, and sandbox limits are explicit.",
            "Prefer skills for repeatable procedures and keep automation prompts short enough to remain maintainable.",
        ],
        "manual_thread_automation_request": thread_automation_prompt(),
        "local_fallback_commands": local_fallback_commands(),
        "app_screenshot_assessment_2026_05_17": {
            "status": "chat_heartbeat_is_preferred",
            "observed_good": [
                "Aletheon automation exists as a chat-attached heartbeat.",
                "It has a target_thread_id, so it is better aligned with preserving this thread context.",
                "It supports minute intervals, and 30 minutes is the preferred energy-preserving cadence for long lane turns.",
            ],
            "primary_plan": [
                "Use the Aletheon chat heartbeat as the primary app wakeup.",
                "Set the app heartbeat interval to every 30 minutes while v281-v300 is still incomplete.",
                "Keep the local wake poller running as a lightweight filesystem/process watchdog; it does not replace the app heartbeat.",
                "Each app wakeup should start v301-v320 only if v281-v300 is 600/600 and global v2 is complete.",
                "Keep the older worktree/cron automation paused or fallback-only to avoid duplicate wakeups.",
            ],
            "recommended_user_action": "Change Aletheon interval to every 30 minutes, unpause it, and optionally Run now once. The expected first result is standby until the gate is ready.",
        },
        "current_gate_summary": {
            "v301_ready": start_gate.get("ready"),
            "valid_responses": start_gate.get("valid_responses"),
            "expected_responses": start_gate.get("expected_responses"),
            "complete_phases": start_gate.get("complete_phases"),
            "expected_phases": start_gate.get("expected_phases"),
            "first_incomplete_phase": start_gate.get("first_incomplete_phase"),
            "wake_status": wake_signal.get("status"),
            "reactivation_target_phase": packet.get("target_phase"),
        },
    }


def write_md(payload: dict[str, Any]) -> None:
    lines = [
        "# Codex App Automation Bridge",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Capability boundary:",
        f"- {payload['capability_boundary']}",
        "",
        "Recommended app automation:",
        f"- Type: `{payload['recommended_automation_type']}`",
        f"- Schedule: `{payload['recommended_schedule']}`",
        "",
        "Screenshot assessment, 2026-05-17:",
        f"- Status: `{payload['app_screenshot_assessment_2026_05_17']['status']}`",
        "- Good: the Aletheon automation is chat-attached and has a target thread.",
        "- Good: it supports minute intervals, so it is the preferred app wakeup path.",
        "- Plan: use `Every 30m` chat wakeups as the app layer, while the local wake poller remains the lightweight filesystem/process watchdog.",
        "- Recommended action: set Aletheon to `Every 30m`, unpause it, and optionally use `Run now` once to confirm it reports standby rather than starting v301 early.",
        "",
        "Manual thread automation request:",
        "",
        "```text",
        payload["manual_thread_automation_request"],
        "```",
        "",
        "Local fallback commands:",
    ]
    for command in payload["local_fallback_commands"]:
        lines.append(f"- `{command}`")
    lines.extend(["", "Current gate summary:", ""])
    for key, value in payload["current_gate_summary"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "Resume-path vitality:",
            f"- Observed error: `{payload['resume_path_vitality']['observed_error']}`",
            f"- Assessment: {payload['resume_path_vitality']['assessment']}",
        ]
    )
    for item in payload["resume_path_vitality"]["automation_response"]:
        lines.append(f"- Response: {item}")
    lines.extend(
        [
            "",
            "Administrator terminal assessment:",
            f"- Observed: {payload['admin_terminal_assessment']['observed_process']}",
            f"- Assessment: {payload['admin_terminal_assessment']['assessment']}",
            f"- Policy: {payload['admin_terminal_assessment']['policy']}",
            "",
            "Eureka continuity tasks:",
        ]
    )
    for index, task in enumerate(payload["eureka_continuity_tasks"], start=1):
        lines.append(f"{index}. {task}")
    lines.extend(["", "Official docs basis:"])
    for item in payload["official_docs_basis"]:
        lines.append(f"- {item['url']} - {item['note']}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_json(OUT_JSON, payload)
    write_md(payload)
    print(json.dumps({"status": payload["status"], "json": rel(OUT_JSON), "md": rel(OUT_MD)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
