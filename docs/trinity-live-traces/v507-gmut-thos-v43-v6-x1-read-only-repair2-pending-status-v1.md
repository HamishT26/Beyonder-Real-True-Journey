# v507 GMUT/THOS v43 v6 x1 Read-Only Repair2 Pending Status

- overall_status: `OPEN_GAP_ARBY_READ_ONLY_REPAIR2_PENDING`
- lane: `Arby`
- repair attempt: `repair2`
- read-only permissions authorized: `true`
- writes authorized: `false`
- raw output publication authorized: `false`
- final message ready: `false`
- next_phase_allowed: `false`

Arby repair2 is now running under the updated read-only authorization. The watcher receipt is status-only, and raw output remains temp-only. v507 v6 x1 stays open until Arby repair2 produces a clean final message and passes the elaboration gate, or a clean blocker receipt replaces it.
