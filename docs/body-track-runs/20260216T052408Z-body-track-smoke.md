# Body Track Smoke Report

- generated_utc: `2026-02-16T05:24:08+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.137168`
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
    "actual": 0.137168,
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
| compile_python_modules | PASS | 0 | 0.031 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.034 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.072 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.031`

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
Registered DID: did:freed:23744e1e2c4a4ac8a211a941595b90ba
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5258117494701771, 'entropy_bits': 0.9980767644501445, 'top_states': [{'state': 1, 'probability': 0.5258117494701771}, {'state': 0, 'probability': 0.4741882505298229}], 'empirical_top_states': [{'state': 1, 'count': 269, 'frequency': 0.525390625}, {'state': 0, 'count': 243, 'frequency': 0.474609375}], 'expected_state_index': 0.5258117494701771, 'measurement_histogram': [243, 269]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5258117494701771, 'entropy_bits': 0.9980767644501445, 'top_states': [{'state': 1, 'probability': 0.5258117494701771}, {'state': 0, 'probability': 0.4741882505298229}], 'empirical_top_states': [{'state': 1, 'count': 269, 'frequency': 0.525390625}, {'state': 0, 'count': 243, 'frequency': 0.474609375}], 'expected_state_index': 0.5258117494701771, 'measurement_histogram': [243, 269]}, 'waste_energy': 8.458905735712442, 'exotic_energy_generated': 2.305937157141628, 'total_exotic_energy': 2.305937157141628}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.557106377422008, 'entropy_bits': 0.9905697788160263, 'top_states': [{'state': 0, 'probability': 0.557106377422008}, {'state': 1, 'probability': 0.442893622577992}], 'empirical_top_states': [{'state': 0, 'count': 285, 'frequency': 0.556640625}, {'state': 1, 'count': 227, 'frequency': 0.443359375}], 'expected_state_index': 0.442893622577992, 'measurement_histogram': [285, 227]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.557106377422008, 'entropy_bits': 0.9905697788160263, 'top_states': [{'state': 0, 'probability': 0.557106377422008}, {'state': 1, 'probability': 0.442893622577992}], 'empirical_top_states': [{'state': 0, 'count': 285, 'frequency': 0.556640625}, {'state': 1, 'count': 227, 'frequency': 0.443359375}], 'expected_state_index': 0.442893622577992, 'measurement_histogram': [285, 227]}, 'waste_energy': 6.7153641563780635, 'exotic_energy_generated': 1.1435761042520425, 'total_exotic_energy': 3.4495132613936703}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.724757,
  "final_total_exotic_energy": 3.449513
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.072`

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
