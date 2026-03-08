# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:56:04+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `108`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.306 | 0.257 | loosen_duration+loosen_health | noisy |
| standard | 0.306 | 0.257 | loosen_duration+loosen_health | noisy |
| strict | 0.676 | 0.653 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.240741`
- observed_false_regression_rate: `0.222222`
```json
{
  "duration_drift_p90": 0.853392,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.547 | 0.491 | noisy |
| 3 | 1 | 0.170 | 0.151 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.712 | 0.615 | noisy |
| 5 | 1 | 0.337 | 0.298 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.765 | 0.627 | noisy |
| 7 | 1 | 0.529 | 0.471 | noisy |
| 7 | 2 | 0.255 | 0.245 | noisy |
| 7 | 3 | 0.118 | 0.118 | acceptable |
| 9 | 0 | 0.800 | 0.620 | noisy |
| 9 | 1 | 0.650 | 0.570 | noisy |
| 9 | 2 | 0.370 | 0.340 | noisy |
| 9 | 3 | 0.230 | 0.230 | noisy |

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
