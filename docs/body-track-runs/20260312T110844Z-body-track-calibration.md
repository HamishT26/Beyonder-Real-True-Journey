# Body Profile Calibration Report

- generated_utc: `2026-03-12T11:08:44+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `158`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.380 | 0.351 | loosen_duration+tighten_health | noisy |
| standard | 0.380 | 0.351 | loosen_duration+tighten_health | noisy |
| strict | 0.766 | 0.755 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.265823`
- observed_false_regression_rate: `0.253165`
```json
{
  "duration_drift_p90": 1.02139,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.635 | 0.596 | noisy |
| 3 | 1 | 0.167 | 0.154 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.792 | 0.727 | noisy |
| 5 | 1 | 0.435 | 0.409 | noisy |
| 5 | 2 | 0.123 | 0.123 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.842 | 0.750 | noisy |
| 7 | 1 | 0.651 | 0.612 | noisy |
| 7 | 2 | 0.329 | 0.322 | noisy |
| 7 | 3 | 0.092 | 0.092 | acceptable |
| 9 | 0 | 0.867 | 0.747 | noisy |
| 9 | 1 | 0.767 | 0.713 | noisy |
| 9 | 2 | 0.513 | 0.493 | noisy |
| 9 | 3 | 0.273 | 0.273 | noisy |

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
