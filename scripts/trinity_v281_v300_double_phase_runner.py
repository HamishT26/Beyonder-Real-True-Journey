#!/usr/bin/env python3
"""Run and synthesize one v281-v300 double Trinity phase."""

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
STOP_FILE = TRACE / f"{LANE}.stop"
PREP = ROOT / "scripts" / "trinity_v281_v300_double_phase_prep.py"
CODEX_LANES = {"arby", "aster_vale"}
KIMI_LANES = {"kimi"}
LANES = ("arby", "kimi", "aster_vale")
REQUIRED_LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")


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


def append_line(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip("\n") + "\n")


def redact(text: str) -> str:
    markers = [
        "__cf" + "_chl",
        "cf_" + "clearance=",
        "Authorization: " + "Bearer",
        "BEGIN " + "PRIVATE KEY",
        "api_" + "key",
        "api" + "key",
        "access_" + "token",
        "remote-control " + "token",
    ]
    clean = text
    for marker in markers:
        clean = clean.replace(marker, f"[REDACTED:{marker}]")
    return clean


def section(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?\s*(.*?)(?=^\s*(?:[-*]\s*)?\**(?:Receipt|Beta|Alpha|Omega|Blocker|Next-phase handoff)\**\s*:|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def clip(text: str, limit: int = 420) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def prompt_file_for_phase(phase: int) -> Path:
    return TRACE / f"{LANE}-phase-v{phase}-v1-prompts-v1.json"


def status_file_for_phase(phase: int, status_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in status_id) or "v1"
    return TRACE / f"{LANE}-phase-v{phase}-runner-status-{safe}.json"


def response_path(lane: str, phase: int, turn: int) -> Path:
    pretty = "aster-vale" if lane == "aster_vale" else lane
    return LANE_DIR / f"{pretty}-phase-v{phase}-response-{turn:02d}.txt"


def raw_path(lane: str, phase: int, turn: int) -> Path:
    pretty = "aster-vale" if lane == "aster_vale" else lane
    return LANE_DIR / f"{pretty}-phase-v{phase}-response-{turn:02d}.raw.txt"


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
    return sum(1 for label in REQUIRED_LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def lane_log(lane: str) -> Path:
    return LANE_DIR / f"{lane}.log"


def prompt_for(turn: dict[str, Any]) -> str:
    contract = turn.get("eureka_session_contract", {})
    guardrails = "\n".join(f"- {item}" for item in turn.get("guardrails", []))
    labels = "\n".join(f"- {item}:" for item in turn.get("required_labels", []))
    return "\n".join(
        [
            f"Marker: {turn['marker']}",
            f"Lane: {turn['name']}",
            f"Role: {turn['role']}",
            f"Topic: {turn['topic']}",
            f"Source dependency: {turn.get('source_dependency', 'none')}",
            "",
            "Eureka Trinity Session:",
            f"Beta: {contract.get('beta', 'Plan from verified inputs.')}",
            f"Alpha: {contract.get('alpha', 'Construct or refine safely.')}",
            f"Omega: {contract.get('omega', 'Test and document honestly.')}",
            "",
            "Guardrails:",
            guardrails,
            "",
            "Respond only with these labels:",
            labels,
        ]
    )


def kimi_prompt_for(turn: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Marker: {turn['marker']}",
            f"Lane: {turn['name']}",
            f"Topic: {turn['topic']}",
            f"Source dependency: {turn.get('source_dependency', 'none')}",
            "",
            "Respond from the prompt only. Do not run commands, inspect files, browse, or create artifacts.",
            "Keep the answer compact and under 240 words.",
            "Use these exact labels:",
            "Receipt:",
            "Beta:",
            "Alpha:",
            "Omega:",
            "Blocker:",
            "Next-phase handoff:",
        ]
    )


def run_codex(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    lane = turn["lane"]
    phase = int(turn["phase"])
    turn_number = int(turn["turn"])
    out = response_path(lane, phase, turn_number)
    raw = raw_path(lane, phase, turn_number)
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--disable",
        "plugins",
        "--sandbox",
        "read-only",
        "-C",
        str(ROOT),
        "-o",
        str(out),
        prompt_for(turn),
    ]
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
    raw.write_text(redact((proc.stdout or "")[-12000:] + "\n--- STDERR ---\n" + (proc.stderr or "")[-12000:]), encoding="utf-8")
    return {"ok": proc.returncode == 0 and is_valid_response(out), "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "response_file": rel(out) if out.exists() else None}


def run_kimi(turn: dict[str, Any], timeout: int, max_steps: int) -> dict[str, Any]:
    lane = turn["lane"]
    phase = int(turn["phase"])
    turn_number = int(turn["turn"])
    out = response_path(lane, phase, turn_number)
    raw = raw_path(lane, phase, turn_number)
    cmd = [
        "kimi",
        "--work-dir",
        str(ROOT),
        "--print",
        "--final-message-only",
        "--max-steps-per-turn",
        str(max_steps),
        "--prompt",
        kimi_prompt_for(turn),
    ]
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
    out.write_text(redact(proc.stdout or ""), encoding="utf-8")
    raw.write_text(redact((proc.stderr or "")[-12000:]), encoding="utf-8")
    return {"ok": proc.returncode == 0 and is_valid_response(out), "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "response_file": rel(out) if out.exists() else None}


def completed_for_phase(phase: int) -> int:
    if not LANE_DIR.exists():
        return 0
    return sum(
        1
        for path in LANE_DIR.glob(f"*-phase-v{phase}-response-*.txt")
        if not path.name.endswith(".raw.txt") and is_valid_response(path)
    )


def run_lane(lane: str, turns: list[dict[str, Any]], timeout: int, kimi_max_steps: int, status: dict[str, Any]) -> None:
    for turn in turns:
        phase = int(turn["phase"])
        turn_number = int(turn["turn"])
        out = response_path(lane, phase, turn_number)
        if STOP_FILE.exists():
            status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, "status": "stopped_by_stop_file"})
            break
        if is_valid_response(out):
            status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, "status": "skipped_existing"})
            continue
        append_line(lane_log(lane), f"{now_iso()} | V{phase}-START | turn={turn_number:02d} | marker={turn['marker']}")
        try:
            if lane in CODEX_LANES:
                result = run_codex(turn, timeout)
            elif lane in KIMI_LANES:
                result = run_kimi(turn, timeout, kimi_max_steps)
            else:
                result = {"ok": False, "error": "unknown_lane"}
        except subprocess.TimeoutExpired:
            result = {"ok": False, "timed_out": True}
        append_line(lane_log(lane), f"{now_iso()} | V{phase}-END | turn={turn_number:02d} | ok={result.get('ok')} | response={result.get('response_file')}")
        status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, **result})
        status["completed_for_phase"] = completed_for_phase(phase)


def synthesize_phase(phase: int, prompt_file: Path) -> dict[str, Any]:
    prompt_payload = read_json(prompt_file, {})
    lanes = []
    for lane in LANES:
        lane_items = []
        for turn in prompt_payload.get("prompts", []):
            if turn.get("lane") != lane:
                continue
            path = response_path(lane, phase, int(turn["turn"]))
            if path.exists() and path.stat().st_size > 0:
                if not is_valid_response(path):
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                lane_items.append(
                    {
                        "turn": turn["turn"],
                        "topic": turn["topic"],
                        "path": rel(path),
                        "receipt": clip(section(text, "Receipt")),
                        "beta": clip(section(text, "Beta")),
                        "alpha": clip(section(text, "Alpha")),
                        "omega": clip(section(text, "Omega")),
                        "blocker": clip(section(text, "Blocker")),
                        "next_phase_handoff": clip(section(text, "Next-phase handoff")),
                    }
                )
        lanes.append({"lane": lane, "completed": len(lane_items), "expected": 10, "responses": lane_items})
    complete_count = sum(lane["completed"] for lane in lanes)
    synthesis = {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "phase": phase,
        "phase_version": "v2",
        "status": "complete_synthesized" if complete_count == 30 else "incomplete_synthesized",
        "completed_responses": complete_count,
        "expected_responses": 30,
        "source_prompt_file": rel(prompt_file),
        "lanes": lanes,
        "v2_decisions": [
            "Keep lane v1 outputs advisory until reviewed and curated.",
            "Prepare the next phase only after all 30 lane replies exist or a blocker is explicitly accepted.",
            "Continue using proof receipts and truth boundaries rather than broad success claims.",
        ],
    }
    out_json = TRACE / f"{LANE}-phase-v{phase}-v2-synthesis-v1.json"
    out_md = TRACE / f"{LANE}-phase-v{phase}-v2-synthesis-v1.md"
    write_json(out_json, synthesis)
    lines = [
        f"# v{phase} Double Trinity v2 Synthesis",
        "",
        f"Generated UTC: `{synthesis['generated_utc']}`",
        f"Status: `{synthesis['status']}`",
        f"Completion: `{complete_count}/30`",
        "",
        "Lane completion:",
    ]
    for lane in lanes:
        lines.append(f"- {lane['lane']}: {lane['completed']}/{lane['expected']}")
    lines.extend(["", "v2 decisions:"])
    for item in synthesis["v2_decisions"]:
        lines.append(f"- {item}")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if complete_count == 30:
        subprocess.run(
            [
                sys.executable,
                str(PREP),
                "--source-phase",
                "v281-v300",
                "--source-dependency",
                rel(out_json),
                "--phase",
                str(phase + 1),
            ],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=600,
            check=False,
        )
    return synthesis


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=281)
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--timeout-sec", type=int, default=43200)
    parser.add_argument("--status-id", default="v1")
    parser.add_argument("--max-turns-per-lane", type=int, default=10)
    parser.add_argument("--only-lane", choices=list(LANES), default="")
    parser.add_argument("--kimi-max-steps", type=int, default=6)
    parser.add_argument("--synthesize-on-complete", action="store_true")
    args = parser.parse_args()

    prompt_file = Path(args.prompt_file) if args.prompt_file else prompt_file_for_phase(args.phase)
    if not prompt_file.is_absolute():
        prompt_file = ROOT / prompt_file
    prompt_payload = read_json(prompt_file, {})
    status_file = status_file_for_phase(args.phase, args.status_id)
    status = {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "phase": args.phase,
        "phase_version": "v1",
        "status": "running",
        "status_file": rel(status_file),
        "prompt_file": rel(prompt_file),
        "timeout_sec": args.timeout_sec,
        "events": [],
    }
    write_json(status_file, status)

    selected_lanes = (args.only_lane,) if args.only_lane else LANES
    for lane in selected_lanes:
        turns = [turn for turn in prompt_payload.get("prompts", []) if turn.get("lane") == lane]
        turns = turns[: max(0, args.max_turns_per_lane)]
        run_lane(lane, turns, args.timeout_sec, args.kimi_max_steps, status)
        write_json(status_file, status)

    status["completed_for_phase"] = completed_for_phase(args.phase)
    status["status"] = "complete" if status["completed_for_phase"] >= len(prompt_payload.get("prompts", [])) else "incomplete"
    if args.synthesize_on_complete:
        synthesis = synthesize_phase(args.phase, prompt_file)
        status["v2_synthesis_status"] = synthesis["status"]
        status["v2_synthesis_completed_responses"] = synthesis["completed_responses"]
    status["finished_utc"] = now_iso()
    write_json(status_file, status)
    print(json.dumps({"status": status["status"], "completed_for_phase": status["completed_for_phase"], "status_file": rel(status_file)}, indent=2))
    return 0 if status["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
