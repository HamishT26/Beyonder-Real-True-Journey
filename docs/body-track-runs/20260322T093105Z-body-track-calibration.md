# Body Profile Calibration Report

- generated_utc: `2026-03-22T09:31:05+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `241`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.531 | 0.517 | loosen_duration+tighten_health | noisy |
| standard | 0.531 | 0.517 | loosen_duration+tighten_health | noisy |
| strict | 0.842 | 0.838 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315353`
- observed_false_regression_rate: `0.307054`
```json
{
  "duration_drift_p90": 1.230996,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.703 | 0.678 | noisy |
| 3 | 1 | 0.226 | 0.218 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.840 | 0.797 | noisy |
| 5 | 1 | 0.544 | 0.527 | noisy |
| 5 | 2 | 0.169 | 0.169 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.889 | 0.830 | noisy |
| 7 | 1 | 0.732 | 0.706 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.914 | 0.837 | noisy |
| 9 | 1 | 0.833 | 0.798 | noisy |
| 9 | 2 | 0.609 | 0.597 | noisy |
| 9 | 3 | 0.356 | 0.356 | noisy |

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
