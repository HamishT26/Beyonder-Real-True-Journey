# Body Profile Calibration Report

- generated_utc: `2026-03-25T20:01:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `312`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.625 | 0.616 | loosen_duration+tighten_health | noisy |
| standard | 0.625 | 0.616 | loosen_duration+tighten_health | noisy |
| strict | 0.878 | 0.875 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317308`
- observed_false_regression_rate: `0.310897`
```json
{
  "duration_drift_p90": 1.287567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.719 | 0.700 | noisy |
| 3 | 1 | 0.219 | 0.213 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.867 | 0.834 | noisy |
| 5 | 1 | 0.545 | 0.532 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.912 | 0.866 | noisy |
| 7 | 1 | 0.745 | 0.725 | noisy |
| 7 | 2 | 0.438 | 0.435 | noisy |
| 7 | 3 | 0.127 | 0.127 | acceptable |
| 9 | 0 | 0.934 | 0.875 | noisy |
| 9 | 1 | 0.852 | 0.826 | noisy |
| 9 | 2 | 0.628 | 0.618 | noisy |
| 9 | 3 | 0.349 | 0.349 | noisy |

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
