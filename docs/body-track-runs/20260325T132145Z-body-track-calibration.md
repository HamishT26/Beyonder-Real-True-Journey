# Body Profile Calibration Report

- generated_utc: `2026-03-25T13:21:45+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `302`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.613 | 0.603 | loosen_duration+tighten_health | noisy |
| standard | 0.613 | 0.603 | loosen_duration+tighten_health | noisy |
| strict | 0.874 | 0.871 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.31457`
- observed_false_regression_rate: `0.307947`
```json
{
  "duration_drift_p90": 1.287567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.693 | noisy |
| 3 | 1 | 0.220 | 0.213 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.862 | 0.829 | noisy |
| 5 | 1 | 0.537 | 0.523 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.909 | 0.861 | noisy |
| 7 | 1 | 0.740 | 0.720 | noisy |
| 7 | 2 | 0.432 | 0.429 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.932 | 0.871 | noisy |
| 9 | 1 | 0.847 | 0.820 | noisy |
| 9 | 2 | 0.622 | 0.612 | noisy |
| 9 | 3 | 0.350 | 0.350 | noisy |

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
