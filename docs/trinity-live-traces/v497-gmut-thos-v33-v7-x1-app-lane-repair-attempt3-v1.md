# v497 GMUT/THOS v33 v7 x1 App-Lane Repair Attempt 3

- overall_status: `PASS_RETRY3_LONG_WATCHER_STARTED`
- generated_utc: `2026-06-06T22:13:40Z`
- phase_advance_allowed: `false`

## Attempts

- Attempt 1: open gap; background watcher started but lower-level launcher timed out before completion notifier appeared.
- Attempt 2: open gap; retry2 repeated the short launcher-timeout failure shape.
- Attempt 3: background watch started; retry3 uses a long launcher timeout aligned to the one-hour app-lane target.

## Repair

Root-cause hypothesis: attempts 1 and 2 used a launcher timeout too short for long app-lane work. Retry3 keeps the existing app watcher route, uses distinct retry3 receipt prefixes, and extends the launcher timeout instead of creating any replacement sibling or new thread.

Next app retry check is not before `2026-06-06T22:27:25Z`.

No raw transport, raw lane text, new threads, old-style spawning, GMUT closure, or canon promotion is claimed.
