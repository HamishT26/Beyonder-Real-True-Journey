# Body Profile Calibration Report

- generated_utc: `2026-03-14T10:26:18+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `175`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.400 | 0.375 | loosen_duration+tighten_health | noisy |
| standard | 0.400 | 0.375 | loosen_duration+tighten_health | noisy |
| strict | 0.783 | 0.774 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.28`
- observed_false_regression_rate: `0.268571`
```json
{
  "duration_drift_p90": 1.087142,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.659 | 0.624 | noisy |
| 3 | 1 | 0.179 | 0.168 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.801 | 0.743 | noisy |
| 5 | 1 | 0.468 | 0.444 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.852 | 0.769 | noisy |
| 7 | 1 | 0.663 | 0.627 | noisy |
| 7 | 2 | 0.355 | 0.349 | noisy |
| 7 | 3 | 0.107 | 0.107 | acceptable |
| 9 | 0 | 0.880 | 0.772 | noisy |
| 9 | 1 | 0.772 | 0.725 | noisy |
| 9 | 2 | 0.521 | 0.503 | noisy |
| 9 | 3 | 0.299 | 0.299 | noisy |

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
