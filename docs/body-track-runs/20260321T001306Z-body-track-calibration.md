# Body Profile Calibration Report

- generated_utc: `2026-03-21T00:13:06+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `228`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.509 | 0.493 | loosen_duration+tighten_health | noisy |
| standard | 0.509 | 0.493 | loosen_duration+tighten_health | noisy |
| strict | 0.833 | 0.828 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.307018`
- observed_false_regression_rate: `0.298246`
```json
{
  "duration_drift_p90": 1.156795,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.695 | 0.668 | noisy |
| 3 | 1 | 0.217 | 0.208 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.830 | 0.786 | noisy |
| 5 | 1 | 0.527 | 0.509 | noisy |
| 5 | 2 | 0.161 | 0.161 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.883 | 0.820 | noisy |
| 7 | 1 | 0.716 | 0.689 | noisy |
| 7 | 2 | 0.405 | 0.401 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.909 | 0.827 | noisy |
| 9 | 1 | 0.823 | 0.786 | noisy |
| 9 | 2 | 0.586 | 0.573 | noisy |
| 9 | 3 | 0.327 | 0.327 | noisy |

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
