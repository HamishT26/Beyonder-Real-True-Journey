# Self Correction Workflow

- pack: `self_correction`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `autonomy_safety`
- continuity_band: `v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `bounded_mutation`

## Workflow Tokens
- static checks
- repair candidates
- no push to main
- explicit gate
