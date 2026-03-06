# Body Profile Policy Delta Report

- generated_utc: `2026-03-06T02:24:55+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `False`
- history_samples: `45`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.200 | 0.200 | 0.053 | 0.053 | keep |
| standard | 0.200 | 0.200 | 0.053 | 0.053 | keep |
| strict | 0.200 | 0.200 | 0.053 | 0.053 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 5, 'max_regressions': 2} | {'window_size': 9, 'max_regressions': 1} | 0.000 | 0.189 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
