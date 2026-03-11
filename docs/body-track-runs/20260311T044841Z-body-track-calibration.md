# Body Profile Calibration Report

- generated_utc: `2026-03-11T04:48:41+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `144`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.354 | 0.321 | loosen_duration+tighten_health | noisy |
| standard | 0.354 | 0.321 | loosen_duration+tighten_health | noisy |
| strict | 0.743 | 0.730 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.263889`
- observed_false_regression_rate: `0.25`
```json
{
  "duration_drift_p90": 1.003021,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.627 | 0.585 | noisy |
| 3 | 1 | 0.169 | 0.155 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.786 | 0.714 | noisy |
| 5 | 1 | 0.429 | 0.400 | noisy |
| 5 | 2 | 0.129 | 0.129 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.826 | 0.725 | noisy |
| 7 | 1 | 0.638 | 0.594 | noisy |
| 7 | 2 | 0.333 | 0.326 | noisy |
| 7 | 3 | 0.101 | 0.101 | acceptable |
| 9 | 0 | 0.853 | 0.721 | noisy |
| 9 | 1 | 0.743 | 0.684 | noisy |
| 9 | 2 | 0.507 | 0.485 | noisy |
| 9 | 3 | 0.287 | 0.287 | noisy |

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
