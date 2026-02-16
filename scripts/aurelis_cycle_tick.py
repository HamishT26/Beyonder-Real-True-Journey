#!/usr/bin/env python3
"""Run one full Aurelis continuity cycle tick in a single command."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT_MD = "docs/aurelis-cycle-tick-report.md"
STDOUT_SENTINEL = "-"


def run(
    cmd: list[str],
    dry_run: bool = False,
    timeout_sec: int = 0,
) -> tuple[bool, str, bool]:
    if dry_run:
        return True, "[dry-run] command not executed", False

    try:
        p = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_sec if timeout_sec > 0 else None,
        )
    except subprocess.TimeoutExpired as exc:
        partial = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
        message = f"[timeout] step exceeded {timeout_sec}s"
        if partial.strip():
            message += f"\n{partial.strip()}"
        return False, message, True

    out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    return p.returncode == 0, out.strip(), False


def resolve_repo_path(path_value: str) -> Path:
    resolved = (ROOT / path_value).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit(f"path must stay within repository root: {path_value}") from exc
    return resolved


def write_text_output(path_value: str, content: str, label: str) -> None:
    if path_value == STDOUT_SENTINEL:
        print(f"\n--- BEGIN {label} ---")
        print(content)
        print(f"--- END {label} ---")
        return

    output_path = resolve_repo_path(path_value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content + "\n", encoding="utf-8")
    print(f"\nWrote {label.lower()}: {output_path.relative_to(ROOT)}")


def write_json_output(path_value: str, payload: dict) -> None:
    formatted = json.dumps(payload, indent=2)
    if path_value == STDOUT_SENTINEL:
        print("\n--- BEGIN CYCLE TICK JSON STATUS ---")
        print(formatted)
        print("--- END CYCLE TICK JSON STATUS ---")
        return

    output_path = resolve_repo_path(path_value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(formatted + "\n", encoding="utf-8")
    print(f"\nWrote cycle tick json status: {output_path.relative_to(ROOT)}")


def build_markdown_report(
    run_started_utc: datetime,
    run_finished_utc: datetime,
    dry_run: bool,
    step_timeout_sec: int,
    results: list[dict[str, str | bool]],
) -> str:
    lines = [
        "# Aurelis Cycle Tick Report",
        "",
        f"- Started (UTC): {run_started_utc.isoformat()}",
        f"- Mode: {'dry-run' if dry_run else 'execute'}",
        f"- Step timeout (s): {step_timeout_sec if step_timeout_sec > 0 else 'disabled'}",
        f"- Finished (UTC): {run_finished_utc.isoformat()}",
        f"- Duration (s): {(run_finished_utc - run_started_utc).total_seconds():.3f}",
        f"- Root: `{ROOT}`",
        "",
        "## Step Results",
        "",
        "| Step | Status | Command |",
        "|---|---|---|",
    ]

    for idx, result in enumerate(results, start=1):
        status = "PASS" if result["ok"] else ("TIMEOUT" if result.get("timed_out") else "FAIL")
        lines.append(f"| {idx} | {status} | `{result['command']}` |")

    lines.append("")
    lines.append("## Step Output")
    lines.append("")

    for idx, result in enumerate(results, start=1):
        lines.append(f"### {idx}. `{result['command']}`")
        lines.append("")
        lines.append("```text")
        lines.append(result["output"] or "(no output)")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def build_json_status(
    run_started_utc: datetime,
    run_finished_utc: datetime,
    dry_run: bool,
    continue_on_error: bool,
    step_timeout_sec: int,
    results: list[dict[str, str | bool]],
) -> dict:
    failed_steps = [idx for idx, result in enumerate(results, start=1) if not result["ok"]]
    return {
        "started_utc": run_started_utc.isoformat(),
        "finished_utc": run_finished_utc.isoformat(),
        "duration_seconds": round((run_finished_utc - run_started_utc).total_seconds(), 3),
        "mode": "dry-run" if dry_run else "execute",
        "continue_on_error": continue_on_error,
        "step_timeout_sec": step_timeout_sec,
        "success": not failed_steps,
        "failed_steps": failed_steps,
        "steps": results,
    }


def validate_report_args(no_report: bool, report_md: str) -> str:
    report_md = report_md.strip()
    if no_report:
        if report_md not in ("", DEFAULT_REPORT_MD):
            raise SystemExit("cannot combine --no-report with a custom --report-md path")
        return ""
    return report_md


def main() -> None:
    p = argparse.ArgumentParser(description="Execute one Aurelis continuity cycle tick")
    p.add_argument("--user-message", required=True)
    p.add_argument("--assistant-reflection", required=True)
    p.add_argument("--progress-snapshot", required=True)
    p.add_argument("--next-step", required=True)
    p.add_argument("--query", default="continue", help="Query term for continuity lookup")
    p.add_argument("--query-limit", type=int, default=3, help="Max number of query results to return")
    p.add_argument("--summary-take", type=int, default=5)
    p.add_argument(
        "--step-timeout-sec",
        type=int,
        default=0,
        help="Per-step timeout in seconds (0 disables timeouts).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print and report commands without executing underlying scripts.",
    )
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running remaining steps after a step failure; exit non-zero at end if any failed.",
    )
    p.add_argument(
        "--report-md",
        default=DEFAULT_REPORT_MD,
        help="Path to write markdown cycle report (use empty string to skip, '-' for stdout).",
    )
    p.add_argument(
        "--json-status",
        default="",
        help="Optional JSON status output path ('-' for stdout, empty to disable).",
    )
    p.add_argument(
        "--no-report",
        action="store_true",
        help="Disable markdown report output (equivalent to --report-md '').",
    )
    args = p.parse_args()

    if args.query_limit < 1:
        raise SystemExit("--query-limit must be >= 1")
    if args.step_timeout_sec < 0:
        raise SystemExit("--step-timeout-sec must be >= 0")

    report_md = validate_report_args(args.no_report, args.report_md)
    json_status = args.json_status.strip()

    if report_md not in ("", STDOUT_SENTINEL):
        resolve_repo_path(report_md)
    if json_status not in ("", STDOUT_SENTINEL):
        resolve_repo_path(json_status)

    steps = [
        [
            "python3",
            "scripts/aurelis_memory_update.py",
            "--user-message",
            args.user_message,
            "--assistant-reflection",
            args.assistant_reflection,
            "--progress-snapshot",
            args.progress_snapshot,
            "--next-step",
            args.next_step,
        ],
        ["python3", "scripts/aurelis_memory_summary.py", "--take", str(args.summary_take)],
        ["python3", "scripts/aurelis_next_steps_snapshot.py"],
        ["python3", "scripts/aurelis_memory_integrity_check.py", "--strict"],
        [
            "python3",
            "scripts/aurelis_memory_query.py",
            "--contains",
            args.query,
            "--limit",
            str(args.query_limit),
        ],
    ]

    started = datetime.now(timezone.utc)
    results: list[dict[str, str | bool]] = []

    for cmd in steps:
        ok, out, timed_out = run(cmd, dry_run=args.dry_run, timeout_sec=args.step_timeout_sec)
        command = shlex.join(cmd)
        print(f"$ {command}")
        print(out)
        results.append({"command": command, "ok": ok, "output": out, "timed_out": timed_out})
        if not ok and not args.continue_on_error:
            break

    finished = datetime.now(timezone.utc)
    report = build_markdown_report(
        started,
        finished,
        args.dry_run,
        args.step_timeout_sec,
        results,
    )
    status_payload = build_json_status(
        started,
        finished,
        args.dry_run,
        args.continue_on_error,
        args.step_timeout_sec,
        results,
    )

    if report_md:
        write_text_output(report_md, report, "CYCLE TICK MARKDOWN REPORT")
    if json_status:
        write_json_output(json_status, status_payload)

    if status_payload["success"]:
        raise SystemExit(0)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
