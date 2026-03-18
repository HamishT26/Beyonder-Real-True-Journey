# Body Profile Calibration Report

- generated_utc: `2026-03-18T03:10:10+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `212`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.476 | 0.459 | loosen_duration+tighten_health | noisy |
| standard | 0.476 | 0.459 | loosen_duration+tighten_health | noisy |
| strict | 0.821 | 0.815 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287736`
- observed_false_regression_rate: `0.278302`
```json
{
  "duration_drift_p90": 1.110042,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.671 | 0.643 | noisy |
| 3 | 1 | 0.190 | 0.181 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.817 | 0.769 | noisy |
| 5 | 1 | 0.490 | 0.471 | noisy |
| 5 | 2 | 0.130 | 0.130 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.874 | 0.806 | noisy |
| 7 | 1 | 0.694 | 0.665 | noisy |
| 7 | 2 | 0.359 | 0.354 | noisy |
| 7 | 3 | 0.097 | 0.097 | acceptable |
| 9 | 0 | 0.902 | 0.814 | noisy |
| 9 | 1 | 0.809 | 0.770 | noisy |
| 9 | 2 | 0.554 | 0.539 | noisy |
| 9 | 3 | 0.279 | 0.279 | noisy |

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
