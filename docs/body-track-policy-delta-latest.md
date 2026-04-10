# Body Profile Policy Delta Report

- generated_utc: `2026-04-10T16:09:46+00:00`
- overall_status: **PASS**
- apply_mode: `False`
- policy_updated: `False`
- history_samples: `470`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.043 | 0.064 | 0.028 | 0.050 | keep |
| standard | 0.017 | 0.064 | 0.002 | 0.050 | keep |
| strict | 0.043 | 0.064 | 0.028 | 0.050 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 3} | {'window_size': 3, 'max_regressions': 3} | 0.000 | 0.000 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
