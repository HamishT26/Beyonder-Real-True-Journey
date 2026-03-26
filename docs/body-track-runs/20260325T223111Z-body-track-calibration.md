# Body Profile Calibration Report

- generated_utc: `2026-03-25T22:31:11+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `315`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.629 | 0.620 | loosen_duration+tighten_health | noisy |
| standard | 0.629 | 0.620 | loosen_duration+tighten_health | noisy |
| strict | 0.879 | 0.877 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.320635`
- observed_false_regression_rate: `0.314286`
```json
{
  "duration_drift_p90": 1.409125,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.722 | 0.703 | noisy |
| 3 | 1 | 0.227 | 0.220 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.868 | 0.836 | noisy |
| 5 | 1 | 0.550 | 0.537 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.913 | 0.867 | noisy |
| 7 | 1 | 0.748 | 0.728 | noisy |
| 7 | 2 | 0.443 | 0.440 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.935 | 0.876 | noisy |
| 9 | 1 | 0.853 | 0.827 | noisy |
| 9 | 2 | 0.632 | 0.622 | noisy |
| 9 | 3 | 0.355 | 0.355 | noisy |

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
