# v478 THOS v14 x7 Start Synthesis

- generated_nz: `2026-06-05T11:11:00+12:00`
- overall_status: `PASS_X7_START_WITH_DIRECT_CAPPED_CLI_PATTERN_REINFORCED`
- claim boundary: v478 THOS v14 x7 start synthesis and x7 closeout handoff only; all GMUT gates remain open; no canon promotion; lane body text and raw output stay unpublished.

## Evidence

- App lanes: `PASS`.
- Cicero completed in `184.64` seconds.
- Kierkegaard completed in `56.547` seconds.
- Aristotle completed in `59.25` seconds.
- CLI lanes: `FINAL_MESSAGES_READY`.
- Arby completed in `191.965` seconds with `1952` final-message bytes and hash `3c1d75c4b4e1f9b1b1142b302fe99b687d3bc47fcceb3a2e21a682f90ac7182e`.
- Aster Vale completed in `188.343` seconds with `1315` final-message bytes and hash `e035ed7d43be39e38e93d315c0dc91baf62318a6a5eb72ed880860c30bcec575`.
- Timing receipt: average `136.149` seconds, under the `312.832` second soft wait foothold.
- Multiplex board: `ALL_LANES_READY`.
- Stale-flow refresh: `READY_NO_STALE_FLOWS`.
- Loader watch: `WATCH_NONBLOCKING_SKILL_NAME_LENGTH_WARNINGS`.

## Lessons

- The five-lane roster completed at x7 start through existing lanes only.
- Direct capped CLI completed Arby and Aster Vale under the soft wait foothold for the second consecutive post-baseline run.
- No final-message marker review was needed for x7 CLI lanes.
- Skill-name length loader warnings appeared in CLI stderr metadata but did not block final-message production.
- x7 start reinforces direct capped CLI as the synthesis-only default for Arby and Aster Vale.

## x7 Closeout Handoff

- Use direct capped CLI advisory again for x7 closeout if the task is synthesis-only.
- Continue exact status-only publication and no raw lane body text.
- Carry the nonblocking skill-name length warning as a watch item, not a live repair.
- Keep command-index v6 alias compatibility and v54/v55 handoff as known surfaces.
- Use the x7 start average of `136.149` seconds as pattern evidence, while preserving `312.832` seconds as the official soft baseline.
