# Body Profile Calibration Report

- generated_utc: `2026-03-12T10:09:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `154`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.390 | 0.361 | loosen_duration+tighten_health | noisy |
| standard | 0.390 | 0.361 | loosen_duration+tighten_health | noisy |
| strict | 0.760 | 0.748 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.272727`
- observed_false_regression_rate: `0.25974`
```json
{
  "duration_drift_p90": 1.035871,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.645 | 0.605 | noisy |
| 3 | 1 | 0.171 | 0.158 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.793 | 0.727 | noisy |
| 5 | 1 | 0.447 | 0.420 | noisy |
| 5 | 2 | 0.127 | 0.127 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.838 | 0.743 | noisy |
| 7 | 1 | 0.655 | 0.615 | noisy |
| 7 | 2 | 0.338 | 0.331 | noisy |
| 7 | 3 | 0.095 | 0.095 | acceptable |
| 9 | 0 | 0.863 | 0.740 | noisy |
| 9 | 1 | 0.760 | 0.705 | noisy |
| 9 | 2 | 0.521 | 0.500 | noisy |
| 9 | 3 | 0.281 | 0.281 | noisy |

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
