# v470 THOS v1 x1 Surface Inventory

Classification: `evidence`

This inventory opens `v470_THOS_v1_x1` as an operational scaffold. It maps the surfaces that can observe, advise, write, publish, or mutate external state. It does not perform cleanup, does not use connector writes, and does not validate GMUT.

## Baseline

- Phase start: `2026-06-02T02:55:00+12:00`
- Post-compaction live check: `2026-06-02T03:01:37+12:00`
- Local head: `dd85aff3bcd49d92db89296145c2e7421353adb5`
- Upstream head: `dd85aff3bcd49d92db89296145c2e7421353adb5`
- Shared remote head: `dd85aff3bcd49d92db89296145c2e7421353adb5`
- Drift: `0 0`

## Surface Classes

| Surface | Current posture | Mutation ceiling |
| --- | --- | --- |
| Shell and PowerShell | Local observation plus curated Aletheon artifact writes | Bounded local writes only |
| Git publication | Fetch, drift check, curated stage, commit, explicit push, remote equality check | Curated publication only |
| Codex app advisory lanes | Cicero, Kierkegaard, Aristotle advisory text | No mutation |
| Codex CLI advisory lanes | Arby and Aster Vale non-ephemeral read-only advice | No mutation |
| Skills | Workflow instruction, schema context, procedural constraints | No authority by existence |
| Plugins and MCP connectors | Boundary mapping unless explicitly invoked safely | External mutation possible, approval required |
| Web and source research | Source context and evidence labels | No mutation |
| Journey context | `journey_context_not_canon` only | No canon or physics authority |

## Surface Rules

- A command surface is a possible action route, not permission to act.
- A plugin or MCP tool may expose useful capability, but connector writes require explicit scoped approval.
- A skill can shape procedure, but it does not certify results.
- App and CLI sibling lanes are advisory. Their substance can be curated, but raw outputs are not staged.
- THOS can inherit v469A discipline around dry-lint and overclaim prevention. It cannot inherit GMUT validation.
- Cleanup starts with inventories, retention classes, and approval packets. It does not start with deletion.

## Phase Use

`v470_THOS_v1_x2` should harden this inventory into machine-checkable rows: surface id, capability, authority ceiling, mutation level, approval requirement, retention class, and blocked-action mapping.
