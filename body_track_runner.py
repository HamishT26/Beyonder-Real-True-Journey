"""
body_track_runner.py
--------------------

Reproducible Body-track smoke runner for Trinity artifacts.

This script executes fixed checks, captures outputs, and writes:
1) timestamped JSON/markdown records,
2) latest JSON/markdown pointers,
3) summary metrics + append-only history.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional


BENCHMARK_PROFILES: Dict[str, Dict[str, float]] = {
    "quick": {
        "min_pass_rate": 1.0,
        "max_duration_sec": 1.5,
        "min_health_score": 94.0,
    },
    "standard": {
        "min_pass_rate": 1.0,
        "max_duration_sec": 1.0,
        "min_health_score": 95.0,
    },
    "strict": {
        "min_pass_rate": 1.0,
        "max_duration_sec": 0.8,
        "min_health_score": 97.0,
    },
}


def _load_profile_benchmark_overrides(policy_path: Path) -> Dict[str, Dict[str, float]]:
    if not policy_path.exists():
        return {}
    try:
        payload = json.loads(policy_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    profiles = payload.get("benchmark_profiles", {})
    if not isinstance(profiles, dict):
        return {}

    normalized: Dict[str, Dict[str, float]] = {}
    for profile, values in profiles.items():
        if not isinstance(values, dict):
            continue
        try:
            normalized[str(profile)] = {
                "min_pass_rate": float(values["min_pass_rate"]),
                "max_duration_sec": float(values["max_duration_sec"]),
                "min_health_score": float(values["min_health_score"]),
            }
        except (KeyError, TypeError, ValueError):
            continue
    return normalized


@dataclass
class StepResult:
    name: str
    command: List[str]
    returncode: int
    duration_seconds: float
    stdout: str
    stderr: str
    metrics: Dict[str, object] = field(default_factory=dict)


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


def _analyze_orchestrator(stdout: str, _stderr: str, returncode: int) -> Dict[str, object]:
    if returncode != 0:
        return {"task_count": 0, "analysis_status": "skipped_due_to_failure"}

    task_payloads: List[Dict[str, object]] = []
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

    exotic_generated: List[float] = []
    final_total_exotic: Optional[float] = None
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


def _speed_band(total_duration_seconds: float) -> str:
    if total_duration_seconds < 0.5:
        return "fast"
    if total_duration_seconds < 2.5:
        return "steady"
    return "heavy"


def _build_summary(generated_utc: str, stamp: str, steps: List[StepResult]) -> Dict[str, object]:
    passed_steps = sum(1 for step in steps if step.returncode == 0)
    total_steps = len(steps)
    total_duration = round(sum(step.duration_seconds for step in steps), 6)
    pass_rate = round((passed_steps / total_steps) if total_steps else 0.0, 6)
    body_health_score = round(pass_rate * 100.0, 2)
    return {
        "generated_utc": generated_utc,
        "stamp": stamp,
        "total_steps": total_steps,
        "passed_steps": passed_steps,
        "failed_steps": total_steps - passed_steps,
        "pass_rate": pass_rate,
        "total_duration_seconds": total_duration,
        "body_health_score": body_health_score,
        "speed_band": _speed_band(total_duration),
    }


def _resolve_benchmark_thresholds(
    profile: str,
    *,
    policy_profiles: Optional[Dict[str, Dict[str, float]]],
    min_pass_rate: Optional[float],
    max_duration_sec: Optional[float],
    min_health_score: Optional[float],
) -> Dict[str, float]:
    policy_defaults = (policy_profiles or {}).get(profile)
    defaults = policy_defaults or BENCHMARK_PROFILES.get(profile, BENCHMARK_PROFILES["standard"])
    return {
        "min_pass_rate": float(defaults["min_pass_rate"] if min_pass_rate is None else min_pass_rate),
        "max_duration_sec": float(defaults["max_duration_sec"] if max_duration_sec is None else max_duration_sec),
        "min_health_score": float(defaults["min_health_score"] if min_health_score is None else min_health_score),
    }


def _load_last_summary(history_path: Path) -> Optional[Dict[str, object]]:
    if not history_path.exists():
        return None
    last_nonempty = ""
    with history_path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                last_nonempty = line
    if not last_nonempty:
        return None
    try:
        parsed = json.loads(last_nonempty)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _evaluate_benchmark(
    summary: Dict[str, object],
    previous: Optional[Dict[str, object]],
    min_pass_rate: float,
    max_duration_sec: float,
    min_health_score: float,
) -> Dict[str, object]:
    pass_rate = float(summary["pass_rate"])
    duration = float(summary["total_duration_seconds"])
    health = float(summary["body_health_score"])
    checks = {
        "pass_rate": {"ok": pass_rate >= min_pass_rate, "actual": pass_rate, "threshold": min_pass_rate},
        "total_duration_seconds": {
            "ok": duration <= max_duration_sec,
            "actual": duration,
            "threshold": max_duration_sec,
        },
        "body_health_score": {
            "ok": health >= min_health_score,
            "actual": health,
            "threshold": min_health_score,
        },
    }
    status = "PASS" if all(item["ok"] for item in checks.values()) else "WARN"

    trend: Dict[str, object] = {"has_previous": previous is not None}
    if previous is not None:
        prev_duration = float(previous.get("total_duration_seconds", duration))
        prev_health = float(previous.get("body_health_score", health))
        duration_delta = round(duration - prev_duration, 6)
        health_delta = round(health - prev_health, 6)
        trend.update(
            {
                "previous_generated_utc": previous.get("generated_utc"),
                "duration_delta_seconds": duration_delta,
                "health_delta": health_delta,
            }
        )
        if duration_delta > 0.2 or health_delta < -2.0:
            trend["classification"] = "regression"
        elif duration_delta < -0.2 or health_delta > 2.0:
            trend["classification"] = "improvement"
        else:
            trend["classification"] = "stable"
    else:
        trend["classification"] = "baseline"

    return {"status": status, "checks": checks, "trend": trend}


def _build_markdown(
    generated_utc: str,
    overall_status: str,
    summary: Dict[str, object],
    benchmark: Dict[str, object],
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
        "## Benchmark guardrail",
        f"- status: **{benchmark['status']}**",
        f"- profile: `{benchmark.get('profile', 'standard')}`",
        f"- trend: `{benchmark['trend']['classification']}`",
        "```json",
        json.dumps(benchmark.get("thresholds", {}), indent=2),
        "```",
        "",
        "### check_results",
        "```json",
        json.dumps(benchmark["checks"], indent=2),
        "```",
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
    parser.add_argument(
        "--profile-policy",
        default="docs/body-profile-policy-v1.json",
        help="Optional profile policy JSON for benchmark threshold overrides.",
    )
    parser.add_argument(
        "--benchmark-profile",
        choices=("quick", "standard", "strict"),
        default="standard",
        help="Threshold preset for benchmark guardrail checks.",
    )
    parser.add_argument(
        "--benchmark-min-pass-rate",
        type=float,
        default=None,
        help="Override minimum pass_rate benchmark threshold.",
    )
    parser.add_argument(
        "--benchmark-max-duration-sec",
        type=float,
        default=None,
        help="Override maximum total_duration_seconds benchmark threshold.",
    )
    parser.add_argument(
        "--benchmark-min-health-score",
        type=float,
        default=None,
        help="Override minimum body_health_score benchmark threshold.",
    )
    parser.add_argument(
        "--latest-benchmark",
        default="docs/body-track-benchmark-latest.json",
        help="Path for latest benchmark guardrail status artifact.",
    )
    parser.add_argument(
        "--fail-on-benchmark",
        action="store_true",
        help="Exit non-zero if benchmark guardrail status is not PASS.",
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
    summary = _build_summary(generated_utc, stamp, steps)
    json_payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "summary": summary,
        "steps": [asdict(step) for step in steps],
    }

    timestamped_json = reports_dir / f"{stamp}-body-track-smoke.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-smoke.md"
    timestamped_metrics = reports_dir / f"{stamp}-body-track-metrics.json"

    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_metrics = Path(args.latest_metrics)
    latest_benchmark = Path(args.latest_benchmark)
    metrics_history = Path(args.metrics_history)

    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    latest_metrics.parent.mkdir(parents=True, exist_ok=True)
    latest_benchmark.parent.mkdir(parents=True, exist_ok=True)
    metrics_history.parent.mkdir(parents=True, exist_ok=True)

    previous_summary = _load_last_summary(metrics_history)
    policy_path = Path(args.profile_policy)
    policy_overrides = _load_profile_benchmark_overrides(policy_path)
    benchmark_thresholds = _resolve_benchmark_thresholds(
        args.benchmark_profile,
        policy_profiles=policy_overrides,
        min_pass_rate=args.benchmark_min_pass_rate,
        max_duration_sec=args.benchmark_max_duration_sec,
        min_health_score=args.benchmark_min_health_score,
    )
    benchmark = _evaluate_benchmark(
        summary=summary,
        previous=previous_summary,
        min_pass_rate=benchmark_thresholds["min_pass_rate"],
        max_duration_sec=benchmark_thresholds["max_duration_sec"],
        min_health_score=benchmark_thresholds["min_health_score"],
    )
    benchmark["profile"] = args.benchmark_profile
    benchmark["thresholds"] = benchmark_thresholds
    benchmark["policy_path"] = str(policy_path)
    benchmark["policy_override_used"] = args.benchmark_profile in policy_overrides
    summary["benchmark_profile"] = args.benchmark_profile
    summary["benchmark_status"] = benchmark["status"]
    summary["benchmark_trend"] = benchmark["trend"]["classification"]

    json_payload["benchmark"] = benchmark
    markdown = _build_markdown(generated_utc, overall_status, summary, benchmark, steps)

    timestamped_benchmark = reports_dir / f"{stamp}-body-track-benchmark.json"
    timestamped_json.write_text(json.dumps(json_payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    timestamped_metrics.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    timestamped_benchmark.write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")

    latest_json.write_text(json.dumps(json_payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    latest_metrics.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    latest_benchmark.write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")

    with metrics_history.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(summary) + "\n")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    print(f"timestamped_metrics={timestamped_metrics}")
    print(f"timestamped_benchmark={timestamped_benchmark}")
    print(f"latest_metrics={latest_metrics}")
    print(f"latest_benchmark={latest_benchmark}")
    print(f"metrics_history={metrics_history}")
    success = overall_status == "PASS"
    if args.fail_on_benchmark and benchmark["status"] != "PASS":
        success = False
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
