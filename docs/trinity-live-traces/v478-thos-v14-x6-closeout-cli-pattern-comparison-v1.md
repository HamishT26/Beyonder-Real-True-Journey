# v478 THOS v14 x6 Closeout CLI Pattern Comparison

- generated_nz: `2026-06-05T10:49:00+12:00`
- overall_status: `PASS_DIRECT_CAPPED_CLI_PATTERN_IMPROVED`
- claim boundary: CLI pattern comparison only; no lane body text; no local paths; all GMUT gates remain open.

## Comparison

- x6 start pattern: standard read-only CLI advisory with external watcher.
- x6 start result: Arby `2205.164` seconds, Aster Vale `2136.519` seconds, completed after the observation window.
- x6 closeout pattern: direct no-tool advisory with launcher-level 30-minute cap.
- x6 closeout result: `FINAL_MESSAGES_READY`, Arby `1349` final-message bytes, Aster Vale `1574` final-message bytes, no final-message sensitive-marker review needed.

## Operator Reading

- The direct capped prompt shape materially reduced CLI output size and avoided the stale TUI wait pattern observed at x6 start.
- Future Arby/Aster calls should prefer direct advisory prompts when the goal is synthesis rather than local tool work.
- Plugin sync warnings in CLI stderr remain a stale-flow watch item, not a lane completion blocker, as long as final-message files are produced.
- The `312.832` second baseline remains a check-in point; direct capped CLI should still be timed rather than assumed fast.
