#!/usr/bin/env python3
"""Launch the app-lane completion notifier with a sanitized status receipt."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTIFIER = REPO_ROOT / "scripts" / "thos_app_lane_completion_notifier.py"
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"
DEFAULT_LANES = "Cicero,Kierkegaard,Aristotle"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def git_text(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def artifact_prefix_for(phase_slug: str) -> str:
    return f"{phase_slug}-app-lane-completion-notifier"


def launcher_prefix_for(phase_slug: str) -> str:
    return f"{phase_slug}-app-lane-watch-launcher"


def redacted_command(command: list[str]) -> list[str]:
    redacted: list[str] = []
    for item in command:
        if "\\" in item or "/" in item or ":" in item:
            redacted.append("<path>")
        else:
            redacted.append(item)
    return redacted


def build_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(NOTIFIER),
        "--phase-slug",
        args.phase_slug,
        "--artifact-prefix",
        args.artifact_prefix,
        "--lanes",
        args.lanes,
        "--retries",
        str(args.retries),
        "--call-timeout-seconds",
        str(args.call_timeout_seconds),
        "--turn-timeout-seconds",
        str(args.turn_timeout_seconds),
    ]
    if args.notify:
        command.append("--notify")
    if args.allow_turn_start_after_resume_timeout:
        command.append("--allow-turn-start-after-resume-timeout")
    return command


def parse_status_stdout(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return {
                "status": parsed.get("status", "unknown"),
                "phase_slug": parsed.get("phase_slug", "unknown"),
                "lanes": parsed.get("lanes", "unknown"),
            }
    except json.JSONDecodeError:
        pass
    for line in reversed([row.strip() for row in text.splitlines() if row.strip()]):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return {
                "status": parsed.get("status", "unknown"),
                "phase_slug": parsed.get("phase_slug", "unknown"),
                "lanes": parsed.get("lanes", "unknown"),
            }
    return {"status": "unparsed", "lanes": "unknown"}


def read_notifier_summary(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    lanes = []
    for lane in payload.get("lanes", []):
        lanes.append(
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
    return {
        "available": True,
        "artifact_type": payload.get("artifact_type"),
        "phase_slug": payload.get("phase_slug"),
        "overall_status": payload.get("overall_status"),
        "lanes": lanes,
    }


def execute_notifier(args: argparse.Namespace, command: list[str]) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.launch_timeout_seconds,
            check=False,
        )
        return {
            "execution_status": "completed",
            "returncode": proc.returncode,
            "stdout_summary": parse_status_stdout(proc.stdout),
            "stdout_bytes": len(proc.stdout.encode("utf-8", errors="replace")),
            "stderr_bytes": len(proc.stderr.encode("utf-8", errors="replace")),
            "stderr_nonempty": bool(proc.stderr.strip()),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "execution_status": "timeout",
            "returncode": None,
            "stdout_bytes": len((exc.stdout or "").encode("utf-8", errors="replace"))
            if isinstance(exc.stdout, str)
            else 0,
            "stderr_bytes": len((exc.stderr or "").encode("utf-8", errors="replace"))
            if isinstance(exc.stderr, str)
            else 0,
            "stderr_nonempty": bool(exc.stderr),
        }


def build_receipt(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    command = build_command(args)
    notifier_json = TRACE_DIR / f"{args.artifact_prefix}-v1.json"
    notifier_md = TRACE_DIR / f"{args.artifact_prefix}-v1.md"
    receipt: dict[str, Any] = {
        "artifact_type": "app_lane_watch_launcher",
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "phase_slug": args.phase_slug,
        "overall_status": "PASS_SHAPE_ONLY" if NOTIFIER.exists() else "FAIL_NOTIFIER_MISSING",
        "local_head_before_run": git_text(["rev-parse", "HEAD"]),
        "remote_head_before_run": git_text(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"]),
        "drift_before_run": git_text(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"]),
        "policy": {
            "existing_app_threads_only": True,
            "new_threads_created": False,
            "old_style_spawn_used": False,
            "read_only_requested": True,
            "approval_policy_requested": "never",
            "unfiltered_event_stream_published": False,
            "advisory_text_published": False,
            "notify_mode": args.notify,
            "lanes": [part.strip() for part in args.lanes.split(",") if part.strip()],
            "retry_attempts_per_operation": args.retries,
            "turn_start_after_resume_timeout_fallback_allowed": bool(args.allow_turn_start_after_resume_timeout),
        },
        "notifier": {
            "script_available": NOTIFIER.exists(),
            "command_preview": redacted_command(command),
            "receipt_json_name": notifier_json.name,
            "receipt_md_name": notifier_md.name,
        },
        "claim_boundary": {
            "scope": "THOS app-lane notifier launch and completion watching only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    if args.execute and NOTIFIER.exists():
        receipt["execution"] = execute_notifier(args, command)
        receipt["notifier_summary"] = read_notifier_summary(notifier_json)
        execution_ok = receipt["execution"].get("returncode") == 0
        notifier_ok = receipt["notifier_summary"].get("overall_status", "").startswith("PASS")
        receipt["overall_status"] = "PASS" if execution_ok and notifier_ok else "OPEN_GAP_APP_LANE_LAUNCH"
    elif args.execute:
        receipt["execution"] = {"execution_status": "skipped_missing_notifier"}
    return receipt


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} App-Lane Watch Launcher",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head_before_run: `{payload['local_head_before_run']}`",
        f"- remote_head_before_run: `{payload['remote_head_before_run']}`",
        f"- drift_before_run: `{payload['drift_before_run']}`",
        "- policy: existing app threads only; no new threads; no old-style spawning; no advisory text publication.",
        "- claim boundary: THOS app-lane watching only; all GMUT gates remain open.",
        "",
        "## Notifier",
        f"- script_available: `{payload['notifier']['script_available']}`",
        f"- receipt_json_name: `{payload['notifier']['receipt_json_name']}`",
        f"- receipt_md_name: `{payload['notifier']['receipt_md_name']}`",
    ]
    execution = payload.get("execution")
    if isinstance(execution, dict):
        lines.extend(
            [
                "",
                "## Execution",
                f"- execution_status: `{execution.get('execution_status')}`",
                f"- returncode: `{execution.get('returncode')}`",
                f"- stdout_summary: `{execution.get('stdout_summary')}`",
                f"- stderr_nonempty: `{execution.get('stderr_nonempty')}`",
            ]
        )
    summary = payload.get("notifier_summary", {})
    if isinstance(summary, dict) and summary.get("available"):
        lines.extend(["", "## Lane Summary"])
        for lane in summary.get("lanes", []):
            lines.append(
                f"- {lane.get('lane')}: `{lane.get('overall_status')}`, duration `{lane.get('duration_seconds')}`, "
                f"read `{lane.get('read_status')}`, resume `{lane.get('resume_status')}`, "
                f"turn `{lane.get('turn_status')}`, completion `{lane.get('completion_status')}`."
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--artifact-prefix")
    parser.add_argument("--launcher-prefix")
    parser.add_argument("--lanes", default=DEFAULT_LANES)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--call-timeout-seconds", type=int, default=90)
    parser.add_argument("--turn-timeout-seconds", type=int, default=900)
    parser.add_argument("--launch-timeout-seconds", type=int, default=3600)
    parser.add_argument(
        "--allow-turn-start-after-resume-timeout",
        action="store_true",
        help="Allow notifier fallback from read-ok/resume-timeout to direct turn/start, with status-only receipt metadata.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.artifact_prefix = args.artifact_prefix or artifact_prefix_for(args.phase_slug)
    args.launcher_prefix = args.launcher_prefix or launcher_prefix_for(args.phase_slug)
    payload = build_receipt(args)
    write_json(TRACE_DIR / f"{args.launcher_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.launcher_prefix}-v1.md", payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
