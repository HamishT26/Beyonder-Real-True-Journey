# Body Profile Calibration Report

- generated_utc: `2026-03-17T02:44:17+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `194`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.443 | 0.422 | loosen_duration+tighten_health | noisy |
| standard | 0.443 | 0.422 | loosen_duration+tighten_health | noisy |
| strict | 0.804 | 0.797 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.283505`
- observed_false_regression_rate: `0.273196`
```json
{
  "duration_drift_p90": 1.107951,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.661 | 0.630 | noisy |
| 3 | 1 | 0.193 | 0.182 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.811 | 0.758 | noisy |
| 5 | 1 | 0.484 | 0.463 | noisy |
| 5 | 2 | 0.142 | 0.142 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.867 | 0.793 | noisy |
| 7 | 1 | 0.686 | 0.654 | noisy |
| 7 | 2 | 0.372 | 0.367 | noisy |
| 7 | 3 | 0.106 | 0.106 | acceptable |
| 9 | 0 | 0.892 | 0.796 | noisy |
| 9 | 1 | 0.796 | 0.753 | noisy |
| 9 | 2 | 0.559 | 0.543 | noisy |
| 9 | 3 | 0.306 | 0.306 | noisy |

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
