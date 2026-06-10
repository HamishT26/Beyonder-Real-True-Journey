# v470 THOS v5 x2 to v470 THOS v6 x1 Handoff

Next expected phase: `v470_THOS_v6_x1`.

## Handoff Tasks

- Extend `scripts/thos_supervisor_gate.py` with optional machine-readable report export if needed.
- Add a blocker ledger artifact that reconciles every `OPEN_GAP` and `FAIL_BLOCKER` row.
- Add a rendered local visualization prototype from v5 x2 dataset rows only.
- Add regression fixtures for unexpected success and unexpected failure.
- Inspect skill frontmatter cleanup candidates as read-only inventory before any repair.
- Keep connector writes unperformed unless named target and separate approval exist.
- Keep all six GMUT gates open.

## Open Blockers

- Expected-failure rows are mapped, but blocker-ledger reconciliation is not yet first-class.
- Visualization is schema-first, not rendered.
- CLI sibling inner shell inspection remains unstable.
- Plugin connector observe-vs-mutate metadata remains partially manual.

Claim ceiling: THOS dry-run evidence only.
