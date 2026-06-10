# v502-gmut-thos-v38-v4-x1 App Watcher Freshness Guard Design

- generated_utc: `2026-06-08T07:17:37Z`
- overall_status: `PASS_APP_WATCHER_FRESHNESS_GUARD_DESIGN_READY`
- design_only: `True`
- full_x2_build_allowed: `False`
- blocked_until_arby_final_message: `True`

Design goal:
- Create a future guard that compares app watcher expected receipts, generation timestamps, lane completion summaries, redaction status, and exposure-guard status before any app-lane completion claim is used for phase advance.

Proposed checks:
- Runner receipt exists and records `PASS_BACKGROUND_WATCH_STARTED` or an explicit open gap.
- Watch launcher receipt exists before completion gate is evaluated.
- Completion notifier receipt exists before completion gate claims pass.
- Completion notifier receipt is redacted before exposure publication.
- Completion gate references expected lanes only.
- Completion gate records all app lanes as completed before next phase approval.
- Generated timestamps are monotonic enough for the phase cadence.
- Exposure guard has zero findings after redaction.
- No raw advisory bodies or app transport are published.
- Duration is not completion proof.

Future CLI:
- Script candidate: `scripts/thos_app_watcher_freshness_guard.py`
- Inputs: app runner, watch launcher, completion notifier, completion gate, redaction, and exposure receipts.
- Outputs: status-only JSON and Markdown receipts.
- Return policy: nonzero on missing, stale, unredacted, or raw-publication open gap.

Publication boundary: status only; no raw lane text, raw transport, local absolute paths, credentials, screenshots, or session streams.

Claim boundary: GMUT and canon gates remain open; duration is not completion proof.
