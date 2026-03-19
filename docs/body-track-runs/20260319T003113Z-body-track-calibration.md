# Body Profile Calibration Report

- generated_utc: `2026-03-19T00:31:13+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `216`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.481 | 0.464 | loosen_duration+tighten_health | noisy |
| standard | 0.481 | 0.464 | loosen_duration+tighten_health | noisy |
| strict | 0.824 | 0.818 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.291667`
- observed_false_regression_rate: `0.282407`
```json
{
  "duration_drift_p90": 1.115875,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.678 | 0.650 | noisy |
| 3 | 1 | 0.192 | 0.182 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.821 | 0.774 | noisy |
| 5 | 1 | 0.500 | 0.481 | noisy |
| 5 | 2 | 0.132 | 0.132 | acceptable |
| 5 | 3 | 0.009 | 0.009 | acceptable |
| 7 | 0 | 0.876 | 0.810 | noisy |
| 7 | 1 | 0.700 | 0.671 | noisy |
| 7 | 2 | 0.371 | 0.367 | noisy |
| 7 | 3 | 0.095 | 0.095 | acceptable |
| 9 | 0 | 0.904 | 0.817 | noisy |
| 9 | 1 | 0.812 | 0.774 | noisy |
| 9 | 2 | 0.562 | 0.548 | noisy |
| 9 | 3 | 0.288 | 0.288 | noisy |

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
