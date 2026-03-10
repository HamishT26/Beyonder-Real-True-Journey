# Postgres Materialization Workflow

- pack: `postgres_materialization`
- pillar: `body`
- gating_class: `staged_setup_gate`
- sync_strategy: `staged_connector`

## Guardrails
- materialize profile only
- dsn and read handshake first
- disposable test schema only
- no production mutation

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
