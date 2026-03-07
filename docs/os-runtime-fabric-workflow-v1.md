# OS Runtime Fabric Workflow

- pack: `os_runtime_fabric`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `public_feeds`

## Guardrails
- official sources only
- cache-backed by default
- no auto-promotion of claims
- pattern registry first

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
