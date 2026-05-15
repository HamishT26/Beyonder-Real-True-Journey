#!/usr/bin/env python3
"""Continue v261-v280 adaptive council blocks until a response target is reached."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v261-v280-adaptive-council"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
STOP_FILE = TRACE / f"{LANE}.stop"
CLOSEOUT = TRACE / f"{LANE}-prep-closeout-v1.json"
SUPERVISOR_STATUS = TRACE / f"{LANE}-continuity-supervisor-status-v1.json"
SUPERVISOR_MD = TRACE / f"{LANE}-continuity-supervisor-v1.md"
RUNNER = ROOT / "scripts" / "trinity_v261_v280_adaptive_block_runner.py"
SYNTH = ROOT / "scripts" / "trinity_v261_v280_block_synthesis.py"
V281_PREP = ROOT / "scripts" / "trinity_v281_v300_double_phase_prep.py"
LANES = ("arby", "kimi", "aster_vale")


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


def response_files() -> list[Path]:
    if not LANE_DIR.exists():
        return []
    return [
        path
        for path in LANE_DIR.glob("*-response-*.txt")
        if not path.name.endswith(".raw.txt") and path.stat().st_size > 0
    ]


def total_responses() -> int:
    return len(response_files())


def completed_for_block(block: int) -> int:
    if not LANE_DIR.exists():
        return 0
    return sum(
        1
        for path in LANE_DIR.glob(f"*-block-{block:02d}-response-*.txt")
        if not path.name.endswith(".raw.txt") and path.stat().st_size > 0
    )


def prompt_file_for_block(block: int) -> Path:
    if block == 2:
        return TRACE / f"{LANE}-next-3-message-block-v1.json"
    return TRACE / f"{LANE}-block-{block:02d}-prompts-v1.json"


def run_checked(cmd: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def ensure_prompt(block: int, status: dict[str, Any]) -> Path | None:
    prompt = prompt_file_for_block(block)
    if prompt.exists():
        return prompt
    previous_completed = completed_for_block(block - 1)
    if previous_completed < 9:
        status["events"].append(
            {
                "time": now_iso(),
                "block": block,
                "status": "prompt_missing_previous_incomplete",
                "previous_completed": previous_completed,
            }
        )
        return None
    proc = run_checked([sys.executable, str(SYNTH), "--block", str(block - 1), "--prepare-next"], timeout=600)
    status["events"].append(
        {
            "time": now_iso(),
            "block": block,
            "status": "prompt_generation_attempted",
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    )
    return prompt if prompt.exists() else None


def update_closeout(status: dict[str, Any]) -> None:
    closeout = read_json(CLOSEOUT, {})
    closeout["continuity_supervisor"] = rel(SUPERVISOR_STATUS)
    closeout["continuity_supervisor_markdown"] = rel(SUPERVISOR_MD)
    closeout["continuity_total_clean_responses"] = total_responses()
    closeout["continuity_target_responses"] = status.get("target_responses")
    closeout["continuity_status"] = status.get("status")
    closeout["continuity_latest_block"] = status.get("latest_block")
    closeout["continuity_updated_utc"] = now_iso()
    write_json(CLOSEOUT, closeout)


def write_markdown(status: dict[str, Any]) -> None:
    lines = [
        "# v261-v280 Continuity Supervisor",
        "",
        f"Generated UTC: `{status.get('generated_utc')}`",
        f"Updated UTC: `{status.get('updated_utc')}`",
        f"Status: `{status.get('status')}`",
        f"Target clean responses: `{status.get('target_responses')}`",
        f"Current clean responses: `{status.get('current_responses')}`",
        f"Latest block: `{status.get('latest_block')}`",
        "",
        "Guardrails:",
        "- Run only prepared prompt blocks.",
        "- Synthesize after each 3-message-per-lane block.",
        "- Keep raw transport logs out of publication until separately scanned.",
        "- Respect the stop file if present.",
        "",
        "Recent events:",
    ]
    for event in status.get("events", [])[-12:]:
        lines.append(f"- `{event.get('time')}` block `{event.get('block')}`: {event.get('status')}")
    SUPERVISOR_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def launch_block(block: int, prompt: Path, timeout_sec: int, status: dict[str, Any]) -> None:
    if completed_for_block(block) >= 9:
        status["events"].append({"time": now_iso(), "block": block, "status": "block_already_complete"})
        return
    processes: dict[str, subprocess.Popen[str]] = {}
    for lane in LANES:
        cmd = [
            sys.executable,
            str(RUNNER),
            "--lane",
            lane,
            "--prompt-file",
            rel(prompt),
            "--timeout-sec",
            str(timeout_sec),
            "--status-id",
            "continuity",
        ]
        processes[lane] = subprocess.Popen(
            cmd,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status["events"].append(
            {"time": now_iso(), "block": block, "lane": lane, "status": "lane_started", "pid": processes[lane].pid}
        )
    write_json(SUPERVISOR_STATUS, status)
    update_closeout(status)
    write_markdown(status)

    deadline = time.time() + timeout_sec
    for lane, proc in processes.items():
        remaining = max(1, int(deadline - time.time()))
        try:
            stdout, stderr = proc.communicate(timeout=remaining)
            status["events"].append(
                {
                    "time": now_iso(),
                    "block": block,
                    "lane": lane,
                    "status": "lane_finished",
                    "returncode": proc.returncode,
                    "stdout_tail": (stdout or "")[-1000:],
                    "stderr_tail": (stderr or "")[-1000:],
                }
            )
        except subprocess.TimeoutExpired:
            proc.terminate()
            status["events"].append({"time": now_iso(), "block": block, "lane": lane, "status": "lane_timeout"})
    status["current_responses"] = total_responses()
    status[f"block_{block:02d}_completed"] = completed_for_block(block)


def synthesize_block(block: int, status: dict[str, Any]) -> None:
    if completed_for_block(block) < 9:
        status["events"].append(
            {"time": now_iso(), "block": block, "status": "synthesis_skipped_incomplete", "completed": completed_for_block(block)}
        )
        return
    proc = run_checked([sys.executable, str(SYNTH), "--block", str(block), "--prepare-next"], timeout=600)
    status["events"].append(
        {
            "time": now_iso(),
            "block": block,
            "status": "synthesis_finished",
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    )


def prepare_v281(status: dict[str, Any]) -> None:
    if not V281_PREP.exists():
        status["events"].append({"time": now_iso(), "block": status.get("latest_block"), "status": "v281_prep_script_missing"})
        return
    proc = run_checked([sys.executable, str(V281_PREP), "--source-phase", "v261-v280", "--phase", "281"], timeout=600)
    status["events"].append(
        {
            "time": now_iso(),
            "block": status.get("latest_block"),
            "status": "v281_prep_finished",
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-block", type=int, default=4)
    parser.add_argument("--target-responses", type=int, default=120)
    parser.add_argument("--timeout-sec", type=int, default=43200)
    parser.add_argument("--sleep-between-blocks-sec", type=int, default=5)
    parser.add_argument("--prepare-v281-on-complete", action="store_true")
    args = parser.parse_args()

    status = read_json(
        SUPERVISOR_STATUS,
        {
            "generated_utc": now_iso(),
            "phase_range": "v261-v280",
            "status_file": rel(SUPERVISOR_STATUS),
            "events": [],
        },
    )
    status.update(
        {
            "updated_utc": now_iso(),
            "status": "running",
            "target_responses": args.target_responses,
            "start_block": args.start_block,
            "timeout_sec": args.timeout_sec,
            "stop_file": rel(STOP_FILE),
            "current_responses": total_responses(),
        }
    )
    write_json(SUPERVISOR_STATUS, status)
    update_closeout(status)
    write_markdown(status)

    block = args.start_block
    while total_responses() < args.target_responses:
        if STOP_FILE.exists():
            status["status"] = "stopped_by_stop_file"
            status["events"].append({"time": now_iso(), "block": block, "status": "stop_file_detected"})
            break
        status["latest_block"] = block
        prompt = ensure_prompt(block, status)
        if not prompt:
            status["status"] = "blocked_missing_prompt"
            break
        launch_block(block, prompt, args.timeout_sec, status)
        synthesize_block(block, status)
        status["current_responses"] = total_responses()
        status["updated_utc"] = now_iso()
        write_json(SUPERVISOR_STATUS, status)
        update_closeout(status)
        write_markdown(status)
        if completed_for_block(block) < 9:
            status["status"] = "blocked_incomplete_block"
            break
        block += 1
        time.sleep(max(0, args.sleep_between_blocks_sec))

    if total_responses() >= args.target_responses:
        status["status"] = "target_reached"
        status["current_responses"] = total_responses()
        status["updated_utc"] = now_iso()
        if args.prepare_v281_on_complete:
            prepare_v281(status)
    status["current_responses"] = total_responses()
    status["updated_utc"] = now_iso()
    write_json(SUPERVISOR_STATUS, status)
    update_closeout(status)
    write_markdown(status)
    print(json.dumps({"status": status["status"], "current_responses": status["current_responses"]}, indent=2))
    return 0 if status["status"] in {"target_reached", "running"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
