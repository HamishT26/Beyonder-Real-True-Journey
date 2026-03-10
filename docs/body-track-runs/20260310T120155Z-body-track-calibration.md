# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:01:55+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `130`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.338 | 0.301 | loosen_duration+loosen_health | noisy |
| standard | 0.338 | 0.301 | loosen_duration+loosen_health | noisy |
| strict | 0.715 | 0.699 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.261538`
- observed_false_regression_rate: `0.246154`
```json
{
  "duration_drift_p90": 1.01415,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.617 | 0.570 | noisy |
| 3 | 1 | 0.172 | 0.156 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.762 | 0.683 | noisy |
| 5 | 1 | 0.421 | 0.389 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.806 | 0.694 | noisy |
| 7 | 1 | 0.613 | 0.565 | noisy |
| 7 | 2 | 0.331 | 0.323 | noisy |
| 7 | 3 | 0.113 | 0.113 | acceptable |
| 9 | 0 | 0.836 | 0.689 | noisy |
| 9 | 1 | 0.713 | 0.648 | noisy |
| 9 | 2 | 0.484 | 0.459 | noisy |
| 9 | 3 | 0.295 | 0.295 | noisy |

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
