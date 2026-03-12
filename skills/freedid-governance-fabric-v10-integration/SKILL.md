---
name: freedid-governance-fabric-v10-integration
description: Operate the Freed ID Governance Fabric V10 pack with explicit v10 proof-B, research, workbench, and repo-authority boundaries.
---

# Freed ID Governance Fabric V10 Integration

Use when Codex needs to work with the `freedid_governance_fabric_v10` pack.

1. Keep the Journey repo authoritative.
2. Treat Notion, Linear, Postgres, GitHub, and the New project workbench as bounded mirrors or tooling surfaces only.
3. Preserve council identity, memory, and command-scope separation.
4. Only use materialize paths for bounded live writes.
