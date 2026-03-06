# Body Profile Calibration Report

- generated_utc: `2026-03-06T12:44:37+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `66`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.197 | 0.102 | loosen_duration+loosen_health | acceptable |
| standard | 0.197 | 0.102 | loosen_duration+loosen_health | acceptable |
| strict | 0.500 | 0.441 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.181818`
- observed_false_regression_rate: `0.151515`
```json
{
  "duration_drift_p90": 0.311608,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.406 | 0.312 | noisy |
| 3 | 1 | 0.125 | 0.094 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.548 | 0.387 | noisy |
| 5 | 1 | 0.258 | 0.194 | noisy |
| 5 | 2 | 0.097 | 0.097 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.600 | 0.367 | noisy |
| 7 | 1 | 0.400 | 0.300 | noisy |
| 7 | 2 | 0.217 | 0.200 | noisy |
| 7 | 3 | 0.067 | 0.067 | acceptable |
| 9 | 0 | 0.655 | 0.345 | noisy |
| 9 | 1 | 0.466 | 0.328 | noisy |
| 9 | 2 | 0.328 | 0.276 | noisy |
| 9 | 3 | 0.172 | 0.172 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
