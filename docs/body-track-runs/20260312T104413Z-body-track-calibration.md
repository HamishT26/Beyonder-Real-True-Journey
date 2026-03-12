# Body Profile Calibration Report

- generated_utc: `2026-03-12T10:44:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `156`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.385 | 0.356 | loosen_duration+tighten_health | noisy |
| standard | 0.385 | 0.356 | loosen_duration+tighten_health | noisy |
| strict | 0.763 | 0.752 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.269231`
- observed_false_regression_rate: `0.25641`
```json
{
  "duration_drift_p90": 1.028631,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.643 | 0.604 | noisy |
| 3 | 1 | 0.169 | 0.156 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.796 | 0.730 | noisy |
| 5 | 1 | 0.441 | 0.414 | noisy |
| 5 | 2 | 0.125 | 0.125 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.840 | 0.747 | noisy |
| 7 | 1 | 0.660 | 0.620 | noisy |
| 7 | 2 | 0.333 | 0.327 | noisy |
| 7 | 3 | 0.093 | 0.093 | acceptable |
| 9 | 0 | 0.865 | 0.743 | noisy |
| 9 | 1 | 0.764 | 0.709 | noisy |
| 9 | 2 | 0.520 | 0.500 | noisy |
| 9 | 3 | 0.277 | 0.277 | noisy |

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
