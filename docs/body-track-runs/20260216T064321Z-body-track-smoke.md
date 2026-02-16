# Body Track Smoke Report

- generated_utc: `2026-02-16T06:43:21+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.187552`
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
    "actual": 0.187552,
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
| run_gmut_simulation | PASS | 0 | 0.117 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
Registered DID: did:freed:c82608022b8b4737af1d649fee7dd978
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6331056418447994, 'entropy_bits': 0.9482576163717027, 'top_states': [{'state': 0, 'probability': 0.6331056418447994}, {'state': 1, 'probability': 0.3668943581552005}], 'empirical_top_states': [{'state': 0, 'count': 324, 'frequency': 0.6328125}, {'state': 1, 'count': 188, 'frequency': 0.3671875}], 'expected_state_index': 0.3668943581552005, 'measurement_histogram': [324, 188]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6331056418447994, 'entropy_bits': 0.9482576163717027, 'top_states': [{'state': 0, 'probability': 0.6331056418447994}, {'state': 1, 'probability': 0.3668943581552005}], 'empirical_top_states': [{'state': 0, 'count': 324, 'frequency': 0.6328125}, {'state': 1, 'count': 188, 'frequency': 0.3671875}], 'expected_state_index': 0.3668943581552005, 'measurement_histogram': [324, 188]}, 'waste_energy': 8.319878917422987, 'exotic_energy_generated': 2.2132526116153244, 'total_exotic_energy': 2.2132526116153244}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5761739008220842, 'entropy_bits': 0.983192256817014, 'top_states': [{'state': 1, 'probability': 0.5761739008220842}, {'state': 0, 'probability': 0.4238260991779159}], 'empirical_top_states': [{'state': 1, 'count': 295, 'frequency': 0.576171875}, {'state': 0, 'count': 217, 'frequency': 0.423828125}], 'expected_state_index': 0.5761739008220842, 'measurement_histogram': [217, 295]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5761739008220842, 'entropy_bits': 0.983192256817014, 'top_states': [{'state': 1, 'probability': 0.5761739008220842}, {'state': 0, 'probability': 0.4238260991779159}], 'empirical_top_states': [{'state': 1, 'count': 295, 'frequency': 0.576171875}, {'state': 0, 'count': 217, 'frequency': 0.423828125}], 'expected_state_index': 0.5761739008220842, 'measurement_histogram': [217, 295]}, 'waste_energy': 7.925501845991507, 'exotic_energy_generated': 1.9503345639943375, 'total_exotic_energy': 4.163587175609662}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.081794,
  "final_total_exotic_energy": 4.163587
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.117`

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
