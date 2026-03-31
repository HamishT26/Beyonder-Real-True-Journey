# Body Profile Calibration Report

- generated_utc: `2026-03-31T03:06:36+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `342`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.637 | 0.630 | loosen_duration+tighten_health | noisy |
| standard | 0.637 | 0.630 | loosen_duration+tighten_health | noisy |
| strict | 0.889 | 0.887 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.330409`
- observed_false_regression_rate: `0.324561`
```json
{
  "duration_drift_p90": 1.562282,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.741 | 0.724 | noisy |
| 3 | 1 | 0.238 | 0.232 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.879 | 0.849 | noisy |
| 5 | 1 | 0.580 | 0.568 | noisy |
| 5 | 2 | 0.192 | 0.192 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.920 | 0.878 | noisy |
| 7 | 1 | 0.768 | 0.750 | noisy |
| 7 | 2 | 0.482 | 0.479 | noisy |
| 7 | 3 | 0.149 | 0.149 | acceptable |
| 9 | 0 | 0.940 | 0.886 | noisy |
| 9 | 1 | 0.865 | 0.841 | noisy |
| 9 | 2 | 0.662 | 0.653 | noisy |
| 9 | 3 | 0.398 | 0.398 | noisy |

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
