# v470 THOS v5 x2 Rule Map Ledger

The v5 x2 rule map gives every dry-run fixture a stable `rule_map_id` and `authority_route`.

## Coverage

- Fixtures mapped: 8.
- Unmapped fixtures: 0.
- Expected failure rows: 4.
- Expected pass rows: 4.

## Rule Families

- Observe-only inventory.
- Dry validation.
- Local write shape.
- Connector mutation gate.
- Destructive cleanup guard.
- Mixed request split.
- Watcher observe-only boundary.

Expected failures are active guardrails, not defects to remove.
