# v507 GMUT/THOS v43 v1 x2 Multiplex Route-State Extension v1

Generated: 2026-06-11T08:15:31Z

Status: ROUTE_STATE_EXTENSION_READY

## Purpose

This extends the Local GHC Multiplex IPC bus with explicit live-adapter route states so v507-v515 phases can distinguish prepared prompts, sent messages, active generation, completion, blockers, and sanitized synthesis.

## Route States

- `prepared`: prompt or route card exists but has not been sent.
- `sent`: message was submitted to the intended lane.
- `generating`: lane is visibly producing or processing a response.
- `complete`: completion marker or explicit completion signal is observed.
- `blocker`: bounded blocker receipt explains why the lane cannot complete.
- `synthesized`: sanitized synthesis or blocker synthesis has been recorded.

## Required Transitions

- `prepared -> sent`
- `sent -> generating`
- `generating -> complete`
- `generating -> blocker`
- `complete -> synthesized`
- `blocker -> synthesized`

## Required Receipt Fields

- Phase.
- Lane.
- Surface.
- State.
- Generated UTC timestamp.
- Marker expected.
- Marker observed.
- Raw boundary.
- Next action.

## Boundary

This extension starts no daemon and performs no external mutation. It forbids raw response bodies, raw transcript bodies, credential material, browser hidden state, screenshot payloads, and session stream payloads in public receipts.

All GMUT, canon, empirical, legal, and consciousness gates remain open.
