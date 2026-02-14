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
    metrics: Dict[str, object]


def _run_step(
    name: str,
    command: List[str],
    analyzer: Optional[Callable[[str, str, int], Dict[str, object]]] = None,
) -> StepResult:
    started = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    duration = time.perf_counter() - started
    metrics: Dict[str, object] = {}
    if analyzer is not None:
        try:
            metrics = analyzer(completed.stdout, completed.stderr, completed.returncode)
        except Exception as exc:  # pragma: no cover - defensive fallback
            metrics = {"analyzer_error": str(exc)}

    return StepResult(
        name=name,
        command=command,
        returncode=completed.returncode,
        duration_seconds=duration,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
        metrics=metrics,
    )


def _trim(text: str, max_lines: int = 20) -> str:
    if not text:
        return "(empty)"
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines] + [f"... ({len(lines) - max_lines} more lines)"])


def _build_markdown(generated_utc: str, overall_status: str, steps: List[StepResult]) -> str:
def _analyze_orchestrator(stdout: str, _stderr: str, returncode: int) -> Dict[str, object]:
    if returncode != 0:
        return {"task_count": 0, "analysis_status": "skipped_due_to_failure"}

    task_payloads = []
    for line in stdout.splitlines():
        if "Task " not in line or " result:" not in line:
            continue
        payload_str = line.split("result:", 1)[1].strip()
        try:
            parsed = ast.literal_eval(payload_str)
        except (ValueError, SyntaxError):
            continue
        if isinstance(parsed, dict):
            task_payloads.append(parsed)

    exotic_generated = []
    final_total_exotic = None
    for payload in task_payloads:
        generated = payload.get("exotic_energy_generated")
        if isinstance(generated, (int, float)):
            exotic_generated.append(float(generated))
        total = payload.get("total_exotic_energy")
        if isinstance(total, (int, float)):
            final_total_exotic = float(total)

    metrics: Dict[str, object] = {"task_count": len(task_payloads)}
    if exotic_generated:
        metrics["avg_exotic_energy_generated"] = round(sum(exotic_generated) / len(exotic_generated), 6)
    if final_total_exotic is not None:
        metrics["final_total_exotic_energy"] = round(final_total_exotic, 6)
    return metrics


def _analyze_simulation(stdout: str, _stderr: str, returncode: int) -> Dict[str, object]:
    if returncode != 0:
        return {"gamma_count": 0, "analysis_status": "skipped_due_to_failure"}

    pattern = re.compile(r"Gamma=([0-9.]+): energy density ratio = ([0-9.]+)")
    gamma_ratios: Dict[str, float] = {}
    for line in stdout.splitlines():
        match = pattern.search(line)
        if match:
            gamma_ratios[match.group(1)] = float(match.group(2))

    metrics: Dict[str, object] = {"gamma_count": len(gamma_ratios), "gamma_ratios": gamma_ratios}
    if gamma_ratios:
        ratios = list(gamma_ratios.values())
        metrics["ratio_min"] = min(ratios)
        metrics["ratio_max"] = max(ratios)
        metrics["ratio_span"] = round(max(ratios) - min(ratios), 6)
    return metrics


def _build_markdown(
    generated_utc: str,
    overall_status: str,
    summary: Dict[str, object],
    steps: List[StepResult],
) -> str:
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
        "## Summary metrics",
        f"- pass_rate: `{summary['pass_rate']}`",
        f"- total_duration_seconds: `{summary['total_duration_seconds']}`",
        f"- body_health_score: `{summary['body_health_score']}`",
        f"- speed_band: `{summary['speed_band']}`",
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
        if step.metrics:
            lines.extend(
                [
                    "",
                    "### extracted_metrics",
                    "```json",
                    json.dumps(step.metrics, indent=2),
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
    parser.add_argument(
        "--latest-metrics",
        default="docs/body-track-metrics-latest.json",
        help="Path for latest body summary metrics artifact.",
    )
    parser.add_argument(
        "--metrics-history",
        default="docs/body-track-metrics-history.jsonl",
        help="Path for append-only body metrics history.",
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
        _run_step(
            "run_full_orchestrator_demo",
            [sys.executable, "trinity_orchestrator_full.py"],
            analyzer=_analyze_orchestrator,
        ),
        _run_step(
            "run_gmut_simulation",
            [sys.executable, "run_simulation.py", "--gammas", *[str(g) for g in args.gammas]],
            analyzer=_analyze_simulation,
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
