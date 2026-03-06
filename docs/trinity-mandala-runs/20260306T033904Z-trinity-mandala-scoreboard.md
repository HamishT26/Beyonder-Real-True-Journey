# Trinity Mandala Scoreboard

- generated_utc: `2026-03-06T03:39:04+00:00`
- hybrid_os_status: **PASS**
- suite_status: `PASS`

## Pillar summary
| pillar | status | watch_items | next_action |
|---|---|---|---|
| mind | PASS | - | Mind pillar currently clear; keep it under the standard suite cadence. |
| body | PASS | - | Body pillar currently clear; keep it under the standard suite cadence. |
| heart | PASS | - | Heart pillar currently clear; keep it under the standard suite cadence. |

## Artifact board
| pillar | artifact | status | detail | path |
|---|---|---|---|---|
| mind | GMUT comparator | PASS | gamma_ratios=3 | `docs/mind-track-gmut-comparator-latest.json` |
| mind | Anchor exclusion note | PASS | status extracted | `docs/mind-track-gmut-anchor-exclusion-latest.json` |
| mind | Anchor trace validation | PASS | checks=10/10 | `docs/mind-track-gmut-trace-validation-latest.json` |
| body | Body smoke | PASS | pass_rate=1.0, total_duration_seconds=1.12395, body_health_score=100.0, benchmark_status=PASS | `docs/body-track-smoke-latest.json` |
| body | Benchmark guardrail | PASS | status extracted | `docs/body-track-benchmark-latest.json` |
| body | Trend guard | PASS | trend=stable_or_improving | `docs/body-track-trend-guard-latest.json` |
| body | Stress window | PASS | status extracted | `docs/body-track-policy-stress-latest.json` |
| heart | Minimum disclosure | PASS | checks=11/11 | `docs/heart-track-min-disclosure-latest.json` |
| heart | Minimum disclosure adversarial | PASS | checks=22/22 | `docs/heart-track-min-disclosure-adversarial-latest.json` |
| heart | Minimum disclosure live path | PASS | checks=6/6 | `docs/heart-track-min-disclosure-live-latest.json` |
| heart | Dispute recourse | PASS | final_case_status=dismissed | `docs/heart-track-dispute-recourse-latest.json` |
| heart | Dispute recourse adversarial | PASS | checks=12/12 | `docs/heart-track-dispute-recourse-adversarial-latest.json` |

## Evidence boundary
- verified_state: Latest suite and pillar artifacts are the current operational evidence boundary.
- watch_state: Promote only PASS-backed states; treat WARN/FAIL artifacts as live investigation targets.
- next_phase_focus: Advance new systems only when they preserve suite pass state and per-pillar traceability.
