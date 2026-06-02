# v470 THOS v6 x8 to v7 x1 Handoff

Next expected phase: `v470_THOS_v7_x1`

## Carry Forward

- Add `precedence_reason` and `dominant_failure_code` to checker output.
- Preserve weaker findings even when a blocker dominates.
- Add explicit count fields for digest refs, orphan rows, duplicate bindings, tuple mismatches, and gate-effect drift.
- Decide whether to migrate the renderer to external JSON or keep validation fixture-only.
- Keep all six GMUT gates open.

## v6 Closeout

v6 closed the classification gap for local row-universe and visualization-binding checks. It did not close GMUT gates, certify safety, or authorize connector actions.
