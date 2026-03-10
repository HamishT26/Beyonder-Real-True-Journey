# Notion Materialization Workflow

- pack: `notion_materialization`
- pillar: `heart`
- gating_class: `staged_setup_gate`
- sync_strategy: `staged_connector`

## Guardrails
- materialize profile only
- token and read handshake first
- disposable staging page only
- no secrets in repo

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
