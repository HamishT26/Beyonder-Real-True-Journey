# v477 THOS v5 x2 Observability Schema

- purpose: standardize future app and CLI watcher receipts.

## Fields
- phase: ties a receipt to one phase-version session
- lane: identifies advisory lane without publishing message text
- run_id: links start, watcher, and completion receipts
- trace_id: stable row-level correlation key
- generated_utc: unambiguous clock source
- status: machine-readable final state
- final_state_reason: explains completion or open gap
- retry_window_seconds: records patience budget
- timeout_reason: separates no-signal, partial-signal, and active-turn blockers
- payload_publication: documents status-only publication boundary
- gmut_gate_state: keeps physics-claim gates visibly open

## Invariants
- No unfiltered event stream is published.
- No local machine-specific filesystem address is required in reader-facing artifacts.
- Existing lanes only; no replacement agent creation.
- All GMUT gates stay open unless exact closure artifacts exist.
