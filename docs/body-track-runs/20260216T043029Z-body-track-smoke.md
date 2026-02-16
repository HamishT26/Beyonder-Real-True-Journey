# Body Track Smoke Report

- generated_utc: `2026-02-16T04:30:29+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.194269`
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
    "actual": 0.194269,
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
| compile_python_modules | PASS | 0 | 0.033 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.036 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.125 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.036`

### stdout (trimmed)
```
Registered DID: did:freed:9d99756e50ad4f64ad31c136c039b0ca
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6538956167755512, 'entropy_bits': 0.9305407372248548, 'top_states': [{'state': 0, 'probability': 0.6538956167755512}, {'state': 1, 'probability': 0.34610438322444875}], 'empirical_top_states': [{'state': 0, 'count': 335, 'frequency': 0.654296875}, {'state': 1, 'count': 177, 'frequency': 0.345703125}], 'expected_state_index': 0.34610438322444875, 'measurement_histogram': [335, 177]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6538956167755512, 'entropy_bits': 0.9305407372248548, 'top_states': [{'state': 0, 'probability': 0.6538956167755512}, {'state': 1, 'probability': 0.34610438322444875}], 'empirical_top_states': [{'state': 0, 'count': 335, 'frequency': 0.654296875}, {'state': 1, 'count': 177, 'frequency': 0.345703125}], 'expected_state_index': 0.34610438322444875, 'measurement_histogram': [335, 177]}, 'waste_energy': 8.157920335037664, 'exotic_energy_generated': 2.105280223358443, 'total_exotic_energy': 2.105280223358443}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7065913692599561, 'entropy_bits': 0.8730837886616531, 'top_states': [{'state': 1, 'probability': 0.7065913692599561}, {'state': 0, 'probability': 0.2934086307400438}], 'empirical_top_states': [{'state': 1, 'count': 362, 'frequency': 0.70703125}, {'state': 0, 'count': 150, 'frequency': 0.29296875}], 'expected_state_index': 0.7065913692599561, 'measurement_histogram': [150, 362]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7065913692599561, 'entropy_bits': 0.8730837886616531, 'top_states': [{'state': 1, 'probability': 0.7065913692599561}, {'state': 0, 'probability': 0.2934086307400438}], 'empirical_top_states': [{'state': 1, 'count': 362, 'frequency': 0.70703125}, {'state': 0, 'count': 150, 'frequency': 0.29296875}], 'expected_state_index': 0.7065913692599561, 'measurement_histogram': [150, 362]}, 'waste_energy': 7.987198002681634, 'exotic_energy_generated': 1.9914653351210885, 'total_exotic_energy': 4.096745558479531}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.048373,
  "final_total_exotic_energy": 4.096746
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.125`

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
