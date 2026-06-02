# v470 THOS v4 x1 Checker Spec

Phase: `v470_THOS_v4_x1`

Script: `scripts/thos_publication_guard.py`

Mode: local, non-mutating, current-phase scoped.

## Purpose

The checker turns the v3 x2 advisory matrix into a small runnable THOS command surface. It validates a named phase artifact set and reports blockers without staging, deleting, uploading, connector writing, or changing files.

## Requirements

- Check the current-phase artifact allowlist.
- Lint forbidden claims.
- Guard raw log, session JSONL, screenshot, and credential-risk paths.
- Guard secret-like content patterns.
- Parse JSON artifacts.
- Validate checker status enums.
- Check trailing whitespace.
- Optionally validate currently staged paths against the current-phase allowlist.
- Record Git drift where readable.
- Preserve `gmUT_gate_effect: none_open_not_tested`.

## Status Lattice

- `FAIL_BLOCKER` dominates all other statuses.
- `OPEN_GAP` dominates `NOT_RUN` and `PASS_SHAPE_ONLY`.
- `NOT_RUN` is allowed only for intentionally skipped checks.
- `PASS_SHAPE_ONLY` means shape or guard evidence only, never workflow certification.

## Example Command

```powershell
python scripts/thos_publication_guard.py --phase-slug v470-thos-v3-x2
```

For staged publication guard:

```powershell
python scripts/thos_publication_guard.py --phase-slug v470-thos-v4-x1 --staged-only --allow-staged scripts/thos_publication_guard.py
```

## Non-Claims

- The checker does not mutate files.
- The checker does not stage files.
- The checker does not perform cleanup.
- The checker does not write connectors.
- The checker does not validate GMUT.
