# Body Track Smoke Report

- generated_utc: `2026-02-16T06:43:22+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.132402`
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
    "actual": 0.132402,
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
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.033 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.069 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.033`

### stdout (trimmed)
```
Registered DID: did:freed:8f7441d81fa6489faf9fecb1d7ddb630
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7765439923276538, 'entropy_bits': 0.7664280500582521, 'top_states': [{'state': 1, 'probability': 0.7765439923276538}, {'state': 0, 'probability': 0.2234560076723461}], 'empirical_top_states': [{'state': 1, 'count': 398, 'frequency': 0.77734375}, {'state': 0, 'count': 114, 'frequency': 0.22265625}], 'expected_state_index': 0.7765439923276538, 'measurement_histogram': [114, 398]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7765439923276538, 'entropy_bits': 0.7664280500582521, 'top_states': [{'state': 1, 'probability': 0.7765439923276538}, {'state': 0, 'probability': 0.2234560076723461}], 'empirical_top_states': [{'state': 1, 'count': 398, 'frequency': 0.77734375}, {'state': 0, 'count': 114, 'frequency': 0.22265625}], 'expected_state_index': 0.7765439923276538, 'measurement_histogram': [114, 398]}, 'waste_energy': 7.482917013622188, 'exotic_energy_generated': 1.6552780090814585, 'total_exotic_energy': 1.6552780090814585}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.516360381887845, 'entropy_bits': 0.9992275525732807, 'top_states': [{'state': 0, 'probability': 0.516360381887845}, {'state': 1, 'probability': 0.48363961811215483}], 'empirical_top_states': [{'state': 0, 'count': 264, 'frequency': 0.515625}, {'state': 1, 'count': 248, 'frequency': 0.484375}], 'expected_state_index': 0.48363961811215483, 'measurement_histogram': [264, 248]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.516360381887845, 'entropy_bits': 0.9992275525732807, 'top_states': [{'state': 0, 'probability': 0.516360381887845}, {'state': 1, 'probability': 0.48363961811215483}], 'empirical_top_states': [{'state': 0, 'count': 264, 'frequency': 0.515625}, {'state': 1, 'count': 248, 'frequency': 0.484375}], 'expected_state_index': 0.48363961811215483, 'measurement_histogram': [264, 248]}, 'waste_energy': 7.05181959953525, 'exotic_energy_generated': 1.3678797330234997, 'total_exotic_energy': 3.0231577421049582}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.511579,
  "final_total_exotic_energy": 3.023158
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.069`

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
