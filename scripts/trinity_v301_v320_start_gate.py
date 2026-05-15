#!/usr/bin/env python3
"""Gate v301-v320 execution on complete v281-v300 and global v2 evidence."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE_DIR = TRACE / "v281-v300-double-trinity-lane-logs"
GLOBAL_V2_STATUS = TRACE / "v281-v300-double-trinity-global-v2-runner-status-v1.json"
SEQUENCE_STATUS = TRACE / "v281-v300-double-trinity-v1-sequence-supervisor-status-v1.json"
GATE_JSON = TRACE / "v301-v320-start-gate-status-v1.json"
GATE_MD = TRACE / "v301-v320-start-gate-status-v1.md"

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


def phase_counts() -> list[dict[str, Any]]:
    rows = []
    for phase in PHASES:
        lanes = {}
        for lane in LANES:
            valid = [turn for turn in range(1, 11) if valid_response(response_path(lane, phase, turn))]
            lanes[lane] = {"valid": len(valid), "expected": 10, "valid_turns": valid}
        total = sum(item["valid"] for item in lanes.values())
        rows.append({"phase": phase, "valid": total, "expected": 30, "complete": total == 30, "lanes": lanes})
    return rows


def global_v2_state() -> dict[str, Any]:
    payload = read_json(GLOBAL_V2_STATUS, {})
    status = str(payload.get("status", "")).lower()
    action = str(payload.get("action", "")).lower()
    complete = status in {"global_v2_complete", "complete"} or action in {"global_v2_complete", "complete"}
    return {
        "path": rel(GLOBAL_V2_STATUS),
        "exists": GLOBAL_V2_STATUS.exists(),
        "status": status,
        "action": action,
        "complete": complete,
    }


def build_gate() -> dict[str, Any]:
    counts = phase_counts()
    valid_total = sum(item["valid"] for item in counts)
    complete_phases = sum(1 for item in counts if item["complete"])
    first_incomplete = next((item["phase"] for item in counts if not item["complete"]), None)
    latest_complete = max((item["phase"] for item in counts if item["complete"]), default=None)
    v2 = global_v2_state()
    ready = valid_total == 600 and complete_phases == 20 and v2["complete"]
    sequence = read_json(SEQUENCE_STATUS, {})
    blockers = []
    if valid_total != 600:
        blockers.append(f"v281-v300 valid replies are {valid_total}/600")
    if complete_phases != 20:
        blockers.append(f"complete phases are {complete_phases}/20")
    if not v2["complete"]:
        blockers.append("global v2 synthesis is not complete")
    return {
        "generated_utc": now_iso(),
        "status": "ready_to_start_v301_v320" if ready else "waiting_for_v281_v300_and_global_v2",
        "ready": ready,
        "valid_responses": valid_total,
        "expected_responses": 600,
        "complete_phases": complete_phases,
        "expected_phases": 20,
        "latest_complete_phase": latest_complete,
        "first_incomplete_phase": first_incomplete,
        "phase_counts": counts,
        "global_v2": v2,
        "sequence_supervisor": {
            "path": rel(SEQUENCE_STATUS),
            "exists": SEQUENCE_STATUS.exists(),
            "status": sequence.get("status"),
            "latest_phase": sequence.get("latest_phase"),
            "updated_utc": sequence.get("updated_utc"),
        },
        "blockers": blockers,
        "next_action": (
            "Start v301-v320 from docs/trinity-live-traces/v301-v320-trinity-hybrid-master-plan-v1.md"
            if ready
            else "Keep v301-v320 on standby; do not stage live partial lane replies."
        ),
    }


def write_md(payload: dict[str, Any]) -> None:
    lines = [
        "# v301-v320 Start Gate Status",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Ready: `{payload['ready']}`",
        f"Responses: `{payload['valid_responses']}/{payload['expected_responses']}`",
        f"Complete phases: `{payload['complete_phases']}/{payload['expected_phases']}`",
        f"Latest complete phase: `v{payload['latest_complete_phase']}`",
        f"First incomplete phase: `v{payload['first_incomplete_phase']}`",
        f"Global v2 complete: `{payload['global_v2']['complete']}`",
        "",
        "Blockers:",
    ]
    blockers = payload.get("blockers") or ["none"]
    for blocker in blockers:
        lines.append(f"- {blocker}")
    lines.extend(["", f"Next action: {payload['next_action']}"])
    GATE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload = build_gate()
    write_json(GATE_JSON, payload)
    write_md(payload)
    print(json.dumps({"status": payload["status"], "ready": payload["ready"], "valid": payload["valid_responses"], "gate": rel(GATE_JSON)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
