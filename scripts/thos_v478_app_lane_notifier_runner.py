#!/usr/bin/env python3
"""Run a bounded v478 app-lane notifier pass through the local Codex app server."""

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
LAUNCHER = ROOT / "scripts" / "thos_app_lane_watch_launcher.py"
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


def command_for(args: argparse.Namespace, artifact_prefix: str, launcher_prefix: str) -> list[str]:
    command = [
        sys.executable,
        str(LAUNCHER),
        "--phase-slug",
        args.phase_slug,
        "--artifact-prefix",
        artifact_prefix,
        "--launcher-prefix",
        launcher_prefix,
        "--lanes",
        args.lanes,
        "--execute",
        "--retries",
        str(args.retries),
        "--call-timeout-seconds",
        str(args.call_timeout_seconds),
        "--turn-timeout-seconds",
        str(args.turn_timeout_seconds),
        "--launch-timeout-seconds",
        str(args.launch_timeout_seconds),
    ]
    if args.notify:
        command.append("--notify")
    return command


def read_json_if_present(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {"available": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {"available": False}
    return payload


def lane_summary(payload: dict[str, Any]) -> list[dict[str, Any]]:
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


def run_launcher(command: list[str], timeout_seconds: int) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
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
    status = "unparsed"
    for line in reversed([row.strip() for row in proc.stdout.splitlines() if row.strip()]):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            status = str(parsed.get("status", "unknown"))
            break
    return {
        "execution_status": "completed",
        "returncode": proc.returncode,
        "stdout_status": status,
        "stdout_bytes": len(proc.stdout.encode("utf-8", errors="replace")),
        "stderr_bytes": len(proc.stderr.encode("utf-8", errors="replace")),
        "stderr_nonempty": bool(proc.stderr.strip()),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    mode = "notify" if args.notify else "probe"
    runner_prefix = args.runner_prefix or f"{args.phase_slug}-app-lane-notifier-runner-{mode}"
    artifact_prefix = args.artifact_prefix or f"{args.phase_slug}-app-lane-runner-{mode}-completion-notifier"
    launcher_prefix = args.launcher_prefix or f"{args.phase_slug}-app-lane-runner-{mode}-watch-launcher"
    command = command_for(args, artifact_prefix, launcher_prefix)
    payload: dict[str, Any] = {
        "artifact_type": "v478_app_lane_notifier_runner",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "mode": mode,
        "overall_status": "PASS_SHAPE_ONLY" if LAUNCHER.exists() else "FAIL_LAUNCHER_MISSING",
        "local_head_before_run": git_text(["rev-parse", "HEAD"]),
        "remote_head_before_run": git_text(["rev-parse", REMOTE_REF]),
        "drift_before_run": git_text(["rev-list", "--left-right", "--count", f"HEAD...{REMOTE_REF}"]),
        "policy": {
            "existing_app_threads_only": True,
            "lanes": [part.strip() for part in args.lanes.split(",") if part.strip()],
            "read_only_requested": True,
            "approval_policy_requested": "never",
            "old_style_spawn_used": False,
            "new_threads_created": False,
            "unfiltered_event_payload_published": False,
            "advisory_body_published": False,
            "retry_attempts_per_operation": args.retries,
        },
        "launcher": {
            "script_available": LAUNCHER.exists(),
            "artifact_prefix": artifact_prefix,
            "launcher_prefix": launcher_prefix,
        },
        "claim_boundary": {
            "scope": "THOS app-lane notifier runner only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    if args.execute and LAUNCHER.exists():
        execution = run_launcher(command, args.launch_timeout_seconds + 30)
        notifier = read_json_if_present(f"{artifact_prefix}-v1.json")
        launcher = read_json_if_present(f"{launcher_prefix}-v1.json")
        payload["execution"] = execution
        payload["notifier_summary"] = {
            "available": bool(notifier.get("artifact_type")),
            "overall_status": notifier.get("overall_status"),
            "lanes": lane_summary(notifier),
        }
        payload["launcher_summary"] = {
            "available": bool(launcher.get("artifact_type")),
            "overall_status": launcher.get("overall_status"),
        }
        execution_ok = execution.get("returncode") == 0
        notifier_status = str(payload["notifier_summary"].get("overall_status", ""))
        launcher_status = str(payload["launcher_summary"].get("overall_status", ""))
        payload["overall_status"] = (
            "PASS"
            if execution_ok and notifier_status.startswith("PASS") and launcher_status.startswith("PASS")
            else "OPEN_GAP_APP_LANE_RUNNER"
        )
    elif args.execute:
        payload["execution"] = {"execution_status": "skipped_missing_launcher"}
    write_json(TRACE_DIR / f"{runner_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{runner_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} App-Lane Notifier Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- mode: `{payload['mode']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head_before_run: `{payload['local_head_before_run']}`",
        f"- remote_head_before_run: `{payload['remote_head_before_run']}`",
        f"- drift_before_run: `{payload['drift_before_run']}`",
        "- policy: existing app threads only; read-only requested; no new threads; no old-style spawning; status-only publication.",
        "- claim boundary: THOS app-lane runner only; all GMUT gates remain open.",
        "",
        "## Launcher",
        f"- artifact_prefix: `{payload['launcher']['artifact_prefix']}`",
        f"- launcher_prefix: `{payload['launcher']['launcher_prefix']}`",
    ]
    execution = payload.get("execution")
    if isinstance(execution, dict):
        lines.extend(
            [
                "",
                "## Execution",
                f"- execution_status: `{execution.get('execution_status')}`",
                f"- returncode: `{execution.get('returncode')}`",
                f"- stdout_status: `{execution.get('stdout_status')}`",
                f"- stderr_nonempty: `{execution.get('stderr_nonempty')}`",
            ]
        )
    notifier = payload.get("notifier_summary")
    if isinstance(notifier, dict):
        lines.extend(["", "## Lane Summary"])
        for row in notifier.get("lanes", []):
            lines.append(
                f"- {row.get('lane')}: `{row.get('overall_status')}`, "
                f"read `{row.get('read_status')}`, resume `{row.get('resume_status')}`, "
                f"turn `{row.get('turn_status')}`, completion `{row.get('completion_status')}`."
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", default="v478-thos-v6-x1")
    parser.add_argument("--lanes", default=DEFAULT_LANES)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--runner-prefix")
    parser.add_argument("--artifact-prefix")
    parser.add_argument("--launcher-prefix")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--call-timeout-seconds", type=int, default=90)
    parser.add_argument("--turn-timeout-seconds", type=int, default=900)
    parser.add_argument("--launch-timeout-seconds", type=int, default=3600)
    return parser.parse_args()


def main() -> int:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "phase_slug": payload["phase_slug"]}, indent=2))
    return 0 if str(payload["overall_status"]).startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
