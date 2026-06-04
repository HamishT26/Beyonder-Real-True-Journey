# v478-thos-v14-x7-start Five-Lane Start Timing

- generated_nz: `2026-06-05T11:09:07+12:00`
- overall_status: `PASS_FIVE_LANE_START`
- observation_run_index_today: `6`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `136.149`
- soft_timeout_baseline_status: `THREE_RUN_BASELINE_ALREADY_READY_X7_START_UNDER_BASELINE`
- publication boundary: lane body text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: start timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T23:02:51+00:00`, completion `2026-06-04T23:05:55+00:00`, duration `184.64`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T23:05:55+00:00`, completion `2026-06-04T23:06:52+00:00`, duration `56.547`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T23:06:52+00:00`, completion `2026-06-04T23:07:51+00:00`, duration `59.25`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T23:02:47+00:00`, completion `2026-06-04T23:05:58+00:00`, duration `191.965`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T23:02:47+00:00`, completion `2026-06-04T23:05:55+00:00`, duration `188.343`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as a post-baseline observation showing the direct capped CLI pattern remained under the `312.832` second soft wait foothold.
- Keep the original three-run baseline as the planning foothold; use x7 start as reinforcing pattern evidence rather than a baseline replacement.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
- Continue direct capped CLI advisory prompts for synthesis-only Arby and Aster Vale calls.
