# Body Profile Calibration Report

- generated_utc: `2026-03-18T02:41:17+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `211`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.479 | 0.461 | loosen_duration+tighten_health | noisy |
| standard | 0.479 | 0.461 | loosen_duration+tighten_health | noisy |
| strict | 0.820 | 0.814 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.2891`
- observed_false_regression_rate: `0.279621`
```json
{
  "duration_drift_p90": 1.110475,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.670 | 0.641 | noisy |
| 3 | 1 | 0.191 | 0.182 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.816 | 0.768 | noisy |
| 5 | 1 | 0.488 | 0.469 | noisy |
| 5 | 2 | 0.130 | 0.130 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.873 | 0.805 | noisy |
| 7 | 1 | 0.693 | 0.663 | noisy |
| 7 | 2 | 0.356 | 0.351 | noisy |
| 7 | 3 | 0.098 | 0.098 | acceptable |
| 9 | 0 | 0.901 | 0.813 | noisy |
| 9 | 1 | 0.808 | 0.768 | noisy |
| 9 | 2 | 0.552 | 0.537 | noisy |
| 9 | 3 | 0.281 | 0.281 | noisy |

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
