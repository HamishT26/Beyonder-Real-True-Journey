# v501-gmut-thos-v37-v2-x2 Build Run Use Closeout

- generated_at_utc: `2026-06-07T23:15:16Z`
- overall_status: `PASS_X2_CODEX_CMD_CALL_COPY_BRIDGE_FIX`
- status_only: `True`

## Fix Summary
The Windows runner now invokes codex.cmd through call before the post-run copy command, allowing the .cmd script to continue and create normalized final-message aliases.

## Checks
- call_prefix_present: `True`
- copy_line_present_after_codex_call: `True`
- read_only_sandbox_present: `True`
- approval_never_present: `True`
- output_last_message_bridge_present: `True`
- json_event_redirect_present: `True`
- stderr_redirect_present: `True`
- parse_lane_safe_bridge: `True`
- parse_lane_aster_bridge: `True`

## Expected Next Phase Effect
v501 v3 x1 should create normalized CLI final-message aliases automatically after each read-only CLI lane completes, reducing false pending notifier gaps.

## Boundary
status-only; no raw lane text, raw logs, temp paths, session streams, screenshots, credentials, or private dumps published
