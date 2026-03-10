# Sentinel Daemon Workflow

- pack: `sentinel_daemon`
- pillar: `trinity`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `autonomy_observation`
- continuity_band: `v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `read_only`

## Workflow Tokens
- manual daemon
- read-only polling
- stale proof detection
- no automatic scheduling
