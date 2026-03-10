---
name: compute-hardware-integration
description: Operate the Compute Hardware pack with cache-backed gating and explicit connector boundaries.
---

# Compute Hardware Integration

Use when Codex needs to work with the `compute_hardware` pack.

## Workflow
1. Read `docs/compute-hardware-contract-v1.json` and `docs/compute-hardware-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/compute-hardware-latest.json.`
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative or comparison docs.
