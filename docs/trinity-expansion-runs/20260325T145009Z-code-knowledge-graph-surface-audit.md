# Trinity Expansion Result: code_knowledge_graph_surface_audit

- generated_utc: `2026-03-25T14:50:09+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| pack_contract_present | PASS | docs/code-knowledge-graph-contract-v1.json |
| pack_fixture_present | PASS | docs/code-knowledge-graph-fixture-v1.json |
| pack_workflow_present | PASS | docs/code-knowledge-graph-workflow-v1.md |
| pack_catalog_entry_present | PASS | docs/code-knowledge-graph-catalog-entry-v1.json |
| manifest_pack_system_count | PASS | pack=code_knowledge_graph |
| extension_catalog_pack_count | PASS | extensions=12 |
| mcp_connector_present | PASS | postgres |
| mcp_status_expected | PASS | status=verified_live_write, actual_state=verified_live_write, expected=verified_live_write |

## Metrics
```json
{
  "extension_count": 12,
  "gating_class": "verified_live_write",
  "pack": "code_knowledge_graph",
  "strategy": "local_probe"
}
```

## Repo targets touched
- `docs/code-knowledge-graph-catalog-entry-v1.json`
- `docs/code-knowledge-graph-contract-v1.json`
- `docs/code-knowledge-graph-fixture-v1.json`
- `docs/code-knowledge-graph-workflow-v1.md`
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-expansion/code-knowledge-graph-sync-bridge-latest.json`
