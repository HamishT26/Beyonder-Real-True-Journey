# Body Profile Calibration Report

- generated_utc: `2026-03-17T21:49:08+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `201`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.458 | 0.438 | loosen_duration+tighten_health | noisy |
| standard | 0.458 | 0.438 | loosen_duration+tighten_health | noisy |
| strict | 0.811 | 0.804 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.283582`
- observed_false_regression_rate: `0.273632`
```json
{
  "duration_drift_p90": 1.110475,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.658 | 0.628 | noisy |
| 3 | 1 | 0.196 | 0.186 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.807 | 0.756 | noisy |
| 5 | 1 | 0.487 | 0.467 | noisy |
| 5 | 2 | 0.137 | 0.137 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.867 | 0.795 | noisy |
| 7 | 1 | 0.682 | 0.651 | noisy |
| 7 | 2 | 0.359 | 0.354 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.896 | 0.803 | noisy |
| 9 | 1 | 0.798 | 0.756 | noisy |
| 9 | 2 | 0.539 | 0.523 | noisy |
| 9 | 3 | 0.295 | 0.295 | noisy |

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
