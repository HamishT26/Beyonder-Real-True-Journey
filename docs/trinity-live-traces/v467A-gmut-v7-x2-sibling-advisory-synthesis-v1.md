# v467A GMUT v7 x2 Sibling Advisory Synthesis

Prepared: 2026-06-01T22:23:17+12:00

All five active lanes returned. The common synthesis is that `v7_x2` may design schema fragments, fixture states, lint catalogs, and registry/digest governance, but must not execute physics or move gate states.

## Adopted Rules

- Fixture states are `clean`, `conflicted`, `quarantined`, and `no_result_heavy`.
- `clean` means structurally well formed only; it still carries `not_run` and `no_result`.
- Schema fragments may define literal input rows and derived lint reports.
- Required-field matrices and forbidden-field registries are allowed.
- Normalized key registry backfill and migration exception ledgers are allowed as design artifacts.
- Stable bundle digest is a future canonicalization target, not a proof.
- Gate-language lint must block closure, safety, proof, recovery, validation, and canon-promotion wording.

All six GMUT gates remain `OPEN_NOT_TESTED`.
