#!/usr/bin/env python3
"""
Apply Body calibration recommendations selectively and report deltas.

This stage compares current policy vs recommended thresholds/window settings and
only applies updates when false-alert behavior improves (or warn-rate improves
with no false-alert regression).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from body_track_runner import BENCHMARK_PROFILES


def _load_trend_profiles() -> Dict[str, Dict[str, float]]:
    guard_path = Path(__file__).resolve().parent / "body_benchmark_trend_guard.py"
    spec = importlib.util.spec_from_file_location("body_benchmark_trend_guard", guard_path)
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    profiles = getattr(module, "TREND_GUARD_PROFILES", {})
    if isinstance(profiles, dict):
        return {
            str(name): {
                "window_size": float(values.get("window_size", 5.0)),
                "max_regressions": float(values.get("max_regressions", 2.0)),
                "max_duration_drift": float(values.get("max_duration_drift", 0.2)),
                "max_health_drop": float(values.get("max_health_drop", 2.0)),
            }
            for name, values in profiles.items()
            if isinstance(values, dict)
        }
    return {}


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
        "warn_rate": float(round(warn_rate, 6)),
        "false_alert_count": float(false_alert_count),
        "false_alert_rate": float(round(false_alert_rate, 6)),
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
        "alert_rate": float(round(alert_rate, 6)),
        "false_alert_count": float(false_alerts),
        "false_alert_rate": float(round(false_alert_rate, 6)),
    }


def _default_policy() -> Dict[str, object]:
    return {
        "policy_version": "v1",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "auto-default",
        "benchmark_profiles": {name: dict(values) for name, values in BENCHMARK_PROFILES.items()},
        "trend_profiles": _load_trend_profiles(),
        "regression_window_policy": {"window_size": 5, "max_regressions": 2},
    }


def _load_policy(path: Path) -> Dict[str, object]:
    payload = _read_json(path)
    if not payload:
        return _default_policy()
    baseline = _default_policy()
    baseline.update(payload)
    if not isinstance(baseline.get("benchmark_profiles"), dict):
        baseline["benchmark_profiles"] = _default_policy()["benchmark_profiles"]
    if not isinstance(baseline.get("trend_profiles"), dict):
        baseline["trend_profiles"] = _default_policy()["trend_profiles"]
    if not isinstance(baseline.get("regression_window_policy"), dict):
        baseline["regression_window_policy"] = {"window_size": 5, "max_regressions": 2}
    return baseline


def _lookup_recommended_thresholds(calibration: Dict[str, object], profile: str) -> Dict[str, float] | None:
    rows = calibration.get("benchmark_profile_analysis", [])
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("profile", "")) != profile:
            continue
        recommended = row.get("recommended_thresholds", {})
        if not isinstance(recommended, dict):
            return None
        try:
            return {
                "min_pass_rate": float(recommended["min_pass_rate"]),
                "max_duration_sec": float(recommended["max_duration_sec"]),
                "min_health_score": float(recommended["min_health_score"]),
            }
        except (KeyError, TypeError, ValueError):
            return None
    return None


def _should_apply_benchmark_update(
    before: Dict[str, float],
    after: Dict[str, float],
    *,
    min_false_alert_gain: float,
    max_warn_rate_increase: float,
) -> bool:
    false_gain = float(before["false_alert_rate"]) - float(after["false_alert_rate"])
    warn_delta = float(after["warn_rate"]) - float(before["warn_rate"])
    if false_gain > min_false_alert_gain and warn_delta <= max_warn_rate_increase:
        return True
    if abs(false_gain) <= 1e-12 and warn_delta < -1e-12:
        return True
    return False


def _should_apply_window_update(
    before: Dict[str, float],
    after: Dict[str, float],
    *,
    min_false_alert_gain: float,
    max_alert_rate_increase: float,
) -> bool:
    false_gain = float(before["false_alert_rate"]) - float(after["false_alert_rate"])
    alert_delta = float(after["alert_rate"]) - float(before["alert_rate"])
    if false_gain > min_false_alert_gain and alert_delta <= max_alert_rate_increase:
        return True
    return False


def _build_markdown(payload: Dict[str, object]) -> str:
    lines = [
        "# Body Profile Policy Delta Report",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- apply_mode: `{payload['apply_mode']}`",
        f"- policy_updated: `{payload['policy_updated']}`",
        f"- history_samples: `{payload['history_samples']}`",
        "",
        "## Benchmark profile deltas",
        "| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in payload["benchmark_deltas"]:
        lines.append(
            f"| {row['profile']} | {row['before']['warn_rate']:.3f} | {row['after']['warn_rate']:.3f} | "
            f"{row['before']['false_alert_rate']:.3f} | {row['after']['false_alert_rate']:.3f} | {row['action']} |"
        )
    window_before = payload["regression_window_delta"]["before"]
    window_after = payload["regression_window_delta"]["after"]
    lines.extend(
        [
            "",
            "## Regression window delta",
            "| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |",
            "|---|---|---:|---:|---:|---:|---|",
            (
                f"| {payload['regression_window_delta']['before_window']} | "
                f"{payload['regression_window_delta']['after_window']} | "
                f"{window_before['alert_rate']:.3f} | {window_after['alert_rate']:.3f} | "
                f"{window_before['false_alert_rate']:.3f} | {window_after['false_alert_rate']:.3f} | "
                f"{payload['regression_window_delta']['action']} |"
            ),
            "",
            "## Selected updates",
            "```json",
            json.dumps(payload["selected_updates"], indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Body policy updates selectively and report delta.")
    parser.add_argument("--metrics-history", default="docs/body-track-metrics-history.jsonl")
    parser.add_argument("--calibration-json", default="docs/body-track-calibration-latest.json")
    parser.add_argument("--policy-json", default="docs/body-profile-policy-v1.json")
    parser.add_argument("--reports-dir", default="docs/body-track-runs")
    parser.add_argument("--latest-json", default="docs/body-track-policy-delta-latest.json")
    parser.add_argument("--latest-md", default="docs/body-track-policy-delta-latest.md")
    parser.add_argument("--target-false-alert-rate", type=float, default=0.15)
    parser.add_argument("--minimum-samples", type=int, default=5)
    parser.add_argument("--min-false-alert-gain", type=float, default=0.001)
    parser.add_argument("--max-warn-rate-increase", type=float, default=0.02)
    parser.add_argument("--max-alert-rate-increase", type=float, default=0.05)
    parser.add_argument("--apply", action="store_true", help="Write selected updates to policy JSON.")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    history_rows = _read_history(Path(args.metrics_history))
    calibration = _read_json(Path(args.calibration_json))
    policy_path = Path(args.policy_json)
    policy = _load_policy(policy_path)
    benchmark_profiles = policy.get("benchmark_profiles", {})
    if not isinstance(benchmark_profiles, dict):
        benchmark_profiles = {}
    regression_policy = policy.get("regression_window_policy", {})
    if not isinstance(regression_policy, dict):
        regression_policy = {"window_size": 5, "max_regressions": 2}

    benchmark_deltas: List[Dict[str, object]] = []
    selected_benchmark_updates: Dict[str, Dict[str, float]] = {}

    for profile, threshold_values in benchmark_profiles.items():
        if not isinstance(threshold_values, dict):
            continue
        try:
            current_thresholds = {
                "min_pass_rate": float(threshold_values["min_pass_rate"]),
                "max_duration_sec": float(threshold_values["max_duration_sec"]),
                "min_health_score": float(threshold_values["min_health_score"]),
            }
        except (KeyError, TypeError, ValueError):
            continue

        recommended = _lookup_recommended_thresholds(calibration, str(profile))
        candidate_thresholds = recommended or current_thresholds
        before_metrics = _benchmark_metrics(history_rows, current_thresholds)
        after_metrics = _benchmark_metrics(history_rows, candidate_thresholds)

        action = "keep"
        if recommended is not None and _should_apply_benchmark_update(
            before_metrics,
            after_metrics,
            min_false_alert_gain=max(0.0, args.min_false_alert_gain),
            max_warn_rate_increase=max(0.0, args.max_warn_rate_increase),
        ):
            action = "apply_recommended_thresholds"
            selected_benchmark_updates[str(profile)] = candidate_thresholds
        benchmark_deltas.append(
            {
                "profile": str(profile),
                "before": before_metrics,
                "after": after_metrics,
                "before_thresholds": current_thresholds,
                "candidate_thresholds": candidate_thresholds,
                "action": action,
            }
        )

    try:
        current_window = {
            "window_size": int(float(regression_policy.get("window_size", 5))),
            "max_regressions": int(float(regression_policy.get("max_regressions", 2))),
        }
    except (TypeError, ValueError):
        current_window = {"window_size": 5, "max_regressions": 2}
    recommended_window_raw = calibration.get("recommendations", {}).get("recommended_regression_window", {})
    recommended_window = current_window
    if isinstance(recommended_window_raw, dict):
        try:
            recommended_window = {
                "window_size": int(float(recommended_window_raw["window_size"])),
                "max_regressions": int(float(recommended_window_raw["max_regressions"])),
            }
        except (KeyError, TypeError, ValueError):
            recommended_window = current_window

    window_before_metrics = _regression_window_metrics(
        history_rows,
        window_size=max(1, int(current_window["window_size"])),
        max_regressions=max(0, int(current_window["max_regressions"])),
    )
    window_after_metrics = _regression_window_metrics(
        history_rows,
        window_size=max(1, int(recommended_window["window_size"])),
        max_regressions=max(0, int(recommended_window["max_regressions"])),
    )
    regression_action = "keep"
    selected_window_update: Dict[str, int] | None = None
    if _should_apply_window_update(
        window_before_metrics,
        window_after_metrics,
        min_false_alert_gain=max(0.0, args.min_false_alert_gain),
        max_alert_rate_increase=max(0.0, args.max_alert_rate_increase),
    ):
        regression_action = "apply_recommended_window"
        selected_window_update = recommended_window

    policy_updated = False
    if args.apply:
        updated_policy = dict(policy)
        updated_profiles: Dict[str, Dict[str, float]] = {}
        for profile, thresholds in benchmark_profiles.items():
            if not isinstance(thresholds, dict):
                continue
            update = selected_benchmark_updates.get(str(profile))
            if update is not None:
                updated_profiles[str(profile)] = update
            else:
                try:
                    updated_profiles[str(profile)] = {
                        "min_pass_rate": float(thresholds["min_pass_rate"]),
                        "max_duration_sec": float(thresholds["max_duration_sec"]),
                        "min_health_score": float(thresholds["min_health_score"]),
                    }
                except (KeyError, TypeError, ValueError):
                    continue
        updated_policy["benchmark_profiles"] = updated_profiles
        if selected_window_update is not None:
            updated_policy["regression_window_policy"] = selected_window_update
        updated_policy["generated_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        updated_policy["source"] = "selective_calibration_application"
        policy_path.parent.mkdir(parents=True, exist_ok=True)
        policy_path.write_text(json.dumps(updated_policy, indent=2) + "\n", encoding="utf-8")
        policy_updated = bool(selected_benchmark_updates) or selected_window_update is not None

    status = "PASS"
    if len(history_rows) < max(1, args.minimum_samples):
        status = "WARN"

    payload: Dict[str, object] = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": status,
        "apply_mode": bool(args.apply),
        "policy_updated": policy_updated,
        "policy_path": str(policy_path),
        "history_samples": len(history_rows),
        "target_false_alert_rate": args.target_false_alert_rate,
        "benchmark_deltas": benchmark_deltas,
        "regression_window_delta": {
            "before_window": current_window,
            "after_window": recommended_window,
            "before": window_before_metrics,
            "after": window_after_metrics,
            "action": regression_action,
        },
        "selected_updates": {
            "benchmark_profiles": selected_benchmark_updates,
            "regression_window_policy": selected_window_update,
        },
    }

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-body-track-policy-delta.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-policy-delta.md"
    markdown = _build_markdown(payload)

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
