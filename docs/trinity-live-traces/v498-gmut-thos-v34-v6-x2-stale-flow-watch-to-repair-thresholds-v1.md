# v498 GMUT/THOS v34 v6 x2 Stale-Flow Watch-to-Repair Thresholds

- generated_utc: `2026-06-07T03:11:20Z`
- overall_status: `PASS_THRESHOLDS_BUILT`

## Thresholds

- Sqlite startup slow warning: watch; repair after three consecutive phase launches where startup slowness correlates with missing or delayed final artifacts.
- Prompt-length loader warning: watch; repair if the prompt fails to load, a lane refuses current phase, or launch receipt becomes incomplete.
- Curated plugin marketplace cache warning: watch; repair if an approved plugin capability becomes unavailable for a required task.
- Generic marker count with strict marker count zero: review; repair if strict quality marker count becomes nonzero or raw output boundary is not temp-only.
- Unredacted app thread ID: repair before publication; always redact before staging.
