# Body Profile Calibration Report

- generated_utc: `2026-03-10T06:21:11+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `121`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.355 | 0.316 | loosen_duration+loosen_health | noisy |
| standard | 0.355 | 0.316 | loosen_duration+loosen_health | noisy |
| strict | 0.711 | 0.693 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.256198`
- observed_false_regression_rate: `0.239669`
```json
{
  "duration_drift_p90": 1.01053,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.597 | 0.546 | noisy |
| 3 | 1 | 0.176 | 0.160 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.744 | 0.658 | noisy |
| 5 | 1 | 0.402 | 0.368 | noisy |
| 5 | 2 | 0.145 | 0.145 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.791 | 0.670 | noisy |
| 7 | 1 | 0.583 | 0.530 | noisy |
| 7 | 2 | 0.322 | 0.313 | noisy |
| 7 | 3 | 0.122 | 0.122 | acceptable |
| 9 | 0 | 0.823 | 0.664 | noisy |
| 9 | 1 | 0.690 | 0.619 | noisy |
| 9 | 2 | 0.442 | 0.416 | noisy |
| 9 | 3 | 0.310 | 0.310 | noisy |

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
