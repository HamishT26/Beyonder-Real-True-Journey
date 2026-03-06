# Body Profile Calibration Report

- generated_utc: `2026-03-06T05:00:53+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `63`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.190 | 0.089 | loosen_duration+loosen_health | acceptable |
| standard | 0.190 | 0.089 | loosen_duration+loosen_health | acceptable |
| strict | 0.508 | 0.446 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.174603`
- observed_false_regression_rate: `0.142857`
```json
{
  "duration_drift_p90": 0.28904,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.410 | 0.311 | noisy |
| 3 | 1 | 0.131 | 0.098 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.525 | 0.356 | noisy |
| 5 | 1 | 0.271 | 0.203 | noisy |
| 5 | 2 | 0.102 | 0.102 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.579 | 0.333 | noisy |
| 7 | 1 | 0.386 | 0.281 | noisy |
| 7 | 2 | 0.228 | 0.211 | noisy |
| 7 | 3 | 0.070 | 0.070 | acceptable |
| 9 | 0 | 0.636 | 0.309 | noisy |
| 9 | 1 | 0.436 | 0.291 | noisy |
| 9 | 2 | 0.291 | 0.236 | noisy |
| 9 | 3 | 0.182 | 0.182 | noisy |

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
