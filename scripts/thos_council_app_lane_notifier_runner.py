#!/usr/bin/env python3
"""Run a bounded council app-lane notifier through the local Codex app server."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
WATCH_LAUNCHER = ROOT / "scripts" / "thos_app_lane_watch_launcher.py"
DEFAULT_LANES = "Cicero,Kierkegaard,Aristotle"
REMOTE_REF = "origin/codex/GHC-Family/beyonder-shared-omega-line"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def git_text(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def read_json_if_present(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False}


def lane_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in payload.get("lanes", []):
        if not isinstance(lane, dict):
            continue
        rows.append(
            {
                "lane": lane.get("lane"),
                "overall_status": lane.get("overall_status"),
                "duration_seconds": lane.get("duration_seconds"),
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_status": lane.get("turn_start", {}).get("status", "not_started"),
                "completion_status": lane.get("turn_completion", {}).get("status", "not_waited"),
            }
        )
    return rows


def gate_status_for_rows(rows: list[dict[str, Any]], expected_lanes: list[str]) -> tuple[str, list[str]]:
    lane_by_name = {str(row.get("lane")): row for row in rows}
    gaps: list[str] = []
    for lane in expected_lanes:
        row = lane_by_name.get(lane)
        if row is None:
            gaps.append(f"{lane}:missing")
            continue
        if row.get("overall_status") != "completed" or row.get("completion_status") != "completed":
            gaps.append(f"{lane}:{row.get('overall_status')}/{row.get('completion_status')}")
    return ("PASS_APP_LANE_COMPLETION_GATE", gaps) if not gaps else ("OPEN_GAP_APP_LANE_COMPLETION_REQUIRED", gaps)


def build_gate_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    mode = "notify" if args.notify else "probe"
    runner_prefix = args.runner_prefix or f"{args.phase_slug}-council-app-lane-notifier-runner-{mode}"
    artifact_prefix = args.artifact_prefix or f"{args.phase_slug}-council-app-lane-completion-notifier-{mode}"
    launcher_prefix = args.launcher_prefix or f"{args.phase_slug}-council-app-lane-watch-launcher-{mode}"
    gate_prefix = args.gate_prefix or f"{args.phase_slug}-council-app-lane-completion-gate-{mode}"
    expected_lanes = [part.strip() for part in args.lanes.split(",") if part.strip()]
    runner = read_json_if_present(TRACE_DIR / f"{runner_prefix}-v1.json")
    notifier = read_json_if_present(TRACE_DIR / f"{artifact_prefix}-v1.json")
    launcher = read_json_if_present(TRACE_DIR / f"{launcher_prefix}-v1.json")
    rows = lane_rows(notifier)
    lane_status, gaps = gate_status_for_rows(rows, expected_lanes)
    runner_status = str(runner.get("overall_status", "missing"))
    notifier_status = str(notifier.get("overall_status", "missing"))
    launcher_status = str(launcher.get("overall_status", "missing"))
    receipt_status = lane_status
    receipt_gaps = list(gaps)
    if not runner_status.startswith("PASS"):
        receipt_status = "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED"
        receipt_gaps.append(f"runner:{runner_status}")
    if not notifier_status.startswith("PASS"):
        receipt_status = "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED"
        receipt_gaps.append(f"notifier:{notifier_status}")
    if launcher_status != "missing" and not launcher_status.startswith("PASS"):
        receipt_status = "OPEN_GAP_APP_LANE_COMPLETION_REQUIRED"
        receipt_gaps.append(f"launcher:{launcher_status}")
    payload: dict[str, Any] = {
        "artifact_type": "council_app_lane_completion_gate",
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "phase_slug": args.phase_slug,
        "mode": mode,
        "overall_status": receipt_status,
        "local_head_at_gate": git_text(["rev-parse", "HEAD"]),
        "remote_head_at_gate": git_text(["rev-parse", REMOTE_REF]),
        "drift_at_gate": git_text(["rev-list", "--left-right", "--count", f"HEAD...{REMOTE_REF}"]),
        "expected_lanes": expected_lanes,
        "gate_inputs": {
            "runner_receipt": f"{runner_prefix}-v1.json",
            "runner_status": runner_status,
            "watch_launcher_receipt": f"{launcher_prefix}-v1.json",
            "watch_launcher_status": launcher_status,
            "completion_notifier_receipt": f"{artifact_prefix}-v1.json",
            "completion_notifier_status": notifier_status,
        },
        "lanes": rows,
        "open_gaps": sorted(set(receipt_gaps)),
        "phase_advance_rule": {
            "all_app_lanes_required": True,
            "all_cli_lanes_required": True,
            "duration_is_completion_proof": False,
            "next_phase_allowed": receipt_status.startswith("PASS"),
        },
        "publication_boundary": {
            "advisory_body_published": False,
            "auth_material_published": False,
            "image_captures_published": False,
            "local_absolute_paths_published": False,
            "raw_transport_published": False,
        },
        "claim_boundary": {
            "scope": "THOS app-lane completion gating only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(TRACE_DIR / f"{gate_prefix}-v1.json", payload)
    write_gate_md(TRACE_DIR / f"{gate_prefix}-v1.md", payload)
    return payload


def run_watch_launcher(args: argparse.Namespace, artifact_prefix: str, launcher_prefix: str) -> dict[str, Any]:
    command = [
        sys.executable,
        str(WATCH_LAUNCHER),
        "--phase-slug",
        args.phase_slug,
        "--artifact-prefix",
        artifact_prefix,
        "--launcher-prefix",
        launcher_prefix,
        "--lanes",
        args.lanes,
        "--retries",
        str(args.retries),
        "--call-timeout-seconds",
        str(args.call_timeout_seconds),
        "--turn-timeout-seconds",
        str(args.turn_timeout_seconds),
        "--launch-timeout-seconds",
        str(args.launch_timeout_seconds),
    ]
    if args.allow_turn_start_after_resume_timeout:
        command.append("--allow-turn-start-after-resume-timeout")
    if args.notify:
        command.append("--notify")
    if args.execute:
        command.append("--execute")
    if not args.execute:
        return {"execution_status": "planned_only", "returncode": None}
    if args.background_watch:
        creationflags = 0
        if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
            creationflags |= subprocess.CREATE_NEW_PROCESS_GROUP
        if hasattr(subprocess, "DETACHED_PROCESS"):
            creationflags |= subprocess.DETACHED_PROCESS
        try:
            proc = subprocess.Popen(
                command,
                cwd=ROOT,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags,
            )
        except OSError as exc:
            return {
                "execution_status": "background_start_failed",
                "returncode": None,
                "error_class": exc.__class__.__name__,
            }
        return {
            "execution_status": "background_watch_started",
            "returncode": None,
            "pid": proc.pid,
            "stdout_boundary": "discarded_not_published",
            "stderr_boundary": "discarded_not_published",
            "watcher_expected_receipts": [
                f"{artifact_prefix}-v1.json",
                f"{artifact_prefix}-v1.md",
                f"{launcher_prefix}-v1.json",
                f"{launcher_prefix}-v1.md",
            ],
        }
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.launch_timeout_seconds + 30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "execution_status": "timeout",
            "returncode": None,
            "stdout_bytes": len(exc.stdout or "") if isinstance(exc.stdout, str) else 0,
            "stderr_bytes": len(exc.stderr or "") if isinstance(exc.stderr, str) else 0,
            "stderr_nonempty": bool(exc.stderr),
        }
    stdout_status = "unparsed"
    for line in reversed([row.strip() for row in proc.stdout.splitlines() if row.strip()]):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            stdout_status = str(parsed.get("status", "unknown"))
            break
    return {
        "execution_status": "completed",
        "returncode": proc.returncode,
        "stdout_status": stdout_status,
        "stdout_bytes": len(proc.stdout.encode("utf-8", errors="replace")),
        "stderr_bytes": len(proc.stderr.encode("utf-8", errors="replace")),
        "stderr_nonempty": bool(proc.stderr.strip()),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    mode = "notify" if args.notify else "probe"
    runner_prefix = args.runner_prefix or f"{args.phase_slug}-council-app-lane-notifier-runner-{mode}"
    artifact_prefix = args.artifact_prefix or f"{args.phase_slug}-council-app-lane-completion-notifier-{mode}"
    launcher_prefix = args.launcher_prefix or f"{args.phase_slug}-council-app-lane-watch-launcher-{mode}"
    execution = run_watch_launcher(args, artifact_prefix, launcher_prefix)
    notifier = read_json_if_present(TRACE_DIR / f"{artifact_prefix}-v1.json")
    launcher = read_json_if_present(TRACE_DIR / f"{launcher_prefix}-v1.json")
    notifier_status = str(notifier.get("overall_status", "missing"))
    launcher_status = str(launcher.get("overall_status", "missing"))
    execution_ok = execution.get("returncode") == 0 or not args.execute
    status_ok = notifier_status.startswith("PASS") and launcher_status.startswith("PASS")
    background_started = execution.get("execution_status") == "background_watch_started"
    background_failed = execution.get("execution_status") == "background_start_failed"
    if background_started:
        overall_status = "PASS_BACKGROUND_WATCH_STARTED"
    elif background_failed:
        overall_status = "OPEN_GAP_BACKGROUND_WATCH_START"
    else:
        overall_status = "PASS" if execution_ok and status_ok else "OPEN_GAP_COUNCIL_APP_LANE"
    payload: dict[str, Any] = {
        "artifact_type": "council_app_lane_notifier_runner",
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "phase_slug": args.phase_slug,
        "mode": mode,
        "overall_status": overall_status,
        "local_head_before_run": git_text(["rev-parse", "HEAD"]),
        "remote_head_before_run": git_text(["rev-parse", REMOTE_REF]),
        "drift_before_run": git_text(["rev-list", "--left-right", "--count", f"HEAD...{REMOTE_REF}"]),
        "policy": {
            "existing_app_threads_only": True,
            "lanes": [part.strip() for part in args.lanes.split(",") if part.strip()],
            "read_only_requested": True,
            "approval_policy_requested": "never",
            "new_threads_created": False,
            "old_style_spawn_used": False,
            "advisory_body_published": False,
            "unfiltered_transport_published": False,
            "retry_attempts_per_operation": args.retries,
            "background_watch_requested": args.background_watch,
            "turn_start_after_resume_timeout_fallback_allowed": bool(args.allow_turn_start_after_resume_timeout),
            "work_while_waiting_required": args.background_watch,
            "phase_advance_requires_all_five_responses": True,
        },
        "local_app_server": {
            "watch_launcher_available": WATCH_LAUNCHER.exists(),
            "completion_notifier_receipt": f"{artifact_prefix}-v1.json",
            "watch_launcher_receipt": f"{launcher_prefix}-v1.json",
            "status_surface": "summaries_only",
            "background_receipts_expected": args.background_watch,
        },
        "execution": execution,
        "notifier_summary": {
            "available": bool(notifier.get("artifact_type")),
            "overall_status": notifier_status,
            "lanes": lane_rows(notifier),
        },
        "launcher_summary": {
            "available": bool(launcher.get("artifact_type")),
            "overall_status": launcher_status,
        },
        "claim_boundary": {
            "scope": "THOS council app-lane notification and completion watching only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
        "cadence_policy": {
            "preferred_x1_minutes": 60,
            "preferred_x2_minutes": 60,
            "duration_is_completion_proof": False,
            "background_watch_allows_productive_waiting": args.background_watch,
            "phase_advance_requires_completion_gate": True,
            "productive_waiting_research_prep_required": True,
        },
    }
    write_json(TRACE_DIR / f"{runner_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{runner_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Council App-Lane Notifier Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- mode: `{payload['mode']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head_before_run: `{payload['local_head_before_run']}`",
        f"- remote_head_before_run: `{payload['remote_head_before_run']}`",
        f"- drift_before_run: `{payload['drift_before_run']}`",
        "- policy: existing app threads only; read-only requested; no new threads; no old-style spawning; status-only publication.",
        f"- background_watch_requested: `{payload['policy'].get('background_watch_requested')}`",
        f"- work_while_waiting_required: `{payload['policy'].get('work_while_waiting_required')}`",
        f"- phase_advance_requires_all_five_responses: `{payload['policy'].get('phase_advance_requires_all_five_responses')}`",
        "- local app server: completion and watch surfaces are summarized only.",
        "- claim boundary: THOS council app-lane watching only; all GMUT gates remain open.",
        "- cadence: one-hour x1/x2 sessions are operating targets, not completion proof.",
        "",
        "## Execution",
        f"- execution_status: `{payload['execution'].get('execution_status')}`",
        f"- returncode: `{payload['execution'].get('returncode')}`",
        f"- pid: `{payload['execution'].get('pid')}`",
        f"- stdout_status: `{payload['execution'].get('stdout_status')}`",
        f"- stderr_nonempty: `{payload['execution'].get('stderr_nonempty')}`",
        "",
        "## Lane Summary",
    ]
    for row in payload.get("notifier_summary", {}).get("lanes", []):
        lines.append(
            f"- {row.get('lane')}: `{row.get('overall_status')}`, duration `{row.get('duration_seconds')}`, "
            f"read `{row.get('read_status')}`, resume `{row.get('resume_status')}`, "
            f"turn `{row.get('turn_status')}`, completion `{row.get('completion_status')}`."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_gate_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Council App-Lane Completion Gate",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- mode: `{payload['mode']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- drift_at_gate: `{payload['drift_at_gate']}`",
        f"- next_phase_allowed: `{payload['phase_advance_rule']['next_phase_allowed']}`",
        "- phase advance rule: all five sibling responses are required; duration is not completion proof.",
        "- claim boundary: THOS app-lane completion gating only; all GMUT gates remain open.",
        "",
        "## Gate Inputs",
        f"- runner: `{payload['gate_inputs']['runner_status']}`",
        f"- watch_launcher: `{payload['gate_inputs']['watch_launcher_status']}`",
        f"- completion_notifier: `{payload['gate_inputs']['completion_notifier_status']}`",
        "",
        "## Lane Summary",
    ]
    for row in payload.get("lanes", []):
        lines.append(
            f"- {row.get('lane')}: `{row.get('overall_status')}`, completion `{row.get('completion_status')}`, "
            f"read `{row.get('read_status')}`, resume `{row.get('resume_status')}`."
        )
    gaps = payload.get("open_gaps", [])
    if gaps:
        lines.extend(["", "## Open Gaps"])
        lines.extend(f"- `{gap}`" for gap in gaps)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lanes", default=DEFAULT_LANES)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--runner-prefix")
    parser.add_argument("--artifact-prefix")
    parser.add_argument("--launcher-prefix")
    parser.add_argument("--gate-prefix")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--call-timeout-seconds", type=int, default=90)
    parser.add_argument("--turn-timeout-seconds", type=int, default=900)
    parser.add_argument("--launch-timeout-seconds", type=int, default=3600)
    parser.add_argument(
        "--allow-turn-start-after-resume-timeout",
        action="store_true",
        help="Allow notifier fallback from read-ok/resume-timeout to direct turn/start, with status-only receipt metadata.",
    )
    parser.add_argument(
        "--background-watch",
        action="store_true",
        help="Start the app-lane watcher as a detached background process and return immediately.",
    )
    parser.add_argument(
        "--gate-only",
        action="store_true",
        help="Do not send messages; harvest watcher receipts and write a strict all-app-lane completion gate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_gate_payload(args) if args.gate_only else build_payload(args)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": payload["phase_slug"]}, indent=2))
    return 0 if str(payload["overall_status"]).startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
