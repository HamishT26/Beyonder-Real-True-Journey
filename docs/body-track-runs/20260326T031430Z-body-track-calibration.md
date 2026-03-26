# Body Profile Calibration Report

- generated_utc: `2026-03-26T03:14:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `328`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.637 | 0.629 | loosen_duration+tighten_health | noisy |
| standard | 0.637 | 0.629 | loosen_duration+tighten_health | noisy |
| strict | 0.884 | 0.882 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.329268`
- observed_false_regression_rate: `0.323171`
```json
{
  "duration_drift_p90": 1.583835,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.730 | 0.712 | noisy |
| 3 | 1 | 0.236 | 0.230 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.873 | 0.843 | noisy |
| 5 | 1 | 0.568 | 0.556 | noisy |
| 5 | 2 | 0.188 | 0.188 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.916 | 0.873 | noisy |
| 7 | 1 | 0.758 | 0.739 | noisy |
| 7 | 2 | 0.463 | 0.460 | noisy |
| 7 | 3 | 0.146 | 0.146 | acceptable |
| 9 | 0 | 0.938 | 0.881 | noisy |
| 9 | 1 | 0.859 | 0.834 | noisy |
| 9 | 2 | 0.647 | 0.637 | noisy |
| 9 | 3 | 0.378 | 0.378 | noisy |

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
