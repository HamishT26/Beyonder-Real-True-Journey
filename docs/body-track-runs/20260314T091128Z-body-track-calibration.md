# Body Profile Calibration Report

- generated_utc: `2026-03-14T09:11:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `172`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.390 | 0.364 | loosen_duration+tighten_health | noisy |
| standard | 0.390 | 0.364 | loosen_duration+tighten_health | noisy |
| strict | 0.779 | 0.770 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.27907`
- observed_false_regression_rate: `0.267442`
```json
{
  "duration_drift_p90": 1.099588,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.653 | 0.618 | noisy |
| 3 | 1 | 0.182 | 0.171 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.798 | 0.738 | noisy |
| 5 | 1 | 0.458 | 0.435 | noisy |
| 5 | 2 | 0.137 | 0.137 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.849 | 0.765 | noisy |
| 7 | 1 | 0.657 | 0.620 | noisy |
| 7 | 2 | 0.343 | 0.337 | noisy |
| 7 | 3 | 0.108 | 0.108 | acceptable |
| 9 | 0 | 0.878 | 0.768 | noisy |
| 9 | 1 | 0.768 | 0.720 | noisy |
| 9 | 2 | 0.512 | 0.494 | noisy |
| 9 | 3 | 0.287 | 0.287 | noisy |

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
