# v468A THOS v1 x2 Schema Card Set

Prepared: 2026-06-01T23:18:00+12:00.

This card set materializes the x1 taxonomy into eight concrete THOS schemas: phase manifest, live-write gate, command surface, skill registry, plugin/API/MCP inventory, blocker ledger, source refresh, and run status.

The core rule is explicit state over implied power. Every card must say what surface it touches, what proof is required, what mutation class applies, and which claim locks remain active. Live-write connector use, destructive cleanup, or Drive mutation must not occur through naming alone; it needs a separate approval record and a receipt.

Run-status validation stays conservative: JSON parse, sensitive/path/session-capture guard, trailing-whitespace check, staged diff review, curated staging, commit, push, and remote equality are the only publication proof claims in this phase.
