# Body Profile Calibration Report

- generated_utc: `2026-03-08T12:58:12+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `99`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.242 | 0.185 | loosen_duration+loosen_health | noisy |
| standard | 0.242 | 0.185 | loosen_duration+loosen_health | noisy |
| strict | 0.646 | 0.620 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.222222`
- observed_false_regression_rate: `0.20202`
```json
{
  "duration_drift_p90": 0.765841,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.505 | 0.443 | noisy |
| 3 | 1 | 0.144 | 0.124 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.684 | 0.579 | noisy |
| 5 | 1 | 0.274 | 0.232 | noisy |
| 5 | 2 | 0.105 | 0.105 | acceptable |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.742 | 0.591 | noisy |
| 7 | 1 | 0.484 | 0.419 | noisy |
| 7 | 2 | 0.183 | 0.172 | noisy |
| 7 | 3 | 0.075 | 0.075 | acceptable |
| 9 | 0 | 0.780 | 0.582 | noisy |
| 9 | 1 | 0.615 | 0.527 | noisy |
| 9 | 2 | 0.308 | 0.275 | noisy |
| 9 | 3 | 0.154 | 0.154 | noisy |

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
