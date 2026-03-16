# Body Profile Calibration Report

- generated_utc: `2026-03-16T01:46:08+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `183`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.421 | 0.398 | loosen_duration+tighten_health | noisy |
| standard | 0.421 | 0.398 | loosen_duration+tighten_health | noisy |
| strict | 0.792 | 0.784 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284153`
- observed_false_regression_rate: `0.273224`
```json
{
  "duration_drift_p90": 1.108997,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.663 | 0.630 | noisy |
| 3 | 1 | 0.193 | 0.182 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.810 | 0.754 | noisy |
| 5 | 1 | 0.486 | 0.464 | noisy |
| 5 | 2 | 0.145 | 0.145 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.859 | 0.780 | noisy |
| 7 | 1 | 0.678 | 0.644 | noisy |
| 7 | 2 | 0.379 | 0.373 | noisy |
| 7 | 3 | 0.113 | 0.113 | acceptable |
| 9 | 0 | 0.886 | 0.783 | noisy |
| 9 | 1 | 0.783 | 0.737 | noisy |
| 9 | 2 | 0.543 | 0.526 | noisy |
| 9 | 3 | 0.326 | 0.326 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
