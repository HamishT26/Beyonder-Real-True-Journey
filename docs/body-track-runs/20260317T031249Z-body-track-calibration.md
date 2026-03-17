# Body Profile Calibration Report

- generated_utc: `2026-03-17T03:12:49+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `195`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.446 | 0.426 | loosen_duration+tighten_health | noisy |
| standard | 0.446 | 0.426 | loosen_duration+tighten_health | noisy |
| strict | 0.805 | 0.798 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.282051`
- observed_false_regression_rate: `0.271795`
```json
{
  "duration_drift_p90": 1.106906,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.658 | 0.627 | noisy |
| 3 | 1 | 0.192 | 0.181 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.806 | 0.754 | noisy |
| 5 | 1 | 0.482 | 0.461 | noisy |
| 5 | 2 | 0.141 | 0.141 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.868 | 0.794 | noisy |
| 7 | 1 | 0.683 | 0.651 | noisy |
| 7 | 2 | 0.370 | 0.365 | noisy |
| 7 | 3 | 0.106 | 0.106 | acceptable |
| 9 | 0 | 0.893 | 0.797 | noisy |
| 9 | 1 | 0.797 | 0.754 | noisy |
| 9 | 2 | 0.556 | 0.540 | noisy |
| 9 | 3 | 0.305 | 0.305 | noisy |

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
