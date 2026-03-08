# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:23:46+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `106`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.292 | 0.242 | loosen_duration+loosen_health | noisy |
| standard | 0.292 | 0.242 | loosen_duration+loosen_health | noisy |
| strict | 0.670 | 0.646 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.235849`
- observed_false_regression_rate: `0.216981`
```json
{
  "duration_drift_p90": 0.797581,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.538 | 0.481 | noisy |
| 3 | 1 | 0.163 | 0.144 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.706 | 0.608 | noisy |
| 5 | 1 | 0.324 | 0.284 | noisy |
| 5 | 2 | 0.127 | 0.127 | acceptable |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.760 | 0.620 | noisy |
| 7 | 1 | 0.520 | 0.460 | noisy |
| 7 | 2 | 0.240 | 0.230 | noisy |
| 7 | 3 | 0.110 | 0.110 | acceptable |
| 9 | 0 | 0.796 | 0.612 | noisy |
| 9 | 1 | 0.643 | 0.561 | noisy |
| 9 | 2 | 0.357 | 0.327 | noisy |
| 9 | 3 | 0.214 | 0.214 | noisy |

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
