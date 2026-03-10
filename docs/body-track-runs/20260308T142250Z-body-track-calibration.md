# Body Profile Calibration Report

- generated_utc: `2026-03-08T14:22:50+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `111`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.324 | 0.279 | loosen_duration+loosen_health | noisy |
| standard | 0.324 | 0.279 | loosen_duration+loosen_health | noisy |
| strict | 0.685 | 0.663 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.243243`
- observed_false_regression_rate: `0.225225`
```json
{
  "duration_drift_p90": 0.886955,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.560 | 0.505 | noisy |
| 3 | 1 | 0.165 | 0.147 | acceptable |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.720 | 0.626 | noisy |
| 5 | 1 | 0.355 | 0.318 | noisy |
| 5 | 2 | 0.140 | 0.140 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.771 | 0.638 | noisy |
| 7 | 1 | 0.543 | 0.486 | noisy |
| 7 | 2 | 0.276 | 0.267 | noisy |
| 7 | 3 | 0.124 | 0.124 | acceptable |
| 9 | 0 | 0.806 | 0.631 | noisy |
| 9 | 1 | 0.660 | 0.583 | noisy |
| 9 | 2 | 0.388 | 0.359 | noisy |
| 9 | 3 | 0.252 | 0.252 | noisy |

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
