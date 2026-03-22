# Body Profile Calibration Report

- generated_utc: `2026-03-22T13:13:10+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `250`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.548 | 0.535 | loosen_duration+tighten_health | noisy |
| standard | 0.548 | 0.535 | loosen_duration+tighten_health | noisy |
| strict | 0.848 | 0.844 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.312`
- observed_false_regression_rate: `0.304`
```json
{
  "duration_drift_p90": 1.34251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.706 | 0.681 | noisy |
| 3 | 1 | 0.222 | 0.214 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.846 | 0.805 | noisy |
| 5 | 1 | 0.545 | 0.528 | noisy |
| 5 | 2 | 0.163 | 0.163 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.893 | 0.836 | noisy |
| 7 | 1 | 0.738 | 0.713 | noisy |
| 7 | 2 | 0.434 | 0.430 | noisy |
| 7 | 3 | 0.127 | 0.127 | acceptable |
| 9 | 0 | 0.917 | 0.843 | noisy |
| 9 | 1 | 0.839 | 0.806 | noisy |
| 9 | 2 | 0.620 | 0.607 | noisy |
| 9 | 3 | 0.347 | 0.347 | noisy |

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
