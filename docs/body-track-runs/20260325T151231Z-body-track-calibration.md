# Body Profile Calibration Report

- generated_utc: `2026-03-25T15:12:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `308`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.620 | 0.611 | loosen_duration+tighten_health | noisy |
| standard | 0.620 | 0.611 | loosen_duration+tighten_health | noisy |
| strict | 0.877 | 0.874 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.318182`
- observed_false_regression_rate: `0.311688`
```json
{
  "duration_drift_p90": 1.397453,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.719 | 0.699 | noisy |
| 3 | 1 | 0.222 | 0.216 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.865 | 0.832 | noisy |
| 5 | 1 | 0.543 | 0.530 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.911 | 0.864 | noisy |
| 7 | 1 | 0.742 | 0.722 | noisy |
| 7 | 2 | 0.434 | 0.430 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.933 | 0.873 | noisy |
| 9 | 1 | 0.850 | 0.823 | noisy |
| 9 | 2 | 0.623 | 0.613 | noisy |
| 9 | 3 | 0.347 | 0.347 | noisy |

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
