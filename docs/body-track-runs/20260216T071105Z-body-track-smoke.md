# Body Track Smoke Report

- generated_utc: `2026-02-16T07:11:05+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.19063`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- profile: `quick`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.5,
  "min_health_score": 94.0
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.19063,
    "threshold": 1.5
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 94.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.033 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.037 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.121 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.033`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
(empty)
```

## run_full_orchestrator_demo

- returncode: `0`
- duration_seconds: `0.037`

### stdout (trimmed)
```
Registered DID: did:freed:f6c2c2cd14cf417ca231eb102d160263
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6765625961764659, 'entropy_bits': 0.9080804109550238, 'top_states': [{'state': 1, 'probability': 0.6765625961764659}, {'state': 0, 'probability': 0.3234374038235342}], 'empirical_top_states': [{'state': 1, 'count': 346, 'frequency': 0.67578125}, {'state': 0, 'count': 166, 'frequency': 0.32421875}], 'expected_state_index': 0.6765625961764659, 'measurement_histogram': [166, 346]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6765625961764659, 'entropy_bits': 0.9080804109550238, 'top_states': [{'state': 1, 'probability': 0.6765625961764659}, {'state': 0, 'probability': 0.3234374038235342}], 'empirical_top_states': [{'state': 1, 'count': 346, 'frequency': 0.67578125}, {'state': 0, 'count': 166, 'frequency': 0.32421875}], 'expected_state_index': 0.6765625961764659, 'measurement_histogram': [166, 346]}, 'waste_energy': 7.459466660068157, 'exotic_energy_generated': 1.6396444400454384, 'total_exotic_energy': 1.6396444400454384}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5726166387051229, 'entropy_bits': 0.9847308850100759, 'top_states': [{'state': 0, 'probability': 0.5726166387051229}, {'state': 1, 'probability': 0.4273833612948771}], 'empirical_top_states': [{'state': 0, 'count': 293, 'frequency': 0.572265625}, {'state': 1, 'count': 219, 'frequency': 0.427734375}], 'expected_state_index': 0.4273833612948771, 'measurement_histogram': [293, 219]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5726166387051229, 'entropy_bits': 0.9847308850100759, 'top_states': [{'state': 0, 'probability': 0.5726166387051229}, {'state': 1, 'probability': 0.4273833612948771}], 'empirical_top_states': [{'state': 0, 'count': 293, 'frequency': 0.572265625}, {'state': 1, 'count': 219, 'frequency': 0.427734375}], 'expected_state_index': 0.4273833612948771, 'measurement_histogram': [293, 219]}, 'waste_energy': 7.3312275051150255, 'exotic_energy_generated': 1.5541516700766833, 'total_exotic_energy': 3.193796110122122}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.596898,
  "final_total_exotic_energy": 3.193796
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.121`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0100: energy density ratio = 1.00993
Gamma=0.0500: energy density ratio = 1.04964
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "gamma_count": 3,
  "gamma_ratios": {
    "0.0000": 1.0,
    "0.0100": 1.00993,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
