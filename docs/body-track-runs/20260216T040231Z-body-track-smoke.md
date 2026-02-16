# Body Track Smoke Report

- generated_utc: `2026-02-16T04:02:31+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.148326`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- trend: `stable`
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.148326,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.034 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.084 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.030`

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
- duration_seconds: `0.034`

### stdout (trimmed)
```
Registered DID: did:freed:bca4f0fb604048c698883f4164a11679
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7473994522805006, 'entropy_bits': 0.8153739369150148, 'top_states': [{'state': 0, 'probability': 0.7473994522805006}, {'state': 1, 'probability': 0.2526005477194993}], 'empirical_top_states': [{'state': 0, 'count': 383, 'frequency': 0.748046875}, {'state': 1, 'count': 129, 'frequency': 0.251953125}], 'expected_state_index': 0.2526005477194993, 'measurement_histogram': [383, 129]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7473994522805006, 'entropy_bits': 0.8153739369150148, 'top_states': [{'state': 0, 'probability': 0.7473994522805006}, {'state': 1, 'probability': 0.2526005477194993}], 'empirical_top_states': [{'state': 0, 'count': 383, 'frequency': 0.748046875}, {'state': 1, 'count': 129, 'frequency': 0.251953125}], 'expected_state_index': 0.2526005477194993, 'measurement_histogram': [383, 129]}, 'waste_energy': 7.403212948878263, 'exotic_energy_generated': 1.6021419659188416, 'total_exotic_energy': 1.6021419659188416}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7489538203393586, 'entropy_bits': 0.8129320731817364, 'top_states': [{'state': 0, 'probability': 0.7489538203393586}, {'state': 1, 'probability': 0.2510461796606414}], 'empirical_top_states': [{'state': 0, 'count': 383, 'frequency': 0.748046875}, {'state': 1, 'count': 129, 'frequency': 0.251953125}], 'expected_state_index': 0.2510461796606414, 'measurement_histogram': [383, 129]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7489538203393586, 'entropy_bits': 0.8129320731817364, 'top_states': [{'state': 0, 'probability': 0.7489538203393586}, {'state': 1, 'probability': 0.2510461796606414}], 'empirical_top_states': [{'state': 0, 'count': 383, 'frequency': 0.748046875}, {'state': 1, 'count': 129, 'frequency': 0.251953125}], 'expected_state_index': 0.2510461796606414, 'measurement_histogram': [383, 129]}, 'waste_energy': 7.345281905632655, 'exotic_energy_generated': 1.5635212704217698, 'total_exotic_energy': 3.1656632363406114}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.582832,
  "final_total_exotic_energy": 3.165663
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.084`

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
