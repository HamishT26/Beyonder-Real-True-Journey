# v141-v160 v2 Alpha Security Cleanup Board v1

- Security posture: repository-scoped Alpha gate.
- External spend: 0.
- Provider mutations: 0.
- Google Drive state: `operator_hold`.

## Key Boundaries

- Operator prompts versus repo-backed evidence.
- Repo artifacts versus external mirrors.
- Read-only CLI consultation versus mutation authority.
- Local validation versus paid provider live writes.
- Candidate systems versus promoted manifest systems.

## Cleanup Candidates

- Keep carried-forward dirty worktree changes unstaged unless allowlisted.
- Exclude raw CLI logs, auth HTML, analytics 403 output, and MCP shutdown warnings.
- Repair malformed skill frontmatter in a later scoped cleanup pack.
- Avoid deleting or merging system manifests without a reversible allowlist.
