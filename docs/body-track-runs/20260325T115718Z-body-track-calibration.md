# Body Profile Calibration Report

- generated_utc: `2026-03-25T11:57:18+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `298`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.607 | 0.598 | loosen_duration+tighten_health | noisy |
| standard | 0.607 | 0.598 | loosen_duration+tighten_health | noisy |
| strict | 0.872 | 0.869 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315436`
- observed_false_regression_rate: `0.308725`
```json
{
  "duration_drift_p90": 1.397453,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.716 | 0.696 | noisy |
| 3 | 1 | 0.223 | 0.216 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.861 | 0.827 | noisy |
| 5 | 1 | 0.544 | 0.531 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.908 | 0.860 | noisy |
| 7 | 1 | 0.740 | 0.719 | noisy |
| 7 | 2 | 0.438 | 0.435 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.931 | 0.869 | noisy |
| 9 | 1 | 0.845 | 0.817 | noisy |
| 9 | 2 | 0.624 | 0.614 | noisy |
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
