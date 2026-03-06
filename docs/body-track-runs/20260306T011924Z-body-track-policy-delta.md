# Body Profile Policy Delta Report

- generated_utc: `2026-03-06T01:19:24+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `True`
- history_samples: `44`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.227 | 0.205 | 0.081 | 0.054 | apply_recommended_thresholds |
| standard | 0.250 | 0.205 | 0.108 | 0.054 | apply_recommended_thresholds |
| strict | 0.250 | 0.205 | 0.108 | 0.054 | apply_recommended_thresholds |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 5, 'max_regressions': 2} | {'window_size': 9, 'max_regressions': 1} | 0.000 | 0.167 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {
    "quick": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 2.019,
      "min_health_score": 37.83
    },
    "standard": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 2.019,
      "min_health_score": 37.83
    },
    "strict": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 2.019,
      "min_health_score": 37.83
    }
  },
  "regression_window_policy": null
}
```
