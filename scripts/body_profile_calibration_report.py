#!/usr/bin/env python3
"""
Generate Body benchmark/trend profile calibration and false-alert statistics.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

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
            str(key): {str(k): float(v) for k, v in value.items() if isinstance(v, (int, float))}
            for key, value in profiles.items()
            if isinstance(value, dict)
        }
    return {}


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


def _percentile(values: Iterable[float], q: float) -> float:
    ordered = sorted(float(value) for value in values)
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return ordered[0]
    clamped = min(1.0, max(0.0, q))
    idx = clamped * (len(ordered) - 1)
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def _run_is_healthy(row: Dict[str, object]) -> bool:
    failed_steps = row.get("failed_steps")
    if isinstance(failed_steps, (int, float)):
        return float(failed_steps) <= 0.0
    return float(row.get("pass_rate", 0.0)) >= 1.0


def _benchmark_eval(row: Dict[str, object], thresholds: Dict[str, float]) -> Tuple[str, Dict[str, bool]]:
    pass_rate = float(row.get("pass_rate", 0.0))
    duration = float(row.get("total_duration_seconds", 0.0))
    health = float(row.get("body_health_score", 0.0))
    checks = {
        "pass_rate": pass_rate >= float(thresholds["min_pass_rate"]),
        "total_duration_seconds": duration <= float(thresholds["max_duration_sec"]),
        "body_health_score": health >= float(thresholds["min_health_score"]),
    }
    status = "PASS" if all(checks.values()) else "WARN"
    return status, checks


def _analyze_benchmark_profiles(
    rows: List[Dict[str, object]],
    target_false_alert_rate: float,
) -> List[Dict[str, object]]:
    analyses: List[Dict[str, object]] = []
    for profile_name, thresholds in BENCHMARK_PROFILES.items():
        warn_count = 0
        false_alert_count = 0
        healthy_count = 0
        warn_reasons = {"pass_rate": 0, "total_duration_seconds": 0, "body_health_score": 0}
        durations: List[float] = []
        healths: List[float] = []

        for row in rows:
            status, checks = _benchmark_eval(row, thresholds)
            healthy = _run_is_healthy(row)
            duration = float(row.get("total_duration_seconds", 0.0))
            health = float(row.get("body_health_score", 0.0))
            durations.append(duration)
            healths.append(health)
            if healthy:
                healthy_count += 1
            if status != "PASS":
                warn_count += 1
                for key, ok in checks.items():
                    if not ok:
                        warn_reasons[key] += 1
                if healthy:
                    false_alert_count += 1

        total = len(rows)
        warn_rate = (warn_count / total) if total else 0.0
        false_alert_rate = (false_alert_count / healthy_count) if healthy_count else 0.0

        recommended = {
            "min_pass_rate": 1.0,
            "max_duration_sec": round(_percentile(durations, 0.95) + 0.05, 3),
            "min_health_score": round(max(0.0, _percentile(healths, 0.05) - 0.5), 2),
        }
        actions = []
        if recommended["max_duration_sec"] > thresholds["max_duration_sec"]:
            actions.append("loosen_duration")
        elif recommended["max_duration_sec"] < thresholds["max_duration_sec"]:
            actions.append("tighten_duration")
        if recommended["min_health_score"] < thresholds["min_health_score"]:
            actions.append("loosen_health")
        elif recommended["min_health_score"] > thresholds["min_health_score"]:
            actions.append("tighten_health")
        action = "keep" if not actions else "+".join(actions)

        analyses.append(
            {
                "profile": profile_name,
                "thresholds": thresholds,
                "total_runs": total,
                "healthy_runs": healthy_count,
                "warn_count": warn_count,
                "warn_rate": round(warn_rate, 6),
                "false_alert_count": false_alert_count,
                "false_alert_rate": round(false_alert_rate, 6),
                "warn_reasons": warn_reasons,
                "recommended_thresholds": recommended,
                "recommendation_action": action,
                "quality": "acceptable" if false_alert_rate <= target_false_alert_rate else "noisy",
            }
        )
    return analyses


def _build_drift_vectors(rows: List[Dict[str, object]]) -> List[Dict[str, float]]:
    vectors: List[Dict[str, float]] = []
    if len(rows) < 2:
        return vectors
    for index in range(1, len(rows)):
        prev = rows[index - 1]
        curr = rows[index]
        prev_duration = float(prev.get("total_duration_seconds", 0.0))
        curr_duration = float(curr.get("total_duration_seconds", 0.0))
        prev_health = float(prev.get("body_health_score", 0.0))
        curr_health = float(curr.get("body_health_score", 0.0))
        vectors.append(
            {
                "duration_drift": curr_duration - prev_duration,
                "health_drop": prev_health - curr_health,
                "healthy": 1.0 if _run_is_healthy(curr) else 0.0,
            }
        )
    return vectors


def _analyze_trend_profiles(
    rows: List[Dict[str, object]],
    target_false_alert_rate: float,
) -> Dict[str, object]:
    trend_profiles = _load_trend_profiles()
    vectors = _build_drift_vectors(rows)
    positive_duration = [max(0.0, item["duration_drift"]) for item in vectors]
    positive_health_drop = [max(0.0, item["health_drop"]) for item in vectors]

    observed_regression_count = sum(
        1 for row in rows if str(row.get("benchmark_trend", "")).lower() == "regression"
    )
    observed_false_regression_count = sum(
        1
        for row in rows
        if str(row.get("benchmark_trend", "")).lower() == "regression" and _run_is_healthy(row)
    )
    observed_regression_rate = (observed_regression_count / len(rows)) if rows else 0.0
    observed_false_regression_rate = (
        observed_false_regression_count / len(rows)
    ) if rows else 0.0

    profile_estimates: List[Dict[str, object]] = []
    for profile_name, thresholds in trend_profiles.items():
        max_duration = float(thresholds.get("max_duration_drift", 0.0))
        max_health_drop = float(thresholds.get("max_health_drop", 0.0))
        exceed_count = 0
        false_exceed_count = 0
        for item in vectors:
            exceeded = (
                max(0.0, item["duration_drift"]) > max_duration
                or max(0.0, item["health_drop"]) > max_health_drop
            )
            if exceeded:
                exceed_count += 1
                if item["healthy"] >= 1.0:
                    false_exceed_count += 1
        total = len(vectors)
        exceed_rate = (exceed_count / total) if total else 0.0
        false_exceed_rate = (false_exceed_count / total) if total else 0.0
        profile_estimates.append(
            {
                "profile": profile_name,
                "thresholds": thresholds,
                "total_vectors": total,
                "drift_exceed_count": exceed_count,
                "drift_exceed_rate": round(exceed_rate, 6),
                "false_exceed_count": false_exceed_count,
                "false_exceed_rate": round(false_exceed_rate, 6),
                "quality": "acceptable" if false_exceed_rate <= target_false_alert_rate else "noisy",
            }
        )

    return {
        "observed_regression_count": observed_regression_count,
        "observed_regression_rate": round(observed_regression_rate, 6),
        "observed_false_regression_count": observed_false_regression_count,
        "observed_false_regression_rate": round(observed_false_regression_rate, 6),
        "drift_percentiles": {
            "duration_drift_p90": round(_percentile(positive_duration, 0.90), 6),
            "health_drop_p90": round(_percentile(positive_health_drop, 0.90), 6),
        },
        "profile_estimates": profile_estimates,
    }


def _analyze_regression_windows(
    rows: List[Dict[str, object]],
    target_false_alert_rate: float,
) -> Dict[str, object]:
    candidate_windows = [3, 5, 7, 9]
    candidate_max_regressions = [0, 1, 2, 3]
    if not rows:
        return {
            "evaluated_windows": [],
            "recommended_window": {"window_size": 5, "max_regressions": 1},
        }

    evaluated: List[Dict[str, object]] = []
    for window_size in candidate_windows:
        for max_regressions in candidate_max_regressions:
            evaluations = 0
            alerts = 0
            false_alerts = 0
            for index in range(window_size - 1, len(rows)):
                window = rows[index - window_size + 1 : index + 1]
                evaluations += 1
                regressions = sum(
                    1 for row in window if str(row.get("benchmark_trend", "")).lower() == "regression"
                )
                alert = regressions > max_regressions
                if alert:
                    alerts += 1
                    window_healthy = all(_run_is_healthy(row) for row in window)
                    if window_healthy:
                        false_alerts += 1
            alert_rate = (alerts / evaluations) if evaluations else 0.0
            false_alert_rate = (false_alerts / evaluations) if evaluations else 0.0
            evaluated.append(
                {
                    "window_size": window_size,
                    "max_regressions": max_regressions,
                    "evaluations": evaluations,
                    "alert_count": alerts,
                    "alert_rate": round(alert_rate, 6),
                    "false_alert_count": false_alerts,
                    "false_alert_rate": round(false_alert_rate, 6),
                    "quality": "acceptable" if false_alert_rate <= target_false_alert_rate else "noisy",
                }
            )

    ranked = sorted(
        evaluated,
        key=lambda item: (
            float(item["false_alert_rate"]),
            abs(float(item["alert_rate"]) - 0.2),
            int(item["window_size"]),
            int(item["max_regressions"]),
        ),
    )
    recommended = {
        "window_size": int(ranked[0]["window_size"]) if ranked else 5,
        "max_regressions": int(ranked[0]["max_regressions"]) if ranked else 1,
    }
    return {
        "evaluated_windows": evaluated,
        "recommended_window": recommended,
    }


def _recommend_defaults(
    benchmark_profiles: List[Dict[str, object]],
    trend_summary: Dict[str, object],
    regression_window_diagnostics: Dict[str, object],
) -> Dict[str, object]:
    benchmark_sorted = sorted(
        benchmark_profiles,
        key=lambda item: (
            float(item.get("false_alert_rate", 1.0)),
            float(item.get("warn_rate", 1.0)),
        ),
    )
    trend_sorted = sorted(
        trend_summary.get("profile_estimates", []),
        key=lambda item: (
            float(item.get("false_exceed_rate", 1.0)),
            float(item.get("drift_exceed_rate", 1.0)),
        ),
    )
    return {
        "recommended_benchmark_profile": benchmark_sorted[0]["profile"] if benchmark_sorted else "standard",
        "recommended_trend_profile": trend_sorted[0]["profile"] if trend_sorted else "standard",
        "recommended_regression_window": regression_window_diagnostics.get(
            "recommended_window",
            {"window_size": 5, "max_regressions": 1},
        ),
    }


def _current_profile_defaults(profile_context: str) -> Dict[str, object]:
    normalized = profile_context.strip().lower()
    if normalized == "quick":
        return {
            "benchmark_profile": "quick",
            "trend_profile": "quick",
            "regression_window": {"window_size": 3, "max_regressions": 1},
        }
    return {
        "benchmark_profile": "standard",
        "trend_profile": "standard",
        "regression_window": {"window_size": 5, "max_regressions": 2},
    }


def _lookup_profile_metric(rows: List[Dict[str, object]], profile: str, metric_key: str) -> float:
    for row in rows:
        if str(row.get("profile", "")) == profile:
            return float(row.get(metric_key, 0.0))
    return 0.0


def _lookup_window_false_alert(
    rows: List[Dict[str, object]],
    *,
    window_size: int,
    max_regressions: int,
) -> float:
    for row in rows:
        if (
            int(row.get("window_size", -1)) == int(window_size)
            and int(row.get("max_regressions", -1)) == int(max_regressions)
        ):
            return float(row.get("false_alert_rate", 0.0))
    return 0.0


def _build_policy_delta_analysis(
    *,
    profile_context: str,
    benchmark_profiles: List[Dict[str, object]],
    trend_summary: Dict[str, object],
    regression_window_diagnostics: Dict[str, object],
    recommendations: Dict[str, object],
) -> Dict[str, object]:
    current = _current_profile_defaults(profile_context)
    current_benchmark = str(current["benchmark_profile"])
    current_trend = str(current["trend_profile"])
    current_window = dict(current["regression_window"])

    recommended_benchmark = str(recommendations.get("recommended_benchmark_profile", current_benchmark))
    recommended_trend = str(recommendations.get("recommended_trend_profile", current_trend))
    recommended_window = dict(
        recommendations.get(
            "recommended_regression_window",
            current_window,
        )
    )

    current_benchmark_false_alert = _lookup_profile_metric(
        benchmark_profiles,
        current_benchmark,
        "false_alert_rate",
    )
    recommended_benchmark_false_alert = _lookup_profile_metric(
        benchmark_profiles,
        recommended_benchmark,
        "false_alert_rate",
    )

    trend_rows = trend_summary.get("profile_estimates", [])
    trend_rows_list = trend_rows if isinstance(trend_rows, list) else []
    current_trend_false_alert = _lookup_profile_metric(
        trend_rows_list,
        current_trend,
        "false_exceed_rate",
    )
    recommended_trend_false_alert = _lookup_profile_metric(
        trend_rows_list,
        recommended_trend,
        "false_exceed_rate",
    )

    window_rows = regression_window_diagnostics.get("evaluated_windows", [])
    window_rows_list = window_rows if isinstance(window_rows, list) else []
    current_window_false_alert = _lookup_window_false_alert(
        window_rows_list,
        window_size=int(current_window.get("window_size", 5)),
        max_regressions=int(current_window.get("max_regressions", 1)),
    )
    recommended_window_false_alert = _lookup_window_false_alert(
        window_rows_list,
        window_size=int(recommended_window.get("window_size", 5)),
        max_regressions=int(recommended_window.get("max_regressions", 1)),
    )

    benchmark_delta = round(recommended_benchmark_false_alert - current_benchmark_false_alert, 6)
    trend_delta = round(recommended_trend_false_alert - current_trend_false_alert, 6)
    window_delta = round(recommended_window_false_alert - current_window_false_alert, 6)
    aggregate_delta = round(benchmark_delta + trend_delta + window_delta, 6)

    apply_candidate = (
        benchmark_delta <= 0.0
        and trend_delta <= 0.0
        and window_delta <= 0.0
        and (benchmark_delta < 0.0 or trend_delta < 0.0 or window_delta < 0.0)
    )

    return {
        "current_policy": {
            "benchmark_profile": current_benchmark,
            "trend_profile": current_trend,
            "regression_window": current_window,
        },
        "recommended_policy": {
            "benchmark_profile": recommended_benchmark,
            "trend_profile": recommended_trend,
            "regression_window": recommended_window,
        },
        "false_alert_before_after": {
            "benchmark_before": round(current_benchmark_false_alert, 6),
            "benchmark_after": round(recommended_benchmark_false_alert, 6),
            "benchmark_delta": benchmark_delta,
            "trend_before": round(current_trend_false_alert, 6),
            "trend_after": round(recommended_trend_false_alert, 6),
            "trend_delta": trend_delta,
            "window_before": round(current_window_false_alert, 6),
            "window_after": round(recommended_window_false_alert, 6),
            "window_delta": window_delta,
            "aggregate_delta": aggregate_delta,
        },
        "apply_recommendation_candidate": apply_candidate,
    }


def _build_markdown(payload: Dict[str, object]) -> str:
    lines = [
        "# Body Profile Calibration Report",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- profile_context: `{payload['profile_context']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- history_samples: `{payload['history_samples']}`",
        "",
        "## Benchmark profile analysis",
        "| profile | warn_rate | false_alert_rate | recommendation_action | quality |",
        "|---|---:|---:|---|---|",
    ]
    for row in payload["benchmark_profile_analysis"]:
        lines.append(
            f"| {row['profile']} | {row['warn_rate']:.3f} | {row['false_alert_rate']:.3f} | "
            f"{row['recommendation_action']} | {row['quality']} |"
        )
    lines.extend(
        [
            "",
            "## Trend alert analysis",
            f"- observed_regression_rate: `{payload['trend_alert_analysis']['observed_regression_rate']}`",
            f"- observed_false_regression_rate: `{payload['trend_alert_analysis']['observed_false_regression_rate']}`",
            "```json",
            json.dumps(payload["trend_alert_analysis"]["drift_percentiles"], indent=2),
            "```",
            "",
            "## Regression window diagnostics",
            "| window_size | max_regressions | alert_rate | false_alert_rate | quality |",
            "|---:|---:|---:|---:|---|",
        ]
    )
    for row in payload["regression_window_diagnostics"]["evaluated_windows"]:
        lines.append(
            f"| {row['window_size']} | {row['max_regressions']} | {row['alert_rate']:.3f} | "
            f"{row['false_alert_rate']:.3f} | {row['quality']} |"
        )
    lines.extend(
        [
            "",
            "## Recommendations",
            "```json",
            json.dumps(payload["recommendations"], indent=2),
            "```",
            "",
            "## Policy delta analysis (before/after false-alert rates)",
            "```json",
            json.dumps(payload["policy_delta_analysis"], indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Body profile calibration report from rolling history.")
    parser.add_argument("--metrics-history", default="docs/body-track-metrics-history.jsonl")
    parser.add_argument("--reports-dir", default="docs/body-track-runs")
    parser.add_argument("--latest-json", default="docs/body-track-calibration-latest.json")
    parser.add_argument("--latest-md", default="docs/body-track-calibration-latest.md")
    parser.add_argument("--profile-context", choices=("quick", "standard", "deep", "mixed"), default="mixed")
    parser.add_argument("--target-false-alert-rate", type=float, default=0.15)
    parser.add_argument("--minimum-samples", type=int, default=5)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    history_rows = _read_history(Path(args.metrics_history))
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    benchmark_profiles = _analyze_benchmark_profiles(history_rows, args.target_false_alert_rate)
    trend_summary = _analyze_trend_profiles(history_rows, args.target_false_alert_rate)
    regression_window_diagnostics = _analyze_regression_windows(history_rows, args.target_false_alert_rate)
    recommendations = _recommend_defaults(benchmark_profiles, trend_summary, regression_window_diagnostics)
    policy_delta_analysis = _build_policy_delta_analysis(
        profile_context=args.profile_context,
        benchmark_profiles=benchmark_profiles,
        trend_summary=trend_summary,
        regression_window_diagnostics=regression_window_diagnostics,
        recommendations=recommendations,
    )

    status = "PASS"
    if len(history_rows) < max(1, args.minimum_samples):
        status = "WARN"
    if any(item.get("quality") == "noisy" for item in benchmark_profiles):
        status = "WARN"
    if any(item.get("quality") == "noisy" for item in trend_summary.get("profile_estimates", [])):
        status = "WARN"
    if any(
        item.get("quality") == "noisy"
        for item in regression_window_diagnostics.get("evaluated_windows", [])
        if int(item.get("window_size", 0)) in {3, 5, 7}
    ):
        status = "WARN"

    payload: Dict[str, object] = {
        "generated_utc": generated_utc,
        "overall_status": status,
        "profile_context": args.profile_context,
        "target_false_alert_rate": args.target_false_alert_rate,
        "history_samples": len(history_rows),
        "benchmark_profile_analysis": benchmark_profiles,
        "trend_alert_analysis": trend_summary,
        "regression_window_diagnostics": regression_window_diagnostics,
        "recommendations": recommendations,
        "policy_delta_analysis": policy_delta_analysis,
    }

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-body-track-calibration.json"
    timestamped_md = reports_dir / f"{stamp}-body-track-calibration.md"
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
