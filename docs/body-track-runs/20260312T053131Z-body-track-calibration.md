# Body Profile Calibration Report

- generated_utc: `2026-03-12T05:31:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `149`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.376 | 0.345 | loosen_duration+tighten_health | noisy |
| standard | 0.376 | 0.345 | loosen_duration+tighten_health | noisy |
| strict | 0.752 | 0.739 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.268456`
- observed_false_regression_rate: `0.255034`
```json
{
  "duration_drift_p90": 1.01777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.633 | 0.592 | noisy |
| 3 | 1 | 0.177 | 0.163 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.786 | 0.717 | noisy |
| 5 | 1 | 0.434 | 0.407 | noisy |
| 5 | 2 | 0.124 | 0.124 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.832 | 0.734 | noisy |
| 7 | 1 | 0.643 | 0.601 | noisy |
| 7 | 2 | 0.322 | 0.315 | noisy |
| 7 | 3 | 0.098 | 0.098 | acceptable |
| 9 | 0 | 0.858 | 0.730 | noisy |
| 9 | 1 | 0.752 | 0.695 | noisy |
| 9 | 2 | 0.504 | 0.482 | noisy |
| 9 | 3 | 0.277 | 0.277 | noisy |

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
