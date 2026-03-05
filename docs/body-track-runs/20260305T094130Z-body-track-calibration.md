# Body Profile Calibration Report

- generated_utc: `2026-03-05T09:41:30+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `36`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.167 | 0.000 | tighten_duration+loosen_health | acceptable |
| standard | 0.167 | 0.000 | tighten_duration+loosen_health | acceptable |
| strict | 0.306 | 0.167 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.027778`
- observed_false_regression_rate: `0.0`
```json
{
  "duration_drift_p90": 0.111081,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.088 | 0.000 | acceptable |
| 3 | 1 | 0.000 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.156 | 0.000 | acceptable |
| 5 | 1 | 0.000 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.233 | 0.000 | acceptable |
| 7 | 1 | 0.000 | 0.000 | acceptable |
| 7 | 2 | 0.000 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.321 | 0.000 | acceptable |
| 9 | 1 | 0.000 | 0.000 | acceptable |
| 9 | 2 | 0.000 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 7,
    "max_regressions": 0
  }
}
```
