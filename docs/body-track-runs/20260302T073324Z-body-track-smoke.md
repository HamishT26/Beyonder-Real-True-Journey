# Body Track Smoke Report

- generated_utc: `2026-03-02T07:33:24+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `1.203952`
- body_health_score: `100.0`
- speed_band: `steady`

## Benchmark guardrail
- status: **PASS**
- profile: `standard`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.274,
  "min_health_score": 32.83
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
    "actual": 1.203952,
    "threshold": 1.274
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 32.83
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.088 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.100 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 1.016 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.088`

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
- duration_seconds: `0.100`

### stdout (trimmed)
```
Registered DID: did:freed:73db7946558c446a9df2d7a8605e321a
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.06795293610968484, 0.9320470638903152], 'counts': {'0': 34, '1': 478}, 'entropy_nats': 0.24831134923048725, 'entropy_bits': 0.3582375521312715, 'mean_phase_rad': 1.1706915081273586, 'coherence': 1.2474837512016128, 'top_outcomes': [{'index': 1, 'count': 478, 'freq': 0.93359375, 'p': 0.9320470638903152}, {'index': 0, 'count': 34, 'freq': 0.06640625, 'p': 0.06795293610968484}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.06795293610968484, 0.9320470638903152], 'counts': {'0': 34, '1': 478}, 'entropy_nats': 0.24831134923048725, 'entropy_bits': 0.3582375521312715, 'mean_phase_rad': 1.1706915081273586, 'coherence': 1.2474837512016128, 'top_outcomes': [{'index': 1, 'count': 478, 'freq': 0.93359375, 'p': 0.9320470638903152}, {'index': 0, 'count': 34, 'freq': 0.06640625, 'p': 0.06795293610968484}]}}, 'waste_energy': 8.460085323133843, 'exotic_energy_generated': 2.3067235487558944, 'total_exotic_energy': 2.3067235487558944}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5739231846985829, 0.426076815301417], 'counts': {'0': 309, '1': 203}, 'entropy_nats': 0.6821777374772522, 'entropy_bits': 0.9841744388632849, 'mean_phase_rad': 1.3589074467336502, 'coherence': 1.9871641272698704, 'top_outcomes': [{'index': 0, 'count': 309, 'freq': 0.603515625, 'p': 0.5739231846985829}, {'index': 1, 'count': 203, 'freq': 0.396484375, 'p': 0.426076815301417}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5739231846985829, 0.426076815301417], 'counts': {'0': 309, '1': 203}, 'entropy_nats': 0.6821777374772522, 'entropy_bits': 0.9841744388632849, 'mean_phase_rad': 1.3589074467336502, 'coherence': 1.9871641272698704, 'top_outcomes': [{'index': 0, 'count': 309, 'freq': 0.603515625, 'p': 0.5739231846985829}, {'index': 1, 'count': 203, 'freq': 0.396484375, 'p': 0.426076815301417}]}}, 'waste_energy': 7.96589214454769, 'exotic_energy_generated': 1.977261429698459, 'total_exotic_energy': 4.283984978454353}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.141992,
  "final_total_exotic_energy": 4.283985
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `1.016`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0200: energy density ratio = 1.01986
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
    "0.0200": 1.01986,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
