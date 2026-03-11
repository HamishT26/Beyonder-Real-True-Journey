# Body Profile Calibration Report

- generated_utc: `2026-03-11T04:13:57+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `142`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.345 | 0.311 | loosen_duration+tighten_health | noisy |
| standard | 0.345 | 0.311 | loosen_duration+tighten_health | noisy |
| strict | 0.739 | 0.726 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.267606`
- observed_false_regression_rate: `0.253521`
```json
{
  "duration_drift_p90": 1.00691,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.636 | 0.593 | noisy |
| 3 | 1 | 0.171 | 0.157 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.783 | 0.710 | noisy |
| 5 | 1 | 0.435 | 0.406 | noisy |
| 5 | 2 | 0.130 | 0.130 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.824 | 0.721 | noisy |
| 7 | 1 | 0.640 | 0.596 | noisy |
| 7 | 2 | 0.338 | 0.331 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.851 | 0.716 | noisy |
| 9 | 1 | 0.739 | 0.679 | noisy |
| 9 | 2 | 0.515 | 0.493 | noisy |
| 9 | 3 | 0.291 | 0.291 | noisy |

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
