# Body Track Policy-Update Trial Design v0

Purpose: define **one selective policy-update trial** so we can run a recommended threshold/profile change, measure the observed false-alert rate, and publish **accepted vs rejected** deltas (before/after).

---

## Trial protocol

1. **Read** latest calibration output: `docs/body-track-calibration-latest.json` (from `body_profile_calibration_report.py`).
2. **Extract** `policy_delta_analysis`: `current_policy`, `recommended_policy`, `false_alert_before_after`, `apply_recommendation_candidate`.
3. **Choose one** policy dimension for the trial (e.g. `benchmark_profile` only for trial 1).
4. **Run** Body track with the **recommended** profile for that dimension (e.g. run `body_track_runner.py --benchmark-profile <recommended_benchmark_profile>` one or more times).
5. **Record** observed false-alert contribution (or pass/warn outcome) over the run(s).
6. **Publish** a trial record: `trial_id`, `generated_utc`, `policy_applied`, `expected_after` (from calibration), `observed_after`, `delta_status`: `accepted` if observed improves or matches expectation, `rejected` otherwise.

---

## Worked example (trial 1: benchmark profile)

- **Input:** Calibration report with `recommended_policy.benchmark_profile` = e.g. `standard`, `false_alert_before_after.benchmark_before` = 0.12, `benchmark_after` = 0.08.
- **Action:** Run body runner with `--benchmark-profile standard` for N runs (or one run and infer from pass/warn).
- **Record:** `observed_benchmark_after` = measured false-alert rate over those runs; if `observed_benchmark_after <= benchmark_after + tolerance` then `delta_status: accepted`, else `rejected`.
- **Publish:** Append one line to `docs/body-track-policy-trials.jsonl` with the trial payload.

---

## Trial record schema (v0)

| Field | Type | Description |
|-------|------|-------------|
| trial_id | string | Unique id, e.g. `trial-20260217-001`. |
| generated_utc | string | ISO8601 UTC. |
| policy_dimension | string | `benchmark_profile`, `trend_profile`, or `regression_window`. |
| recommended_value | object | The recommended value (string or dict). |
| expected_before | float | False-alert rate before (from calibration). |
| expected_after | float | False-alert rate after (from calibration). |
| observed_after | float \| null | Measured rate after applying recommendation; null until run. |
| delta_status | string | `accepted`, `rejected`, or `pending` (if observed_after is null). |

---

## Script

- **scripts/body_policy_trial_one.py** — Reads `docs/body-track-calibration-latest.json`, builds one trial record from `policy_delta_analysis`, appends to `docs/body-track-policy-trials.jsonl`. Sets `observed_after: null` and `delta_status: pending` so a future run (or manual step) can fill observed and set accepted/rejected.

---

## References

- `scripts/body_profile_calibration_report.py`: `_build_policy_delta_analysis`, output schema.
- `body_track_runner.py`: `--benchmark-profile`, `BENCHMARK_PROFILES`.
- Coordination next step: "run selective policy-update trials and publish accepted vs rejected recommendation deltas."

---

*Caelis · Session 4 · 2026-02-17 · Body track advancement*
