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
