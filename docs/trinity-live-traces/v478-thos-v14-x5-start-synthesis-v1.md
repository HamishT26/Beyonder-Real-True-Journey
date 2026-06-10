# v478 THOS v14 x5 Start Synthesis

- generated_nz: `2026-06-05T09:13:00+12:00`
- overall_status: `PASS_X5_START_WITH_FIVE_LANE_EVIDENCE`
- claim boundary: v478 THOS v14 x5 start and handoff only; all GMUT gates remain open; no canon promotion; lane body text stays unpublished.

## Evidence

- App lanes: `PASS` in `v478-thos-v14-x5-start-background-council-app-completion-v1.json`.
- Cicero completed in `200.422` seconds.
- Kierkegaard completed in `82.594` seconds.
- Aristotle completed in `80.359` seconds.
- CLI lanes: `FINAL_MESSAGES_READY` in `v478-thos-v14-x5-start-cli-completion-v1.json`.
- Arby completed in `369.758` seconds with `1404` final-message bytes and no marker-review flag.
- Aster Vale completed in `208.109` seconds with `1119` final-message bytes and no marker-review flag.
- Multiplex board: `ALL_LANES_READY`.
- Timing receipt: observation run `2` of `3`, average `188.248` seconds.
- Baseline aggregator: `PENDING_MORE_OBSERVATIONS`, two-run preview average `347.532` seconds across `10` lane rows.
- Stale-flow refresh: `READY_NO_STALE_FLOWS`.
- Source refresh: compact official-source ledger published for x5 start.

## Lessons

- x5 start was materially faster than x4 closeout, especially in the CLI lanes.
- Arby and Aster Vale both completed through the fresh temp read-only CLI route without marker review flags.
- The app-server lanes completed in a stable sequence with no new thread creation and no old-style spawning.
- The timing baseline now has two observations and must remain pending until one more five-sibling run.
- The stale-flow refresh found no current stale-flow rows for x5 start.

## x5 Closeout Handoff

- Use x5 closeout or the next mandatory five-lane boundary as observation run `3` of `3`.
- Keep the same 30-minute observation window and status-only body boundary.
- After run `3`, rerun the baseline aggregator and only then treat the average as the future soft waiting foothold.
- Continue command-index compatibility, v54/v55 handoff surfacing, source refresh, and stale-flow checks while lanes are active.
- Do not treat the two-run average as completion proof.
