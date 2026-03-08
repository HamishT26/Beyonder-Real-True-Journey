# Body Profile Calibration Report

- generated_utc: `2026-03-08T12:28:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `98`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.235 | 0.176 | loosen_duration+loosen_health | noisy |
| standard | 0.235 | 0.176 | loosen_duration+loosen_health | noisy |
| strict | 0.643 | 0.615 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.214286`
- observed_false_regression_rate: `0.193878`
```json
{
  "duration_drift_p90": 0.718997,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.500 | 0.438 | noisy |
| 3 | 1 | 0.135 | 0.115 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.681 | 0.574 | noisy |
| 5 | 1 | 0.266 | 0.223 | noisy |
| 5 | 2 | 0.096 | 0.096 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.739 | 0.587 | noisy |
| 7 | 1 | 0.478 | 0.413 | noisy |
| 7 | 2 | 0.174 | 0.163 | noisy |
| 7 | 3 | 0.065 | 0.065 | acceptable |
| 9 | 0 | 0.778 | 0.578 | noisy |
| 9 | 1 | 0.611 | 0.522 | noisy |
| 9 | 2 | 0.300 | 0.267 | noisy |
| 9 | 3 | 0.144 | 0.144 | acceptable |

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
