# GitHub Materialization Workflow

- pack: `github_materialization`
- pillar: `trinity`
- gating_class: `staged_setup_gate`
- sync_strategy: `staged_connector`

## Guardrails
- materialize profile only
- disposable branch tracer
- read handshake before write
- never target main

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
