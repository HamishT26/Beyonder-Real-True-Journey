# Trinity Expansion Result: trinity_dependency_surface_report

- generated_utc: `2026-04-08T14:20:00+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| import_scan_complete | PASS | imports=82 |
| dependency_surface_documented | PASS | external=13 |

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
    "pypdf",
    "vertexai"
  ],
  "total_import_roots": 82
}
```

## Repo targets touched
- `scripts/run_all_trinity_systems.py`
- `scripts/trinity_expansion_system_runner.py`
