#!/usr/bin/env python3
"""
Produce a stressed-window Body policy delta report.

This script synthesizes deterministic noisy benchmark windows to estimate
before/after policy behavior under non-ideal conditions.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _read_json(path: Path) -> Dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    return payload if isinstance(payload, dict) else {}


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


def _run_is_healthy(row: Dict[str, object]) -> bool:
    failed_steps = row.get("failed_steps")
    if isinstance(failed_steps, (int, float)):
        return float(failed_steps) <= 0.0
    return float(row.get("pass_rate", 0.0)) >= 1.0


def _as_thresholds(raw: Dict[str, object]) -> Dict[str, float] | None:
    try:
        return {
            "min_pass_rate": float(raw["min_pass_rate"]),
            "max_duration_sec": float(raw["max_duration_sec"]),
            "min_health_score": float(raw["min_health_score"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


def _benchmark_metrics(rows: List[Dict[str, object]], thresholds: Dict[str, float]) -> Dict[str, float]:
    warn_count = 0
    false_alert_count = 0
    healthy_count = 0
    for row in rows:
        healthy = _run_is_healthy(row)
        if healthy:
            healthy_count += 1
        pass_rate_ok = float(row.get("pass_rate", 0.0)) >= float(thresholds["min_pass_rate"])
        duration_ok = float(row.get("total_duration_seconds", 0.0)) <= float(thresholds["max_duration_sec"])
        health_ok = float(row.get("body_health_score", 0.0)) >= float(thresholds["min_health_score"])
        status_ok = pass_rate_ok and duration_ok and health_ok
        if not status_ok:
            warn_count += 1
            if healthy:
                false_alert_count += 1

    total = len(rows)
    warn_rate = (warn_count / total) if total else 0.0
    false_alert_rate = (false_alert_count / healthy_count) if healthy_count else 0.0
    return {
        "total_runs": float(total),
        "healthy_runs": float(healthy_count),
        "warn_count": float(warn_count),
        "warn_rate": round(warn_rate, 6),
        "false_alert_count": float(false_alert_count),
        "false_alert_rate": round(false_alert_rate, 6),
    }


def _regression_window_metrics(
    rows: List[Dict[str, object]],
    *,
    window_size: int,
    max_regressions: int,
) -> Dict[str, float]:
    if not rows or window_size <= 0:
        return {
            "evaluations": 0.0,
            "alert_count": 0.0,
            "alert_rate": 0.0,
            "false_alert_count": 0.0,
            "false_alert_rate": 0.0,
        }
    evaluations = 0
    alerts = 0
    false_alerts = 0
    for idx in range(window_size - 1, len(rows)):
        window = rows[idx - window_size + 1 : idx + 1]
        evaluations += 1
        regressions = sum(1 for row in window if str(row.get("benchmark_trend", "")).lower() == "regression")
        alert = regressions > max_regressions
        if alert:
            alerts += 1
            if all(_run_is_healthy(row) for row in window):
                false_alerts += 1
    alert_rate = (alerts / evaluations) if evaluations else 0.0
    false_alert_rate = (false_alerts / evaluations) if evaluations else 0.0
    return {
        "evaluations": float(evaluations),
        "alert_count": float(alerts),
        "alert_rate": round(alert_rate, 6),
        "false_alert_count": float(false_alerts),
        "false_alert_rate": round(false_alert_rate, 6),
    }


def _recommended_thresholds(calibration: Dict[str, object], profile: str) -> Dict[str, float] | None:
    rows = calibration.get("benchmark_profile_analysis", [])
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("profile", "")) != profile:
            continue
        candidate = row.get("recommended_thresholds", {})
        if isinstance(candidate, dict):
            return _as_thresholds(candidate)
    return None


def _make_stressed_rows(
    source_rows: List[Dict[str, object]],
    *,
    scenario_length: int,
    duration_step: float,
    health_step: float,
    periodic_duration_spike: float,
    periodic_health_drop: float,
) -> List[Dict[str, object]]:
    baseline = source_rows[-1] if source_rows else {}
    base_duration = float(baseline.get("total_duration_seconds", 0.2))
    base_health = float(baseline.get("body_health_score", 100.0))
    stressed: List[Dict[str, object]] = []
    for index in range(max(1, scenario_length)):
        row: Dict[str, object] = {
            "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "pass_rate": 1.0,
            "failed_steps": 0,
        }
        duration = base_duration + (duration_step * index)
        health = base_health - (health_step * index)
        if index % 3 == 1:
            duration += periodic_duration_spike
            health -= periodic_health_drop
            row["benchmark_trend"] = "regression"
        elif index % 5 == 0 and index > 0:
            duration += periodic_duration_spike * 0.7
            health -= periodic_health_drop * 0.8
            row["benchmark_trend"] = "regression"
        else:
            row["benchmark_trend"] = "stable"

        row["total_duration_seconds"] = round(max(0.0, duration), 6)
        row["body_health_score"] = round(max(0.0, min(100.0, health)), 2)
        stressed.append(row)
    return stressed


def _build_markdown(payload: Dict[str, object]) -> str:
    lines = [
        "# Body Policy Stress-Window Delta Report",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- history_samples: `{payload['history_samples']}`",
        f"- stressed_samples: `{payload['stressed_samples']}`",
        "",
        "## Benchmark profile stressed deltas",
        "| profile | before_warn | after_warn | before_false_alert | after_false_alert | false_alert_delta | warn_rate_delta |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["benchmark_stress_deltas"]:
        lines.append(
            f"| {row['profile']} | {row['before']['warn_rate']:.3f} | {row['after']['warn_rate']:.3f} | "
            f"{row['before']['false_alert_rate']:.3f} | {row['after']['false_alert_rate']:.3f} | "
            f"{row['false_alert_rate_delta']:.3f} | {row['warn_rate_delta']:.3f} |"
        )

    window = payload["regression_window_stress_delta"]
    lines.extend(
        [
            "",
            "## Regression-window stressed delta",
            "| before_window | after_window | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | false_alert_delta |",
            "|---|---|---:|---:|---:|---:|---:|",
            (
                f"| {window['before_window']} | {window['after_window']} | "
                f"{window['before']['alert_rate']:.3f} | {window['after']['alert_rate']:.3f} | "
                f"{window['before']['false_alert_rate']:.3f} | {window['after']['false_alert_rate']:.3f} | "
                f"{window['false_alert_rate_delta']:.3f} |"
            ),
            "",
            "## Scenario parameters",
            "```json",
            json.dumps(payload["scenario_parameters"], indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate stressed-window Body policy delta analysis.")
    parser.add_argument("--metrics-history", default="docs/body-track-metrics-history.jsonl")
    parser.add_argument("--calibration-json", default="docs/body-track-calibration-latest.json")
    parser.add_argument("--policy-json", default="docs/body-profile-policy-v1.json")
    parser.add_argument("--reports-dir", default="docs/body-track-runs")
    parser.add_argument("--latest-json", default="docs/body-track-policy-stress-latest.json")
    parser.add_argument("--latest-md", default="docs/body-track-policy-stress-latest.md")
    parser.add_argument("--scenario-length", type=int, default=12)
    parser.add_argument("--duration-step", type=float, default=0.08)
    parser.add_argument("--health-step", type=float, default=0.35)
    parser.add_argument("--periodic-duration-spike", type=float, default=0.55)
    parser.add_argument("--periodic-health-drop", type=float, default=2.4)
    parser.add_argument("--minimum-samples", type=int, default=5)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    history_rows = _read_history(Path(args.metrics_history))
    calibration = _read_json(Path(args.calibration_json))
    policy = _read_json(Path(args.policy_json))
    policy_profiles = policy.get("benchmark_profiles", {})
    if not isinstance(policy_profiles, dict):
        policy_profiles = {}
    policy_window = policy.get("regression_window_policy", {})
    if not isinstance(policy_window, dict):
        policy_window = {"window_size": 5, "max_regressions": 2}

    stressed_rows = _make_stressed_rows(
        history_rows,
        scenario_length=max(1, args.scenario_length),
        duration_step=max(0.0, args.duration_step),
        health_step=max(0.0, args.health_step),
        periodic_duration_spike=max(0.0, args.periodic_duration_spike),
        periodic_health_drop=max(0.0, args.periodic_health_drop),
    )

    benchmark_stress_deltas: List[Dict[str, object]] = []
    non_zero_deltas = 0
    for profile, raw in policy_profiles.items():
        if not isinstance(raw, dict):
            continue
        current = _as_thresholds(raw)
        if current is None:
            continue
        candidate = _recommended_thresholds(calibration, str(profile)) or current
        before = _benchmark_metrics(stressed_rows, current)
        after = _benchmark_metrics(stressed_rows, candidate)
        false_delta = round(float(after["false_alert_rate"]) - float(before["false_alert_rate"]), 6)
        warn_delta = round(float(after["warn_rate"]) - float(before["warn_rate"]), 6)
        if abs(false_delta) > 0.0 or abs(warn_delta) > 0.0:
            non_zero_deltas += 1
        benchmark_stress_deltas.append(
            {
                "profile": str(profile),
                "before_thresholds": current,
                "candidate_thresholds": candidate,
                "before": before,
                "after": after,
                "false_alert_rate_delta": false_delta,
                "warn_rate_delta": warn_delta,
            }
        )

    try:
        before_window = {
            "window_size": int(float(policy_window.get("window_size", 5))),
            "max_regressions": int(float(policy_window.get("max_regressions", 2))),
        }
    except (TypeError, ValueError):
        before_window = {"window_size": 5, "max_regressions": 2}

    rec_window_raw = calibration.get("recommendations", {}).get("recommended_regression_window", {})
    if isinstance(rec_window_raw, dict):
        try:
            after_window = {
                "window_size": int(float(rec_window_raw.get("window_size", before_window["window_size"]))),
                "max_regressions": int(float(rec_window_raw.get("max_regressions", before_window["max_regressions"]))),
            }
        except (TypeError, ValueError):
            after_window = dict(before_window)
    else:
        after_window = dict(before_window)

    window_before = _regression_window_metrics(
        stressed_rows,
        window_size=max(1, before_window["window_size"]),
        max_regressions=max(0, before_window["max_regressions"]),
    )
    window_after = _regression_window_metrics(
        stressed_rows,
        window_size=max(1, after_window["window_size"]),
        max_regressions=max(0, after_window["max_regressions"]),
    )
    window_false_delta = round(float(window_after["false_alert_rate"]) - float(window_before["false_alert_rate"]), 6)
    if abs(window_false_delta) > 0.0:
        non_zero_deltas += 1

    status = "PASS"
    if len(history_rows) < max(1, args.minimum_samples):
        status = "WARN"

    payload: Dict[str, object] = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": status,
        "history_samples": len(history_rows),
        "stressed_samples": len(stressed_rows),
        "non_zero_delta_count": non_zero_deltas,
        "benchmark_stress_deltas": benchmark_stress_deltas,
        "regression_window_stress_delta": {
            "before_window": before_window,
            "after_window": after_window,
            "before": window_before,
            "after": window_after,
            "false_alert_rate_delta": window_false_delta,
            "alert_rate_delta": round(float(window_after["alert_rate"]) - float(window_before["alert_rate"]), 6),
        },
        "scenario_parameters": {
            "scenario_length": max(1, args.scenario_length),
            "duration_step": max(0.0, args.duration_step),
            "health_step": max(0.0, args.health_step),
            "periodic_duration_spike": max(0.0, args.periodic_duration_spike),
            "periodic_health_drop": max(0.0, args.periodic_health_drop),
        },
    }
    markdown = _build_markdown(payload)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-body-track-policy-stress.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-policy-stress.md"

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")

    if args.fail_on_warn and status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
