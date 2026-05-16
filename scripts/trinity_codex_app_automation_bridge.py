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
            "Schedule: every 5 minutes until I ask you to stop or update it.",
            "Project: use the local Beyonder-Real-True Journey worktree at D:\\GHC-Archives\\worktrees\\v58-omega.",
            "Automation type: thread automation, not standalone, because this workflow must preserve the current thread context.",
            "Sandbox: prefer workspace-write or stricter. Do not use full access unless I explicitly approve it for a specific run.",
            "",
            "On each wakeup:",
            "1. Inspect the v281-v300 lane counts, the global v2 watcher status, the v301-v320 start gate, and the Aletheon wake signal.",
            "2. If v281-v300 is below 600/600 or global v2 is incomplete, report only material progress, blockers, or stale runners. Do not stage live partial lane replies.",
            "3. If v281-v300 is 600/600 and global v2 is complete, wake Aletheon in this thread and ask to begin v301-v320 from the prepared gate and reactivation packet.",
            "4. Before any commit or push, verify branch drift and stage only curated non-raw artifacts. Never stage .raw.txt files, stdout/stderr logs, live .log files, or active partial lane files.",
            "5. Preserve the truth boundary: the local wake signal is a durable prompt, not proof that the app can resume itself without this automation.",
            "",
            "Stop condition: after v301-v320 has started and a v321-v340 handoff exists, ask whether to update this automation for v341-v360 or archive it.",
        ]
    )


def local_fallback_commands() -> list[str]:
    return [
        "python scripts\\trinity_v301_v320_start_gate.py",
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
        "recommended_schedule": "every 5 minutes until v301-v320 starts or the user updates the automation",
        "manual_thread_automation_request": thread_automation_prompt(),
        "local_fallback_commands": local_fallback_commands(),
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
