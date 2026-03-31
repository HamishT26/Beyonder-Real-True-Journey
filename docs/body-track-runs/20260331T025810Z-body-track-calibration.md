# Body Profile Calibration Report

- generated_utc: `2026-03-31T02:58:10+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `341`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.639 | 0.632 | loosen_duration+tighten_health | noisy |
| standard | 0.639 | 0.632 | loosen_duration+tighten_health | noisy |
| strict | 0.889 | 0.886 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.331378`
- observed_false_regression_rate: `0.325513`
```json
{
  "duration_drift_p90": 1.56767,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.740 | 0.723 | noisy |
| 3 | 1 | 0.239 | 0.233 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.878 | 0.849 | noisy |
| 5 | 1 | 0.582 | 0.570 | noisy |
| 5 | 2 | 0.193 | 0.193 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.919 | 0.878 | noisy |
| 7 | 1 | 0.767 | 0.749 | noisy |
| 7 | 2 | 0.481 | 0.478 | noisy |
| 7 | 3 | 0.149 | 0.149 | acceptable |
| 9 | 0 | 0.940 | 0.886 | noisy |
| 9 | 1 | 0.865 | 0.841 | noisy |
| 9 | 2 | 0.661 | 0.652 | noisy |
| 9 | 3 | 0.399 | 0.399 | noisy |

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
