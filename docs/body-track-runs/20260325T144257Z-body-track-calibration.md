# Body Profile Calibration Report

- generated_utc: `2026-03-25T14:42:57+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `307`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.619 | 0.610 | loosen_duration+tighten_health | noisy |
| standard | 0.619 | 0.610 | loosen_duration+tighten_health | noisy |
| strict | 0.876 | 0.873 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315961`
- observed_false_regression_rate: `0.309446`
```json
{
  "duration_drift_p90": 1.424924,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.718 | 0.698 | noisy |
| 3 | 1 | 0.220 | 0.213 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.865 | 0.832 | noisy |
| 5 | 1 | 0.541 | 0.528 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.910 | 0.864 | noisy |
| 7 | 1 | 0.741 | 0.721 | noisy |
| 7 | 2 | 0.432 | 0.429 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.933 | 0.873 | noisy |
| 9 | 1 | 0.849 | 0.823 | noisy |
| 9 | 2 | 0.622 | 0.612 | noisy |
| 9 | 3 | 0.344 | 0.344 | noisy |

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
