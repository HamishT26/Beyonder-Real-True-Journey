"""
body_track_runner.py
--------------------

Reproducible Body-track smoke runner for Trinity artifacts.

This script executes a fixed set of checks, captures outputs, and writes:
1) a timestamped JSON record,
2) a timestamped markdown report,
3) latest JSON/markdown pointers for quick review.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List


@dataclass
class StepResult:
    name: str
    command: List[str]
    returncode: int
    duration_seconds: float
    stdout: str
    stderr: str


def _run_step(name: str, command: List[str]) -> StepResult:
    started = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    duration = time.perf_counter() - started
    return StepResult(
        name=name,
        command=command,
        returncode=completed.returncode,
        duration_seconds=duration,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def _trim(text: str, max_lines: int = 20) -> str:
    if not text:
        return "(empty)"
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines] + [f"... ({len(lines) - max_lines} more lines)"])


def _build_markdown(generated_utc: str, overall_status: str, steps: List[StepResult]) -> str:
    rows = []
    for step in steps:
        step_status = "PASS" if step.returncode == 0 else "FAIL"
        rows.append(
            f"| {step.name} | {step_status} | {step.returncode} | {step.duration_seconds:.3f} | "
            f"`{' '.join(step.command)}` |"
        )

    lines = [
        "# Body Track Smoke Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Step summary",
        "| step | status | returncode | duration_seconds | command |",
        "|---|---|---:|---:|---|",
    ]
    if rows:
        lines.extend(rows)
    else:
        lines.append("| (none) |")

    for step in steps:
        lines.extend(
            [
                "",
                f"## {step.name}",
                "",
                f"- returncode: `{step.returncode}`",
                f"- duration_seconds: `{step.duration_seconds:.3f}`",
                "",
                "### stdout (trimmed)",
                "```",
                _trim(step.stdout),
                "```",
                "",
                "### stderr (trimmed)",
                "```",
                _trim(step.stderr),
                "```",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Body-track smoke checks and emit reports.")
    parser.add_argument(
        "--gammas",
        type=float,
        nargs="+",
        default=[0.0, 0.05, 0.1],
        help="Gamma values for run_simulation.py",
    )
    parser.add_argument(
        "--reports-dir",
        default="docs/body-track-runs",
        help="Directory for timestamped report artifacts.",
    )
    parser.add_argument(
        "--latest-json",
        default="docs/body-track-smoke-latest.json",
        help="Path for latest JSON status artifact.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/body-track-smoke-latest.md",
        help="Path for latest markdown status artifact.",
    )
    args = parser.parse_args()

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    py_files = [
        "Freed_id_registry.py",
        "freed_id_registry.py",
        "qc_transmuter.py",
        "trinity_orchestrator.py",
        "trinity_orchestrator_full.py",
        "trinity_simulation_engine.py",
        "run_simulation.py",
        "body_track_runner.py",
    ]

    steps = [
        _run_step("compile_python_modules", [sys.executable, "-m", "py_compile", *py_files]),
        _run_step("run_full_orchestrator_demo", [sys.executable, "trinity_orchestrator_full.py"]),
        _run_step(
            "run_gmut_simulation",
            [sys.executable, "run_simulation.py", "--gammas", *[str(g) for g in args.gammas]],
        ),
    ]

    overall_status = "PASS" if all(step.returncode == 0 for step in steps) else "FAIL"
    json_payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "steps": [asdict(step) for step in steps],
    }
    markdown = _build_markdown(generated_utc, overall_status, steps)

    timestamped_json = reports_dir / f"{stamp}-body-track-smoke.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-smoke.md"
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(json_payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(json_payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
