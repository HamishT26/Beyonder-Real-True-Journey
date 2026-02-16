#!/usr/bin/env python3
"""
Body benchmark trend guard.

Consumes Body benchmark + metrics history artifacts and emits a trend guard
status that can be used in suite orchestration.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Dict, List, Tuple


TREND_GUARD_PROFILES: Dict[str, Dict[str, float]] = {
    "quick": {
        "window_size": 3.0,
        "max_regressions": 1.0,
        "max_duration_drift": 0.25,
        "max_health_drop": 2.5,
    },
    "standard": {
        "window_size": 5.0,
        "max_regressions": 2.0,
        "max_duration_drift": 0.2,
        "max_health_drop": 2.0,
    },
    "strict": {
        "window_size": 7.0,
        "max_regressions": 1.0,
        "max_duration_drift": 0.12,
        "max_health_drop": 1.0,
    },
}


def _read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_history(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        return []
    rows: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


def _build_markdown(generated_utc: str, payload: Dict[str, object]) -> str:
    lines = [
        "# Body Benchmark Trend Guard Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- trend_profile: `{payload.get('trend_profile', 'standard')}`",
        f"- trend_classification: `{payload['trend_classification']}`",
        f"- window_size_used: `{payload['window_size_used']}`",
        "",
        "## Thresholds",
        "```json",
        json.dumps(payload.get("thresholds", {}), indent=2),
        "```",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['check']} | {check['status']} | {check['detail']} |")
    return "\n".join(lines).strip() + "\n"


def _check(name: str, ok: bool, detail: str) -> Dict[str, str]:
    return {"check": name, "status": "PASS" if ok else "WARN", "detail": detail}


def _resolve_guard_thresholds(
    trend_profile: str,
    *,
    window_size: int | None,
    max_regressions: int | None,
    max_duration_drift: float | None,
    max_health_drop: float | None,
) -> Dict[str, float]:
    defaults = TREND_GUARD_PROFILES.get(trend_profile, TREND_GUARD_PROFILES["standard"])
    return {
        "window_size": float(defaults["window_size"] if window_size is None else window_size),
        "max_regressions": float(defaults["max_regressions"] if max_regressions is None else max_regressions),
        "max_duration_drift": float(
            defaults["max_duration_drift"] if max_duration_drift is None else max_duration_drift
        ),
        "max_health_drop": float(defaults["max_health_drop"] if max_health_drop is None else max_health_drop),
    }


def _evaluate(
    benchmark: Dict[str, object],
    history: List[Dict[str, object]],
    window_size: int,
    max_regressions: int,
    max_duration_drift: float,
    max_health_drop: float,
) -> Tuple[str, str, List[Dict[str, str]], int]:
    checks: List[Dict[str, str]] = []
    benchmark_status = str(benchmark.get("status", "WARN"))
    checks.append(
        _check(
            "latest_benchmark_status",
            benchmark_status == "PASS",
            f"status={benchmark_status}",
        )
    )

    if not history:
        checks.append(_check("history_exists", False, "no metrics history entries found"))
        return "WARN", "insufficient_history", checks, 0

    window = history[-window_size:]
    window_len = len(window)
    checks.append(_check("history_window_available", window_len >= 2, f"window_len={window_len}"))

    regressions = sum(1 for row in window if str(row.get("benchmark_trend", "")).lower() == "regression")
    checks.append(
        _check(
            "regression_count_window",
            regressions <= max_regressions,
            f"regressions={regressions}, max={max_regressions}",
        )
    )

    duration_values = [float(row.get("total_duration_seconds", 0.0)) for row in window]
    health_values = [float(row.get("body_health_score", 0.0)) for row in window]
    latest_duration = duration_values[-1]
    latest_health = health_values[-1]

    if window_len >= 2:
        prev_duration_med = median(duration_values[:-1])
        prev_health_med = median(health_values[:-1])
        duration_drift = latest_duration - prev_duration_med
        health_drop = prev_health_med - latest_health
    else:
        duration_drift = 0.0
        health_drop = 0.0

    checks.append(
        _check(
            "duration_drift_window",
            duration_drift <= max_duration_drift,
            f"drift={duration_drift:.6f}, max={max_duration_drift}",
        )
    )
    checks.append(
        _check(
            "health_drop_window",
            health_drop <= max_health_drop,
            f"drop={health_drop:.6f}, max={max_health_drop}",
        )
    )

    overall_status = "PASS" if all(check["status"] == "PASS" for check in checks) else "WARN"
    if overall_status == "PASS":
        trend = "stable_or_improving"
    elif regressions > max_regressions:
        trend = "regression_pressure"
    else:
        trend = "watch"
    return overall_status, trend, checks, window_len


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Body benchmark trend guard status.")
    parser.add_argument("--latest-benchmark", default="docs/body-track-benchmark-latest.json")
    parser.add_argument("--metrics-history", default="docs/body-track-metrics-history.jsonl")
    parser.add_argument("--reports-dir", default="docs/body-track-runs")
    parser.add_argument("--latest-json", default="docs/body-track-trend-guard-latest.json")
    parser.add_argument("--latest-md", default="docs/body-track-trend-guard-latest.md")
    parser.add_argument("--trend-profile", choices=("quick", "standard", "strict"), default="standard")
    parser.add_argument("--window-size", type=int, default=None)
    parser.add_argument("--max-regressions", type=int, default=None)
    parser.add_argument("--max-duration-drift", type=float, default=None)
    parser.add_argument("--max-health-drop", type=float, default=None)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    benchmark_path = Path(args.latest_benchmark)
    history_path = Path(args.metrics_history)
    if not benchmark_path.exists():
        raise SystemExit(f"Missing benchmark artifact: {benchmark_path}")

    benchmark = _read_json(benchmark_path)
    history = _read_history(history_path)
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    thresholds = _resolve_guard_thresholds(
        args.trend_profile,
        window_size=args.window_size,
        max_regressions=args.max_regressions,
        max_duration_drift=args.max_duration_drift,
        max_health_drop=args.max_health_drop,
    )

    overall_status, trend, checks, window_len = _evaluate(
        benchmark=benchmark,
        history=history,
        window_size=max(1, int(thresholds["window_size"])),
        max_regressions=max(0, int(thresholds["max_regressions"])),
        max_duration_drift=max(0.0, float(thresholds["max_duration_drift"])),
        max_health_drop=max(0.0, float(thresholds["max_health_drop"])),
    )

    payload: Dict[str, object] = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "trend_profile": args.trend_profile,
        "thresholds": thresholds,
        "trend_classification": trend,
        "window_size_used": window_len,
        "checks": checks,
    }
    markdown = _build_markdown(generated_utc, payload)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json = reports_dir / f"{stamp}-body-track-trend-guard.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-trend-guard.md"
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")

    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
