#!/usr/bin/env python3
"""Run real CLI sibling lanes for one bounded v341-v360 phase."""

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
RECEIPT_DIR = TRACE / "v341-v360-cli-sibling-receipts"
RAW_DIR = TRACE / "v341-v360-cli-sibling-raw"
RUNNER_STATUS = TRACE / "v341-v360-cli-sibling-runner-status-v1.json"
PROTOCOL = TRACE / "v281-v360-cli-sibling-report-protocol-v1.md"
PHASE_MIN = 341
PHASE_MAX = 360

LANES: dict[str, dict[str, str]] = {
    "arby": {
        "display": "Arby",
        "surface": "Codex CLI",
        "role": "Codex CLI publication, GitHub proof, and branch-home lane",
    },
    "kimi": {
        "display": "Kimi",
        "surface": "Kimi CLI",
        "role": "Kimi CLI provider, relay, cost, and policy-honest handoff lane",
    },
    "aster_vale": {
        "display": "Aster Vale",
        "surface": "Codex CLI",
        "role": "Codex CLI validation, Windows sandbox, TUI, and runtime-health lane",
    },
}

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


def redact(text: str) -> str:
    markers = (
        "Authorization: Bearer",
        "BEGIN PRIVATE KEY",
        "access_token",
        "api_key",
        "apikey",
        "cf_clearance=",
        "__cf_chl",
        "remote-control token",
    )
    clean = text
    for marker in markers:
        clean = clean.replace(marker, f"[REDACTED:{marker}]")
    return clean


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def phase_start_path(phase: int) -> Path:
    return TRACE / f"v341-v360-sibling-phase-v{phase}-start-v1.json"


def aggregate_paths(phase: int) -> tuple[Path, Path]:
    stem = TRACE / f"v341-v360-sibling-phase-v{phase}-cli-receipts-v1"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def receipt_path(lane: str, phase: int) -> Path:
    return RECEIPT_DIR / f"{lane}-phase-v{phase}-receipt-v1.md"


def raw_path(lane: str, phase: int) -> Path:
    return RAW_DIR / f"{lane}-phase-v{phase}-raw-v1.txt"


def codex_executable() -> str:
    if sys.platform.startswith("win"):
        return shutil.which("codex.cmd") or shutil.which("codex.exe") or shutil.which("codex") or "codex"
    return shutil.which("codex") or "codex"


def cli_path(name: str) -> str | None:
    return shutil.which(name)


def has_required_labels(text: str) -> bool:
    return all(re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text) for label in REQUIRED_LABELS)


def valid_receipt(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_receipt_file"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 160:
        return False, "receipt_too_short"
    if not has_required_labels(text):
        return False, "missing_required_labels"
    invalid = ("Traceback (most recent call last)", "Max number of steps reached", "To resume this session:")
    if any(marker in text for marker in invalid):
        return False, "contains_invalid_transport_marker"
    return True, "valid_cli_receipt"


def prompt_for(phase: int, lane: str, start: dict[str, Any], max_steps: int) -> str:
    config = LANES[lane]
    plan = start.get("phase_plan") or {}
    source = start.get("handoff", {}).get("path") or "docs/trinity-live-traces/v341-v360-final-handoff-v1.json"
    return "\n".join(
        [
            f"Marker: v341-v360:v{phase}:{lane}:cli-receipt-v1",
            f"Lane: {config['display']}",
            f"Surface: {config['surface']}",
            f"Role: {config['role']}",
            f"Phase: v{phase}",
            f"Source dependency: {source}",
            f"Report protocol: {rel(PROTOCOL)}",
            f"Requested maximum useful steps: {max_steps}",
            "",
            "You are running as the real CLI sibling lane named above. Produce a concise, durable receipt for this phase.",
            "Use only safe read-only reasoning and repository inspection if your CLI exposes it without extra approval.",
            "Do not commit, push, delete, reset, rebase, force-push, rewrite history, expose secrets, or mutate external services.",
            "Do not claim that another lane ran. Speak only for your own lane.",
            "If a requested capability is unavailable, state it as a blocker and still provide the best receipt from available context.",
            "",
            "Current phase plan capsule:",
            f"- Lead sibling: {plan.get('lead_sibling')}",
            f"- Beta: {plan.get('beta')}",
            f"- Alpha: {plan.get('alpha')}",
            f"- Omega: {plan.get('omega')}",
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
    cmd = [
        codex_executable(),
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
        "-",
    ]
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
            "receipt_path": rel(out) if out.exists() else None,
        }


def run_kimi(phase: int, lane: str, start: dict[str, Any], timeout: int, max_steps: int) -> dict[str, Any]:
    out = receipt_path(lane, phase)
    raw = raw_path(lane, phase)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "kimi",
        "--work-dir",
        str(ROOT),
        "--print",
        "--final-message-only",
        "--max-steps-per-turn",
        str(max_steps),
        "--prompt",
        prompt_for(phase, lane, start, max_steps),
    ]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout, check=False)
        out.write_text(redact(proc.stdout or ""), encoding="utf-8")
        raw.write_text(redact((proc.stderr or "")[-16000:]), encoding="utf-8")
        valid, reason = valid_receipt(out)
        return {
            "lane": LANES[lane]["display"],
            "surface": LANES[lane]["surface"],
            "receipt_status": reason if valid else f"blocked_{reason}",
            "valid": valid,
            "returncode": proc.returncode,
            "duration_sec": round(time.time() - started, 3),
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
            "receipt_path": rel(out) if out.exists() else None,
        }


def write_status(phase: int, status: str, events: list[dict[str, Any]], active_lane: str | None = None) -> None:
    write_json(
        RUNNER_STATUS,
        {
            "generated_utc": now_iso(),
            "phase_range": "v341-v360",
            "phase": phase,
            "status": status,
            "active_lane": active_lane,
            "events": events,
        },
    )


def write_aggregate(phase: int, lane_results: list[dict[str, Any]], max_steps: int) -> dict[str, Any]:
    aggregate_json, aggregate_md = aggregate_paths(phase)
    complete = all(item.get("valid") for item in lane_results) and {item.get("lane") for item in lane_results} == {
        "Arby",
        "Kimi",
        "Aster Vale",
    }
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v341-v360",
        "phase": phase,
        "artifact_id": f"v341-v360-sibling-phase-v{phase}-cli-receipts-v1",
        "status": "cli_receipts_complete" if complete else "blocked_cli_receipts_incomplete",
        "max_steps_per_kimi_turn": max_steps,
        "codex_sandbox": "read-only",
        "lane_receipts": lane_results,
        "truth_boundaries": [
            "These receipts come from real CLI invocations for Arby, Kimi, and Aster Vale.",
            "Raw transport output is quarantined outside the curated aggregate and should not be staged.",
            "Sibling lanes do not commit, push, delete, rebase, reset, or rewrite history.",
            "Aletheon remains the publication approver.",
        ],
        "next_action": (
            f"Complete v{phase} with scripts/trinity_v341_v360_sibling_phase_complete.py after branch drift and staging checks."
            if complete
            else "Resolve missing or invalid CLI lane receipts before completing the phase."
        ),
    }
    write_json(aggregate_json, payload)
    lines = [
        f"# v{phase} CLI Sibling Receipts",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Lane receipts:",
    ]
    for item in lane_results:
        lines.append(f"- {item.get('lane')}: `{item.get('receipt_status')}` via {item.get('surface')} at `{item.get('receipt_path')}`")
    lines.extend(["", "Truth boundaries:"])
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", f"Next action: {payload['next_action']}"])
    aggregate_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    parser.add_argument("--only-lane", choices=sorted(LANES), default="")
    parser.add_argument("--timeout-sec", type=int, default=3600)
    parser.add_argument("--kimi-timeout-sec", type=int, default=3600)
    parser.add_argument("--max-steps", type=int, default=200)
    args = parser.parse_args()

    validate_phase(args.phase)
    start = read_json(phase_start_path(args.phase), {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{args.phase} must have a phase start artifact before CLI sibling receipts can run")

    if not cli_path("kimi") and not args.only_lane:
        raise SystemExit("kimi CLI is unavailable; cannot produce required Kimi receipt")

    selected = [args.only_lane] if args.only_lane else list(LANES)
    events: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    write_status(args.phase, "running", events)
    for lane in selected:
        events.append({"time": now_iso(), "lane": LANES[lane]["display"], "status": "started"})
        write_status(args.phase, "running", events, LANES[lane]["display"])
        if lane in ("arby", "aster_vale"):
            result = run_codex(args.phase, lane, start, args.timeout_sec, args.max_steps)
        else:
            result = run_kimi(args.phase, lane, start, args.kimi_timeout_sec, args.max_steps)
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
    return 0 if aggregate["status"] == "cli_receipts_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
