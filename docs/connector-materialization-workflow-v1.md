# Connector Materialization Workflow

- pack: `connector_materialization`
- pillar: `trinity`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `connector_hardening`
- continuity_band: `v5-v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `write_proof`

## Workflow Tokens
- fresh read proof
- fresh write proof
- rollback-safe target
- no main writes
