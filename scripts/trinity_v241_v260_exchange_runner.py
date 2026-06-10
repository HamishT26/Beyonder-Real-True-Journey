#!/usr/bin/env python3
"""Run bounded v241-v260 council exchanges.

The runner turns queued council touchpoints into real CLI probes. It is designed
to be boring on purpose: no commits, no provider mutations, no remote-control
tokens, and every response gets its own receipt file.
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
LANE = "v241-v260-multiplex-council"
LEDGER = TRACE / f"{LANE}-150-touchpoint-ledger-v1.json"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
ACTION_PACK = TRACE / f"{LANE}-live-write-action-pack-v1.md"
CLOSEOUT = TRACE / f"{LANE}-closeout-v1.json"
STOP_FILE = TRACE / f"{LANE}.stop"

CODEX_LANES = {"arby", "aster_vale"}
KIMI_LANES = {"kimi"}
LANE_NAMES = {"arby": "Arby", "kimi": "Kimi", "aster_vale": "Aster Vale"}

SECRET_MARKERS = [
    "__cf" + "_chl",
    "cf_" + "clearance=",
    "Authorization: " + "Bearer",
    "BEGIN " + "PRIVATE KEY",
    "api_" + "key",
    "api" + "key",
    "access_" + "token",
    "remote-control " + "token",
]


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
    return LANE_DIR / f"{pretty}-response-{turn:02d}.txt"


def raw_path(lane: str, turn: int) -> Path:
    pretty = "aster-vale" if lane == "aster_vale" else lane
    return LANE_DIR / f"{pretty}-response-{turn:02d}.raw.txt"


def lane_log(lane: str) -> Path:
    return LANE_DIR / f"{lane}.log"


def status_path(status_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in status_id.strip()) or "v1"
    return TRACE / f"{LANE}-exchange-runner-status-{safe}.json"


def prompt_for(turn: dict[str, Any]) -> str:
    marker = turn["expected_response_marker"]
    return "\n".join(
        [
            f"Marker: {marker}",
            f"Lane: {turn['name']}",
            f"Role: {turn['role']}",
            f"Phase: {turn['phase']}",
            f"Topic: {turn['topic']}",
            "",
            "Respond only. Do not edit files. Do not commit. Do not run destructive commands.",
            "Keep the response under 180 words.",
            "Include exactly four labeled lines:",
            "Evidence:",
            "Risk:",
            "Command/skill improvement:",
            "Eureka proposal:",
            "",
            "If you cannot verify a fact in this bounded probe, say what proof is missing instead of guessing.",
        ]
    )


def redact(text: str) -> str:
    redacted = text
    for marker in SECRET_MARKERS:
        redacted = redacted.replace(marker, f"[REDACTED:{marker}]")
    return redacted


def run_codex(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    out = response_path(turn["lane"], int(turn["turn"]))
    raw = raw_path(turn["lane"], int(turn["turn"]))
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
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    raw.write_text(redact((proc.stdout or "")[-12000:] + "\n--- STDERR ---\n" + (proc.stderr or "")[-12000:]), encoding="utf-8")
    return {
        "ok": proc.returncode == 0 and out.exists(),
        "returncode": proc.returncode,
        "duration_sec": round(time.time() - started, 3),
        "response_file": rel(out) if out.exists() else None,
        "raw_file": rel(raw),
    }


def run_kimi(turn: dict[str, Any], timeout: int) -> dict[str, Any]:
    out = response_path(turn["lane"], int(turn["turn"]))
    raw = raw_path(turn["lane"], int(turn["turn"]))
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
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    out.write_text(redact(proc.stdout or ""), encoding="utf-8")
    raw.write_text(redact((proc.stderr or "")[-12000:]), encoding="utf-8")
    return {
        "ok": proc.returncode == 0 and out.exists() and out.stat().st_size > 0,
        "returncode": proc.returncode,
        "duration_sec": round(time.time() - started, 3),
        "response_file": rel(out) if out.exists() else None,
        "raw_file": rel(raw),
    }


def update_closeout(status: dict[str, Any]) -> None:
    closeout = read_json(CLOSEOUT, {})
    completed = int(status.get("completed_response_count", 0))
    total = int(status.get("target_total", 150))
    closeout["touchpoints_completed_as_real_cli_replies"] = completed
    closeout["touchpoints_queued"] = max(total - completed, 0)
    closeout["status"] = "multiplex_council_exchange_runner_active" if completed < total else "multiplex_council_exchange_runner_complete"
    closeout["exchange_runner_status"] = status.get("status_file")
    closeout["stop_file"] = rel(STOP_FILE)
    closeout["truth_boundary"] = "only response files written by the runner count as completed real CLI replies"
    write_json(CLOSEOUT, closeout)


def write_action_pack() -> None:
    ACTION_PACK.write_text(
        "\n".join(
            [
                "# v241-v260 Live Write Action Pack",
                "",
                "Purpose: turn queued council prompts into real CLI responses while remote-control QR remains postponed.",
                "",
                "Required surfaces:",
                "- Codex CLI for Arby and Aster Vale, run with `--sandbox read-only` and plugins disabled.",
                "- Kimi CLI for Kimi, run as a one-step bounded print response because no read-only Kimi flag is exposed in current help.",
                "- Local multiplex TUI: `docs/trinity-live-traces/v241-v260-multiplex-council-multiplex-tui.ps1`.",
                "- Stop file: create `docs/trinity-live-traces/v241-v260-multiplex-council.stop` to halt the runner before the next turn.",
                "",
                "Safety boundaries:",
                "- No commits.",
                "- No provider mutations.",
                "- No remote-control QR tokens stored.",
                "- No dashboard dependency.",
                "- Each response is counted only when its response file exists.",
                "",
                "Run modes:",
                "- Full run: `python scripts/trinity_v241_v260_exchange_runner.py --start-turn 2 --end-turn 50 --lanes arby,kimi,aster_vale`.",
                "- Small batch: `python scripts/trinity_v241_v260_exchange_runner.py --start-turn 2 --end-turn 5 --lanes arby,kimi,aster_vale`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-turn", type=int, default=2)
    parser.add_argument("--end-turn", type=int, default=50)
    parser.add_argument("--lanes", default="arby,kimi,aster_vale")
    parser.add_argument("--timeout-sec", type=int, default=420)
    parser.add_argument("--sleep-sec", type=float, default=2.0)
    parser.add_argument("--status-id", default="v1")
    args = parser.parse_args()

    ledger = read_json(LEDGER, {})
    turns = ledger.get("turns", [])
    requested_lanes = [lane.strip() for lane in args.lanes.split(",") if lane.strip()]
    selected = [
        turn
        for turn in turns
        if turn.get("lane") in requested_lanes and args.start_turn <= int(turn.get("turn", 0)) <= args.end_turn
    ]
    write_action_pack()

    status = {
        "generated_utc": now_iso(),
        "lane": LANE,
        "status_id": args.status_id,
        "status_file": rel(status_path(args.status_id)),
        "start_turn": args.start_turn,
        "end_turn": args.end_turn,
        "lanes": requested_lanes,
        "target_total": 150,
        "selected_count": len(selected),
        "completed_response_count": count_existing_responses(),
        "events": [],
        "stop_file": rel(STOP_FILE),
    }
    status_file = status_path(args.status_id)
    write_json(status_file, status)

    for turn in selected:
        lane = turn["lane"]
        turn_number = int(turn["turn"])
        if STOP_FILE.exists():
            status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, "status": "stopped_by_stop_file"})
            break
        if response_path(lane, turn_number).exists() and response_path(lane, turn_number).stat().st_size > 0:
            status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, "status": "skipped_existing"})
            continue
        append_line(lane_log(lane), f"{now_iso()} | REAL-EXCHANGE-START | turn={turn_number:02d} | marker={turn['expected_response_marker']}")
        try:
            if lane in CODEX_LANES:
                result = run_codex(turn, args.timeout_sec)
            elif lane in KIMI_LANES:
                result = run_kimi(turn, args.timeout_sec)
            else:
                result = {"ok": False, "error": "unknown_lane"}
        except subprocess.TimeoutExpired:
            result = {"ok": False, "timed_out": True}
        except Exception as exc:  # noqa: BLE001 - receipt should capture unexpected runner failures.
            result = {"ok": False, "error": repr(exc)}
        append_line(lane_log(lane), f"{now_iso()} | REAL-EXCHANGE-END | turn={turn_number:02d} | ok={result.get('ok')} | response={result.get('response_file')}")
        if result.get("response_file"):
            text = response_path(lane, turn_number).read_text(encoding="utf-8", errors="replace")
            append_line(lane_log(lane), f"{now_iso()} | REAL-EXCHANGE-RESPONSE-BEGIN | turn={turn_number:02d}")
            append_line(lane_log(lane), text[:2500])
            append_line(lane_log(lane), f"{now_iso()} | REAL-EXCHANGE-RESPONSE-END | turn={turn_number:02d}")
        status["events"].append({"time": now_iso(), "lane": lane, "turn": turn_number, **result})
        status["completed_response_count"] = count_existing_responses()
        write_json(status_file, status)
        update_closeout(status)
        time.sleep(args.sleep_sec)

    status["finished_utc"] = now_iso()
    status["completed_response_count"] = count_existing_responses()
    write_json(status_file, status)
    update_closeout(status)
    print(json.dumps({"completed_response_count": status["completed_response_count"], "status_file": rel(status_file)}, indent=2))
    return 0


def count_existing_responses() -> int:
    count = 0
    for lane in LANE_NAMES:
        for turn in range(1, 51):
            path = response_path(lane, turn)
            if path.exists() and path.stat().st_size > 0:
                count += 1
    return count


if __name__ == "__main__":
    raise SystemExit(main())
