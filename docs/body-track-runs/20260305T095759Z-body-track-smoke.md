# Body Track Smoke Report

- generated_utc: `2026-03-05T09:57:59+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.385009`
- body_health_score: `100.0`
- speed_band: `fast`

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
    "actual": 0.385009,
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
| compile_python_modules | PASS | 0 | 0.087 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.089 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.210 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.087`

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
- duration_seconds: `0.089`

### stdout (trimmed)
```
Registered DID: did:freed:fb93e85fc326439f8a676b109453730c
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8645298324609961, 0.13547016753900393], 'counts': {'0': 440, '1': 72}, 'entropy_nats': 0.39665452973059645, 'entropy_bits': 0.5722515229884754, 'mean_phase_rad': 0.5125261182441325, 'coherence': 1.5744853948551558, 'top_outcomes': [{'index': 0, 'count': 440, 'freq': 0.859375, 'p': 0.8645298324609961}, {'index': 1, 'count': 72, 'freq': 0.140625, 'p': 0.13547016753900393}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8645298324609961, 0.13547016753900393], 'counts': {'0': 440, '1': 72}, 'entropy_nats': 0.39665452973059645, 'entropy_bits': 0.5722515229884754, 'mean_phase_rad': 0.5125261182441325, 'coherence': 1.5744853948551558, 'top_outcomes': [{'index': 0, 'count': 440, 'freq': 0.859375, 'p': 0.8645298324609961}, {'index': 1, 'count': 72, 'freq': 0.140625, 'p': 0.13547016753900393}]}}, 'waste_energy': 8.140597901304842, 'exotic_energy_generated': 2.0937319342032272, 'total_exotic_energy': 2.0937319342032272}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.20395107174465574, 0.7960489282553443], 'counts': {'0': 100, '1': 412}, 'entropy_nats': 0.5058312261324611, 'entropy_bits': 0.7297602014680855, 'mean_phase_rad': 0.8200976236220652, 'coherence': 1.6039745653158735, 'top_outcomes': [{'index': 1, 'count': 412, 'freq': 0.8046875, 'p': 0.7960489282553443}, {'index': 0, 'count': 100, 'freq': 0.1953125, 'p': 0.20395107174465574}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.20395107174465574, 0.7960489282553443], 'counts': {'0': 100, '1': 412}, 'entropy_nats': 0.5058312261324611, 'entropy_bits': 0.7297602014680855, 'mean_phase_rad': 0.8200976236220652, 'coherence': 1.6039745653158735, 'top_outcomes': [{'index': 1, 'count': 412, 'freq': 0.8046875, 'p': 0.7960489282553443}, {'index': 0, 'count': 100, 'freq': 0.1953125, 'p': 0.20395107174465574}]}}, 'waste_energy': 7.794960319581032, 'exotic_energy_generated': 1.863306879720688, 'total_exotic_energy': 3.957038813923915}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.978519,
  "final_total_exotic_energy": 3.957039
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.210`

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
