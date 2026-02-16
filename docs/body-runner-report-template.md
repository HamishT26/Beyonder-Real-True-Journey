# Body Runner Report Template

Use this template for each Body-track validation cycle.

---

## Metadata
- generated_utc:
- branch:
- commit:
- runner_version:
- overall_status: PASS/FAIL

## Summary metrics
- pass_rate:
- total_duration_seconds:
- body_health_score:
- speed_band:

## Benchmark guardrail
- status: PASS/WARN
- profile: quick/standard/strict
- trend: baseline/stable/improvement/regression
- checks:
  - pass_rate:
  - total_duration_seconds:
  - body_health_score:

## Trend guard window
- status: PASS/WARN
- trend_profile: quick/standard/strict
- trend_classification: stable_or_improving/watch/regression_pressure/insufficient_history
- window_size_used:
- checks:
  - latest_benchmark_status:
  - regression_count_window:
  - duration_drift_window:
  - health_drop_window:

## Profile calibration
- overall_status: PASS/WARN
- history_samples:
- benchmark_profile_analysis:
  - profile:
  - warn_rate:
  - false_alert_rate:
  - recommended_thresholds:
- trend_alert_analysis:
  - observed_regression_rate:
  - observed_false_regression_rate:
  - drift_percentiles:
    - duration_drift_p90:
    - health_drop_p90:
- regression_window_diagnostics:
  - recommended_window:
    - window_size:
    - max_regressions:
  - evaluated_windows:
    - window_size:
    - max_regressions:
    - alert_rate:
    - false_alert_rate:

## Steps
| step | status | returncode | duration_seconds | command | artifact |
|---|---|---:|---:|---|---|
| compile_python_modules |  |  |  |  |  |
| run_full_orchestrator_demo |  |  |  |  |  |
| run_gmut_simulation |  |  |  |  |  |

## Evidence boundaries
- confirmed_evidence:
- inference:
- open_gap:

## Next actions
1.
2.
3.
