# Body Track Smoke Report

- generated_utc: `2026-02-16T01:57:24+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.171442`
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
    "actual": 0.171442,
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
| compile_python_modules | PASS | 0 | 0.047 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.035 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.090 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.047`

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
- duration_seconds: `0.035`

### stdout (trimmed)
```
Registered DID: did:freed:dce99ed0dd9b4ad69a69130986fae917
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6437987259364734, 'entropy_bits': 0.9394847125273915, 'top_states': [{'state': 0, 'probability': 0.6437987259364734}, {'state': 1, 'probability': 0.3562012740635266}], 'empirical_top_states': [{'state': 0, 'count': 330, 'frequency': 0.64453125}, {'state': 1, 'count': 182, 'frequency': 0.35546875}], 'expected_state_index': 0.3562012740635266, 'measurement_histogram': [330, 182]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6437987259364734, 'entropy_bits': 0.9394847125273915, 'top_states': [{'state': 0, 'probability': 0.6437987259364734}, {'state': 1, 'probability': 0.3562012740635266}], 'empirical_top_states': [{'state': 0, 'count': 330, 'frequency': 0.64453125}, {'state': 1, 'count': 182, 'frequency': 0.35546875}], 'expected_state_index': 0.3562012740635266, 'measurement_histogram': [330, 182]}, 'waste_energy': 7.450578243155671, 'exotic_energy_generated': 1.633718828770447, 'total_exotic_energy': 1.633718828770447}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6005940048010227, 'entropy_bits': 0.9706020632393337, 'top_states': [{'state': 1, 'probability': 0.6005940048010227}, {'state': 0, 'probability': 0.3994059951989773}], 'empirical_top_states': [{'state': 1, 'count': 308, 'frequency': 0.6015625}, {'state': 0, 'count': 204, 'frequency': 0.3984375}], 'expected_state_index': 0.6005940048010227, 'measurement_histogram': [204, 308]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6005940048010227, 'entropy_bits': 0.9706020632393337, 'top_states': [{'state': 1, 'probability': 0.6005940048010227}, {'state': 0, 'probability': 0.3994059951989773}], 'empirical_top_states': [{'state': 1, 'count': 308, 'frequency': 0.6015625}, {'state': 0, 'count': 204, 'frequency': 0.3984375}], 'expected_state_index': 0.6005940048010227, 'measurement_histogram': [204, 308]}, 'waste_energy': 6.54051436861879, 'exotic_energy_generated': 1.027009579079193, 'total_exotic_energy': 2.66072840784964}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.330364,
  "final_total_exotic_energy": 2.660728
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.090`

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
