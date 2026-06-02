# v470 THOS v7 x4 to v7 x5 Handoff

Next expected phase: `v470_THOS_v7_x5`

## Carry Forward

- Add multiple fixture variants per family instead of one curated sample.
- Add a dedicated temporary malformed-manifest regression harness.
- Consider making manifest-aware assertion checking mandatory for future visualization publication phases only after coverage deepens.
- Keep renderer migration blocked until multi-variant assertion coverage remains green.
- Keep connector writes, cloud writes, destructive cleanup, and GMUT gate movement outside this local guard lane.

## Open Blockers

- Current coverage is explicit but still shallow: one variant per major assertion family.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup.
- All six GMUT gates remain open.
