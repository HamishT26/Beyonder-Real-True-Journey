# Body Profile Calibration Report

- generated_utc: `2026-03-22T19:34:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `256`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.559 | 0.546 | loosen_duration+tighten_health | noisy |
| standard | 0.559 | 0.546 | loosen_duration+tighten_health | noisy |
| strict | 0.852 | 0.847 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316406`
- observed_false_regression_rate: `0.308594`
```json
{
  "duration_drift_p90": 1.452396,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.689 | noisy |
| 3 | 1 | 0.228 | 0.220 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.849 | 0.810 | noisy |
| 5 | 1 | 0.552 | 0.536 | noisy |
| 5 | 2 | 0.175 | 0.175 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.896 | 0.840 | noisy |
| 7 | 1 | 0.744 | 0.720 | noisy |
| 7 | 2 | 0.440 | 0.436 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.919 | 0.847 | noisy |
| 9 | 1 | 0.843 | 0.810 | noisy |
| 9 | 2 | 0.625 | 0.613 | noisy |
| 9 | 3 | 0.355 | 0.355 | noisy |

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
