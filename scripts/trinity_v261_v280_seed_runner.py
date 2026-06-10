#!/usr/bin/env python3
"""Run the v261-v280 adaptive seed cycle.

Cycle 1 sends five bounded prompts to each lane. Later cycles should be
generated from the actual responses in three-cycle planning blocks.
"""

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
SEED = TRACE / f"{LANE}-seed-prompts-v1.json"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
STATUS_DIR = TRACE
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


def response_path(lane: str, turn: int) -> Path:
    pretty = "aster-vale" if lane == "aster_vale" else lane
    return LANE_DIR / f"{pretty}-cycle-01-response-{turn:02d}.txt"


def raw_path(lane: str, turn: int) -> Path:
    pretty = "aster-vale" if lane == "aster_vale" else lane
    return LANE_DIR / f"{pretty}-cycle-01-response-{turn:02d}.raw.txt"


def lane_log(lane: str) -> Path:
    return LANE_DIR / f"{lane}.log"


def status_path(status_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in status_id) or "v1"
    return STATUS_DIR / f"{LANE}-seed-runner-status-{safe}.json"


def prompt_for(turn: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Marker: {turn['marker']}",
            f"Lane: {turn['name']}",
            f"Role: {turn['role']}",
            f"Topic: {turn['topic']}",
            "",
            "Respond only. Do not edit files. Do not commit. Do not run destructive commands.",
            "Keep the response under 260 words.",
            "Include these labels:",
            "Receipt:",
            "Blocker:",
            "Refinement:",
            "Next-cycle proposal:",
            "",
            "Use the v241-v260 results as context, but do not claim unverified web or provider access.",
        ]
    )


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


def run_codex(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    turn_number = int(turn["turn"])
    out = response_path(turn["lane"], turn_number)
    raw = raw_path(turn["lane"], turn_number)
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
    return {"ok": proc.returncode == 0 and out.exists(), "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "response_file": rel(out) if out.exists() else None}


def run_kimi(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    turn_number = int(turn["turn"])
    out = response_path(turn["lane"], turn_number)
    raw = raw_path(turn["lane"], turn_number)
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


def count_responses() -> int:
    if not LANE_DIR.exists():
        return 0
    return sum(1 for path in LANE_DIR.glob("*cycle-01-response-*.txt") if not path.name.endswith(".raw.txt") and path.stat().st_size > 0)


def update_closeout(status: dict[str, Any]) -> None:
    closeout = read_json(CLOSEOUT, {})
    closeout["status"] = "seed_running" if count_responses() < 15 else "seed_complete"
    closeout["seed_completed_responses"] = count_responses()
    closeout["seed_runner_status"] = status.get("status_file")
    closeout["multiplex_refresh_seconds"] = 180
    closeout["planning_block_after_seed"] = "three 5-prompt-per-lane cycles at a time"
    write_json(CLOSEOUT, closeout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True)
    parser.add_argument("--timeout-sec", type=int, default=7200)
    parser.add_argument("--status-id", default="v1")
    args = parser.parse_args()

    seed = read_json(SEED, {})
    turns = [turn for turn in seed.get("prompts", []) if turn.get("lane") == args.lane]
    status_file = status_path(args.status_id)
    status = {
        "generated_utc": now_iso(),
        "phase_range": "v261-v280",
        "lane": args.lane,
        "status_id": args.status_id,
        "status_file": rel(status_file),
        "selected_count": len(turns),
        "events": [],
        "stop_file": rel(STOP_FILE),
    }
    write_json(status_file, status)
    for turn in turns:
        turn_number = int(turn["turn"])
        if STOP_FILE.exists():
            status["events"].append({"time": now_iso(), "turn": turn_number, "status": "stopped_by_stop_file"})
            break
        if response_path(args.lane, turn_number).exists() and response_path(args.lane, turn_number).stat().st_size > 0:
            status["events"].append({"time": now_iso(), "turn": turn_number, "status": "skipped_existing"})
            continue
        append_line(lane_log(args.lane), f"{now_iso()} | V261-SEED-START | turn={turn_number:02d} | marker={turn['marker']}")
        try:
            if args.lane in CODEX_LANES:
                result = run_codex(turn, args.timeout_sec)
            elif args.lane in KIMI_LANES:
                result = run_kimi(turn, args.timeout_sec)
            else:
                result = {"ok": False, "error": "unknown_lane"}
        except subprocess.TimeoutExpired:
            result = {"ok": False, "timed_out": True}
        append_line(lane_log(args.lane), f"{now_iso()} | V261-SEED-END | turn={turn_number:02d} | ok={result.get('ok')} | response={result.get('response_file')}")
        if result.get("response_file"):
            text = response_path(args.lane, turn_number).read_text(encoding="utf-8", errors="replace")
            append_line(lane_log(args.lane), f"{now_iso()} | V261-SEED-RESPONSE-BEGIN | turn={turn_number:02d}")
            append_line(lane_log(args.lane), text[:2600])
            append_line(lane_log(args.lane), f"{now_iso()} | V261-SEED-RESPONSE-END | turn={turn_number:02d}")
        status["events"].append({"time": now_iso(), "turn": turn_number, **result})
        status["completed_total"] = count_responses()
        write_json(status_file, status)
        update_closeout(status)
    status["finished_utc"] = now_iso()
    status["completed_total"] = count_responses()
    write_json(status_file, status)
    update_closeout(status)
    print(json.dumps({"lane": args.lane, "completed_total": status["completed_total"], "status_file": rel(status_file)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
