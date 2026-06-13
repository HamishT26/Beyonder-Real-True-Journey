# v497 GMUT/THOS v33 v5 x1 X2 Builder Preflight Spec

- overall_status: `PASS_PREFLIGHT_SPEC_READY_NOT_EXECUTED`
- generated_utc: `2026-06-06T19:27:00Z`
- target_x2_slug: `v497-gmut-thos-v33-v5-x2`

## Requirements Before X2 Build

- `one_hour_x1_gate`: x1 should get the requested long planning window before closeout.
- `five_lane_visibility`: all lanes must be visible through curated receipts.
- `cli_quality_or_bounded_repair`: CLI lanes need elaboration pass or an explicit bounded blocker receipt.
- `x2_prep_gate`: x2 needs its 10-minute preparation gate before build/run/test/use.
- `source_reflection_build_inputs`: source ledger, reflection spine, skill overlay, command map, and watcher schema should feed the build.
- `publication_validation`: parse, compile where applicable, scan, whitespace-check, exact-stage, commit, push, and remote-verify.

## Do Not Execute Until

- Aster Vale repair either passes or has a bounded blocker receipt.
- The one-hour v5 x1 closeout mark is reached.
- The 10-minute v5 x2 prep gate is reached after x2 starts.

All GMUT and canon gates remain open. No raw/private material is published.
