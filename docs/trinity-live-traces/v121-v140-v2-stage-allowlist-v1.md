# v121-v140 v2 Stage Allowlist

- generated_utc: `2026-05-06T00:23:48+00:00`
- purpose: curated publication slice for the v121-v140 v2 repo-only 400-system and offline materialize L5-readiness pass
- google_drive_state: `operator_hold`
- external_provider_mutations: `held`
- external_spend_nzd: `0`
- materialization_level_actual: `readiness_only`

## Include

- `scripts/trinity_v121_v140_v2_candidate_systems.py`
- `docs/trinity-expansion-system-manifest-v17.json`
- `docs/trinity-expansion-manifest-validation-latest.json`
- `docs/trinity-expansion-manifest-validation-latest.md`
- `docs/trinity-live-traces/v121-v140-v2-*`
- `docs/trinity-live-traces/v140-v2-materialize-l5-suite-status.*`
- `docs/trinity-live-traces/v121-v140-v2-candidate-system-results/*`
- `docs/v121-beta-alpha-omega-v2-closeout-summary-v1.*` through `docs/v140-beta-alpha-omega-v2-closeout-summary-v1.*`
- `docs/trinity-expansion/v133-v2-*` through `docs/trinity-expansion/v140-v2-*`

## Exclude

- `__pycache__/**`
- `docs/system-suite-run-report.md`
- generic latest control tower and scoreboard files
- provider caches and materialization ledgers
- private chat ledgers and unrelated council memory ledgers
- older v96-v120 candidate results
- unrelated carried-forward dirty tree surfaces
