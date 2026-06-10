#!/usr/bin/env python3
"""Coordinate app and CLI sibling completion watchers with curated receipts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
APP_RUNNER = ROOT / "scripts" / "thos_council_app_lane_notifier_runner.py"
CLI_NOTIFIER = ROOT / "scripts" / "thos_cli_lane_completion_notifier.py"
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


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False}


def run_command(command: list[str], timeout_seconds: int) -> dict[str, Any]:
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
            status = str(parsed.get("status", parsed.get("aggregate_status", "unknown")))
            break
    return {
        "execution_status": "completed",
        "returncode": proc.returncode,
        "stdout_status": status,
        "stdout_bytes": len(proc.stdout.encode("utf-8", errors="replace")),
        "stderr_bytes": len(proc.stderr.encode("utf-8", errors="replace")),
        "stderr_nonempty": bool(proc.stderr.strip()),
    }


def app_command(args: argparse.Namespace) -> tuple[list[str], str, str, str]:
    runner_prefix = f"{args.phase_slug}-background-council-app-runner"
    artifact_prefix = f"{args.phase_slug}-background-council-app-completion"
    launcher_prefix = f"{args.phase_slug}-background-council-app-watch"
    command = [
        sys.executable,
        str(APP_RUNNER),
        "--phase-slug",
        args.phase_slug,
        "--lanes",
        args.app_lanes,
        "--runner-prefix",
        runner_prefix,
        "--artifact-prefix",
        artifact_prefix,
        "--launcher-prefix",
        launcher_prefix,
        "--retries",
        str(args.retries),
        "--call-timeout-seconds",
        str(args.app_call_timeout_seconds),
        "--turn-timeout-seconds",
        str(args.app_turn_timeout_seconds),
        "--launch-timeout-seconds",
        str(args.app_launch_timeout_seconds),
    ]
    if args.notify:
        command.append("--notify")
    if args.execute:
        command.append("--execute")
    return command, runner_prefix, artifact_prefix, launcher_prefix


def cli_command(args: argparse.Namespace, output_dir: Path) -> tuple[list[str], str]:
    receipt_prefix = f"{args.phase_slug}-background-cli-completion"
    command = [
        sys.executable,
        str(CLI_NOTIFIER),
        "--output-dir",
        str(output_dir),
        "--phase-slug",
        args.phase_slug,
        "--poll-seconds",
        str(args.cli_poll_seconds),
        "--timeout-seconds",
        str(args.cli_timeout_seconds),
        "--receipt-json",
        str(TRACE_DIR / f"{receipt_prefix}-v1.json"),
        "--receipt-md",
        str(TRACE_DIR / f"{receipt_prefix}-v1.md"),
    ]
    for lane in [part.strip() for part in args.cli_lanes.split(",") if part.strip()]:
        command.extend(["--lane", lane])
    return command, receipt_prefix


def lane_completion_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "notifier_summary" in payload:
        return payload.get("notifier_summary", {}).get("lanes", [])
    return payload.get("lanes", [])


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    app_cmd, app_runner_prefix, app_artifact_prefix, app_launcher_prefix = app_command(args)
    cli_output_dir = Path(args.cli_output_dir) if args.cli_output_dir else Path(tempfile.gettempdir()) / f"{args.phase_slug}-cli-lanes"
    cli_cmd, cli_receipt_prefix = cli_command(args, cli_output_dir)
    payload: dict[str, Any] = {
        "artifact_type": "background_sibling_notifier_runner",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "mode": "execute" if args.execute else "plan",
        "overall_status": "PLAN_ONLY",
        "local_head_before_run": git_text(["rev-parse", "HEAD"]),
        "remote_head_before_run": git_text(["rev-parse", REMOTE_REF]),
        "drift_before_run": git_text(["rev-list", "--left-right", "--count", f"HEAD...{REMOTE_REF}"]),
        "policy": {
            "existing_app_threads_only": True,
            "new_threads_created": False,
            "old_style_spawn_used": False,
            "app_lanes": [part.strip() for part in args.app_lanes.split(",") if part.strip()],
            "cli_lanes": [part.strip() for part in args.cli_lanes.split(",") if part.strip()],
            "status_only_publication": True,
            "final_marker_bridge": "hash_and_byte_count_only",
            "temp_output_publication": "redacted_summary_only",
        },
        "receipts": {
            "app_runner": f"{app_runner_prefix}-v1.json",
            "app_completion": f"{app_artifact_prefix}-v1.json",
            "app_watch": f"{app_launcher_prefix}-v1.json",
            "cli_completion": f"{cli_receipt_prefix}-v1.json",
        },
        "claim_boundary": {
            "scope": "THOS sibling notification and completion watching only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    if args.execute:
        app_execution = run_command(app_cmd, args.app_launch_timeout_seconds + 60)
        cli_execution = run_command(cli_cmd, int(args.cli_timeout_seconds + 30))
        app_receipt = read_json(TRACE_DIR / f"{app_runner_prefix}-v1.json")
        cli_receipt = read_json(TRACE_DIR / f"{cli_receipt_prefix}-v1.json")
        app_status = str(app_receipt.get("overall_status", "missing"))
        cli_status = str(cli_receipt.get("aggregate_status", "missing"))
        payload["execution"] = {"app": app_execution, "cli": cli_execution}
        payload["summaries"] = {
            "app_status": app_status,
            "app_lanes": lane_completion_rows(app_receipt),
            "cli_status": cli_status,
            "cli_lanes": lane_completion_rows(cli_receipt),
        }
        payload["overall_status"] = (
            "ALL_DONE"
            if app_status.startswith("PASS") and cli_status == "FINAL_MESSAGES_READY"
            else "APP_DONE_CLI_FINAL_MARKER_OPEN"
            if app_status.startswith("PASS")
            else "OPEN_GAP_BACKGROUND_NOTIFIER"
        )
    write_json(TRACE_DIR / f"{args.runner_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.runner_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Background Sibling Notifier Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- mode: `{payload['mode']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head_before_run: `{payload['local_head_before_run']}`",
        f"- remote_head_before_run: `{payload['remote_head_before_run']}`",
        f"- drift_before_run: `{payload['drift_before_run']}`",
        "- policy: existing app threads only; no new threads; no old-style spawning; status-only publication.",
        "- final marker bridge: hash and byte counts only; temp output remains unpublished.",
        "- claim boundary: THOS notification only; all GMUT gates remain open.",
        "",
        "## Receipts",
        *[f"- {name}: `{receipt}`" for name, receipt in payload["receipts"].items()],
    ]
    summaries = payload.get("summaries")
    if isinstance(summaries, dict):
        lines.extend(
            [
                "",
                "## Summary",
                f"- app_status: `{summaries.get('app_status')}`",
                f"- cli_status: `{summaries.get('cli_status')}`",
            ]
        )
        for lane in summaries.get("app_lanes", []):
            lines.append(f"- app {lane.get('lane')}: `{lane.get('overall_status')}`, completion `{lane.get('completion_status')}`.")
        for lane in summaries.get("cli_lanes", []):
            lines.append(f"- cli {lane.get('lane')}: `{lane.get('completion_status')}`, final bytes `{lane.get('final_message_bytes')}`.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--runner-prefix")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--app-lanes", default="Cicero,Kierkegaard,Aristotle")
    parser.add_argument("--cli-lanes", default="Arby,Aster Vale")
    parser.add_argument("--cli-output-dir")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--app-call-timeout-seconds", type=int, default=90)
    parser.add_argument("--app-turn-timeout-seconds", type=int, default=900)
    parser.add_argument("--app-launch-timeout-seconds", type=int, default=3600)
    parser.add_argument("--cli-poll-seconds", type=float, default=30)
    parser.add_argument("--cli-timeout-seconds", type=float, default=3600)
    args = parser.parse_args()
    args.runner_prefix = args.runner_prefix or f"{args.phase_slug}-background-sibling-notifier-runner"
    return args


def main() -> int:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "phase_slug": payload["phase_slug"]}, indent=2))
    return 0 if payload["overall_status"] in {"ALL_DONE", "APP_DONE_CLI_FINAL_MARKER_OPEN", "PLAN_ONLY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
