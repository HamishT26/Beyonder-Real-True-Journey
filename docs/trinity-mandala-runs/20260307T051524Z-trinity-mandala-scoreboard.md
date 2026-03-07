# Trinity Mandala Scoreboard

- generated_utc: `2026-03-07T05:15:24+00:00`
- hybrid_os_status: **FAIL**
- suite_status: `PASS`

## Pillar summary
| pillar | status | watch_items | next_action |
|---|---|---|---|
| mind | FAIL | Mind expansion constellation, Mind readiness gate | Re-run and inspect: Mind expansion constellation, Mind readiness gate. |
| body | FAIL | Body expansion constellation, Body readiness gate | Re-run and inspect: Body expansion constellation, Body readiness gate. |
| heart | FAIL | Heart readiness gate | Re-run and inspect: Heart readiness gate. |

## Artifact board
| pillar | artifact | status | detail | path |
|---|---|---|---|---|
| mind | GMUT comparator | PASS | gamma_ratios=3 | `docs/mind-track-gmut-comparator-latest.json` |
| mind | Anchor exclusion note | PASS | status extracted | `docs/mind-track-gmut-anchor-exclusion-latest.json` |
| mind | Anchor trace validation | PASS | checks=10/10 | `docs/mind-track-gmut-trace-validation-latest.json` |
| mind | Mind API signal board | PASS | freshness_status=PASS, source_count=14, apis=2 | `docs/mind-theory-signal-board-latest.json` |
| mind | Mind expansion constellation | FAIL | checks=8/9 | `docs/trinity-expansion/mind-theory-constellation-board-latest.json` |
| mind | Mind readiness gate | FAIL | checks=0/2 | `docs/trinity-expansion/mind-theory-readiness-gate-latest.json` |
| body | Body smoke | PASS | pass_rate=1.0, total_duration_seconds=0.895408, body_health_score=100.0, benchmark_status=PASS | `docs/body-track-smoke-latest.json` |
| body | Benchmark guardrail | PASS | status extracted | `docs/body-track-benchmark-latest.json` |
| body | Trend guard | PASS | trend=stable_or_improving | `docs/body-track-trend-guard-latest.json` |
| body | Stress window | PASS | status extracted | `docs/body-track-policy-stress-latest.json` |
| body | Body API signal board | PASS | freshness_status=PASS, source_count=17, apis=2 | `docs/body-compute-signal-board-latest.json` |
| body | Body expansion constellation | FAIL | checks=0/2 | `docs/trinity-expansion/body-compute-signal-quality-gate-latest.json` |
| body | Body readiness gate | FAIL | checks=0/2 | `docs/trinity-expansion/body-compute-readiness-gate-latest.json` |
| heart | Minimum disclosure | PASS | checks=11/11 | `docs/heart-track-min-disclosure-latest.json` |
| heart | Minimum disclosure adversarial | PASS | checks=22/22 | `docs/heart-track-min-disclosure-adversarial-latest.json` |
| heart | Minimum disclosure live path | PASS | checks=6/6 | `docs/heart-track-min-disclosure-live-latest.json` |
| heart | Dispute recourse | PASS | final_case_status=dismissed | `docs/heart-track-dispute-recourse-latest.json` |
| heart | Dispute recourse adversarial | PASS | checks=12/12 | `docs/heart-track-dispute-recourse-adversarial-latest.json` |
| heart | Heart API signal board | PASS | freshness_status=PASS, source_count=17, apis=3 | `docs/heart-governance-signal-board-latest.json` |
| heart | Heart expansion constellation | PASS | checks=9/9 | `docs/trinity-expansion/heart-governance-constellation-board-latest.json` |
| heart | Heart readiness gate | FAIL | checks=0/2 | `docs/trinity-expansion/heart-governance-readiness-gate-latest.json` |

## Context blocks
| label | status | detail | path |
|---|---|---|---|
| API constellation board | PASS | manifest_validation_status=PASS, promotion_candidates=4 | `docs/trinity-api-constellation-board-latest.json` |
| Extension catalog validation | PASS | status extracted | `docs/trinity-extension-catalog-validation-latest.json` |
| Expansion manifest validation | PASS | status extracted | `docs/trinity-expansion-manifest-validation-latest.json` |
| Expansion result validation | PASS | status extracted | `docs/trinity-expansion-result-validation-latest.json` |
| Capability surface audit | FAIL | checks=0/2 | `docs/trinity-expansion/trinity-capability-surface-audit-latest.json` |
| Hardening release gate | FAIL | checks=8/10 | `docs/trinity-expansion/trinity-release-gate-board-latest.json` |
| Trinity supercycle gate | FAIL | checks=0/2 | `docs/trinity-expansion/trinity-supercycle-gate-latest.json` |
| Figma collaboration gate | FAIL | checks=5/6 | `docs/trinity-expansion/figma-collab-gate-latest.json` |
| Linear collaboration gate | FAIL | checks=5/6 | `docs/trinity-expansion/linear-collab-gate-latest.json` |
| Playwright ops gate | FAIL | checks=5/6 | `docs/trinity-expansion/playwright-ops-gate-latest.json` |
| GitHub devflow gate | FAIL | checks=5/6 | `docs/trinity-expansion/github-devflow-gate-latest.json` |
| Memory continuity gate | PASS | checks=5/5 | `docs/trinity-expansion/memory-continuity-gate-latest.json` |
| Operator release gate | PASS | checks=5/5 | `docs/trinity-expansion/operator-release-gate-latest.json` |
| Compute hardware gate | FAIL | checks=4/5 | `docs/trinity-expansion/compute-hardware-gate-latest.json` |
| Identity governance gate | PASS | checks=5/5 | `docs/trinity-expansion/identity-governance-gate-latest.json` |
| Public intelligence gate | FAIL | checks=4/5 | `docs/trinity-expansion/public-intelligence-gate-latest.json` |

## Evidence boundary
- verified_state: Latest suite and pillar artifacts are the current operational evidence boundary.
- watch_state: Promote only PASS-backed states; treat WARN/FAIL artifacts as live investigation targets.
- next_phase_focus: Advance new systems only when they preserve suite pass state and per-pillar traceability.
