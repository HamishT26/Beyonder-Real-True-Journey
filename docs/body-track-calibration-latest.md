# Body Profile Calibration Report

- generated_utc: `2026-04-06T15:44:55+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `446`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.525 | 0.517 | loosen_duration+tighten_health | noisy |
| standard | 0.525 | 0.517 | loosen_duration+tighten_health | noisy |
| strict | 0.890 | 0.888 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313901`
- observed_false_regression_rate: `0.309417`
```json
{
  "duration_drift_p90": 1.112642,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.712 | 0.698 | noisy |
| 3 | 1 | 0.221 | 0.216 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.851 | 0.828 | noisy |
| 5 | 1 | 0.548 | 0.538 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.902 | 0.870 | noisy |
| 7 | 1 | 0.725 | 0.711 | noisy |
| 7 | 2 | 0.450 | 0.448 | noisy |
| 7 | 3 | 0.125 | 0.125 | acceptable |
| 9 | 0 | 0.932 | 0.890 | noisy |
| 9 | 1 | 0.826 | 0.808 | noisy |
| 9 | 2 | 0.619 | 0.612 | noisy |
| 9 | 3 | 0.358 | 0.358 | noisy |

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
