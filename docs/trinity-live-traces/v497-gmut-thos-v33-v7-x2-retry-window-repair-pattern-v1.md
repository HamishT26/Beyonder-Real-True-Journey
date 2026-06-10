# v497 GMUT/THOS v33 v7 x2 Retry-Window Repair Pattern

- overall_status: `PASS_RETRY_WINDOW_REPAIR_PATTERN_BUILT`
- generated_utc: `2026-06-06T22:41:20Z`

## Pattern

- Symptom: background watcher starts but completion notifier remains missing.
- Diagnosis: launcher timeout may be shorter than intended lane runtime.
- Repair: retry the existing lane route with distinct receipt prefixes and a timeout aligned to the runtime target.
- Proof: retry3 completed app lanes after attempts 1 and 2 used shorter launcher windows.

Safe limits remain: no replacement siblings, no new threads, no raw transport publication, no session editing, and no account/app setting mutation.
