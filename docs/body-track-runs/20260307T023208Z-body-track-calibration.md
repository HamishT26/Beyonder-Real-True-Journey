# Body Profile Calibration Report

- generated_utc: `2026-03-07T02:32:08+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `81`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.210 | 0.135 | loosen_duration+loosen_health | acceptable |
| standard | 0.210 | 0.135 | loosen_duration+loosen_health | acceptable |
| strict | 0.580 | 0.541 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.185185`
- observed_false_regression_rate: `0.160494`
```json
{
  "duration_drift_p90": 0.363885,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.443 | 0.367 | noisy |
| 3 | 1 | 0.114 | 0.089 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.610 | 0.481 | noisy |
| 5 | 1 | 0.234 | 0.182 | noisy |
| 5 | 2 | 0.078 | 0.078 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.680 | 0.493 | noisy |
| 7 | 1 | 0.387 | 0.307 | noisy |
| 7 | 2 | 0.173 | 0.160 | noisy |
| 7 | 3 | 0.053 | 0.053 | acceptable |
| 9 | 0 | 0.726 | 0.479 | noisy |
| 9 | 1 | 0.521 | 0.411 | noisy |
| 9 | 2 | 0.260 | 0.219 | noisy |
| 9 | 3 | 0.137 | 0.137 | acceptable |

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
