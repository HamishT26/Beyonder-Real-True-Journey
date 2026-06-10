#!/usr/bin/env python3
"""Write an honest Aletheon reactivation packet for long-running local controllers."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
PACKET_JSON = TRACE / "aletheon-reactivation-packet-v1.json"
PACKET_MD = TRACE / "aletheon-reactivation-packet-v1.md"


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


def packet_prompt(source: str, target_phase: str) -> str:
    return "\n".join(
        [
            "Aletheon reactivation request:",
            f"Source controller: {source}",
            f"Target phase: {target_phase}",
            "Please reopen the Beyonder-Real-True Journey worktree and inspect the latest status files before acting.",
            "Required first checks:",
            "1. Verify branch and remote drift.",
            "2. Verify valid-response counts and blocked phases.",
            "3. Stage only curated non-raw artifacts.",
            "4. Continue forward-only; do not reset, rebase, force-push, or publish raw logs.",
            "If v281-v300 and its global v2 synthesis are complete, begin the prepared next phase plan.",
        ]
    )


def write_packet(source: str, target_phase: str, reason: str) -> dict[str, Any]:
    payload = {
        "generated_utc": now_iso(),
        "source": source,
        "target_phase": target_phase,
        "reason": reason,
        "status": "reactivation_packet_ready",
        "capability_boundary": (
            "This packet is a durable re-entry prompt and proof pointer. It does not by itself wake a Codex app thread."
        ),
        "proof_files": [
            "docs/trinity-live-traces/v281-v300-double-trinity-v1-sequence-supervisor-status-v1.json",
            "docs/trinity-live-traces/v281-v300-double-trinity-global-v2-runner-status-v1.json",
            "docs/trinity-live-traces/v281-v300-double-trinity-blocked-phase-refresh-status-v1.json",
            "docs/trinity-live-traces/v301-v320-aletheon-base-plan-v1.json",
            "docs/trinity-live-traces/codex-app-automation-bridge-v1.json",
        ],
        "app_automation_bridge": "docs/trinity-live-traces/codex-app-automation-bridge-v1.md",
        "reactivation_prompt": packet_prompt(source, target_phase),
    }
    write_json(PACKET_JSON, payload)
    lines = [
        "# Aletheon Reactivation Packet",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Source: `{source}`",
        f"Target phase: `{target_phase}`",
        f"Status: `{payload['status']}`",
        "",
        "Capability boundary:",
        f"- {payload['capability_boundary']}",
        "",
        "Proof files:",
    ]
    for item in payload["proof_files"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "App automation bridge:", f"- `{payload['app_automation_bridge']}`"])
    lines.extend(["", "Reactivation prompt:", "", "```text", payload["reactivation_prompt"], "```"])
    PACKET_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="continuity-supervisor")
    parser.add_argument("--target-phase", default="v341-v360")
    parser.add_argument("--reason", default="long-running phase completion handoff")
    args = parser.parse_args()
    payload = write_packet(args.source, args.target_phase, args.reason)
    print(json.dumps({"status": payload["status"], "packet": rel(PACKET_JSON)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
