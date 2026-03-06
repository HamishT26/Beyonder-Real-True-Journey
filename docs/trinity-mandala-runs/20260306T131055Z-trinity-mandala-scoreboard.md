# Trinity Mandala Scoreboard

- generated_utc: `2026-03-06T13:10:55+00:00`
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
| mind | Mind API signal board | PASS | freshness_status=PASS, source_count=14, apis=2 | `docs/mind-theory-signal-board-latest.json` |
| mind | Mind expansion constellation | PASS | checks=9/9 | `docs/trinity-expansion/mind-theory-constellation-board-latest.json` |
| body | Body smoke | PASS | pass_rate=1.0, total_duration_seconds=0.868603, body_health_score=100.0, benchmark_status=PASS | `docs/body-track-smoke-latest.json` |
| body | Benchmark guardrail | PASS | status extracted | `docs/body-track-benchmark-latest.json` |
| body | Trend guard | PASS | trend=stable_or_improving | `docs/body-track-trend-guard-latest.json` |
| body | Stress window | PASS | status extracted | `docs/body-track-policy-stress-latest.json` |
| body | Body API signal board | PASS | freshness_status=PASS, source_count=17, apis=3 | `docs/body-compute-signal-board-latest.json` |
| body | Body expansion constellation | PASS | checks=3/3 | `docs/trinity-expansion/body-compute-signal-quality-gate-latest.json` |
| heart | Minimum disclosure | PASS | checks=11/11 | `docs/heart-track-min-disclosure-latest.json` |
| heart | Minimum disclosure adversarial | PASS | checks=22/22 | `docs/heart-track-min-disclosure-adversarial-latest.json` |
| heart | Minimum disclosure live path | PASS | checks=6/6 | `docs/heart-track-min-disclosure-live-latest.json` |
| heart | Dispute recourse | PASS | final_case_status=dismissed | `docs/heart-track-dispute-recourse-latest.json` |
| heart | Dispute recourse adversarial | PASS | checks=12/12 | `docs/heart-track-dispute-recourse-adversarial-latest.json` |
| heart | Heart API signal board | PASS | freshness_status=PASS, source_count=17, apis=3 | `docs/heart-governance-signal-board-latest.json` |
| heart | Heart expansion constellation | PASS | checks=9/9 | `docs/trinity-expansion/heart-governance-constellation-board-latest.json` |

## Context blocks
| label | status | detail | path |
|---|---|---|---|
| API constellation board | PASS | manifest_validation_status=PASS, promotion_candidates=4 | `docs/trinity-api-constellation-board-latest.json` |
| Expansion manifest validation | PASS | status extracted | `docs/trinity-expansion-manifest-validation-latest.json` |
| Expansion result validation | PASS | status extracted | `docs/trinity-expansion-result-validation-latest.json` |

## Evidence boundary
- verified_state: Latest suite and pillar artifacts are the current operational evidence boundary.
- watch_state: Promote only PASS-backed states; treat WARN/FAIL artifacts as live investigation targets.
- next_phase_focus: Advance new systems only when they preserve suite pass state and per-pillar traceability.
