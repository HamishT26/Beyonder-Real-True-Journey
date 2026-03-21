# Body Profile Calibration Report

- generated_utc: `2026-03-21T01:14:22+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `229`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.511 | 0.495 | loosen_duration+tighten_health | noisy |
| standard | 0.511 | 0.495 | loosen_duration+tighten_health | noisy |
| strict | 0.834 | 0.829 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310044`
- observed_false_regression_rate: `0.30131`
```json
{
  "duration_drift_p90": 1.146815,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.696 | 0.670 | noisy |
| 3 | 1 | 0.220 | 0.211 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.831 | 0.787 | noisy |
| 5 | 1 | 0.529 | 0.511 | noisy |
| 5 | 2 | 0.164 | 0.164 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.883 | 0.821 | noisy |
| 7 | 1 | 0.717 | 0.691 | noisy |
| 7 | 2 | 0.408 | 0.404 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.910 | 0.828 | noisy |
| 9 | 1 | 0.824 | 0.787 | noisy |
| 9 | 2 | 0.588 | 0.575 | noisy |
| 9 | 3 | 0.330 | 0.330 | noisy |

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
