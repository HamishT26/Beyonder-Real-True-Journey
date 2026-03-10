# Materialization Ladder Governor Workflow

- pack: `materialization_ladder_governor`
- pillar: `trinity`
- gating_class: `active`
- sync_strategy: `local_probe`
- activation_group: `materialization_ladder`
- continuity_band: `v7`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `bounded_write`

## Workflow Tokens
- ladder registry
- proof-gated promotion
- rollback required
- readiness only above l2 until proven
