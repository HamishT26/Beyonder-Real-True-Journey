# Trinity Expansion Result: trinity_safe_bootstrap_audit

- generated_utc: `2026-03-08T12:04:06+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| unsafe_markers_absent | FAIL | hits={'config': ['GITHUB_PERSONAL_ACCESS_TOKEN']} |
| god_functions_absent_or_safe | PASS | hits=[] |
| shell_rc_injection_absent | PASS | hits={'config': ['GITHUB_PERSONAL_ACCESS_TOKEN']} |

## Metrics
```json
{
  "dangerous_marker_count": 1,
  "files_scanned": 5,
  "marker_hits": {
    "config": [
      "GITHUB_PERSONAL_ACCESS_TOKEN"
    ]
  }
}
```

## Repo targets touched
- `docs/trinity-safe-bootstrap-config-v1.toml`
- `docs/trinity-safe-bootstrap-template-v1.sh`
