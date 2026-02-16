# Body Track Smoke Report

- generated_utc: `2026-02-16T10:32:58+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.193897`
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
    "actual": 0.193897,
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
| run_full_orchestrator_demo | PASS | 0 | 0.035 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.129 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.035`

### stdout (trimmed)
```
Registered DID: did:freed:72aa3d1576ab4e70aa9b9b92e72a5d52
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7005372553021362, 'entropy_bits': 0.8806331705962387, 'top_states': [{'state': 1, 'probability': 0.7005372553021362}, {'state': 0, 'probability': 0.2994627446978638}], 'empirical_top_states': [{'state': 1, 'count': 359, 'frequency': 0.701171875}, {'state': 0, 'count': 153, 'frequency': 0.298828125}], 'expected_state_index': 0.7005372553021362, 'measurement_histogram': [153, 359]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7005372553021362, 'entropy_bits': 0.8806331705962387, 'top_states': [{'state': 1, 'probability': 0.7005372553021362}, {'state': 0, 'probability': 0.2994627446978638}], 'empirical_top_states': [{'state': 1, 'count': 359, 'frequency': 0.701171875}, {'state': 0, 'count': 153, 'frequency': 0.298828125}], 'expected_state_index': 0.7005372553021362, 'measurement_histogram': [153, 359]}, 'waste_energy': 8.772965471657391, 'exotic_energy_generated': 2.515310314438261, 'total_exotic_energy': 2.515310314438261}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.9393246897154669, 'entropy_bits': 0.33011983629210534, 'top_states': [{'state': 0, 'probability': 0.9393246897154669}, {'state': 1, 'probability': 0.06067531028453312}], 'empirical_top_states': [{'state': 0, 'count': 481, 'frequency': 0.939453125}, {'state': 1, 'count': 31, 'frequency': 0.060546875}], 'expected_state_index': 0.06067531028453312, 'measurement_histogram': [481, 31]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.9393246897154669, 'entropy_bits': 0.33011983629210534, 'top_states': [{'state': 0, 'probability': 0.9393246897154669}, {'state': 1, 'probability': 0.06067531028453312}], 'empirical_top_states': [{'state': 0, 'count': 481, 'frequency': 0.939453125}, {'state': 1, 'count': 31, 'frequency': 0.060546875}], 'expected_state_index': 0.06067531028453312, 'measurement_histogram': [481, 31]}, 'waste_energy': 7.655074899255068, 'exotic_energy_generated': 1.7700499328367114, 'total_exotic_energy': 4.285360247274973}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.14268,
  "final_total_exotic_energy": 4.28536
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.129`

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
