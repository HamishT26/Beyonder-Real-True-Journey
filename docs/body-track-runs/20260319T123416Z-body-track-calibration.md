# Body Profile Calibration Report

- generated_utc: `2026-03-19T12:34:16+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `221`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.493 | 0.477 | loosen_duration+tighten_health | noisy |
| standard | 0.493 | 0.477 | loosen_duration+tighten_health | noisy |
| strict | 0.828 | 0.822 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.303167`
- observed_false_regression_rate: `0.294118`
```json
{
  "duration_drift_p90": 1.126855,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.685 | 0.658 | noisy |
| 3 | 1 | 0.205 | 0.196 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.825 | 0.779 | noisy |
| 5 | 1 | 0.512 | 0.493 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.879 | 0.814 | noisy |
| 7 | 1 | 0.707 | 0.679 | noisy |
| 7 | 2 | 0.386 | 0.381 | noisy |
| 7 | 3 | 0.107 | 0.107 | acceptable |
| 9 | 0 | 0.906 | 0.822 | noisy |
| 9 | 1 | 0.817 | 0.779 | noisy |
| 9 | 2 | 0.573 | 0.559 | noisy |
| 9 | 3 | 0.305 | 0.305 | noisy |

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
