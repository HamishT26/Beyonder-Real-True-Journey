# v478 THOS v1 x1 Watcher Template

- generated_nz: `2026-06-04T08:49:34+12:00`
- overall_status: `PASS_WITH_CLI_OPEN_GAP`

## Criteria
- `app_probe`: `PASS` — run app-lane probe before notify.
- `app_notify`: `PASS` — send existing-thread notify only after probe passes.
- `app_completion`: `PASS` — observe turn completion per app lane.
- `cli_single_poll`: `PASS` — run one bounded CLI poll per phase closeout.
- `cli_final_marker`: `OPEN_GAP` — require final-message marker for CLI closure.
- `temp_only`: `PASS` — keep CLI watcher output temp-only.
- `transport_summary_only`: `PASS` — publish status summaries only.
- `retry_rule`: `PASS` — retry only when a new blocker class appears.
- `x_overlay_rule`: `PASS` — add x3 only when blocker dominance justifies it.
