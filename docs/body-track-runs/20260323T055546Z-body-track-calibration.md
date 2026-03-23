# Body Profile Calibration Report

- generated_utc: `2026-03-23T05:55:46+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `280`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| standard | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| strict | 0.864 | 0.861 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.307143`
- observed_false_regression_rate: `0.3`
```json
{
  "duration_drift_p90": 1.237281,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.698 | 0.676 | noisy |
| 3 | 1 | 0.216 | 0.209 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.851 | 0.815 | noisy |
| 5 | 1 | 0.525 | 0.511 | noisy |
| 5 | 2 | 0.163 | 0.163 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.901 | 0.850 | noisy |
| 7 | 1 | 0.730 | 0.708 | noisy |
| 7 | 2 | 0.420 | 0.416 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.926 | 0.860 | noisy |
| 9 | 1 | 0.838 | 0.809 | noisy |
| 9 | 2 | 0.614 | 0.603 | noisy |
| 9 | 3 | 0.338 | 0.338 | noisy |

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
