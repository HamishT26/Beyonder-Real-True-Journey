# Body Profile Calibration Report

- generated_utc: `2026-03-22T19:30:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `255`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.557 | 0.544 | loosen_duration+tighten_health | noisy |
| standard | 0.557 | 0.544 | loosen_duration+tighten_health | noisy |
| strict | 0.851 | 0.847 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317647`
- observed_false_regression_rate: `0.309804`
```json
{
  "duration_drift_p90": 1.479868,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.688 | noisy |
| 3 | 1 | 0.229 | 0.221 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.849 | 0.809 | noisy |
| 5 | 1 | 0.550 | 0.534 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.896 | 0.839 | noisy |
| 7 | 1 | 0.743 | 0.719 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.919 | 0.846 | noisy |
| 9 | 1 | 0.842 | 0.810 | noisy |
| 9 | 2 | 0.623 | 0.611 | noisy |
| 9 | 3 | 0.352 | 0.352 | noisy |

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
