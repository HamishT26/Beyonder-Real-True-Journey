# Body Profile Calibration Report

- generated_utc: `2026-03-08T14:12:41+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `110`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.318 | 0.272 | loosen_duration+loosen_health | noisy |
| standard | 0.318 | 0.272 | loosen_duration+loosen_health | noisy |
| strict | 0.682 | 0.660 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.245455`
- observed_false_regression_rate: `0.227273`
```json
{
  "duration_drift_p90": 0.900284,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.556 | 0.500 | noisy |
| 3 | 1 | 0.167 | 0.148 | acceptable |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.717 | 0.623 | noisy |
| 5 | 1 | 0.349 | 0.311 | noisy |
| 5 | 2 | 0.142 | 0.142 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.769 | 0.635 | noisy |
| 7 | 1 | 0.538 | 0.481 | noisy |
| 7 | 2 | 0.269 | 0.260 | noisy |
| 7 | 3 | 0.125 | 0.125 | acceptable |
| 9 | 0 | 0.804 | 0.627 | noisy |
| 9 | 1 | 0.657 | 0.578 | noisy |
| 9 | 2 | 0.382 | 0.353 | noisy |
| 9 | 3 | 0.245 | 0.245 | noisy |

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
