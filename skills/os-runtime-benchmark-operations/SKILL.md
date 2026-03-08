---
name: os-runtime-benchmark-operations
description: Operate the OS Runtime Benchmark Operations pack with explicit cache-backed promotion boundaries.
---

# OS Runtime Benchmark Operations

Use when Codex needs to work with the `os_runtime_benchmark` pack.

## Workflow
1. Read `docs/os-runtime-benchmark-contract-v1.json` and `docs/os-runtime-benchmark-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/os-runtime-benchmark-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
