# v545 GMUT/THOS v81 v1 x1 Lumen Browser Route Prep

Generated NZ: `2026-06-17T14:38:00+12:00`

Status: `READY_AFTER_V544_V8_X2_CLOSEOUT`

This is a prep card only. It does not claim that v545 has started. It prepares the Lumen solo Browser route for the next round-robin step after v544 v8 x1 and v544 v8 x2 close cleanly.

## Route Preference

- Use the in-app Browser current ChatGPT panel first.
- Refresh the Browser tab if the branched Lumen panel is stale or visually stuck.
- Use Browser developer-mode/CDP only if the Browser runtime exposes it.
- Do not switch to Chrome unless a later exact fallback condition is met.

## Five-Step Retry Ladder

- Attempt 1: Read visible state, locate the composer, type/send from the current Browser panel.
- Attempt 2: Refresh the Browser tab, re-read visible state, and retry send.
- Attempt 3: Use DOM locator fallback for the composer and send control.
- Attempt 4: Use keyboard fallback with the focused composer.
- Attempt 5: Publish a status-only blocker receipt and ask Hamish for manual refresh if Browser remains blocked.

## Lumen Prompt Shape

- Minimum runtime target: 5 minutes, with longer reasoning welcome.
- Expected marker: `LUMEN_V545_V1_X1_ADVISORY_COMPLETE`.
- Ask for current-state confirmation, omega-mini lookup sanity, 20+ approval/eureka candidates, x2 build/run/test/use priorities, open-gate audit, and route-health advice.

## Boundary

No raw Lumen reply, raw Browser URL, raw route handle, screenshots, credentials, local absolute paths, final physics, consciousness proof, legal closure, canon promotion, or GMUT empirical closure is published here.
