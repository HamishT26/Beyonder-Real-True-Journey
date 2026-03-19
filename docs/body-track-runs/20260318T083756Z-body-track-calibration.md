# Body Profile Calibration Report

- generated_utc: `2026-03-18T08:37:56+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `215`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.479 | 0.462 | loosen_duration+tighten_health | noisy |
| standard | 0.479 | 0.462 | loosen_duration+tighten_health | noisy |
| strict | 0.823 | 0.817 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.288372`
- observed_false_regression_rate: `0.27907`
```json
{
  "duration_drift_p90": 1.113076,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.676 | 0.648 | noisy |
| 3 | 1 | 0.192 | 0.183 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.820 | 0.773 | noisy |
| 5 | 1 | 0.498 | 0.479 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.009 | 0.009 | acceptable |
| 7 | 0 | 0.876 | 0.809 | noisy |
| 7 | 1 | 0.699 | 0.670 | noisy |
| 7 | 2 | 0.368 | 0.364 | noisy |
| 7 | 3 | 0.096 | 0.096 | acceptable |
| 9 | 0 | 0.903 | 0.816 | noisy |
| 9 | 1 | 0.812 | 0.773 | noisy |
| 9 | 2 | 0.560 | 0.546 | noisy |
| 9 | 3 | 0.285 | 0.285 | noisy |

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
