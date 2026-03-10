# Body Profile Calibration Report

- generated_utc: `2026-03-08T14:28:59+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `112`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.330 | 0.286 | loosen_duration+loosen_health | noisy |
| standard | 0.330 | 0.286 | loosen_duration+loosen_health | noisy |
| strict | 0.688 | 0.667 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.241071`
- observed_false_regression_rate: `0.223214`
```json
{
  "duration_drift_p90": 0.873627,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.564 | 0.509 | noisy |
| 3 | 1 | 0.164 | 0.145 | acceptable |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.722 | 0.630 | noisy |
| 5 | 1 | 0.352 | 0.315 | noisy |
| 5 | 2 | 0.139 | 0.139 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.774 | 0.642 | noisy |
| 7 | 1 | 0.547 | 0.491 | noisy |
| 7 | 2 | 0.274 | 0.264 | noisy |
| 7 | 3 | 0.123 | 0.123 | acceptable |
| 9 | 0 | 0.808 | 0.635 | noisy |
| 9 | 1 | 0.663 | 0.587 | noisy |
| 9 | 2 | 0.394 | 0.365 | noisy |
| 9 | 3 | 0.260 | 0.260 | noisy |

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
