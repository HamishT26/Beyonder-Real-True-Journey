# Body Track Smoke Report

- generated_utc: `2026-02-16T02:00:07+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.153233`
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
    "actual": 0.153233,
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
| compile_python_modules | PASS | 0 | 0.031 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.041 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.082 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.041`

### stdout (trimmed)
```
Registered DID: did:freed:6d4ceaf0ae7c462c820cdf767d3cd431
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7079010040586481, 'entropy_bits': 0.871417244949648, 'top_states': [{'state': 1, 'probability': 0.7079010040586481}, {'state': 0, 'probability': 0.292098995941352}], 'empirical_top_states': [{'state': 1, 'count': 362, 'frequency': 0.70703125}, {'state': 0, 'count': 150, 'frequency': 0.29296875}], 'expected_state_index': 0.7079010040586481, 'measurement_histogram': [150, 362]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7079010040586481, 'entropy_bits': 0.871417244949648, 'top_states': [{'state': 1, 'probability': 0.7079010040586481}, {'state': 0, 'probability': 0.292098995941352}], 'empirical_top_states': [{'state': 1, 'count': 362, 'frequency': 0.70703125}, {'state': 0, 'count': 150, 'frequency': 0.29296875}], 'expected_state_index': 0.7079010040586481, 'measurement_histogram': [150, 362]}, 'waste_energy': 7.688046191946823, 'exotic_energy_generated': 1.7920307946312148, 'total_exotic_energy': 1.7920307946312148}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.812440766172422, 'entropy_bits': 0.696337551325796, 'top_states': [{'state': 1, 'probability': 0.812440766172422}, {'state': 0, 'probability': 0.18755923382757805}], 'empirical_top_states': [{'state': 1, 'count': 416, 'frequency': 0.8125}, {'state': 0, 'count': 96, 'frequency': 0.1875}], 'expected_state_index': 0.812440766172422, 'measurement_histogram': [96, 416]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.812440766172422, 'entropy_bits': 0.696337551325796, 'top_states': [{'state': 1, 'probability': 0.812440766172422}, {'state': 0, 'probability': 0.18755923382757805}], 'empirical_top_states': [{'state': 1, 'count': 416, 'frequency': 0.8125}, {'state': 0, 'count': 96, 'frequency': 0.1875}], 'expected_state_index': 0.812440766172422, 'measurement_histogram': [96, 416]}, 'waste_energy': 7.734929251485883, 'exotic_energy_generated': 1.8232861676572554, 'total_exotic_energy': 3.61531696228847}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.807658,
  "final_total_exotic_energy": 3.615317
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.082`

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
