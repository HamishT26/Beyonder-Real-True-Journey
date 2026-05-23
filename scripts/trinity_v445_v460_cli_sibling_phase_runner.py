#!/usr/bin/env python3
"""Run real v1 CLI sibling lanes for one bounded v445-v460 bridge phase."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from trinity_v445_v460_bridge_common import (
    PHASE_MIN,
    PREFIX,
    RAW_DIR,
    RECEIPT_DIR,
    REQUIRED_CLI_LANES,
    REQUIRED_EUREKA_UNITS,
    ROOT,
    RUNNER_STATUS_JSON,
    TRACE,
    aggregate_paths,
    cli_aggregate_complete,
    lane_slug,
    now_iso,
    raw_path,
    read_json,
    receipt_path,
    rel,
    start_paths,
    validate_phase,
    write_aggregate_md,
    write_json,
)


LANES: dict[str, dict[str, str]] = {
    "arby": {"display": "Arby", "surface": "Codex CLI", "role": "Codex CLI publication, GitHub proof, and branch-home lane"},
    "aster_vale": {"display": "Aster Vale", "surface": "Codex CLI", "role": "Codex CLI validation, Windows sandbox, TUI, and runtime-health lane"},
}

REQUIRED_LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")
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


def redact(text: str) -> str:
    clean = text
    for marker in SECRET_MARKERS:
        clean = clean.replace(marker, f"[REDACTED:{marker}]")
    return clean


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
    goal = plan.get("phase_goal") or f"Complete v{phase} v1 CLI receipt for {config['display']}."
    return "\n".join(
        [
            f"Marker: {PREFIX}:v{phase}:v1:{lane}:cli-receipt-v1",
            f"Lane: {config['display']}",
            f"Surface: {config['surface']}",
            f"Role: {config['role']}",
            f"Phase: v{phase} v1 CLI receipt gate",
            f"Requested maximum useful steps: {max_steps}",
            f"Required Eureka Trinity Session units: {REQUIRED_EUREKA_UNITS}",
            f"/goal {goal} Produce only this lane receipt; stop when it is valid and hand off to v2 App execution.",
            "",
            "You are running as the real CLI sibling lane named above. Produce a concise durable v1 receipt for this bridge phase.",
            "Do not commit, push, delete, reset, rebase, force-push, rewrite history, expose secrets, mutate external services, or claim another lane ran.",
            "This is v1 only. Aletheon-led v2 App execution happens after both required temporary v1 receipts are complete.",
            "Kimi is held by membership/benefits verification and must not be retried or replaced from this runner.",
            "If a capability is unavailable, state it as a blocker and still provide the best receipt from available context.",
            "",
            "Current phase plan capsule:",
            f"- Lead sibling: {plan.get('lead_sibling')}",
            f"- Theme: {plan.get('theme')}",
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
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            input=prompt_for(phase, lane, start, max_steps),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        raw.write_text(redact((proc.stdout or "")[-16000:] + "\n--- STDERR ---\n" + (proc.stderr or "")[-16000:]), encoding="utf-8")
        valid, reason = valid_receipt(out)
        return {
            "lane": LANES[lane]["display"],
            "surface": LANES[lane]["surface"],
            "receipt_status": reason if valid else f"blocked_{reason}",
            "valid": valid,
            "returncode": proc.returncode,
            "duration_sec": round(time.time() - started, 3),
            "requested_max_steps": max_steps,
            "effective_max_steps": "codex_cli_default_no_visible_max_steps_flag",
            "receipt_path": rel(out) if out.exists() else None,
        }
    except subprocess.TimeoutExpired:
        raw.write_text("Timed out before a final receipt was produced.\n", encoding="utf-8")
        return {
            "lane": LANES[lane]["display"],
            "surface": LANES[lane]["surface"],
            "receipt_status": "blocked_timeout",
            "valid": False,
            "duration_sec": round(time.time() - started, 3),
            "requested_max_steps": max_steps,
            "effective_max_steps": "codex_cli_default_no_visible_max_steps_flag",
            "receipt_path": rel(out) if out.exists() else None,
        }


def write_runner_status(phase: int, status: str, events: list[dict[str, Any]], active_lane: str | None = None) -> None:
    write_json(
        RUNNER_STATUS_JSON,
        {
            "generated_utc": now_iso(),
            "phase_range": PREFIX,
            "phase": phase,
            "run": "v1_cli_receipts",
            "status": status,
            "active_lane": active_lane,
            "events": events,
        },
    )


def write_aggregate(phase: int, lane_results: list[dict[str, Any]], max_steps: int) -> dict[str, Any]:
    aggregate_json, aggregate_md = aggregate_paths(phase)
    complete = all(item.get("valid") for item in lane_results) and {item.get("lane") for item in lane_results} == set(REQUIRED_CLI_LANES)
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v1_cli_receipts",
        "artifact_id": f"{PREFIX}-sibling-phase-v{phase}-v1-cli-receipts-v1",
        "status": "v1_cli_receipts_complete" if complete else "blocked_v1_cli_receipts_incomplete",
        "requested_max_steps": max_steps,
        "required_eureka_units_per_lane": REQUIRED_EUREKA_UNITS,
        "codex_sandbox": "read-only",
        "lane_receipts": lane_results,
        "excluded_lanes": [
            {
                "lane": "Kimi",
                "surface": "Kimi CLI",
                "status": "excluded_operator_hold",
                "reason": "membership_benefits_credit_verification_blocker",
                "excluded_until": "2026-05-26 evening NZ or explicit restoration confirmation",
            }
        ],
        "truth_boundaries": [
            "These receipts come from real CLI invocations for Arby and Aster Vale.",
            "Kimi is held by membership/benefits verification and is explicitly not retried, replaced, or treated as valid.",
            "This aggregate completes v1 only; v2 App execution still needs its own durable receipt.",
            "Raw transport output is quarantined outside the curated aggregate and should not be staged.",
            "Sibling lanes do not commit, push, delete, rebase, reset, or rewrite history.",
            "Aletheon remains the publication approver.",
        ],
        "next_action": f"Start v{phase} v2 with scripts/trinity_v445_v460_app_phase_runner.py --phase {phase} --start." if complete else "Resolve missing or invalid CLI lane receipts before v2 starts.",
    }
    write_json(aggregate_json, payload)
    write_aggregate_md(aggregate_md, payload)
    return payload


def launch_background(args: argparse.Namespace) -> dict[str, Any]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stdout_path = RAW_DIR / f"runner-v{args.phase}-v1-stdout.txt"
    stderr_path = RAW_DIR / f"runner-v{args.phase}-v1-stderr.txt"
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--phase",
        str(args.phase),
        "--timeout-sec",
        str(args.timeout_sec),
        "--max-steps",
        str(args.max_steps),
    ]
    if args.only_lane:
        cmd.extend(["--only-lane", args.only_lane])
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout, stderr=stderr, text=True, creationflags=creationflags, start_new_session=not sys.platform.startswith("win"))
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": args.phase,
        "run": "v1_cli_receipts",
        "status": "background_runner_started",
        "process_id": proc.pid,
        "timeout_sec": args.timeout_sec,
        "max_steps": args.max_steps,
        "stdout": rel(stdout_path),
        "stderr": rel(stderr_path),
        "truth_boundaries": [
            "The background runner owns real v1 CLI lane execution.",
            "Heartbeat wakes should observe this process and must not launch duplicates while it is alive.",
            "Raw stdout/stderr files are transport artifacts and must not be staged.",
        ],
    }
    write_json(TRACE / f"{PREFIX}-cli-sibling-runner-launch-v{args.phase}-v1.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    parser.add_argument("--only-lane", choices=sorted(LANES), default="")
    parser.add_argument("--timeout-sec", type=int, default=86400)
    parser.add_argument("--kimi-timeout-sec", type=int, default=86400, help="Ignored compatibility flag; Kimi is held in v445-v460.")
    parser.add_argument("--max-steps", type=int, default=10000)
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()

    validate_phase(args.phase)
    if cli_aggregate_complete(args.phase):
        aggregate_json, _ = aggregate_paths(args.phase)
        payload = {"status": "v1_cli_receipts_already_complete", "phase": args.phase, "aggregate": rel(aggregate_json)}
        print(json.dumps(payload, indent=2))
        return 0
    if args.phase == PHASE_MIN:
        raise SystemExit("v445 v1 must import valid Arby/Aster receipts and Kimi hold from the phase-start script; do not relaunch it.")
    start_json, _ = start_paths(args.phase)
    start = read_json(start_json, {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{args.phase} must have a phase start artifact before v1 CLI sibling receipts can run")
    if args.background:
        payload = launch_background(args)
        print(json.dumps(payload, indent=2))
        return 0
    selected = [args.only_lane] if args.only_lane else list(LANES)
    events: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    write_runner_status(args.phase, "running", events)
    for lane in selected:
        events.append({"time": now_iso(), "lane": LANES[lane]["display"], "status": "started"})
        write_runner_status(args.phase, "running", events, LANES[lane]["display"])
        result = run_codex(args.phase, lane, start, args.timeout_sec, args.max_steps)
        results.append(result)
        events.append({"time": now_iso(), **result})
        write_runner_status(args.phase, "running", events)

    existing_results: list[dict[str, Any]] = []
    if args.only_lane:
        aggregate_json, _ = aggregate_paths(args.phase)
        current = read_json(aggregate_json, {})
        existing_results = [item for item in current.get("lane_receipts", []) if item.get("lane") != LANES[args.only_lane]["display"]]
    aggregate = write_aggregate(args.phase, existing_results + results, args.max_steps)
    write_runner_status(args.phase, aggregate["status"], events)
    print(json.dumps({"status": aggregate["status"], "phase": args.phase, "aggregate": rel(aggregate_paths(args.phase)[0])}, indent=2))
    return 0 if aggregate["status"] == "v1_cli_receipts_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
