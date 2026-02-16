# Nightly Handoff Snapshot

- generated_utc: `2026-02-16T10:04:09+00:00`
- session_label: `nz-monday-night-closeout`
- session_status: **STABLE_WITH_GAPS**

## Track artifact statuses
| artifact | status | path |
|---|---|---|
| suite | PASS | `docs/system-suite-status.json` |
| body_benchmark | PASS | `docs/body-track-benchmark-latest.json` |
| body_trend_guard | PASS | `docs/body-track-trend-guard-latest.json` |
| body_calibration | PASS | `docs/body-track-calibration-latest.json` |
| heart_gov002_standard | PASS | `docs/heart-track-min-disclosure-latest.json` |
| heart_gov002_live | PASS | `docs/heart-track-min-disclosure-live-latest.json` |
| heart_gov002_adversarial | PASS | `docs/heart-track-min-disclosure-adversarial-latest.json` |
| heart_gov003 | PASS | `docs/heart-track-auditability-latest.json` |
| heart_gov004_standard | PASS | `docs/heart-track-dispute-recourse-latest.json` |
| heart_gov004_adversarial | PASS | `docs/heart-track-dispute-recourse-adversarial-latest.json` |
| heart_gov005 | PASS | `docs/heart-track-governance-latest.json` |
| mind_comparator | PASS | `docs/mind-track-gmut-comparator-latest.json` |
| mind_anchor_exclusion | WARN | `docs/mind-track-gmut-anchor-exclusion-latest.json` |

## Next-launch focus
1. Heart: progress GOV-004 from callback-level checks to DID-method signature verification.
2. Body: test selective policy updates and publish before/after false-alert deltas.
3. Mind: attach source-side extraction artifacts and uncertainty equations per trace ID.
