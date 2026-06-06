# v497 GMUT/THOS v33 v5 x1 Watcher Telemetry Schema Draft

- overall_status: `PASS_SCHEMA_DRAFT_READY_FOR_X2`
- generated_utc: `2026-06-06T19:12:00Z`
- purpose: prepare x2 watcher and notifier hardening without polling sibling lanes early or publishing raw outputs.

## Required Top-Level Fields

- `artifact_type`
- `phase_slug`
- `generated_utc`
- `boundary`
- `lane_rows`
- `overall_status`
- `raw_boundary`
- `claim_boundary`

## Lane Row Fields

- `lane_name`
- `lane_kind`
- `existing_lane_only`
- `new_thread_created`
- `old_style_spawn_used`
- `sandbox_requested`
- `approval_policy_requested`
- `status`
- `completion_status`
- `quality_status`
- `word_count`
- `required_heading_count`
- `missing_required_heading_count`
- `sensitive_or_path_marker_count`
- `raw_output_boundary`
- `repair_state`
- `next_manual_check_utc`

## X2 Use Cases

- Normalize app and CLI watcher rows into one board without raw output reads.
- Represent substantial-but-unharvestable CLI output as `repair_launched` instead of failure.
- Delay manual checks to approved cadence marks while preserving `next_manual_check_utc`.
- Expose `phase_advance_allowed` only when all required lane rows pass completion and quality gates.
- Carry no-overclaim and raw-boundary fields through every status receipt.

All GMUT, physics, consciousness, and canon gates remain open. No raw lane text, raw app transport, raw CLI output, screenshots, credentials, session streams, or private dumps are published.
