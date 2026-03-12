# Body Profile Calibration Report

- generated_utc: `2026-03-12T11:50:22+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `162`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.370 | 0.342 | loosen_duration+tighten_health | noisy |
| standard | 0.370 | 0.342 | loosen_duration+tighten_health | noisy |
| strict | 0.765 | 0.755 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.265432`
- observed_false_regression_rate: `0.253086`
```json
{
  "duration_drift_p90": 1.00691,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.631 | 0.594 | noisy |
| 3 | 1 | 0.163 | 0.150 | acceptable |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.785 | 0.722 | noisy |
| 5 | 1 | 0.424 | 0.399 | noisy |
| 5 | 2 | 0.120 | 0.120 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.840 | 0.750 | noisy |
| 7 | 1 | 0.635 | 0.596 | noisy |
| 7 | 2 | 0.321 | 0.314 | noisy |
| 7 | 3 | 0.090 | 0.090 | acceptable |
| 9 | 0 | 0.870 | 0.753 | noisy |
| 9 | 1 | 0.753 | 0.701 | noisy |
| 9 | 2 | 0.500 | 0.481 | noisy |
| 9 | 3 | 0.266 | 0.266 | noisy |

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
