# Body Profile Calibration Report

- generated_utc: `2026-03-11T04:31:27+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `143`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.350 | 0.316 | loosen_duration+tighten_health | noisy |
| standard | 0.350 | 0.316 | loosen_duration+tighten_health | noisy |
| strict | 0.741 | 0.728 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.265734`
- observed_false_regression_rate: `0.251748`
```json
{
  "duration_drift_p90": 1.004965,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.631 | 0.589 | noisy |
| 3 | 1 | 0.170 | 0.156 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.784 | 0.712 | noisy |
| 5 | 1 | 0.432 | 0.403 | noisy |
| 5 | 2 | 0.129 | 0.129 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.825 | 0.723 | noisy |
| 7 | 1 | 0.642 | 0.599 | noisy |
| 7 | 2 | 0.336 | 0.328 | noisy |
| 7 | 3 | 0.102 | 0.102 | acceptable |
| 9 | 0 | 0.852 | 0.719 | noisy |
| 9 | 1 | 0.741 | 0.681 | noisy |
| 9 | 2 | 0.511 | 0.489 | noisy |
| 9 | 3 | 0.289 | 0.289 | noisy |

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
