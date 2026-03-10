# Body Profile Calibration Report

- generated_utc: `2026-03-10T09:04:42+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `123`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.350 | 0.310 | loosen_duration+loosen_health | noisy |
| standard | 0.350 | 0.310 | loosen_duration+loosen_health | noisy |
| strict | 0.715 | 0.698 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.260163`
- observed_false_regression_rate: `0.243902`
```json
{
  "duration_drift_p90": 1.004965,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.595 | 0.545 | noisy |
| 3 | 1 | 0.174 | 0.157 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.748 | 0.664 | noisy |
| 5 | 1 | 0.403 | 0.370 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.795 | 0.675 | noisy |
| 7 | 1 | 0.590 | 0.538 | noisy |
| 7 | 2 | 0.325 | 0.316 | noisy |
| 7 | 3 | 0.120 | 0.120 | acceptable |
| 9 | 0 | 0.826 | 0.670 | noisy |
| 9 | 1 | 0.696 | 0.626 | noisy |
| 9 | 2 | 0.452 | 0.426 | noisy |
| 9 | 3 | 0.304 | 0.304 | noisy |

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
