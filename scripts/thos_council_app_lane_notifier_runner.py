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
    if args.notify:
        command.append("--notify")
    if args.execute:
        command.append("--execute")
    if not args.execute:
        return {"execution_status": "planned_only", "returncode": None}
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
    payload: dict[str, Any] = {
        "artifact_type": "council_app_lane_notifier_runner",
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "phase_slug": args.phase_slug,
        "mode": mode,
        "overall_status": "PASS" if execution_ok and status_ok else "OPEN_GAP_COUNCIL_APP_LANE",
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
        },
        "local_app_server": {
            "watch_launcher_available": WATCH_LAUNCHER.exists(),
            "completion_notifier_receipt": f"{artifact_prefix}-v1.json",
            "watch_launcher_receipt": f"{launcher_prefix}-v1.json",
            "status_surface": "summaries_only",
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
        "- local app server: completion and watch surfaces are summarized only.",
        "- claim boundary: THOS council app-lane watching only; all GMUT gates remain open.",
        "",
        "## Execution",
        f"- execution_status: `{payload['execution'].get('execution_status')}`",
        f"- returncode: `{payload['execution'].get('returncode')}`",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
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
