# Body Profile Calibration Report

- generated_utc: `2026-03-06T03:33:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `54`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.222 | 0.106 | loosen_duration+loosen_health | acceptable |
| standard | 0.222 | 0.106 | loosen_duration+loosen_health | acceptable |
| strict | 0.481 | 0.404 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.12963`
- observed_false_regression_rate: `0.092593`
```json
{
  "duration_drift_p90": 0.304917,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.308 | 0.192 | noisy |
| 3 | 1 | 0.096 | 0.058 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.440 | 0.240 | noisy |
| 5 | 1 | 0.160 | 0.080 | acceptable |
| 5 | 2 | 0.040 | 0.040 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.500 | 0.208 | noisy |
| 7 | 1 | 0.271 | 0.146 | acceptable |
| 7 | 2 | 0.083 | 0.062 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.565 | 0.174 | noisy |
| 9 | 1 | 0.326 | 0.152 | noisy |
| 9 | 2 | 0.152 | 0.087 | acceptable |
| 9 | 3 | 0.022 | 0.022 | acceptable |

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
