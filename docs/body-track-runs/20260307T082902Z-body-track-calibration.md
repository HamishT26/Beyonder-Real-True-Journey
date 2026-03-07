# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:29:02+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `94`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.202 | 0.138 | loosen_duration+loosen_health | acceptable |
| standard | 0.202 | 0.138 | loosen_duration+loosen_health | acceptable |
| strict | 0.628 | 0.598 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.191489`
- observed_false_regression_rate: `0.170213`
```json
{
  "duration_drift_p90": 0.363259,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.478 | 0.413 | noisy |
| 3 | 1 | 0.098 | 0.076 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.667 | 0.556 | noisy |
| 5 | 1 | 0.233 | 0.189 | noisy |
| 5 | 2 | 0.067 | 0.067 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.727 | 0.568 | noisy |
| 7 | 1 | 0.455 | 0.386 | noisy |
| 7 | 2 | 0.148 | 0.136 | acceptable |
| 7 | 3 | 0.045 | 0.045 | acceptable |
| 9 | 0 | 0.767 | 0.558 | noisy |
| 9 | 1 | 0.593 | 0.500 | noisy |
| 9 | 2 | 0.267 | 0.233 | noisy |
| 9 | 3 | 0.116 | 0.116 | acceptable |

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
