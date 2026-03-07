# Body Profile Calibration Report

- generated_utc: `2026-03-07T02:35:16+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `82`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.207 | 0.133 | loosen_duration+loosen_health | acceptable |
| standard | 0.207 | 0.133 | loosen_duration+loosen_health | acceptable |
| strict | 0.573 | 0.533 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.182927`
- observed_false_regression_rate: `0.158537`
```json
{
  "duration_drift_p90": 0.325547,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.450 | 0.375 | noisy |
| 3 | 1 | 0.113 | 0.087 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.615 | 0.487 | noisy |
| 5 | 1 | 0.244 | 0.192 | noisy |
| 5 | 2 | 0.077 | 0.077 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.684 | 0.500 | noisy |
| 7 | 1 | 0.395 | 0.316 | noisy |
| 7 | 2 | 0.171 | 0.158 | noisy |
| 7 | 3 | 0.053 | 0.053 | acceptable |
| 9 | 0 | 0.730 | 0.486 | noisy |
| 9 | 1 | 0.527 | 0.419 | noisy |
| 9 | 2 | 0.257 | 0.216 | noisy |
| 9 | 3 | 0.135 | 0.135 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
