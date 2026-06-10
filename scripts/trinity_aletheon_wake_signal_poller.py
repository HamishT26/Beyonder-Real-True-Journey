#!/usr/bin/env python3
"""Write a durable Aletheon wake signal when long-running phase gates complete."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE_DIR = TRACE / "v281-v300-double-trinity-lane-logs"
GLOBAL_V2_STATUS = TRACE / "v281-v300-double-trinity-global-v2-runner-status-v1.json"
WAKE_JSON = TRACE / "aletheon-wake-signal-v1.json"
WAKE_MD = TRACE / "aletheon-wake-signal-v1.md"
STOP_FILE = TRACE / "aletheon-wake-signal-poller.stop"

LANES = ("arby", "kimi", "aster-vale")
PHASES = range(281, 301)
LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")


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


def response_path(lane: str, phase: int, turn: int) -> Path:
    return LANE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    invalid = ("Max number of steps reached", "To resume this session:", "Traceback (most recent call last)")
    if any(marker in text for marker in invalid):
        return False
    return sum(1 for label in LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def phase_counts() -> dict[str, Any]:
    phase_rows = []
    for phase in PHASES:
        lanes = {}
        for lane in LANES:
            valid = [turn for turn in range(1, 11) if valid_response(response_path(lane, phase, turn))]
            lanes[lane] = {"valid": len(valid), "expected": 10}
        total = sum(item["valid"] for item in lanes.values())
        phase_rows.append({"phase": phase, "valid": total, "expected": 30, "complete": total == 30, "lanes": lanes})
    return {
        "valid_responses": sum(item["valid"] for item in phase_rows),
        "expected_responses": 600,
        "complete_phases": sum(1 for item in phase_rows if item["complete"]),
        "expected_phases": 20,
        "phase_rows": phase_rows,
    }


def global_v2_complete() -> dict[str, Any]:
    status = read_json(GLOBAL_V2_STATUS, {})
    state = str(status.get("status", "")).lower()
    action = str(status.get("action", "")).lower()
    complete = state in {"global_v2_complete", "complete"} or action in {"global_v2_complete", "complete"}
    return {"path": rel(GLOBAL_V2_STATUS), "exists": GLOBAL_V2_STATUS.exists(), "status": state, "action": action, "complete": complete}


def wake_payload(reason: str) -> dict[str, Any]:
    counts = phase_counts()
    v2 = global_v2_complete()
    ready = counts["valid_responses"] == counts["expected_responses"] and v2["complete"]
    return {
        "generated_utc": now_iso(),
        "status": "wake_ready" if ready else "waiting",
        "reason": reason,
        "capability_boundary": "This is a durable local wake signal. It cannot force the Codex desktop app to resume without an exposed app-level automation surface.",
        "phase_counts": counts,
        "global_v2": v2,
        "resume_prompt": "\n".join(
            [
                "Aletheon, resume from this wake signal.",
                "First inspect v281-v300 counts, global v2 status, and branch drift.",
                "If complete, begin the v301-v320 master plan; otherwise keep monitoring without staging live partials.",
            ]
        ),
        "next_files": [
            "docs/trinity-live-traces/v301-v320-trinity-hybrid-master-plan-v1.json",
            "docs/trinity-live-traces/v281-v360-gmut-trinity-mandala-waiting-room-synthesis-v1.json",
            "docs/trinity-live-traces/aletheon-reactivation-system-design-v2.json",
        ],
    }


def write_wake(payload: dict[str, Any]) -> None:
    write_json(WAKE_JSON, payload)
    lines = [
        "# Aletheon Wake Signal",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Completion: `{payload['phase_counts']['valid_responses']}/{payload['phase_counts']['expected_responses']}`",
        f"Global v2 complete: `{payload['global_v2']['complete']}`",
        "",
        f"Boundary: {payload['capability_boundary']}",
        "",
        "Resume prompt:",
        "",
        "```text",
        payload["resume_prompt"],
        "```",
    ]
    WAKE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--poll-sec", type=int, default=300)
    parser.add_argument("--reason", default="v281-v300 completion monitor")
    args = parser.parse_args()

    while True:
        payload = wake_payload(args.reason)
        write_wake(payload)
        print(json.dumps({"status": payload["status"], "wake": rel(WAKE_JSON)}, indent=2))
        if not args.watch or payload["status"] == "wake_ready" or STOP_FILE.exists():
            return 0 if payload["status"] in {"wake_ready", "waiting"} else 1
        time.sleep(max(30, args.poll_sec))


if __name__ == "__main__":
    raise SystemExit(main())
