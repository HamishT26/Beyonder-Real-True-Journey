# Body Profile Calibration Report

- generated_utc: `2026-03-17T02:17:06+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `193`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.440 | 0.419 | loosen_duration+tighten_health | noisy |
| standard | 0.440 | 0.419 | loosen_duration+tighten_health | noisy |
| strict | 0.803 | 0.796 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284974`
- observed_false_regression_rate: `0.274611`
```json
{
  "duration_drift_p90": 1.108997,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.665 | 0.634 | noisy |
| 3 | 1 | 0.194 | 0.183 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.815 | 0.762 | noisy |
| 5 | 1 | 0.487 | 0.466 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.866 | 0.791 | noisy |
| 7 | 1 | 0.690 | 0.658 | noisy |
| 7 | 2 | 0.374 | 0.369 | noisy |
| 7 | 3 | 0.107 | 0.107 | acceptable |
| 9 | 0 | 0.892 | 0.795 | noisy |
| 9 | 1 | 0.795 | 0.751 | noisy |
| 9 | 2 | 0.562 | 0.546 | noisy |
| 9 | 3 | 0.308 | 0.308 | noisy |

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
