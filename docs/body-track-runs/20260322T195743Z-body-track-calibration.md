# Body Profile Calibration Report

- generated_utc: `2026-03-22T19:57:43+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `257`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.560 | 0.548 | loosen_duration+tighten_health | noisy |
| standard | 0.560 | 0.548 | loosen_duration+tighten_health | noisy |
| strict | 0.852 | 0.848 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.319066`
- observed_false_regression_rate: `0.311284`
```json
{
  "duration_drift_p90": 1.424924,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.714 | 0.690 | noisy |
| 3 | 1 | 0.227 | 0.220 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.850 | 0.810 | noisy |
| 5 | 1 | 0.553 | 0.538 | noisy |
| 5 | 2 | 0.178 | 0.178 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.896 | 0.841 | noisy |
| 7 | 1 | 0.745 | 0.721 | noisy |
| 7 | 2 | 0.442 | 0.438 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.920 | 0.847 | noisy |
| 9 | 1 | 0.843 | 0.811 | noisy |
| 9 | 2 | 0.627 | 0.614 | noisy |
| 9 | 3 | 0.357 | 0.357 | noisy |

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
