#!/usr/bin/env python3
"""Run real v1 CLI sibling lanes for one bounded v421-v440 phase."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
RECEIPT_DIR = TRACE / "v421-v440-cli-sibling-receipts"
RAW_DIR = TRACE / "v421-v440-cli-sibling-raw"
RUNNER_STATUS = TRACE / "v421-v440-cli-sibling-runner-status-v1.json"
PROTOCOL = TRACE / "v281-v360-cli-sibling-report-protocol-v1.md"
PHASE_MIN = 421
PHASE_MAX = 440
CODEX_SESSION_MODE = "recorded_for_resume"

LANES: dict[str, dict[str, str]] = {
    "arby": {"display": "Arby", "surface": "Codex CLI", "role": "Codex CLI publication, GitHub proof, and branch-home lane"},
    "kimi": {"display": "Kimi", "surface": "Kimi CLI", "role": "Kimi CLI provider, relay, cost, and policy-honest handoff lane"},
    "aster_vale": {"display": "Aster Vale", "surface": "Codex CLI", "role": "Codex CLI validation, Windows sandbox, TUI, and runtime-health lane"},
}
REQUIRED_LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")
REQUIRED_EUREKA_UNITS = 50
SECRET_MARKERS = (
    "Authorization:" + " Bearer",
    "BEGIN " + "PRIVATE KEY",
    "access" + "_token",
    "api" + "_key",
    "api" + "key",
    "cf_" + "clearance=",
    "__cf" + "_chl",
    "remote-control " + "token",
)


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


def redact(text: str) -> str:
    clean = text
    for marker in SECRET_MARKERS:
        clean = clean.replace(marker, f"[REDACTED:{marker}]")
    return clean


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def phase_start_path(phase: int) -> Path:
    return TRACE / f"v421-v440-sibling-phase-v{phase}-start-v1.json"


def aggregate_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"v421-v440-sibling-phase-v{phase}-v1-cli-receipts-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def receipt_path(lane: str, phase: int) -> Path:
    return RECEIPT_DIR / f"{lane}-phase-v{phase}-v1-receipt-v1.md"


def raw_path(lane: str, phase: int) -> Path:
    return RAW_DIR / f"{lane}-phase-v{phase}-v1-raw-v1.txt"


def codex_executable() -> str:
    if sys.platform.startswith("win"):
        return shutil.which("codex.cmd") or shutil.which("codex.exe") or shutil.which("codex") or "codex"
    return shutil.which("codex") or "codex"


def cli_path(name: str) -> str | None:
    return shutil.which(name)


def has_required_labels(text: str) -> bool:
    return all(re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text) for label in REQUIRED_LABELS)


def eureka_unit_count(text: str) -> int:
    matches = re.findall(r"(?im)^\s*(?:[-*]\s*)?\**Eureka(?:\s+Trinity)?\s+Session\s+\d{1,3}\b", text)
    if matches:
        return len(matches)
    return len(re.findall(r"(?im)^\s*(?:[-*]\s*)?\**Eureka\s+\d{1,3}\b", text))


def valid_receipt(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_receipt_file"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 160:
        return False, "receipt_too_short"
    if not has_required_labels(text):
        return False, "missing_required_labels"
    count = eureka_unit_count(text)
    if count < REQUIRED_EUREKA_UNITS:
        return False, f"missing_eureka_units_{count}_of_{REQUIRED_EUREKA_UNITS}"
    invalid = ("Traceback (most recent call last)", "Max number of steps reached", "To resume this session:")
    if any(marker in text for marker in invalid):
        return False, "contains_invalid_transport_marker"
    return True, "valid_cli_receipt"


def prompt_for(phase: int, lane: str, start: dict[str, Any], max_steps: int) -> str:
    config = LANES[lane]
    plan = start.get("phase_plan") or {}
    goal = (plan.get("goal_mode") or {}).get("phase_goal") or f"Complete v{phase} v1 CLI receipt for {config['display']}."
    return "\n".join(
        [
            f"Marker: v421-v440:v{phase}:v1:{lane}:cli-receipt-v1",
            f"Lane: {config['display']}",
            f"Surface: {config['surface']}",
            f"Role: {config['role']}",
            f"Phase: v{phase} v1 CLI receipt gate",
            f"Report protocol: {rel(PROTOCOL)}",
            f"Requested maximum useful steps: {max_steps}",
            f"Required Eureka Trinity Session units: {REQUIRED_EUREKA_UNITS}",
            f"/goal {goal} Produce only this lane receipt; stop when it is valid and hand off to v2 App execution.",
            "",
            "You are running as the real CLI sibling lane named above. Produce a concise durable v1 receipt for this phase.",
            "Do not commit, push, delete, reset, rebase, force-push, rewrite history, expose secrets, mutate external services, or claim another lane ran.",
            "This is v1 only. Aletheon-led v2 App execution happens after all three v1 receipts are complete.",
            "If a capability is unavailable, state it as a blocker and still provide the best receipt from available context.",
            "",
            "Current phase plan capsule:",
            f"- Lead sibling: {plan.get('lead_sibling')}",
            f"- Beta: {plan.get('beta')}",
            f"- Alpha: {plan.get('alpha')}",
            f"- Omega: {plan.get('omega')}",
            "",
            "Include exactly this structured section before Blocker:",
            "Eureka Sessions:",
            "For each number 01 through 50, write one compact line beginning with `Eureka Session NN:` and covering Beta insight, Alpha action, and Omega validation/handoff.",
            "",
            "Respond with these labels exactly, each with concrete non-empty content:",
            "Receipt:",
            "Beta:",
            "Alpha:",
            "Omega:",
            "Blocker:",
            "Next-phase handoff:",
        ]
    )


def run_codex(phase: int, lane: str, start: dict[str, Any], timeout: int, max_steps: int) -> dict[str, Any]:
    out = receipt_path(lane, phase)
    raw = raw_path(lane, phase)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw.parent.mkdir(parents=True, exist_ok=True)
    cmd = [codex_executable(), "exec", "--disable", "plugins", "--sandbox", "read-only", "-C", str(ROOT), "-o", str(out), "-"]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, input=prompt_for(phase, lane, start, max_steps), text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
        raw.write_text(redact((proc.stdout or "")[-16000:] + "\n--- STDERR ---\n" + (proc.stderr or "")[-16000:]), encoding="utf-8")
        valid, reason = valid_receipt(out)
        return {"lane": LANES[lane]["display"], "surface": LANES[lane]["surface"], "receipt_status": reason if valid else f"blocked_{reason}", "valid": valid, "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "requested_max_steps": max_steps, "effective_max_steps": "codex_cli_default_no_visible_max_steps_flag", "receipt_path": rel(out) if out.exists() else None}
    except subprocess.TimeoutExpired:
        raw.write_text("Timed out before a final receipt was produced.\n", encoding="utf-8")
        return {"lane": LANES[lane]["display"], "surface": LANES[lane]["surface"], "receipt_status": "blocked_timeout", "valid": False, "duration_sec": round(time.time() - started, 3), "requested_max_steps": max_steps, "effective_max_steps": "codex_cli_default_no_visible_max_steps_flag", "receipt_path": rel(out) if out.exists() else None}


def kimi_command(max_steps: int, prompt: str) -> list[str]:
    return ["kimi", "--work-dir", str(ROOT), "--print", "--final-message-only", "--max-steps-per-turn", str(max_steps), "--prompt", prompt]


def should_retry_kimi(stderr: str, max_steps: int) -> bool:
    lowered = stderr.lower()
    return max_steps > 200 and ("max" in lowered or "step" in lowered or "invalid" in lowered)


def run_kimi_once(phase: int, lane: str, start: dict[str, Any], timeout: int, max_steps: int) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.time()
    proc = subprocess.run(kimi_command(max_steps, prompt_for(phase, lane, start, max_steps)), cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
    return proc, time.time() - started


def run_kimi(phase: int, lane: str, start: dict[str, Any], timeout: int, max_steps: int) -> dict[str, Any]:
    out = receipt_path(lane, phase)
    raw = raw_path(lane, phase)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    used_steps = max_steps
    downgrade_note = None
    try:
        proc, _ = run_kimi_once(phase, lane, start, timeout, max_steps)
        if proc.returncode != 0 and should_retry_kimi(proc.stderr or "", max_steps):
            downgrade_note = "kimi_retried_with_2000_after_rejecting_10000"
            used_steps = 2000
            proc, _ = run_kimi_once(phase, lane, start, timeout, used_steps)
        out.write_text(redact(proc.stdout or ""), encoding="utf-8")
        raw.write_text(redact((proc.stderr or "")[-16000:]), encoding="utf-8")
        valid, reason = valid_receipt(out)
        return {"lane": LANES[lane]["display"], "surface": LANES[lane]["surface"], "receipt_status": reason if valid else f"blocked_{reason}", "valid": valid, "returncode": proc.returncode, "duration_sec": round(time.time() - started, 3), "requested_max_steps": max_steps, "effective_max_steps": used_steps, "downgrade_note": downgrade_note, "receipt_path": rel(out) if out.exists() else None}
    except subprocess.TimeoutExpired:
        raw.write_text("Timed out before a final receipt was produced.\n", encoding="utf-8")
        return {"lane": LANES[lane]["display"], "surface": LANES[lane]["surface"], "receipt_status": "blocked_timeout", "valid": False, "duration_sec": round(time.time() - started, 3), "requested_max_steps": max_steps, "effective_max_steps": used_steps, "downgrade_note": downgrade_note, "receipt_path": rel(out) if out.exists() else None}


def write_status(phase: int, status: str, events: list[dict[str, Any]], active_lane: str | None = None) -> None:
    write_json(RUNNER_STATUS, {"generated_utc": now_iso(), "phase_range": "v421-v440", "phase": phase, "run": "v1_cli_receipts", "status": status, "active_lane": active_lane, "events": events})


def write_aggregate(phase: int, lane_results: list[dict[str, Any]], max_steps: int) -> dict[str, Any]:
    aggregate_json, aggregate_md = aggregate_paths(phase)
    complete = all(item.get("valid") for item in lane_results) and {item.get("lane") for item in lane_results} == {"Arby", "Kimi", "Aster Vale"}
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v421-v440",
        "phase": phase,
        "run": "v1_cli_receipts",
        "artifact_id": f"v421-v440-sibling-phase-v{phase}-v1-cli-receipts-v1",
        "status": "v1_cli_receipts_complete" if complete else "blocked_v1_cli_receipts_incomplete",
        "requested_max_steps": max_steps,
        "required_eureka_units_per_lane": REQUIRED_EUREKA_UNITS,
        "codex_sandbox": "read-only",
        "codex_session_mode": CODEX_SESSION_MODE,
        "lane_receipts": lane_results,
        "truth_boundaries": [
            "These receipts come from real CLI invocations for Arby, Kimi, and Aster Vale.",
            "This aggregate completes v1 only; v2 App execution still needs its own durable receipt.",
            "Raw transport output is quarantined outside the curated aggregate and should not be staged.",
            "Sibling lanes do not commit, push, delete, rebase, reset, or rewrite history.",
            "Aletheon remains the publication approver.",
        ],
        "next_action": f"Start v{phase} v2 with scripts/trinity_v421_v440_app_phase_runner.py --phase {phase} --start." if complete else "Resolve missing or invalid CLI lane receipts before v2 starts.",
    }
    write_json(aggregate_json, payload)
    lines = [f"# v{phase} v1 CLI Sibling Receipts", "", f"Generated UTC: `{payload['generated_utc']}`", f"Status: `{payload['status']}`", "", "Lane receipts:"]
    for item in lane_results:
        suffix = f"; downgrade={item.get('downgrade_note')}" if item.get("downgrade_note") else ""
        lines.append(f"- {item.get('lane')}: `{item.get('receipt_status')}` via {item.get('surface')} at `{item.get('receipt_path')}` requested_steps `{item.get('requested_max_steps')}` effective_steps `{item.get('effective_max_steps')}`{suffix}")
    lines.extend(["", "Truth boundaries:", *[f"- {item}" for item in payload["truth_boundaries"]], "", f"Next action: {payload['next_action']}"])
    aggregate_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def launch_background(args: argparse.Namespace) -> dict[str, Any]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stdout_path = RAW_DIR / f"runner-v{args.phase}-v1-stdout.txt"
    stderr_path = RAW_DIR / f"runner-v{args.phase}-v1-stderr.txt"
    cmd = [sys.executable, str(Path(__file__).resolve()), "--phase", str(args.phase), "--timeout-sec", str(args.timeout_sec), "--kimi-timeout-sec", str(args.kimi_timeout_sec), "--max-steps", str(args.max_steps)]
    if args.only_lane:
        cmd.extend(["--only-lane", args.only_lane])
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout, stderr=stderr, text=True, creationflags=creationflags, start_new_session=not sys.platform.startswith("win"))
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v421-v440",
        "phase": args.phase,
        "run": "v1_cli_receipts",
        "status": "background_runner_started",
        "process_id": proc.pid,
        "timeout_sec": args.timeout_sec,
        "kimi_timeout_sec": args.kimi_timeout_sec,
        "max_steps": args.max_steps,
        "stdout": rel(stdout_path),
        "stderr": rel(stderr_path),
        "truth_boundaries": [
            "The background runner owns real v1 CLI lane execution.",
            "Heartbeat wakes should observe this process and must not launch duplicates while it is alive.",
            "Raw stdout/stderr files are transport artifacts and must not be staged.",
        ],
    }
    write_json(TRACE / f"v421-v440-cli-sibling-runner-launch-v{args.phase}-v1.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    parser.add_argument("--only-lane", choices=sorted(LANES), default="")
    parser.add_argument("--timeout-sec", type=int, default=86400)
    parser.add_argument("--kimi-timeout-sec", type=int, default=86400)
    parser.add_argument("--max-steps", type=int, default=10000)
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()

    validate_phase(args.phase)
    start = read_json(phase_start_path(args.phase), {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{args.phase} must have a phase start artifact before v1 CLI sibling receipts can run")
    if args.background:
        payload = launch_background(args)
        print(json.dumps(payload, indent=2))
        return 0
    if not cli_path("kimi") and not args.only_lane:
        raise SystemExit("kimi CLI is unavailable; cannot produce required Kimi receipt")

    selected = [args.only_lane] if args.only_lane else list(LANES)
    events: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    write_status(args.phase, "running", events)
    for lane in selected:
        events.append({"time": now_iso(), "lane": LANES[lane]["display"], "status": "started"})
        write_status(args.phase, "running", events, LANES[lane]["display"])
        result = run_codex(args.phase, lane, start, args.timeout_sec, args.max_steps) if lane in ("arby", "aster_vale") else run_kimi(args.phase, lane, start, args.kimi_timeout_sec, args.max_steps)
        results.append(result)
        events.append({"time": now_iso(), **result})
        write_status(args.phase, "running", events)

    existing_results: list[dict[str, Any]] = []
    if args.only_lane:
        aggregate_json, _ = aggregate_paths(args.phase)
        current = read_json(aggregate_json, {})
        existing_results = [item for item in current.get("lane_receipts", []) if item.get("lane") != LANES[args.only_lane]["display"]]
    aggregate = write_aggregate(args.phase, existing_results + results, args.max_steps)
    write_status(args.phase, aggregate["status"], events)
    print(json.dumps({"status": aggregate["status"], "phase": args.phase, "aggregate": rel(aggregate_paths(args.phase)[0])}, indent=2))
    return 0 if aggregate["status"] == "v1_cli_receipts_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
