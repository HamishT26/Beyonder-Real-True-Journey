# v470 THOS v2 x1 Command Surface Registry Template

Classification: `evidence`

This template turns the x2 schema into a practical command registry. It is a template only: no command is executed by this artifact.

## Required Fields

| Field | Purpose |
| --- | --- |
| `command_id` | Stable row id. |
| `command_pattern` | Command or family being classified. |
| `intent` | Why it would be used. |
| `cwd_scope` | Intended workspace or path scope. |
| `surface_class` | Shell, git, validator, artifact, connector, or unknown. |
| `mutation_level` | Read-only, local write, git mutation, external mutation, destructive, or unknown. |
| `approval_policy` | None for read-only, explicit required, or blocked in advisory. |
| `allowed_in_advisory` | Boolean guard. |
| `allowed_in_dirty_worktree` | Whether dirty state changes the permission. |
| `source_authority` | Local artifact, tool output, advisory, or open gap. |
| `retention_class` | Publication and retention handling. |
| `safe_output_claim` | The strongest allowed wording. |

## Safety Rules

- Every command declares cwd scope before execution.
- Read-only commands cannot expose sensitive values.
- No deletion or recursive cleanup from advisory lanes.
- No reset, rebase, force push, overwrite checkout, or broad restore.
- No staging, commit, or push from advisory-only scope.
- Connector writes require a scoped approval packet.
- Generated reports must label observed, inferred, or advisory status.
- THOS command checks cannot be described as GMUT validation.

Rows can be `PASS_SHAPE_ONLY` only when read-only or explicitly blocked.
