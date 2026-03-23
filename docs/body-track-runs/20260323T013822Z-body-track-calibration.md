# Body Profile Calibration Report

- generated_utc: `2026-03-23T01:38:22+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `265`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.574 | 0.562 | loosen_duration+tighten_health | noisy |
| standard | 0.574 | 0.562 | loosen_duration+tighten_health | noisy |
| strict | 0.857 | 0.853 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313208`
- observed_false_regression_rate: `0.30566`
```json
{
  "duration_drift_p90": 1.26871,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.688 | noisy |
| 3 | 1 | 0.221 | 0.213 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.854 | 0.816 | noisy |
| 5 | 1 | 0.540 | 0.525 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.900 | 0.846 | noisy |
| 7 | 1 | 0.741 | 0.718 | noisy |
| 7 | 2 | 0.436 | 0.432 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.922 | 0.852 | noisy |
| 9 | 1 | 0.848 | 0.817 | noisy |
| 9 | 2 | 0.626 | 0.615 | noisy |
| 9 | 3 | 0.358 | 0.358 | noisy |

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
