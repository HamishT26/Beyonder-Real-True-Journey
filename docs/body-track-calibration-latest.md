# Body Profile Calibration Report

- generated_utc: `2026-04-05T15:06:20+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `442`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.529 | 0.522 | loosen_duration+tighten_health | noisy |
| standard | 0.529 | 0.522 | loosen_duration+tighten_health | noisy |
| strict | 0.889 | 0.887 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.31448`
- observed_false_regression_rate: `0.309955`
```json
{
  "duration_drift_p90": 1.114376,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.698 | noisy |
| 3 | 1 | 0.220 | 0.216 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.849 | 0.826 | noisy |
| 5 | 1 | 0.546 | 0.537 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.901 | 0.869 | noisy |
| 7 | 1 | 0.722 | 0.709 | noisy |
| 7 | 2 | 0.447 | 0.445 | noisy |
| 7 | 3 | 0.124 | 0.124 | acceptable |
| 9 | 0 | 0.931 | 0.889 | noisy |
| 9 | 1 | 0.825 | 0.806 | noisy |
| 9 | 2 | 0.615 | 0.608 | noisy |
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
