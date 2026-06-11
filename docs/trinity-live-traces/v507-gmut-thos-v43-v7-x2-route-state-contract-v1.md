# v507 GMUT/THOS v43 v7 x2 Route State Contract

Generated UTC: `2026-06-11T15:20:34Z`

Status: `PREPARED_ROUTE_STATE_CONTRACT`

## States

- `prepared`
- `sent`
- `generating`
- `complete`
- `blocker`
- `synthesized`

## Transitions

- `prepared -> sent`: message is submitted through the approved route only.
- `sent -> generating`: lane work is observed or inferred from status-safe UI state.
- `generating -> complete`: assistant final marker is verified outside prompt echo.
- `generating -> blocker`: bounded retries fail or route is unavailable.
- `complete -> synthesized`: status-only metrics and advisory synthesis are recorded.
- `blocker -> synthesized`: blocker receipt is recorded without creating replacement siblings.

## Boundary

No raw lane text, raw transcript body, response body, credentials, screenshots, session streams, or local private paths are published. GMUT and canon gates remain open.
