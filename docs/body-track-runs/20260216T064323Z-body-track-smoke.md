# Body Track Smoke Report

- generated_utc: `2026-02-16T06:43:23+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.12764`
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
    "actual": 0.12764,
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
| run_full_orchestrator_demo | PASS | 0 | 0.033 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.064 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.033`

### stdout (trimmed)
```
Registered DID: did:freed:88ab45487ae442f5bb76db38cb455fd4
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5667145376364962, 'entropy_bits': 0.9871192404679539, 'top_states': [{'state': 1, 'probability': 0.5667145376364962}, {'state': 0, 'probability': 0.43328546236350385}], 'empirical_top_states': [{'state': 1, 'count': 290, 'frequency': 0.56640625}, {'state': 0, 'count': 222, 'frequency': 0.43359375}], 'expected_state_index': 0.5667145376364962, 'measurement_histogram': [222, 290]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5667145376364962, 'entropy_bits': 0.9871192404679539, 'top_states': [{'state': 1, 'probability': 0.5667145376364962}, {'state': 0, 'probability': 0.43328546236350385}], 'empirical_top_states': [{'state': 1, 'count': 290, 'frequency': 0.56640625}, {'state': 0, 'count': 222, 'frequency': 0.43359375}], 'expected_state_index': 0.5667145376364962, 'measurement_histogram': [222, 290]}, 'waste_energy': 8.320178275127766, 'exotic_energy_generated': 2.21345218341851, 'total_exotic_energy': 2.21345218341851}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5667653162043083, 'entropy_bits': 0.987099566131451, 'top_states': [{'state': 1, 'probability': 0.5667653162043083}, {'state': 0, 'probability': 0.4332346837956917}], 'empirical_top_states': [{'state': 1, 'count': 290, 'frequency': 0.56640625}, {'state': 0, 'count': 222, 'frequency': 0.43359375}], 'expected_state_index': 0.5667653162043083, 'measurement_histogram': [222, 290]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5667653162043083, 'entropy_bits': 0.987099566131451, 'top_states': [{'state': 1, 'probability': 0.5667653162043083}, {'state': 0, 'probability': 0.4332346837956917}], 'empirical_top_states': [{'state': 1, 'count': 290, 'frequency': 0.56640625}, {'state': 0, 'count': 222, 'frequency': 0.43359375}], 'expected_state_index': 0.5667653162043083, 'measurement_histogram': [222, 290]}, 'waste_energy': 7.868947963056682, 'exotic_energy_generated': 1.9126319753711205, 'total_exotic_energy': 4.126084158789631}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.063042,
  "final_total_exotic_energy": 4.126084
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.064`

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
