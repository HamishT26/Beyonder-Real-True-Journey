# Body Profile Calibration Report

- generated_utc: `2026-04-08T14:28:46+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `454`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.515 | 0.508 | loosen_duration+tighten_health | noisy |
| standard | 0.515 | 0.508 | loosen_duration+tighten_health | noisy |
| strict | 0.879 | 0.877 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.312775`
- observed_false_regression_rate: `0.30837`
```json
{
  "duration_drift_p90": 1.107951,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.710 | 0.697 | noisy |
| 3 | 1 | 0.217 | 0.212 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.851 | 0.829 | noisy |
| 5 | 1 | 0.540 | 0.531 | noisy |
| 5 | 2 | 0.169 | 0.169 | noisy |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.904 | 0.873 | noisy |
| 7 | 1 | 0.721 | 0.708 | noisy |
| 7 | 2 | 0.444 | 0.442 | noisy |
| 7 | 3 | 0.123 | 0.123 | acceptable |
| 9 | 0 | 0.933 | 0.892 | noisy |
| 9 | 1 | 0.827 | 0.809 | noisy |
| 9 | 2 | 0.614 | 0.608 | noisy |
| 9 | 3 | 0.354 | 0.354 | noisy |

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
