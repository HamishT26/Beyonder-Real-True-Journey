# Body Profile Calibration Report

- generated_utc: `2026-03-31T02:37:26+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `340`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.638 | 0.631 | loosen_duration+tighten_health | noisy |
| standard | 0.638 | 0.631 | loosen_duration+tighten_health | noisy |
| strict | 0.888 | 0.886 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.332353`
- observed_false_regression_rate: `0.326471`
```json
{
  "duration_drift_p90": 1.573059,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.740 | 0.722 | noisy |
| 3 | 1 | 0.240 | 0.234 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.878 | 0.848 | noisy |
| 5 | 1 | 0.580 | 0.568 | noisy |
| 5 | 2 | 0.193 | 0.193 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.919 | 0.877 | noisy |
| 7 | 1 | 0.766 | 0.749 | noisy |
| 7 | 2 | 0.479 | 0.476 | noisy |
| 7 | 3 | 0.150 | 0.150 | acceptable |
| 9 | 0 | 0.940 | 0.886 | noisy |
| 9 | 1 | 0.864 | 0.840 | noisy |
| 9 | 2 | 0.660 | 0.651 | noisy |
| 9 | 3 | 0.398 | 0.398 | noisy |

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
