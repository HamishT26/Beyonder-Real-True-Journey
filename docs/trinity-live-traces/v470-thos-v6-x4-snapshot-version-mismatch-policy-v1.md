# v470 THOS v6 x4 Snapshot Version Mismatch Policy

This policy freezes the v6 x4 default: exact match or fail closed. If compatibility is ever allowed, it must be named in a separate compatibility artifact.

## Version Axes

- Manifest schema version.
- Snapshot contract version.
- Consumer compatibility version.

## Policy

Unknown manifest versions and unknown snapshot versions are `FAIL_BLOCKER`. Documented minor compatibility can be an `OPEN_GAP` until a scoped artifact proves the mapping. GMUT gate-effect drift is always `FAIL_BLOCKER` in THOS infrastructure.
