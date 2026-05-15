#!/usr/bin/env python3
"""Wait for all v281-v300 v1 lane outputs, then write one global v2 synthesis."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v281-v300-double-trinity"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
PREP = ROOT / "scripts" / "trinity_v281_v300_global_v2_prep.py"
PLAN_JSON = TRACE / f"{LANE}-global-v2-session-plan-v1.json"
SYNTH_JSON = TRACE / f"{LANE}-global-v2-synthesis-v1.json"
SYNTH_MD = TRACE / f"{LANE}-global-v2-synthesis-v1.md"
STATUS_JSON = TRACE / f"{LANE}-global-v2-runner-status-v1.json"
STATUS_MD = TRACE / f"{LANE}-global-v2-runner-status-v1.md"
PHASES = list(range(281, 301))
LANES = ("arby", "kimi", "aster-vale")
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


def is_valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    invalid_markers = (
        "Max number of steps reached",
        "To resume this session:",
        "Traceback (most recent call last)",
    )
    if any(marker in text for marker in invalid_markers):
        return False
    return sum(1 for label in LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def section(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?\s*(.*?)(?=^\s*(?:[-*]\s*)?\**(?:Receipt|Beta|Alpha|Omega|Blocker|Next-phase handoff)\**\s*:|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def clip(text: str, limit: int = 360) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def phase_counts(phase: int) -> dict[str, Any]:
    lanes: dict[str, Any] = {}
    for lane in LANES:
        valid_turns = [turn for turn in range(1, 11) if is_valid_response(response_path(lane, phase, turn))]
        lanes[lane] = {
            "valid_responses": len(valid_turns),
            "expected_responses": 10,
            "valid_turns": valid_turns,
        }
    total = sum(item["valid_responses"] for item in lanes.values())
    return {
        "phase": phase,
        "valid_responses": total,
        "expected_responses": 30,
        "status": "complete" if total == 30 else "waiting_for_v1",
        "lanes": lanes,
    }


def all_phase_counts() -> list[dict[str, Any]]:
    return [phase_counts(phase) for phase in PHASES]


def ready(counts: list[dict[str, Any]]) -> bool:
    return all(item["valid_responses"] == item["expected_responses"] for item in counts)


def run_prep(write_supervisor_candidate: bool) -> dict[str, Any]:
    cmd = [sys.executable, str(PREP)]
    if write_supervisor_candidate:
        cmd.append("--write-supervisor-candidate")
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=600,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-2000:],
        "stderr_tail": (proc.stderr or "")[-2000:],
    }


def lane_digest(phase: int, lane: str) -> dict[str, Any]:
    receipts = []
    handoffs = []
    blockers = []
    for turn in range(1, 11):
        path = response_path(lane, phase, turn)
        if not is_valid_response(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        receipts.append(clip(section(text, "Receipt"), 220))
        handoffs.append(clip(section(text, "Next-phase handoff"), 220))
        blocker = section(text, "Blocker")
        if blocker and blocker.lower() not in {"none", "n/a", "no blocker"}:
            blockers.append(clip(blocker, 220))
    return {
        "lane": lane,
        "valid_responses": len(receipts),
        "receipt_samples": receipts[:3],
        "handoff_samples": handoffs[:3],
        "blocker_samples": blockers[:3],
    }


def build_synthesis(plan: dict[str, Any], counts: list[dict[str, Any]]) -> dict[str, Any]:
    task_by_phase = {int(item["phase"]): item for item in plan.get("phase_v2_tasks", [])}
    phases = []
    for item in counts:
        phase = int(item["phase"])
        task = task_by_phase.get(phase, {})
        phases.append(
            {
                "phase": phase,
                "status": "v2_ready" if item["status"] == "complete" else "waiting_for_v1",
                "input_counts": item,
                "lane_digests": [lane_digest(phase, lane) for lane in LANES],
                "v2_task_pack": {
                    "system_expansions": task.get("system_expansions", []),
                    "commands": task.get("commands", []),
                    "skills": task.get("skills", []),
                    "eureka_proposals": task.get("eureka_proposals", []),
                },
                "v2_declaration": (
                    "Aletheon v2 synthesis is ready for curated execution from all 30 lane responses."
                    if item["status"] == "complete"
                    else "Deferred until all 30 lane responses pass validity gates."
                ),
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "status": "global_v2_complete" if ready(counts) else "waiting_for_all_v1_phases",
        "source_plan": rel(PLAN_JSON),
        "valid_v1_responses": sum(item["valid_responses"] for item in counts),
        "expected_v1_responses": len(PHASES) * 30,
        "phases": phases,
        "publication_policy": [
            "Curate summaries and proof receipts only.",
            "Keep raw transport logs quarantined outside publication commits.",
            "Treat placeholder or resume output as invalid until repaired.",
            "Do not mark the Continuity Supervisor official until persistence proof is reviewed by the user.",
        ],
    }


def write_synthesis_md(synthesis: dict[str, Any]) -> None:
    lines = [
        "# v281-v300 Global v2 Synthesis",
        "",
        f"Generated UTC: `{synthesis['generated_utc']}`",
        f"Status: `{synthesis['status']}`",
        f"Valid v1 responses: `{synthesis['valid_v1_responses']}/{synthesis['expected_v1_responses']}`",
        "",
        "Phase Summary:",
    ]
    for phase in synthesis["phases"]:
        counts = phase["input_counts"]
        lines.append(f"- v{phase['phase']}: {counts['valid_responses']}/{counts['expected_responses']} valid, `{phase['status']}`.")
    lines.extend(["", "Publication Policy:"])
    for item in synthesis["publication_policy"]:
        lines.append(f"- {item}")
    SYNTH_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_status(status: dict[str, Any]) -> None:
    write_json(STATUS_JSON, status)
    lines = [
        "# v281-v300 Global v2 Runner Status",
        "",
        f"Generated UTC: `{status.get('generated_utc')}`",
        f"Updated UTC: `{status.get('updated_utc')}`",
        f"Status: `{status.get('status')}`",
        f"Valid v1 responses: `{status.get('valid_v1_responses')}/{status.get('expected_v1_responses')}`",
        "",
        "Recent Events:",
    ]
    for event in status.get("events", [])[-12:]:
        lines.append(f"- `{event.get('time')}` {event.get('status')}: {event.get('valid_v1_responses')}/{event.get('expected_v1_responses')}")
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_once(write_supervisor_candidate: bool) -> dict[str, Any]:
    prep = run_prep(write_supervisor_candidate)
    counts = all_phase_counts()
    synthesis = build_synthesis(read_json(PLAN_JSON, {}), counts)
    write_json(SYNTH_JSON, synthesis)
    write_synthesis_md(synthesis)
    return {
        "prep": prep,
        "status": synthesis["status"],
        "valid_v1_responses": synthesis["valid_v1_responses"],
        "expected_v1_responses": synthesis["expected_v1_responses"],
        "synthesis": rel(SYNTH_JSON),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--poll-sec", type=int, default=180)
    parser.add_argument("--timeout-sec", type=int, default=86400)
    parser.add_argument("--write-supervisor-candidate", action="store_true")
    args = parser.parse_args()

    status: dict[str, Any] = {
        "generated_utc": now_iso(),
        "status": "running" if args.watch else "single_check",
        "events": [],
    }
    deadline = time.time() + args.timeout_sec
    while True:
        counts = all_phase_counts()
        valid = sum(item["valid_responses"] for item in counts)
        expected = len(PHASES) * 30
        status.update(
            {
                "updated_utc": now_iso(),
                "valid_v1_responses": valid,
                "expected_v1_responses": expected,
                "phase_counts": counts,
            }
        )
        status["events"].append(
            {
                "time": now_iso(),
                "status": "ready" if ready(counts) else "waiting_for_all_v1_phases",
                "valid_v1_responses": valid,
                "expected_v1_responses": expected,
            }
        )
        write_status(status)
        if ready(counts) or not args.watch:
            result = run_once(args.write_supervisor_candidate)
            status.update({"updated_utc": now_iso(), **result})
            write_status(status)
            print(json.dumps(result, indent=2))
            return 0 if result["status"] == "global_v2_complete" else 2
        if time.time() >= deadline:
            status["status"] = "timed_out_waiting_for_all_v1"
            status["updated_utc"] = now_iso()
            write_status(status)
            print(json.dumps({"status": status["status"], "valid_v1_responses": valid, "expected_v1_responses": expected}, indent=2))
            return 1
        time.sleep(max(1, args.poll_sec))


if __name__ == "__main__":
    raise SystemExit(main())
