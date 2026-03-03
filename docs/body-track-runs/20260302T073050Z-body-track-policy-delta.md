# Body Profile Policy Delta Report

- generated_utc: `2026-03-02T07:30:50+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `True`
- history_samples: `28`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.214 | 0.214 | 0.000 | 0.000 | keep |
| standard | 0.250 | 0.214 | 0.045 | 0.000 | apply_recommended_thresholds |
| strict | 0.250 | 0.214 | 0.045 | 0.000 | apply_recommended_thresholds |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 5, 'max_regressions': 2} | {'window_size': 5, 'max_regressions': 0} | 0.000 | 0.208 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {
    "standard": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 1.274,
      "min_health_score": 32.83
    },
    "strict": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 1.274,
      "min_health_score": 32.83
    }
  },
  "regression_window_policy": null
}
```
