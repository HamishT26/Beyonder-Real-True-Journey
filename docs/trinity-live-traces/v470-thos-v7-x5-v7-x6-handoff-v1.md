# v470 THOS v7 x5 to v7 x6 Handoff

Next expected phase: `v470_THOS_v7_x6`

## Carry Forward

- Add formal machine-readable reason codes in the publication guard.
- Expand malformed coverage with unknown schema version, duplicate normalized path, Windows case-collision path, unexpected role enum, and expected-negative unexpected pass.
- Consider mandatory manifest-aware assertion checking for future visualization phases only after broader coverage remains green.
- Keep renderer migration blocked until manifest regression coverage deepens.
- Keep connector writes, cloud writes, destructive cleanup, and GMUT gate movement outside this local guard lane.

## Open Blockers

- The harness currently matches expected reason fragments, not formal reason codes.
- Coverage is stronger than v7 x4 but not exhaustive for every path-normalization variant.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup.
- All six GMUT gates remain open.
