# Body Profile Calibration Report

- generated_utc: `2026-03-20T23:01:08+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `222`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.495 | 0.479 | loosen_duration+tighten_health | noisy |
| standard | 0.495 | 0.479 | loosen_duration+tighten_health | noisy |
| strict | 0.829 | 0.823 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.301802`
- observed_false_regression_rate: `0.292793`
```json
{
  "duration_drift_p90": 1.116875,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.686 | 0.659 | noisy |
| 3 | 1 | 0.209 | 0.200 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.826 | 0.780 | noisy |
| 5 | 1 | 0.514 | 0.495 | noisy |
| 5 | 2 | 0.147 | 0.147 | acceptable |
| 5 | 3 | 0.023 | 0.023 | acceptable |
| 7 | 0 | 0.880 | 0.815 | noisy |
| 7 | 1 | 0.708 | 0.681 | noisy |
| 7 | 2 | 0.389 | 0.384 | noisy |
| 7 | 3 | 0.111 | 0.111 | acceptable |
| 9 | 0 | 0.907 | 0.822 | noisy |
| 9 | 1 | 0.818 | 0.780 | noisy |
| 9 | 2 | 0.575 | 0.561 | noisy |
| 9 | 3 | 0.308 | 0.308 | noisy |

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
