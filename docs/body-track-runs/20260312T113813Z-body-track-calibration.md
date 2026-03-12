# Body Profile Calibration Report

- generated_utc: `2026-03-12T11:38:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `161`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.373 | 0.344 | loosen_duration+tighten_health | noisy |
| standard | 0.373 | 0.344 | loosen_duration+tighten_health | noisy |
| strict | 0.764 | 0.753 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.267081`
- observed_false_regression_rate: `0.254658`
```json
{
  "duration_drift_p90": 1.01053,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.629 | 0.591 | noisy |
| 3 | 1 | 0.164 | 0.151 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.783 | 0.720 | noisy |
| 5 | 1 | 0.427 | 0.401 | noisy |
| 5 | 2 | 0.121 | 0.121 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.839 | 0.748 | noisy |
| 7 | 1 | 0.639 | 0.600 | noisy |
| 7 | 2 | 0.323 | 0.316 | noisy |
| 7 | 3 | 0.090 | 0.090 | acceptable |
| 9 | 0 | 0.869 | 0.752 | noisy |
| 9 | 1 | 0.758 | 0.706 | noisy |
| 9 | 2 | 0.503 | 0.484 | noisy |
| 9 | 3 | 0.268 | 0.268 | noisy |

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
