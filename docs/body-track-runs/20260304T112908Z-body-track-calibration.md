# Body Profile Calibration Report

- generated_utc: `2026-03-04T11:29:08+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `32`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.188 | 0.000 | tighten_duration+loosen_health | acceptable |
| standard | 0.188 | 0.000 | tighten_duration+loosen_health | acceptable |
| strict | 0.344 | 0.192 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.03125`
- observed_false_regression_rate: `0.0`
```json
{
  "duration_drift_p90": 0.126336,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.100 | 0.000 | acceptable |
| 3 | 1 | 0.000 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.179 | 0.000 | acceptable |
| 5 | 1 | 0.000 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.269 | 0.000 | acceptable |
| 7 | 1 | 0.000 | 0.000 | acceptable |
| 7 | 2 | 0.000 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.375 | 0.000 | acceptable |
| 9 | 1 | 0.000 | 0.000 | acceptable |
| 9 | 2 | 0.000 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 5,
    "max_regressions": 0
  }
}
```
