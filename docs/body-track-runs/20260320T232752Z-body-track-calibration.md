# Body Profile Calibration Report

- generated_utc: `2026-03-20T23:27:52+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `224`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.500 | 0.484 | loosen_duration+tighten_health | noisy |
| standard | 0.500 | 0.484 | loosen_duration+tighten_health | noisy |
| strict | 0.830 | 0.825 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.303571`
- observed_false_regression_rate: `0.294643`
```json
{
  "duration_drift_p90": 1.116375,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.689 | 0.662 | noisy |
| 3 | 1 | 0.207 | 0.198 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.827 | 0.782 | noisy |
| 5 | 1 | 0.518 | 0.500 | noisy |
| 5 | 2 | 0.155 | 0.155 | noisy |
| 5 | 3 | 0.023 | 0.023 | acceptable |
| 7 | 0 | 0.881 | 0.817 | noisy |
| 7 | 1 | 0.711 | 0.683 | noisy |
| 7 | 2 | 0.394 | 0.390 | noisy |
| 7 | 3 | 0.119 | 0.119 | acceptable |
| 9 | 0 | 0.907 | 0.824 | noisy |
| 9 | 1 | 0.819 | 0.782 | noisy |
| 9 | 2 | 0.579 | 0.565 | noisy |
| 9 | 3 | 0.315 | 0.315 | noisy |

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
