# Body Track Smoke Report

- generated_utc: `2026-03-04T11:26:18+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `1.023693`
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
    "actual": 1.023693,
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
| compile_python_modules | PASS | 0 | 0.083 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.091 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.850 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.083`

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
- duration_seconds: `0.091`

### stdout (trimmed)
```
Registered DID: did:freed:e741c8507f24457d9ce7b810c2afb528
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.10542320924619243, 0.8945767907538076], 'counts': {'0': 61, '1': 451}, 'entropy_nats': 0.3368381421328241, 'entropy_bits': 0.4859547172372771, 'mean_phase_rad': 0.2849153872194817, 'coherence': 1.3612895544696697, 'top_outcomes': [{'index': 1, 'count': 451, 'freq': 0.880859375, 'p': 0.8945767907538076}, {'index': 0, 'count': 61, 'freq': 0.119140625, 'p': 0.10542320924619243}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.10542320924619243, 0.8945767907538076], 'counts': {'0': 61, '1': 451}, 'entropy_nats': 0.3368381421328241, 'entropy_bits': 0.4859547172372771, 'mean_phase_rad': 0.2849153872194817, 'coherence': 1.3612895544696697, 'top_outcomes': [{'index': 1, 'count': 451, 'freq': 0.880859375, 'p': 0.8945767907538076}, {'index': 0, 'count': 61, 'freq': 0.119140625, 'p': 0.10542320924619243}]}}, 'waste_energy': 8.933218804719472, 'exotic_energy_generated': 2.6221458698129805, 'total_exotic_energy': 2.6221458698129805}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6945895694947433, 0.30541043050525685], 'counts': {'0': 370, '1': 142}, 'entropy_nats': 0.6153790877995633, 'entropy_bits': 0.887804358235204, 'mean_phase_rad': 0.7215264814520704, 'coherence': 1.8748684341328512, 'top_outcomes': [{'index': 0, 'count': 370, 'freq': 0.72265625, 'p': 0.6945895694947433}, {'index': 1, 'count': 142, 'freq': 0.27734375, 'p': 0.30541043050525685}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6945895694947433, 0.30541043050525685], 'counts': {'0': 370, '1': 142}, 'entropy_nats': 0.6153790877995633, 'entropy_bits': 0.887804358235204, 'mean_phase_rad': 0.7215264814520704, 'coherence': 1.8748684341328512, 'top_outcomes': [{'index': 0, 'count': 370, 'freq': 0.72265625, 'p': 0.6945895694947433}, {'index': 1, 'count': 142, 'freq': 0.27734375, 'p': 0.30541043050525685}]}}, 'waste_energy': 7.697926374035981, 'exotic_energy_generated': 1.7986175826906539, 'total_exotic_energy': 4.420763452503635}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.210382,
  "final_total_exotic_energy": 4.420763
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.850`

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
