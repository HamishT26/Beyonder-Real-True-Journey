# Body Profile Calibration Report

- generated_utc: `2026-03-22T12:46:00+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `249`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.546 | 0.533 | loosen_duration+tighten_health | noisy |
| standard | 0.546 | 0.533 | loosen_duration+tighten_health | noisy |
| strict | 0.847 | 0.843 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313253`
- observed_false_regression_rate: `0.305221`
```json
{
  "duration_drift_p90": 1.369982,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.704 | 0.680 | noisy |
| 3 | 1 | 0.223 | 0.215 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.845 | 0.804 | noisy |
| 5 | 1 | 0.547 | 0.531 | noisy |
| 5 | 2 | 0.163 | 0.163 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.893 | 0.835 | noisy |
| 7 | 1 | 0.737 | 0.712 | noisy |
| 7 | 2 | 0.436 | 0.432 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.917 | 0.842 | noisy |
| 9 | 1 | 0.838 | 0.805 | noisy |
| 9 | 2 | 0.622 | 0.610 | noisy |
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
