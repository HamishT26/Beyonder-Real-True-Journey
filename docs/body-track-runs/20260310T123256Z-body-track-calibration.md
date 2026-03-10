# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:32:56+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `134`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.336 | 0.299 | loosen_duration+loosen_health | noisy |
| standard | 0.336 | 0.299 | loosen_duration+loosen_health | noisy |
| strict | 0.724 | 0.709 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.268657`
- observed_false_regression_rate: `0.253731`
```json
{
  "duration_drift_p90": 1.003021,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.629 | 0.583 | noisy |
| 3 | 1 | 0.182 | 0.167 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.769 | 0.692 | noisy |
| 5 | 1 | 0.438 | 0.408 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.812 | 0.703 | noisy |
| 7 | 1 | 0.625 | 0.578 | noisy |
| 7 | 2 | 0.352 | 0.344 | noisy |
| 7 | 3 | 0.109 | 0.109 | acceptable |
| 9 | 0 | 0.841 | 0.698 | noisy |
| 9 | 1 | 0.722 | 0.659 | noisy |
| 9 | 2 | 0.500 | 0.476 | noisy |
| 9 | 3 | 0.310 | 0.310 | noisy |

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
