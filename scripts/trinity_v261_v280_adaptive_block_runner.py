#!/usr/bin/env python3
"""Run a prepared v261-v280 adaptive prompt block for one council lane."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v261-v280-adaptive-council"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
STOP_FILE = TRACE / f"{LANE}.stop"
CLOSEOUT = TRACE / f"{LANE}-prep-closeout-v1.json"
CODEX_LANES = {"arby", "aster_vale"}
KIMI_LANES = {"kimi"}


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


def lane_log(lane: str) -> Path:
    return LANE_DIR / f"{lane}.log"


def pretty_lane(lane: str) -> str:
    return "aster-vale" if lane == "aster_vale" else lane


def response_path(lane: str, block: int, turn: int) -> Path:
    return LANE_DIR / f"{pretty_lane(lane)}-block-{block:02d}-response-{turn:02d}.txt"


def raw_path(lane: str, block: int, turn: int) -> Path:
    return LANE_DIR / f"{pretty_lane(lane)}-block-{block:02d}-response-{turn:02d}.raw.txt"


def status_path(status_id: str, lane: str, block: int) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in status_id) or "v1"
    return TRACE / f"{LANE}-block-{block:02d}-runner-status-{lane}-{safe}.json"


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
    redacted = text
    for marker in markers:
        redacted = redacted.replace(marker, f"[REDACTED:{marker}]")
    return redacted


def prompt_for(turn: dict[str, Any]) -> str:
    contract = "\n".join(f"- {item}" for item in turn.get("prompt_contract", []))
    return "\n".join(
        [
            f"Marker: {turn['marker']}",
            f"Lane: {turn['name']}",
            f"Role: {turn['role']}",
            f"Topic: {turn['topic']}",
            f"Synthesis dependency: {turn.get('synthesis_dependency', 'none')}",
            "",
            "Contract:",
            contract,
            "",
            "Respond only. Include these labels:",
            "Receipt:",
            "Blocker:",
            "Refinement:",
            "Next-cycle proposal:",
        ]
    )


def run_codex(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    lane = turn["lane"]
    block = int(turn["block"])
    turn_number = int(turn["turn"])
    out = response_path(lane, block, turn_number)
    raw = raw_path(lane, block, turn_number)
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
    return {"ok": proc.returncode == 0 and out.exists() and out.stat().st_size > 0, "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "response_file": rel(out) if out.exists() else None}


def run_kimi(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    lane = turn["lane"]
    block = int(turn["block"])
    turn_number = int(turn["turn"])
    out = response_path(lane, block, turn_number)
    raw = raw_path(lane, block, turn_number)
    cmd = [
        "kimi",
        "--work-dir",
        str(ROOT),
        "--print",
        "--final-message-only",
        "--max-steps-per-turn",
        "1",
        "--prompt",
        prompt_for(turn),
    ]
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
    out.write_text(redact(proc.stdout or ""), encoding="utf-8")
    raw.write_text(redact((proc.stderr or "")[-12000:]), encoding="utf-8")
    return {"ok": proc.returncode == 0 and out.exists() and out.stat().st_size > 0, "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "response_file": rel(out) if out.exists() else None}


def completed_for_block(block: int) -> int:
    if not LANE_DIR.exists():
        return 0
    return sum(1 for path in LANE_DIR.glob(f"*-block-{block:02d}-response-*.txt") if not path.name.endswith(".raw.txt") and path.stat().st_size > 0)


def update_closeout(block: int) -> None:
    closeout = read_json(CLOSEOUT, {})
    completed = completed_for_block(block)
    closeout[f"block_{block:02d}_completed_responses"] = completed
    closeout[f"block_{block:02d}_status"] = "complete" if completed >= 9 else "running"
    closeout["latest_active_block"] = block
    closeout["multiplex_refresh_seconds"] = 30
    write_json(CLOSEOUT, closeout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--timeout-sec", type=int, default=7200)
    parser.add_argument("--status-id", default="v1")
    args = parser.parse_args()

    prompt_file = Path(args.prompt_file)
    if not prompt_file.is_absolute():
        prompt_file = ROOT / prompt_file
    prompts_payload = read_json(prompt_file, {})
    block = int(prompts_payload.get("block", 2))
    turns = [turn for turn in prompts_payload.get("prompts", []) if turn.get("lane") == args.lane]
    status_file = status_path(args.status_id, args.lane, block)
    status = {
        "generated_utc": now_iso(),
        "phase_range": "v261-v280",
        "block": block,
        "lane": args.lane,
        "status_id": args.status_id,
        "status_file": rel(status_file),
        "prompt_file": rel(prompt_file),
        "selected_count": len(turns),
        "events": [],
        "stop_file": rel(STOP_FILE),
    }
    write_json(status_file, status)
    marker_prefix = f"V261-BLOCK-{block:02d}"
    for turn in turns:
        turn_number = int(turn["turn"])
        out = response_path(args.lane, block, turn_number)
        if STOP_FILE.exists():
            status["events"].append({"time": now_iso(), "turn": turn_number, "status": "stopped_by_stop_file"})
            break
        if out.exists() and out.stat().st_size > 0:
            status["events"].append({"time": now_iso(), "turn": turn_number, "status": "skipped_existing"})
            continue
        append_line(lane_log(args.lane), f"{now_iso()} | {marker_prefix}-START | turn={turn_number:02d} | marker={turn['marker']}")
        try:
            if args.lane in CODEX_LANES:
                result = run_codex(turn, args.timeout_sec)
            elif args.lane in KIMI_LANES:
                result = run_kimi(turn, args.timeout_sec)
            else:
                result = {"ok": False, "error": "unknown_lane"}
        except subprocess.TimeoutExpired:
            result = {"ok": False, "timed_out": True}
        append_line(lane_log(args.lane), f"{now_iso()} | {marker_prefix}-END | turn={turn_number:02d} | ok={result.get('ok')} | response={result.get('response_file')}")
        if result.get("response_file") and out.exists():
            text = out.read_text(encoding="utf-8", errors="replace")
            append_line(lane_log(args.lane), f"{now_iso()} | {marker_prefix}-RESPONSE-BEGIN | turn={turn_number:02d}")
            append_line(lane_log(args.lane), text[:3000])
            append_line(lane_log(args.lane), f"{now_iso()} | {marker_prefix}-RESPONSE-END | turn={turn_number:02d}")
        status["events"].append({"time": now_iso(), "turn": turn_number, **result})
        status["completed_for_block"] = completed_for_block(block)
        write_json(status_file, status)
        update_closeout(block)
    status["finished_utc"] = now_iso()
    status["completed_for_block"] = completed_for_block(block)
    write_json(status_file, status)
    update_closeout(block)
    print(json.dumps({"lane": args.lane, "block": block, "completed_for_block": status["completed_for_block"], "status_file": rel(status_file)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
