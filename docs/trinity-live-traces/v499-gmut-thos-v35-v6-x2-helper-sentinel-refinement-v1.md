# v499 GMUT/THOS v35 v6 x2 Helper Sentinel Refinement

- generated_utc: `2026-06-07T09:57:10Z`
- overall_status: `PASS_HELPER_SENTINEL_REFINEMENT_BUILT`
- target_script: `thos_cli_strict_stdin_lane_launcher.py`

## Changes

- Write a wrapper-start sentinel before invoking Codex CLI.
- Write a wrapper-exit JSON receipt with exit code, copy status, raw/expected existence, and byte counts.
- Capture launcher-level stdout/stderr privately instead of discarding them.
- Keep no-space bridge output and expected notifier filename copy.
- Publish status-only receipts.

This fixes the core v6 x1 lesson: process start is not execution proof.
