# Body Track Smoke Report

- generated_utc: `2026-03-02T07:01:00+00:00`
- overall_status: **FAIL**

## Summary metrics
- pass_rate: `0.333333`
- total_duration_seconds: `1.38487`
- body_health_score: `33.33`
- speed_band: `steady`

## Benchmark guardrail
- status: **WARN**
- profile: `standard`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.0,
  "min_health_score": 95.0
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": false,
    "actual": 0.333333,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": false,
    "actual": 1.38487,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": false,
    "actual": 33.33,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | FAIL | 1 | 0.080 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | FAIL | 1 | 0.088 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 1.217 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `1`
- duration_seconds: `0.080`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
[Errno 2] No such file or directory: 'Freed_id_registry.py'
```

## run_full_orchestrator_demo

- returncode: `1`
- duration_seconds: `0.088`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
Traceback (most recent call last):
  File "/home/hamisht4647/Beyonder-Real-True-Journey-1/trinity_orchestrator_full.py", line 22, in <module>
    from freed_id_registry import FreedIDRegistry, DIDDocument
  File "/home/hamisht4647/Beyonder-Real-True-Journey-1/freed_id_registry.py", line 280
    claims = credential_service.get("credential", {})
IndentationError: unexpected indent
```

### extracted_metrics
```json
{
  "task_count": 0,
  "analysis_status": "skipped_due_to_failure"
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `1.217`

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
