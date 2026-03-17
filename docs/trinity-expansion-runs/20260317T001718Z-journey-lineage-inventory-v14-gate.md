# Trinity Expansion Result: journey_lineage_inventory_v14_gate

- generated_utc: `2026-03-17T00:17:18+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/journey-lineage-inventory-v14-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/journey-lineage-inventory-v14-sync-bridge-latest.json | FAIL | missing artifact: docs/trinity-expansion/journey-lineage-inventory-v14-sync-bridge-latest.json |
| dependency:docs/trinity-expansion/journey-lineage-inventory-v14-materialization-tracer-latest.json | FAIL | missing artifact: docs/trinity-expansion/journey-lineage-inventory-v14-materialization-tracer-latest.json |
| dependency:docs/trinity-expansion/journey-lineage-inventory-v14-cache-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/journey-lineage-inventory-v14-cache-board-latest.json |
| dependency:docs/trinity-expansion/journey-lineage-inventory-v14-risk-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/journey-lineage-inventory-v14-risk-board-latest.json |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "journey_lineage_inventory_v14",
  "pass_like_dependencies": 1
}
```

## Repo targets touched
- `docs/trinity-mcp-cache/journey-lineage-inventory-v14-latest.json`
- `docs/v14-trinity-verdict-v1.json`
- `docs/v29-v38-legacy-reconstruction-map-v1.json`
- `docs/version-module-inventory-v1.json`
