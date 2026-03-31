# Trinity Expansion Result: trinity_dependency_surface_report

- generated_utc: `2026-03-31T02:39:19+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| import_scan_complete | PASS | imports=74 |
| dependency_surface_documented | PASS | external=12 |

## Metrics
```json
{
  "external_import_roots": [
    "Freed_id_audit_log",
    "Freed_id_registry",
    "cryptography",
    "did_webvh",
    "fluid_capability_test_suite",
    "fluid_experiment_runner",
    "google",
    "google_auth_oauthlib",
    "googleapiclient",
    "matplotlib",
    "numpy",
    "pypdf"
  ],
  "total_import_roots": 74
}
```

## Repo targets touched
- `scripts/run_all_trinity_systems.py`
- `scripts/trinity_expansion_system_runner.py`
