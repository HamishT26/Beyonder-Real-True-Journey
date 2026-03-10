# Filesystem Materialization Workflow

- pack: `filesystem_materialization`
- pillar: `trinity`
- gating_class: `staged_setup_gate`
- sync_strategy: `staged_connector`

## Guardrails
- materialize profile only
- scoped connector required
- local shell is not mcp promotion
- write tracer must stay disposable

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
