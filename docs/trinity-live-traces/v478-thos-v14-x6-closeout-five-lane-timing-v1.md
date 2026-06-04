# v478-thos-v14-x6-closeout Five-Lane Closeout Timing

- generated_nz: `2026-06-05T10:50:00+12:00`
- overall_status: `PASS_FIVE_LANE_CLOSEOUT`
- observation_run_index_today: `5`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `161.032`
- soft_timeout_baseline_status: `THREE_RUN_BASELINE_ALREADY_READY_X6_CLOSEOUT_UNDER_BASELINE`
- publication boundary: lane body text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: closeout timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T22:42:48+00:00`, completion `2026-06-04T22:46:30+00:00`, duration `222.36`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T22:46:30+00:00`, completion `2026-06-04T22:47:27+00:00`, duration `56.64`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T22:47:27+00:00`, completion `2026-06-04T22:48:26+00:00`, duration `59.094`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T22:42:44+00:00`, completion `2026-06-04T22:46:44+00:00`, duration `240.966`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T22:42:44+00:00`, completion `2026-06-04T22:46:30+00:00`, duration `226.098`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as a post-baseline observation showing the direct capped CLI pattern completed under the `312.832` second soft wait foothold.
- Keep the original three-run baseline as the planning foothold; use this closeout as pattern evidence rather than a baseline replacement.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
- Prefer direct capped CLI advisory prompts for future synthesis-only Arby and Aster Vale calls.
